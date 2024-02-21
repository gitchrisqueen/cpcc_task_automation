import os
from datetime import datetime
from typing import Type

import openai
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import PydanticOutputParser
from langchain_community.agent_toolkits.base import BaseToolkit
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool, ToolException
from langchain_core.utils.function_calling import convert_to_openai_tool

from cqc_cpcc.exam_review import *
from cqc_cpcc.utilities.utils import read_file

EXAM_INSTRUCTIONS = """Program Description
   An acting coach charges new clients for acting instruction services based on duration of sessions in hours. The coach charges an hourly rate of $55.25 per hour for Child Acting Sessions and $88.35 per hour for Adult Acting Sessions. Write a program that determines a bill for booking an acting coach session. The program must:
   \t1.	Ask the user to enter the type of session (child or adult) service to determine the hourly rate of the session.
   \t\t* If an invalid session type is entered, the rate for an adult acting session will be applied. 
   \t2.	Ask the user to enter the number of minutes of the duration of the session. This acting coach requires users to book a minimum of 50 minutes for a session. The maximum time that can be booked for a session is 180 minutes.
   \t\t* If an invalid number of minutes is entered, a standard session length of 55 minutes will be booked automatically.
   \t3.	The program must calculate the duration of the session in hours. This acting coach charges 1 hour for every 50 minutes of duration of a session.
   \t4.	This acting coach is also offering a special 15% promotional discount when users enter the following discount code: ACT151TCA. Ask the user to enter the discount code.
   \t\t* If an invalid discount code is entered, no discount will be applied.
   \t5.	The program must calculate the charge for the acting coach session. The amount due is the product of the total hours of the session and the hourly rate for a session depending on the type of acting session. Apply the discount code as necessary to the charge.
   \t6.	The program must display the type of session, the duration of the session in hours, the hourly rate for the session, the subtotal (session charge before discount), the discounted amount (if applicable), and the final amount due for the session.
   """

# NOTE: Make sure to use r""" to indicate raw string
EXAM_SOLUTION = r"""import java.util.*;

public class Exam1_SPR24B
{
   // main method - aka the 'brain' method
   public static void main(String[] args)
   {
       Scanner input = new Scanner(System.in);
       double minutes, hours;
       final double CHILDHOURLY = 55.25, ADULTHOURLY = 88.35;
       double rate, serviceCharges, discount;
       char serviceType;
       String discountCode = "";

       System.out.println("\nBook a session with an Acting Coach now!");

       System.out.println("Choose from one of the following types of voice instruction services: ");
       System.out.println("\t C - Child Acting Session");
       System.out.println("\t A - Adult Acting Session");
       System.out.print("Enter your choice (C or A): ");
       serviceType = input.next().charAt(0);

       // clear the buffer
       input.nextLine();

       // set the rate
       if(serviceType == 'C')
       {
         System.out.printf("\nChild Acting Session rate: $%.2f per hour \n", CHILDHOURLY);
         rate = CHILDHOURLY;
       }
       else if(serviceType == 'A')
       {
         System.out.printf("\nAdult Acting Session rate: $%.2f per hour \n", ADULTHOURLY);
         rate = ADULTHOURLY;
       }
       else
       {
         System.out.println("\nInvalid choice. Adult Acting Session rate applied.");
         System.out.printf("\nAdult Acting Session rate: $%.2f per hour \n", ADULTHOURLY);
         rate = ADULTHOURLY;
       }

       System.out.print("\nEnter the total minutes of for the Acting Session (min: 50 - max: 180): ");
       minutes = input.nextInt();

       if(minutes < 50 || minutes > 180)
       {
         System.out.println("\nInvalid entry. 55 Minute Acting Session Booked.");
         minutes = 55;
       }

       // calculate the hours
       hours = minutes / 50.0;

       // calculate the charges for the session
       serviceCharges = hours * rate;

       // clear the buffer
       input.nextLine();

       System.out.print("\nThere is a promotional discount available! Enter the discount code: ");
       discountCode = input.nextLine();

       if(discountCode.equals("ACT151TCA"))
       {
         System.out.println("\n15% Discount Applied!");
         discount = serviceCharges * 0.15;
       }
       else
       {
         System.out.println("\nInvalid code. No discount applied!");
         discount = 0.00;
       }

       System.out.println("\n-------------------------------------------------------------");
       System.out.println("Acting Coach Session Info");
       if(serviceType == 'C')
         System.out.println("Session Type: \t\t\tChild Acting");
       else
         System.out.println("Session Type: \t\t\tAdult Acting");
       System.out.printf("Session Duration: \t%.2f hours \n", hours);
       System.out.printf("Session Rate: \t\t\t$%.2f per hour \n", rate);
       System.out.printf("Session Charge: \t\t$%.2f \n", serviceCharges);
       System.out.printf("Discount: \t\t\t\t$%.2f \n", discount);
       System.out.printf("Amount Due: \t\t\t$%.2f \n", serviceCharges - discount);
       System.out.println("-------------------------------------------------------------");
   }   
}
"""

