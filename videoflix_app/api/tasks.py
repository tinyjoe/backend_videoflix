import os
import subprocess

from django.core.files import File
from django.conf import settings
from numpy import rint
from videoflix_app.models import Video
from .services import validate_hls


def convert_video(video_id, resolution):
    """
    Converts the video to the specified resolution using ffmpeg.
    Supported resolutions: '480p', '720p', '1080p'
    """
    video = Video.objects.get(id=video_id)
    if not video.video_file:
        raise RuntimeError('No video file found for conversion.')
    input_path = video.video_file.path
    base, _ = os.path.splitext(os.path.basename(input_path))
    target_filename = f"{base}_{resolution}.mp4"
    target_dir = os.path.join(settings.MEDIA_ROOT, 'videos',resolution)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, target_filename)
    cmd = ffmpeg_command(resolution, input_path, target_path)
    result = subprocess.run(cmd, capture_output=True, text=True)   
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {result.stderr}")
    save_resolutions(resolution, video, target_path, target_filename)
    video.save()


def ffmpeg_command(resolution, input_path, target_path):
    """
    The function `ffmpeg_command` generates an FFmpeg command to resize a video file to a specified
    resolution.
    """
    cmd = ['ffmpeg', '-y', '-i', input_path, '-vf', f"scale=hd{resolution[:-1]}", '-c:v', 'libx264', '-preset', 'fast', '-crf', '23', '-c:a', 'aac', target_path]
    return cmd


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
    resolutions = {}
    assign_resolutions_paths(video, resolutions)
    base_dir = os.path.join(settings.HLS_ROOT, str(video.id))
    os.makedirs(base_dir, exist_ok=True)
    resolution_subprocess(video.id, base_dir, resolutions)
    write_hls_file(video.id, os.path.join(base_dir, 'index.m3u8'))
    validate_hls(video.id)
    video.hls_ready = True
    print("BASE:", base_dir)
    print("FILES:", os.listdir(base_dir))
    video.save()


def assign_resolutions_paths(video, resolutions):
    """
    The function `assign_resolutions_paths` assigns paths for different video resolutions to a
    dictionary based on the availability of those resolutions in the input video object.
    """
    if video.video_480p:
        resolutions['480p'] = video.video_480p.path
    if video.video_720p:
        resolutions['720p'] = video.video_720p.path
    if video.video_1080p:
        resolutions['1080p'] = video.video_1080p.path
    if not resolutions: 
        raise RuntimeError('no encoded videos found for HLS conversion.')


def resolution_subprocess(video_id, base_dir, resolutions):
    """
    Creates HLS variant playlists and segments.
    """
    for res, input_path in resolutions.items():
        if not os.path.exists(input_path):
            raise RuntimeError(f"Missing source file: {input_path}")
        out_dir = os.path.join(base_dir, res)
        os.makedirs(out_dir, exist_ok=True)
        cmd = ['ffmpeg', '-y', '-i', input_path, '-hls_time', '6', '-hls_playlist_type', 'vod', '-hls_base_url', f'/api/video/{video_id}/{res}/','-hls_segment_filename', os.path.join(out_dir, 'segment_%03d.ts'), os.path.join(out_dir, 'index.m3u8')]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")


def write_hls_file(video_id, master_path):
    """
    Writes the master HLS playlist.
    """
    content = f"""#EXTM3U
    #EXT-X-VERSION:3
    #EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=854x480
    /api/video/{video_id}/480p/index.m3u8
    #EXT-X-STREAM-INF:BANDWIDTH=2500000,RESOLUTION=1280x720
    /api/video/{video_id}/720p/index.m3u8x
    #EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080
    /api/video/{video_id}/1080p/index.m3u8
    """
    with open(master_path, "w") as f:
        f.write(content)