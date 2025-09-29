from rest_framework import serializers
from .models import TeamMember, FashionImage, MediaFile

class FashionImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FashionImage
        fields = ['id', 'image_url', 'order']
    
    def get_image_url(self, obj):
        # Use Supabase URL if available, otherwise fallback to local file
        if obj.image_url:
            return obj.image_url
        
        # Fallback to local file (for migration purposes)
        request = self.context.get('request')
        if obj.image_file and obj.image_file.name:
            filename = obj.image_file.name.split('/')[-1]
            if request:
                return f"{request.scheme}://{request.get_host()}/media/images/{filename}"
            return f"/media/images/{filename}"
        
        return None

class MediaFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = MediaFile
        fields = ['id', 'name', 'media_type', 'file_url', 'description']
    
    def get_file_url(self, obj):
        # Use Supabase URL if available, otherwise fallback to local file
        if obj.file_url:
            return obj.file_url
        
        # Fallback to local file (for migration purposes)
        request = self.context.get('request')
        if obj.file and obj.file.name:
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        
        return None

class TeamMemberSerializer(serializers.ModelSerializer):
    images = FashionImageSerializer(many=True, read_only=True, context={'request': None})
    
    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'title', 'view_url', 'images']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request:
            self.fields['images'].context['request'] = request
