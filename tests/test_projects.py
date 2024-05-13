import os
from http import HTTPStatus

import pytest
import vimeo
from vimeo_utils import delete_video
from vimeo_utils import upload_video
from vimeo_utils.projects import create_project
from vimeo_utils.projects import delete_project
from vimeo_utils.projects import get_all_projects
from vimeo_utils.projects import move_to_project
from vimeo_utils.utils import get_project_id_from_uri
from vimeo_utils.utils import get_video_id_from_uri


@pytest.fixture(scope="module")
def vimeo_client() -> vimeo.VimeoClient:
    return vimeo.VimeoClient(
        token=os.getenv("VIMEO_ACCESS_TOKEN"),
        key=os.getenv("VIMEO_CLIENT_ID"),
        secret=os.getenv("VIMEO_CLIENT_SECRET"),
    )


@pytest.fixture(scope="module")
def video_id(vimeo_client, video_params):
    # This is where the tests will be run
    video_uri = upload_video(vimeo_client, "tests/test.mp4", params=video_params)
    yield get_video_id_from_uri(video_uri)

    # Teardown: Delete the project using its uri
    delete_video(vimeo_client, video_uri)


@pytest.fixture(scope="module")
def project_id(vimeo_client):
    # Create a new project and retrieve its ID
    response = create_project(vimeo_client, "Test Project")

    # This is where the tests will be run
    yield get_project_id_from_uri(response["uri"])

    # Teardown: Delete the project using its ID
    delete_project(vimeo_client, get_project_id_from_uri(response["uri"]))


def test_create_project(project_id):
    assert project_id is not None
    assert isinstance(project_id, int)


def test_get_all_projects(vimeo_client):
    response = get_all_projects(vimeo_client)
    assert response.status_code == HTTPStatus.OK
    expected_keys = {"total", "page", "per_page", "paging", "data"}
    assert all(key in response.json() for key in expected_keys)


# def test_move_to_project(vimeo_client, project_id, video_id):
#     response = move_to_project(vimeo_client, project_id, video_id)
#     assert response.status_code == HTTPStatus.NO_CONTENT
