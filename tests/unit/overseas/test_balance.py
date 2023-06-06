from pprint import pprint

class TestOverseasBalance:

    def test_fetch_balance(self, overseas_client, apple):
        portfolio = overseas_client.balance.fetch()

        for stock in portfolio:
            pprint(stock.custom.dict())
            assert stock.custom.symbol == apple

