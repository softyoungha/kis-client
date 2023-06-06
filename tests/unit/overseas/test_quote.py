from kis.core.overseas import OverseasClient


class TestOverseasQuote:

    def test_fetch_price(self, overseas_client, apple):
        price = overseas_client.quote.fetch_current_price(apple)
        assert price.custom.symbol == apple

    def test_fetch_price_detail(self, overseas_client, apple):
        if overseas_client.is_dev:
            return

        price = overseas_client.quote.fetch_current_price_detail(apple)
        print(price)
        assert price.data.symbol == apple

    def test_fetch_ohlcv_daily(self, overseas_client, apple):
        summary, detail = overseas_client.quote.fetch_histories(
            apple,
            end_date="20230101",
            standard="D"
        )
        assert summary.symbol == "AAPL"
        assert detail[0].low <= detail[0].open <= detail[0].high

    def test_fetch_ohlcv_weekly(self, overseas_client, apple):
        summary, detail = overseas_client.quote.fetch_histories(
            apple,
            start_date="20070820",
            end_date="20230101",
            standard="W"
        )
        assert summary.symbol == "AAPL"
        assert detail[0].low <= detail[0].open <= detail[0].high
        assert len(detail) == 802
        assert detail[-1].business_date.strftime("%Y%m%d") == "20070820"
        assert detail[0].business_date.strftime("%Y%m%d") == "20221227"

    def test_fetch_ohlcv_monthly(self, overseas_client, apple):
        summary, detail = overseas_client.quote.fetch_histories(
            apple,
            end_date="20230101",
            standard="M"
        )
        assert summary.symbol == "AAPL"
        assert detail[0].low <= detail[0].open <= detail[0].high
        assert len(detail) == 186
        assert detail[-1].business_date.strftime("%Y%m%d") == "20070831"
        assert detail[0].business_date.strftime("%Y%m%d") == "20221230"

    def test_fetch_all_ohlcv_monthly(self, overseas_client, apple):
        summary, detail = overseas_client.quote.fetch_histories(
            apple,
            start_date="20220101",
            end_date="20230101",
            standard="M"
        )
        assert len(detail) == 12, "12개월"

    def test_fetch_all_ohlcv_monthly_2(self, overseas_client, apple):
        summary, detail = overseas_client.quote.fetch_histories(
            apple,
            start_date="20200101",
            end_date="20230306",
            standard="M"
        )
        assert len(detail) == 39, "12 * 3 + 3개월"

    def test_fetch_all_ohlcv_daily(self, overseas_client, apple):
        summary, detail = overseas_client.quote.fetch_histories(
            apple,
            start_date="20220101",
            end_date="20230101",
            standard="D"
        )
        assert len(detail) == 251, "영업일 기준 251일"

