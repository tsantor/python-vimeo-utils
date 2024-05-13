"""Implementation of https://developer.vimeo.com/api/reference/folders"""

from typing import Optional

from requests import Response
from vimeo import VimeoClient

from .utils import build_user_uri


def create_project(
    vclient: VimeoClient,
    name: str,
    parent_folder_uri=None,
    fields=None,
    user_id: Optional[int] = None,  # noqa: UP007
) -> Response:
    """Create a new project."""
    user_uri = build_user_uri(user_id)
    data = {"name": name, "parent_folder_uri": parent_folder_uri}
    fields = fields or ["uri", "name"]
    params = {"fields": ",".join(fields)} if fields else {}
    response = vclient.post(f"{user_uri}/projects", data=data, params=params)
    response.raise_for_status()
    return response.json()


def delete_project(
    vclient: VimeoClient,
    project_id: int,
    should_delete_clips: bool = False,
    user_id: Optional[int] = None,  # noqa: UP007
) -> Response:
    """Delete a project."""
    user_uri = build_user_uri(user_id)
    params = {"should_delete_clips": should_delete_clips}
    response = vclient.delete(f"{user_uri}/projects/{project_id}", params=params)
    response.raise_for_status()
    return response


def get_all_projects(
    vclient: VimeoClient, user_id: Optional[int] = None, params: Optional[dict] = None
) -> Response:  # noqa: UP007
    """Returns paginated folders belonging to the authenticated user."""
    user_uri = build_user_uri(user_id)
    params = params or {}
    response = vclient.get(f"{user_uri}/projects", params=params)
    response.raise_for_status()
    return response


def move_to_project(
    vclient: VimeoClient,
    project_id: int,
    video_id: int,
    user_id: Optional[int] = None,  # noqa: UP007
) -> Response:
    """Move a video to a project."""
    user_uri = build_user_uri(user_id)
    uri = f"{user_uri}/projects/{project_id}/videos/{video_id}"
    response = vclient.put(uri)
    response.raise_for_status()
    return response
