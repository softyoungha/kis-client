import logging
from datetime import datetime
import time
from typing import Dict, Optional
from functools import cached_property
import os

import requests
from requests.sessions import merge_setting
from requests.structures import CaseInsensitiveDict

from kis.utils.tool import load_yaml, save_yaml
from kis.exceptions import KISServerHTTPError, KISServerInternalError, KISBadArguments
from .schema import Token, DestroyTokenRespData, GetHashKeyRespData

logger = logging.getLogger(__name__)

REQUEST_MIN_INTERVAL = 0.0001


class KisSession(requests.Session):

    def __init__(
            self,
            credentials: Dict[str, str],
            base_url: str,
            token_path: str = None,
    ):
        super().__init__()
        self.credentials = credentials
        self.base_url: str = base_url

        # default header
        self.set_default_headers(
            {"content-type": "application/json; charset=UTF-8"}
        )

        # request interval을 유지하기 위해 사용
        self.last_request_timestamp = time.time()

        # init
        self._token_path = token_path
        if token_path := self.token_path:
            try:
                self.token = Token(**load_yaml(token_path))
            except Exception:
                self.token = None
            self.login(self.token)

    def set_default_headers(self, headers: dict):
        self.headers = merge_setting(
            self.headers or {}, headers, dict_class=CaseInsensitiveDict
        )
        return self

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        if not self.token:
            self.login()

        if self.token.is_expired:
            self.login()

        if not url.startswith(self.base_url):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"

        # 간격 사이에 request가 발생하면 time.sleep
        now = time.time()
        if self.last_request_timestamp - now < REQUEST_MIN_INTERVAL:
            time.sleep(REQUEST_MIN_INTERVAL - (self.last_request_timestamp - now))

        logger.debug("- %s, %s", method, url)
        try:
            self.last_request_timestamp = time.time()
            res = super().request(method=method, url=url, **kwargs)
            res.raise_for_status()
            return res
        except requests.exceptions.HTTPError as err:
            raise KISServerHTTPError(url) from err
        except requests.exceptions.ConnectionError as err:
            raise KISServerInternalError(url) from err

    @cached_property
    def token_path(self):
        return (
                self._token_path
                or os.getenv("KIS_TOKEN_PATH")
                or os.path.join(os.getcwd(), ".cache", "token.yaml")
        )

    def create_token(self):
        data = {
            "grant_type": "client_credentials",
            **self.credentials
        }

        try:
            self.last_request_timestamp = time.time()
            res = requests.post(
                f"{self.base_url}/oauth2/tokenP",
                json=data,
                headers={"content-type": "application/json; charset=UTF-8"}
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise KISBadArguments("Invalid credentials") from err
        except requests.exceptions.ConnectionError as err:
            raise KISServerInternalError("KIS Server Internal Error") from err

        # get new token info
        token = Token(**res.json())

        # save token info as yaml file
        os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
        save_yaml(self.token.dict(), file_path=self.token_path)
        return token

    def login(self, token: Token = None):
        if not token:
            token = self.create_token()

        # set header
        self.set_default_headers(
            {
                "Authorization": f"Bearer {token.access_token}",
                **self.credentials
            }
        )

    def destroy_token(self):
        data = {
            "token": self.token,
            **self.credentials
        }

        self.last_request_timestamp = time.time()
        res = requests.post(
            f"{self.base_url}/oauth2/tokenP",
            json=data,
            headers={"content-type": "application/json; charset=UTF-8"}
        )
        return DestroyTokenRespData(**res.json())

    def get_hash_key(self, body: Dict[str, str]) -> GetHashKeyRespData:
        try:
            self.last_request_timestamp = time.time()
            res = requests.post(
                f"{self.base_url}/uapi/hashkey",
                json=body,
                headers={
                    "content-type": "application/json; charset=UTF-8",
                    "User-Agent": "Mozilla/5.0",
                    **self.credentials,
                }
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise KISBadArguments("Invalid credentials") from err
        except requests.exceptions.ConnectionError as err:
            raise KISServerInternalError("KIS Server Internal Error") from err

        return GetHashKeyRespData(**res.json())
