import os
from functools import cached_property

from typing import Optional, Tuple
from pydantic import BaseModel, SecretStr, Field, PrivateAttr
from kis.exceptions import KISBadArguments, KISSecretNotFound, KISAccountNotFound

from kis.base.session import KisSession


def get_base_url(is_dev: bool) -> str:
    if is_dev:
        return "https://openapivts.koreainvestment.com:29443"
    return "https://openapi.koreainvestment.com:9443"


class KisClientBase(BaseModel):
    is_dev: bool = True
    app_key: Optional[SecretStr] = None
    app_secret: Optional[SecretStr] = None
    account: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        keep_untouched = (cached_property,)

    def __repr__(self, name: str = None):
        options = []
        if self.is_dev:
            options.append("모의투자")
        else:
            options.append("실거래")
        if self.account:
            options.append(f"account={self.account}")
        else:
            options.append("account='Not Set'")
        return f"{name or self.__repr_name__()}({' '.join(options)})"

    @property
    def account_split(self) -> Tuple[str, str]:
        if not self.account:
            if not (account := os.getenv("KIS_ACCOUNT")):
                raise KISAccountNotFound(
                    "'account' is not set. "
                    "Put 'account' as argument or set $KIS_ACCOUNT env variable."
                )
            self.account = account
        prefix, suffix = self.account.split("-")
        return prefix, suffix

    @cached_property
    def session(self) -> KisSession:
        if not self.app_key:
            if not (app_key := os.getenv("KIS_APP_KEY")):
                raise KISSecretNotFound(
                    "'app_key' is not set. "
                    "Put 'app_key' as argument or set $KIS_APP_KEY env variable."
                )
            self.app_key = SecretStr(app_key)

        if not self.app_secret:
            if not (app_secret := os.getenv("KIS_APP_SECRET")):
                raise KISSecretNotFound(
                    "'app_secret' is not set. "
                    "Put 'app_secret' as argument or set $KIS_APP_SECRET env variable."
                )
            self.app_secret = SecretStr(app_secret)

        credentials = {
            "appkey": self.app_key.get_secret_value(),
            "appsecret": self.app_secret.get_secret_value()
        }
        return KisSession(
            credentials=credentials,
            base_url=get_base_url(is_dev=self.is_dev)
        )

    @property
    def quote(self) -> "Quote":
        return Quote(client=self)

    @cached_property
    def order(self) -> "Order":
        return Order(client=self)

    @cached_property
    def balance(self) -> "Balance":
        return Balance(client=self)


class SubClass(BaseModel):
    client: KisClientBase

    def __repr__(self):
        return self.client.__repr__(self.__repr_name__())

    @property
    def is_dev(self) -> bool:
        return self.client.is_dev


class Quote(SubClass):
    """ 가격 조회 관련 API """

    def fetch_current_price(self, symbol: str):
        """현재가 조회"""
        raise NotImplementedError("fetch_current_price not implemented")

    def _fetch_prices_by_minutes(self, symbol: str, to: str):
        """분봉 조회 출력 30개"""
        raise NotImplementedError("fetch_prices_by_minutes not implemented")

    def fetch_prices_by_minutes(self, symbol: str, to: str):
        """모든일자 분봉 조회"""
        raise NotImplementedError("fetch_all_prices_by_minutes not implemented")

    def _fetch_histories(self, symbol: str, end_date: str, standard: str):
        """기간별 시세 조회 100개"""
        raise NotImplementedError("fetch_ohlcv not implemented")

    def fetch_histories(self, symbol: str, end_date: str, standard: str):
        """기간별 시세 조회"""
        raise NotImplementedError("fetch_all_ohlcv not implemented")


class Order(SubClass):
    """ 주문관련 API """

    def _order(
            self,
            order_type: str,
            symbol: str,
            quantity: int,
            price: int = None,
            as_market_price: bool = False,

    ):
        """
        주문 전송
        :param order_type: 주문구분 (buy, sell)
        :param symbol: 종목코드
        :param quantity: 주문수량
        :param price: 주문단가
        :param as_market_price: 시장가 주문 여부
        """
        raise NotImplementedError("_order not implemented")

    def buy(
            self,
            symbol: str,
            quantity: int,
            price: int = None,
            as_market_price: bool = False,
            **kwargs
    ):
        """
        주식 매수
        :param symbol: 종목코드
        :param quantity: 주문수량
        :param price: 주문단가
        :param as_market_price: 시장가 주문 여부
        """
        return self._order(
            order_type="buy",
            symbol=symbol,
            quantity=quantity,
            price=price,
            as_market_price=as_market_price,
        )

    def sell(
            self,
            symbol: str,
            quantity: int,
            price: int = None,
            as_market_price: bool = False,
    ):
        """
        주식 매도
        :param symbol: 종목코드
        :param quantity: 주문수량
        :param price: 주문단가
        :param as_market_price: 시장가 주문 여부
        """
        return self._order(
            order_type="buy",
            symbol=symbol,
            quantity=quantity,
            price=price,
            as_market_price=as_market_price,
        )

    def _modify(
            self,
            modify_type: str,
            org_no: str,
            order_no: str,
            quantity: int = None,
            total: bool = False,
            price: int = None,
            as_market_price: bool = False,
    ):
        """
        주식 정정/취소
        :param modify_type: 주문구분 (modify, cancel)
        :param org_no: 한국거래소주문조직번호
        :param order_no: 주문번호
        :param quantity: 정정수량
        :param total: 전량 정정 여부
        :param price: 정정단가
        :param as_market_price: 시장가 주문 여부
        """
        raise NotImplementedError("modify not implemented")

    def update(
            self,
            org_no: str,
            order_no: str,
            price: int = None,
            quantity: int = None,
            total: bool = False,
            as_market_price: bool = False,
    ):
        """
        주식 정정
        :param org_no: 한국거래소주문조직번호
        :param order_no: 주문번호
        :param quantity: 정정수량
        :param total: 전량 정정 여부
        :param price: 정정단가
        :param as_market_price: 시장가 주문 여부
        """
        return self._modify(
            modify_type="update",
            org_no=org_no,
            order_no=order_no,
            quantity=quantity,
            total=total,
            price=price,
            as_market_price=as_market_price
        )

    def cancel(
            self,
            org_no: str,
            order_no: str,
            quantity: int = None,
            total: bool = False,
    ):
        """
        주식 취소
        :param org_no:
        :param order_no:
        :param quantity:
        :param total:
        :return:
        """
        return self._modify(
            modify_type="cancel",
            org_no=org_no,
            order_no=order_no,
            quantity=quantity,
            total=total,
        )

    def fetch_orders(
            self,
            order_no: str,
            order_type: str,
    ):
        """주문 조회"""
        raise NotImplementedError("fetch_order not implemented")


class Balance(SubClass):
    """ 잔고 조회 관련 API """

    def fetch(self):
        """주식 잔고 조회"""
        raise NotImplementedError("fetch not implemented")
