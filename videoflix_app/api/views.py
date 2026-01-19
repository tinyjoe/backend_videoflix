from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.authentication import JWTAuthentication

from videoflix_app.models import Video
from .serializers import VideoListSerializer
from .authentication import CookieJWTAuthentication

class VideoListView(ListAPIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all().order_by('id')
    serializer_class = VideoListSerializer