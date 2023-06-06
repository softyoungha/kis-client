from datetime import datetime, timedelta
from typing import Optional, List
import altair as alt

import pandas as pd
import streamlit as st

from kis import DomesticClient
from kis.core import MasterBook
from kis.core.domestic.schema import PriceCustom, FetchOHLCVSummary, FetchOHLCVHistory
from kis.utils.tool import is_korea_market_open

today = datetime.now().date()
month_ago = today - timedelta(days=30)
year_ago = today - timedelta(days=365)


def handle_submit():
    # clear and get new data
    get_data.clear()
    get_data(True)


@st.cache_data
def get_data(error_log: bool = False):
    try:
        client = st.session_state.get("client")
        if not client:
            raise ValueError("로그인이 필요합니다.")

        symbol = st.session_state.domestic_selected_symbol
        if not symbol:
            raise ValueError("종목코드를 입력해주세요.")
        start_date, end_date, standard = (
            st.session_state.domestic_start_date,
            st.session_state.domestic_end_date,
            st.session_state.domestic_standard
        )
        client: DomesticClient = st.session_state.get("client")
        try:
            summary, histories = client.quote.fetch_histories(
                symbol,
                start_date,
                end_date,
                standard=standard,
            )
        except Exception as err:
            raise err

        df = pd.DataFrame([row.dict() for row in histories])
        return summary, df
    except Exception as err:
        if error_log:
            if isinstance(err, ValueError):
                st.warning(err)
            else:
                st.error(err)
        return None, None


@st.cache_data
def fetch_master():
    kospi_master = MasterBook.get("KOSPI", with_detail=True)
    kosdaq_master = MasterBook.get("KOSDAQ", with_detail=True)
    return pd.concat([kospi_master, kosdaq_master], axis=0)


def format_standard(x):
    if x == "D":
        return "일"
    elif x == "W":
        return "주"
    elif x == "M":
        return "월"
    elif x == "Y":
        return "년"
    raise ValueError(f"Unknown standard: {x}")


def render():
    # load & define
    is_market_open = is_korea_market_open()

    summary, df_histories = get_data()
    print(summary, df_histories)

    summary: Optional[FetchOHLCVSummary]
    df_histories: Optional[pd.DataFrame]

    # layout
    col_left, col_right = st.columns([1, 4], gap="medium")
    with col_left:
        st.subheader("Select")

        with st.form("view-domestic"):
            st.text_input(
                "종목코드",
                value="",
                max_chars=10,
                key="domestic_selected_symbol",
            )

            st.radio(
                "기준",
                options=("D", "W", "M", "Y"),
                key="domestic_standard",
                format_func=format_standard
            )

            st.date_input(
                "조회 기간 시작 날짜",
                value=year_ago,
                key="domestic_start_date",
            )
            st.date_input(
                "조회 기간 종료 날짜",
                value=today,
                key="domestic_end_date",
            )

            st.form_submit_button(
                "조회",
                on_click=handle_submit,
                type="primary",
                use_container_width=True,
            )

    with col_right:
        if summary:
            st.subheader("Summary")

            # row 1
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(f"종목: {summary.symbol}", value=summary.symbol_name)
            col2.metric("시가총액", value=summary.market_cap)
            col3.metric("부호", value=summary.diff_sign.value)
            col4.metric(
                "누적 거래량",
                value=summary.accumulated_volume,
                delta=summary.diff_volume,
                help="전일대비"
            )

            # row 2
            col1, col2, col3, col4 = st.columns(4)
            if is_market_open:
                delta_help = "시가 대비"
                delta = summary.price_current - summary.price_open
            else:
                delta_help = "전일 대비"
                delta = summary.price_current - summary.price_base
            col1.metric(
                "현재가",
                value=summary.price_current,
                delta=delta,
                help=delta_help
            )
            col2.metric("EPS", value=int(summary.eps))
            col3.metric("PBR", value=summary.pbr)
            col4.metric("PER", value=summary.per)

        if df_histories is not None:
            st.divider()
            st.subheader("History")

            standard = st.session_state.get("domestic_standard")

            if standard == "D":
                time_unit = "yearmonthdate"
            elif standard == "W":
                time_unit = "yearmonthdate"
            elif standard == "M":
                time_unit = "yearmonth"
            elif standard == "Y":
                time_unit = "year"
                
            # x
            x = alt.X(
                "business_date:N",
                title="영업일",
                axis=alt.Axis(),
                scale=alt.Scale(),
                timeUnit=time_unit,
            )
            
            # y: min max scaling
            y_min, y_max = df_histories["close"].min(), df_histories["close"].max()
            y_diff = y_max - y_min
            y_scale = alt.Scale(domain=(y_min - y_diff * 0.05, y_max + y_diff * 0.05))
            y = alt.Y(
                "close:Q",
                title="종가",
                axis=alt.Axis(),
                scale=y_scale,
            )

            # line
            chart = (
                alt.Chart(df_histories)
                .encode(x=x, y=y)
                .mark_line()
            )

            # area
            if standard != "Y":
                chart += (
                    alt.Chart(df_histories)
                    .encode(
                        x=x,
                        y=alt.Y("low:Q"),
                        y2=alt.Y2("high:Q"),
                    )
                    .mark_area(opacity=0.3)
                )

            # add point
            chart += (
                alt.Chart(df_histories)
                .encode(x=x, y=y)
                .mark_point(size=50, color="black", fill="white")
                .add_selection(
                    alt.selection_single(
                        on="mouseover",
                        nearest=True,
                        empty="none",
                        fields=["business_date"],
                    )
                )
            )

            chart.interactive()

            # draw
            st.altair_chart(chart, use_container_width=True)


            import backtrader as bt

            from kis.utils.tool import as_datetime

            # Create a subclass of Strategy to define the indicators and logic

            class SmaCross(bt.Strategy):
                # list of parameters which are configurable for the strategy
                params = dict(
                    pfast=10,  # period for the fast moving average
                    pslow=30  # period for the slow moving average
                )

                def __init__(self):
                    sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
                    sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
                    self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

                def next(self):
                    if not self.position:  # not in the market
                        if self.crossover > 0:  # if fast crosses slow to the upside
                            self.buy()  # enter long

                    elif self.crossover < 0:  # in the market & cross to the downside
                        self.close()  # close long position

            cerebro = bt.Cerebro()

            cerebro.broker.setcash(100000)  # 자산을 10만원으로 초기화

            cerebro.addstrategy(SmaCross)
            df = df_histories.copy()
            df["business_date"] = pd.to_datetime(df["business_date"].apply(lambda x: as_datetime(x)))
            df.set_index("business_date", inplace=True)
            df = df[["open", "high", "low", "close", "volume"]]
            print(df.head())

            print(df.isna().sum())
            print(df.dropna())

            data0 = bt.feeds.PandasData(
                dataname=df,
                openinterest=None,
            )
            cerebro.adddata(data0)


            print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())  # 시작 시 자산

            cerebro.run()

            print('Final Portfollio Value: %.2f' % cerebro.broker.getvalue())  # 종료 시 자산

            cerebro.plot()

