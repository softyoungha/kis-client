import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Literal, Optional, Tuple, Union, overload

from kis.core.base.resources import Quote
from kis.core.domestic.schema import (
    FetchOHLCVHistory,
    FetchOHLCVSummary,
    PrettyPrice,
    Price,
    PriceHistoryByMinutes,
    PricesSummaryByMinutes,
)
from kis.exceptions import KISBadArguments, KISNoData
from kis.utils.tool import as_datetime

from .client import DomesticResource

logger = logging.getLogger(__name__)


class DomesticQuote(DomesticResource, Quote):
    def fetch_current_price(
        self,
        symbol: str,
    ) -> Price:
        """
        국내주식시세/주식현재가 시세 조회

        ---

        주식 현재가 시세 API입니다. 실시간 시세를 원하신다면 웹소켓 API를 활용하세요.

        See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-quotations#L_07802512-4f49-4486-91b4-1050b6f5dc9d
        """
        headers = {"tr_id": "FHKST01010100", "custtype": "P"}
        params = {"fid_cond_mrkt_div_code": "J", "fid_input_iscd": symbol}

        res = self.client.fetch_data(
            "/uapi/domestic-stock/v1/quotations/inquire-price",
            headers=headers,
            params=params,
            data_class=Price,
            key_column="bstp_kor_isnm",
        )

        return res.data

    def _fetch_prices_by_minutes(self, symbol: str, to: Union[str, datetime, date]):
        """
        주식 당일 분봉 조회

        ---

        국내주식시세/주식당일분봉조회

        주식당일분봉조회 API입니다.
        실전계좌/모의계좌의 경우, 한 번의 호출에 최대 30건까지 확인 가능합니다.

        See https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-quotations#L_eddbb36a-1d55-461a-b242-3067ba1e5640
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
            "fid_pw_data_incu_yn": "Y",
        }

        return self.client.fetch_data(
            "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice",
            headers=headers,
            params=params,
            summary_class=PricesSummaryByMinutes,
            detail_class=List[Dict[str, Any]],
        )

    def fetch_prices_by_minutes(
        self, symbol: str, to: Optional[str] = None, count: Optional[int] = None
    ) -> Tuple[PricesSummaryByMinutes, List[PriceHistoryByMinutes]]:
        """
        주식 당일 분봉 연속 조회

        :param symbol: 종목코드
        :param to: 조회할 시간 (HHMMSS)
        :param count: 조회할 횟수(Optional)
        """
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

        summary: Optional[PricesSummaryByMinutes] = None
        full_histories: List[PriceHistoryByMinutes] = []

        while count > 0:
            result = self._fetch_prices_by_minutes(symbol, to)
            summary = result.summary
            histories = [
                PriceHistoryByMinutes(**history)
                for history in result.detail
                if history.get("stck_bsop_date")
            ]

            full_histories += histories

            # 30개 이하로 가져오면 break
            if len(histories) != 30:
                break

            # get last output
            to = (histories[-1].full_execution_time - timedelta(minutes=1)).strftime(
                "%H%M%S"
            )
            if to <= "090001":
                break
            count -= 1

        if summary is None:
            raise KISNoData("No 'FetchOHLCVSummary' data found. ")

        return summary, full_histories

    def _fetch_histories(
        self,
        symbol: str,
        start_date: Optional[Union[str, datetime, date]] = None,
        end_date: Optional[Union[str, datetime, date]] = None,
        standard: str = "D",
        adjust: bool = True,
    ):
        """
        국내 주식 기간별 조회 fetch one

        ---

        국내주식시세/국내주식기간별시세

        국내주식기간별시세(일/주/월/년) API입니다.
        실전계좌/모의계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능합니다.

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
        logger.debug(f" - start_date: {start_date}, end_date: {end_date}")

        headers = {"tr_id": "FHKST03010100", "custtype": "P"}
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
            "FID_INPUT_DATE_1": start_date,
            "FID_INPUT_DATE_2": end_date,
            "FID_PERIOD_DIV_CODE": standard,
            "FID_ORG_ADJ_PRC": "0" if adjust else "1",
        }

        return self.client.fetch_data(
            "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice",
            headers=headers,
            params=params,
            summary_class=FetchOHLCVSummary,
            detail_class=List[Dict[str, str]],
        )

    def fetch_histories(
        self,
        symbol: str,
        start_date: Optional[Union[str, datetime, date]] = None,
        end_date: Optional[Union[str, datetime, date]] = None,
        standard: str = "D",
        count: Optional[int] = None,
        adjust: bool = True,
    ) -> Tuple[FetchOHLCVSummary, List[FetchOHLCVHistory]]:
        """
        국내 주식 기간별 연속 조회

        :param symbol: 종목코드
        :param start_date: 조회 시작 날짜(Optional)
        :param end_date: 조회 종료 날짜(Optional)
        :param standard: 기간별 구분 (일: 'D', 주: 'W', 월: 'M', 년: 'Y')
        :param count: 조회할 횟수(Optional)
        :param adjust: 수정주가 여부
        """
        if count is None:
            count = 10
        logger.info(
            f"Fetch: symbol='{symbol}' standard='{standard}' BETWEEN '{start_date}' AND '{end_date}'"
        )

        summary: Optional[FetchOHLCVSummary] = None
        full_histories: List[FetchOHLCVHistory] = []
        while count > 0:
            result = self._fetch_histories(
                symbol,
                start_date=start_date,
                end_date=end_date,
                standard=standard,
                adjust=adjust,
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
            end_date = (last_history.business_date - timedelta(days=1)).strftime(
                "%Y%m%d"
            )
            count -= 1

        if summary is None:
            raise KISNoData("No 'FetchOHLCVSummary' data found. ")

        return summary, full_histories
