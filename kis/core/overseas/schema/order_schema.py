from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel, Field, validator


class OrderData(BaseModel):
    """
    해외주식주문/해외주식 주문 - Response Body output 응답상세 Pretty Columns

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
    해외주식주문/해외주식 매수가능금액조회 - Response Body output 응답상세

    See https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_2a155fee-882f-4d80-8183-559f2f6983e9
    """

    tr_crcy_cd: str = Field(title="거래통화코드")
    ord_psbl_frcr_amt: float = Field(title="주문가능외화금액")
    sll_ruse_psbl_amt: float = Field(title="매도재사용가능금액", description="가능금액 산정 시 사용")
    ovrs_ord_psbl_amt: float = Field(
        title="해외주문가능금액", description="한국투자 앱 해외주식 주문화면내 '외화' 인경우 주문가능금액"
    )
    max_ord_psbl_qty: int = Field(title="최대주문가능수량")
    echm_af_ord_psbl_amt: float = Field(title="환전이후주문가능금액")
    echm_af_ord_psbl_qty: int = Field(title="환전이후주문가능수량")
    ord_psbl_qty: int = Field(title="주문가능수량")
    exrt: float = Field(title="환율")
    frcr_ord_psbl_amt1: float = Field(
        title="외화주문가능금액1", description="한국투자 앱 해외주식 주문화면내 '통합' 인경우 주문가능금액"
    )
    ovrs_max_ord_psbl_qty: int = Field(title="해외최대주문가능수량")

    @property
    def pretty(self) -> "PrettyBidAvailability":
        return PrettyBidAvailability(**self.dict())


class PrettyBidAvailability(BaseModel):
    """해외주식주문/해외주식 매수가능금액조회 - Response Body output 응답상세"""

    currency_code: str = Field(alias="tr_crcy_cd", title="거래통화코드")
    exchange_rate: float = Field(alias="exrt", title="환율")
    sell_reuse_possible_amount: float = Field(
        alias="sll_ruse_psbl_amt", title="매도재사용가능금액", description="가능금액 산정 시 사용"
    )
    order_possible_amount: float = Field(
        alias="ovrs_ord_psbl_amt",
        title="해외주문가능금액",
        description="한국투자 앱 해외주식 주문화면내 '외화' 인경우 주문가능금액",
    )
    order_possible_foreign_amount: float = Field(
        alias="ord_psbl_frcr_amt", title="주문가능외화금액"
    )
    order_possible_quantity: int = Field(alias="ord_psbl_qty", title="주문가능수량")
    max_order_possible_quantity: int = Field(alias="max_ord_psbl_qty", title="최대주문가능수량")
    exchange_after_order_possible_amount: float = Field(
        alias="echm_af_ord_psbl_amt", title="환전이후주문가능금액"
    )
    exchange_after_order_possible_quantity: int = Field(
        alias="echm_af_ord_psbl_qty", title="환전이후주문가능수량"
    )
    total_order_possible_amount: float = Field(
        alias="frcr_ord_psbl_amt1",
        title="외화주문가능금액1",
        description="한국투자 앱 해외주식 주문화면내 '통합' 인경우 주문가능금액",
    )
    overseas_max_order_possible_quantity: int = Field(
        alias="ovrs_max_ord_psbl_qty", title="해외최대주문가능수량"
    )


class UnExecutedOrder(BaseModel):
    """
    해외주식주문/해외주식 미체결내역 - Response Body output 응답상세

    See https://apiportal.koreainvestment.com/apiservice/oauth2#L_5c87ba63-740a-4166-93ac-803510bb9c02
    """

    ord_dt: str = Field(title="주문일자")
    ord_gno_brno: str = Field(title="주문채번지점번호")
    odno: str = Field(title="주문번호")
    orgn_odno: str = Field(title="원주문번호")
    pdno: str = Field(title="상품번호")
    prdt_name: str = Field(title="상품명")
    sll_buy_dvsn_cd: str = Field(title="매도매수구분코드")
    sll_buy_dvsn_cd_name: str = Field(title="매도매수구분코드명")
    rvse_cncl_dvsn_cd: str = Field(title="정정취소구분코드")
    rvse_cncl_dvsn_cd_name: str = Field(title="정정취소구분코드명")
    rjct_rson: str = Field(title="거부사유")
    rjct_rson_name: str = Field(title="거부사유명")
    ord_tmd: str = Field(title="주문시각")
    tr_mket_name: str = Field(title="거래시장명")
    tr_crcy_cd: str = Field(title="거래통화코드")
    natn_cd: str = Field(title="국가코드")
    natn_kor_name: str = Field(title="국가한글명")
    ft_ord_qty: int = Field(title="FT주문수량")
    ft_ccld_qty: int = Field(title="FT체결수량")
    nccs_qty: int = Field(title="미체결수량")
    ft_ord_unpr3: float = Field(title="FT주문단가3")
    ft_ccld_unpr3: float = Field(title="FT체결단가3")
    ft_ccld_amt3: float = Field(title="FT체결금액3")
    ovrs_excg_cd: str = Field(title="해외거래소코드")
    prcs_stat_name: str = Field(title="처리상태명")
    loan_type_cd: str = Field(title="대출유형코드")
    loan_dt: str = Field(title="대출일자")

    @property
    def pretty(self) -> "PrettyUnExecutedOrder":
        return PrettyUnExecutedOrder(**self.dict())


