import os
import uuid
from typing import Optional
from supabase import create_client, Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class SupabaseStorageService:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        self.bucket_name = os.getenv('SUPABASE_BUCKET_NAME', 'fashion-images')
        
        if not self.supabase_url or not self.supabase_key:
            logger.warning("Supabase credentials not found. Using local storage fallback.")
            self.client = None
        else:
            try:
                self.client: Client = create_client(self.supabase_url, self.supabase_key)
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                self.client = None
    
    def upload_file(self, file_path: str, file_name: str, folder: str = "images") -> Optional[str]:
        """
        Upload a file to Supabase storage
        
        Args:
            file_path: Local path to the file
            file_name: Name for the file in storage
            folder: Folder in the bucket to store the file
            
        Returns:
            Public URL of the uploaded file or None if failed
        """
        if not self.client:
            logger.warning("Supabase client not available. Cannot upload file.")
            return None
            
        try:
            # Generate unique filename to avoid conflicts
            file_extension = os.path.splitext(file_name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            storage_path = f"{folder}/{unique_filename}"
            
            # Read file content
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # Upload to Supabase
            result = self.client.storage.from_(self.bucket_name).upload(
                path=storage_path,
                file=file_content,
                file_options={"content-type": self._get_content_type(file_extension)}
            )
            
            if result:
                # Get public URL
                public_url = self.client.storage.from_(self.bucket_name).get_public_url(storage_path)
                logger.info(f"File uploaded successfully: {public_url}")
                return public_url
            else:
                logger.error("Failed to upload file to Supabase")
                return None
                
        except Exception as e:
            logger.error(f"Error uploading file to Supabase: {e}")
            return None
    
    def upload_file_from_content(self, file_content: bytes, file_name: str, folder: str = "images") -> Optional[str]:
        """
        Upload file content directly to Supabase storage
        
        Args:
            file_content: File content as bytes
            file_name: Name for the file in storage
            folder: Folder in the bucket to store the file
            
        Returns:
            Public URL of the uploaded file or None if failed
        """
        if not self.client:
            logger.warning("Supabase client not available. Cannot upload file.")
            return None
            
        try:
            # Generate unique filename to avoid conflicts
            file_extension = os.path.splitext(file_name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            storage_path = f"{folder}/{unique_filename}"
            
            # Upload to Supabase
            result = self.client.storage.from_(self.bucket_name).upload(
                path=storage_path,
                file=file_content,
                file_options={"content-type": self._get_content_type(file_extension)}
            )
            
            if result:
                # Get public URL
                public_url = self.client.storage.from_(self.bucket_name).get_public_url(storage_path)
                logger.info(f"File uploaded successfully: {public_url}")
                return public_url
            else:
                logger.error("Failed to upload file to Supabase")
                return None
                
        except Exception as e:
            logger.error(f"Error uploading file to Supabase: {e}")
            return None
    
    def delete_file(self, file_url: str) -> bool:
        """
        Delete a file from Supabase storage
        
        Args:
            file_url: Public URL of the file to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        if not self.client:
            logger.warning("Supabase client not available. Cannot delete file.")
            return False
            
        try:
            # Extract path from URL
            path = self._extract_path_from_url(file_url)
            if not path:
                logger.error("Could not extract path from URL")
                return False
            
            # Delete from Supabase
            result = self.client.storage.from_(self.bucket_name).remove([path])
            
            if result:
                logger.info(f"File deleted successfully: {file_url}")
                return True
            else:
                logger.error("Failed to delete file from Supabase")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting file from Supabase: {e}")
            return False
    
    def _get_content_type(self, file_extension: str) -> str:
        """Get content type based on file extension"""
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
            '.avi': 'video/x-msvideo',
            '.pdf': 'application/pdf',
        }
        return content_types.get(file_extension.lower(), 'application/octet-stream')
    
    def _extract_path_from_url(self, url: str) -> Optional[str]:
        """Extract storage path from Supabase public URL"""
        try:
            # Supabase URLs typically look like: https://project.supabase.co/storage/v1/object/public/bucket/path
            parts = url.split('/storage/v1/object/public/')
            if len(parts) > 1:
                path_with_bucket = parts[1]
                # Remove bucket name from path
                path_parts = path_with_bucket.split('/', 1)
                if len(path_parts) > 1:
                    return path_parts[1]  # Return path without bucket name
            return None
        except Exception as e:
            logger.error(f"Error extracting path from URL: {e}")
            return None

# Global instance
supabase_storage = SupabaseStorageService()
