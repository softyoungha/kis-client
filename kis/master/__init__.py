from urllib import request
import os
from abc import ABCMeta
from typing import Optional
import zipfile
import tempfile
from kis.enum import Exchange
from typing import Union
from kis.exceptions import KISBadArguments

MASTER_DIR = os.path.join(os.getcwd(), ".cache", "master")


class MasterBook(metaclass=ABCMeta):
    """
    Master book class.
    종목코드 마스터 파일을 다운로드하고, 데이터프레임으로 변환하는 클래스입니다.

    :example:
    >>> import pandas as pd
    >>> from kis.master import MasterBook
    >>> df: pd.DataFrame = MasterBook.get("kospi")
    >>> df.head()
    >>>
    >>> df: pd.DataFrame = MasterBook.get("KOSDAQ", only_symbol=True)
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
            with tempfile.TemporaryDirectory(prefix="kis-", suffix=self.name) as dirname:
                self.download_file(dirname)

    def get_dataframe(self):
        """Get master dataframe."""
        raise NotImplemented("create_dataframe method must be implemented.")

    @classmethod
    def get(cls, name: str, only_symbol: bool = False):
        """
        Get master book instance by exchange name.
        :param name: exchange name
        :param only_symbol: if True, return only symbol column
        """
        if (name := name.upper()) in list(Exchange):
            if name == Exchange.KOSPI:
                from .kospi import KospiMaster
                master = KospiMaster()
                symbol_columns = ["단축코드", "한글명", "그룹코드"]
                renamed_symbol_columns = ["symbol", "korean", "group"]
            elif name == Exchange.KOSDAQ:
                from .kosdaq import KosdaqMaster
                master = KosdaqMaster()
                symbol_columns = ["단축코드", "한글명", "증권그룹구분코드"]
                renamed_symbol_columns = ["symbol", "korean", "group"]
            else:
                from .overseas import OverseasMaster
                master = OverseasMaster(name)
                symbol_columns = ["national_code", "exchange_code", "symbol", "korean_name"]
                renamed_symbol_columns = ["nation_code", "exchange", "symbol", "korean"]

            df = master.get_dataframe()
            if only_symbol:
                return (
                    df
                    .loc[:, symbol_columns]
                    .rename(columns=dict(zip(symbol_columns, renamed_symbol_columns)))
                )
            return df
        raise ValueError("Invalid exchange name.")
