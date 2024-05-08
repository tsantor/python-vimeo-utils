import os

from vimeo_utils.videos import file_exists_in_contents
from vimeo_utils.videos import get_all_videos
from vimeo_utils.videos import get_videos
from vimeo_utils.videos import get_videos_from_folder


def test_get_videos(vimeo_client):
    response = get_videos(vimeo_client)
    expected_keys = {"total", "page", "per_page", "paging", "data"}
    assert all(key in response for key in expected_keys)


def test_get_videos_from_folder(vimeo_client):
    response = get_videos_from_folder(
        vimeo_client, os.getenv("VIMEO_USER_ID"), os.getenv("VIMEO_FOLDER_ID")
    )
    expected_keys = {"total", "page", "per_page", "paging", "data"}
    assert all(key in response for key in expected_keys)


def test_get_all_videos(vimeo_client):
    response = get_all_videos(vimeo_client)
    assert isinstance(response, list)
    assert all(isinstance(video, dict) for video in response)
    expected_keys = {"uri", "name", "created_time", "status"}
    assert all(expected_keys.issubset(video.keys()) for video in response)


def test_file_exists_in_contents():
    video_uri = "/videos/123456"
    contents = [
        {"uri": "/videos/123456", "name": "Video1"},
        {"uri": "/videos/789012", "name": "Video2"},
    ]

    assert file_exists_in_contents(video_uri, contents) is True

    video_uri = "/videos/345678"
    assert file_exists_in_contents(video_uri, contents) is False
