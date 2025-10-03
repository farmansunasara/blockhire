"""
Serializers for document-related API endpoints.
"""
import hashlib
from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from .models import DocumentRecord, DocumentVersion, DocumentAccessLog


class DocumentUploadSerializer(serializers.Serializer):
    """
    Serializer for document upload.
    """
    file = serializers.FileField()
    is_original = serializers.BooleanField(default=False)
    
    def validate_file(self, value):
        """
        Validate uploaded file.
        """
        # Check file size
        if value.size > settings.MAX_FILE_SIZE:
            raise serializers.ValidationError(
                f'File size too large. Maximum size is {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB'
            )
        
        # Check file type
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in settings.ALLOWED_FILE_TYPES:
            raise serializers.ValidationError(
                f'File type not allowed. Allowed types: {", ".join(settings.ALLOWED_FILE_TYPES)}'
            )
        
        return value
    
    def create(self, validated_data):
        """
        Create document record and generate hash.
        """
        file = validated_data['file']
        is_original = validated_data['is_original']
        user = self.context['request'].user
        
        # Generate document hash
        file.seek(0)
        file_content = file.read()
        doc_hash = hashlib.sha256(file_content).hexdigest()
        
        # Check if document already exists
        existing_doc = DocumentRecord.objects.filter(doc_hash=doc_hash).first()
        if existing_doc:
            # If it's the same user, allow update
            if existing_doc.user == user:
                # Update existing document
                existing_doc.file_name = file.name
                existing_doc.file_size = file.size
                existing_doc.storage_path = f"documents/{user.emp_id}/{file.name}"
                existing_doc.file_type = file.name.split('.')[-1].lower()
                existing_doc.upload_ip = self.context['request'].META.get('REMOTE_ADDR')
                existing_doc.user_agent = self.context['request'].META.get('HTTP_USER_AGENT')
                existing_doc.save()
                return existing_doc
            else:
                raise serializers.ValidationError('Document with this hash already exists and belongs to another user')
        
        # Check if this is the first document for this user (make it original)
        existing_docs = DocumentRecord.objects.filter(user=user).count()
        is_first_document = existing_docs == 0
        
        # Create document record with S3 file
        document = DocumentRecord.objects.create(
            user=user,
            doc_hash=doc_hash,
            file_name=file.name,
            file_size=file.size,
            is_original=is_original or is_first_document,  # First document is always original
            storage_path=f"documents/{user.emp_id}/{file.name}",
            file_type=file.name.split('.')[-1].lower(),
            upload_ip=self.context['request'].META.get('REMOTE_ADDR'),
            user_agent=self.context['request'].META.get('HTTP_USER_AGENT'),
            file=file  # This will automatically upload to S3
        )
        
        # Update user profile with document information
        try:
            profile = user.profile
            # Add to document history array
            if doc_hash not in profile.doc_history:
                profile.doc_history.append(doc_hash)
            
            # If this is the original document, set as the valid doc_hash
            if document.is_original:
                profile.doc_hash = doc_hash
                profile.storage_path = document.storage_path
            
            profile.save()
        except:
            pass  # Profile might not exist yet
        
        return document


class DocumentRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for document records.
    """
    file_size_mb = serializers.ReadOnlyField()
    download_url = serializers.ReadOnlyField()
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentRecord
        fields = (
            'id', 'doc_hash', 'upload_date', 'file_name', 'file_size',
            'file_size_mb', 'is_original', 'storage_path', 'file_type',
            'download_url', 'user_name'
        )
        read_only_fields = ('id', 'doc_hash', 'upload_date', 'user_name')
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def to_representation(self, instance):
        """
        Convert snake_case to camelCase for frontend compatibility.
        """
        data = super().to_representation(instance)
        return {
            'id': data['id'],
            'docHash': data['doc_hash'],
            'uploadDate': data['upload_date'],
            'fileName': data['file_name'],
            'fileSize': data['file_size'],
            'fileSizeMb': data['file_size_mb'],
            'isOriginal': data['is_original'],
            'storagePath': data['storage_path'],
            'fileType': data['file_type'],
            'downloadUrl': data['download_url'],
            'userName': data['user_name']
        }


class DocumentVersionSerializer(serializers.ModelSerializer):
    """
    Serializer for document versions.
    """
    class Meta:
        model = DocumentVersion
        fields = (
            'id', 'version_number', 'doc_hash', 'file_name',
            'file_size', 'upload_date', 'change_reason'
        )
        read_only_fields = ('id', 'version_number', 'upload_date')


class DocumentAccessLogSerializer(serializers.ModelSerializer):
    """
    Serializer for document access logs.
    """
    accessed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentAccessLog
        fields = (
            'id', 'access_type', 'access_date', 'ip_address',
            'accessed_by_name'
        )
        read_only_fields = ('id', 'access_date', 'accessed_by_name')
    
    def get_accessed_by_name(self, obj):
        return f"{obj.accessed_by.first_name} {obj.accessed_by.last_name}"


class DocumentHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for document history.
    """
    versions = DocumentVersionSerializer(many=True, read_only=True)
    access_logs = DocumentAccessLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = DocumentRecord
        fields = (
            'id', 'doc_hash', 'upload_date', 'file_name', 'file_size',
            'is_original', 'storage_path', 'file_type', 'versions', 'access_logs'
        )
