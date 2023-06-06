from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, Field, validator, root_validator
from kis.core.enum import Exchange, Sign


class Price(BaseModel):
    """
    해외주식현재가/해외주식 현재체결가 - Response body output 응답상세

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-current#L_3eeac674-072d-4674-a5a7-f0ed01194a81
    """
    rsym: str = Field(title="실시간조회종목코드")
    zdiv: float = Field(title="소수점자리수")
    base: float = Field(title="전일종가")
    pvol: int = Field(title="전일거래량")
    last: float = Field(title="현재가")
    sign: str = Field(title="대비기호")
    diff: float = Field(title="대비")
    fltt_rt: Optional[float] = Field(title="등락율")
    tvol: int = Field(title="거래량", description="당일 조회시점까지 전체 거래량")
    tamt: float = Field(title="거래대금", description="당일 조회시점까지 전체 거래금액")
    ordy: str = Field(title="매수가능여부")

    @property
    def custom(self) -> "CustomPrice":
        return CustomPrice(**self.dict())


class CustomPrice(BaseModel):
    """해외주식현재가/해외주식 현재체결가 - Response body output 응답상세 Custom"""

    exchange: Exchange = Field(title="국내종목코드")
    symbol: str = Field(title="실시간조회종목코드")
    current: float = Field(alias="last", title="현재가")
    base: float = Field(alias="base", title="전일종가")
    volume: int = Field(alias="tvol", title="거래량", description="당일 조회시점까지 전체 거래량")
    amount: float = Field(alias="tamt", title="거래대금", description="당일 조회시점까지 전체 거래금액")
    float_point: int = Field(alias="zdiv", title="소수점자리수")
    x_volume: float = Field(alias="pvol", title="전일거래량")
    diff_sign: Sign = Field(alias="sign", title="대비기호(전일 대비 부호)")
    diff_price: float = Field(alias="diff", title="대비", description="현재가 - 전일종가")
    order_state: str = Field(alias="ordy", title="매수가능여부", description="매수주문 가능 종목 여부")
    _rsym: str = Field(alias="rsym", title="실시간조회종목코드")

    @root_validator(pre=True)
    def set_exchange_and_symbol(cls, values: dict):
        # rsym = D+시장구분(3자리)+종목코드
        rsym = values.get("rsym")
        values.update(exchange=Exchange(rsym[1:4]).name, symbol=rsym[4:])
        return values

    @validator("diff_sign", pre=True)
    def set_diff_sign(cls, diff_sign: str):
        return Sign.from_value(diff_sign)


class PriceDetail(BaseModel):
    """
    해외주식현재가/해외주식 현재가상세 - Response body output 응답상세

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-current#L_abc66a03-8103-4f6d-8ba8-450c2b935e14
    """

    exchange: Exchange = Field(title="국내종목코드")
    symbol: str = Field(title="실시간조회종목코드")
    current: float = Field(alias="last", title="현재가")
    base: float = Field(alias="base", title="전일종가")
    open: float = Field(alias="open", title="시가")
    high: float = Field(alias="high", title="고가")
    low: float = Field(alias="low", title="저가")
    total_volume: int = Field(alias="tvol", title="거래량")
    total_amount: float = Field(alias="tamt", title="거래대금")
    float_point: int = Field(alias="zdiv", title="소수점자리수")
    x_volume: float = Field(alias="pvol", title="전일거래량")
    market_cap: float = Field(alias="tomv", title="시가총액")
    x_amount: float = Field(alias="pamt", title="전일거래대금")
    per: float = Field(alias="perx", title="PER")
    pbr: float = Field(alias="pbrx", title="PBR")
    eps: float = Field(alias="epsx", title="EPS")
    bps: float = Field(alias="bpsx", title="BPS")
    price_upper_bound: float = Field(alias="uplp", title="상한가")
    price_lower_bound: float = Field(alias="dnlp", title="하한가")
    high_price_52w: float = Field(alias="h52p", title="52주최고가")
    high_date_52w: date = Field(alias="h52d", title="52주최고일자")
    low_price_52w: float = Field(alias="l52p", title="52주최저가")
    low_date_52w: date = Field(alias="l52d", title="52주최저일자")
    shares: float = Field(alias="shar", title="상장주수")
    capital: float = Field(alias="mcap", title="자본금")
    currency: str = Field(alias="curr", title="통화")
    unit: int = Field(alias="vnit", title="매매단위")
    t_xprc: float = Field(alias="t_xprc", title="원환산당일가격")
    t_xdif: float = Field(alias="t_xdif", title="원환산당일대비")
    t_xrat: float = Field(alias="t_xrat", title="원환산당일등락")
    p_xprc: float = Field(alias="p_xprc", title="원환산전일가격")
    p_xdif: float = Field(alias="p_xdif", title="원환산전일대비")
    p_xrat: float = Field(alias="p_xrat", title="원환산전일등락")
    t_rate: float = Field(alias="t_rate", title="당일환율")
    p_rate: Optional[float] = Field(alias="p_rate", title="전일환율")
    t_xsgn: str = Field(alias="t_xsgn", title="원환산당일기호")
    p_xsng: str = Field(alias="p_xsng", title="원환산전일기호")
    tick_size: str = Field(alias="e_hogau", title="호가단위")
    sector: str = Field(alias="e_icod", title="업종(섹터)")
    face_value: float = Field(alias="e_parp", title="액면가")
    order_state: str = Field(
        alias="e_ordyn",
        title="거래가능여부",
        description="매수주문 가능 종목 여부. '매매 불가'/'매매 가능'"
    )
    etp_name: str = Field(alias="etyp_nm", title="ETP 분류명")
    _rsym: str = Field(alias="rsym", title="실시간조회종목코드")

    @root_validator(pre=True)
    def set_exchange_and_symbol(cls, values: dict):
        # rsym = D+시장구분(3자리)+종목코드
        rsym = values.get("rsym")
        values.update(exchange=Exchange(rsym[1:4]).name, symbol=rsym[4:])
        return values

    @validator("high_date_52w", "low_date_52w", pre=True)
    def set_date(cls, date_str: str):
        return datetime.strptime(date_str, "%Y%m%d").date()

    @validator("p_rate", pre=True)
    def validate_p_rate(cls, p_rate: str):
        if not p_rate:
            return None
        return float(p_rate)


