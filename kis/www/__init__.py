import streamlit as st
import sys
import os

sys.path.append(os.getcwd())

from kis.www.sidebar import sidebar
from kis.www.home import home
from kis.www.quote import quote
from kis.www.order import order
from kis.www.balance import balance


def create_app():
    st.set_page_config(
        page_icon="💋",
        page_title="KIS manager",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    pages = {
        "Home": home,
        "📈 주가조회": quote,
        "🙋‍♂️ 주문": order,
        "🤦‍♂️ 잔고조회": balance,
    }

    selected_page = sidebar(pages)

    pages[selected_page]()


if __name__ == "__main__":
    create_app()
