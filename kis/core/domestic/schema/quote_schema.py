from datetime import datetime, date, time
from pydantic import BaseModel, Field, validator
from typing import Optional

from kis.core.enum import Sign


class Price(BaseModel):
    """
    국내주식주문/주식현재가 시세 - Response Body output 응답상세

    See https://apiportal.koreainvestment.com/apiservice/oauth2#L_5c87ba63-740a-4166-93ac-803510bb9c02
    """
    iscd_stat_cls_code: str = Field(title="종목상태구분코드")
    marg_rate: float = Field(title="증거금 비율")
    rprs_mrkt_kor_name: str = Field(title="대표시장 한글명")
    new_hgpr_lwpr_cls_code: Optional[str] = Field(title="신 고가 저가 구분 코드")
    bstp_kor_isnm: str = Field(title="업종 한글명")
    temp_stop_yn: str = Field(title="임시 정지 여부")
    oprc_rang_cont_yn: str = Field(title="종가 범위 연장 여부")
    clpr_rang_cont_yn: str = Field(title="종가 범위 연장 여부")
    crdt_able_yn: str = Field(title="신용 가능 여부")
    grmn_rate_cls_code: str = Field(title="보증금 비율 구분 코드")
    elw_pblc_yn: str = Field(title="ELW 발행 여부")
    stck_prpr: int = Field(title="주식 가격")
    prdy_vrss: int = Field(title="전일 대비")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_ctrt: float = Field(title="전일 대비 대비율")
    acml_tr_pbmn: int = Field(title="누적 거래대금")
    acml_vol: int = Field(title="누적 거래량")
    prdy_vrss_vol_rate: float = Field(title="전일 대비 거래량 비율")
    stck_oprc: int = Field(title="시가")
    stck_hgpr: int = Field(title="고가")
    stck_lwpr: int = Field(title="저가")
    stck_mxpr: int = Field(title="상한가")
    stck_llam: int = Field(title="하한가")
    stck_sdpr: int = Field(title="기준가")
    wghn_avrg_stck_prc: float = Field(title="가중 평균 주식 가격")
    hts_frgn_ehrt: float = Field(title="HTS 외국인 소진율")
    frgn_ntby_qty: int = Field(title="외국인 순매수 수량")
    pgtr_ntby_qty: int = Field(title="프로그램매매 순매수 수량")
    pvt_scnd_dmrs_prc: float = Field(title="피벗 2차 디저항 가격")
    pvt_frst_dmrs_prc: float = Field(title="피벗 1차 디저항 가격")
    pvt_pont_val: float = Field(title="피벗 포인트 값")
    pvt_frst_dmsp_prc: float = Field(title="피벗 1차 디지지 가격")
    pvt_scnd_dmsp_prc: float = Field(title="피벗 2차 디지지 가격")
    dmrs_val: float = Field(title="	디저항 값")
    dmsp_val: float = Field(title="디지지 값")
    cpfn: int = Field(title="자본금")
    rstc_wdth_prc: float = Field(title="제한 폭 가격")
    stck_fcam: int = Field(title="주식 액면가")
    stck_sspr: int = Field(title="주식 대용가")
    aspr_unit: int = Field(title="호가단위")
    hts_deal_qty_unit_val: int = Field(title="HTS 매매 수량 단위 값")
    lstn_stcn: int = Field(title="상장 주수")
    hts_avls: int = Field(title="HTS 시가총액")
    per: float = Field(title="PER")
    pbr: float = Field(title="PBR")
    stac_month: str = Field(title="결산 월")
    vol_tnrt: float = Field(title="거래량 회전율")
    eps: float = Field(title="EPS")
    bps: float = Field(title="BPS")
    d250_hgpr: float = Field(title="250일 최고가")
    d250_hgpr_date: str = Field(title="250일 최고가 일자")
    d250_hgpr_vrss_prpr_rate: float = Field(title="250일 최고가 대비 현재가 비율")
    d250_lwpr: float = Field(title="250일 최저가")
    d250_lwpr_date: str = Field(title="250일 최저가 일자")
    d250_lwpr_vrss_prpr_rate: float = Field(title="250일 최저가 대비 현재가 비율")
    stck_dryy_hgpr: float = Field(title="주식 연중 최고가")
    dryy_hgpr_vrss_prpr_rate: float = Field(title="연중 최고가 대비 현재가 비율")
    dryy_hgpr_date: str = Field(title="연중 최고가 일자")
    stck_dryy_lwpr: float = Field(title="주식 연중 최저가")
    dryy_lwpr_vrss_prpr_rate: float = Field(title="연중 최저가 대비 현재가 비율")
    dryy_lwpr_date: str = Field(title="연중 최저가 일자")
    w52_hgpr: float = Field(title="52주일 최고가")
    w52_hgpr_vrss_prpr_ctrt: float = Field(title="52주일 최고가 대비 현재가 대비")
    w52_hgpr_date: str = Field(title="52주일 최고가 일자")
    w52_lwpr: float = Field(title="52주일 최저가")
    w52_lwpr_vrss_prpr_ctrt: float = Field(title="52주일 최저가 대비 현재가 대비")
    w52_lwpr_date: str = Field(title="52주일 최저가 일자")
    whol_loan_rmnd_rate: float = Field(title="전체 융자 잔고 비율")
    ssts_yn: str = Field(title="공매도가능여부")
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드")
    fcam_cnnm: str = Field(title="액면가 통화명")
    cpfn_cnnm: str = Field(title="자본금 통화명")
    apprch_rate: Optional[float] = Field(title="접근도")
    frgn_hldn_qty: int = Field(title="외국인 보유 수량")
    vi_cls_code: str = Field(title="VI적용구분코드")
    ovtm_vi_cls_code: str = Field(title="시간외단일가VI적용구분코드")
    last_ssts_cntg_qty: int = Field(title="최종 공매도 체결 수량")
    invt_caful_yn: str = Field(title="투자유의여부")
    mrkt_warn_cls_code: str = Field(title="시장경고코드", description="00: 없음/01: 투자주의/02: 투자경고/03: 투자위험")
    short_over_yn: str = Field(title="단기과열여부")

    @property
    def custom(self) -> "PriceCustom":
        return PriceCustom(**self.dict())


