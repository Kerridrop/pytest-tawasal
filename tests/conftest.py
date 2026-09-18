import pytest

from config import STAGE_URL, STAGE_AUTH_TOKEN, PAYLOAD1, TEST_EMAIL_CREATE, PLANS
from api.base import BaseApiStage


@pytest.fixture(scope="session")
def api():
    return BaseApiStage()


@pytest.fixture(scope="class")
def subscription(api):
    response = api.create_sub(TEST_EMAIL_CREATE, PLANS["Pro"], quantity=5)
    assert response.status_code == 201, f"Creating error: {response.text[:50]}"

    data = response.json()

    yield data

    api.cancel_sub(data["subscriptionID"])