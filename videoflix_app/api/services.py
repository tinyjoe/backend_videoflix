import os
from django.conf import settings
from django.http import Http404
from pathlib import Path


def get_hls_base_dir(video_id: int) -> str:
    return os.path.join(settings.MEDIA_ROOT, 'hls', f"video_{video_id}")


def build_hls_manifest_path(video_id: int, resolution: str) -> str:
    return os.path.join(get_hls_base_dir(video_id), resolution, 'index.m3u8')


def hls_manifest_exists(video_id: int, resolution: str) -> bool:
    return os.path.exists(build_hls_manifest_path(video_id, resolution))


def safe_join(base: str, *paths):
    base_path = Path(base).resolve()
    final_path = base_path.joinpath(*paths).resolve()
    if not str(final_path).startswith(str(base_path)):
        raise Http404('Invalid path')
    return final_path