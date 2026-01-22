from django.http import FileResponse
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from videoflix_app.models import Video
from .serializers import VideoListSerializer
from .services import build_hls_manifest_path, hls_manifest_exists
from .authentication import CookieJWTAuthentication

class VideoListView(ListAPIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all().order_by('id')
    serializer_class = VideoListSerializer


class HLSManifestView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, video_id: int, resolution: str):
        if not hls_manifest_exists(video_id, resolution):
            return Response(status=404)
        path = build_hls_manifest_path(video_id, resolution)
        return FileResponse(open(path, "rb"), content_type="application/vnd.apple.mpegurl")