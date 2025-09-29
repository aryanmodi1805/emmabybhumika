from django.core.management.base import BaseCommand
from django.core.files import File
from fashion_images.models import MediaFile
import os

class Command(BaseCommand):
    help = 'Populate the database with all media files'

    def handle(self, *args, **options):
        # Clear existing media files
        MediaFile.objects.all().delete()
        
        # Base media directory
        media_base = 'media'
        
        # Process logos
        logos_dir = os.path.join(media_base, 'logos')
        if os.path.exists(logos_dir):
            for filename in os.listdir(logos_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # Check if already exists to avoid duplicates
                    if not MediaFile.objects.filter(name=filename, media_type='logo').exists():
                        file_path = os.path.join(logos_dir, filename)
                        with open(file_path, 'rb') as f:
                            django_file = File(f)
                            media_file = MediaFile.objects.create(
                                name=filename,
                                media_type='logo',
                                file=django_file,
                                description=f'Logo file: {filename}'
                            )
                            self.stdout.write(
                                self.style.SUCCESS(f'Created logo: {filename}')
                            )
        
        # Process videos
        videos_dir = os.path.join(media_base, 'videos')
        if os.path.exists(videos_dir):
            for filename in os.listdir(videos_dir):
                if filename.lower().endswith(('.mp4', '.avi', '.mov')):
                    # Check if already exists to avoid duplicates
                    if not MediaFile.objects.filter(name=filename, media_type='video').exists():
                        file_path = os.path.join(videos_dir, filename)
                        with open(file_path, 'rb') as f:
                            django_file = File(f)
                            media_file = MediaFile.objects.create(
                                name=filename,
                                media_type='video',
                                file=django_file,
                                description=f'Video file: {filename}'
                            )
                            self.stdout.write(
                                self.style.SUCCESS(f'Created video: {filename}')
                            )
        
        # Process fashion images
        images_dir = os.path.join(media_base, 'images')
        if os.path.exists(images_dir):
            for filename in os.listdir(images_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    # Check if already exists to avoid duplicates
                    if not MediaFile.objects.filter(name=filename, media_type='image').exists():
                        file_path = os.path.join(images_dir, filename)
                        with open(file_path, 'rb') as f:
                            django_file = File(f)
                            media_file = MediaFile.objects.create(
                                name=filename,
                                media_type='image',
                                file=django_file,
                                description=f'Fashion image: {filename}'
                            )
                            self.stdout.write(
                                self.style.SUCCESS(f'Created image reference: {filename}')
                            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with all media files')
        )
