import os
import django_rq

from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from videoflix_app.models import Video
from .tasks import convert_video, convert_mp4_to_hls


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    The function `video_post_save` enqueues tasks to convert a newly created video file to different
    resolutions and formats using a task queue.
    """
    if created and instance.video_file: 
        def enqueue_tasks():
            queue = django_rq.get_queue('default')
            queue.enqueue(convert_video, instance.id, '480p')
            queue.enqueue(convert_video, instance.id, '720p')
            queue.enqueue(convert_video, instance.id, '1080p')
            queue.enqueue(convert_mp4_to_hls, instance.id)
        transaction.on_commit(enqueue_tasks)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes files from filesystem when corresponding `Video` object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
    if instance.video_480p:
        if os.path.isfile(instance.video_480p.path):
            os.remove(instance.video_480p.path)
    if instance.video_720p:
        if os.path.isfile(instance.video_720p.path):
            os.remove(instance.video_720p.path)
    if instance.video_1080p:
        if os.path.isfile(instance.video_1080p.path):
            os.remove(instance.video_1080p.path)