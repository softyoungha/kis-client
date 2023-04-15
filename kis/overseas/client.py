from functools import cached_property

from kis.base import KisClientBase
from .quote import OverseasQuote
from .order import OverseasOrder
from .balance import OverseasBalance


class OverseasClient(KisClientBase):

    @cached_property
    def quote(self) -> "OverseasQuote":
        return OverseasQuote(client=self)

    @cached_property
    def order(self) -> "OverseasOrder":
        return OverseasOrder(client=self)

    @cached_property
    def balance(self) -> "OverseasBalance":
        return OverseasBalance(client=self)
