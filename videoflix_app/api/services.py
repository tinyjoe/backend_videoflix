from django.conf import settings
from django.http import Http404
from pathlib import Path


def safe_join(base: str, *paths):
    base_path = Path(base).resolve()
    final_path = base_path.joinpath(*paths).resolve()
    if base_path not in final_path.parents:
        raise Http404('Invalid path')
    return final_path


def build_hls_base_dir(video_id: int):
    return safe_join(settings.HLS_ROOT, str(video_id))


def build_hls_manifest_path(video_id: int, resolution: str):
    return safe_join(settings.HLS_ROOT, str(video_id), resolution, 'index.m3u8')


def build_hls_master_path(video_id: int):
    return safe_join(settings.HLS_ROOT, str(video_id), 'index.m3u8')


def hls_manifest_exists(video_id: int, resolution: str):
    path = build_hls_manifest_path(video_id, resolution)
    return path.exists()


def hls_master_exists(video_id: int):
    path = build_hls_master_path(video_id)
    return path.exists()