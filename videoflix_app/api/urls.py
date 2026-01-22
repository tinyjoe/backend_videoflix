from django.urls import path

from .views import VideoListView, HLSManifestView

urlpatterns=[
    path('video/', VideoListView.as_view(), name='all_videos'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', HLSManifestView.as_view(), name='hls_manifest'),
]