"""
Verification-related API views.
"""
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from accounts.models import User, UserProfile
from documents.models import DocumentRecord
from .models import VerificationRequest, VerificationResult, VerificationLog
from .serializers import (
    DocumentVerificationSerializer, VerificationResponseSerializer,
    VerificationRequestSerializer, VerificationResultSerializer,
    VerificationLogSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow public verification
def verify_document(request):
    """
    Verify document authenticity.
    """
    serializer = DocumentVerificationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': 'Validation failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    emp_id = serializer.validated_data['emp_id']
    doc_hash = serializer.validated_data['doc_hash']
    
    # Create verification request
    verification_request = VerificationRequest.objects.create(
        emp_id=emp_id,
        doc_hash=doc_hash,
        requested_by=request.user if request.user.is_authenticated else None,
        request_ip=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT')
    )
    
    # Log verification attempt
    VerificationLog.objects.create(
        verification_request=verification_request,
        action='verification_attempt',
        details=f"Verification requested for emp_id: {emp_id}, doc_hash: {doc_hash}",
        performed_by=request.user if request.user.is_authenticated else None,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    try:
        # Find user by employee ID
        try:
            user = User.objects.get(emp_id=emp_id)
        except User.DoesNotExist:
            verification_request.mark_failed("Employee not found")
            return Response({
                'is_valid': False,
                'message': 'Employee not found',
                'verification_date': verification_request.verification_date
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user has a profile
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            verification_request.mark_failed("Employee profile not found")
            return Response({
                'is_valid': False,
                'message': 'Employee profile not found',
                'verification_date': verification_request.verification_date
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if profile has original document hash
        if not profile.doc_hash:
            verification_request.mark_failed("No original document found for employee")
            return Response({
                'success': False,
                'error': 'No original document found for employee',
                'data': {
                    'isValid': False,
                    'message': 'No original document found for employee',
                    'verificationDate': verification_request.verification_date
                }
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Compare document hashes
        if profile.doc_hash != doc_hash:
            verification_request.mark_failed("Document hash does not match original")
            return Response({
                'success': True,
                'data': {
                    'isValid': False,
                    'message': 'Document is tampered or not the original',
                    'verificationDate': verification_request.verification_date
                },
                'message': 'Document verification completed'
            }, status=status.HTTP_200_OK)
        
        # Document is valid
        verification_request.mark_verified("Document verified successfully")
        
        # Create verification result
        result = VerificationResult.objects.create(
            verification_request=verification_request,
            employee_details={
                'emp_id': user.emp_id,
                'user_hash': user.user_hash,
                'email': user.email,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'job_designation': profile.job_designation,
                'department': profile.department,
                'is_profile_complete': profile.is_profile_complete
            },
            document_preview_url=f"/api/documents/preview/{doc_hash}/",
            download_url=f"/api/documents/download/{doc_hash}/",
            verification_metadata={
                'verified_at': timezone.now().isoformat(),
                'verification_method': 'hash_comparison',
                'original_doc_hash': profile.doc_hash
            }
        )
        
        # Log successful verification
        VerificationLog.objects.create(
            verification_request=verification_request,
            action='verification_success',
            details=f"Document verified successfully for {user.emp_id}",
            performed_by=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response({
            'success': True,
            'data': {
                'isValid': True,
                'message': 'Document verified successfully',
                'employeeDetails': result.employee_details,
                'documentPreview': result.document_preview_url,
                'downloadLink': result.download_url,
                'verificationDate': verification_request.verification_date
            },
            'message': 'Document verification completed successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        verification_request.mark_failed(f"Verification failed: {str(e)}")
        
        # Log error
        VerificationLog.objects.create(
            verification_request=verification_request,
            action='verification_error',
            details=f"Verification failed: {str(e)}",
            performed_by=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response({
            'success': False,
            'error': 'Verification failed due to server error',
            'data': {
                'isValid': False,
                'message': 'Verification failed due to server error',
                'verificationDate': verification_request.verification_date
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verification_status(request, emp_id):
    """
    Get verification status for an employee.
    """
    try:
        user = User.objects.get(emp_id=emp_id)
        verifications = VerificationRequest.objects.filter(emp_id=emp_id)
        
        serializer = VerificationRequestSerializer(verifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response(
            {'error': 'Employee not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verification_logs(request, verification_id):
    """
    Get verification logs for a specific verification request.
    """
    try:
        verification_request = VerificationRequest.objects.get(id=verification_id)
        logs = VerificationLog.objects.filter(verification_request=verification_request)
        
        serializer = VerificationLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except VerificationRequest.DoesNotExist:
        return Response(
            {'error': 'Verification request not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_verifications(request):
    """
    Get current user's verification requests.
    """
    verifications = VerificationRequest.objects.filter(requested_by=request.user)
    serializer = VerificationRequestSerializer(verifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)