from pydantic import BaseModel, Field


class Stock(BaseModel):
    """
    해외주식현재가/해외주식 잔고 - Response Body output1 응답상세1

    See https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_0482dfb1-154c-476c-8a3b-6fc1da498dbf
    """
    cano: str = Field(title="종합계좌번호", description="계좌번호 체계(8-2)의 앞 8자리")
    acnt_prdt_cd: str = Field(title="계좌상품코드", description="계좌상품코드")
    prdt_type_cd: str = Field(title="상품유형코드")
    ovrs_pdno: str = Field(title="해외상품번호")
    ovrs_item_name: str = Field(title="해외종목명")
    frcr_evlu_pfls_amt: float = Field(title="외화평가손익금액", description="해당 종목의 매입금액과 평가금액의 외회기준 비교 손익")
    evlu_pfls_rt: float = Field(title="평가손익율", description="해당 종목의 평가손익을 기준으로 한 수익률")
    pchs_avg_pric: float = Field(title="매입평균가격", description="해당 종목의 매수 평균 단가")
    ovrs_cblc_qty: int = Field(title="해외잔고수량")
    ord_psbl_qty: int = Field(title="주문가능수량", description="매도 가능한 주문 수량")
    frcr_pchs_amt1: float = Field(title="외화매입금액1", description="해당 종목의 외화 기준 매입금액")
    ovrs_stck_evlu_amt: float = Field(title="해외주식평가금액", description="해당 종목의 외화 기준 평가금액")
    now_pric2: float = Field(title="현재가격2", description="해당 종목의 현재가")
    tr_crcy_cd: str = Field(title="거래통화코드")
    ovrs_excg_cd: str = Field(title="해외거래소코드")
    loan_type_cd: str = Field(title="대출유형코드")
    loan_dt: str = Field(title="대출일자")
    expd_dt: str = Field(title="만기일자")

    @property
    def custom(self) -> "CustomStock":
        return CustomStock(**self.dict())


class CustomStock(BaseModel):
    """ 해외주식현재가/해외주식 잔고 - Response Body output1 응답상세1 Custom """
    account_prefix: str = Field(alias="cano", title="종합계좌번호")
    account_suffix: str = Field(alias="acnt_prdt_cd", title="계좌상품코드")
    product_type_code: str = Field(alias="prdt_type_cd", title="상품유형코드")
    symbol: str = Field(alias="ovrs_pdno", title="해외상품번호")
    symbol_name: str = Field(alias="ovrs_item_name", title="해외종목명")
    profit_loss_amount: float = Field(alias="frcr_evlu_pfls_amt", title="외화평가손익금액", description="평가손익")
    profit_loss_rate: float = Field(alias="evlu_pfls_rt", title="평가손익율", description="수익률")
    inventory_quantity: int = Field(alias="ovrs_cblc_qty", title="해외잔고수량", description="보유수량")
    possible_quantity: int = Field(alias="ord_psbl_qty", title="주문가능수량", description="매도가능수량")
    avg_purchase_price: float = Field(alias="pchs_avg_pric", title="매입평균가격", description="매입단가")
    purchase_amount: float = Field(alias="frcr_pchs_amt1", title="외화매입금액1")
    evaluated_amount: float = Field(alias="ovrs_stck_evlu_amt", title="해외주식평가금액")
    current_price: float = Field(alias="now_pric2", title="현재가격2")
    currency_code: str = Field(alias="tr_crcy_cd", title="거래통화코드")
    exchange_code: str = Field(alias="ovrs_excg_cd", title="해외거래소코드")
    loan_type_code: str = Field(alias="loan_type_cd", title="대출유형코드")


class Deposit(BaseModel):
    """
    해외주식현재가/해외주식 잔고 - Response Body output1 응답상세2

    See https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_0482dfb1-154c-476c-8a3b-6fc1da498dbf
    """

    buy_amount: float = Field(alias="frcr_buy_amt_smtl1", title="외화매수금액합계1")
    total_buy_amount: float = Field(alias="frcr_buy_amt_smtl2", title="외화매수금액합계2")
    purchase_amount: float = Field(alias="frcr_pchs_amt1", title="외화매입금액1")
    realized_profit_loss_amount: float = Field(alias="ovrs_rlzt_pfls_amt", title="해외실현손익금액")
    total_realized_profit_loss_amount: float = Field(alias="ovrs_rlzt_pfls_amt2", title="해외실현손익금액2")
    realized_profit_loss_rate: float = Field(alias="rlzt_erng_rt", title="실현수익율")
    sum_profit_loss_amount: float = Field(alias="ovrs_tot_pfls", title="해외총손익")
    total_profit_loss_amount: float = Field(alias="tot_evlu_pfls_amt", title="총평가손익금액")
    total_profit_loss_rate: float = Field(alias="tot_pftrt", title="총수익률")
