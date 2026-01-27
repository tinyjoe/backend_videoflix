from django.db import models

class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    category = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/original/')
    video_480p = models.FileField(upload_to='videos/480p/', null=True, blank=True)
    video_720p = models.FileField(upload_to='videos/720p/', null=True, blank=True)
    video_1080p = models.FileField(upload_to='videos/1080p/', null=True, blank=True)
    is_ready = models.BooleanField(default=False)
