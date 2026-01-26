from django.urls import path

from .views import VideoListView, HLSManifestView, HlsSegmentView

urlpatterns=[
    path('video/', VideoListView.as_view(), name='all_videos'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', HLSManifestView.as_view(), name='hls_manifest'),
    path('api/video/<int:movie_id>/<str:resolution>/<str:segment>/', HlsSegmentView.as_view(), name='hls_segment'),
]