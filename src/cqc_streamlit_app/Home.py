#  Copyright (c) 2024. Christopher Queen Consulting LLC (http://www.ChristopherQueenConsulting.com/)
import os

import streamlit as st

from cqc_cpcc.utilities.utils import read_file
from cqc_streamlit_app.utils import get_cpcc_css

# Initialize session state variables
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ""

if 'instructor_user_id' not in st.session_state:
    st.session_state.instructor_user_id = ""

if 'instructor_password' not in st.session_state:
    st.session_state.instructor_password = ""

if 'instructor_signature' not in st.session_state:
    st.session_state.instructor_signature = "Your Instructor"


def main():

    # TODO: Initialize other session state variables - the ones you need in .env

    st.set_page_config(page_title="CPCC Task Automation", page_icon="🦜️🔗")  # TODO: Change the page icon

    css = get_cpcc_css()
    st.markdown(
        css,
        unsafe_allow_html=True
    )

    st.header("Welcome to CPCC Task Automation! 👋")

    # Get the ReadMe Markdown and display it
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_markdown = read_file(parent_directory + "/README.md")

    st.markdown(readme_markdown)


if __name__ == '__main__':
    main()