# NOTE: Make sure to use r""" to indicate raw string
STUDENT_SUBMISSION = r"""import java.util.Scanner;

public class Exam1Harris{

   public static void main(String[] args){
      
   Scanner scanner = new Scanner(System.in);
   
   // Ask user to enter type of session. 
   System.out.println("Hello!");
   System.out.println("What type of service will you be using? \n1. Child \n2. Adult \nPlease enter either the corresponding number from the selection above.");
   int userInputService = scanner.nextInt();
   
   // Convert user selection into hourly rate.
   double hourlyRate = 0.0;
   double minuteRate = 0.0;
   String serviceType = ""; 
   if (userInputService == 1){
      serviceType = "Child";
      hourlyRate = 55.25;
      minuteRate = (hourlyRate / 50);
   } else if (userInputService == 2){
      serviceType = "Adult";
      hourlyRate = 88.35;
      minuteRate = (hourlyRate / 50);
   } else {
      serviceType = "Adult";
      hourlyRate = 88.35;
      minuteRate = (hourlyRate / 50);
   }
   
   // Ask user to enter duration of session in minutes.
   System.out.println("Sessions must be booked a minimum of 50 minutes. Sessions can be no longer than 180 minutes. \nPlease enter the duration (in minutes) of your session.: ");
   int userInputMinutes = scanner.nextInt();
   
   // Calculate duration of session into hours. (1 hour = 50 minutes).
   int sessionHours = 0;
   int sessionMinutes = 0;
   if (userInputMinutes >= 50 && userInputMinutes <= 180){
      sessionHours = (userInputMinutes / 50);
      sessionMinutes = (userInputMinutes % 50);
   } else {
      sessionHours = 1;
      sessionMinutes = 5;
   }
   
   // Calculate total charge for session.
   double subtotal = ((sessionHours * hourlyRate) + (sessionMinutes * minuteRate));

   
   // Ask user to input promotional discount ACT151TCA.
   scanner.nextLine();
   final String discountCode = "ACT151TCA";
   System.out.println("Please enter any promotional discount codes: ");
   String userInputDiscount = scanner.nextLine();
   
   // Calculate discount.
   double discountAmount = 0.0;
   if (userInputDiscount.equals(discountCode)){
      discountAmount = (subtotal * 0.15);
   } else {
      discountAmount = 0.0;
   }
         
   // Amount due.
   double totalDue = (subtotal - discountAmount);
   
   // Output receipt. Include type of session, duration of session in hours, hourly rate, subtotal, discounted amount, and amount due.
   System.out.println("Please review your receipt.");
   System.out.println("Type of service: " + serviceType + ".");
   
   if (sessionMinutes > 0){
      System.out.println("Session duration: " + sessionHours + " hour(s) and " + sessionMinutes + " minute(s).");
   } else if (sessionMinutes == 0){
      System.out.println("Session duration: " + sessionHours + " hour(s).");
   }
   
   System.out.println("Hourly rate of service: $" + hourlyRate + ".");
   System.out.printf("Subtotal: $%.2f." , subtotal);
   System.out.printf("\nDiscounted amount: $%.2f", discountAmount);
   System.out.printf("\nAmount due: $%.2f" , totalDue);
   System.out.println("\n \nThank you for using this program.");
      
   }

}

"""


