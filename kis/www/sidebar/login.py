import streamlit as st

from kis.core import DomesticClient
from kis.exceptions import KISBadArguments
from kis.constants import KIS_ACCOUNT, KIS_APP_KEY, KIS_APP_SECRET


def handle_login():
    is_dev = st.session_state.get("is_dev")
    app_key = st.session_state.get("app_key")
    app_secret = st.session_state.get("app_secret")
    account = st.session_state.get("account")

    if not app_key:
        st.error("app_key를 입력해주세요.")
        return

    if not app_secret:
        st.error("app_secret를 입력해주세요.")
        return

    if not account:
        st.error("account를 입력해주세요.")
        return

    try:
        client = DomesticClient(
            is_dev=is_dev,
            app_key=app_key,
            app_secret=app_secret,
            account=account,
            load_token=False
        )
        client.session.create_token()
    except KISBadArguments as e:
        st.error(f"로그인 실패: {str(e)}")
        return

    # new client!
    st.session_state["client"] = client

    st.success("로그인 성공!")


def render_login_form():
    with st.form("login_form"):
        st.text_input(
            "증권계좌번호",
            key="account",
            value=KIS_ACCOUNT,
            placeholder="예: 12345678-01",
            autocomplete="account",
        )

        # app_key
        st.text_input(
            "app_key",
            type="password",
            key="app_key",
            value=KIS_APP_KEY,
            help="KIS Developers로부터 받은 app key",
            max_chars=36,
            autocomplete="app_key",
        )

        # secret_key
        st.text_input(
            "app_secret",
            type="password",
            key="app_secret",
            value=KIS_APP_SECRET,
            help="KIS Developers로부터 받은 app secret",
            max_chars=180,
            autocomplete="app_secret",
        )

        # 모의투자
        st.checkbox(
            "모의투자",
            value=True,
            key="is_dev",
        )

        # login button
        st.form_submit_button(
            "로그인",
            on_click=handle_login,
            type="primary",
            use_container_width=True,
        )
