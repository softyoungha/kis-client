from datetime import datetime, timedelta

import streamlit as st

today = datetime.now().date()
month_ago = today - timedelta(days=30)


def render():
    symbol = st.text_input(
        "종목코드",
        value="",
        max_chars=6,
        key="overseas_symbol",
    )
    start_date = st.date_input(
        "조회 기간 시작 날짜",
        value=month_ago,
        key="overseas_start_date"
    )
    end_date = st.date_input(
        "조회 기간 종료 날짜",
        value=today,
        key="overseas_end_date"
    )
    st.write(symbol, start_date, end_date)
