import streamlit as st


def handle_logout():
    # remove client
    st.session_state["client"] = None


def render_logout_form():
    with st.form("logout_form"):
        # client: DomesticClient = st.session_state["client"]
        account = st.session_state["client"].account
        st.write(f"증권계좌번호: '{account}' login")

        st.form_submit_button(
            "로그아웃",
            on_click=handle_logout,
            type="secondary",
            use_container_width=True,
        )