class PriceCustom(BaseModel):
    """국내주식주문/주식현재가 시세 - Response Body output 응답상세 Custom"""
    # about prices
    upper_bound: int = Field(alias="stck_mxpr", title="상한가", example=80900)
    lower_bound: int = Field(alias="stck_llam", title="하한가", example=43700)
    high: int = Field(alias="stck_hgpr", title="최고가", example=65200)
    current: int = Field(alias="stck_prpr", title="현재가", example=65000)
    low: int = Field(alias="stck_lwpr", title="최저가", example=63800)
    open: int = Field(alias="stck_oprc", title="시가", example=63800)
    base: int = Field(alias="stck_sdpr", title="기준가(전일 종가)", example=62300)

    # about stock
    sector_korean: str = Field(alias="bstp_kor_isnm", title="업종 한글 종목명", example='전기.전자')
    symbol: str = Field(alias="stck_shrn_iscd", title="주식 단축 종목코드", example='005930')
    market_name: str = Field(alias="rprs_mrkt_kor_name", title="대표 시장 한글명", example='KOSPI200')
    market_cap: int = Field(alias="hts_avls", title="HTS 시가총액", example=3880359)
    bps: float = Field(alias="bps", title="BPS", example=50817.00)
    eps: float = Field(alias="eps", title="EPS", example=8057.00)
    pbr: float = Field(alias="pbr", example='1.28')
    per: float = Field(alias="per", example='8.07')

    diff_rate: float = Field(alias="prdy_ctrt", title="전일 대비율", example=4.41)
    diff_volume_rate: float = Field(alias="prdy_vrss_vol_rate", example=183.26)
    diff_price: int = Field(alias="prdy_vrss", title="전일 대비", example=1000)
    diff_sign: Sign = Field(alias="prdy_vrss_sign", title="전일 대비 부호", example="2")

    @validator("diff_sign", pre=True)
    def set_diff_sign(cls, diff_sign: str):
        return Sign.from_value(diff_sign)

    def __repr__(self):
        return (
            f"FetchPrice(symbol='{self.symbol}', "
            f"current={self.current})"
        )


