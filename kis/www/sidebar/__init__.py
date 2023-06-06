import streamlit as st
from .login import render_login_form
from .logout import render_logout_form


def sidebar(pages: dict):
    with st.sidebar:
        # title
        st.title("💋KIS manager")

        # description
        st.write("한국투자증권 Open API를 이용한 주식 매매 프로그램입니다.")

        # select pages
        with st.container():
            selected_page = st.selectbox("메뉴", pages.keys())

        # divider
        st.divider()

        # credentials container
        with st.container():

            st.header("Credentials")

            is_client_exists = st.session_state.get("client", None) is not None

            if is_client_exists:
                render_logout_form()
            else:
                render_login_form()

    return selected_page


