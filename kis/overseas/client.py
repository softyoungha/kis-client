from typing import Optional, Union
from functools import cached_property
from pydantic import validator
from kis.base import KisClientBase
from kis.enum import Exchange
from kis.exceptions import KISBadArguments
from .quote import OverseasQuote
from .order import OverseasOrder
from .balance import OverseasBalance


class OverseasClient(KisClientBase):
    exchange: Optional[Exchange] = None

    @validator("exchange")
    def validate_exchange(cls, exchange: Union[str, Exchange]) -> Optional[Exchange]:
        if not exchange:
            return None
        return Exchange.from_value(exchange)

    @cached_property
    def quote(self) -> "OverseasQuote":
        return OverseasQuote(client=self)

    @cached_property
    def order(self) -> "OverseasOrder":
        return OverseasOrder(client=self)

    @cached_property
    def balance(self) -> "OverseasBalance":
        return OverseasBalance(client=self)


OverseasQuote.update_forward_refs(OverseasClient=OverseasClient)
OverseasOrder.update_forward_refs(OverseasClient=OverseasClient)
OverseasBalance.update_forward_refs(OverseasClient=OverseasClient)