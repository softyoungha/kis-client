import logging
from datetime import date, datetime
from typing import Any, Dict, List, Literal, Optional, Union, overload

from kis.core.base.resources import Order
from kis.core.base.schema import ResponseData
from kis.core.enum import Exchange
from kis.exceptions import KISBadArguments, KISDevModeError, KISNoData
from kis.utils.tool import as_datetime

from .client import OverseasResource
from .schema import (
    BidAvailability,
    ExecutedOrder,
    OrderData,
    PrettyBidAvailability,
    PrettyExecutedOrder,
    PrettyUnExecutedOrder,
    UnExecutedOrder,
)

logger = logging.getLogger(__name__)


class OverseasOrder(OverseasResource, Order):
    """해외주식 주문 조회"""

    def _order(
        self,
        order_type: Literal["buy", "sell"],
        symbol: str,
        quantity: int,
        price: Optional[float] = None,
        order_division: Optional[str] = None,
        as_market_price: bool = False,
        exchange: Union[str, Exchange] = None,
    ) -> OrderData:
        """
        해외주식주문/해외주식 주문

        모의투자에서는 지정가만 사용할 수 있습니다.

        See https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_e4a7e5fd-eed5-4a85-93f0-f46b804dae5f

        :param order_type: 주문구분 (buy, sell)
        :param symbol: 종목코드
        :param quantity: 주문수량 (0을 입력하면 잔량 전부)
        :param price: 주문단가 (as_market_price가 True일 경우 무시)
        :param as_market_price: 시장가 주문 여부
        :param order_division: 주문구분 (00: 지정가, 01: 시장가, etc)
        :param exchange: 거래소
        """
        exchange = exchange or self.client.exchange
        if self.client.strict:
            exchange = Exchange.from_value(exchange)
        else:
            exchange = Exchange.find_symbol(symbol)

        account_prefix, account_suffix = self.client.get_account()

        if quantity is None:
            raise KISBadArguments("quantity is required")

        if order_type == "buy":
            if exchange in (Exchange.NAS, Exchange.NYS, Exchange.AMS):
                tr_id = "VTTT1002U" if self.is_dev else "JTTT1002U"
            elif exchange in (Exchange.TSE,):
                tr_id = "VTTS0308U" if self.is_dev else "TTTS0308U"
            elif exchange in (Exchange.SHS,):
                tr_id = "VTTS0202U" if self.is_dev else "TTTS0202U"
            elif exchange in (Exchange.HKS,):
                tr_id = "VTTS1002U" if self.is_dev else "TTTS1002U"
            elif exchange in (Exchange.SZS,):
                tr_id = "VTTS0305U" if self.is_dev else "TTTS0305U"
            else:
                tr_id = "VTTS0311U" if self.is_dev else "TTTS0311U"

        else:
            if exchange in (Exchange.NAS, Exchange.NYS, Exchange.AMS):
                tr_id = "VTTT1001U" if self.is_dev else "JTTT1006U"
            elif exchange in (Exchange.TSE,):
                tr_id = "VTTS0307U" if self.is_dev else "TTTS0307U"
            elif exchange in (Exchange.SHS,):
                tr_id = "VTTS1005U" if self.is_dev else "TTTS1005U"
            elif exchange in (Exchange.HKS,):
                tr_id = "VTTS1001U" if self.is_dev else "TTTS1001U"
            elif exchange in (Exchange.SZS,):
                tr_id = "VTTS0304U" if self.is_dev else "TTTS0304U"
            else:
                tr_id = "VTTS0310U" if self.is_dev else "TTTS0310U"

        if order_division:
            price = 0
        else:
            if as_market_price:
                price = 0
                order_division = "01"
            else:
                if not price:
                    raise KISBadArguments("price is required")
                order_division = "00"

        headers = {"tr_id": tr_id, "custtype": "P"}
        data = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "OVRS_EXCG_CD": exchange.code,
            "PDNO": symbol,
            "ORD_QTY": str(quantity),
            "OVRS_ORD_UNPR": str(price),
            "ORD_SVR_DVSN_CD": "0",
            "ORD_DVSN": order_division,
        }
        return self.client.send_order(
            "/uapi/overseas-stock/v1/trading/order",
            headers=headers,
            body=data,
            data_class=OrderData,
        ).data

    def buy(
        self,
        symbol: str,
        quantity: int,
        price: Optional[float] = None,
        order_division: Optional[str] = None,
        as_market_price: bool = False,
        exchange: Union[str, Exchange] = None,
    ) -> OrderData:
        """
        주식 매수

        :param symbol: 종목코드
        :param quantity: 주문수량 (입력하지 않을 경우 전량 구매)
        :param price: 주문단가 (as_market_price=True일 경우 무시)
        :param as_market_price: 시장가 주문 여부
        :param order_division: 주문구분 (00: 지정가, 01: 시장가, etc)
        :param exchange: 거래소
        """
        return self._order(
            order_type="buy",
            symbol=symbol,
            quantity=quantity,
            price=price,
            as_market_price=as_market_price,
            order_division=order_division,
            exchange=exchange,
        )

    def sell(
        self,
        symbol: str,
        quantity: int,
        price: Optional[float] = None,
        order_division: Optional[str] = None,
        as_market_price: bool = False,
        exchange: Union[str, Exchange] = None,
    ) -> OrderData:
        """
        주식 매도

        :param symbol: 종목코드
        :param quantity: 주문수량 (0을 입력하면 잔량 전부)
        :param price: 주문단가 (as_market_price가 True일 경우 무시)
        :param as_market_price: 시장가 주문 여부
        :param order_division: 주문구분 (00: 지정가, 01: 시장가, etc)
        :param exchange: 거래소
        """
        return self._order(
            order_type="sell",
            symbol=symbol,
            quantity=quantity,
            price=price,
            as_market_price=as_market_price,
            order_division=order_division,
            exchange=exchange,
        )

    def _modify(
        self,
        modify_type: str,
        org_no: str,
        order_no: str,
        symbol: str,
        quantity: int = None,
        price: Optional[float] = None,
        as_market_price: bool = False,
        exchange: Union[str, Exchange] = None,
    ):
        """
        주문 수정/취소

        ---

        해외주식주문/해외주식 정정취소주문

        See https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_4812f155-bdb5-47ac-a35b-a70d3d8f14c9

        :param modify_type: 주문구분 (cancel, update)
        :param org_no: 한국거래소주문조직번호
        :param order_no: 주문번호
        :param quantity: 주문수량
        :param total: True 잔량 전체, False 잔량 일부
        :param price: 가격
        :param as_market_price: 시장가 주문 여부
        :param exchange: 거래소
        """
        exchange = exchange or self.client.exchange
        if self.client.strict:
            exchange = Exchange.from_value(exchange)
        else:
            exchange = Exchange.find_symbol(symbol)

        account_prefix, account_suffix = self.client.get_account()

        if self.is_dev:
            if exchange in (Exchange.NAS, Exchange.NYS, Exchange.AMS):
                tr_id = "VTTT1004U"
            elif exchange in (Exchange.TSE,):
                tr_id = "VTTS0309U"
            elif exchange in (Exchange.SHS,):
                tr_id = "VTTS0302U"
            elif exchange in (Exchange.HKS,):
                tr_id = "VTTS1003U"
            elif exchange in (Exchange.SZS,):
                tr_id = "VTTS0306U"
            elif exchange in (Exchange.HNX,):
                tr_id = "VTTS0312U"
            else:
                raise KISBadArguments("exchange is not supported")
        else:
            if exchange in (Exchange.NAS, Exchange.NYS, Exchange.AMS):
                tr_id = "JTTT1004U"
            elif exchange in (Exchange.TSE,):
                tr_id = "TTTS0309U"
            elif exchange in (Exchange.SHS,):
                tr_id = "TTTS0302U"
            elif exchange in (Exchange.HKS,):
                tr_id = "TTTS1003U"
            elif exchange in (Exchange.SZS,):
                tr_id = "TTTS0306U"
            elif exchange in (Exchange.HNX,):
                tr_id = "TTTS0312U"
            else:
                raise KISBadArguments("exchange is not supported")

        if not price:
            raise KISBadArguments("price is required")

        if modify_type == "cancel":
            quantity = 0
            cancel_or_update_cd = "02"
        else:
            cancel_or_update_cd = "01"

        headers = {"tr_id": tr_id, "custtype": "P"}
        data = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "OVRS_EXCG_CD": exchange.code,
            "PDNO": symbol,
            "ORGN_ODNO": order_no,
            "RVSE_CNCL_DVSN_CD": cancel_or_update_cd,
            "ORD_QTY": str(quantity),
            "OVRS_ORD_UNPR": str(price),
            "MGCO_APTM_ODNO": "",
            "ORD_SVR_DVSN_CD": "0",
        }

        return self.client.send_order(
            "/uapi/overseas-stock/v1/trading/order-rvsecncl",
            headers=headers,
            body=data,
            data_class=OrderData,
        )

    @overload
    def get_available_amount(self, symbol: str, price: float) -> PrettyBidAvailability:
        ...

    @overload
    def get_available_amount(
        self, symbol: str, price: float, is_market_price: Literal[False]
    ) -> PrettyBidAvailability:
        ...

    @overload
    def get_available_amount(
        self, symbol: str, is_market_price: Literal[True]
    ) -> PrettyBidAvailability:
        ...

    def get_available_amount(
        self,
        symbol: str,
        price: float,
        exchange: Union[str, Exchange] = None,
    ):
        """
        주문 가능 금액 확인

        ---

        해외주식주문/해외주식 매수가능금액조회

        해외주식 매수가능금액조회 API입니다.
        ※ 모의투자는 사용 불가합니다.

        See https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_2a155fee-882f-4d80-8183-559f2f6983e9

        :param symbol: 종목코드
        :param price: 주문가격
        :param exchange: 거래소
        """
        if self.is_dev:
            raise KISDevModeError()

        exchange = exchange or self.client.exchange
        if self.client.strict:
            exchange = Exchange.from_value(exchange)
        else:
            exchange = Exchange.find_symbol(symbol)

        account_prefix, account_suffix = self.client.get_account()

        tr_id = "TTTS3007R" if self.client.is_day else "JTTT3007R"

        headers = {"tr_id": tr_id, "custtype": "P"}
        params = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "OVRS_EXCG_CD": exchange.code,
            "OVRS_ORD_UNPR": str(price),
            "ITEM_CD": symbol,
        }

        return self.client.fetch_data(
            "/uapi/overseas-stock/v1/trading/inquire-psamount",
            headers=headers,
            params=params,
            data_class=BidAvailability,
        ).data

    def _fetch_unfilled_orders(
        self,
        exchange: Union[str, Exchange] = None,
        fk200: str = "",
        nk200: str = "",
    ):
        """
        주문 정정/취소 가능 조회

        ---
        해외주식주문/해외주식 미체결내역

        접수된 해외주식 주문 중 체결되지 않은 미체결 내역을 조회하는 API입니다.

        See https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_60cae69d-c121-4dd9-902c-1112567fd88e

        :param exchange: 거래소 코드
        :param fk200: 연속조회검색조건200
        :param nk200: 연속조회키200
        """
        exchange = exchange or self.client.exchange
        if self.client.strict:
            exchange = Exchange.from_value(exchange)

        account_prefix, account_suffix = self.client.get_account()

        sort_sqn = "DS"
        if self.is_dev:
            if self.client.is_day:
                tr_id = "VTTS3018R"
            else:
                tr_id = "VTTT3018R"
        else:
            if self.client.is_day:
                tr_id = "TTTS3018R"
                sort_sqn = ""
            else:
                tr_id = "JTTT3018R"

        headers = {"tr_id": tr_id, "custtype": "P"}
        params = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "OVRS_EXCG_CD": exchange.code,
            "SORT_SQN": sort_sqn,
            "CTX_AREA_FK200": fk200,
            "CTX_AREA_NK200": nk200,
        }
        return self.client.fetch_data(
            "/uapi/overseas-stock/v1/trading/inquire-nccs",
            headers=headers,
            params=params,
            data_class=List[Dict[str, Any]],
        )

    def fetch_unexecuted_orders(
        self,
        exchange: Union[str, Exchange] = None,
    ) -> List[UnExecutedOrder]:
        """
        주문 정정/취소 가능 조회

        :param exchange: 거래소 코드
        """
        try:
            result = self._fetch_unfilled_orders(exchange=exchange)
        except KISNoData as err:
            logger.warning(err.msg)
            return []

        items = [UnExecutedOrder(**row) for row in result.data]

        while result.has_next:
            result = self._fetch_unfilled_orders(
                exchange=exchange,
                fk200=result.fk200,
                nk200=result.nk200,
            )
            items.extend([UnExecutedOrder(**row) for row in result.data])
        return items

    def _fetch_executed_orders(
        self,
        start_date: Union[str, datetime, date],
        end_date: Union[str, datetime, date],
        symbol: Optional[str] = None,
        order_type: Literal["all", "buy", "sell"] = "all",
        execution_type: Literal["all", "executed", "unexecuted"] = "all",
        exchange: Union[str, Exchange] = "%",
        reverse: bool = False,
        fk200: str = "",
        nk200: str = "",
    ):
        """
        기간별 주문체결내역 조회 once

        ---
        해외주식주문/해외주식 주문체결내역

        일정 기간의 해외주식 주문 체결 내역을 확인하는 API입니다.

        See https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_6d715b38-566f-4045-a08c-4a594d3a3314

        :param start_date: 조회 시작일 (YYYYMMDD)
        :param end_date: 조회 종료일 (YYYYMMDD)
        :param symbol: 종목코드
        :param order_type: 주문구분 (all, buy, sell)
        :param execution_type: 체결구분 (all, executed, unexecuted)
        :param exchange: 거래소 코드("%" 입력시 전종목 검색)
        :param fk200: 연속조회검색조건200
        :param nk200: 연속조회키200
        """
        if exchange != "%":
            exchange = Exchange.from_value(exchange or self.client.exchange)

        account_prefix, account_suffix = self.client.get_account()

        if self.is_dev:
            if self.client.is_day:
                tr_id = "VTTS3035R"
            else:
                tr_id = "VTTS3035R"
            order_division_code = "00"
            execution_type_code = "00"
        else:
            if self.client.is_day:
                tr_id = "TTTS3035R"
            else:
                tr_id = "JTTT3001R"

            if order_type == "buy":
                order_division_code = "02"
            elif order_type == "sell":
                order_division_code = "01"
            else:
                order_division_code = "00"

            if execution_type == "executed":
                execution_type_code = "01"
            elif execution_type == "unexecuted":
                execution_type_code = "02"
            else:
                execution_type_code = "00"

        headers = {"tr_id": tr_id, "custtype": "P"}
        params = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "PDNO": symbol or "%",
            "ORD_STRT_DT": as_datetime(start_date, fmt="%Y%m%d"),
            "ORD_END_DT": as_datetime(end_date, fmt="%Y%m%d"),
            "SLL_BUY_DVSN": order_division_code,
            "CCLD_NCCS_DVSN": execution_type_code,
            "OVRS_EXCG_CD": exchange.code or "%",
            "SORT_SQN": "DS" if reverse else "AS",
            "ORD_DT": "",
            "ORD_GNO_BRNO": "",
            "ODNO": "",
            "CTX_AREA_FK200": fk200,
            "CTX_AREA_NK200": nk200,
        }

        return self.client.fetch_data(
            "/uapi/overseas-stock/v1/trading/inquire-ccnl",
            headers=headers,
            params=params,
            data_class=List[Dict[str, Any]],
        )

    def fetch_executed_orders(
        self,
        start_date: Union[str, datetime, date],
        end_date: Union[str, datetime, date],
        symbol: Optional[str] = None,
        order_type: Literal["all", "buy", "sell"] = "all",
        execution_type: Literal["all", "executed", "unexecuted"] = "all",
        reverse: bool = False,
        exchange: Union[str, Exchange] = None,
    ) -> List[ExecutedOrder]:
        """
        기간별 주문체결내역 연속조회

        ---
        해외주식주문/해외주식 주문체결내역

        일정 기간의 해외주식 주문 체결 내역을 확인하는 API입니다

        See https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_6d715b38-566f-4045-a08c-4a594d3a3314
        """

        exchange = exchange or self.client.exchange
        if self.client.strict:
            exchange = Exchange.from_value(exchange)
        else:
            exchange = Exchange.find_symbol(symbol)

        options = dict(
            start_date=as_datetime(start_date, fmt="%Y%m%d"),
            end_date=as_datetime(end_date, fmt="%Y%m%d"),
            symbol=symbol,
            order_type=order_type,
            execution_type=execution_type,
            exchange=exchange,
            reverse=reverse,
        )

        # fetch first
        try:
            result = self._fetch_executed_orders(**options)
        except KISNoData as err:
            logger.warning(err.msg)
            return []

        items = [ExecutedOrder(**row) for row in result.data]

        # fetch continuously
        while result.has_next:
            result = self._fetch_executed_orders(
                **options,
                fk200=result.fk200,
                nk200=result.nk200,
            )
            items.extend([ExecutedOrder(**row) for row in result.data])
        return items