def get_test_definitions() -> ErrorDefinitions:
    return ErrorDefinitions(
        all_minor_errors=[
            MinorError(
                error_type=MinorErrorType.NAMING_CONVENTION,
                line_numbers_of_error=[113],
                error_details="Use lower camel_case when creating variables"),
            MinorError(
                error_type=MinorErrorType.NAMING_CONVENTION,
                line_numbers_of_error=[200, 113, 414],
                error_details="Use lower camel_case when creating variables"),
            MinorError(
                error_type=MinorErrorType.NAMING_CONVENTION,
                line_numbers_of_error=[311, 414],
                error_details="Use lower camel_case when creating variables"),
            MinorError(
                error_type=MinorErrorType.CONSTANTS_ERROR,
                line_numbers_of_error=[20],
                error_details="You did not use any constants as expected")
        ]
        ,
        all_major_errors=[
            MajorError(
                error_type=MajorErrorType.INSUFFICIENT_DOCUMENTATION,
                line_numbers_of_error=[90],
                error_details="You did not put any comments in your code")
        ]

    )


def test_code_loader():
    from langchain.text_splitter import Language
    from langchain_community.document_loaders.generic import GenericLoader
    from langchain_community.document_loaders.parsers import LanguageParser

    repo_path = "//downloads/exam1"

    # Load
    java_docs_loader = GenericLoader.from_filesystem(
        repo_path,
        glob="**/*",
        suffixes=[".java"],
        exclude=["**/non-utf8-encoding.java"],
        parser=LanguageParser(language=None, parser_threshold=500),

    )
    java_documents = java_docs_loader.load()
    print("Java Document Length: %s" % len(java_documents))

    text_loader = GenericLoader.from_filesystem(
        repo_path,
        glob="**/*",
        suffixes=[".txt"],
        exclude=["**/non-utf8-encoding.txt"],
        parser=LanguageParser(language=None, parser_threshold=500),

    )
    text_documents = text_loader.load()
    print("Text Document Length: %s" % len(text_documents))

    from langchain.text_splitter import RecursiveCharacterTextSplitter

    java_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.JAVA, chunk_size=2000, chunk_overlap=200
    )
    java_texts = java_splitter.split_documents(java_documents)
    print("Java text Length: %s" % len(java_texts))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    text_texts = text_splitter.split_documents(text_documents)
    print("Text Texts Length: %s" % len(java_texts))

    from langchain_community.vectorstores import Chroma
    from langchain_openai import OpenAIEmbeddings

    db = Chroma.from_documents(java_texts + text_texts, OpenAIEmbeddings(disallowed_special=()))
    retriever = db.as_retriever(
        search_type="mmr",  # Also test "similarity"
        search_kwargs={"k": 8},
    )

    from langchain.chains import ConversationalRetrievalChain
    from langchain.memory import ConversationSummaryMemory
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model_name="gpt-4")
    memory = ConversationSummaryMemory(
        llm=llm, memory_key="chat_history", return_messages=True
    )
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

    questions = [
        # "How many comments are in the users code?",
        # "How are the session minutes calculated? ",
        # "What is the discount amount when a proper discount code is provided?",
        # "Tell me an improvement that could be made to the code and what line number where you would make it"
        # "How mand lines are in the code?",
        # "What line does the class definition start on?",
        # "What line does the first method start on?",
        # "What line number is the total due calculated on?",
        # "How many total lines are there in the file?",
        # "What would the output be from the code be if the user entered '1', '2', then 'ACT151TCA' when prompted in the terminal while running the code?"
        """
        You are a Java 151 professor grading a student's exam submission.
        Consider the file Exam1_Instructions.txt as "Exam Instructions".
        Consider the file Exam1_Solution.java as "Example Solutions".
        Consider the file Exam1Harris.java as "Student Submission".
        Using the Exam Instructions and Example Solution as your grading guide, analyze the Student Submission to identify all errors.
        The maximum exam points are 200.
        Subtract 40 points for all major errors.
        Subtract 10 points for all minor errors.
        Output the error descriptions and the total points awarded.
        
        """

    ]

    for question in questions:
        result = qa(question)
        print(f"-> **Question**: {question} \n")
        print(f"**Answer**: {result['answer']} \n")


