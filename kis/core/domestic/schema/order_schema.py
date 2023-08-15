from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel, Field, validator


class OrderData(BaseModel):
    """
    국내주식주문/주식주문(현금) - Response Body output 응답상세 (Pretty Columns)

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_aade4c72-5fb7-418a-9ff2-254b4d5f0ceb
    """

    org_no: str = Field(alias="KRX_FWDG_ORD_ORGNO", title="한국거래소주문조직번호", example="")
    order_no: str = Field(alias="ODNO", title="주문번호", example="")
    order_time: time = Field(alias="ORD_TMD", title="주문시각", example="")

    def __repr__(self):
        return (
            f"OrderData("
            f"org_no='{self.org_no}', "
            f"order_no='{self.order_no}', "
            f"order_time='{self.order_time}')"
        )

    @validator("order_time", pre=True)
    def set_time(cls, value: str) -> time:
        return datetime.strptime(value, "%H%M%S").time()


class BidAvailability(BaseModel):
    """
    국내주식주문/매수가능조회 - Response Body output 응답상세

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_806e407c-3082-44c0-9d71-e8534db5ad54
    """

    ord_psbl_cash: float = Field(title="주문가능현금")
    ord_psbl_sbst: float = Field(title="주문가능대용")
    ruse_psbl_amt: float = Field(title="재사용가능금액")
    fund_rpch_chgs: float = Field(title="펀드환매대금")
    psbl_qty_calc_unpr: float = Field(title="가능수량계산단가")
    nrcvb_buy_amt: float = Field(title="미수없는매수금액")
    nrcvb_buy_qty: int = Field(title="미수없는매수수량")
    max_buy_amt: float = Field(title="최대매수금액")
    max_buy_qty: int = Field(title="최대매수수량")
    cma_evlu_amt: float = Field(title="CMA평가금액")
    ovrs_re_use_amt_wcrc: float = Field(title="해외재사용금액원화")
    ord_psbl_frcr_amt_wcrc: float = Field(title="주문가능외화금액원화")

    @property
    def pretty(self) -> "PrettyBidAvailability":
        return PrettyBidAvailability(**self.dict())


class PrettyBidAvailability(BaseModel):
    """국내주식주문/매수가능조회 - Response Body output 응답상세 Pretty"""

    available_cash: float = Field(alias="ord_psbl_cash", title="주문가능현금")
    available_substitute: float = Field(alias="ord_psbl_sbst", title="주문가능대용")
    available_reuse: float = Field(alias="ruse_psbl_amt", title="재사용가능금액")
    available_quantity: int = Field(alias="psbl_qty_calc_unpr", title="가능수량계산단가")
    non_receivable_buy_amount: float = Field(alias="nrcvb_buy_amt", title="미수없는매수금액")
    non_receivable_buy_quantity: int = Field(alias="nrcvb_buy_qty", title="미수없는매수수량")
    max_buy_amount: float = Field(alias="max_buy_amt", title="최대매수금액")
    max_buy_quantity: int = Field(alias="max_buy_qty", title="최대매수수량")
    cma_eval_amount: float = Field(alias="cma_evlu_amt", title="CMA평가금액")
    overseas_reuse_amount: float = Field(
        alias="ovrs_re_use_amt_wcrc", title="해외재사용금액원화"
    )
    available_foreign_currency_amount: float = Field(
        alias="ord_psbl_frcr_amt_wcrc", title="주문가능외화금액원화"
    )
    fund_repayment: float = Field(alias="fund_rpch_chgs", title="펀드환매대금")


