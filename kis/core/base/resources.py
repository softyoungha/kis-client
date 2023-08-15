"""국내/해외 주식 관련 API 리소스 모델을 추상화합니다."""
from .client import KisClientBase


class Resource:
    def __init__(self, client: KisClientBase):
        self.client = client


class Quote(Resource):
    """가격 조회 관련 API"""

    def fetch_current_price(self, *args, **kwargs):
        """현재가 조회"""
        raise NotImplementedError("fetch_current_price not implemented")

    def fetch_histories(self, *args, **kwargs):
        """기간별 시세 조회"""
        raise NotImplementedError("fetch_all_ohlcv not implemented")


class Order(Resource):
    """주문관련 API"""

    def _order(self, *args, **kwargs):
        """주문 전송"""
        raise NotImplementedError("_order not implemented")

    def buy(self, *args, **kwargs):
        """주식 매수"""
        raise NotImplementedError("buy not implemented")

    def sell(self, *args, **kwargs):
        """주식 매도"""
        raise NotImplementedError("sell not implemented")

    def _modify(self, *args, **kwargs):
        """주문 수정/취소"""
        raise NotImplementedError("modify not implemented")

    def update(self, *args, **kwargs):
        """주식 정정"""
        raise NotImplementedError("update not implemented")

    def cancel(self, *args, **kwargs):
        """주식 취소"""
        raise NotImplementedError("cancel not implemented")

    def get_available_amount(self, *args, **kwargs):
        """주식 주문가능금액 조회"""
        raise NotImplementedError("check_available_amount not implemented")

    def fetch_unexecuted_orders(self, **kwargs):
        """미체결내역 조회"""
        raise NotImplementedError("fetch_unfilled_orders not implemented")

    def fetch_executed_orders(self, **kwargs):
        """기간별 체결내역 조회"""
        raise NotImplementedError("fetch_filled_orders not implemented")


class Balance(Resource):
    """잔고 조회 관련 API"""

    def fetch(self):
        """주식 잔고 조회"""
        raise NotImplementedError("fetch not implemented")
