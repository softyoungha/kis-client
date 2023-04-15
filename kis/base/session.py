import logging
from datetime import datetime
from typing import Dict, Optional

import requests
from requests.sessions import merge_setting
from requests.structures import CaseInsensitiveDict

from kis.exceptions import KISServerHTTPError, KISServerInternalError
from .schema import CreateTokenRespData, DestroyTokenRespData, GetHashKeyRespData

logger = logging.getLogger(__name__)


class KisSession(requests.Session):

    def __init__(self, credentials: Dict[str, str], base_url: str):
        super().__init__()
        self.credentials = credentials
        self.base_url: str = base_url

        # default header
        self.set_default_headers(
            {"content-type": "application/json; charset=UTF-8"}
        )

        # token
        self.token: Optional[str] = None
        self.token_expired_at: Optional[int] = None

    def set_default_headers(self, headers: dict):
        self.headers = merge_setting(
            self.headers or {}, headers, dict_class=CaseInsensitiveDict
        )
        return self

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        if self.is_token_expired:
            self.login()

        if not url.startswith(self.base_url):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        logger.debug("- %s, %s", method, url)
        try:
            res = super().request(method=method, url=url, **kwargs)
            res.raise_for_status()
            return res
        except requests.exceptions.HTTPError as err:
            raise KISServerHTTPError(url) from err
        except requests.exceptions.ConnectionError as err:
            raise KISServerInternalError(url) from err

    def create_token(self) -> CreateTokenRespData:
        data = {
            "grant_type": "client_credentials",
            **self.credentials
        }

        res = requests.post(
            f"{self.base_url}/oauth2/tokenP",
            json=data,
            headers={"content-type": "application/json; charset=UTF-8"}
        )
        return CreateTokenRespData(**res.json())

    def destroy_token(self):
        data = {
            "token": self.token,
            **self.credentials
        }

        res = requests.post(
            f"{self.base_url}/oauth2/tokenP",
            json=data,
            headers={"content-type": "application/json; charset=UTF-8"}
        )
        return DestroyTokenRespData(**res.json())

    def get_hash_key(self, body: Dict[str, str]) -> GetHashKeyRespData:
        res = requests.post(
            f"{self.base_url}/uapi/hashkey",
            json=body,
            headers={
                "content-type": "application/json; charset=UTF-8",
                "User-Agent": "Mozilla/5.0",
                **self.credentials,
            }
        )
        return GetHashKeyRespData(**res.json())

    @property
    def is_token_expired(self) -> bool:
        if self.token is None:
            return True
        return datetime.now().timestamp() > self.token_expired_at

    def login(self):
        data = self.create_token()

        # renew expired_at
        self.token = data.access_token
        self.token_expired_at = int(datetime.now().timestamp()) + data.expires_in

        # set header
        self.set_default_headers(
            {
                "Authorization": f"Bearer {data.access_token}",
                **self.credentials
            }
        )
