from vimeo import VimeoClient


def get_user(vclient: VimeoClient, fields=None) -> dict:
    """Get user info with sane field defaults."""
    fields = fields or [
        "uri",
        "name",
        "link",
        "location",
        "bio",
        "short_bio",
        "created_time",
    ]
    params = {"fields": ",".join(fields)} if fields else {}

    uri = "/me/"
    response = vclient.get(uri, params=params)
    response.raise_for_status()
    return response.json()
