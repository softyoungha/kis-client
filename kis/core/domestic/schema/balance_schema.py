from typing import Optional
from pydantic import BaseModel, Field


class Stock(BaseModel):
    """
    국내주식주문/주식잔고조회 - Response Body output1 응답상세1

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_66c61080-674f-4c91-a0cc-db5e64e9a5e6
    """
    pdno: str = Field(title="상품번호")
    prdt_name: str = Field(title="상품명")
    trad_dvsn_name: str = Field(title="매매구분명")
    bfdy_buy_qty: int = Field(title="전일매수수량")
    bfdy_sll_qty: int = Field(title="전일매도수량")
    thdt_buy_qty: int = Field(title="금일매수수량")
    thdt_sll_qty: int = Field(title="금일매도수량")
    hldg_qty: int = Field(title="보유수량")
    ord_psbl_qty: int = Field(title="주문가능수량")
    pchs_avg_pric: float = Field(title="매입평균가격")
    pchs_amt: int = Field(title="매입금액")
    prpr: int = Field(title="현재가")
    evlu_amt: int = Field(title="평가금액")
    evlu_pfls_amt: int = Field(title="평가손익금액")
    evlu_pfls_rt: float = Field(title="평가손익율")
    evlu_erng_rt: float = Field(title="평가수익율")
    loan_dt: str = Field(title="대출일자")
    loan_amt: int = Field(title="대출금액")
    stln_slng_chgs: int = Field(title="대주매각대금")
    expd_dt: str = Field(title="만기일자")
    fltt_rt: Optional[float] = Field(title="등락율")
    bfdy_cprs_icdc: str = Field(title="전일대비증감")
    item_mgna_rt_name: str = Field(title="종목증거금율명")
    grta_rt_name: str = Field(title="보증금율명")
    sbst_pric: int = Field(title="대용가격")
    stck_loan_unpr: int = Field(title="주식대출단가")

    @property
    def custom(self) -> "CustomStock":
        return CustomStock(**self.dict())


class CustomStock(BaseModel):
    """ 국내주식주문/주식잔고조회 - Response Body output1 응답상세1 Custom """
    symbol: str = Field(alias="pdno", title="상품번호")
    symbol_name: str = Field(alias="prdt_name", title="상품명")
    order_division: str = Field(alias="trad_dvsn_name", title="매매구분명")
    x_buy_quantity: str = Field(alias="dfdy_buy_qty", title="전일매수수량")
    x_sell_quantity: str = Field(alias="bfdy_sll_qty", title="전일매도수량")
    today_buy_quantity: str = Field(alias="thdt_buyqty", title="금일매수수량")
    today_sell_quantity: str = Field(alias="thdt_sll_qty", title="금일매도수량")
    current_quantity: str = Field(alias="hldg_qty", title="보유수량")
    possible_quantity: str = Field(alias="ord_psbl_qty", title="주문가능수량")
    current_price: str = Field(alias="prpr", title="현재가")
    average_price: str = Field(alias="pchs_avg_pric", title="매입평균가격")
    purchase_amount: str = Field(alias="pchs_amt", title="매입금액")
    eval_amount: str = Field(alias="evlu_amt", title="평가금액")
    eval_profit_loss_amount: str = Field(
        alias="evlu_pfls_amt", title="평가손익금액",
        description="evaluated profits and loss amount. 평가금액 - 매입금액"
    )
    eval_profit_loss_rate: str = Field(alias="evlu_pfls_rt", title="평가손익율")
    eval_earning_rate: str = Field(alias="evlu_erng_rt", title="평가수익율")
    loan_date: str = Field(alias="loan_dt", title="대출일자")
    loan_amount: str = Field(alias="loan_amt", title="대출금액")
    expire_date: str = Field(alias="expd_dt", title="만기일자")


