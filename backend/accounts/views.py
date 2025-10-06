"""
Account-related API views.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import AllowAnyPermission
from rest_framework.response import Response
from django.contrib.auth import logout
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserProfileSerializer, UserProfileUpdateSerializer, LoginResponseSerializer,
    RefreshTokenSerializer
)
from .authentication import generate_tokens, revoke_all_user_tokens


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def test_endpoint(request):
    """
    Test endpoint to verify API is working.
    """
    return Response({
        'success': True,
        'message': 'API is working!',
        'method': request.method,
        'data': request.data if request.method == 'POST' else None,
        'user': str(request.user) if hasattr(request, 'user') else 'Anonymous',
        'authenticated': request.user.is_authenticated if hasattr(request, 'user') else False
    }, status=200)


@api_view(['POST'])
@permission_classes([AllowAnyPermission])
def register(request):
    """
    Register a new user.
    """
    print(f"Registration request data: {request.data}")
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            first_name=user.first_name or "",
            last_name=user.last_name or ""
        )
        
        # Generate tokens
        tokens = generate_tokens(user)
        
        # Prepare response in expected format
        response_data = {
            'success': True,
            'data': {
                'user': UserSerializer(user).data,
                'tokens': tokens
            },
            'message': 'Registration successful'
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    print(f"Validation errors: {serializer.errors}")
    return Response({
        'success': False,
        'error': 'Validation failed',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAnyPermission])
def login(request):
    """
    Authenticate user and return tokens.
    """
    print(f"Login request data: {request.data}")
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Generate tokens
        tokens = generate_tokens(user)
        
        # Prepare response in expected format
        response_data = {
            'success': True,
            'data': {
                'user': UserSerializer(user).data,
                'tokens': tokens
            },
            'message': 'Login successful'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'error': 'Authentication failed',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout user and revoke tokens.
    """
    # Revoke all user tokens
    revoke_all_user_tokens(request.user)
    
    # Django logout (using django.contrib.auth.logout)
    from django.contrib.auth import logout as django_logout
    django_logout(request)
    
    return Response({
        'success': True,
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    Refresh access token using refresh token.
    """
    serializer = RefreshTokenSerializer(data=request.data)
    
    if serializer.is_valid():
        tokens = serializer.validated_data['refresh']
        return Response({
            'success': True,
            'data': tokens,
            'message': 'Token refreshed successfully'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'error': 'Token refresh failed',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get current user profile.
    """
    try:
        profile = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update user profile.
    """
    try:
        profile = request.user.profile
        serializer = UserProfileUpdateSerializer(profile, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            # Return updated profile with flat structure
            profile_serializer = UserProfileSerializer(request.user.profile)
            return Response({
                'success': True,
                'data': profile_serializer.data,
                'message': 'Profile updated successfully'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'error': 'Validation failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except UserProfile.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_profile(request):
    """
    Mark profile as complete.
    """
    try:
        profile = request.user.profile
        profile.is_profile_complete = True
        profile.save()
        
        return Response(
            {'message': 'Profile marked as complete'}, 
            status=status.HTTP_200_OK
        )
    
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'Profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    Get current user information.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)