class PrettyUnExecutedOrder(BaseModel):
    """해외주식주문/해외주식 미체결내역 - Response Body output 응답상세 Pretty"""

    symbol: str = Field(alias="pdno", title="종목코드")
    symbol_name: str = Field(alias="prdt_name", title="종목명")
    org_no: str = Field(alias="ord_gno_brno", title="주문채번지점번호")
    order_no: str = Field(alias="odno", title="주문번호")
    origin_order_no: Optional[str] = Field(alias="orgn_odno", title="원주문번호")
    order_type: str = Field(alias="sll_buy_dvsn_cd", title="매도매수구분코드")
    modify_type: str = Field(alias="rvse_cncl_dvsn_cd", title="정정취소구분코드")
    order_date: date = Field(alias="ord_dt", title="주문일자")
    order_time: time = Field(alias="ord_tmd", title="주문시각", description="주문 접수 시간")
    quantity: int = Field(alias="ft_ord_qty", title="주문수량")
    price: float = Field(alias="ft_ord_unpr3", title="주문가격")
    executed_quantity: int = Field(alias="ft_ccld_qty", title="체결된 수량")
    executed_price: float = Field(alias="ft_ccld_unpr3", title="체결된 가격")
    executed_amount: float = Field(alias="ft_ccld_amt3", title="체결된 금액")
    unfilled_quantity: int = Field(alias="nccs_qty", title="미체결수량")

    # etc
    order_type_name: str = Field(alias="sll_buy_dvsn_cd_name", title="매도매수구분코드명")
    modify_type_name: str = Field(alias="rvse_cncl_dvsn_cd_name", title="정정취소구분코드명")
    reject_reason: str = Field(
        alias="rjct_rson", title="거부사유", description="정상 처리되지 못하고 거부된 주문의 사유"
    )
    reject_reason_name: str = Field(
        alias="rjct_rson_name", title="거부사유명", description="정상 처리되지 못하고 거부된 주문의 사유명"
    )
    market_name: str = Field(alias="tr_mket_name", title="거래시장명")
    currency_code: str = Field(alias="tr_crcy_cd", title="거래통화코드")
    national_code: str = Field(alias="natn_cd", title="국가코드")
    national_korean: str = Field(alias="natn_kor_name", title="국가한글명")
    exchange_cd: str = Field(alias="ovrs_excg_cd", title="해외거래소코드")
    status: str = Field(alias="prcs_stat_name", title="처리상태명")
    loadn_type_code: str = Field(alias="loan_type_cd", title="대출유형코드")
    loan_date: str = Field(alias="loan_dt", title="대출일자")

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

    @validator("modify_type", pre=True)
    def set_modify_type(cls, value: str) -> str:
        if value == "01":
            return "modify"  # 정정
        elif value == "02":
            return "cancel"  # 취소
        return "default"  # 보통

    @validator("order_date", pre=True)
    def set_date(cls, value: str) -> date:
        return datetime.strptime(value, "%Y%m%d").date()

    @validator("order_time", pre=True)
    def set_time(cls, value: str) -> time:
        return datetime.strptime(value, "%H%M%S").time()


