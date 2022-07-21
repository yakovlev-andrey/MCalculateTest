import pytest
import os
from starlette.testclient import TestClient
from unittest import mock

from main import app


@pytest.fixture(scope="module")
def test_app():
    with mock.patch.dict(os.environ, {"FLOWER_URL": "http://flower:5555"}):
        client = TestClient(app, base_url="http://testserver")
        yield client  # testing happens here
