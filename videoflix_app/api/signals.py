import os
import django_rq

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from videoflix_app.models import Video
from .tasks import convert_480p, convert_720p, convert_1080p


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created: 
        print('New video uploaded')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_480p, instance.video_file.path)
        queue.enqueue(convert_720p, instance.video_file.path)
        queue.enqueue(convert_1080p, instance.video_file.path)


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
