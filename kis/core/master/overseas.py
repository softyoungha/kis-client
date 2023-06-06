import os

import pandas as pd

from . import MasterBook


class OverseasMaster(MasterBook):

    def __init__(self, name: str):
        super().__init__(exchange=name)

    def get_dataframe(self) -> pd.DataFrame:
        file_name = os.path.join(self.cache_dir, f"{self.name.upper()}MST.COD")
        if not os.path.exists(file_name):
            self.download_file()

        columns = [
            "national_code",
            "exchange_id",
            "exchange_code",
            "exchange_name",
            "symbol",
            "realtime_symbol",
            "korean_name",
            "english_name",
            "security_type",  # (1:Index,2:Stock,3:ETP(ETF),4:Warrant)
            "currency",
            "float_position",
            "data_type",
            "base_price",
            "bid_order_size",
            "ask_order_size",
            "market_start_time",  # (HHMM)
            "market_end_time",  # (HHMM)
            "dr_yn",  # (Y/N)
            "dr_national_code",  # DR국가코드
            "sector",  # 업종분류코드
            "existence_of_constituent_stocks",  # 지수구성종목 존재 여부 (0:구성종목없음,1:구성종목있음)
            "tick_size_type",
            "type",  # 구분코드(001:ETF,002:ETN,003:ETC,004:Others,005:VIX Underlying ETF,006:VIX Underlying ETN)
            "tick_size_type_detail"
        ]

        df = pd.read_table(file_name, sep="\t", encoding="cp949")
        df.columns = columns
        return df
