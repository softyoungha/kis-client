from typing import Any, Dict, List, Literal, Tuple, overload

from kis.core.base.resources import Balance

from .client import DomesticResource
from .schema import Deposit, PrettyDeposit, PrettyStock, Stock


class DomesticBalance(DomesticResource, Balance):
    """
    국내 잔고 조회
    https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_66c61080-674f-4c91-a0cc-db5e64e9a5e6
    """

    def _fetch_one(
        self,
        fk100: str = "",
        nk100: str = "",
    ):
        """
        국내주식주문/주식잔고조회 1회 호출

        ---

        [한국투자증권 OPEN API doc]
        주식 잔고조회 API입니다.
        실전계좌의 경우, 한 번의 호출에 최대 50건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.
        모의계좌의 경우, 한 번의 호출에 최대 20건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.

        :reference:
            https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_66c61080-674f-4c91-a0cc-db5e64e9a5e6

        :param fk100: 연속 조회
        :param nk100:
        :return:
        """
        account_prefix, account_suffix = self.client.get_account()
        tr_id = "VTTC8434R" if self.is_dev else "TTTC8434R"

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
        return self.client.fetch_data(
            "/uapi/domestic-stock/v1/trading/inquire-balance",
            headers,
            params,
            summary_class=List[Dict[str, Any]],
            detail_class=List[Dict[str, Any]],
        )

    def fetch(self) -> Tuple[List[Stock], List[Deposit]]:
        """
        국내주식주문/주식잔고조회 연속 호출
        """
        # get one
        result = self._fetch_one()

        portfolio, deposits = (
            [Stock(**row) for row in result.summary],
            [Deposit(**row) for row in result.detail],
        )
        while result.has_next:
            result = self._fetch_one(fk100=result.fk100, nk100=result.nk100)
            portfolio.extend([Stock(**row) for row in result.summary])
            deposits.extend([Deposit(**row) for row in result.detail])

        return portfolio, deposits
