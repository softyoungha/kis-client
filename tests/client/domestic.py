import pytest
from pprint import pprint
from kis.client.domestic import KisDomesticClient, NAMED_SYMBOLS
from pydantic import ValidationError


@pytest.fixture(scope="class")
def client(app_key: str, app_secret: str):
    return KisDomesticClient(app_key=app_key, app_secret=app_secret, is_dev=True)


@pytest.fixture(scope="class")
def symbol():
    return NAMED_SYMBOLS["삼성전자"]


class TestKisDomesticClient:

    def test_fetch_price(self, client: KisDomesticClient, symbol: str):
        price = client.fetch_current_price(symbol)
        assert price.data.symbol == symbol

    def test_fetch_prices_by_minutes(self, client: KisDomesticClient, symbol: str):
        price = client.fetch_prices_by_minutes(symbol, to="123000")
        pprint(price.summary)
        pprint(price.detail)

    def test_fetch_all_prices_by_minutes(self, client: KisDomesticClient, symbol: str):
        price = client.fetch_all_prices_by_minutes(symbol, to="123000")
        pprint(price)

    def test_fetch_ohlcv(self, client: KisDomesticClient, symbol: str):
        price = client.fetch_ohlcv(symbol, end_date="20230101", standard="M")
        pprint(price)

    def test_fetch_all_ohlcv(self, client: KisDomesticClient, symbol: str):
        price = client.fetch_all_ohlcv(symbol, end_date="20230101", standard="M")
        pprint(price)
