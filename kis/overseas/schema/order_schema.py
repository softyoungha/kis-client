from pydantic import BaseModel, Field


class FetchOrdersData(BaseModel):
    """
    https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_d4537e9c-73f7-414c-9fb0-4eae3bc397d0
    """
    symbol: str = Field(alias="pdno", title="상품번호")
    symbol_korean: str = Field(alias="prdt_name", title="상품명")
    org_no: str = Field(alias="ord_gno_brno", title="주문채번지점번호")
    order_no: str = Field(alias="odno", title="주문번호")
    origin_order_no: str = Field(alias="orgn_odno", title="원주문번호", description="정정/취소 주문인 경우")
    quantity: int = Field(alias="ord_qty", title="주문수량")
    price: int = Field(alias="ord_unpr", title="주문단가")
    time: str = Field(alias="ord_tmd", title="주문시각")
    executed_quantity: int = Field(alias="tot_ccld_qty", title="총체결수량")
    executed_amount: int = Field(alias="tot_ccld_amt", title="총체결금액")
    possible_quantity: int = Field(alias="psbl_qty", title="가능수량")

    # etc
    ord_dvsn_name: str = Field(alias="ord_dvsn_name", title="주문구분명")
    rvse_cncl_dvsn_name: str = Field(alias="rvse_cncl_dvsn_name", title="정정취소구분명")
    sll_buy_dvsn_cd: str = Field(alias="sll_buy_dvsn_cd", title="매도매수구분코드")
    ord_dvsn_cd: str = Field(alias="ord_dvsn_cd", title="주문구분코드")
    mgco_aptm_odno: str = Field(alias="mgco_aptm_odno", title="운용사지정주문번호")

    @property
    def order_type(self) -> str:
        if self.sll_buy_dvsn_cd == "01":
            return "buy"
        return "sell"

    @property
    def modify_type(self) -> str:
        if self.rvse_cncl_dvsn_name == "정정":
            return "modify"
        return "cancel"

    @property
    def is_market_price(self) -> bool:
        return self.ord_dvsn_cd == "01"


class OrderData(BaseModel):
    """
    https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_aade4c72-5fb7-418a-9ff2-254b4d5f0ceb
    """

    org_no: str = Field(alias="KRX_FWDG_ORD_ORGNO", title="한국거래소주문조직번호", example='')
    order_no: str = Field(alias="ODNO", title="주문번호", example='')
    open: str = Field(alias="ORD_TMD", title="주문시각", example='')

    def __repr__(self):
        return (
            f"OrderData("
            f"org_no='{self.org_no}', "
            f"order_no='{self.order_no}', "
            f"open='{self.open}')"
        )
