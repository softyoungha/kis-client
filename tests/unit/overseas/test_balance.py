from pprint import pprint


class TestOverseasBalance:
    def test_fetch_balance(self, overseas_client, apple):
        """주식 잔고를 조회합니다"""
        portfolio = overseas_client.balance.fetch()

        for stock in portfolio:
            pprint(stock.pretty.dict())
            assert stock.pretty.symbol == apple
