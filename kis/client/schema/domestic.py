from datetime import datetime
from pydantic import BaseModel, Field



class FetchPrice(BaseModel):
    """
    :reference: https://me2.kr/HNVld
    """
    price_upper_bound: float = Field(alias="stck_mxpr", title="상한가", example=80900)
    price_highest: float = Field(alias="stck_hgpr", title="최고가", example=65200)
    price_current: float = Field(alias="stck_prpr", title="현재가", example=65000)
    price_lowest: float = Field(alias="stck_lwpr", title="최저가", example=63800)
    price_lower_bound: float = Field(alias="stck_llam", title="하한가", example=43700)
    price_open: float = Field(alias="stck_oprc", title="시가", example=63800)
    price_standard: float = Field(alias="stck_sdpr", title="기준가(전일 종가)", example=62300)

    bstp_kor_isnm: str = Field(alias="bstp_kor_isnm", title="업종 한글 종목명", example='전기.전자')
    symbol: str = Field(alias="stck_shrn_iscd", title="주식 단축 종목코드",  example='005930')
    market_name: str = Field(alias="rprs_mrkt_kor_name", title="대표 시장 한글명", example='KOSPI200')
    hts_market_cap: int = Field(alias="hts_avls", title="HTS 시가총액", example=3880359)
    bps: float = Field(alias="bps", title="BPS", example=50817.00)
    eps: float = Field(alias="eps", title="EPS", example=8057.00)
    pbr: float = Field(alias="pbr", example='1.28')
    per: float = Field(alias="per", example='8.07')

    iscd_stat_cls_code: str = Field(alias="iscd_stat_cls_code", title="종목 상태 구분 코드", example='55')
    marg_rate: float = Field(alias="marg_rate", title="증거금 비율", example=20.00)
    temp_stop_yn: str = Field(alias="temp_stop_yn", example='N')
    acml_tr_pbmn: int = Field(alias="acml_tr_pbmn", example=1778208943700)
    acml_vol: int = Field(alias="acml_vol", example=27476120)
    aspr_unit: int = Field(alias="aspr_unit", example=100)
    clpr_rang_cont_yn: str = Field(alias="clpr_rang_cont_yn", example='N')
    cpfn: int = Field(alias="cpfn", example=7780)
    cpfn_cnnm: str = Field(alias="cpfn_cnnm", example='7,780 억')
    crdt_able_yn: str = Field(alias="crdt_able_yn", example='Y')
    d250_hgpr: int = Field(alias="d250_hgpr", example=69000)
    d250_hgpr_date: str = Field(alias="d250_hgpr_date", example='20220413')
    d250_hgpr_vrss_prpr_rate: float = Field(alias="d250_hgpr_vrss_prpr_rate", example=-5.80)
    d250_lwpr: int = Field(alias="d250_lwpr", example=51800)
    d250_lwpr_date: str = Field(alias="d250_lwpr_date", example='20220930')
    d250_lwpr_vrss_prpr_rate: float = Field(alias="d250_lwpr_vrss_prpr_rate", example=25.48)
    dmrs_val: int = Field(alias="dmrs_val", example=62950)
    dmsp_val: int = Field(alias="dmsp_val", example=61650)
    dryy_hgpr_date: str = Field(alias="dryy_hgpr_date", example='20230407')
    dryy_hgpr_vrss_prpr_rate: float = Field(alias="dryy_hgpr_vrss_prpr_rate", example=-0.31)
    dryy_lwpr_date: str = Field(alias="dryy_lwpr_date", example='20230103')
    dryy_lwpr_vrss_prpr_rate: float = Field(alias="dryy_lwpr_vrss_prpr_rate", example=19.27)
    elw_pblc_yn: str = Field(alias="elw_pblc_yn", example='Y')
    fcam_cnnm: int = Field(alias="fcam_cnnm", example=100)
    frgn_hldn_qty: int = Field(alias="frgn_hldn_qty", example=3064926246)
    frgn_ntby_qty: int = Field(alias="frgn_ntby_qty", example=14429002)
    grmn_rate_cls_code: str = Field(alias="grmn_rate_cls_code", example='40')
    hts_deal_qty_unit_val: int = Field(alias="hts_deal_qty_unit_val", example=1)
    hts_frgn_ehrt: float = Field(alias="hts_frgn_ehrt", example=51.34)
    invt_caful_yn: str = Field(alias="invt_caful_yn", example='N')
    last_ssts_cntg_qty: int = Field(alias="last_ssts_cntg_qty", example=499171)
    lstn_stcn: int = Field(alias="lstn_stcn", example=5969782550)
    mrkt_warn_cls_code: str = Field(alias="mrkt_warn_cls_code", example='00')
    oprc_rang_cont_yn: str = Field(alias="oprc_rang_cont_yn", example='N')
    ovtm_vi_cls_code: str = Field(alias="ovtm_vi_cls_code", example='N')
    pgtr_ntby_qty: int = Field(alias="pgtr_ntby_qty", example=11678793)
    prdy_ctrt: float = Field(alias="prdy_ctrt", example=4.33)
    prdy_vrss: int = Field(alias="prdy_vrss", example=2700)
    prdy_vrss_sign: str = Field(alias="prdy_vrss_sign", example='2')
    prdy_vrss_vol_rate: float = Field(alias="prdy_vrss_vol_rate", example=183.26)
    pvt_frst_dmrs_prc: int = Field(alias="pvt_frst_dmrs_prc", example=63166)
    pvt_frst_dmsp_prc: int = Field(alias="pvt_frst_dmsp_prc", example=61866)
    pvt_pont_val: int = Field(alias="pvt_pont_val", example=62733)
    pvt_scnd_dmrs_prc: int = Field(alias="pvt_scnd_dmrs_prc", example=64033)
    pvt_scnd_dmsp_prc: int = Field(alias="pvt_scnd_dmsp_prc", example=61433)
    rstc_wdth_prc: int = Field(alias="rstc_wdth_prc", example=18600)
    short_over_yn: str = Field(alias="short_over_yn", example='N')
    sltr_yn: str = Field(alias="sltr_yn", example='N')
    ssts_yn: str = Field(alias="ssts_yn", example='Y')
    stac_month: str = Field(alias="stac_month", example='12')
    stck_dryy_hgpr: int = Field(alias="stck_dryy_hgpr", example=65200)
    stck_dryy_lwpr: int = Field(alias="stck_dryy_lwpr", example=54500)
    stck_fcam: str = Field(alias="stck_fcam", example='100')
    stck_sspr: int = Field(alias="stck_sspr", example=49840)
    vi_cls_code: str = Field(alias="vi_cls_code", example='N')
    vol_tnrt: float = Field(alias="vol_tnrt", example=0.46)
    w52_hgpr: float = Field(alias="w52_hgpr", example=69000)
    w52_hgpr_date: str = Field(alias="w52_hgpr_date", example='20220413')
    w52_hgpr_vrss_prpr_ctrt: float = Field(alias="w52_hgpr_vrss_prpr_ctrt", example=-5.80)
    w52_lwpr: int = Field(alias="w52_lwpr", example=51800)
    w52_lwpr_date: str = Field(alias="w52_lwpr_date", example='20220930')
    w52_lwpr_vrss_prpr_ctrt: float = Field(alias="w52_lwpr_vrss_prpr_ctrt", example=25.48)
    wghn_avrg_stck_prc: float = Field(alias="wghn_avrg_stck_prc", example=64718.35)
    whol_loan_rmnd_rate: float = Field(alias="whol_loan_rmnd_rate", example=0.07)

    def __repr__(self):
        return (
            f"FetchPrice(symbol='{self.symbol}', "
            f"current={self.price_current})"
        )

