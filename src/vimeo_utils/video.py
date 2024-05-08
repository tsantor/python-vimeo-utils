import logging
import time
from typing import Optional

from requests import Request
from vimeo import VimeoClient

from .constants import TranscodeStatus
from .constants import VideoStatus
from .exceptions import TranscodingError

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


def upload_video(vclient: VimeoClient, video_file, params) -> str:
    """Upload video."""
    return vclient.upload(video_file, data=params)


def get_video_info(vclient: VimeoClient, vimeo_uri: str, fields=None) -> dict:
    """Return video info with sane defaults."""
    fields = fields or [
        "uri",
        "name",
        "description",
        "link",
        "created_time",
        "privacy",
        "download",
        "status",
        "upload",
        "transcode",
        "is_playable",
    ]
    params = {"fields": ",".join(fields)} if fields else {}
    response = vclient.get(vimeo_uri, params=params)
    response.raise_for_status()
    return response.json()


def edit_video(vclient: VimeoClient, vimeo_uri: str, params: dict) -> dict:
    """Edit a video."""
    response = vclient.patch(vimeo_uri, data=params)
    response.raise_for_status()
    return response.json()


def set_embed_preset(vclient: VimeoClient, vimeo_uri: str, preset_id: int) -> Request:
    """Set the embed preset."""
    uri = f"{vimeo_uri}/presets/{preset_id}"
    response = vclient.put(uri)
    response.raise_for_status()
    return response


def add_domain_to_whitelist(
    vclient: VimeoClient, vimeo_uri: str, domain: str
) -> Request:
    """Add domain to whitelist."""
    uri = f"{vimeo_uri}/privacy/domains/{domain}"
    response = vclient.put(uri)
    response.raise_for_status()
    return response


def get_download_link(vclient: VimeoClient, vimeo_uri: str) -> Optional[str]:  # noqa: UP007
    """Get download link. HD is priority."""
    video_info = get_video_info(vclient, vimeo_uri, fields=["download"])
    if "download" in video_info:
        hd_downloads = (
            video for video in video_info["download"] if video["quality"] == "hd"
        )
        sd_downloads = (
            video for video in video_info["download"] if video["quality"] == "sd"
        )

        # Prefer HD downloads
        try:
            return max(hd_downloads, key=lambda x: x.get("height", 0))["link"]
        except ValueError:
            pass

        # If no HD downloads, get the highest quality SD download
        try:
            return max(sd_downloads, key=lambda x: x.get("height", 0))["link"]
        except ValueError:
            pass

    return None


def move_to_project(vclient: VimeoClient, vimeo_uri: str, project_id: int) -> Request:
    """Move to project"""
    vimeo_uri = vimeo_uri.lstrip("/")
    uri = f"/me/projects/{project_id}/{vimeo_uri}"
    response = vclient.put(uri)
    response.raise_for_status()
    return response


def delete_video(vclient: VimeoClient, vimeo_uri: str) -> Request:
    response = vclient.delete(vimeo_uri)
    response.raise_for_status()
    return response


def get_status(vclient: VimeoClient, vimeo_uri: str) -> str:
    """Get video status."""
    video_info = get_video_info(vclient, vimeo_uri, fields=["status"])
    return video_info["status"]


def get_transcode_status(vclient: VimeoClient, vimeo_uri: str) -> str:
    """Get video transcode status."""
    video_info = get_video_info(vclient, vimeo_uri, fields=["transcode"])
    return video_info["transcode"]["status"]


def is_available(vclient: VimeoClient, vimeo_uri) -> bool:
    return get_status(vclient, vimeo_uri) == VideoStatus.AVAILABLE


def is_transcode_complete(vclient: VimeoClient, vimeo_uri: str) -> bool:
    return get_transcode_status(vclient, vimeo_uri) == TranscodeStatus.COMPLETE


def is_playable(vclient: VimeoClient, vimeo_uri: str) -> bool:
    video_info = get_video_info(vclient, vimeo_uri, fields=["is_playable"])
    return video_info["is_playable"]


def block_until_available(
    vclient: VimeoClient, vimeo_uri: str, interval: int = 30
) -> None:
    """Blocks until video is available. Be careful with this."""
    error_statuses = {
        VideoStatus.TRANSCODING_ERROR,
        VideoStatus.UPLOADING_ERROR,
    }
    while True:
        status = get_status(vclient, vimeo_uri)
        if status == VideoStatus.AVAILABLE:
            return
        if status in error_statuses:
            msg = "Transcoding/Uploading error"
            raise TranscodingError(msg)
        time.sleep(interval)
