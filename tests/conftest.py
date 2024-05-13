import os

import pytest
import vimeo
from dotenv import load_dotenv
from vimeo_utils.client import VimeoAPIClient

load_dotenv()


@pytest.fixture(scope="module")
def video_params():
    return {
        "name": "Test",
        "description": "Test upload and edit",
        "privacy": {
            "add": False,
            "comments": "nobody",
            "download": True,
            "embed": "public",
            "view": "disable",
        },
        "review_page": {"active": False},
        "embed": {
            "buttons": {
                "embed": False,
                "like": False,
                "share": False,
                "watchlater": False,
            },
            "title": {
                "name": "hide",
                "owner": "hide",
                "portrait": "hide",
            },
            "logos": {"vimeo": False},
            "end_screen": {"type": "empty"},
        },
    }


@pytest.fixture(scope="module")
def vimeo_client() -> vimeo.VimeoClient:
    return vimeo.VimeoClient(
        token=os.getenv("VIMEO_ACCESS_TOKEN"),
        key=os.getenv("VIMEO_CLIENT_ID"),
        secret=os.getenv("VIMEO_CLIENT_SECRET"),
    )


@pytest.fixture(scope="module")
def vclient(vimeo_client) -> VimeoAPIClient:
    return VimeoAPIClient(vimeo_client)


@pytest.fixture(scope="module")
def video_uri(vclient, video_params):
    # Setup: Upload a video and retrieve its URI
    video_uri = vclient.upload_video("tests/test.mp4", params=video_params)

    # Block until video is available
    vclient.block_until_available(video_uri)

    # This is where the tests will be run
    yield video_uri

    # Teardown: Delete the project using its uri
    vclient.delete_video(video_uri)


@pytest.fixture(scope="module")
def video_uri_no_wait(vclient, video_params):
    # Setup: Upload a video and retrieve its URI
    video_uri = vclient.upload_video("tests/test.mp4", params=video_params)

    # Block until video is available
    # vclient.block_until_available(video_uri)

    # This is where the tests will be run
    yield video_uri

    # Teardown: Delete the project using its uri
    vclient.delete_video(video_uri)
