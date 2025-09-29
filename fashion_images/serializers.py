from rest_framework import serializers
from .models import TeamMember, FashionImage

class FashionImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FashionImage
        fields = ['id', 'image_url', 'order']
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        # Extract filename from the image_file path
        filename = obj.image_file.name.split('/')[-1]
        if request:
            return f"{request.scheme}://{request.get_host()}/media/images/{filename}"
        return f"/media/images/{filename}"

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
