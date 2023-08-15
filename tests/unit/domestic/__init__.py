from pprint import pprint
import pytest
from kis.core.domestic import DomesticClient, NAMED_SYMBOLS


@pytest.fixture(scope="class")
def domestic_client(app_key: str, app_secret: str):
    return DomesticClient(app_key=app_key, app_secret=app_secret, is_dev=True)


@pytest.fixture(scope="class")
def samsung():
    return NAMED_SYMBOLS["삼성전자"]
