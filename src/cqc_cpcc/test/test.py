from selenium.webdriver.support import expected_conditions as EC

import cqc_cpcc.attendance as AT
from cqc_cpcc.utilities.cpcc_utils import *
from cqc_cpcc.utilities.logger import logger
from cqc_cpcc.utilities.selenium_util import *


def test_max_select():
    driver, wait = get_session_driver()

    faculty_url = AT.MYCOLLEGE_URL + "/Student/Student/Faculty"
    url = "https://brightspace.cpcc.edu/d2l/le/content/168093/viewContent/6353658/View"

    driver.get(faculty_url)

    # Login
    duo_login(driver)

    # Wait for title to change
    wait.until(EC.title_is("Faculty - MyCollege"))

    AT.get_attendance_from_brightspace_urls(driver, [url])


def test_attendance_records():
    from attendance_records_example import a_records
    n_records = AT.normalize_attendance_records(a_records)
    logger.info("Attendance Records (normalized): %s" % str(n_records))


def test_attend_dict_merge():
    from attendance_records_example import a_records_old
    from attendance_records_example import a_records
    merged_dict = AT.get_merged_attendance_dict(a_records_old, a_records)
    logger.info("Attendance Records (merged): %s" % str(merged_dict))


def test_string_join():
    my_list = ["a","b"]
    or_path = "' or text()='".join(my_list)
    print("Or Path= %s" % or_path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_string_join()
    # test_max_select()
    # test_attendance_records()
    # test_attend_dict_merge()