class UnExecutedOrder(BaseModel):
    """
    국내주식주문/주식정정취소가능주문조회 - Response Body output 응답상세

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_d4537e9c-73f7-414c-9fb0-4eae3bc397d0
    """

    ord_gno_brno: str = Field(title="주문채번지점번호")
    odno: str = Field(title="주문번호")
    orgn_odno: str = Field(title="원주문번호")
    ord_dvsn_name: str = Field(title="주문구분명")
    pdno: str = Field(title="상품번호")
    prdt_name: str = Field(title="상품명")
    rvse_cncl_dvsn_name: str = Field(title="정정취소구분명")
    ord_qty: int = Field(title="주문수량")
    ord_unpr: int = Field(title="주문단가")
    ord_tmd: str = Field(title="주문시각")
    tot_ccld_qty: int = Field(title="총체결수량")
    tot_ccld_amt: float = Field(title="총체결금액")
    psbl_qty: int = Field(title="가능수량")
    sll_buy_dvsn_cd: str = Field(title="매도매수구분코드")
    ord_dvsn_cd: str = Field(title="주문구분코드")
    mgco_aptm_odno: str = Field(title="운용사지정주문번호")

    @property
    def pretty(self) -> "PrettyUnExecutedOrder":
        return PrettyUnExecutedOrder(**self.dict())


class PrettyUnExecutedOrder(BaseModel):
    """국내주식주문/주식정정취소가능주문조회 - Response Body output 응답상세 Pretty"""

    symbol: str = Field(alias="pdno", title="상품번호")
    symbol_name: str = Field(alias="prdt_name", title="상품명")
    org_no: str = Field(alias="ord_gno_brno", title="주문채번지점번호")
    order_no: str = Field(alias="odno", title="주문번호")
    origin_order_no: Optional[str] = Field(
        alias="orgn_odno", title="원주문번호", description="정정/취소 주문인 경우"
    )
    order_type: str = Field(alias="sll_buy_dvsn_cd", title="매도매수구분코드")
    modify_type: str = Field(alias="rvse_cncl_dvsn_name", title="정정취소구분명")

    quantity: int = Field(alias="ord_qty", title="주문수량")
    price: int = Field(alias="ord_unpr", title="주문단가")
    time: str = Field(alias="ord_tmd", title="주문시각")
    executed_quantity: int = Field(alias="tot_ccld_qty", title="총체결수량")
    executed_amount: int = Field(alias="tot_ccld_amt", title="총체결금액")
    possible_quantity: int = Field(alias="psbl_qty", title="가능수량")

    # etc
    ord_dvsn_name: str = Field(alias="ord_dvsn_name", title="주문구분명")
    ord_dvsn_cd: str = Field(alias="ord_dvsn_cd", title="주문구분코드")
    mgco_aptm_odno: str = Field(alias="mgco_aptm_odno", title="운용사지정주문번호")

    @validator("origin_order_no", pre=True)
    def set_origin_order_no(cls, origin_order_no: str) -> Optional[str]:
        if origin_order_no == "0":
            return None
        return origin_order_no

    @validator("order_type", pre=True)
    def set_order_type(cls, value: str) -> str:
        if value == "01":
            return "buy"
        return "sell"

    @validator("modify_type", pre=True)
    def set_modify_type(cls, value: str) -> Optional[str]:
        if value == "정정":
            return "modify"
        elif value == "취소":
            return "cancel"
        return "default"

    @property
    def is_market_price(self) -> bool:
        return self.ord_dvsn_cd == "01"


class ExecutedOrderSummary(BaseModel):
    """
    국내주식주문/주식일별주문체결조회 - Response Body output1 응답상세1

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_bc51f9f7-146f-4971-a5ae-ebd574acec12
    """

    ord_dt: str = Field(title="주문일자")
    ord_gno_brno: str = Field(title="주문채번지점번호")
    odno: str = Field(title="주문번호")
    orgn_odno: str = Field(title="원주문번호")
    ord_dvsn_name: str = Field(title="주문구분명")
    sll_buy_dvsn_cd: str = Field(title="매도매수구분코드")
    sll_buy_dvsn_cd_name: str = Field(title="매도매수구분코드명")
    pdno: str = Field(title="상품번호")
    prdt_name: str = Field(title="상품명")
    ord_qty: int = Field(title="주문수량")
    ord_unpr: int = Field(title="주문단가")
    ord_tmd: str = Field(title="주문시각")
    tot_ccld_qty: int = Field(title="총체결수량")
    avg_prvs: float = Field(title="평균가")
    cncl_yn: str = Field(title="취소여부")
    tot_ccld_amt: int = Field(title="총체결금액")
    loan_dt: str = Field(title="대출일자")
    ord_dvsn_cd: str = Field(title="주문구분코드")
    cncl_cfrm_qty: int = Field(title="취소확인수량")
    rmn_qty: int = Field(title="잔여수량")
    rjct_qty: int = Field(title="거부수량")
    ccld_cndt_name: str = Field(title="체결조건명")
    infm_tmd: str = Field(title="통보시각")
    ctac_tlno: str = Field(title="연락전화번호")
    prdt_type_cd: str = Field(title="상품유형코드")
    excg_dvsn_cd: str = Field(title="거래소구분코드")

    @property
    def pretty(self) -> "PrettyExecutedOrderSummary":
        return PrettyExecutedOrderSummary(**self.dict())


