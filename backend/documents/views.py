"""
Document-related API views.
"""
import os
from django.http import HttpResponse, Http404
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .models import DocumentRecord, DocumentAccessLog
from .serializers import (
    DocumentUploadSerializer, DocumentRecordSerializer,
    DocumentHistorySerializer, DocumentAccessLogSerializer
)


class DocumentUploadView(APIView):
    """
    Handle document uploads.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        """
        Upload a new document.
        """
        serializer = DocumentUploadSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            try:
                document = serializer.save()
                
                # Log access
                DocumentAccessLog.objects.create(
                    document=document,
                    accessed_by=request.user,
                    access_type='upload',
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT')
                )
                
                response_serializer = DocumentRecordSerializer(document)
                return Response({
                    'success': True,
                    'data': response_serializer.data,
                    'message': 'Document uploaded successfully'
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response({
                    'success': False,
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': False,
            'error': 'Validation failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_history(request):
    """
    Get user's document history.
    """
    documents = DocumentRecord.objects.filter(user=request.user)
    serializer = DocumentHistorySerializer(documents, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_document(request, doc_hash):
    """
    Download a document by hash.
    """
    try:
        document = DocumentRecord.objects.get(
            doc_hash=doc_hash,
            user=request.user
        )
        
        # Log access
        DocumentAccessLog.objects.create(
            document=document,
            accessed_by=request.user,
            access_type='download',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        # For now, return a placeholder response
        # In production, this would serve the actual file
        response = HttpResponse(
            f"Document {document.file_name} would be downloaded here",
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{document.file_name}"'
        return response
        
    except DocumentRecord.DoesNotExist:
        raise Http404("Document not found")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_details(request, doc_hash):
    """
    Get document details by hash.
    """
    try:
        document = DocumentRecord.objects.get(
            doc_hash=doc_hash,
            user=request.user
        )
        
        # Log access
        DocumentAccessLog.objects.create(
            document=document,
            accessed_by=request.user,
            access_type='view',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        serializer = DocumentRecordSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except DocumentRecord.DoesNotExist:
        return Response(
            {'error': 'Document not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_document(request, doc_hash):
    """
    Delete a document by hash.
    """
    try:
        document = DocumentRecord.objects.get(
            doc_hash=doc_hash,
            user=request.user
        )
        
        # Don't allow deletion of original document
        if document.is_original:
            return Response(
                {'error': 'Cannot delete original document'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        document.delete()
        return Response(
            {'message': 'Document deleted successfully'}, 
            status=status.HTTP_200_OK
        )
        
    except DocumentRecord.DoesNotExist:
        return Response(
            {'error': 'Document not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def access_logs(request, doc_hash):
    """
    Get access logs for a document.
    """
    try:
        document = DocumentRecord.objects.get(
            doc_hash=doc_hash,
            user=request.user
        )
        
        logs = DocumentAccessLog.objects.filter(document=document)
        serializer = DocumentAccessLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except DocumentRecord.DoesNotExist:
        return Response(
            {'error': 'Document not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_hashes(request):
    """
    Get user's document history as an array of hashes.
    Returns the docHistory[] array as specified in the workflow.
    """
    try:
        profile = request.user.profile
        return Response({
            'success': True,
            'data': {
                'docHash': profile.doc_hash,  # Original valid hash
                'docHistory': profile.doc_history,  # Array of all hashes
                'storagePath': profile.storage_path
            },
            'message': 'Document history retrieved successfully'
        }, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)