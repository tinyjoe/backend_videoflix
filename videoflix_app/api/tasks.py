import os
import subprocess

from django.core.files import File
from django.conf import settings
from videoflix_app.models import Video


def convert_video(video_id, resolution):
    """
    Converts the video to the specified resolution using ffmpeg.
    Supported resolutions: '480p', '720p', '1080p'
    """
    video = Video.objects.get(id=video_id)
    input_path = video.video_file.path
    base, _ = os.path.splitext(os.path.basename(input_path))
    target_filename = f"{base}_{resolution}.mp4"
    target_dir = os.path.join(settings.MEDIA_ROOT, 'videos',resolution)
    os.makedirs(target_dir, exist_ok=True)
    target_absolute_path = os.path.join(target_dir, target_filename)
    cmd = ['ffmpeg', '-y', '-i', input_path, '-vf', f"scale=hd{resolution[:-1]}", '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', target_absolute_path]
    subprocess.run(cmd, check=True)   
    save_resolutions(resolution, video, target_absolute_path, target_filename)
    video.save()


def save_resolutions(resolution, video, target_absolute_path, target_filename):
    """
    The function `save_resolutions` saves a video file with different resolutions using Django's file
    handling.
    """
    with open(target_absolute_path, 'rb') as f:
        django_file = File(f)
        if resolution == '480p':
            video.video_480p.save(target_filename, django_file, save=False)
        elif resolution == '720p':
            video.video_720p.save(target_filename, django_file, save=False)
        elif resolution == '1080p':
            video.video_1080p.save(target_filename, django_file, save=False)


def convert_mp4_to_hls(video_id):
    """
    Converts all available MP4 resolutions to HLS.
    """
    video = Video.objects.get(id=video_id)
    base_dir = os.path.join(settings.MEDIA_ROOT, 'hls', str(video.id))
    os.makedirs(base_dir, exist_ok=True)
    resolutions = {'480p': video.video_480p.path,'720p': video.video_720p.path,'1080p': video.video_1080p.path,}
    resolution_subprocess(video.id, base_dir, resolutions)
    master_path = os.path.join(base_dir, 'index.m3u8')
    write_hls_file(video.id, master_path)
    video.hls_ready = True
    video.save()


def resolution_subprocess(video_id,base_dir, resolutions):
    """
    Creates HLS variant playlists and segments.
    """
    for res, input_path in resolutions.items():
        out_dir = os.path.join(base_dir, res)
        os.makedirs(out_dir, exist_ok=True)
        cmd = ['ffmpeg', '-y', '-i', input_path, '-hls_time', '6', '-hls_playlist_type', 'vod', '-hls_base_url', f'/api/video/{video_id}/{res}/','-hls_segment_filename', os.path.join(out_dir, "segment_%03d.ts"), os.path.join(out_dir, "index.m3u8")]
        subprocess.run(cmd, check=True)


def write_hls_file(master_path):
    """
    Writes the master HLS playlist.
    """
    with open(master_path, 'w') as file: 
        file.write("""#EXTM3U
        #EXT-X-VERSION:3
        #EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=854x480
        /api/video/{video.id}/480p/index.m3u8
        #EXT-X-STREAM-INF:BANDWIDTH=2500000,RESOLUTION=1280x720
        /api/video/{video.id}/720p/index.m3u8
        #EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080
        /api/video/{video.id}/1080p/index.m3u8
        """)