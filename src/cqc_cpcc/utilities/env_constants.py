import os

# Get constants from .env file
INSTRUCTOR_USERID = os.environ['INSTRUCTOR_USERID']
INSTRUCTOR_PASS = os.environ['INSTRUCTOR_PASS']
HEADLESS_BROWSER = os.environ['HEADLESS_BROWSER'] == 'True'
WAIT_DEFAULT_TIMEOUT = float(os.environ['WAIT_DEFAULT_TIMEOUT'])
MAX_WAIT_RETRY = int(os.environ['MAX_WAIT_RETRY'])
RETRY_PARSER_MAX_RETRY = int(os.environ['RETRY_PARSER_MAX_RETRY'])
SHOW_ERROR_LINE_NUMBERS = bool(os.environ['SHOW_ERROR_LINE_NUMBERS'])
FEEDBACK_SIGNATURE = os.environ['FEEDBACK_SIGNATURE']


# Set other constants
BRIGHTSPACE_URL = "https://brightspace.cpcc.edu"
MYCOLLEGE_URL = "https://mycollegess.cpcc.edu"
MYCOLLEGE_FACULTY_TITLE = 'Faculty - MyCollege'
BRIGHTSPACE_HOMEPAGE_TITLE = 'Homepage - Central Piedmont'



