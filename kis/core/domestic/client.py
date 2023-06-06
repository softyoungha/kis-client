from typing import TYPE_CHECKING
from functools import cached_property

from kis.core.base import KisClientBase

if TYPE_CHECKING:
    from .quote import DomesticQuote
    from .order import DomesticOrder
    from .balance import DomesticBalance


class DomesticClient(KisClientBase):
    """국내 주식 전용 Client"""
    NAME = "DOMESTIC"

    @cached_property
    def quote(self) -> "DomesticQuote":
        from .quote import DomesticQuote
        return DomesticQuote(client=self)

    @cached_property
    def order(self) -> "DomesticOrder":
        from .order import DomesticOrder
        return DomesticOrder(client=self)

    @cached_property
    def balance(self) -> "DomesticBalance":
        from .balance import DomesticBalance
        return DomesticBalance(client=self)


class DomesticResource:
    def __init__(self, client: DomesticClient):
        self.client = client

    @property
    def is_dev(self) -> bool:
        return self.client.is_dev
