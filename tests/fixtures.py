import os
import pytest


@pytest.fixture(name="app_key", scope="session")
def fixture_app_key():
    return os.getenv("KIS_APP_KEY")


@pytest.fixture(name="app_secret", scope="session")
def fixture_app_secret():
    return os.getenv("KIS_APP_SECRET")


@pytest.fixture(name="account", scope="session")
def fixture_account():
    return os.getenv("KIS_ACCOUNT")
