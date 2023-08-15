from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, overload

from kis.core.base.resources import Quote
from kis.core.enum import Exchange
from kis.core.overseas.schema import (
    FetchOHLCVHistory,
    FetchOHLCVSummary,
    Price,
    PriceDetail,
)
from kis.exceptions import KISBadArguments, KISDevModeError
from kis.utils.tool import as_datetime

from .client import OverseasResource


class OverseasQuote(OverseasResource, Quote):
    @overload
    def fetch_current_price(self, symbol: str) -> Price:
        """client 생성시 입력한 exchange 사용"""
        ...

    @overload
    def fetch_current_price(self, symbol: str, exchange: Union[str, Exchange]) -> Price:
        """exchange 지정"""
        ...

    def fetch_current_price(
        self,
        symbol: str,
        exchange: Union[str, Exchange] = None,
    ):

        """
        해외주식현재가/해외주식 현재체결가 조회

        See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-current#L_3eeac674-072d-4674-a5a7-f0ed01194a81
        """
        exchange = exchange or self.client.exchange
        if self.client.strict:
            exchange = Exchange.from_value(exchange)
        else:
            exchange = Exchange.find_symbol(symbol)

        headers = {"tr_id": "HHDFS00000300", "custtype": "P"}
        params = {
            "AUTH": "",
            "EXCD": exchange.name,
            "SYMB": symbol,
        }
        return self.client.fetch_data(
            "/uapi/overseas-price/v1/quotations/price",
            headers=headers,
            params=params,
            data_class=Price,
            key_column="base",
        ).data

    def fetch_current_price_detail(
        self, symbol: str, exchange: Union[str, Exchange] = None
    ):
        """
        https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-current#L_3eeac674-072d-4674-a5a7-f0ed01194a81
        """
        if self.is_dev:
            raise KISDevModeError()

        exchange = exchange or self.client.exchange
        if self.client.strict:
            exchange = Exchange.from_value(exchange)
        else:
            exchange = Exchange.find_symbol(symbol)

        headers = {"tr_id": "HHDFS76200200", "csstype": "P"}
        params = {
            "AUTH": "",
            "EXCD": exchange.name,
            "SYMB": symbol,
        }
        return self.client.fetch_data(
            "/uapi/overseas-price/v1/quotations/price-detail",
            headers=headers,
            params=params,
            data_class=PriceDetail,
        )

    def _fetch_histories(
        self,
        symbol: str,
        exchange: Union[str, Exchange] = None,
        end_date: Optional[Union[str, datetime, date]] = None,
        standard: str = "D",
        adjust: bool = True,
    ):
        """
        국내주식시세/국내주식기간별시세
        100개씩 리턴

        :param symbol: 종목코드
        :param end_date: 조회 기준일자(예: '20230416')
        :param standard: 기준(일: 'D', 주: 'W', 월: 'M', 년: 'Y')
        :param adjust: 수정주가 여부
        """
        exchange = exchange or self.client.exchange
        if self.client.strict:
            exchange = Exchange.from_value(exchange)
        else:
            exchange = Exchange.find_symbol(symbol)

        if end_date:
            end_date = as_datetime(end_date, fmt="%Y%m%d")
        else:
            end_date = ""

        if standard == "D":
            standard_code = "0"
        elif standard == "W":
            standard_code = "1"
        elif standard == "M":
            standard_code = "2"
        else:
            raise KISBadArguments("standard must be one of ('D', 'W', 'M')")

        headers = {"tr_id": "HHDFS76240000", "custtype": "P"}
        params = {
            "AUTH": "",
            "SYMB": symbol,
            "EXCD": exchange.name,
            "GUBN": standard_code,
            "BYMD": end_date,
            "MODP": "1" if adjust else "0",
        }
        return self.client.fetch_data(
            "/uapi/overseas-price/v1/quotations/dailyprice",
            headers=headers,
            params=params,
            summary_class=FetchOHLCVSummary,
            detail_class=List[Dict[str, str]],
        )

    def fetch_histories(
        self,
        symbol: str,
        exchange: Union[str, Exchange] = None,
        start_date: Optional[Union[str, datetime, date]] = None,
        end_date: Optional[Union[str, datetime, date]] = None,
        standard: str = "D",
        count: Optional[int] = None,
        adjust: bool = True,
    ) -> Tuple[FetchOHLCVSummary, List[FetchOHLCVHistory]]:
        if count is None:
            count = 10

        if start_date:
            start_date = as_datetime(start_date)

        def filter_func(row: dict) -> bool:
            business_date = row.get("xymd", "")
            try:
                business_date = as_datetime(business_date)
            except ValueError:
                return False
            if start_date:
                return start_date <= business_date
            return bool(business_date) and bool(row.get("tvol"))

        summary: Optional[FetchOHLCVSummary] = None
        full_histories: List[FetchOHLCVHistory] = []
        while count > 0:
            result = self._fetch_histories(
                symbol, exchange, end_date=end_date, standard=standard, adjust=adjust
            )
            # summary update
            if summary is None:
                summary = result.summary
            # filter & map
            histories = [
                FetchOHLCVHistory(**row) for row in result.detail if filter_func(row)
            ]
            # no more histories -> break
            if not histories:
                break
            # append
            full_histories += histories
            # under 100 -> break
            if len(histories) != 100:
                break
            # meet start_date -> break
            if start_date:
                if histories[-1].business_date == start_date:
                    break
            # get last output
            last_history = histories[-1]
            end_date = (last_history.business_date - timedelta(days=1)).strftime(
                "%Y%m%d"
            )
            count -= 1

        return summary, full_histories
