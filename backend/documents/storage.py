"""
Custom storage configuration for documents.
"""
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class DocumentStorage(FileSystemStorage):
    """
    Custom storage for document files.
    """
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = os.path.join(settings.MEDIA_ROOT, 'documents')
        if base_url is None:
            base_url = settings.MEDIA_URL + 'documents/'
        super().__init__(location, base_url)
    
    def get_available_name(self, name, max_length=None):
        """
        Return a filename that's free on the target storage system.
        """
        # Add timestamp to avoid conflicts
        import time
        name, ext = os.path.splitext(name)
        timestamp = int(time.time())
        return f"{name}_{timestamp}{ext}"
