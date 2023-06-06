import logging
from datetime import datetime
import time
from typing import Dict, TYPE_CHECKING, Optional
from functools import cached_property
import os

import requests
from requests.sessions import merge_setting
from requests.structures import CaseInsensitiveDict

from kis.utils.tool import load_yaml, save_yaml
from kis.exceptions import KISServerHTTPError, KISServerInternalError, KISBadArguments, KISRecursionError
from .schema import Token, DestroyTokenRespData, GetHashKeyRespData

if TYPE_CHECKING:
    from kis.core.base.client import KisClientBase

logger = logging.getLogger(__name__)

REQUEST_MIN_INTERVAL = 0.1


class KisSession(requests.Session):

    def __init__(
            self,
            client: "KisClientBase",
            credentials: Dict[str, str],
            base_url: str,
    ):
        super().__init__()
        self.client = client
        self.credentials = credentials
        self.base_url: str = base_url

        # default header
        self.set_default_headers(
            {"content-type": "application/json; charset=UTF-8"}
        )

        # request interval을 유지하기 위해 사용
        self._last_request_time = time.time()

        # init token info
        self._token = None
        self._token_path = self.client.token_path

        # 처음 생성시 token load
        if self.client.load_token and (token_path := self.token_path):
            if os.path.exists(token_path):
                try:
                    self.token = Token(**load_yaml(token_path))
                    logger.info(f"Token file is loaded.")
                except Exception:
                    logger.info("Something is wrong in token. Need to create new token.")

    def set_default_headers(self, headers: dict):
        self.headers = merge_setting(
            self.headers or {}, headers, dict_class=CaseInsensitiveDict
        )
        return self

    @cached_property
    def token_path(self) -> str:
        """ Get token path from client or environment variable or default path """
        return (
                self._token_path
                or os.getenv("KIS_TOKEN_PATH")
                or os.path.join(os.getcwd(), ".cache", self.client.account, "token.yaml")
        )

    @property
    def token(self) -> Token:
        return self._token

    @token.setter
    def token(self, value: Token):
        # set header
        self.set_default_headers({
            "Authorization": f"Bearer {value.access_token}",
            **self.credentials
        })
        self._token = value

    @property
    def is_token_valid(self) -> bool:
        if self.token is None:
            logger.info("Token is not exist. Create new token.")
            return False
        if self.token.is_expired:
            logger.info(f"Token is expired. Create new token.")
            return False
        return True

    def request(self, method: str, url: str, after_login: bool = False, **kwargs) -> requests.Response:
        """ get/post/put/patch/delete 등 요청을 보내는 base method """
        # renew token
        if not self.is_token_valid or after_login:
            self.create_token()

        if not url.startswith(self.base_url):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"

        # 간격 사이에 request가 발생하면 time.sleep
        # Too many request 방지
        diff = time.time() - self._last_request_time
        if diff < REQUEST_MIN_INTERVAL:
            sleep = REQUEST_MIN_INTERVAL - diff
            time.sleep(sleep)

        logger.debug("- %s, %s", method, url)
        self._last_request_time = time.time()
        res = super().request(method=method, url=url, **kwargs)

        try:
            res.raise_for_status()
            return res
        except requests.exceptions.HTTPError as err:
            data = res.json()
            msg_code = data["msg_cd"]

            if data["rt_cd"] == "1":

                if msg_code == "EGW00123":
                    # 서버로부터 토큰 만료 응답 받음
                    # -> token 새로 생성 후 after_login=True로 다시 요청
                    if not after_login:
                        logger.warning(f"Token is wrong. Create new token.: {data['msg1']}")
                        return self.request(
                            method=method,
                            url=url,
                            after_login=True,
                            **kwargs
                        )
                    raise KISBadArguments(f"{msg_code}: {data['msg1']}") from err
                elif msg_code == "90070000":
                    # "모의투자 처리계좌의 ID와 사용자정보가 상이하여 처리 불가능 합니다."
                    raise KISBadArguments(f"{msg_code}: {data['msg1']}") from err

                elif msg_code == "IGW00002":
                    # 인증 시점의 계좌번호와 요청 계좌번호가 일치하지 않습니다
                    raise KISBadArguments(f"{msg_code}: {data['msg1']}") from err
            logger.error(f"KIS Server Error: {msg_code} {data['msg1']}")
            raise KISServerHTTPError(url) from err
        except requests.exceptions.ConnectionError as err:
            raise KISServerInternalError(url) from err

    def create_token(self):
        """Create new token and save it as yaml file"""
        data = {
            "grant_type": "client_credentials",
            **self.credentials
        }

        self._last_request_time = time.time()
        try:
            res = requests.post(
                f"{self.base_url}/oauth2/tokenP",
                json=data,
                headers={"content-type": "application/json; charset=UTF-8"}
            )
            res.raise_for_status()
            data = res.json()
        except requests.exceptions.HTTPError as err:
            if data["error_code"] == "EGW00102":
                raise KISBadArguments(data["error_description"]) from err
            raise KISBadArguments("Invalid credentials") from err
        except requests.exceptions.ConnectionError as err:
            raise KISServerInternalError("KIS Server Internal Error") from err

        # get new token info
        token = Token(
            access_token=data["access_token"],
            token_type=data["token_type"],
            expired_at=int(datetime.now().timestamp()) + data["expires_in"],
        )

        # save token info as yaml file
        save_yaml(token.dict(), file_path=self.token_path)
        logger.info(f"Token is saved successfully in '{self.token_path}'")

        # save token
        self.token = token
        return token

    def destroy_token(self):
        """Destroy token in KIS server and remove token file"""
        data = {
            "token": self.token,
            **self.credentials
        }

        self._last_request_time = time.time()
        res = requests.post(
            f"{self.base_url}/oauth2/tokenP",
            json=data,
            headers={"content-type": "application/json; charset=UTF-8"}
        )
        logger.info("Token is destroyed successfully in KIS server")

        os.remove(self.token_path)
        logger.info(f"Token is removed successfully in '{self.token_path}'")
        return DestroyTokenRespData(**res.json())

    def get_hash_key(self, body: Dict[str, str]) -> GetHashKeyRespData:
        """Get hash key from KIS server"""
        try:
            self._last_request_time = time.time()
            res = requests.post(
                f"{self.base_url}/uapi/hashkey",
                json=body,
                headers={
                    "content-type": "application/json; charset=UTF-8",
                    "User-Agent": "Mozilla/5.0",
                    "custtype": "P",
                    **self.credentials,
                }
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise KISBadArguments("Invalid credentials") from err
        except requests.exceptions.ConnectionError as err:
            raise KISServerInternalError("KIS Server Internal Error") from err

        logger.info("Hash key is generated successfully")
        return GetHashKeyRespData(**res.json())
