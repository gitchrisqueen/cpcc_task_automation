#  Copyright (c) 2024. Christopher Queen Consulting LLC (http://www.ChristopherQueenConsulting.com/)

import streamlit as st

# Streamlit app
st.subheader('Settings')

# Get API keys
openai_api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type="password")
st.caption("*Required for all apps; get it [here](https://platform.openai.com/account/api-keys).*")

# Get CPCC variables
instructor_user_id = st.text_input("Instructor User ID", value=st.session_state.instructor_user_id)
st.caption("*Required for all apps")
instructor_password = st.text_input("Instructor Password", value=st.session_state.instructor_password, type="password")
st.caption("*Required for all apps")

# instructor_signature = st.text_input("Instructor Signature", value="Your Instructor" if st.session_state.instructor_signature is None else st.session_state.instructor_signature)
instructor_signature = st.text_input("Instructor Signature",
                                     value=st.session_state.get("instructor_signature", "Your Instructor"))

required_vars = [openai_api_key, instructor_user_id, instructor_password, instructor_signature]

# If the 'Save' button is clicked
if st.button("Save"):
    if any(not var.strip() for var in required_vars):
        st.error("Please provide the missing API keys.")
    else:
        st.session_state.openai_api_key = openai_api_key
        st.session_state.instructor_user_id = instructor_user_id
        st.session_state.instructor_password = instructor_password
        st.session_state.instructor_signature = instructor_signature
