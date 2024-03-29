#  Copyright (c) 2024. Christopher Queen Consulting LLC (http://www.ChristopherQueenConsulting.com/)
import os
import tempfile

import pandas as pd
import streamlit as st
from langchain_openai import ChatOpenAI

from cqc_cpcc.project_feedback import FeedbackType, get_feedback_guide
from cqc_cpcc.utilities.utils import read_file

def add_upload_file_element(uploader_text: str, accepted_file_types: list[str], success_message: bool = True):
    uploaded_file = st.file_uploader(uploader_text, type=accepted_file_types)
    if uploaded_file is not None:
        file_extension = os.path.splitext(uploaded_file.name)[1]
        if success_message:
            st.success("File uploaded successfully.")
        # Create a temporary file to store the uploaded instructions
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
        temp_file.write(uploaded_file.getvalue())
        #temp_file.close()
        return temp_file.name


def define_feedback_types():
    st.header("Define Feedback Types")

    # Preload the table with default rows and values
    default_data = [
        {"Name": "COMMENTS_MISSING", "Description": "The code does not include sufficient commenting throughout"},
        {"Name": "SYNTAX_ERROR", "Description": "There are syntax errors in the code"},
        {"Name": "SPELLING_ERROR", "Description": "There are spelling mistakes in the code"},
        {"Name": "OUTPUT_ALIGNMENT_ERROR",
         "Description": "There are output alignment issues in the code that will affect exam grades"},
        {"Name": "PROGRAMMING_STYLE",
         "Description": "There are programming style issues that do not adhere to java language standards"},
        {"Name": "ADDITIONAL_TIPS_PROVIDED", "Description": "Additional insights regarding the code and learning"},
    ]
    feedback_types_df = pd.DataFrame(default_data)

    # Allow users to edit the table
    edited_df = st.data_editor(feedback_types_df, key='feedback_types', hide_index=True,
                               num_rows="dynamic",
                               column_config={
                                   'Name': st.column_config.TextColumn('Name (required)',
                                                                       help='Uppercase and Underscores only',
                                                                       validate="^[A-Z_]+$", required=True),
                                   'Description': st.column_config.TextColumn('Description (required)', required=True)
                               }
                               )  # 👈 An editable dataframe

    return edited_df


@st.cache(allow_output_mutation=True, hash_funcs={ChatOpenAI: id})
def get_custom_llm(temperature: float, model: str) -> ChatOpenAI:
    """
    This function returns a cached instance of ChatOpenAI based on the temperature and model.
    If the temperature or model changes, a new instance will be created and cached.
    """
    return ChatOpenAI(temperature=temperature, model=model)


def main():

    st.set_page_config(page_title="Give Feedback", page_icon="🦜️🔗")  # TODO: Change the page icon

    st.markdown("""Here we will give feedback to student project submissions""")


    # Add elements to page to work with

     # Text input for entering a course name
    course_name = st.text_input("Enter Course Name")

    st.header("Instructions File")
    instructions_file_path = add_upload_file_element("Upload Assignment Instructions", ["txt", "docx", "pdf"])

    st.header("Solution File")
    solution_file_path = add_upload_file_element("Upload Assignment Solution", ["txt", "docx", "pdf", "java", "zip"])

    st.header("Feedback Types")
    feedback_types = define_feedback_types()
    feedback_types_list = []
    # Show success message if feedback types are defined
    if not feedback_types.empty:
        st.success("Feedback types defined.")
        # Convert DataFrame to list of FeedbackType objects
        for _, row in feedback_types.iterrows():
            name = row["Name"]
            description = row["Description"]
            feedback_types_list.append(FeedbackType(name, description))

    if st.button('Display Feedback Types List'):
        st.write("Feedback Types:", feedback_types_list)

    # Dropdown for selecting ChatGPT models
    default_option = "gpt-3.5-turbo-16k-0613"
    model_options = [default_option, "gpt-4-1106-preview"]
    selected_model = st.selectbox("Select ChatGPT Model", model_options, index=model_options.index(default_option))

    # Slider for selecting a value (ranged from 0.2 to 0.8, with step size 0.01)
    default_value = 0.2
    temperature = st.slider("Chat GPT Temperature", min_value=0.2, max_value=0.8, step=0.1, value=default_value,
                               format="%.2f")


    st.header("Student Submission File(s)")
    student_submission_file_path = add_upload_file_element("Upload Student Submission", ["txt", "docx", "pdf", "java", "zip"])
    # Checkbox for enabling Markdown wrapping
    wrap_code_in_markdown = st.checkbox("Student Submission Is Code", True)


    if instructions_file_path and solution_file_path and student_submission_file_path:
        st.write("All required file have been uploaded successfully.")
        # Perform other operations with the uploaded files
        # After processing, the temporary files will be automatically deleted

        student_file_name, student_file_extension = os.path.splitext(student_submission_file_path)
        base_student_filename = os.path.basename(student_submission_file_path)

        # TODO: Create the feedback item - Make this chattable so that the instructor can make changes

        print("Generating Feedback for: %s" % base_student_filename)

        if False: # TODO: Enable once you have proper API access to OpenAI
            # Create the custom llm
            custom_llm = get_custom_llm(temperature=temperature, model=selected_model)

            #st.write("Instruction File Path: %s" % instructions_file_path)
            assignment_instructions = read_file(instructions_file_path)
            assignment_solution = read_file(solution_file_path)
            student_submission = read_file(student_submission_file_path)

            feedback_guide = get_feedback_guide(assignment=assignment_instructions,
                                                solution=assignment_solution,
                                                student_submission=student_submission,
                                                course_name=course_name,
                                                wrap_code_in_markdown=wrap_code_in_markdown,
                                                custom_llm=custom_llm
                                                )

            # Output feedback to log and streamlit
            feedback = "\n".join([str(x) for x in feedback_guide.all_feedback])

            pre_feedback = "Good job submitting your assignment. "
            if len(feedback) > 0:
                pre_feedback = pre_feedback + "Here is my feedback:\n\n"
            else:
                pre_feedback = pre_feedback + "I find no issues with your submission. Keep up the good work!"
            post_feedback = "\n\n - " + st.session_state.instructor_signature
            print("\n\n" + pre_feedback + feedback + post_feedback)
        else:
            pre_feedback = "Good job submitting your assignment. "
            # Loop through each feedback type and reply some giberrish
            feedback = ""
            for ft in feedback_types_list:
                feedback += "Details: "+str(ft.value)
            post_feedback = "\n\n - " + st.session_state.instructor_signature

        # Display text output TODO: Look into other format options. Markdown is allowed
        st.text(pre_feedback + feedback + post_feedback)


if __name__ == '__main__':
    main()
