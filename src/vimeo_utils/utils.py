def build_user_uri(user_id: None) -> str:
    """Build the user URI."""
    if user_id:
        return f"/users/{user_id}"
    return "/me"


def get_project_id_from_uri(uri: str) -> int:
    """Get project ID from URI."""
    return int(uri.split("/")[-1])


def get_video_id_from_uri(uri: str) -> int:
    """Get video ID from URI."""
    return uri.split("/")[-1]