class ExecutedOrder(BaseModel):
    """
    해외주식주문/해외주식 주문체결내역 - Response Body output 응답상세

    See https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_6d715b38-566f-4045-a08c-4a594d3a3314
    """

    ord_dt: str = Field(title="주문일자")
    ord_gno_brno: str = Field(title="주문채번지점번호")
    odno: str = Field(title="주문번호")
    orgn_odno: str = Field(title="원주문번호")
    sll_buy_dvsn_cd: str = Field(title="매도매수구분코드")
    sll_buy_dvsn_cd_name: str = Field(title="매도매수구분코드명")
    rvse_cncl_dvsn: str = Field(title="정정취소구분")
    rvse_cncl_dvsn_name: str = Field(title="정정취소구분명")
    pdno: str = Field(title="상품번호")
    prdt_name: str = Field(title="상품명")
    ft_ord_qty: int = Field(title="FT주문수량")
    ft_ord_unpr3: float = Field(title="FT주문단가3")
    ft_ccld_qty: int = Field(title="FT체결수량")
    ft_ccld_unpr3: float = Field(title="FT체결단가3")
    ft_ccld_amt3: float = Field(title="FT체결금액3")
    nccs_qty: int = Field(title="미체결수량")
    prcs_stat_name: str = Field(title="처리상태명")
    rjct_rson: str = Field(title="거부사유")
    ord_tmd: str = Field(title="주문시각")
    tr_mket_name: str = Field(title="거래시장명")
    tr_natn: str = Field(title="거래국가")
    tr_natn_name: str = Field(title="거래국가명")
    ovrs_excg_cd: str = Field(title="해외거래소코드")
    tr_crcy_cd: str = Field(title="거래통화코드")
    dmst_ord_dt: str = Field(title="국내주문일자")
    thco_ord_tmd: str = Field(title="당사주문시각")
    loan_type_cd: str = Field(title="대출유형코드")
    mdia_dvsn_name: str = Field(title="매체구분명")
    loan_dt: str = Field(title="대출일자")
    rjct_rson_name: str = Field(title="거부사유명")

    @property
    def pretty(self) -> "PrettyExecutedOrder":
        return PrettyExecutedOrder(**self.dict())


class PrettyExecutedOrder(BaseModel):
    """해외주식주문/해외주식 주문체결내역 - Response Body output 응답상세 Pretty"""

    symbol: str = Field(alias="pdno", title="상품번호")
    symbol_name: str = Field(alias="prdt_name", title="상품명")
    org_no: str = Field(alias="ord_gno_brno", title="주문채번지점번호")
    order_no: str = Field(alias="odno", title="주문번호")
    origin_order_no: Optional[str] = Field(alias="orgn_odno", title="원주문번호")
    order_date: date = Field(alias="ord_dt", title="주문일자")
    order_time: time = Field(alias="ord_tmd", title="주문시각")
    korean_order_date: date = Field(alias="dmst_ord_dt", title="국내주문일자")
    korean_order_time: time = Field(alias="thco_ord_tmd", title="당사주문시각")
    order_type: str = Field(alias="sll_buy_dvsn_cd", title="매도매수구분코드")
    modify_type: str = Field(alias="rvse_cncl_dvsn", title="정정취소구분")
    quantity: int = Field(alias="ft_ord_qty", title="FT주문수량")
    price: float = Field(alias="ft_ord_unpr3", title="FT주문단가3")
    executed_quantity: int = Field(alias="ft_ccld_qty", title="FT체결수량")
    executed_price: float = Field(alias="ft_ccld_unpr3", title="FT체결단가3")
    executed_amount: float = Field(alias="ft_ccld_amt3", title="FT체결금액3")
    unexecuted_quantity: int = Field(alias="nccs_qty", title="미체결수량")

    # etc
    order_type_name: str = Field(alias="sll_buy_dvsn_cd_name", title="매도매수구분코드명")
    modify_type_name: str = Field(alias="rvse_cncl_dvsn_name", title="정정취소구분명")
    status: str = Field(alias="prcs_stat_name", title="처리상태명")
    reject_reason: str = Field(alias="rjct_rson", title="거부사유")
    reject_reason_name: str = Field(alias="rjct_rson_name", title="거부사유명")
    market_name: str = Field(alias="tr_mket_name", title="거래시장명")
    national_code: str = Field(alias="tr_natn", title="거래국가")
    national_korean: str = Field(alias="tr_natn_name", title="거래국가명")
    exchange_code: str = Field(alias="ovrs_excg_cd", title="해외거래소코드")
    currency_code: str = Field(alias="tr_crcy_cd", title="거래통화코드")
    loan_type_code: str = Field(alias="loan_type_cd", title="대출유형코드")
    media_division_name: str = Field(alias="mdia_dvsn_name", title="매체구분명")
    loan_date: str = Field(alias="loan_dt", title="대출일자")

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

    @validator("modify_type", pre=True)
    def set_modify_type(cls, value: str) -> Optional[str]:
        if value == "01":
            return "modify"  # 정정
        elif value == "02":
            return "cancel"  # 취소
        return "default"  # 보통

    @validator("order_date", "korean_order_date", pre=True)
    def set_date(cls, value: str) -> date:
        return datetime.strptime(value, "%Y%m%d").date()

    @validator("order_time", "korean_order_time", pre=True)
    def set_time(cls, value: str) -> time:
        return datetime.strptime(value, "%H%M%S").time()
