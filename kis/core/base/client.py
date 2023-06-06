import logging
from functools import cached_property
from typing import Optional, Tuple, Dict, TYPE_CHECKING, overload, TypeVar, Any, Type, Literal, Union, List

from pydantic import BaseModel, SecretStr

from kis.constants import KIS_APP_KEY, KIS_APP_SECRET, KIS_ACCOUNT
from kis.exceptions import KISBadArguments, KISSecretNotFound, KISAccountNotFound, KISNoData, handle_error
from .session import KisSession
from .schema import ResponseData, ResponseDataDetail

if TYPE_CHECKING:
    from kis.core.base.resources import Quote, Order, Balance, BackTest

logger = logging.getLogger(__name__)

DataSchema = TypeVar("DataSchema")
SummarySchema = TypeVar("SummarySchema")
DetailSchema = TypeVar("DetailSchema")


def get_base_url(is_dev: bool) -> str:
    if is_dev:
        return "https://openapivts.koreainvestment.com:29443"
    return "https://openapi.koreainvestment.com:9443"


class KisClientBase:
    NAME = "ABSTRACT"

    def __init__(
            self,
            is_dev: bool = True,
            app_key: Optional[str] = None,
            app_secret: Optional[str] = None,
            account: Optional[str] = None,
            load_token: bool = True,
            token_path: Optional[str] = None,
    ):
        self.is_dev = is_dev
        self.load_token = load_token
        self.token_path = token_path

        app_key = app_key or KIS_APP_KEY
        if not app_key:
            raise KISSecretNotFound(
                "'app_key' is not set. "
                "Put 'app_key' as argument or set $KIS_APP_KEY env variable."
            )
        self.app_key = SecretStr(app_key)

        app_secret = app_secret or KIS_APP_SECRET
        if not app_secret:
            raise KISSecretNotFound(
                "'app_secret' is not set. "
                "Put 'app_secret' as argument or set $KIS_APP_SECRET env variable."
            )
        self.app_secret = SecretStr(app_secret)

        account = account or KIS_ACCOUNT
        if not account:
            raise KISAccountNotFound(
                "'account' is not set. "
                "Put 'account' as argument or set $KIS_ACCOUNT env variable."
            )
        self.account = account

        logger.info(f"{self} initialized")

    def __repr__(self, name: str = None):
        options = []
        if self.is_dev:
            options.append("모의투자")
        else:
            options.append("실거래")
        if self.account:
            options.append(f"account='{self.account}'")
        else:
            options.append("account='Not Set'")
        return f"{name or self.__class__.__name__}({' '.join(options)})"

    def get_account(self) -> Tuple[str, str]:
        prefix, suffix = self.account.split("-")
        return prefix, suffix

    @cached_property
    def session(self) -> KisSession:
        credentials = {
            "appkey": self.app_key.get_secret_value(),
            "appsecret": self.app_secret.get_secret_value()
        }
        return KisSession(
            client=self,
            credentials=credentials,
            base_url=get_base_url(is_dev=self.is_dev)
        )

    @cached_property
    def quote(self) -> "Quote":
        from kis.core.base.resources import Quote
        return Quote(client=self)

    @cached_property
    def order(self) -> "Order":
        from kis.core.base.resources import Order
        return Order(client=self)

    @cached_property
    def balance(self) -> "Balance":
        from kis.core.base.resources import Balance
        return Balance(client=self)

    @cached_property
    def balance(self) -> "BackTest":
        from kis.core.base.resources import BackTest
        return BackTest(client=self)

    @overload
    def fetch_data(
            self, url: str, headers: Dict[str, str], params: Optional[Dict[str, str]],
            data_class: Literal[None] = None,
            summary_class: Literal[None] = None, detail_class: Literal[None] = None,
            **kwargs
    ) -> ResponseData[Dict[str, str]]:
        """ Fetch data from KIS API - no pydantic class """
        ...

    @overload
    def fetch_data(
            self, url: str, headers: Dict[str, str], params: Dict[str, str],
            data_class: Type[DataSchema],
            summary_class: Literal[None] = None, detail_class: Literal[None] = None,
            **kwargs
    ) -> ResponseData[DataSchema]:
        """ Fetch data from KIS API - with one pydantic class """
        ...

    @overload
    def fetch_data(
            self, url: str, headers: Dict[str, str], params: Optional[Dict[str, str]],
            summary_class: Type[SummarySchema], detail_class: Type[DetailSchema],
            data_class: Literal[None] = None,
            **kwargs
    ):
        """ Fetch data from KIS API - with two pydantic classes(summary/detail) """
        ...

    def fetch_data(
            self, url: str, headers: Dict[str, str], params: Optional[Dict[str, str]] = None,
            data_class=None, summary_class=None, detail_class=None, key_column: str = None
    ):
        res = self.session.get(
            url,
            headers=headers,
            params=params or None
        )
        data = res.json()

        # handle error
        handle_error(data)

        # key column
        if key_column is not None:
            if not data["output"].get(key_column, "").strip():
                raise KISBadArguments("No such data")

        data.update(
            tr_id=res.headers.get("tr_id"),
            tr_cont=res.headers.get("tr_cont")
        )
        from pprint import pprint
        pprint(data)
        if data_class:
            return ResponseData[data_class](**data)
        if summary_class or detail_class:
            if summary_class and detail_class:
                return ResponseDataDetail[summary_class, detail_class](**data)
            raise KISBadArguments("Either 'summary_class' or 'detail_class' must be set")
        return data

    @overload
    def send_order(
            self, url: str, headers: Dict[str, str], body: Dict[str, str],
            data_class: Literal[None] = None
    ) -> ResponseData[Dict[str, str]]:
        """ Send order to KIS API - no pydantic class """
        ...

    @overload
    def send_order(
            self, url: str, headers: Dict[str, str], body: Dict[str, str],
            data_class: Type[DataSchema]
    ) -> ResponseData[DataSchema]:
        """ Send order to KIS API - with one pydantic class """
        ...

    def send_order(
            self,
            url: str,
            headers: Dict[str, str],
            body: Dict[str, str],
            data_class=None
    ):
        # get hash key
        res = self.session.get_hash_key(body)
        hash_key = res.hash
        headers = headers.copy()
        headers.update({"hashkey": hash_key})

        # post
        res = self.session.post(
            url,
            headers=headers,
            json=body
        )
        data = res.json()

        # handle error
        handle_error(data)

        if data_class:
            return ResponseData[data_class](**data)
        return data
