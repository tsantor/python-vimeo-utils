from vimeo_utils.user import get_user


def test_get_user(vimeo_client):
    response = get_user(vimeo_client)
    expected_keys = [
        "uri",
        "name",
        "link",
        "location",
        "bio",
        "short_bio",
        "created_time",
    ]
    assert all(key in response for key in expected_keys)
