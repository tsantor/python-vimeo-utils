import os

import pytest
import vimeo
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture()
def user_id():
    return os.getenv("VIMEO_USER_ID")


@pytest.fixture()
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


# @pytest.fixture()
# def project_id():
#     return os.getenv("VIMEO_FOLDER_ID")


@pytest.fixture()
def vimeo_client() -> vimeo.VimeoClient:
    return vimeo.VimeoClient(
        token=os.getenv("VIMEO_ACCESS_TOKEN"),
        key=os.getenv("VIMEO_CLIENT_ID"),
        secret=os.getenv("VIMEO_CLIENT_SECRET"),
    )