class FetchOHLCVSummary(BaseModel):
    """
    해외주식현재가/해외주식 기간별시세 - Response output1 응답상세1 Custom

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-current#L_0e9fb2ba-bbac-4735-925a-a35e08c9a790
    """
    exchange: Exchange = Field(title="국내종목코드")
    symbol: str = Field(title="실시간조회종목코드")
    float_point: int = Field(alias="zdiv", title="소수점자리수")
    record_count: int = Field(alias="nrec", title="총 레코드수")
    _rsym: str = Field(alias="rsym", title="실시간조회종목코드")

    @root_validator(pre=True)
    def set_exchange_and_symbol(cls, values: dict):
        # rsym = D+시장구분(3자리)+종목코드
        rsym = values.get("rsym")
        values.update(exchange=Exchange(rsym[1:4]).name, symbol=rsym[4:])
        return values


class FetchOHLCVHistory(BaseModel):
    """
    해외주식현재가/해외주식 기간별시세 - Response output2 응답상세2 Custom

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-current#L_0e9fb2ba-bbac-4735-925a-a35e08c9a790
    """
    business_date: date = Field(alias="xymd", title="일자(YYYYMMDD)")
    close: float = Field(alias="clos", title="종가")
    open: float = Field(alias="open", title="시가")
    high: float = Field(alias="high", title="고가")
    low: float = Field(alias="low", title="저가")
    volume: int = Field(alias="tvol", title="거래량")
    amount: float = Field(alias="tamt", title="거래대금")
    diff_price: float = Field(alias="diff", title="대비", description="해당 일자의 종가와 해당 전일 종가의 차이 (해당일 종가-해당 전일 종가)")
    diff_sign: Sign = Field(alias="sign", title="대비기호")
    fluc_rate: float = Field(alias="rate", title="등락율", description="해당 전일 대비 / 해당일 종가 * 100")
    bid_price: float = Field(
        alias="pbid",
        title="매수호가",
        description="마지막 체결이 발생한 시점의 매수호가. 해당 일자 거래량 0인 경우 값이 수신되지 않음"
    )
    bid_volume: int = Field(alias="vbid", title="매수호가잔량", description="해당 일자 거래량 0인 경우 값이 수신되지 않음")
    ask_price: float = Field(
        alias="pask",
        title="매도호가",
        description="마지막 체결이 발생한 시점의 매도호가. 해당 일자 거래량 0인 경우 값이 수신되지 않음"
    )
    ask_volume: int = Field(alias="vask", title="매도호가잔량", description="해당 일자 거래량 0인 경우 값이 수신되지 않음")

    @validator("business_date", pre=True)
    def set_business_date(cls, business_date: str):
        return datetime.strptime(business_date, "%Y%m%d").date()

    @validator("diff_sign", pre=True)
    def set_diff_sign(cls, diff_sign: str):
        return Sign.from_value(diff_sign)



