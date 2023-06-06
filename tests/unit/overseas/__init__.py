import pytest
from kis.core.overseas import OverseasClient, NAMED_SYMBOLS


@pytest.fixture(scope="class")
def overseas_client(app_key: str, app_secret: str):
    return OverseasClient(
        app_key=app_key,
        app_secret=app_secret,
        is_dev=True,
        exchange="NAS"
    )


@pytest.fixture(scope="class")
def apple():
    return NAMED_SYMBOLS["애플"]
