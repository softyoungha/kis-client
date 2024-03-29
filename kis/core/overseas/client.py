from functools import cached_property
from typing import TYPE_CHECKING, Optional, Union

import requests
from pydantic import validator

from kis.core.base.client import KisClientBase
from kis.core.enum import Exchange
from kis.core.master import MasterBook
from kis.core.overseas.schema import Currency
from kis.exceptions import KISBadArguments

if TYPE_CHECKING:
    from .balance import OverseasBalance
    from .order import OverseasOrder
    from .quote import OverseasQuote


class OverseasClient(KisClientBase):
    """해외 주식 전용 Client"""

    NAME = "OVERSEAS"
    SYMBOL_MASTER = MasterBook.get("USA")

    def __init__(
        self,
        is_dev: bool = True,
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None,
        account: Optional[str] = None,
        exchange: Union[str, Exchange] = None,
    ):
        super().__init__(
            is_dev=is_dev,
            app_key=app_key,
            app_secret=app_secret,
            account=account,
        )
        self.exchange = exchange

    @property
    def exchange(self) -> Optional[Exchange]:
        return self._exchange

    @exchange.setter
    def exchange(self, exchange: Optional[Union[str, Exchange]] = None):
        if exchange:
            exchange = Exchange.from_value(exchange)
            if not exchange:
                raise KISBadArguments("'exchange' is required")
        self._exchange = exchange

    @validator("exchange")
    def validate_exchange(cls, exchange: Union[str, Exchange]) -> Optional[Exchange]:
        if not exchange:
            return None
        return Exchange.from_value(exchange)

    @property
    def is_day(self) -> bool:
        """
        해외주식 주야간원장구분조회를 통해 주간인지 여부를 확인합니다.

        :reference: https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_4e89faf9-0109-4f33-b463-fd88e01cc9b2
        :return: True if day, False if night
        """
        headers = {"tr_id": "JTTT3010R"}
        res = self.session.post(
            "/uapi/overseas-stock/v1/trading/dayornight", headers=headers
        )
        return res.json()["output"]["PSBL_YN"] == "N"

    @staticmethod
    def get_currency() -> Currency:
        res = requests.get(
            "https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD"
        )
        data = res.json()[0]
        return Currency(
            price=data["basePrice"],
            opening=data["openingPrice"],
            change=data["changePrice"],
            buying=data["cashBuyingPrice"],
            selling=data["cashSellingPrice"],
            sending=data["ttBuyingPrice"],
            receiving=data["ttSellingPrice"],
        )

    @cached_property
    def quote(self) -> "OverseasQuote":
        from .quote import OverseasQuote

        return OverseasQuote(client=self)

    @cached_property
    def order(self) -> "OverseasOrder":
        from .order import OverseasOrder

        return OverseasOrder(client=self)

    @cached_property
    def balance(self) -> "OverseasBalance":
        from .balance import OverseasBalance

        return OverseasBalance(client=self)


class OverseasResource:
    def __init__(self, client: OverseasClient):
        self.client = client

    @property
    def is_dev(self) -> bool:
        return self.client.is_dev
