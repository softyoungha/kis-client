import os
import tempfile
import zipfile
from abc import ABCMeta
from typing import Literal, Optional, Union, overload
from urllib import request

import pandas as pd

from kis.constants import CONFIG_DIR
from kis.core.enum import Exchange

MASTER_DIR = os.path.join(CONFIG_DIR, "master")


class MasterBook(metaclass=ABCMeta):
    """
    Master book class.
    종목코드 마스터 파일을 다운로드하고, 데이터프레임으로 변환하는 클래스입니다.

    :example:
    >>> import pandas as pd
    >>> from kis.core import MasterBook
    >>> df: pd.DataFrame = MasterBook.get("kospi")
    >>> df.head()
    >>>
    >>> df: pd.DataFrame = MasterBook.get("KOSDAQ", with_detail=True)
    >>> df.head()
    >>>
    >>> df: pd.DataFrame = MasterBook.get("AMS")
    >>> df.head()
    """

    def __init__(self, exchange: Union[str, Exchange]):
        exchange = Exchange.from_value(exchange)

        self.exchange = exchange
        self.master_info = self.exchange.master_file_name
        self.cache_dir = os.path.join(MASTER_DIR, exchange)

    @property
    def name(self):
        """Get exchange name."""
        return self.exchange.name.lower()

    @property
    def url(self):
        """Get master file url."""
        return (
            "https://new.real.download.dws.co.kr/common/master/"
            + self.exchange.master_file_name
        )

    def download_file(self, dirname: Optional[str] = None):
        """Download master file and unzip it."""
        if dirname:

            # path
            master_path = os.path.join(dirname, "code.zip")
            save_dir = os.path.join(MASTER_DIR, self.name)

            # download
            request.urlretrieve(self.url, filename=master_path)

            # unzip
            zip = zipfile.ZipFile(master_path)
            zip.extractall(save_dir)
            zip.close()

        else:
            with tempfile.TemporaryDirectory(
                prefix="kis-", suffix=self.name
            ) as dirname:
                self.download_file(dirname)

    def get_dataframe(self):
        """Get master dataframe."""
        raise NotImplemented("create_dataframe method must be implemented.")

    @overload
    @classmethod
    def get(cls, name: str, with_detail: bool = False) -> pd.DataFrame:
        """str을 사용하는 경우(lower/upper case 허용)"""
        ...

    @overload
    @classmethod
    def get(
        cls,
        name: Literal["KOSPI", "KOSDAQ", "KRX", "NAS", "NYS", "AMS", "USA"],
        with_detail: bool = False,
    ) -> pd.DataFrame:
        """str을 사용하는 경우"""
        ...

    @overload
    @classmethod
    def get(cls, name: Exchange, with_detail: bool = False) -> pd.DataFrame:
        """Exchange enum을 사용하는 경우"""
        ...

    @classmethod
    def get(cls, name: str, with_detail: bool = False) -> pd.DataFrame:
        """
        Get master book instance by exchange name.
        :param name: exchange name
            한국: 'KOSPI', 'KOSDAQ', 'KRX'(KOSPI + KOSDAQ)
            해외: 'NAS','NYS','AMS', 'USA'(NAS + NYS + AMS)
                  and etc('SHS','SHI','SZS','SZI','TSE','HKS','HNX','HSX')
        :param with_detail: if False, return only symbol column
        """
        if name == "KRX":
            return pd.concat(
                [
                    cls.get(Exchange.KOSPI, with_detail=with_detail),
                    cls.get(Exchange.KOSDAQ, with_detail=with_detail),
                ],
                axis=0,
            )

        if name == "USA":
            return pd.concat(
                [
                    cls.get(Exchange.NAS, with_detail=with_detail),
                    cls.get(Exchange.NYS, with_detail=with_detail),
                    cls.get(Exchange.AMS, with_detail=with_detail),
                ],
                axis=0,
            )

        if (name := name.upper()) in list(Exchange):
            if name == Exchange.KOSPI:
                from .kospi import KospiMaster

                master = KospiMaster()
                symbol_columns = ["단축코드", "한글명", "그룹코드"]
                renamed_symbol_columns = ["symbol", "symbol_name", "group"]
            elif name == Exchange.KOSDAQ:
                from .kosdaq import KosdaqMaster

                master = KosdaqMaster()
                symbol_columns = ["단축코드", "한글명", "증권그룹구분코드"]
                renamed_symbol_columns = ["symbol", "symbol_name", "group"]
            else:
                from .overseas import OverseasMaster

                master = OverseasMaster(name)
                symbol_columns = [
                    "national_code",
                    "exchange_code",
                    "symbol",
                    "korean_name",
                ]
                renamed_symbol_columns = [
                    "nation_code",
                    "exchange",
                    "symbol",
                    "symbol_name",
                ]

            df = master.get_dataframe()
            if with_detail:
                return df
            return df.loc[:, symbol_columns].rename(
                columns=dict(zip(symbol_columns, renamed_symbol_columns))
            )
        raise ValueError("Invalid exchange name.")
