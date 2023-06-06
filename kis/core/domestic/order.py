from datetime import datetime, date
from typing import Optional, Literal, List, Any, Dict, Union, overload, Tuple

from kis.core.base.resources import Order
from kis.exceptions import KISBadArguments, KISDevModeError
from kis.utils.tool import as_datetime
from .client import DomesticResource
from .schema import (
    OrderData,
    UnExecutedOrder,
    BidAvailability,
    ExecutedOrderSummary,
    ExecutedOrderDetail
)

order_division_map = {
    "지정가": "01",
    "시장가": "02",
    "조건부지정가": "03",
    "최유리지정가": "04",
    "최우선지정가": "05",
    "장전시간외": "06",
    "장후시간외": "07",
    "시간외단일가": "08",
    "자기주식": "09",
    "자기주식S-Option": "10",
    "자기주식금전신탁": "11",
    "IOC지정가": "12",
    "FOK지정가": "13",
    "IOC시장가": "14",
    "FOK시장가": "15",
    "IOC최유리": "16",
    "FOK최유리": "17"
}


class DomesticOrder(DomesticResource, Order):
    """국내 주문 조회"""

    def _order(
            self,
            order_type: Literal["buy", "sell"],
            symbol: str,
            quantity: int,
            price: Optional[int] = None,
            order_division: Optional[str] = None,
            as_market_price: bool = False,
            **kwargs
    ) -> OrderData:
        """
        국내주식주문/주식주문(현금)

        ---

        국내주식주문(현금) API 입니다.

        See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_aade4c72-5fb7-418a-9ff2-254b4d5f0ceb

        :param order_type: 주문구분 (buy, sell)
        :param symbol: 종목코드
        :param quantity: 주문수량
        :param price: 주문단가
        :param as_market_price: 시장가 주문 여부
        :param order_division: 주문구분 (00: 지정가, 01: 시장가, etc)
        """
        account_prefix, account_suffix = self.client.get_account()

        if quantity is None:
            raise KISBadArguments("quantity is required")

        if order_type == "buy":
            tr_id = "VTTC0802U" if self.is_dev else "TTTC0802U"

        else:
            tr_id = "VTTC0801U" if self.is_dev else "TTTC0801U"

        if order_division:
            if order_division in order_division_map.keys():
                order_division = order_division_map[order_division]
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
            "PDNO": symbol,
            "ORD_DVSN": order_division,
            "ORD_QTY": str(quantity),
            "ORD_UNPR": str(price)
        }
        return self.client.send_order(
            "/uapi/domestic-stock/v1/trading/order-cash",
            headers=headers,
            body=data,
            data_class=OrderData
        ).data

    def buy(
            self,
            symbol: str,
            quantity: int,
            price: Optional[int] = None,
            order_division: Optional[str] = None,
            as_market_price: bool = False,
            **kwargs
    ) -> OrderData:
        return super().buy(
            symbol=symbol,
            quantity=quantity,
            price=price,
            order_division=order_division,
            as_market_price=as_market_price,
            exchange=None,
        )

    def sell(
            self,
            symbol: str,
            quantity: Optional[int] = None,
            price: Optional[int] = None,
            order_division: Optional[str] = None,
            as_market_price: bool = False,
            **kwargs
    ) -> OrderData:
        return super().sell(
            symbol=symbol,
            quantity=quantity,
            price=price,
            order_division=order_division,
            as_market_price=as_market_price,
            exchange=None,
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
            order_division: str = None,
    ) -> OrderData:
        """
        국내주식주문/주식주문(정정취소)

        ---

        주문 건에 대하여 정정 및 취소하는 API입니다.
        단, 이미 체결된 건은 정정 및 취소가 불가합니다.

        See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_4bfdfb2b-34a7-43f6-935a-e637724f960a

        :param modify_type: 주문구분 (cancel, update)
        :param org_no: 한국거래소주문조직번호
        :param order_no: 주문번호
        :param quantity: 주문수량
        :param total: True 잔량 전체, False 잔량 일부
        :param price: 가격
        :param as_market_price: 시장가 주문 여부
        :param order_division: 주문구분 (00: 지정가, 01: 시장가, etc)
                See ORD_DVSN. https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_4bfdfb2b-34a7-43f6-935a-e637724f960a
        """
        account_prefix, account_suffix = self.client.get_account()

        tr_id = "VTTC0803U" if self.is_dev else "TTTC0803U"

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
            "ORD_DVSN": order_division,
            "RVSE_CNCL_DVSN_CD": cancel_or_update_cd,
            "ORD_QTY": str(quantity),
            "ORD_UNPR": str(price),
            "QTY_ALL_ORD_YN": is_total,
        }
        return self.client.send_order(
            "/uapi/domestic-stock/v1/trading/order-rvsecncl",
            headers=headers,
            body=data,
            data_class=OrderData
        ).data

    def update(
            self,
            org_no: str, order_no: str,
            quantity: Optional[int] = None, price: Optional[int] = None,
            total: bool = False, as_market_price: bool = False
    ):
        """
        주식 정정

        :param org_no: 한국거래소주문조직번호
        :param order_no: 주문번호
        :param quantity: 정정수량
        :param price: 정정단가
        :param total: 전량 정정 여부
        :param as_market_price: 시장가 주문 여부
        """
        return self._modify(
            modify_type="update",
            org_no=org_no,
            order_no=order_no,
            quantity=quantity,
            total=total,
            price=price,
            as_market_price=as_market_price
        )

    def cancel(
            self,
            org_no: str,
            order_no: str,
            quantity: Optional[int] = None,
            total: bool = False,
    ):
        """
        주식 취소

        :param org_no: 한국거래소주문조직번호
        :param order_no: 주문번호
        :param quantity: 취소수량
        :param total: 전량 취소 여부
        """
        return self._modify(
            modify_type="cancel",
            org_no=org_no,
            order_no=order_no,
            quantity=quantity,
            total=total,
        )

    @overload
    def get_available_amount(
            self,
            symbol: str,
            price: int
    ) -> BidAvailability:
        ...

    @overload
    def get_available_amount(
            self,
            symbol: str,
            price: int,
            is_market_price: Literal[False]
    ) -> BidAvailability:
        ...

    def get_available_amount(
            self,
            symbol: str,
            price: Optional[int] = None,
            is_market_price: bool = False,
            order_division_code: Optional[str] = None,
            contain_cma: bool = True,
            contain_overseas: bool = True,
    ):
        """
        주문 가능 금액 확인

        ---

        국내주식주문/매수가능조회

        매수가능 조회 API입니다. 실전계좌/모의계좌의 경우, 한 번의 호출에 최대 1건까지 확인 가능합니다

        See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_806e407c-3082-44c0-9d71-e8534db5ad54

        :param symbol: 종목코드
        :param price: 주문가격
        :param is_market_price: 시장가 주문 여부
        :param order_division_code: 주문구분 (00: 지정가, 01: 시장가, etc)
        :param contain_cma: CMA 포함 여부
        :param contain_overseas: 해외주식 포함 여부
        """
        account_prefix, account_suffix = self.client.get_account()

        tr_id = "VTTC8908R" if self.is_dev else "TTTC8908R"
        if order_division_code:
            price = 0
        else:
            if is_market_price:
                price = 0
                order_division_code = "01"
            else:
                order_division_code = "00"
        contain_cma = "Y" if contain_cma else "N"
        contain_overseas = "Y" if contain_overseas else "N"

        headers = {"tr_id": tr_id, "custtype": "P"}
        params = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "PDNO": symbol,
            "ORD_UNPR": str(price),
            "ORD_DVSN": order_division_code,
            "CMA_EVLU_AMT_ICLD_YN": contain_cma,  # CMA 평가금액 포함여부
            "OVRS_ICLD_YN": contain_overseas  # 해외포함여부
        }

        return self.client.fetch_data(
            "/uapi/domestic-stock/v1/trading/inquire-psbl-order",
            headers=headers,
            params=params,
            data_class=BidAvailability
        ).data

    def _fetch_unexecuted_orders(
            self,
            sort_by: Literal["order_no", "symbol", None] = None,
            order_type: Literal["all", "buy", "sell"] = "all",
            fk100: str = "",
            nk100: str = "",
    ):
        """
        주문 미체결 내역 조회

        ---

        국내주식주문/주식정정취소가능주문조회

        See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_d4537e9c-73f7-414c-9fb0-4eae3bc397d0

        :param sort_by: 정렬기준 (order_no, symbol)
        :param order_type: 주문구분 (buy, sell)
        :param fk100: 연속조회검색조건100
        :param nk100: 연속조회키100
        """
        if self.is_dev:
            raise KISDevModeError("Not supported in dev mode")

        account_prefix, account_suffix = self.client.get_account()

        if sort_by == "order_no":
            sort_by_code = "1"
        elif sort_by == "symbol":
            sort_by_code = "2"
        else:
            sort_by_code = "0"

        if order_type == "buy":
            order_division_code = "2"
        elif order_type == "sell":
            order_division_code = "1"
        else:
            order_division_code = "0"

        headers = {"tr_id": "TTTC8036R", "custtype": "P"}
        params = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "CTX_AREA_FK100": fk100,
            "CTX_AREA_NK100": nk100,
            "INQR_DVSN_1": sort_by_code,
            "INQR_DVSN_2": order_division_code
        }

        return self.client.fetch_data(
            "/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl",
            headers=headers,
            params=params,
            data_class=List[Dict[str, Any]]
        )

    def fetch_unexecuted_orders(
            self,
            sort_by: Literal["order_no", "symbol", None] = None,
            order_type: Literal["all", "buy", "sell"] = "all",
    ) -> List[UnExecutedOrder]:
        """
        주문 정정/취소 가능 조회

        :param sort_by: 정렬기준 (order_no, symbol)
        :param order_type: 주문구분 (buy, sell)
        """

        result = self._fetch_unexecuted_orders(
            sort_by=sort_by,
            order_type=order_type,
        )

        items = [UnExecutedOrder(**row) for row in result.data]

        while result.has_next:
            result = self._fetch_unexecuted_orders(
                sort_by=sort_by,
                order_type=order_type,
                fk100=result.fk100,
                nk100=result.nk100,
            )
            items.extend([UnExecutedOrder(**row) for row in result.data])
        return items

    def _fetch_executed_orders(
            self,
            start_date: Union[str, datetime, date],
            end_date: Union[str, datetime, date],
            order_type: Literal["all", "buy", "sell"] = "all",
            execution_type: Literal["all", "executed", "unexecuted"] = "all",
            symbol: Optional[str] = None,
            reverse: bool = False,
            fk100: str = "",
            nk100: str = "",
    ):
        """
        일자별 체결내역 조회 once

        ---

        국내주식주문/주식일별주문체결조회

        See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_bc51f9f7-146f-4971-a5ae-ebd574acec12

        :param start_date: 조회시작일
        :param end_date: 조회종료일
        :param order_type: 조회할 주문 타입 (all, buy, sell)
        :param execution_type: 조회할 주문 체결 여부 (all, executed, unexecuted)
        :param symbol: 종목코드
        :param reverse: 역순으로 조회할지 여부
        :param fk100: 연속조회검색조건100
        :param nk100: 연속조회키100
        """
        tr_id = "VTTC8001R" if self.is_dev else "TTTC8001R"

        account_prefix, account_suffix = self.client.get_account()

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
            "INQR_STRT_DT": as_datetime(start_date, fmt="%Y%m%d"),
            "INQR_END_DT": as_datetime(end_date, fmt="%Y%m%d"),
            "SLL_BUY_DVSN_CD": order_division_code,
            "INQR_DVSN": "00" if reverse else "01",
            "PDNO": symbol or "",
            "CCLD_DVSN": execution_type_code,
            "ORD_GNO_BRNO": "",
            "ODNO": "",
            "INQR_DVSN_1": "",
            "INQR_DVSN_3": "00",
            "CTX_AREA_FK100": fk100,
            "CTX_AREA_NK100": nk100,
        }
        return self.client.fetch_data(
            "/uapi/domestic-stock/v1/trading/inquire-daily-ccld",
            headers=headers,
            params=params,
            summary_class=List[Dict[str, Any]],
            detail_class=ExecutedOrderDetail,
        )

    def fetch_executed_orders(
            self,
            start_date: Union[str, datetime, date],
            end_date: Union[str, datetime, date],
            order_type: Literal["all", "buy", "sell"] = "all",
            execution_type: Literal["all", "executed", "unexecuted"] = "all",
            symbol: Optional[str] = None,
            reverse: bool = False,
    ) -> Tuple[List[ExecutedOrderSummary], ExecutedOrderDetail]:
        """
        일자별 체결내역 연속조회

        ---

        국내주식주문/주식일별주문체결조회

        See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_bc51f9f7-146f-4971-a5ae-ebd574acec12

        :param start_date: 조회시작일
        :param end_date: 조회종료일
        :param order_type: 조회할 주문 타입 (all, buy, sell)
        :param execution_type: 조회할 주문 체결 여부 (all, executed, unexecuted)
        :param symbol: 종목코드
        :param reverse: 역순 조회 여부
        """
        options = dict(
            start_date=as_datetime(start_date, fmt="%Y%m%d"),
            end_date=as_datetime(end_date, fmt="%Y%m%d"),
            order_type=order_type,
            execution_type=execution_type,
            symbol=symbol,
            reverse=reverse,
        )

        result = self._fetch_executed_orders(**options)

        summary_items = [ExecutedOrderSummary(**row) for row in result.summary]

        while result.has_next:
            result = self._fetch_executed_orders(
                **options,
                fk100=result.fk100,
                nk100=result.nk100,
            )
            summary_items.extend([ExecutedOrderSummary(**row) for row in result.summary])
            print(result.detail)

        return summary_items, result.detail