class Deposit(BaseModel):
    """
    국내주식주문/주식잔고조회 - Response Body output2 응답상세2

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_66c61080-674f-4c91-a0cc-db5e64e9a5e6
    """
    dnca_tot_amt: int = Field(title="예수금총금액")
    nxdy_excc_amt: int = Field(title="익일정산금액")
    prvs_rcdl_excc_amt: int = Field(title="가수도정산금액")
    cma_evlu_amt: int = Field(title="CMA평가금액")
    bfdy_buy_amt: int = Field(title="전일매수금액")
    thdt_buy_amt: int = Field(title="금일매수금액")
    nxdy_auto_rdpt_amt: int = Field(title="익일자동상환금액")
    bfdy_sll_amt: int = Field(title="전일매도금액")
    thdt_sll_amt: int = Field(title="금일매도금액")
    d2_auto_rdpt_amt: int = Field(title="D+2자동상환금액")
    bfdy_tlex_amt: int = Field(title="전일제비용금액")
    thdt_tlex_amt: int = Field(title="금일제비용금액")
    tot_loan_amt: int = Field(title="총대출금액")
    scts_evlu_amt: int = Field(title="유가평가금액")
    tot_evlu_amt: int = Field(title="총평가금액")
    nass_amt: int = Field(title="순자산금액")
    fncg_gld_auto_rdpt_yn: str = Field(title="융자금자동상환여부")
    pchs_amt_smtl_amt: int = Field(title="매입금액합계금액")
    evlu_amt_smtl_amt: int = Field(title="평가금액합계금액")
    evlu_pfls_smtl_amt: int = Field(title="평가손익합계금액")
    tot_stln_slng_chgs: int = Field(title="총대주매각대금")
    bfdy_tot_asst_evlu_amt: int = Field(title="전일총자산평가금액")
    asst_icdc_amt: int = Field(title="자산증감액")
    asst_icdc_erng_rt: float = Field(title="자산증감수익율")

    @property
    def custom(self) -> "CustomDeposit":
        return CustomDeposit(**self.dict())


class CustomDeposit(BaseModel):
    """ 국내주식주문/주식잔고조회 - Response Body output2 응답상세2 Custom """
    deposit_total_amount: float = Field(alias="dnca_tot_amt", title="예수금총금액")
    cma_amount: float = Field(alias="cma_evlu_amt", title="CMA평가금액")
    buy_amount: float = Field(alias="thdt_buy_amt", title="금일매수금액")
    sell_amount: float = Field(alias="thdt_sll_amt", title="금일매도금액")
    market_evaluated_amount: float = Field(alias="scts_evlu_amt", title="유가평가금액")
    total_evaluated_amount: float = Field(alias="tot_evlu_amt", title="총평가금액", description="주식 평가금액 + 예수금 총액")
    total_loan_amount: float = Field(alias="tot_loan_amt", title="총대출금액")
    tax_exchange_amount: float = Field(
        alias="thdt_tlex_amt", title="금일제비용금액", description="tax_liability_exchange_amount"
    )
    net_asset_amount: float = Field(alias="nass_amt", title="순자산금액")
    sum_purchase_amount: float = Field(alias="pchs_amt_smtl_amt", title="매입금액합계금액")
    sum_evaluated_amount: float = Field(alias="evlu_amt_smtl_amt", title="평가금액합계금액")
    profit_loss_amount: float = Field(
        alias="evlu_pfls_smtl_amt", title="평가손익합계금액",
        description="sum total amount of profit and loss amount of evaluation"
    )
    net_asset_change: int = Field(alias="asst_icdc_amt", title="자산증감액")
    asset_growth_rate: float = Field(alias="asst_icdc_erng_rt", title="자산증감수익율")

    # 전일
    x_buy_amount: float = Field(alias="bfdy_buy_amt", title="전일매수금액")
    x_sell_amount: float = Field(alias="bfdy_sll_amt", title="전일매도금액")
    x_total_evaluated_amount: float = Field(alias="bfdy_tot_asst_evlu_amt", title="전일총자산평가금액")
    x_tax_exchange_amount: float = Field(
        alias="bfdy_tlex_amt", title="전일제비용금액", description="tax_liability_exchange_amount"
    )

    # 익일
    next_auto_repayment_amount: float = Field(alias="nxdy_auto_rdpt_amt", title="익일자동상환금액")
    next_exchange_amount: float = Field(alias="nxdy_excc_amt", title="익일정산금액", description="")

    # D+2
    d2_auto_repayment_amount: float = Field(alias="d2_auto_rdpt_amt", title="D+2자동상환금액")
