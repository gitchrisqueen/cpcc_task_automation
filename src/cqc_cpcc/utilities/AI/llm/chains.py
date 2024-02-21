from pprint import pprint
from typing import Type, TypeVar

from langchain.output_parsers import PydanticOutputParser, RetryWithErrorOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.utils import Output
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel

from cqc_cpcc.utilities.AI.llm.prompts import *
from cqc_cpcc.utilities.env_constants import RETRY_PARSER_MAX_RETRY
from cqc_cpcc.utilities.utils import wrap_code_in_markdown_backticks

retry_model = 'gpt-4-1106-preview'
retry_llm = ChatOpenAI(temperature=0, model=retry_model)

T = TypeVar("T", bound=BaseModel)


def retry_output(output: Output, parser: BaseOutputParser, prompt: PromptTemplate, **prompt_args) -> str:
    final_output = output
    retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=retry_llm,
                                                       max_retries=RETRY_PARSER_MAX_RETRY
                                                       )
    try:
        prompt_value = prompt.format_prompt(**prompt_args)
        final_output = retry_parser.parse_with_prompt(output.content, prompt_value)
    except OutputParserException as e:
        print("Exception During Retry Output: %s" % e)
        # if max_tries > 0:
        #    finalOutput = retryOutput(finalOutput, prompt, max_tries - 1, **prompt_args)
    return final_output


def generate_error_definitions(llm: BaseChatModel, pydantic_object: Type[T], major_error_type_list: list,
                               minor_error_type_list: list, exam_instructions: str, exam_solution: str,
                               student_submission: str, wrap_code_in_markdown=True) -> str:
    """ Returns a properly formatted error definitions object from LLM"""

    parser = PydanticOutputParser(pydantic_object=pydantic_object)
    format_instructions = parser.get_format_instructions()

    prompt = PromptTemplate(
        # template_format="jinja2",
        input_variables=["exam_instructions", "exam_solution", "submission"],
        partial_variables={
            "format_instructions": format_instructions,
            "major_error_types": "\n\t".join(major_error_type_list),
            "minor_error_types": "\n\t".join(minor_error_type_list)
        },
        template=(
            EXAM_REVIEW_PROMPT_BASE
        ).strip(),
    )

    # prompt_value = prompt.format_prompt(exam_instructions=exam_instructions, exam_solution=exam_solution, submission=student_submission)
    # print("\n\nPrompt Value:")
    # pprint(prompt_value)
    # print("\n\n")

    llm.bind(
        response_format={"type": "json_object"}
    )

    completion_chain = prompt | llm

    if wrap_code_in_markdown:
        exam_solution = wrap_code_in_markdown_backticks(exam_solution)
        student_submission = wrap_code_in_markdown_backticks(student_submission)

    output = completion_chain.invoke({
        "exam_instructions": exam_instructions,
        "exam_solution": exam_solution,
        "submission": student_submission,
        "response_format": {"type": "json_object"}
    })

    print("\n\nOutput:")
    pprint(output.content)

    try:
        final_output = parser.parse(output.content)
    except Exception as e:
        print("\n\nException during parse:")
        print(e)
        final_output = retry_output(output, parser, prompt,
                                    exam_instructions=exam_instructions,
                                    exam_solution=exam_solution,
                                    submission=student_submission)

    return final_output


def generate_feedback(llm: BaseChatModel, pydantic_object: Type[T], feedback_type_list: list, assignment: str,
                      solution: str, student_submission: str, course_name: str, wrap_code_in_markdown=True) -> str:
    """
    Generates feedback based on the assignment, solution, student submission and course name using the LLM model.
    """
    parser = PydanticOutputParser(pydantic_object=pydantic_object)
    format_instructions = parser.get_format_instructions()

    prompt = PromptTemplate(
        # template_format="jinja2",
        input_variables=["assignment", "solution", "submission", "course_name"],
        partial_variables={
            "format_instructions": format_instructions,
            "feedback_types": "\n\t".join(feedback_type_list)

        },
        template=(
            # ASSIGNMENT_FEEDBACK_PROMPT_BASE
            CODE_ASSIGNMENT_FEEDBACK_PROMPT_BASE
        ).strip(),
    )

    # prompt_value = prompt.format_prompt(exam_instructions=EXAM_INSTRUCTIONS, submission=STUDENT_SUBMISSION)
    # pprint(prompt_value)

    llm.bind(
        response_format={"type": "json_object"}
    )

    completion_chain = prompt | llm

    if wrap_code_in_markdown:
        solution = wrap_code_in_markdown_backticks(solution)
        student_submission = wrap_code_in_markdown_backticks(student_submission)

    output = completion_chain.invoke({
        "assignment": assignment,
        "solution": solution,
        "submission": student_submission,
        "course_name": course_name,
        "response_format": {"type": "json_object"}
    })

    print("\n\nOutput:")
    pprint(output)

    try:
        final_output = parser.parse(output.content)
    except Exception as e:
        print(e)
        final_output = retry_output(output, parser, prompt,
                                    assignment=assignment,
                                    solution=solution,
                                    submission=student_submission,
                                    course_name=course_name
                                    )

    print("\n\nFinal Output:")
    pprint(output)

    return final_output
