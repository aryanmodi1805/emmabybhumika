from django.core.management.base import BaseCommand
from django.core.files import File
from fashion_images.models import TeamMember, FashionImage
import os

class Command(BaseCommand):
    help = 'Populate the database with team members and images'

    def handle(self, *args, **options):
        # Clear existing data
        TeamMember.objects.all().delete()
        
        # Team members data
        team_data = [
            {
                'name': 'Sarah Johnson',
                'title': 'Creative Designer',
                'view_url': '/designer/sarah-johnson',
                'images': ['1.jpg', '2.JPG', '3.JPG', '4.jpg', '5.JPG']
            },
            {
                'name': 'Emma Wilson',
                'title': 'Fashion Stylist',
                'view_url': '/stylist/emma-wilson',
                'images': ['6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpg']
            },
            {
                'name': 'Maya Patel',
                'title': 'Brand Manager',
                'view_url': '/manager/maya-patel',
                'images': ['11.jpg', '12.jpg', '13.jpg', '14.jpg', '15.jpg']
            },
            {
                'name': 'Jessica Chen',
                'title': 'Art Director',
                'view_url': '/director/jessica-chen',
                'images': ['16.jpg', '17.jpg', '18.jpg', '19.jpg', '20.jpg']
            }
        ]
        
        # Create team members and their images
        for member_data in team_data:
            member = TeamMember.objects.create(
                name=member_data['name'],
                title=member_data['title'],
                view_url=member_data['view_url']
            )
            
            # Add images for this member
            for order, image_name in enumerate(member_data['images']):
                # Check image paths
                image_paths = [
                    os.path.join('media', 'images', image_name)
                ]
                
                image_found = False
                for image_path in image_paths:
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as f:
                            django_file = File(f)
                            fashion_image = FashionImage.objects.create(
                                team_member=member,
                                order=order,
                                image_file=django_file
                            )
                            self.stdout.write(
                                self.style.SUCCESS(f'Created image {image_name} for {member.name} from {image_path}')
                            )
                            image_found = True
                            break
                
                if not image_found:
                    self.stdout.write(
                        self.style.WARNING(f'Image {image_name} not found in any expected location')
                    )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with team members and images')
        )
