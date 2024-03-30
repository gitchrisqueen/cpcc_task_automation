#  Copyright (c) 2024. Christopher Queen Consulting LLC (http://www.ChristopherQueenConsulting.com/)

import streamlit as st

from cqc_streamlit_app.utils import get_cpcc_css


def main():
    # TODO: Initialize other session state variables - the ones you need in .env

    st.set_page_config(page_title="CPCC Grade Exams", page_icon="🦜️🔗")  # TODO: Change the page icon

    css = get_cpcc_css()
    st.markdown(
        css,
        unsafe_allow_html=True
    )

    st.markdown(
        """Here we will grade exams""")


if __name__ == '__main__':
    main()
