#  Copyright (c) 2024. Christopher Queen Consulting LLC (http://www.ChristopherQueenConsulting.com/)

import streamlit as st
import tempfile
import os

st.set_page_config(page_title="Give Feedback", page_icon="🦜️🔗") # TODO: Change the page icon

st.markdown("""Here we will give feedback to student project submissions""")

def upload_instructions():
    uploaded_file = st.file_uploader("Upload Assignment Instructions", type=["txt", "docx", "pdf"])
    if uploaded_file is not None:
        st.success("File uploaded successfully.")
        # Create a temporary file to store the uploaded instructions
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.getvalue())
        temp_file.close()
        return temp_file.name

def upload_solution():
    uploaded_file = st.file_uploader("Upload Assignment Solution", type=["txt", "docx", "pdf", "java", "zip"])
    if uploaded_file is not None:
        st.success("File uploaded successfully.")
        # Create a temporary file to store the uploaded solution
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.getvalue())
        temp_file.close()
        return temp_file.name


def define_feedback_types():
    feedback_types = st.text_area("Define Feedback Types")
    if feedback_types:
        st.success("Feedback types defined.")


st.header("Upload Instructions")
instructions_file_path = upload_instructions()

st.header("Upload Solution")
solution_file_path = upload_solution()

st.header("Feedback Types")
define_feedback_types()

if instructions_file_path and solution_file_path:
    st.write("Both instructions file and solution file have been uploaded successfully.")
    # Perform other operations with the uploaded files
    # For example, you can pass the file paths to other functions or libraries
    # After processing, the temporary files will be automatically deleted

