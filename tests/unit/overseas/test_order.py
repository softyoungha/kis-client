import pytest
from kis.core.overseas import OverseasClient, NAMED_SYMBOLS
from datetime import datetime


class TestOverseasBalance:

    def test_get_available_amount(self, overseas_client, apple):
        if overseas_client.is_dev:
            return

        price = overseas_client.quote.fetch_current_price(apple).custom

        data = overseas_client.order.get_available_amount(
            symbol=apple,
            price=price.current,
        )
        assert data

    def test_fetch_unfilled_orders(self, overseas_client):
        orders = overseas_client.order.fetch_unexecuted_orders()
        assert orders

    def test_fetch_filled_orders(self, overseas_client):
        orders = overseas_client.order.fetch_executed_orders(
            '20230501',
            '20230502',
            order_type="all",
            execution_type="all",
        )
        for order in orders:
            # print(order)
            print(order.custom)
        assert orders

    def test_order_price(self, overseas_client, apple):
        price = overseas_client.quote.fetch_current_price(apple).custom
        print(price.current)

        result = overseas_client.order.buy(
            apple,
            price="165",
            quantity=10,
        )
        print(result)
        pytest.shared["order_specified_price"] = result

    def test_order_as_market_price(self, overseas_client, apple):
        if overseas_client.is_dev:
            return

        result = overseas_client.order.buy(
            apple,
            quantity=10,
            as_market_price=True
        )
        pytest.shared["order_market_price"] = result

    def test_fetch_orders(self, overseas_client):
        orders = overseas_client.order.fetch_unexecuted_orders()
        orders = [order.custom for order in orders]
        assert orders
        assert pytest.shared["order_specified_price"] in [order.order_no for order in orders]
        assert pytest.shared["order_market_price"] in [order.order_no for order in orders]

    def test_update_order(self, overseas_client):
        order = pytest.shared["order_specified_price"]
        result = overseas_client.order.update(
            org_no=order.org_no,
            order_no=order.order_no,
            quantity=5
        )

        orders = overseas_client.order.fetch_unexecuted_orders()
        orders = [order.custom for order in orders]
        for order in orders:
            if order.order_no == result.order_no:
                assert order.modify_type == "update"
                assert order.quantity == 5
                break

    def test_cancel(self, overseas_client):
        order = pytest.shared["order_specified_price"]
        result = overseas_client.order.cancel(
            org_no=order.org_no,
            order_no=order.order_no,
            quantity=3,
        )

        orders = overseas_client.order.fetch_unexecuted_orders()
        orders = [order.custom for order in orders]
        for order in orders:
            if order.order_no == result.order_no:
                assert order.modify_type == "cancel"
                break

    def test_fetch_executed_orders(self, overseas_client):
        result = overseas_client.order.fetch_executed_orders(
            start_date='20230401',
            end_date='20230502',
            order_type="buy"
        )
        for order in result:
            print(order.custom)
