"""
Custom Cloudinary storage for document files.
"""
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary import uploader
import cloudinary


class DocumentCloudinaryStorage(MediaCloudinaryStorage):
    """
    Custom Cloudinary storage that handles document files properly.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set location attribute for Django compatibility
        self.location = 'documents'
    
    def _upload(self, file, folder=None, public_id=None, resource_type='raw'):
        """
        Upload file to Cloudinary with proper resource type for documents.
        """
        try:
            # Determine resource type based on file extension
            file_extension = file.name.split('.')[-1].lower()
            
            # Set resource type based on file type
            if file_extension in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']:
                resource_type = 'image'
            elif file_extension in ['mp4', 'webm', 'ogv', 'avi', 'mov']:
                resource_type = 'video'
            else:
                # For documents (PDF, DOC, TXT, etc.), use 'raw'
                resource_type = 'raw'
            
            # Upload to Cloudinary
            result = uploader.upload(
                file,
                folder=folder,
                public_id=public_id,
                resource_type=resource_type,
                use_filename=True,
                unique_filename=True
            )
            
            return result
            
        except Exception as e:
            print(f"❌ Cloudinary upload error: {e}")
            raise e
    
    def save(self, name, content, max_length=None):
        """
        Save file to Cloudinary with proper handling for documents.
        """
        try:
            # Extract the folder and filename from the name
            # name format: "documents/EMP774329/hash.pdf"
            parts = name.split('/')
            if len(parts) >= 3:
                folder = f"{parts[0]}/{parts[1]}"  # "documents/EMP774329"
                filename = parts[2].split('.')[0]  # "hash" (without extension)
            else:
                folder = 'documents'
                filename = name.split('/')[-1].split('.')[0]
            
            print(f"📁 Uploading to folder: {folder}")
            print(f"📄 Filename: {filename}")
            
            # Upload the file
            result = self._upload(content, folder=folder, public_id=filename)
            
            # Return the original name to maintain consistency
            return name
            
        except Exception as e:
            print(f"❌ Error saving to Cloudinary: {e}")
            raise e
    
    def exists(self, name):
        """
        Check if file exists in Cloudinary.
        """
        try:
            # For Cloudinary, we'll assume the file exists if we can get its URL
            # This is a simplified check - in production you might want to use Cloudinary API
            return True  # Assume file exists if it was uploaded successfully
        except Exception as e:
            print(f"❌ Error checking file existence: {e}")
            return False
    
    def size(self, name):
        """
        Get the size of the file.
        """
        try:
            # For Cloudinary, we can't easily get file size without API call
            # Return a default size or implement API call to get actual size
            return 0  # Default size
        except Exception as e:
            print(f"❌ Error getting file size: {e}")
            return 0
    
    def url(self, name):
        """
        Get the URL for the file.
        """
        try:
            # For raw files, we need to construct the URL manually
            if name.endswith(('.pdf', '.doc', '.docx', '.txt', '.zip', '.rar')):
                # Extract the public_id from the name
                # name format: "documents/EMP774329/hash.pdf"
                parts = name.split('/')
                if len(parts) >= 3:
                    # Construct public_id: "documents/EMP774329/hash"
                    public_id = f"{parts[0]}/{parts[1]}/{parts[2].split('.')[0]}"
                else:
                    public_id = name.split('.')[0]
                
                # Construct URL for raw files
                cloud_name = cloudinary.config().cloud_name
                url = f"https://res.cloudinary.com/{cloud_name}/raw/upload/v1/{public_id}"
                print(f"🔗 Generated URL: {url}")
                return url
            else:
                # Use default URL generation for images/videos
                return super().url(name)
        except Exception as e:
            print(f"❌ Error getting URL: {e}")
            return f"/media/{name}"  # Fallback to local URL
