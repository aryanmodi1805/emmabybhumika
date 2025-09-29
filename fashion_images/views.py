from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
from django.conf import settings
import os
from .models import TeamMember, FashionImage, MediaFile
from .serializers import TeamMemberSerializer, MediaFileSerializer

class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    
    @action(detail=False, methods=['get'])
    def card_data(self, request):
        """API endpoint that returns card data in the same format as frontend expects"""
        team_members = TeamMember.objects.prefetch_related('images').all()
        serializer = self.get_serializer(team_members, many=True)
        
        # Transform the data to match frontend format
        card_data = []
        for member in serializer.data:
            card_data.append({
                'id': member['id'],
                'name': member['name'],
                'title': member['title'],
                'images': [img['image_url'] for img in member['images']],
                'viewUrl': member['view_url']
            })
        
        return Response(card_data)

def serve_media(request, media_type, filename):
    """Serve media files directly from the backend"""
    # Current path structure: media/images/, media/videos/, media/logos/
    media_path = os.path.join(settings.MEDIA_ROOT, media_type, filename)
    
    if os.path.exists(media_path):
        # Determine content type based on file extension
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            content_type = 'image/jpeg' if filename.lower().endswith(('.jpg', '.jpeg')) else 'image/png'
        elif filename.lower().endswith('.mp4'):
            content_type = 'video/mp4'
        else:
            content_type = 'application/octet-stream'
        
        with open(media_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            response['Cache-Control'] = 'public, max-age=31536000'
            return response
    else:
        return HttpResponse('Media file not found', status=404)

def serve_image(request, image_name):
    """Serve images directly from the backend (legacy endpoint)"""
    return serve_media(request, 'images', image_name)

class MediaFileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    
    @action(detail=False, methods=['get'])
    def media_list(self, request):
        """Get list of all media files"""
        media_files = MediaFile.objects.all()
        serializer = self.get_serializer(media_files, many=True, context={'request': request})
        
        media_data = []
        for media in serializer.data:
            media_data.append({
                'name': media['name'],
                'type': media['media_type'],
                'url': media['file_url'],
                'description': media['description']
            })
        
        return Response(media_data)