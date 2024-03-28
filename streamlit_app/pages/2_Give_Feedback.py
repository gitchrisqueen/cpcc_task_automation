#  Copyright (c) 2024. Christopher Queen Consulting LLC (http://www.ChristopherQueenConsulting.com/)

import streamlit as st
import tempfile
import pandas as pd
import os

from cqc_cpcc.project_feedback import FeedbackType

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
    st.header("Define Feedback Types")

    # Pre-load the table with default rows and values
    default_data = [
        {"Name": "COMMENTS_MISSING", "Description": "The code does not include sufficient commenting throughout"},
        {"Name": "SYNTAX_ERROR", "Description": "There are syntax errors in the code"},
        {"Name": "SPELLING_ERROR", "Description": "There are spelling mistakes in the code"},
        {"Name": "OUTPUT_ALIGNMENT_ERROR", "Description": "There are output alignment issues in the code that will affect exam grades"},
        {"Name": "PROGRAMMING_STYLE", "Description": "There are programming style issues that do not adhere to java language standards"},
        {"Name": "ADDITIONAL_TIPS_PROVIDED", "Description": "Additional insights regarding the code and learning"},
    ]
    feedback_types_df = pd.DataFrame(default_data)

    # Allow users to edit the table
    feedback_types_df = st.dataframe(feedback_types_df)

    # Add a new row button
    if st.button("Add Feedback Type"):
        feedback_types_df = feedback_types_df.append({"Name": "", "Description": ""}, ignore_index=True)

    # Allow users to delete rows
    rows_to_delete = st.multiselect("Select Rows to Delete", feedback_types_df.index.tolist())
    if len(rows_to_delete) > 0:
        feedback_types_df = feedback_types_df.drop(index=rows_to_delete)

    # Convert DataFrame to list of FeedbackType objects
    feedback_types_list = []
    for _, row in feedback_types_df.iterrows():
        name = row["Name"]
        description = row["Description"]
        feedback_types_list.append(FeedbackType(name, description))

    # Show success message if feedback types are defined
    if feedback_types_list:
        st.success("Feedback types defined.")

    return feedback_types_list

st.header("Instructions File")
instructions_file_path = upload_instructions()

st.header("Solution File")
solution_file_path = upload_solution()

st.header("Feedback Types")
feedback_types_list = define_feedback_types()
if feedback_types_list:
    st.write("Feedback Types:", feedback_types_list)

if instructions_file_path and solution_file_path:
    st.write("Both instructions file and solution file have been uploaded successfully.")
    # Perform other operations with the uploaded files
    # For example, you can pass the file paths to other functions or libraries
    # After processing, the temporary files will be automatically deleted

