from typing import Optional
from kis.base.client import Order
from kis.base import fetch, order
from kis.exceptions import KISBadArguments
from .schema import OrderData, FetchOrdersData


class DomesticOrder(Order):
    """국내 주문 조회"""

    @order(
        "/uapi/domestic-stock/v1/trading/order-cash",
        data_class=OrderData
    )
    def _order(
            self,
            order_type: str,
            symbol: str,
            quantity: int,
            price: int = None,
            as_market_price: bool = False,
    ):
        """
        주문 전송
        :param order_type: 주문구분 (buy, sell)
        :param symbol: 종목코드
        :param quantity: 주문수량
        :param price: 주문단가
        :param as_market_price: 시장가 주문 여부
        """
        account_prefix, account_suffix = self.client.account_split

        if order_type == "buy":
            tr_id = "VTTC0802U" if self.client.is_dev else "TTTC0802U"

        else:
            tr_id = "VTTC0801U" if self.client.is_dev else "TTTC0801U"

        if as_market_price:
            price = 0
            order_code = "01"
        else:
            if not price:
                raise KISBadArguments("price is required")
            order_code = "00"

        headers = {"tr_id": tr_id, "custtype": "P"}
        data = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "PDNO": symbol,
            "ORD_DVSN": order_code,
            "ORD_QTY": str(quantity),
            "ORD_UNPR": str(price)
        }
        return headers, data

    @order(
        "/uapi/domestic-stock/v1/trading/order-rvsecncl",
        data_class=OrderData
    )
    def _modify(
            self,
            modify_type: str,
            org_no: str,
            order_no: str,
            quantity: int = None,
            total: bool = False,
            price: int = None,
            as_market_price: bool = False,
    ):
        """
        주문 수정/취소
        :param modify_type: 주문구분 (cancel, update)
        :param org_no: 한국거래소주문조직번호
        :param order_no: 주문번호
        :param quantity: 주문수량
        :param total: True 잔량 전체, False 잔량 일부
        :param price: 가격
        :param as_market_price: 시장가 주문 여부
        """
        account_prefix, account_suffix = self.client.account_split

        tr_id = "VTTC0803U" if self.client.is_dev else "TTTC0803U"

        if as_market_price:
            price = 0
            order_code = "01"
        else:
            if not price:
                raise KISBadArguments("price is required")
            order_code = "00"

        if total:
            quantity = 0
            is_total = "Y"
        else:
            if not quantity:
                raise KISBadArguments("quantity is required")
            if quantity <= 0:
                raise KISBadArguments("quantity must be greater than 0")
            is_total = "N"

        if modify_type == "cancel":
            quantity = 0
            cancel_or_update_cd = "02"
        else:
            cancel_or_update_cd = "01"

        headers = {"tr_id": tr_id, "custtype": "P"}
        data = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "KRX_FWDG_ORD_ORGNO": org_no,
            "ORGN_ODNO": order_no,
            "ORD_DVSN": order_code,
            "RVSE_CNCL_DVSN_CD": cancel_or_update_cd,
            "ORD_QTY": str(quantity),
            "ORD_UNPR": str(price),
            "QTY_ALL_ORD_YN": is_total,
        }
        return headers, data

    @fetch(
        "uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl",
        data_class=FetchOrdersData
    )
    def fetch_orders(
            self,
            order_no: str,
            order_by: Optional[str] = None,
            order_type: Optional[str] = None,
            fk100: str = "",
            nk100: str = "",
    ):
        """
        주문 정정/취소 가능 조회
        :param order_no: 주문번호
        :param order_by: 정렬기준 (order_no, symbol)
        :param order_type: 주문구분 (buy, sell)
        :param fk100: 연속조회검색조건100
        :param nk100: 연속조회키100
        """
        if self.client.is_dev:
            raise KISBadArguments("Not supported in dev mode")

        account_prefix, account_suffix = self.client.account_split

        if order_by == "order_no":
            order_by_code = "1"
        elif order_by == "symbol":
            order_by_code = "2"
        else:
            order_by_code = "0"

        if order_type == "buy":
            order_type_code = "2"
        elif order_type == "sell":
            order_type_code = "1"
        else:
            order_type_code = "0"

        headers = {"tr_id": "TTTC8036R", "custtype": "P"}
        params = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "CTX_AREA_FK100": fk100,
            "CTX_AREA_NK100": nk100,
            "INQR_DVSN_1": order_by_code,
            "INQR_DVSN_2": order_type_code
        }
        return headers, params

    @fetch(
        "/uapi/domestic-stock/v1/trading/inquire-psbl-order",
        # TODO data_class=FetchOrdersData
    )
    def check_buy(
            self,
            symbol: str,
            price: int = None,
            is_market_price: bool = False,
            contain_cma: bool = True,
            contain_overseas: bool = True,
    ):
        """
        주문 가능 여부
        :param symbol: 종목코드
        :param price: 주문가격
        :param is_market_price: 시장가 주문 여부
        :param contain_cma: CMA 포함 여부
        :param contain_overseas: 해외주식 포함 여부
        """
        account_prefix, account_suffix = self.client.account_split

        tr_id = "VTTC8908R" if self.client.is_dev else "TTTC8908R"
        if is_market_price:
            price = 0
            order_type_code = "01"
        else:
            order_type_code = "00"
        contain_cma = "Y" if contain_cma else "N"
        contain_overseas = "Y" if contain_overseas else "N"

        headers = {"tr_id": tr_id, "custtype": "P"}
        params = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "PDNO": symbol,
            "ORD_UNPR": str(price),
            "ORD_DVSN": order_type_code,
            "CMA_EVLU_AMT_ICLD_YN": contain_cma,  # CMA 평가금액 포함여부
            "OVRS_ICLD_YN": contain_overseas  # 해외포함여부
        }
        return headers, params
