import os
from django.conf import settings


def get_hls_base_dir(video_id: int) -> str:
    return os.path.join(settings.MEDIA_ROOT, 'hls', f"video_{video_id}")


def build_hls_manifest_path(video_id: int, resolution: str) -> str:
    return os.path.join(get_hls_base_dir(video_id), resolution, 'index.m3u8')


def hls_manifest_exists(video_id: int, resolution: str) -> bool:
    return os.path.exists(build_hls_manifest_path(video_id, resolution))