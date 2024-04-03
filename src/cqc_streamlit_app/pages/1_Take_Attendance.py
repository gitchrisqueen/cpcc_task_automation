#  Copyright (c) 2024. Christopher Queen Consulting LLC (http://www.ChristopherQueenConsulting.com/)

import streamlit as st

from cqc_streamlit_app.initi_pages import init_session_state
from cqc_streamlit_app.utils import get_cpcc_css

# Initialize session state variables
init_session_state()

def main():
    # TODO: Initialize other session state variables - the ones you need in .env

    st.set_page_config(page_title="CPCC Take Attendance", page_icon="🦜️🔗")  # TODO: Change the page icon

    css = get_cpcc_css()
    st.markdown(
        css,
        unsafe_allow_html=True
    )

    st.markdown(
        """Here we will take attandance for you and provide log of what we have for each of our courses for each date""")


if __name__ == '__main__':
    main()
