"""
Document-related API views.
"""
import os
import hashlib
import secrets
import time
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .models import DocumentRecord, DocumentAccessLog
from accounts.models import UserProfile
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
        print(f"Document upload request data: {request.data}")
        print(f"Request files: {request.FILES}")
        print(f"Request method: {request.method}")
        
        serializer = DocumentUploadSerializer(
            data=request.data,
            context={'request': request}
        )
        
        print(f"Serializer data: {serializer.initial_data}")
        print(f"Serializer is valid: {serializer.is_valid()}")
        if not serializer.is_valid():
            print(f"Serializer errors: {serializer.errors}")
        
        if serializer.is_valid():
            try:
                # Get the uploaded file
                uploaded_file = serializer.validated_data['file']
                
                # Generate document hash from file content + document name + random salt
                file_content = uploaded_file.read()
                
                # Create a unique salt combining timestamp and random data
                timestamp = str(int(time.time() * 1000))  # milliseconds for uniqueness
                random_salt = secrets.token_hex(16)  # 32-character random hex
                
                # Combine file content, document name, and salt for hash
                hash_input = file_content + uploaded_file.name.encode('utf-8') + timestamp.encode('utf-8') + random_salt.encode('utf-8')
                doc_hash = hashlib.sha256(hash_input).hexdigest()
                
                print(f"Hash generation details:")
                print(f"  - File name: {uploaded_file.name}")
                print(f"  - File size: {len(file_content)} bytes")
                print(f"  - Timestamp: {timestamp}")
                print(f"  - Random salt: {random_salt}")
                print(f"  - Generated hash: {doc_hash}")
                
                # Reset file pointer for saving
                uploaded_file.seek(0)
                
                # Create storage path with hash as filename for uniqueness
                file_extension = os.path.splitext(uploaded_file.name)[1]
                storage_filename = f"{doc_hash}{file_extension}"
                storage_path = f"documents/{request.user.emp_id}/{storage_filename}"
                
                # Save file to storage
                print(f"Saving file to storage path: {storage_path}")
                saved_path = default_storage.save(storage_path, uploaded_file)
                print(f"File saved to: {saved_path}")
                print(f"File exists in storage: {default_storage.exists(saved_path)}")
                
                # Create document record
                document = DocumentRecord.objects.create(
                    user=request.user,
                    doc_hash=doc_hash,
                    file_name=uploaded_file.name,
                    file_size=uploaded_file.size,
                    storage_path=saved_path,  # Actual saved file path
                    file_type=uploaded_file.content_type.split('/')[-1],
                    upload_ip=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT')
                )
                print(f"Document record created with ID: {document.id}")
                
                # Update user profile with document hash
                try:
                    profile = request.user.profile
                    if not profile.doc_hash:  # First document becomes original
                        profile.doc_hash = doc_hash
                        profile.storage_path = document.storage_path
                        document.is_original = True
                        document.save()
                    
                    # Add to document history
                    if doc_hash not in profile.doc_history:
                        profile.doc_history.append(doc_hash)
                        profile.save()
                        
                except Exception as e:
                    print(f"Error updating profile: {e}")
                
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
        
        # Check if file exists in storage
        print(f"Checking if file exists: {document.storage_path}")
        print(f"File exists: {default_storage.exists(document.storage_path)}")
        print(f"Storage location: {default_storage.location}")
        
        if not default_storage.exists(document.storage_path):
            print(f"File not found in storage: {document.storage_path}")
            return Response({
                'success': False,
                'error': 'File not found in storage'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get file from storage
        file = default_storage.open(document.storage_path, 'rb')
        
        # Create file response
        response = FileResponse(
            file,
            content_type='application/octet-stream',
            as_attachment=True,
            filename=document.file_name
        )
        
        # Set additional headers
        response['Content-Length'] = document.file_size
        response['Content-Disposition'] = f'attachment; filename="{document.file_name}"'
        
        return response
        
    except DocumentRecord.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Document not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Download failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def preview_document(request, doc_hash):
    """
    Preview a document by hash (for verification purposes).
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
        
        # Check if file exists in storage
        if not default_storage.exists(document.storage_path):
            return Response({
                'success': False,
                'error': 'File not found in storage'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get file from storage
        file = default_storage.open(document.storage_path, 'rb')
        
        # Determine content type based on file type
        content_type = 'application/pdf' if document.file_type.lower() == 'pdf' else 'application/octet-stream'
        
        # Create file response for preview
        response = FileResponse(
            file,
            content_type=content_type,
            as_attachment=False  # Preview, not download
        )
        
        # Set additional headers
        response['Content-Length'] = document.file_size
        response['Content-Disposition'] = f'inline; filename="{document.file_name}"'
        
        return response
        
    except DocumentRecord.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Document not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Preview failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)