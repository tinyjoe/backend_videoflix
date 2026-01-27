from django.contrib import admin

from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    exclude = ('video_480p', 'video_720p', 'video_1080p')
