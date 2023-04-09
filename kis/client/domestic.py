from dataclasses import dataclass, field
from dateutil.parser import parse
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from kis.base import KisClientBase, fetch, order
from .schema.domestic import *
from kis.exceptions import KISBadArguments


NAMED_SYMBOLS = {
    "삼성전자": "005930"
}


# @dataclass
class KisDomesticClient(KisClientBase):

    @fetch(
        "/uapi/domestic-stock/v1/quotations/inquire-price",
        data_class=FetchPrice
    )
    def fetch_current_price(self, symbol: str):
        """주식현재가시세"""
        headers = {"tr_id": "FHKST01010100"}
        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": symbol
        }
        return headers, params

    @fetch(
        "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice",
        summary_class=FetchPricesByMinutesSummary,
        detail_class=List[FetchPriceByMinutesHistory]
    )
    def fetch_prices_by_minutes(self, symbol: str, to: str):
        """
        국내주식시세/주식당일분봉조회
        최대 30개씩 출력
        """
        try:
            datetime.strptime(to, "%H%M%S")
        except ValueError as err:
            raise KISBadArguments() from err

        headers = {"tr_id": "FHKST03010200"}
        params = {
            "fid_etc_cls_code": "",
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": symbol,
            "fid_input_hour_1": to,  # HH:MM:SS
            "fid_pw_data_incu_yn": "Y"
        }
        return headers, params

    def fetch_all_prices_by_minutes(
            self,
            symbol: str,
            to: Optional[str] = None,
            count: Optional[int] = None
    ) -> Tuple[FetchPricesByMinutesSummary, List[FetchPriceByMinutesHistory]]:
        now = datetime.now()
        if not to:
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

        full_histories = []

        while count > 0:
            result = self.fetch_prices_by_minutes(symbol, to)
            summary, histories = result.summary, result.detail
            full_histories += histories

            # get last output
            to = (histories[-1].datetime - timedelta(minutes=1)).strftime("%H%M%S")
            if to <= "090001":
                break
            count -= 1

        return summary, full_histories

    @fetch("/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice")
    def fetch_ohlcv(
            self,
            symbol: str,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            standard: str = "D",
            adjust: bool = True
    ):
        """
        국내주식시세/국내주식기간별시세
        100개씩 리턴
        """
        start_date = parse(start_date).strftime("%Y%m%d") if start_date else "19800104"
        end_date = (
            parse(end_date) if end_date else datetime.now()
        ).strftime("%Y%m%d")

        headers = {"tr_id": "FHKST03010100"}
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
            "FID_INPUT_DATE_1": start_date,
            "FID_INPUT_DATE_2": end_date,
            "FID_PERIOD_DIV_CODE": standard,
            "FID_ORG_ADJ_PRC": 0 if adjust else 1
        }
        return headers, params

    def fetch_all_ohlcv(
            self,
            symbol: str,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            standard: str = "D",
            count: Optional[int] = None
    ):
        if count is None:
            count = 10

        full_histories = []

        while count > 0:
            result: dict = self.fetch_ohlcv(
                symbol,
                start_date=start_date,
                end_date=end_date,
                standard=standard
            )
            summary, histories = result["output1"], result["output2"]
            full_histories += histories

            # break
            need_break = False
            for history in histories:
                if not history:
                    need_break = True
                    break
            if need_break:
                break

            # get last output
            last_history = histories[-1]
            last_date = last_history["stck_bsop_date"]
            end_date = (datetime.strptime(last_date, "%Y%m%d") - timedelta(days=1)).strftime("%Y%m%d")
            count -= 1

        return {
            "summary": summary,
            "histories": full_histories
        }








