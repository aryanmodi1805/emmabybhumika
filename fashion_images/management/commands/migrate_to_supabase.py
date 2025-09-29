import os
from django.core.management.base import BaseCommand
from django.conf import settings
from fashion_images.models import FashionImage, MediaFile
from fashion_images.supabase_service import supabase_storage
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Migrate existing images from local storage to Supabase'

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

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force = options['force']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No files will be uploaded'))
        
        # Check if Supabase is configured
        if not supabase_storage.client:
            self.stdout.write(
                self.style.ERROR('Supabase not configured. Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.')
            )
            return
        
        self.stdout.write('Starting migration to Supabase...')
        
        # Migrate FashionImage objects
        self.migrate_fashion_images(dry_run, force)
        
        # Migrate MediaFile objects
        self.migrate_media_files(dry_run, force)
        
        self.stdout.write(self.style.SUCCESS('Migration completed!'))

    def migrate_fashion_images(self, dry_run=False, force=False):
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
            
            local_path = os.path.join(settings.MEDIA_ROOT, image.image_file.name)
            
            if not os.path.exists(local_path):
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  Error: Local file not found: {local_path}')
                )
                continue
            
            if dry_run:
                self.stdout.write(f'  Would migrate: {image.team_member.name} - Image {image.order}')
                migrated_count += 1
                continue
            
            # Upload to Supabase
            filename = os.path.basename(image.image_file.name)
            supabase_url = supabase_storage.upload_file(
                file_path=local_path,
                file_name=filename,
                folder='fashion-images'
            )
            
            if supabase_url:
                image.image_url = supabase_url
                image.save()
                migrated_count += 1
                self.stdout.write(f'  Migrated: {image.team_member.name} - Image {image.order}')
            else:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  Failed to upload: {image.team_member.name} - Image {image.order}')
                )
        
        self.stdout.write(f'FashionImage migration summary: {migrated_count} migrated, {skipped_count} skipped, {error_count} errors')

    def migrate_media_files(self, dry_run=False, force=False):
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
            
            local_path = os.path.join(settings.MEDIA_ROOT, media.file.name)
            
            if not os.path.exists(local_path):
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  Error: Local file not found: {local_path}')
                )
                continue
            
            if dry_run:
                self.stdout.write(f'  Would migrate: {media.name}')
                migrated_count += 1
                continue
            
            # Upload to Supabase
            filename = os.path.basename(media.file.name)
            folder = f'media-{media.media_type}s'  # e.g., 'media-images', 'media-videos'
            supabase_url = supabase_storage.upload_file(
                file_path=local_path,
                file_name=filename,
                folder=folder
            )
            
            if supabase_url:
                media.file_url = supabase_url
                media.save()
                migrated_count += 1
                self.stdout.write(f'  Migrated: {media.name}')
            else:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  Failed to upload: {media.name}')
                )
        
        self.stdout.write(f'MediaFile migration summary: {migrated_count} migrated, {skipped_count} skipped, {error_count} errors')
