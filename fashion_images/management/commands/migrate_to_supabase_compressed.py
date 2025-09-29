import os
from django.core.management.base import BaseCommand
from django.conf import settings
from fashion_images.models import FashionImage, MediaFile
from fashion_images.supabase_service import supabase_storage
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Migrate existing images from local storage to Supabase with compression'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually uploading',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force re-upload even if Supabase URL already exists',
        )
        parser.add_argument(
            '--max-size',
            type=int,
            default=5,
            help='Maximum file size in MB after compression (default: 5MB)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force = options['force']
        max_size_mb = options['max_size']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No files will be uploaded'))
        
        # Check if Supabase is configured
        if not supabase_storage.client:
            self.stdout.write(
                self.style.ERROR('Supabase not configured. Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.')
            )
            return
        
        self.stdout.write('Starting migration to Supabase with compression...')
        
        # Migrate FashionImage objects
        self.migrate_fashion_images(dry_run, force, max_size_mb)
        
        # Migrate MediaFile objects
        self.migrate_media_files(dry_run, force, max_size_mb)
        
        self.stdout.write(self.style.SUCCESS('Migration completed!'))

    def compress_image(self, input_path, output_path, max_size_mb):
        """Compress image to specified maximum size"""
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Calculate compression quality
                original_size = os.path.getsize(input_path)
                target_size = max_size_mb * 1024 * 1024  # Convert MB to bytes
                
                if original_size <= target_size:
                    # No compression needed
                    img.save(output_path, 'JPEG', quality=95)
                    return output_path
                
                # Calculate quality based on size ratio
                quality = int((target_size / original_size) * 95)
                quality = max(10, min(95, quality))  # Keep quality between 10-95
                
                # Try different quality levels
                for q in range(quality, 10, -5):
                    img.save(output_path, 'JPEG', quality=q)
                    if os.path.getsize(output_path) <= target_size:
                        break
                
                return output_path
                
        except Exception as e:
            logger.error(f"Error compressing image {input_path}: {e}")
            return None

    def migrate_fashion_images(self, dry_run=False, force=False, max_size_mb=5):
        """Migrate FashionImage objects to Supabase"""
        self.stdout.write('\nMigrating FashionImage objects...')
        
        images = FashionImage.objects.all()
        migrated_count = 0
        skipped_count = 0
        error_count = 0
        
        for image in images:
            # Skip if already has Supabase URL and not forcing
            if image.image_url and not force:
                skipped_count += 1
                self.stdout.write(f'  Skipped {image.team_member.name} - Image {image.order} (already has Supabase URL)')
                continue
            
            # Check if local file exists
            if not image.image_file or not image.image_file.name:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  Error: {image.team_member.name} - Image {image.order} has no local file')
                )
                continue
            
            # Fix the path - extract filename and create correct path
            file_path = image.image_file.name
            filename = os.path.basename(file_path)  # Get just the filename (e.g., "1.jpg")
            file_path = f'images/{filename}'  # Create correct path (e.g., "images/1.jpg")
            
            local_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            if not os.path.exists(local_path):
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  Error: Local file not found: {local_path}')
                )
                continue
            
            if dry_run:
                file_size_mb = os.path.getsize(local_path) / (1024 * 1024)
                self.stdout.write(f'  Would migrate: {image.team_member.name} - Image {image.order} ({file_size_mb:.1f}MB)')
                migrated_count += 1
                continue
            
            # Compress image if needed
            compressed_path = local_path
            if os.path.getsize(local_path) > max_size_mb * 1024 * 1024:
                temp_path = local_path + '.compressed.jpg'
                compressed_path = self.compress_image(local_path, temp_path, max_size_mb)
                if not compressed_path:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'  Failed to compress: {image.team_member.name} - Image {image.order}')
                    )
                    continue
            
            # Upload to Supabase
            filename = os.path.basename(file_path)
            supabase_url = supabase_storage.upload_file(
                file_path=compressed_path,
                file_name=filename,
                folder='fashion-images'
            )
            
            # Clean up temporary compressed file
            if compressed_path != local_path and os.path.exists(compressed_path):
                os.remove(compressed_path)
            
            if supabase_url:
                image.image_url = supabase_url
                image.save()
                migrated_count += 1
                file_size_mb = os.path.getsize(local_path) / (1024 * 1024)
                self.stdout.write(f'  Migrated: {image.team_member.name} - Image {image.order} ({file_size_mb:.1f}MB)')
            else:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  Failed to upload: {image.team_member.name} - Image {image.order}')
                )
        
        self.stdout.write(f'FashionImage migration summary: {migrated_count} migrated, {skipped_count} skipped, {error_count} errors')

    def migrate_media_files(self, dry_run=False, force=False, max_size_mb=5):
        """Migrate MediaFile objects to Supabase"""
        self.stdout.write('\nMigrating MediaFile objects...')
        
        media_files = MediaFile.objects.all()
        migrated_count = 0
        skipped_count = 0
        error_count = 0
        
        for media in media_files:
            # Skip if already has Supabase URL and not forcing
            if media.file_url and not force:
                skipped_count += 1
                self.stdout.write(f'  Skipped {media.name} (already has Supabase URL)')
                continue
            
            # Check if local file exists
            if not media.file or not media.file.name:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  Error: {media.name} has no local file')
                )
                continue
            
            # Fix the path - remove duplicate 'media/' prefix
            file_path = media.file.name
            if file_path.startswith('media/media/'):
                file_path = file_path.replace('media/media/', '')
            elif file_path.startswith('media/'):
                file_path = file_path.replace('media/', '')
            
            local_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            if not os.path.exists(local_path):
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  Error: Local file not found: {local_path}')
                )
                continue
            
            if dry_run:
                file_size_mb = os.path.getsize(local_path) / (1024 * 1024)
                self.stdout.write(f'  Would migrate: {media.name} ({file_size_mb:.1f}MB)')
                migrated_count += 1
                continue
            
            # Compress image files if needed
            compressed_path = local_path
            if media.media_type == 'image' and os.path.getsize(local_path) > max_size_mb * 1024 * 1024:
                temp_path = local_path + '.compressed.jpg'
                compressed_path = self.compress_image(local_path, temp_path, max_size_mb)
                if not compressed_path:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'  Failed to compress: {media.name}')
                    )
                    continue
            
            # Upload to Supabase
            filename = os.path.basename(media.file.name)
            folder = f'media-{media.media_type}s'  # e.g., 'media-images', 'media-videos'
            supabase_url = supabase_storage.upload_file(
                file_path=compressed_path,
                file_name=filename,
                folder=folder
            )
            
            # Clean up temporary compressed file
            if compressed_path != local_path and os.path.exists(compressed_path):
                os.remove(compressed_path)
            
            if supabase_url:
                media.file_url = supabase_url
                media.save()
                migrated_count += 1
                file_size_mb = os.path.getsize(local_path) / (1024 * 1024)
                self.stdout.write(f'  Migrated: {media.name} ({file_size_mb:.1f}MB)')
            else:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  Failed to upload: {media.name}')
                )
        
        self.stdout.write(f'MediaFile migration summary: {migrated_count} migrated, {skipped_count} skipped, {error_count} errors')
