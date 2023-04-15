from functools import cached_property

from kis.base import KisClientBase
from .quote import DomesticQuote
from .order import DomesticOrder
from .balance import DomesticBalance


class DomesticClient(KisClientBase):

    @cached_property
    def quote(self) -> "DomesticQuote":
        return DomesticQuote(client=self)

    @cached_property
    def order(self) -> "DomesticOrder":
        return DomesticOrder(client=self)

    @cached_property
    def balance(self) -> "DomesticBalance":
        return DomesticBalance(client=self)
