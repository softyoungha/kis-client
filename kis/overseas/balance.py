from kis.base.client import Balance
from kis.base import fetch
from kis.exceptions import KISBadArguments
from typing import List, TYPE_CHECKING
from .schema import Portfolio, Deposit

if TYPE_CHECKING:
    from kis.overseas.client import OverseasClient


class OverseasBalance(Balance):
    """
    국내 잔고 조회
    https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_66c61080-674f-4c91-a0cc-db5e64e9a5e6
    """
    client: "OverseasClient"

    @fetch(
        "/uapi/Overseas-stock/v1/trading/inquire-balance",
        summary_class=List[Portfolio],
        detail_class=List[Deposit]
    )
    def _fetch_one(
            self,
            fk100: str = "",
            nk100: str = "",
    ):
        """주식 잔고 조회"""
        account_prefix, account_suffix = self.client.account_split
        tr_id = "VTTC8434R" if self.client.is_dev else "TTTC8434R"

        headers = {"tr_id": tr_id, "custtype": "P"}
        params = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "AFHR_FLPR_YN": "N",  # 시간외 단일가여부
            "OFL_YN": "N",  # 오프라인여부
            "INQR_DVSN": "01",  # 조회 구분(대출일별 01/종목별 02)
            "UNPR_DVSN": "01",  # 단가 구분
            "FUND_STTL_ICLD_YN": "N",  # 펀드 결제분 포함 여부
            "FNCG_AMT_AUTO_RDPT_YN": "N",  # 융자금액 자동상환여부
            "PRCS_DVSN": "01",  # 00 전일매매 포함/ 01 전일매매미포함
            "CTX_AREA_FK100": fk100,  # 연속조회검색조건100
            "CTX_AREA_NK100": nk100,  # 연속조회키100
        }
        return headers, params


    def fetch(self):
        pass
