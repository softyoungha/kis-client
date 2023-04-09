import os
import pytest

@pytest.fixture(name="app_key", scope="session")
def fixture_app_key():
    return os.getenv("app_key")

@pytest.fixture(name="app_secret", scope="session")
def fixture_app_secret():
    return os.getenv("app_secret")


@pytest.fixture(name="overseas_client", scope="session")
def fixture_overseas_client():
    return None