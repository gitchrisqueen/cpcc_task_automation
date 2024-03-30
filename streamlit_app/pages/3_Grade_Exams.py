#  Copyright (c) 2024. Christopher Queen Consulting LLC (http://www.ChristopherQueenConsulting.com/)

import streamlit as st

from streamlit_app.Home import add_cpcc_theming


def main():
    # TODO: Initialize other session state variables - the ones you need in .env

    st.set_page_config(page_title="CPCC Grade Exams", page_icon="🦜️🔗")  # TODO: Change the page icon

    add_cpcc_theming()

    st.markdown(
        """Here we will grade exams""")


if __name__ == '__main__':
    main()