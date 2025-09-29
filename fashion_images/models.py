from django.db import models

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    view_url = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class FashionImage(models.Model):
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='images/')
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.team_member.name} - Image {self.order}"

class MediaFile(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('logo', 'Logo'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='media/')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.media_type})"