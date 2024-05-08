import os

import pytest
import vimeo
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture()
def vimeo_client() -> vimeo.VimeoClient:
    return vimeo.VimeoClient(
        token=os.getenv("VIMEO_ACCESS_TOKEN"),
        key=os.getenv("VIMEO_CLIENT_ID"),
        secret=os.getenv("VIMEO_CLIENT_SECRET"),
    )