def test_upgraded_prompt_style():
    exam_instructions_file = ""
    exam_solution_file = ""
    submission_file = ""
    major_error_types_list = ""
    minor_error_types_list = ""

    # Chain of prompts
    prompts = [
        f'Retrieve the content from the exam instructions file: {exam_instructions_file}',
        f'Retrieve the content from the example solution file: {exam_solution_file}',
        f'Retrieve the content from the student submission file: {submission_file}',
        f'Retrieve the major error types as a string list from the Enum class: {major_error_types_list}',
        f'Retrieve the minor error types as a string list from the Enum class: {minor_error_types_list}',
        "Analyze the student submission based on the given exam instructions and example solution.",
        "Identify and list all major errors in the student submission with detailed descriptions and corresponding line numbers.",
        "Identify and list all minor errors in the student submission with detailed descriptions and corresponding line numbers.",
        "Evaluate the comments-to-code ratio in the student submission and check if it meets the 10% or higher requirement.",
        "Provide a constructive and friendly tone in describing each error, adhering to the provided Major Error Types and Minor Error Types.",
        "Follow the Output Instructions for formatting the final response."
    ]

    # Generate prompts using OpenAI API
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompts,
        temperature=0.7,
        max_tokens=1500,
        stop=None
    )


def _handle_error(error: ToolException) -> str:
    return (
            "The following errors occurred during tool execution:"
            + error.args[0]
            # + traceback.format_exc()  # TODO: Take this out after debugging
            + "Please fix any validation errors you can."
            + "Otherwise, Please try another tool."
    )


class JavaToolInput(BaseModel):
    jc: JavaCode = Field(description="Object containing the entire raw java code you want to search")
    search_string: StrictStr = Field(description="The line of code you want to search for in the java code")

    @staticmethod
    def get_line_number(jc: JavaCode, search_string: StrictStr) -> int | None:
        """ Returns the line number where the search_string appears within the JavaCode"""
        return jc.get_line_number(search_string)


class JavaTool(BaseTool):
    name: str = "java_line_number_finder"
    description: str = "Tool returns the line number that the text appears on"
    args_schema: Type[BaseModel] = JavaToolInput
    verbose = True
    handle_tool_error = _handle_error

    def _run(self, jti: JavaToolInput, run_manager: Optional[CallbackManagerForToolRun] = None, ) -> int | None:
        return jti.get_line_number(jti.jc, jti.search_string)


class JavaToolKit(BaseToolkit):
    tools: List[BaseTool] = []

    @classmethod
    def from_self(cls) -> "JavaToolKit":
        # Create the Tools

        line_number_tools = JavaTool()
        tools = []
        tools.append(line_number_tools)
        return cls(tools=tools)

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return self.tools


