from datetime import timedelta, datetime, date
from typing import Optional, List, Tuple, Union, Dict, Any, TYPE_CHECKING

from dateutil.parser import parse
from datetime import datetime

from kis.base import fetch
from kis.base.client import Quote
from kis.exceptions import KISBadArguments, KISNoData
from kis.utils.tool import as_datetime
from kis.domestic.schema import (
    FetchPrice,
    FetchPricesByMinutesSummary,
    FetchPriceByMinutesHistory,
    FetchOHLCVSummary,
    FetchOHLCVHistory,
)

if TYPE_CHECKING:
    from kis.domestic.client import DomesticClient


class DomesticQuote(Quote):
    client: "DomesticClient"

    @fetch(
        "/uapi/domestic-stock/v1/quotations/inquire-price",
        data_class=FetchPrice
    )
    def fetch_current_price(self, symbol: str):
        """주식현재가시세"""
        headers = {"tr_id": "FHKST01010100", "custtype": "P"}
        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": symbol
        }
        return headers, params

    @fetch(
        "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice",
        summary_class=FetchPricesByMinutesSummary,
        detail_class=List[Dict[str, Any]]
    )
    def _fetch_prices_by_minutes(self, symbol: str, to: Union[str, datetime, date]):
        """
        국내주식시세/주식당일분봉조회
        최대 30개씩 출력
        """
        try:
            datetime.strptime(to, "%H%M%S")
        except ValueError as err:
            raise KISBadArguments() from err

        headers = {"tr_id": "FHKST03010200", "custtype": "P"}
        params = {
            "fid_etc_cls_code": "",
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": symbol,
            "fid_input_hour_1": to,  # HHMMSS
            "fid_pw_data_incu_yn": "Y"
        }
        return headers, params

    def fetch_prices_by_minutes(
            self,
            symbol: str,
            to: Optional[str] = None,
            count: Optional[int] = None
    ) -> Tuple[FetchPricesByMinutesSummary, List[FetchPriceByMinutesHistory]]:
        if not to:
            now = datetime.now()
            if now.weekday() in [5, 6]:
                # 토/일
                to = "153000"
            else:
                # 월
                to = now.strftime("%H%M%S")
                if to > "153000":
                    to = "153000"

        if count is None:
            count = 14

        summary: Optional[FetchPricesByMinutesSummary] = None
        full_histories: List[FetchPriceByMinutesHistory] = []

        while count > 0:
            result = self._fetch_prices_by_minutes(symbol, to)
            summary = result.summary
            histories = [
                FetchPriceByMinutesHistory(**history)
                for history in result.detail
                if history.get("stck_bsop_date")
            ]

            full_histories += histories

            # 30개 이하로 가져오면 break
            if len(histories) != 30:
                break

            # get last output
            to = (histories[-1].full_execution_time - timedelta(minutes=1)).strftime("%H%M%S")
            if to <= "090001":
                break
            count -= 1

        if summary is None:
            raise KISNoData("No 'FetchOHLCVSummary' data found. ")

        return summary, full_histories

    @fetch(
        "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice",
        summary_class=FetchOHLCVSummary,
        detail_class=List[Dict[str, str]]
    )
    def _fetch_histories(
            self,
            symbol: str,
            start_date: Optional[Union[str, datetime, date]] = None,
            end_date: Optional[Union[str, datetime, date]] = None,
            standard: str = "D",
            adjust: bool = True
    ):
        """
        국내주식시세/국내주식기간별시세
        100개씩 리턴
        :param symbol: 종목코드
        :param start_date: 시작일자(예: '20230416')
        :param end_date: 종료일자(예: '20230416')
        :param standard: 기준(일: 'D', 주: 'W', 월: 'M', 년: 'Y')
        :param adjust: 수정주가 여부
        """
        if start_date:
            start_date = as_datetime(start_date, fmt="%Y%m%d")
        else:
            start_date = "19800104"

        if end_date:
            end_date = as_datetime(end_date, fmt="%Y%m%d")
        else:
            end_date = datetime.now().strftime("%Y%m%d")

        headers = {"tr_id": "FHKST03010100", "custtype": "P"}
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
            "FID_INPUT_DATE_1": start_date,
            "FID_INPUT_DATE_2": end_date,
            "FID_PERIOD_DIV_CODE": standard,
            "FID_ORG_ADJ_PRC": "0" if adjust else "1"
        }
        return headers, params

    def fetch_histories(
            self,
            symbol: str,
            start_date: Optional[Union[str, datetime, date]] = None,
            end_date: Optional[Union[str, datetime, date]] = None,
            standard: str = "D",
            count: Optional[int] = None
    ) -> Tuple[FetchOHLCVSummary, List[FetchOHLCVHistory]]:
        if count is None:
            count = 10

        summary: Optional[FetchOHLCVSummary] = None
        full_histories: List[FetchOHLCVHistory] = []
        while count > 0:
            result = self._fetch_histories(
                symbol,
                start_date=start_date,
                end_date=end_date,
                standard=standard
            )

            if summary is None:
                summary = result.summary

            histories = [
                FetchOHLCVHistory(**row)
                for row in result.detail
                if row.get("stck_bsop_date")
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

        if summary is None:
            raise KISNoData("No 'FetchOHLCVSummary' data found. ")

        return summary, full_histories
