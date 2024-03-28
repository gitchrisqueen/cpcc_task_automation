#  Copyright (c) 2024. Christopher Queen Consulting LLC (http://www.ChristopherQueenConsulting.com/)

import streamlit as st
from cqc_cpcc.utilities.utils import read_file



st.set_page_config(page_title="Take Attendance", page_icon="🦜️🔗") # TODO: Change the page icon

st.header("CPCC Task Automation - Take Attendance")

st.markdown("""Here we will take attandance for you and provide log of what we have for each of our courses for each date""")