def test_openai_pydantic_functions():
    exam_prompt_base = """You are a Java 151 professor grading a student's exam submission. Complete the following Tasks using the Task Completion Strategy.
    
    Tasks:
    Using the given Exam Instructions and given Example Solution, analyze the Student Submission to identify all major and minor errors.
    Convert the Student Submission to JavaCode model.
    Use sufficient_amount_of_comments to determine if submission has a sufficient amount of comments.
    Use get_line_number to provide the correct line number for error references.
    Provide a detailed description for each error written objectively and constructively and direct referring only to the code.
    Include the corresponding line number(s) from the the Student Submission to the identified error when it is appropriate.
    Do not omit any errors identified. 
    If any errors are similar in nature list it only only once using the most relevant error type prioritizing the major over minor error type selection.
    Both major and minor errors list should be exhaustive.
    Use the Major Error Types and Minor Error Types as your guide for error identification.
    The errors you identify will be used to determine the student's final grade on their exam submission.
    
    Be honest but fair and use a friendly tone. 
    
    ---
    Exam Instructions: 
    {exam_instructions}
    
    ---
    Example Solution:
    {exam_solution}
    
    ---
    Major Error Types:
    {major_error_types}
    
    ---
    Minor Error Types:
    {minor_error_types}
    
    --- 
    Student Submission: 
    {submission}
    
    ---
    Task Completion Strategy:
        
    Task: The task are you currently trying to complete    
    Thought: you should always think about what to do
    Action: the action to take, should be one of your tools functions if needed
    Action Input: the input to the action (try to resolve validation errors)
    Observation: the result of the action
    .. (this Task/Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the task current task 
    .. (this Task/Final Answer can repeat N times)
    All Task Completed: Once all task are completed you can give your final response using the Final Output Instructions
    
    
    IMPORTANT: Your response to the user must follow the Final Output Instructions exactly.
    
    ---
    Final Output Instructions:
    {format_instructions}
    
    Start your Tasks!
    
    Question: What are the major and minor errors found in the Student Submission?
    Task: {task}
    Thought: {agent_scratchpad}
    
    Final Output:
    """

    """
    prompt = ChatPromptTemplate.from_messages(
        [("system", exam_prompt_base
       )]
    )
    """

    parser = PydanticOutputParser(pydantic_object=ErrorDefinitions)
    format_instructions = parser.get_format_instructions()

    prompt = PromptTemplate(
        # template_format="jinja2",
        input_variables=["exam_instructions", "exam_solution", "submission"],
        partial_variables={
            "format_instructions": format_instructions,
            "major_error_types": "\n\t".join(MajorErrorType.list()),
            "minor_error_types": "\n\t".join(MinorErrorType.list())
        },
        template=(
            exam_prompt_base
        ).strip(),
    )

    pydantic_schemas = [
        # ErrorDefinitions,
        # MajorError,
        # MinorError,
        JavaCode,
        JavaToolInput
    ]

    tools = [convert_to_openai_tool(p) for p in pydantic_schemas]

    model_version = 'gpt-3.5-turbo-16k-0613'
    # model_version = "gpt-3.5-turbo-1106"

    llm = ChatOpenAI(model=model_version).bind(
        # tools=tools,
        # response_format={"type": "json_object"}
    )

    # chain = prompt | model | PydanticToolsParser(tools=[pydantic_schemas])
    # chain = prompt | model

    chat_history = MessagesPlaceholder(variable_name="chat_history")
    # memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent_kwargs = {
        # "extra_prompt_messages": [chat_history],
        "system_message": prompt,
        "memory_prompts": [chat_history],
        "input_variables": ["task", "agent_scratchpad", "chat_history",
                            "exam_instructions", "exam_solution", "submission"
                            ],
        "verbose": True,
    }

    toolkit = JavaToolKit.from_self()
    tools = toolkit.get_tools()
    # tools = [StructuredTool.from_function(JavaToolInput.get_line_number)]

    chain = initialize_agent(
        tools=tools,
        llm=llm,
        # agent=AgentType.OPENAI_FUNCTIONS,
        # agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
        # max_iterations=5,
        handle_parsing_errors="Check your output try to resolve any validation errors",
        # return_intermediate_steps=True,
        # early_stopping_method="generate"
    )

    output = chain.invoke({"input": {
        "exam_instructions": EXAM_INSTRUCTIONS,
        "exam_solution": EXAM_SOLUTION,
        "submission": STUDENT_SUBMISSION,
        "response_format": {"type": "json_object"}
    }})

    print(output)


