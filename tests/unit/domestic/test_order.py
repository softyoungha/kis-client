from datetime import datetime
import pytest
from kis.core.domestic import DomesticClient, NAMED_SYMBOLS

class TestDomesticBalance:

    def test_get_available_amount(self, domestic_client, samsung):
        data = domestic_client.order.get_available_amount(
            symbol=samsung,
            price=65500
        )
        print(data)
        assert data

    def test_fetch_unexecuted_orders(self, domestic_client):
        orders = domestic_client.order.fetch_unexecuted_orders()
        print(orders)
        assert orders

    def test_fetch_executed_orders(self, domestic_client):
        orders, details = domestic_client.order.fetch_executed_orders(
            '20230301',
            '20230401',
            order_type="all",
            execution_type="all",
        )
        print(orders)
        assert orders

    def test_order_price(self, domestic_client, samsung):
        price = domestic_client.quote.fetch_current_price(samsung)
        print(price.current)

        result = domestic_client.order.buy(
            samsung,
            price=int(price.current),
            quantity=10,
        )
        print(result)
        pytest.shared["order_specified_price"] = result

    def test_order_as_market_price(self, domestic_client, samsung):
        result = domestic_client.order.buy(
            samsung,
            quantity=10,
            as_market_price=True
        )
        print(result)
        pytest.shared["order_market_price"] = result

    def test_fetch_orders(self, domestic_client):
        orders = domestic_client.order.fetch_unexecuted_orders()
        assert orders
        assert pytest.shared["order_specified_price"] in [order.order_no for order in orders]
        assert pytest.shared["order_market_price"] in [order.order_no for order in orders]

    def test_update_order(self, domestic_client):
        order = pytest.shared["order_specified_price"]
        result = domestic_client.order.update(
            org_no=order.org_no,
            order_no=order.order_no,
            quantity=5
        )

        orders = domestic_client.order.fetch_unexecuted_orders()
        for order in orders:
            if order.order_no == result.order_no:
                assert order.modify_type == "update"
                assert order.quantity == 5
                break

    def test_cancel(self, domestic_client):
        order = pytest.shared["order_specified_price"]
        result = domestic_client.order.cancel(
            org_no=order.org_no,
            order_no=order.order_no,
            quantity=3,
        )

        orders = domestic_client.order.fetch_unexecuted_orders()
        for order in orders:
            if order.order_no == result.order_no:
                assert order.modify_type == "cancel"
                break

    def test_fetch_order(self, domestic_client):
        result = domestic_client.order.fetch_executed_orders(
            start_date=datetime.now(),
            end_date=datetime.now(),
            order_type="buy"
        )
        assert result