class FetchPricesByMinutesSummary(BaseModel):
    """
    :reference: https://me2.kr/MZUXv
    """
    symbol_korean: str = Field(alias="hts_kor_isnm", title="HTS 한글 종목명", example='삼성전자')
    prdy_ctrt: float = Field(alias="prdy_ctrt", title="전일 대비율", example=4.33)
    prdy_vrss: int = Field(alias="prdy_vrss", title="전일 대비", example=2700)
    prdy_vrss_sign: str = Field(alias="prdy_vrss_sign", title="전일 대비 부호", example='2')
    stck_prdy_clpr: int = Field(alias="stck_prdy_clpr", title="주식 전일 종가", example=62300)
    cumulative_amount: int = Field(alias="acml_tr_pbmn", title="누적 거래 대금", example=1778208943700)
    cumulative_volume: int = Field(alias="acml_vol", title="누적 거래량", example=27476120)
    current: float = Field(alias="stck_prpr", title="현재가", example=65000)

    def __repr__(self):
        return (
            f"FetchPricesSummary(symbol_korean='{self.symbol_korean}', "
            f"current={self.current})"
        )


class FetchPriceByMinutesHistory(BaseModel):
    """
    :reference: https://me2.kr/MZUXv
    """
    business_date: str = Field(alias="stck_bsop_date", title="주식 영업 일자", example="20230407")
    execution_time: str = Field(alias="stck_cntg_hour", title="주식 체결 시간", example="123000")
    cumulative_amount: int = Field(alias="acml_tr_pbmn", title="누적 거래 대금", example=1241610558700)
    volume: int = Field(alias="cntg_vol", title="체결 거래량", example=27099)
    highest: float = Field(alias="stck_hgpr", title="최고가", example=65200)
    current: float = Field(alias="stck_prpr", title="현재가", example=65000)
    lowest: float = Field(alias="stck_lwpr", title="최저가", example=63800)
    open: float = Field(alias="stck_oprc", title="시가", example=63800)

    @property
    def datetime(self) -> datetime:
        return datetime.strptime(
            self.business_date + self.execution_time,
            "%Y%m%d%H%M%S"
        )

    def __repr__(self):
        return (
            f"FetchPricesHistory("
            f"datetime='{self.datetime.strftime('%Y-%m-%d %H:%M:%S')}', "
            f"current={self.current}, "
            f"volume={self.volume})"
        )