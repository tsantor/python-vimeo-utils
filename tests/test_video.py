import os
from http import HTTPStatus

import pytest
import vimeo
from dotenv import load_dotenv
from vimeo_utils import add_domain_to_whitelist
from vimeo_utils import block_until_available
from vimeo_utils import delete_video
from vimeo_utils import edit_video
from vimeo_utils import get_download_link
from vimeo_utils import get_status
from vimeo_utils import get_transcode_status
from vimeo_utils import get_video_info
from vimeo_utils import is_available
from vimeo_utils import is_playable
from vimeo_utils import is_transcode_complete
from vimeo_utils import set_embed_preset
from vimeo_utils import upload_video
from vimeo_utils.constants import TranscodeStatus
from vimeo_utils.constants import VideoStatus

load_dotenv()


@pytest.fixture(scope="class")
def vimeo_client() -> vimeo.VimeoClient:
    return vimeo.VimeoClient(
        token=os.getenv("VIMEO_ACCESS_TOKEN"),
        key=os.getenv("VIMEO_CLIENT_ID"),
        secret=os.getenv("VIMEO_CLIENT_SECRET"),
    )


@pytest.fixture(scope="class", autouse=True)
def _setup_and_teardown(vimeo_client, video_params, request):
    # Upload video
    request.cls.video_uri = upload_video(
        vimeo_client, "tests/test.mp4", params=video_params
    )

    # Block until video is available
    block_until_available(vimeo_client, request.cls.video_uri)

    yield  # This is where the tests will be run

    # Delete video
    delete_video(vimeo_client, request.cls.video_uri)


class TestSafely:
    """Waits for video to be available before running tests."""

    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    def test_get_video_info(self, vimeo_client):
        response = get_video_info(vimeo_client, self.video_uri)
        expected_keys = [
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

        assert all(key in response for key in expected_keys)

    def test_edit_video(self, vimeo_client):
        params = {
            "name": "Test edit",
            "description": "Test edit",
        }
        response = edit_video(vimeo_client, self.video_uri, params)
        assert response["name"] == "Test edit"
        assert response["description"] == "Test edit"

    def test_set_embed_preset(self, vimeo_client):
        preset_id = os.getenv("VIMEO_EMBED_PRESET")
        response = set_embed_preset(vimeo_client, self.video_uri, preset_id)
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_add_domain_to_whitelist(self, vimeo_client):
        domain = "example.com"
        response = add_domain_to_whitelist(vimeo_client, self.video_uri, domain)
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_get_transcode_status(self, vimeo_client):
        response = get_transcode_status(vimeo_client, self.video_uri)
        allowed_statuses = [
            TranscodeStatus.COMPLETE,
            TranscodeStatus.ERROR,
            TranscodeStatus.IN_PROGRESS,
        ]
        assert any(status in response for status in allowed_statuses)

    def test_get_status(self, vimeo_client):
        response = get_status(vimeo_client, self.video_uri)
        allowed_statuses = [
            VideoStatus.AVAILABLE,
            VideoStatus.TRANSCODE_STARTING,
            VideoStatus.TRANSCODING,
            VideoStatus.TRANSCODING_ERROR,
            VideoStatus.UNAVAILABLE,
            VideoStatus.UPLOADING,
            VideoStatus.UPLOADING_ERROR,
        ]
        assert any(status in response for status in allowed_statuses)

    def test_is_available(self, vimeo_client):
        response = is_available(vimeo_client, self.video_uri)
        assert response is True

    def test_is_transcode_complete(self, vimeo_client) -> bool:
        response = is_transcode_complete(vimeo_client, self.video_uri)
        assert response is True

    def test_is_playable(self, vimeo_client):
        response = is_playable(vimeo_client, self.video_uri)
        assert response is True

    def test_get_download_link(self, vimeo_client):
        response = get_download_link(vimeo_client, self.video_uri)
        assert response is not None
        assert response.startswith(
            "https://player.vimeo.com/progressive_redirect/download"
        )

    # def test_delete_video(self, vimeo_client):
    #     response = delete_video(vimeo_client, self.video_uri)
    #     assert response.status_code == HTTPStatus.NO_CONTENT
