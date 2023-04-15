import pytest
from pprint import pprint
from kis.domestic import DomesticClient, NAMED_SYMBOLS


@pytest.fixture(scope="class")
def client(app_key: str, app_secret: str):
    return DomesticClient(app_key=app_key, app_secret=app_secret, is_dev=False)


@pytest.fixture(scope="class")
def symbol():
    return NAMED_SYMBOLS["삼성전자"]


class TestDomesticQuote:

    def test_fetch_price(self, client: DomesticClient, symbol: str):
        price = client.quote.fetch_current_price(symbol)
        assert price.data.symbol == symbol

    def test_fetch_prices_by_minutes(self, client: DomesticClient, symbol: str):
        summary, full_histories = client.quote.fetch_prices_by_minutes(
            symbol,
            to="123000"
        )
        assert summary.symbol_korean == "삼성전자"

    def test_fetch_all_prices_by_minutes(self, client: DomesticClient, symbol: str):
        summary, full_histories = client.quote.fetch_prices_by_minutes(
            symbol,
            to="123000"
        )
        assert summary.symbol_korean == "삼성전자"

    def test_fetch_ohlcv_daily(self, client: DomesticClient, symbol: str):
        summary, detail = client.quote.fetch_histories(
            symbol,
            end_date="20230101",
            standard="D"
        )
        assert summary.symbol_korean == "삼성전자"
        assert summary.price_lowest <= summary.price_open <= summary.price_highest

    def test_fetch_ohlcv_weekly(self, client: DomesticClient, symbol: str):
        summary, detail = client.quote.fetch_histories(
            symbol,
            end_date="20230101",
            standard="W"
        )
        assert summary.symbol_korean == "삼성전자"
        assert summary.price_lowest <= summary.price_open <= summary.price_highest

    def test_fetch_ohlcv_monthly(self, client: DomesticClient, symbol: str):
        summary, detail = client.quote.fetch_histories(
            symbol,
            end_date="20230101",
            standard="M"
        )
        assert summary.symbol_korean == "삼성전자"
        assert summary.price_lowest <= summary.price_open <= summary.price_highest

    def test_fetch_ohlcv_year(self, client: DomesticClient, symbol: str):
        summary, detail = client.quote.fetch_histories(
            symbol,
            end_date="20230101",
            standard="Y"
        )
        # print(summary)
        assert summary.symbol_korean == "삼성전자"
        assert summary.price_lowest <= summary.price_open <= summary.price_highest
        assert len(detail) < 50, "year 단위로 50개를 넘지 못함"

    def test_fetch_all_ohlcv_monthly(self, client: DomesticClient, symbol: str):
        summary, detail = client.quote.fetch_histories(
            symbol,
            start_date="20220101",
            end_date="20230101",
            standard="M"
        )
        assert len(detail) == 12, "12개월"

    def test_fetch_all_ohlcv_monthly_2(self, client: DomesticClient, symbol: str):
        summary, detail = client.quote.fetch_histories(
            symbol,
            start_date="20200101",
            end_date="20230306",
            standard="M"
        )
        assert len(detail) == 38, "12 * 3 + 2개월"

    def test_fetch_all_ohlcv_daily(self, client: DomesticClient, symbol: str):
        summary, detail = client.quote.fetch_histories(
            symbol,
            start_date="20220101",
            end_date="20230101",
            standard="D"
        )
        assert len(detail) == 246, "영업일 기준 246일"


class TestDomesticBalance:

    def test_fetch_balance(self, client: DomesticClient):
        result = client.balance.fetch()
        assert len(result.detail) >= 1