class PricesSummaryByMinutes(BaseModel):
    """
    국내주식시세/주식당일분봉조회 - Response Body output 응답상세1 Custom

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-quotations#L_eddbb36a-1d55-461a-b242-3067ba1e5640
    """
    symbol_name: str = Field(alias="hts_kor_isnm", title="HTS 한글 종목명", example='삼성전자')
    diff_rate: float = Field(alias="prdy_ctrt", title="전일 대비율", example=4.41)
    diff_price: int = Field(alias="prdy_vrss", title="전일 대비", example=1000)
    diff_sign: Sign = Field(alias="prdy_vrss_sign", title="전일 대비 부호", example="2")
    stck_prdy_clpr: int = Field(alias="stck_prdy_clpr", title="주식 전일 종가", example=62300)
    accumulated_amount: int = Field(alias="acml_tr_pbmn", title="누적 거래 대금", example=1778208943700)
    accumulated_volume: int = Field(alias="acml_vol", title="누적 거래량", example=27476120)
    current: float = Field(alias="stck_prpr", title="현재가", example=65000)

    @validator("diff_sign", pre=True)
    def set_diff_sign(cls, diff_sign: str):
        return Sign.from_value(diff_sign)

    def __repr__(self):
        return (
            f"FetchPricesSummary(symbol_name='{self.symbol_name}', "
            f"current={self.current})"
        )


class PriceHistoryByMinutes(BaseModel):
    """
    국내주식시세/주식당일분봉조회 - Response Body output2 응답상세2 Custom

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-quotations#L_eddbb36a-1d55-461a-b242-3067ba1e5640
    """
    business_date: date = Field(alias="stck_bsop_date", title="주식 영업 일자", example="20230407")
    execution_time: time = Field(alias="stck_cntg_hour", title="주식 체결 시간", example="123000")
    accumulated_amount: int = Field(alias="acml_tr_pbmn", title="누적 거래 대금", example=1241610558700)
    volume: int = Field(alias="cntg_vol", title="체결 거래량", example=27099)
    highest: float = Field(alias="stck_hgpr", title="최고가", example=65200)
    current: float = Field(alias="stck_prpr", title="현재가", example=65000)
    lowest: float = Field(alias="stck_lwpr", title="최저가", example=63800)
    open: float = Field(alias="stck_oprc", title="시가", example=63800)

    @validator("business_date", pre=True)
    def set_business_date(cls, business_date: str) -> date:
        return datetime.strptime(business_date, "%Y%m%d").date()

    @validator("execution_time", pre=True)
    def set_execution_time(cls, execution_time: str) -> time:
        return datetime.strptime(execution_time, "%H%M%S").time()

    @property
    def full_execution_time(self) -> datetime:
        return datetime.combine(self.business_date, self.execution_time)

    def __repr__(self):
        return (
            f"FetchPricesHistory("
            f"datetime='{self.full_execution_time.strftime('%Y-%m-%d %H:%M:%S')}', "
            f"current={self.current}, "
            f"volume={self.volume})"
        )


