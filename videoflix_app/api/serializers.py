from rest_framework import serializers

from videoflix_app.models import Video


class VideoListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing video objects.
    """
    thumbnail_url = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None


class HLSManifestRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting an HLS manifest.
    """
    video_id = serializers.IntegerField()
    resolution = serializers.ChoiceField(choices=['480p', '720p', '1080p'])