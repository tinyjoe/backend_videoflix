import os
import subprocess


from django.core.files import File
from videoflix_app.models import Video
from django.conf import settings


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


def convert_mp4_to_hls(video_id):
    video = Video.objects.get(id=video_id)
    base_dir = os.path.join(settings.MEDIA_ROOT, 'hls', f"video_{video.id}")
    os.makedirs(base_dir, exist_ok=True)
    resolutions = {'480p': video.video_480p.path,'720p': video.video_720p.path,'1080p': video.video_1080p.path,}
    resolution_subprocess(base_dir, resolutions)
    master_path = os.path.join(base_dir, 'index.m3u8')
    write_hls_file(master_path)
    video.hls_ready = True
    video.save()


def resolution_subprocess(base_dir, resolutions):
    for res, input_path in resolutions.items():
        out_dir = os.path.join(base_dir, res)
        os.makedirs(out_dir, exist_ok=True)
        cmd = ['ffmpeg', '-y', '-i', input_path, '-hls_time', '6', '-hls_playlist_type', 'vod', '-hls_segment_filename', f"{out_dir}/segment_%03d.ts", f"{out_dir}/index.m3u8"]
        subprocess.run(cmd, check=True)


def write_hls_file(master_path):
    with open(master_path, 'w') as file: 
        file.write("""#EXTM3U
        #EXT-X-VERSION:3
        #EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=854x480
        480p/index.m3u8
        #EXT-X-STREAM-INF:BANDWIDTH=2500000,RESOLUTION=1280x720
        720p/index.m3u8
        #EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080
        1080p/index.m3u8
        """)