from rest_framework import serializers

from videoflix_app.models import Video


class VideoListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing video objects.
    """
    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']


class HLSManifestRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting an HLS manifest.
    """
    video_id = serializers.IntegerField()
    resolution = serializers.ChoiceField(choices=['480p', '720p', '1080p'])