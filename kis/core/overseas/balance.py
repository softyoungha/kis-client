from typing import Any, Dict, List, Union

from kis.core.base.resources import Balance
from kis.core.enum import Exchange
from kis.core.overseas.client import OverseasResource

from .schema import Deposit, Stock


class OverseasBalance(OverseasResource, Balance):
    """
    해외주식주문/해외 잔고 조회

    See https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_0482dfb1-154c-476c-8a3b-6fc1da498dbf
    """

    def _fetch_one(
        self,
        exchange: Union[str, Exchange] = None,
        fk200: str = "",
        nk200: str = "",
    ):
        """주식 잔고 조회"""
        if exchange:
            exchange = Exchange.from_value(exchange)
        else:
            exchange = self.client.exchange

        account_prefix, account_suffix = self.client.get_account()

        if self.is_dev:
            if self.client.is_day:
                tr_id = "VTTS3012R"
            else:
                tr_id = "VTTT3012R"
        else:
            if self.client.is_day:
                tr_id = "TTTS3012R"
            else:
                tr_id = "JTTT3012R"

        headers = {"tr_id": tr_id, "custtype": "P"}
        params = {
            "CANO": account_prefix,
            "ACNT_PRDT_CD": account_suffix,
            "OVRS_EXCG_CD": exchange.code,
            "TR_CRCY_CD": exchange.currency(),
            "CTX_AREA_FK200": fk200,  # 연속조회검색조건200
            "CTX_AREA_NK200": nk200,  # 연속조회키200
        }

        return self.client.fetch_data(
            "/uapi/overseas-stock/v1/trading/inquire-balance",
            headers=headers,
            params=params,
            summary_class=List[Dict[str, Any]],
            detail_class=Dict[str, Any],
        )

    def fetch(self) -> List[Stock]:
        """해외주식 잔고 조회"""
        result = self._fetch_one()

        portfolio, deposit = [
            [Stock(**row) for row in result.summary],
            Deposit(**result.detail),
        ]
        while result.has_next:
            result = self._fetch_one(fk200=result.fk200, nk200=result.nk200)
            portfolio.append([Stock(**row) for row in result.summary])

        return portfolio