class PrettyExecutedOrderSummary(BaseModel):
    """국내주식주문/주식일별주문체결조회 - Response Body output1 응답상세1 Pretty"""

    symbol: str = Field(alias="pdno", title="상품번호")
    symbol_name: str = Field(alias="prdt_name", title="상품명")
    org_no: str = Field(alias="ord_gno_brno", title="주문채번지점번호")
    order_no: str = Field(alias="odno", title="주문번호")
    origin_order_no: Optional[str] = Field(alias="orgn_odno", title="원주문번호")
    order_type: str = Field(alias="sll_buy_dvsn_cd", title="매도매수구분코드")
    order_date: date = Field(alias="ord_dt", title="주문일자")
    order_time: time = Field(alias="ord_tmd", title="주문시각")
    quantity: int = Field(alias="ord_qty", title="주문수량")
    price: int = Field(alias="ord_unpr", title="주문단가")
    executed_quantity: int = Field(alias="tot_ccld_qty", title="총체결수량")
    executed_amount: int = Field(alias="tot_ccld_amt", title="총체결금액")
    average_price: float = Field(alias="avg_prvs", title="평균가")
    is_cancel: str = Field(alias="cncl_yn", title="취소여부")
    order_division_code: str = Field(alias="ord_dvsn_cd", title="주문구분코드")
    order_division_name: str = Field(alias="ord_dvsn_name", title="주문구분명")

    # etc
    order_type_name: str = Field(alias="sll_buy_dvsn_cd_name", title="매도매수구분코드명")
    loan_dt: str = Field(alias="loan_dt", title="대출일자")
    inform_time: time = Field(alias="infm_tmd", title="통보시각")
    cancel_confirmed_quantity: int = Field(alias="cncl_cfrm_qty", title="취소확인수량")
    remain_quantity: int = Field(alias="rmn_qty", title="잔여수량")
    rejected_quantity: int = Field(alias="rjct_qty", title="거부수량")
    executed_condition_name: str = Field(alias="ccld_cndt_name", title="체결조건명")
    contact_number: str = Field(alias="ctac_tlno", title="연락전화번호")
    product_type_code: str = Field(alias="prdt_type_cd", title="상품유형코드")
    exchange_code: str = Field(alias="excg_dvsn_cd", title="거래소구분코드")

    @validator("origin_order_no", pre=True)
    def set_origin_order_no(cls, origin_order_no: str) -> Optional[str]:
        if origin_order_no == "0":
            return None
        return origin_order_no

    @validator("order_type", pre=True)
    def set_order_type(cls, order_type: str) -> str:
        if order_type == "01":
            return "buy"
        return "sell"

    @validator("order_date", pre=True)
    def set_date(cls, value: str) -> date:
        return datetime.strptime(value, "%Y%m%d").date()

    @validator("order_time", "inform_time", pre=True)
    def set_time(cls, value: str) -> time:
        return datetime.strptime(value, "%H%M%S").time()


class ExecutedOrderDetail(BaseModel):
    """국내주식주문/주식일별주문체결조회 - Response Body output2 응답상세2 Pretty"""

    total_order_quantity: int = Field(alias="tot_ord_qty", title="총주문수량")
    total_executed_quantity: int = Field(alias="tot_ccld_qty", title="총체결수량")
    average_price: float = Field(alias="pchs_avg_pric", title="매입평균가격")
    total_executed_amount: int = Field(alias="tot_ccld_amt", title="총체결금액")
    prsm_tlex_smtl: int = Field(alias="prsm_tlex_smtl", title="추정제비용합계")
