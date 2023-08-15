import configparser
import logging
import os
from functools import cached_property
from typing import (
    TYPE_CHECKING,
    Dict,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    overload,
)

from pydantic import SecretStr

from kis.constants import CONFIG_PATH, KIS_ACCOUNT, KIS_APP_KEY, KIS_APP_SECRET
from kis.exceptions import (
    KISAccountNotFound,
    KISBadArguments,
    KISSecretNotFound,
    handle_error,
)

from .schema import ResponseData, ResponseDataDetail
from .session import KisSession

if TYPE_CHECKING:
    from kis.core.base.resources import Balance, Order, Quote

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

    @overload
    def __init__(
        self,
        is_dev: bool,
        app_key: str,
        app_secret: str,
        account: str,
    ):
        """is_dev, app_key, app_secret, account 직접 입력"""
        ...

    @overload
    def __init__(self, profile_name: str):
        """`kis config init`으로 설정된 `profile_name` 사용"""
        ...

    @overload
    def __init__(self, strict: Literal[True]):
        """`kis config init`으로 설정된 `default` profile_name 사용"""
        ...

    def __init__(
        self,
        is_dev: bool = True,
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None,
        account: Optional[str] = None,
        profile_name: Optional[str] = None,
        load_token: bool = True,
        token_path: Optional[str] = None,
        strict: bool = False,
    ):
        """
        KisClient Base Class

        DomesticClient(국내 주식), OverseasClient(해외 주식)의 부모 클래스로 Kis 서버와
        직접 연결하는 Session을 생성합니다. app_key, app_secret, account, is_dev 여부는 필수이며,
        `python -m kis config init`으로 먼저 입력받았다면 profile_name만 입력받아도 작동합니다.

        `session` property 로 Kis 서버와 직접 통신하는 `KisSession` 객체를 얻을 수 있습니다.
        `KisSession`는 client로 입력받은 `app_key`, `app_secret`, `account` 정보를 통해
        첫번째 request를 전송할 때 자동으로 token을 생성/갱신하는 Pretty requests.Session class입니다.
        requests 라이브러리의 get/post/put/delete/patch 메서드를 사용할 수 있으므로 KIS OpenAPI에서
        필요한 기능을 커스텀할 수 있습니다.

        :param is_dev: 모의투자 여부
        :param app_key: KIS OpenAPI app_key
        :param app_secret: KIS OpenAPI app_secret
        :param account: app_key, app_secret을 발급받은 증권계좌번호(예: 12345678-01)
        :param profile_name: `kis config init`에서 등록한 profile_name
        :param load_token: 디스크에 저장된 token을 재사용할지 여부. False일 경우 새로운 토큰 생성
        :param token_path: 임의로 저장된 token_path 사용.
        :param strict: strict mode.
            [KisClient]
            False이고 입력받은 app_key, app_secret, account가 없을 경우 profile_name을 'default'로 변경
            [Exchange, 거래소 관련]
            False일 경우 입력받은 symbol에 대해서 자동으로 거래소를 찾음.
            True일 경우 거래소를 입력받아야 함.
        """
        if (
            not strict
            and not app_key
            and not app_secret
            or not account
            or not profile_name
        ):
            logger.warning(
                "strict mode is False. profile_name will be set to 'default'"
            )
            profile_name = "default"

        self.profile_name = profile_name
        if profile_name:
            if not os.path.exists(CONFIG_PATH):
                raise KISBadArguments(f"Config file not found: '{CONFIG_PATH}'")
            config = configparser.ConfigParser()
            config.read(CONFIG_PATH)
            if profile_name not in config.sections():
                raise KISBadArguments(
                    f"Profile '{profile_name}' not found in config file: '{CONFIG_PATH}'"
                )
            if is_dev or app_key or app_secret or account:
                logger.warning(
                    "`profile_name` is given. "
                    "`is_dev`, `app_key`, `app_secret`, `account` will be ignored."
                )

            self.is_dev = config[profile_name]["is_dev"]
            app_key = config[profile_name]["app_key"]
            app_secret = config[profile_name]["app_secret"]
            account = config[profile_name]["account"]

        else:
            self.is_dev = is_dev

        self.strict = strict
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
        """
        KisSession 객체를 로드합니다.

        첫번째 client 생성시 캐싱된 후 이후에는 해당 session을 재사용합니다.
        만약 생성된 session에 문제가 생긴 경우 client를 재생성해야 합니다.
        """
        credentials = {
            "appkey": self.app_key.get_secret_value(),
            "appsecret": self.app_secret.get_secret_value(),
        }
        return KisSession(
            client=self,
            credentials=credentials,
            base_url=get_base_url(is_dev=self.is_dev),
        )

    @cached_property
    def quote(self) -> "Quote":
        """주식 시세 조회를 위한 subclass"""
        from kis.core.base.resources import Quote

        return Quote(client=self)

    @cached_property
    def order(self) -> "Order":
        """주식 주문을 위한 subclass"""
        from kis.core.base.resources import Order

        return Order(client=self)

    @cached_property
    def balance(self) -> "Balance":
        """주식 잔고 조회를 위한 subclass"""
        from kis.core.base.resources import Balance

        return Balance(client=self)

    @overload
    def fetch_data(
        self,
        url: str,
        headers: Dict[str, str],
        params: Optional[Dict[str, str]],
        data_class: Literal[None] = None,
        summary_class: Literal[None] = None,
        detail_class: Literal[None] = None,
        **kwargs,
    ) -> ResponseData[Dict[str, str]]:
        """Fetch data from KIS API - no pydantic class"""
        ...

    @overload
    def fetch_data(
        self,
        url: str,
        headers: Dict[str, str],
        params: Dict[str, str],
        data_class: Type[DataSchema],
        summary_class: Literal[None] = None,
        detail_class: Literal[None] = None,
        **kwargs,
    ) -> ResponseData[DataSchema]:
        """Fetch data from KIS API - with one pydantic class"""
        ...

    @overload
    def fetch_data(
        self,
        url: str,
        headers: Dict[str, str],
        params: Optional[Dict[str, str]],
        summary_class: Type[SummarySchema],
        detail_class: Type[DetailSchema],
        data_class: Literal[None] = None,
        **kwargs,
    ):
        """Fetch data from KIS API - with two pydantic classes(summary/detail)"""
        ...

    def fetch_data(
        self,
        url: str,
        headers: Dict[str, str],
        params: Optional[Dict[str, str]] = None,
        data_class=None,
        summary_class=None,
        detail_class=None,
        key_column: str = None,
    ):
        res = self.session.get(url, headers=headers, params=params or None)
        data = res.json()

        # handle error
        handle_error(data)

        # key column
        if key_column is not None:
            if not data["output"].get(key_column, "").strip():
                raise KISBadArguments("No such data")

        data.update(tr_id=res.headers.get("tr_id"), tr_cont=res.headers.get("tr_cont"))

        if data_class:
            return ResponseData[data_class](**data)
        if summary_class or detail_class:
            if summary_class and detail_class:
                return ResponseDataDetail[summary_class, detail_class](**data)
            raise KISBadArguments(
                "Either 'summary_class' or 'detail_class' must be set"
            )
        return data

    @overload
    def send_order(
        self,
        url: str,
        headers: Dict[str, str],
        body: Dict[str, str],
        data_class: Literal[None] = None,
    ) -> ResponseData[Dict[str, str]]:
        """Send order to KIS API - no pydantic class"""
        ...

    @overload
    def send_order(
        self,
        url: str,
        headers: Dict[str, str],
        body: Dict[str, str],
        data_class: Type[DataSchema],
    ) -> ResponseData[DataSchema]:
        """Send order to KIS API - with one pydantic class"""
        ...

    def send_order(
        self, url: str, headers: Dict[str, str], body: Dict[str, str], data_class=None
    ):
        # get hash key
        res = self.session.get_hash_key(body)
        hash_key = res.hash
        headers = headers.copy()
        headers.update({"hashkey": hash_key})

        # post
        res = self.session.post(url, headers=headers, json=body)
        data = res.json()

        # handle error
        handle_error(data)

        if data_class:
            return ResponseData[data_class](**data)
        return data
