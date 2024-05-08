import concurrent.futures
import logging
import re

from vimeo import VimeoClient

logger = logging.getLogger(__name__)


def file_exists_in_contents(video_uri: str, contents: list[dict]) -> bool:
    return any(obj["uri"] == video_uri for obj in contents)


def extract_page_number(url: str) -> int:
    """Function to extract page number from a given URL."""
    match = re.search(r"page=(\d+)", url)
    return int(match.group(1)) if match else 1


def get_videos(vclient: VimeoClient, url: str = "/me/videos", page: int = 1) -> dict:
    """Get single page of videos, 100 max."""
    params = {
        "fields": "uri,name,created_time,status",
        "page": page,
        "per_page": 100,
    }
    response = vclient.get(url, params=params, timeout=60)
    response.raise_for_status()
    return response.json()


def get_all_videos(vclient: VimeoClient, url="/me/videos") -> list[dict]:
    """Get all videos."""
    videos = []

    response = get_videos(vclient, url)
    videos.extend(x for x in response["data"])

    # Extracting next and last page numbers
    paging = response.get("paging", {})
    next_url = paging.get("next") or ""
    last_url = paging.get("last") or ""
    next_page = extract_page_number(next_url)
    last_page = extract_page_number(last_url) or next_page
    if last_page > 1:
        last_page += 1

        # Get all the rest of the pages
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            future_to_page = {
                executor.submit(get_videos, vclient, url, page): page
                for page in range(next_page, last_page)
            }
            for future in concurrent.futures.as_completed(future_to_page):
                response = future.result()
                videos.extend(x for x in response["data"])
    return videos


def get_videos_from_folder(
    vclient: VimeoClient, user_id: int, project_id: int
) -> list[dict]:
    url = f"/users/{user_id}/folders/{project_id}/videos"
    return get_videos(vclient, url)
