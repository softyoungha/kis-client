from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kis.core.domestic import DomesticClient


class TestDomesticQuote:
    def test_fetch_price(self, domestic_client: "DomesticClient", samsung: str):
        """현재가를 조회합니다."""
        price = domestic_client.quote.fetch_current_price(samsung)
        assert price.pretty.symbol == samsung

    def test_fetch_prices_by_minutes(
        self, domestic_client: "DomesticClient", samsung: str
    ):
        """오늘의 분단위 시세를 조회합니다."""
        summary, full_histories = domestic_client.quote.fetch_prices_by_minutes(
            samsung, to="123000"
        )
        assert summary.symbol_name == "삼성전자"

    def test_fetch_ohlcv_daily(self, domestic_client: "DomesticClient", samsung: str):
        """일봉 시세를 조회합니다"""
        summary, detail = domestic_client.quote.fetch_histories(
            samsung, end_date="20230101", standard="D"
        )
        assert summary.symbol_name == "삼성전자"
        assert summary.price_lowest <= summary.price_open <= summary.price_highest

    def test_fetch_ohlcv_weekly(self, domestic_client: "DomesticClient", samsung: str):
        """주봉 시세를 조회합니다."""
        summary, detail = domestic_client.quote.fetch_histories(
            samsung, end_date="20230101", standard="W"
        )
        assert summary.symbol_name == "삼성전자"
        assert summary.price_lowest <= summary.price_open <= summary.price_highest

    def test_fetch_ohlcv_monthly(self, domestic_client: "DomesticClient", samsung: str):
        """월봉 시세를 조회합니다."""
        summary, detail = domestic_client.quote.fetch_histories(
            samsung, end_date="20230101", standard="M"
        )
        assert summary.symbol_name == "삼성전자"
        assert summary.price_lowest <= summary.price_open <= summary.price_highest

    def test_fetch_ohlcv_year(self, domestic_client: "DomesticClient", samsung: str):
        """년봉 시세를 조회합니다."""
        summary, detail = domestic_client.quote.fetch_histories(
            samsung, end_date="20230101", standard="Y"
        )
        # print(summary)
        assert summary.symbol_name == "삼성전자"
        assert summary.price_lowest <= summary.price_open <= summary.price_highest
        assert len(detail) < 50, "year 단위로 50개를 넘지 못함"

    def test_fetch_all_ohlcv_monthly(
        self, domestic_client: "DomesticClient", samsung: str
    ):
        """모든 월봉 시세를 조회합니다."""
        summary, detail = domestic_client.quote.fetch_histories(
            samsung, start_date="20220101", end_date="20230101", standard="M"
        )
        assert len(detail) == 12, "12개월"

    def test_fetch_all_ohlcv_monthly_2(
        self, domestic_client: "DomesticClient", samsung: str
    ):
        """모든 월봉 시세를 조회합니다."""
        summary, detail = domestic_client.quote.fetch_histories(
            samsung, start_date="20200101", end_date="20230306", standard="M"
        )
        assert len(detail) == 38, "12 * 3 + 2개월"

    def test_fetch_all_ohlcv_daily(
        self, domestic_client: "DomesticClient", samsung: str
    ):
        """모든 일봉 시세를 조회합니다."""
        summary, detail = domestic_client.quote.fetch_histories(
            samsung, start_date="20220101", end_date="20230101", standard="D"
        )
        assert len(detail) == 246, "영업일 기준 246일"