def grade_submissions():
    code_grader = CodeGrader(200, 40, 10)

    code_grader.grade_submission(EXAM_INSTRUCTIONS, EXAM_SOLUTION, STUDENT_SUBMISSION)
    print("Grade Feedback:\n%s" % code_grader.get_text_feedback())

    # Example usage
    """
    exampl_error_definitions = get_test_definitions()
    code_grader.major_errors = exampl_error_definitions.get_major_errors_unique()
    code_grader.minor_errors = exampl_error_definitions.get_minor_errors_unique()
    code_grader.points = 100
    code_grader.major_deduction_total = 80
    code_grader.minor_deduction_total = 20
    """

    assignment_name = "Programming Exam 1"
    student_file_name = "Exam1Harris"
    time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_path = f"./logs/{assignment_name}_{student_file_name}-{model}_temp({str(temperature)})-{time_stamp}.docx".replace(
        " ", "_")

    # Style the feedback and save to .docx file
    code_grader.save_feedback_to_docx(file_path)


def grade_all_from_directory(exam_instructions_file: str, exam_solution_file: str, downloaded_exams_directory: str):
    # Get the exam instructions
    exam_instructions = read_file(exam_instructions_file)

    # print("Exam Instructions:\n%s" % exam_instructions)

    # Get the exam example solution
    exam_solution = read_file(exam_solution_file)

    # print("Exam Solutions:\n%s" % exam_solution)

    # Get all the files in the current working directory
    files = [file for file in os.listdir(downloaded_exams_directory) if file.endswith(".java")]

    assignment_name = "Programming Exam 1"
    time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # Loop through every file in directory and grade the assignment saved to a file
    for file in files:
        student_submission = read_file(downloaded_exams_directory + "/" + file)
        # print("Student Submission:\n%s" % student_submission)

        student_file_name, student_file_extension = os.path.splitext(file)

        print("Grading: %s" % student_file_name)

        code_grader = CodeGrader(200, 40, 10)
        code_grader.grade_submission(exam_instructions, exam_solution, student_submission)
        print("\n\nGrade Feedback:\n%s" % code_grader.get_text_feedback())

        file_path = f"./logs/{assignment_name}_{student_file_name}-{model}_temp({str(temperature)})-{time_stamp}.docx".replace(
            " ", "_")

        # Style the feedback and save to .docx file
        code_grader.save_feedback_to_docx(file_path)


if __name__ == '__main__':
    #code_grader = CodeGrader(200, 40, 10)
    #code_grader.save_feedback_template("/Users/christopherqueen/Google Drive/CPCC/CPCC_Task_Automation/downloads/CSC151-N853/exam1/Grading_Feedback_Template.docx")
    #exit(0)


    grade_all_from_directory(
        exam_instructions_file="//downloads/CSC151-N853/exam1/Exam1_Instructions.txt",
        exam_solution_file="//downloads/CSC151-N853/exam1/Exam1_Solution.java",
        #downloaded_exams_directory="/Users/christopherqueen/Google Drive/CPCC/CPCC_Task_Automation/downloads/CSC151-N853/exam1/submissions_test"
        # Exception directory (belwo_
        downloaded_exams_directory = "/Users/christopherqueen/Google Drive/CPCC/CPCC_Task_Automation/downloads/CSC151-N853/exam1/submissions_late_exception"

        # TODO: Testing directory
        #downloaded_exams_directory="/Users/christopherqueen/Google Drive/CPCC/CPCC_Task_Automation/downloads/exam1/submissions_all"

    )

    # jc = JavaCode(raw_code=STUDENT_SUBMISSION)
    # line_number = jc.get_line_number(r"// Amount due.")
    # print("Code found on line number: %s" % str(line_number))
    # print("Comments Count: %d" % jc.comments_count)

    # test_openai_pydantic_functions()

    # test_code_loader()
    # exit(0)

    # print(wrap_code_in_markdown_backticks(STUDENT_SUBMISSION))
    # exit(0)
