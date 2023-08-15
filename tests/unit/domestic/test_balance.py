from kis.core.domestic import DomesticClient


class TestDomesticBalance:
    def test_fetch_balance(self, domestic_client: "DomesticClient"):
        """주식 잔고를 조회합니다"""
        portfolio, deposit = domestic_client.balance.fetch()
        # pprint(deposit[0].Pretty.dict())
        assert len(deposit) >= 1
