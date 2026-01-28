import os
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from videoflix_app.models import Video
from .serializers import VideoListSerializer
from .services import build_hls_manifest_path, hls_manifest_exists, safe_join
from .authentication import CookieJWTAuthentication

class VideoListView(ListAPIView):
    """
    View to list all videos.
    """
    ##authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all().order_by('id')
    serializer_class = VideoListSerializer


class HLSManifestView(APIView):
    """
    View to serve HLS manifest files for a given video and resolution.
    """
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, movie_id: int, resolution: str):
        """
        This Python function retrieves an HLS manifest file for a specific video based on the video ID
        and resolution provided.
        """
        if not hls_manifest_exists(movie_id, resolution):
            return Response(status=404)
        path = build_hls_manifest_path(movie_id, resolution)
        return FileResponse(open(path, 'rb'), content_type='application/vnd.apple.mpegurl')
    

class HlsSegmentView(APIView):
    """
    Returns a single HLS .ts segment.
    """
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, movie_id: int, resolution: str, segment: str):
        """
        This function retrieves a video segment based on the provided video ID, resolution, and segment
        name, handling errors for invalid or missing segments.
        """
        if not segment.endswith('.ts'):
            raise Http404('Invalid segment')
        segment_path = segment_path = safe_join(settings.HLS_ROOT, str(movie_id), resolution, segment,)
        if not os.path.exists(segment_path):
            raise Http404('Segment not found')
        try:
            return FileResponse(open(segment_path, 'rb'),content_type='video/MP2T',)
        except IOError:
            raise Http404('Segment not readable')