"""
JWT Authentication for BlockHire API.
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import JWTToken

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication class.
    """
    
    def authenticate(self, request):
        """
        Authenticate the request using JWT token.
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        print(f"JWT Auth - Header: {auth_header}")
        
        if not auth_header or not auth_header.startswith('Bearer '):
            print("JWT Auth - No valid auth header")
            return None
            
        token = auth_header.split(' ')[1]
        print(f"JWT Auth - Token: {token[:20]}...")
        
        try:
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET_KEY, 
                algorithms=['HS256']
            )
            print(f"JWT Auth - Payload: {payload}")
            
            user_id = payload.get('user_id')
            if not user_id:
                print("JWT Auth - No user_id in payload")
                raise AuthenticationFailed('Invalid token payload')
                
            try:
                user = User.objects.get(id=user_id)
                print(f"JWT Auth - User found: {user.email}")
            except User.DoesNotExist:
                print("JWT Auth - User not found")
                raise AuthenticationFailed('User not found')
                
            # Check if token is revoked
            if JWTToken.objects.filter(
                user=user, 
                token=token, 
                is_revoked=True
            ).exists():
                print("JWT Auth - Token revoked")
                raise AuthenticationFailed('Token has been revoked')
                
            print("JWT Auth - Authentication successful")
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            print("JWT Auth - Token expired")
            # For expired tokens, return None instead of raising exception
            # This allows the view to handle the case where no authentication is required
            return None
        except jwt.InvalidTokenError:
            print("JWT Auth - Invalid token")
            # For invalid tokens, return None instead of raising exception
            return None
        except Exception as e:
            print(f"JWT Auth - Exception: {str(e)}")
            # For other exceptions, return None instead of raising exception
            return None


def generate_tokens(user):
    """
    Generate access and refresh tokens for a user.
    """
    now = datetime.utcnow()
    
    # Access token payload
    access_payload = {
        'user_id': user.id,
        'email': user.email,
        'emp_id': user.emp_id,
        'user_hash': user.user_hash,
        'type': 'access',
        'iat': now,
        'exp': now + timedelta(seconds=settings.JWT_ACCESS_TOKEN_LIFETIME)
    }
    
    # Refresh token payload
    refresh_payload = {
        'user_id': user.id,
        'type': 'refresh',
        'iat': now,
        'exp': now + timedelta(seconds=settings.JWT_REFRESH_TOKEN_LIFETIME)
    }
    
    # Generate tokens
    access_token = jwt.encode(
        access_payload, 
        settings.JWT_SECRET_KEY, 
        algorithm='HS256'
    )
    
    refresh_token = jwt.encode(
        refresh_payload, 
        settings.JWT_SECRET_KEY, 
        algorithm='HS256'
    )
    
    # Store refresh token in database
    from django.utils import timezone as django_timezone
    JWTToken.objects.create(
        user=user,
        token=refresh_token,
        expires_at=django_timezone.now() + timedelta(seconds=settings.JWT_REFRESH_TOKEN_LIFETIME)
    )
    
    return {
        'access': access_token,
        'refresh': refresh_token,
        'access_expires_in': settings.JWT_ACCESS_TOKEN_LIFETIME,
        'refresh_expires_in': settings.JWT_REFRESH_TOKEN_LIFETIME
    }


def refresh_access_token(refresh_token):
    """
    Generate new access token using refresh token.
    """
    try:
        payload = jwt.decode(
            refresh_token, 
            settings.JWT_SECRET_KEY, 
            algorithms=['HS256']
        )
        
        if payload.get('type') != 'refresh':
            raise AuthenticationFailed('Invalid token type')
            
        user_id = payload.get('user_id')
        if not user_id:
            raise AuthenticationFailed('Invalid token payload')
            
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
            
        # Check if refresh token exists and is not revoked
        try:
            token_obj = JWTToken.objects.get(
                user=user, 
                token=refresh_token, 
                is_revoked=False
            )
            
            if token_obj.is_expired:
                raise AuthenticationFailed('Refresh token has expired')
                
        except JWTToken.DoesNotExist:
            raise AuthenticationFailed('Invalid refresh token')
            
        # Generate new access token
        now = datetime.utcnow()
        access_payload = {
            'user_id': user.id,
            'email': user.email,
            'emp_id': user.emp_id,
            'user_hash': user.user_hash,
            'type': 'access',
            'iat': now,
            'exp': now + timedelta(seconds=settings.JWT_ACCESS_TOKEN_LIFETIME)
        }
        
        access_token = jwt.encode(
            access_payload, 
            settings.JWT_SECRET_KEY, 
            algorithm='HS256'
        )
        
        return {
            'access': access_token,
            'access_expires_in': settings.JWT_ACCESS_TOKEN_LIFETIME
        }
        
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Refresh token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid refresh token')
    except Exception as e:
        raise AuthenticationFailed(f'Token refresh failed: {str(e)}')


def revoke_token(token):
    """
    Revoke a JWT token.
    """
    try:
        token_obj = JWTToken.objects.get(token=token)
        token_obj.is_revoked = True
        token_obj.save()
        return True
    except JWTToken.DoesNotExist:
        return False


def revoke_all_user_tokens(user):
    """
    Revoke all tokens for a user.
    """
    JWTToken.objects.filter(user=user, is_revoked=False).update(is_revoked=True)
