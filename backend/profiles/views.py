"""
Profile-related API views.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import UserProfile
from .serializers import (
    UserProfileSerializer, UserProfileUpdateSerializer,
    ProfileCompletionSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    Get current user's profile.
    """
    try:
        profile = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Profile retrieved successfully'
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
    Update current user's profile.
    """
    try:
        profile = request.user.profile
        serializer = UserProfileUpdateSerializer(profile, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            # Return updated profile with full structure
            profile_serializer = UserProfileSerializer(profile)
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
def profile_completion_status(request):
    """
    Get profile completion status and missing fields.
    """
    try:
        profile = request.user.profile
        
        required_fields = [
            'first_name', 'last_name', 'date_of_birth',
            'mobile', 'address', 'job_designation', 'department'
        ]
        
        completed_fields = []
        missing_fields = []
        
        for field in required_fields:
            value = getattr(profile, field)
            if value:
                completed_fields.append(field)
            else:
                missing_fields.append(field)
        
        completion_percentage = int((len(completed_fields) / len(required_fields)) * 100)
        is_complete = len(missing_fields) == 0
        
        response_data = {
            'is_complete': is_complete,
            'completion_percentage': completion_percentage,
            'missing_fields': missing_fields,
            'completed_fields': completed_fields
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'Profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )