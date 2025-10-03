"""
Issuer-related API views.
"""
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import User, UserProfile
from .models import Issuer, IssuerAuthorization, IssuerAccessLog, IssuerSettings
from .serializers import (
    IssuerSerializer, IssuerAuthorizationSerializer,
    IssuerAuthorizationRequestSerializer, IssuerAccessLogSerializer,
    IssuerSettingsSerializer, EmployeeDetailsSerializer
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def authorize_employee(request):
    """
    Authorize an employee for document access.
    """
    serializer = IssuerAuthorizationRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': 'Validation failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    emp_id = serializer.validated_data['emp_id']
    user_hash = serializer.validated_data['user_hash']
    reason = serializer.validated_data.get('reason', '')
    
    # Find employee
    try:
        employee = User.objects.get(emp_id=emp_id, user_hash=user_hash)
    except User.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Employee not found with provided credentials'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Get or create issuer (for now, create a default issuer)
    issuer, created = Issuer.objects.get_or_create(
        issuer_id=f"ISSUER_{request.user.id}",
        defaults={
            'name': f"Issuer {request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
            'company': 'BlockHire System'
        }
    )
    
    # Check if authorization already exists
    authorization, created = IssuerAuthorization.objects.get_or_create(
        issuer=issuer,
        emp_id=emp_id,
        user_hash=user_hash,
        defaults={
            'employee': employee,
            'created_by': request.user,
            'reason': reason
        }
    )
    
    if not created:
        return Response({
            'success': False,
            'error': 'Employee already authorized'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Auto-approve if issuer settings allow
    try:
        settings = issuer.settings
        if settings.auto_approve:
            authorization.approve("Auto-approved by issuer settings")
    except IssuerSettings.DoesNotExist:
        # Create default settings
        IssuerSettings.objects.create(
            issuer=issuer,
            auto_approve=False
        )
    
    # Log authorization
    IssuerAccessLog.objects.create(
        issuer=issuer,
        action='authorize',
        emp_id=emp_id,
        user_hash=user_hash,
        details=f"Authorization request created for {emp_id}",
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT')
    )
    
    response_serializer = IssuerAuthorizationSerializer(authorization)
    return Response({
        'success': True,
        'data': response_serializer.data,
        'message': 'Employee authorized successfully'
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_employee_details(request):
    """
    Get employee details for verification.
    """
    serializer = IssuerAuthorizationRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': 'Validation failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    emp_id = serializer.validated_data['emp_id']
    user_hash = serializer.validated_data['user_hash']
    
    # Find employee
    try:
        employee = User.objects.get(emp_id=emp_id, user_hash=user_hash)
    except User.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Employee not found with provided credentials'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check if employee has profile
    try:
        profile = employee.profile
    except UserProfile.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Employee profile not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check authorization
    issuer, _ = Issuer.objects.get_or_create(
        issuer_id=f"ISSUER_{request.user.id}",
        defaults={
            'name': f"Issuer {request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
            'company': 'BlockHire System'
        }
    )
    
    try:
        authorization = IssuerAuthorization.objects.get(
            issuer=issuer,
            emp_id=emp_id,
            user_hash=user_hash
        )
        
        if not authorization.permission_granted:
            return Response({
                'success': False,
                'error': 'Employee not authorized'
            }, status=status.HTTP_403_FORBIDDEN)
    except IssuerAuthorization.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Employee not authorized'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Log access
    IssuerAccessLog.objects.create(
        issuer=issuer,
        action='view_profile',
        emp_id=emp_id,
        user_hash=user_hash,
        details=f"Employee details accessed for {emp_id}",
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT')
    )
    
    # Prepare response data in camelCase for frontend compatibility
    response_data = {
        'empId': employee.emp_id,
        'userHash': employee.user_hash,
        'email': employee.email,
        'firstName': profile.first_name,
        'lastName': profile.last_name,
        'jobDesignation': profile.job_designation,
        'department': profile.department,
        'isProfileComplete': profile.is_profile_complete,
        'hasOriginalDocument': bool(profile.doc_hash),
        'createdAt': employee.created_at,
        'updatedAt': employee.updated_at
    }
    
    return Response({
        'success': True,
        'data': response_data,
        'message': 'Employee details retrieved successfully'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authorized_employees(request):
    """
    Get list of authorized employees for current issuer.
    """
    issuer, _ = Issuer.objects.get_or_create(
        issuer_id=f"ISSUER_{request.user.id}",
        defaults={
            'name': f"Issuer {request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
            'company': 'BlockHire System'
        }
    )
    
    authorizations = IssuerAuthorization.objects.filter(
        issuer=issuer,
        permission_granted=True
    )
    
    serializer = IssuerAuthorizationSerializer(authorizations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def revoke_authorization(request, emp_id):
    """
    Revoke authorization for an employee.
    """
    issuer, _ = Issuer.objects.get_or_create(
        issuer_id=f"ISSUER_{request.user.id}",
        defaults={
            'name': f"Issuer {request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
            'company': 'BlockHire System'
        }
    )
    
    try:
        authorization = IssuerAuthorization.objects.get(
            issuer=issuer,
            emp_id=emp_id
        )
        
        authorization.revoke("Revoked by issuer")
        
        # Log revocation
        IssuerAccessLog.objects.create(
            issuer=issuer,
            action='revoke_access',
            emp_id=emp_id,
            details=f"Authorization revoked for {emp_id}",
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return Response(
            {'message': 'Authorization revoked successfully'}, 
            status=status.HTTP_200_OK
        )
        
    except IssuerAuthorization.DoesNotExist:
        return Response(
            {'error': 'Authorization not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def access_logs(request):
    """
    Get access logs for current issuer.
    """
    issuer, _ = Issuer.objects.get_or_create(
        issuer_id=f"ISSUER_{request.user.id}",
        defaults={
            'name': f"Issuer {request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
            'company': 'BlockHire System'
        }
    )
    
    logs = IssuerAccessLog.objects.filter(issuer=issuer)
    serializer = IssuerAccessLogSerializer(logs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def issuer_settings(request):
    """
    Get or update issuer settings.
    """
    issuer, _ = Issuer.objects.get_or_create(
        issuer_id=f"ISSUER_{request.user.id}",
        defaults={
            'name': f"Issuer {request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
            'company': 'BlockHire System'
        }
    )
    
    settings, created = IssuerSettings.objects.get_or_create(issuer=issuer)
    
    if request.method == 'GET':
        serializer = IssuerSettingsSerializer(settings)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = IssuerSettingsSerializer(settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)