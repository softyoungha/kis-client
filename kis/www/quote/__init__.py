from typing import TYPE_CHECKING

import streamlit as st
from kis.www.quote.domestic import render as render_domestic_tab
from kis.www.quote.overseas import render as render_overseas_tab
from kis.utils.tool import is_korea_market_open, is_us_market_hours


if TYPE_CHECKING:
    pass


def quote():

    title, _,  desc = st.columns([2, 8, 2])

    with title:
        st.header("📈 시세 조회")

    with desc:
        if is_korea_market_open():
            text = "- 국내 시장: 🌞 Open!"
        else:
            text = "- 국내 시장: 🌛 Closed"

        if is_us_market_hours():
            text += "\n- 해외 시장: 🌞 Open!"
        else:
            text += "\n- 해외 시장: 🌛 Closed"
        st.markdown(text)

    domestic_tab, overseas_tab = st.tabs(["국내", "해외"])

    with domestic_tab:
        render_domestic_tab()

    with overseas_tab:
        render_overseas_tab()
