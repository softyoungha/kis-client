# pylint: disable=no-self-use, unused-variable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kis.core import OverseasClient


class TestOverseasQuote:
    """해외 주식 시세 조회 테스트"""

    def test_fetch_price(self, overseas_client: "OverseasClient", apple: str):
        """현재가를 조회합니다."""
        price = overseas_client.quote.fetch_current_price(apple)
        assert price.pretty.symbol == apple

    def test_fetch_price_detail(self, overseas_client: "OverseasClient", apple: str):
        """현재가 상세 정보를 조회합니다."""
        if overseas_client.is_dev:
            return

        price = overseas_client.quote.fetch_current_price_detail(apple)
        print(price)
        assert price.data.symbol == apple

    def test_fetch_ohlcv_daily(self, overseas_client: "OverseasClient", apple: str):
        """일봉을 조회합니다."""
        summary, detail = overseas_client.quote.fetch_histories(
            apple, end_date="20230101", standard="D"
        )
        assert summary.symbol == "AAPL"
        assert detail[0].low <= detail[0].open <= detail[0].high

    def test_fetch_ohlcv_weekly(self, overseas_client: "OverseasClient", apple: str):
        """주봉을 조회합니다."""
        summary, detail = overseas_client.quote.fetch_histories(
            apple, start_date="20070820", end_date="20230101", standard="W"
        )
        assert summary.symbol == "AAPL"
        assert detail[0].low <= detail[0].open <= detail[0].high
        assert len(detail) == 802
        assert detail[-1].business_date.strftime("%Y%m%d") == "20070820"
        assert detail[0].business_date.strftime("%Y%m%d") == "20221227"

    def test_fetch_ohlcv_monthly(self, overseas_client, apple):
        """월봉을 조회합니다."""
        summary, detail = overseas_client.quote.fetch_histories(
            apple, end_date="20230101", standard="M"
        )
        assert summary.symbol == "AAPL"
        assert detail[0].low <= detail[0].open <= detail[0].high
        assert len(detail) == 186
        assert detail[-1].business_date.strftime("%Y%m%d") == "20070831"
        assert detail[0].business_date.strftime("%Y%m%d") == "20221230"

    def test_fetch_all_ohlcv_monthly(
        self, overseas_client: "OverseasClient", apple: str
    ):
        """월봉을 조회합니다."""
        summary, detail = overseas_client.quote.fetch_histories(
            apple, start_date="20220101", end_date="20230101", standard="M"
        )
        assert len(detail) == 12, "12개월"

    def test_fetch_all_ohlcv_monthly_2(
        self, overseas_client: "OverseasClient", apple: str
    ):
        """월봉을 조회합니다.""" ""
        summary, detail = overseas_client.quote.fetch_histories(
            apple, start_date="20200101", end_date="20230306", standard="M"
        )
        assert len(detail) == 39, "12 * 3 + 3개월"

    def test_fetch_all_ohlcv_daily(self, overseas_client: "OverseasClient", apple: str):
        """일봉을 조회합니다."""
        summary, detail = overseas_client.quote.fetch_histories(
            apple, start_date="20220101", end_date="20230101", standard="D"
        )
        assert len(detail) == 251, "영업일 기준 251일"