class FetchOHLCVSummary(BaseModel):
    """
    국내주식시세/국내주식기간별시세(일/주/월/년) - Response Body output1 응답상세1 (Custom Columns)

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-quotations#L_a08c3421-e50f-4f24-b1fe-64c12f723c77
    """
    # 종목 정보
    symbol: str = Field(alias="stck_shrn_iscd", title="주식 단축 종목코드", example="005930")
    symbol_name: str = Field(alias="hts_kor_isnm", title="HTS 한글 종목명", example="삼성전자")
    face_value: int = Field(alias="stck_fcam", title="주식 액면가", example=100)
    shares: int = Field(alias="lstn_stcn", title="상장 주수", example=5969782550)
    capital: int = Field(alias="cpfn", title="자본금", example=596978255000)
    market_cap: int = Field(alias="hts_avls", title="시가총액", example=3870000000000)
    per: float = Field(alias="per", title="PER", example=0.00)
    eps: float = Field(alias="eps", title="EPS", example=0)
    pbr: float = Field(alias="pbr", title="PBR", example=0.00)
    whole_loan_remain_rate: Optional[float] = Field(alias="itewhol_loan_rmnd_ratem", title="전체 융자 잔고 비율", example=0.00)

    # 가격 정보
    price_upper_bound: int = Field(alias="stck_mxpr", title="상한가", example=0)
    price_highest: int = Field(alias="stck_hgpr", title="최고가", example=65000)
    price_current: int = Field(alias="stck_prpr", title="주식 현재가", example=65000)
    price_lowest: int = Field(alias="stck_lwpr", title="최저가", example=63800)
    price_lower_bound: int = Field(alias="stck_llam", title="하한가", example=0)
    price_open: int = Field(alias="stck_oprc", title="시가", example=63800)
    price_base: int = Field(alias="stck_prdy_clpr", title="주식 전일 종가", example=61000)
    accumulated_volume: int = Field(alias="acml_vol", title="누적 거래량", example=27476120)
    accumulated_amount: int = Field(alias="acml_tr_pbmn", title="누적 거래 대금", example=1241610558700)
    ask_price: int = Field(alias="askp", title="매도호가", example=65000)
    bid_price: int = Field(alias="bidp", title="매수호가", example=64900)
    volume_rotation: float = Field(alias="vol_tnrt", title="거래량 회전율", example=0.00)

    # 전일 정보
    x_open: int = Field(alias="stck_prdy_oprc", title="주식 전일 시가", example=63800)
    x_highest: int = Field(alias="stck_prdy_hgpr", title="주식 전일 최고가", example=64400)
    x_lowest: int = Field(alias="stck_prdy_lwpr", title="주식 전일 최저가", example=63000)
    x_volume: int = Field(alias="prdy_vol", title="전일 거래량", example=27099)

    # 전일 대비
    diff_price: int = Field(alias="prdy_vrss", title="전일 대비", example=1000)
    diff_volume: int = Field(alias="prdy_vrss_vol", title="전일 대비 거래량", example=27099)
    diff_rate: float = Field(alias="prdy_ctrt", title="전일 대비율", example=4.41)
    diff_sign: Sign = Field(alias="prdy_vrss_sign", title="전일 대비 부호", example="2")

    @validator("diff_sign", pre=True)
    def set_diff_sign(cls, diff_sign: str):
        return Sign.from_value(diff_sign)


class FetchOHLCVHistory(BaseModel):
    """
    국내주식시세/국내주식기간별시세(일/주/월/년) - Response Body output2 응답상세2 Custom

    See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-quotations#L_a08c3421-e50f-4f24-b1fe-64c12f723c77
    """
    business_date: date = Field(alias="stck_bsop_date", title="주식 영업 일자", example="20210601")
    close: int = Field(alias="stck_clpr", title="주식 종가", example=65000)
    open: int = Field(alias="stck_oprc", title="주식 시가", example=63800)
    high: int = Field(alias="stck_hgpr", title="주식 최고가", example=65000)
    low: int = Field(alias="stck_lwpr", title="주식 최저가", example=63800)
    volume: int = Field(alias="acml_vol", title="누적 거래량", example=27476120)
    amount: int = Field(alias="acml_tr_pbmn", title="누적 거래 대금", example=1241610558700)
    diff_sign: Sign = Field(alias="prdy_vrss_sign", title="전일 대비 부호", example="1")
    diff_price: int = Field(alias="prdy_vrss", title="전일 대비", example=1200)

    # etc
    prtt_rate: float = Field(alias="prtt_rate", title="분할 비율", example=0.00)
    mod_yn: str = Field(alias="mod_yn", title="분할변경여부", example="N")
    flng_cls_code: str = Field(alias="flng_cls_code", title="락 구분 코드", example="00")

    @validator("business_date", pre=True, always=True)
    def set_business_date(cls, business_date: str) -> date:
        return datetime.strptime(business_date, "%Y%m%d").date()

    @validator("diff_sign", pre=True)
    def set_diff_sign(cls, diff_sign: str):
        return Sign.from_value(diff_sign)
