from kis.core.domestic import DomesticClient


class TestDomesticBalance:

    def test_fetch_balance(self, domestic_client):
        portfolio, deposit = domestic_client.balance.fetch()
        # pprint(deposit[0].custom.dict())
        assert len(deposit) >= 1
