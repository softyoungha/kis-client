from datetime import timedelta, date
from typing import Optional, List, Tuple, Union, Dict, TYPE_CHECKING

from datetime import datetime

from kis.enum import Exchange
from kis.base import fetch
from kis.base.client import Quote
from kis.exceptions import KISBadArguments
from kis.utils.tool import as_datetime
from kis.overseas.schema import (
    FetchPrice,
    FetchPriceDetail,
    FetchOHLCVSummary,
    FetchOHLCVHistory,
)

if TYPE_CHECKING:
    from kis.overseas.client import OverseasClient


class OverseasQuote(Quote):
    client: "OverseasClient"

    @fetch(
        "/uapi/overseas-price/v1/quotations/price",
        data_class=FetchPrice,
    )
    def fetch_current_price(self, symbol: str, exchange: Union[str, Exchange] = None):
        """
        https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-current#L_3eeac674-072d-4674-a5a7-f0ed01194a81
        """
        # get exchange
        exchange = Exchange.from_value(exchange) if exchange else self.client.exchange
        if not exchange:
            raise KISBadArguments("'exchange' is required")

        headers = {"tr_id": "HHDFS00000300", "custtype": "P"}
        params = {
            "AUTH": "",
            "EXCD": exchange.name,
            "SYMB": symbol,
        }
        return headers, params

    @fetch(
        "/uapi/overseas-price/v1/quotations/price-detail",
        data_class=FetchPriceDetail,
    )
    def fetch_current_price_detail(self, symbol: str, exchange: Union[str, Exchange] = None):
        """
        https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-current#L_3eeac674-072d-4674-a5a7-f0ed01194a81
        """
        if not self.is_dev:
            raise KISBadArguments("This API is only available in dev mode")

        # get exchange
        exchange = Exchange.from_value(exchange) if exchange else self.client.exchange
        if not exchange:
            raise KISBadArguments("'exchange' is required")

        headers = {"tr_id": "HHDFS76200200", "custtype": "P"}
        params = {
            "AUTH": "",
            "EXCD": exchange.name,
            "SYMB": symbol,
        }
        return headers, params

    @fetch(
        "/uapi/overseas-price/v1/quotations/dailyprice",
        summary_class=FetchOHLCVSummary,
        detail_class=List[Dict[str, str]]
    )
    def _fetch_histories(
            self,
            symbol: str,
            exchange: Union[str, Exchange] = None,
            end_date: Optional[Union[str, datetime, date]] = None,
            standard: str = "D",
            adjust: bool = True
    ):
        """
        국내주식시세/국내주식기간별시세
        100개씩 리턴
        :param symbol: 종목코드
        :param end_date: 조회 기준일자(예: '20230416')
        :param standard: 기준(일: 'D', 주: 'W', 월: 'M', 년: 'Y')
        :param adjust: 수정주가 여부
        """
        # get exchange
        exchange = Exchange.from_value(exchange) if exchange else self.client.exchange
        if not exchange:
            raise KISBadArguments("'exchange' is required")

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
        return headers, params

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

        def filter_func(row: dict) -> bool:
            business_date = row.get("xymd", "")
            if start_date:
                return start_date.strftime("%Y%m%d") <= business_date
            return bool(business_date) and bool(row.get("tvol"))

        summary: Optional[FetchOHLCVSummary] = None
        full_histories: List[FetchOHLCVHistory] = []
        while count > 0:
            result = self._fetch_histories(
                symbol,
                exchange,
                end_date=end_date,
                standard=standard,
                adjust=adjust
            )

            if summary is None:
                summary = result.summary

            histories = [
                FetchOHLCVHistory(**row)
                for row in result.detail
                if filter_func(row)
            ]

            if not histories:
                break

            full_histories += histories

            # 100개 이하로 가져오면 break
            if len(histories) != 100:
                break

            # start_date에 도달하면 break
            if histories[-1].business_date == start_date:
                break

            # get last output
            last_history = histories[-1]
            end_date = (last_history.business_date - timedelta(days=1)).strftime("%Y%m%d")
            count -= 1

        return summary, full_histories

