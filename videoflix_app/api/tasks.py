import os
import subprocess

from django.core.files import File
from videoflix_app.models import Video

def convert_video(video_id, resolution):
    """
    Converts the video to the specified resolution using ffmpeg.
    Supported resolutions: '480p', '720p', '1080p'
    """
    video = Video.objects.get(id=video_id)
    input_path = video.video_file.path
    base, ext = os.path.splitext(os.path.basename(input_path))
    target_filename = f"{base}_{resolution}.mp4"
    target_relative_path = f"videos/{resolution}/{target_filename}"
    target_absolute_path = os.path.join(os.path.dirname(video.video_file.path), '..', resolution, target_filename)
    os.makedirs(os.path.dirname(target_absolute_path), exist_ok=True)
    cmd = ["ffmpeg", "-y", "-i", input_path, "-vf", f"scale=hd{resolution[:-1]}", "-c:v", "libx264", "-crf", "23", "-c:a", "aac", target_absolute_path]  
    subprocess.run(cmd, check=True)   
    save_resolutions(resolution, video, input_path, target_filename)
    video.save()


def save_resolutions(resolution, video, input_path, target_filename):
    """
    The function `save_resolutions` saves a video file with different resolutions using Django's file
    handling.
    """
    with open(input_path, 'rb') as f:
        django_file = File(f)
        if resolution == '480p':
            video.video_480p.save(target_filename, django_file, save=False)
        elif resolution == '720p':
            video.video_720p.save(target_filename, django_file, save=False)
        elif resolution == '1080p':
            video.video_1080p.save(target_filename, django_file, save=False)
