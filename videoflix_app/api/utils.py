from django.conf import settings
from django.http import Http404
from pathlib import Path


def safe_join(base: str, *paths):
    """
    The function `safe_join` takes a base path and additional paths, resolves them, and ensures that the
    final path is within the base path to prevent directory traversal attacks.
    """
    base_path = Path(base).resolve()
    final_path = base_path.joinpath(*paths).resolve()
    if base_path not in final_path.parents:
        raise Http404('Invalid path')
    return final_path


def build_hls_base_dir(video_id: int):
    """
    The function `build_hls_base_dir` returns the base directory path for storing HLS files associated
    with a given video ID.
    """
    return safe_join(settings.HLS_ROOT, str(video_id))


def build_hls_manifest_path(video_id: int, resolution: str):
    """
    The function `build_hls_manifest_path` constructs the path to an HLS manifest file based on the
    video ID and resolution provided.
    """
    return safe_join(settings.HLS_ROOT, str(video_id), resolution, 'index.m3u8')


def build_hls_master_path(video_id: int):
    """
    The function `build_hls_master_path` constructs the path to the HLS master playlist file for a given
    video ID.
    """
    return safe_join(settings.HLS_ROOT, str(video_id), 'index.m3u8')


def hls_manifest_exists(video_id: int, resolution: str):
    """
    The function `hls_manifest_exists` checks if an HLS manifest file exists for a given video ID and
    resolution.
    """
    path = build_hls_manifest_path(video_id, resolution)
    return path.exists()


def hls_master_exists(video_id: int):
    """
    The function `hls_master_exists` checks if an HLS master file exists for a given video ID.
    """
    path = build_hls_master_path(video_id)
    return path.exists()


def validate_hls(video_id):
    """
    The function `validate_hls` checks for the presence of HLS manifest files for different resolutions
    associated with a given video ID.
    """
    for res in ['480p', '720p', '1080p']:
        path = Path(settings.HLS_ROOT) / str(video_id) / res / 'index.m3u8'
        print("CHECK:", path)
        if not path.exists():
            raise RuntimeError(f"Missing HLS manifest for resolution {res}")