from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'team-members', views.TeamMemberViewSet)
router.register(r'media-files', views.MediaFileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/card-data/', views.TeamMemberViewSet.as_view({'get': 'card_data'}), name='card-data'),
    path('media/<str:media_type>/<str:filename>', views.serve_media, name='serve-media'),
    path('images/<str:image_name>', views.serve_image, name='serve-image'),
]
