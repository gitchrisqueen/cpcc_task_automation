import datetime as DT
import re
from collections import defaultdict

from selenium.webdriver.support.ui import Select

from cqc_cpcc.utilities.cpcc_utils import duo_login
from cqc_cpcc.utilities.date import format_year, get_datetime
from cqc_cpcc.utilities.selenium_util import *
from cqc_cpcc.utilities.utils import first_two_uppercase, html_table_to_dict, get_unique_names_flip_first_last, \
    flip_name, get_unique_names


def take_attendance():
    # From Mycollege find all courses belonging to instructor
    faculty_url = MYCOLLEGE_URL + "/Student/Student/Faculty"

    driver, wait = get_session_driver()

    driver.get(faculty_url)
    # Wait for title to change
    wait.until(EC.title_is("Web Login Service"))

    original_window = driver.current_window_handle

    # Login
    duo_login(driver)

    # Wait for title to change
    wait.until(EC.title_is(MYCOLLEGE_FACULTY_TITLE))

    # Switch back to original window
    # driver.switch_to.window(original_window)

    # Find each course
    # sections_table = driver.find_element(By.XPATH, "//table[id*='faculty-sections']")

    # course_section_atags = driver.find_elements(By.XPATH, "//a[starts-with(@id, 'section') and contains(@id, 'link')]")

    course_section_atags = wait.until(
        lambda d: d.find_elements(By.XPATH, "//a[starts-with(@id, 'section') and contains(@id, 'link')]"),
        "Waiting for auth buttons")

    course_urls = {}
    for atag in course_section_atags:
        course_name = atag.text
        course_urls[course_name] = atag.get_attribute("href")

    # TODO: GO TO BRIGHTSPACE and get attendance via submissions within the last 7 days for all courses
    # attendance_records = get_attendance_from_brightspace(driver)

    # TODO: For each course find nearest name match and record attendance

    for course_name in course_urls:
        url = course_urls[course_name]
        logger.info("%s URL found: %s" % (course_name, url))

        # Switch back to original window
        driver.switch_to.window(original_window)

        # Process course tab
        mycollegeTab_process(driver, url)

    # Put focus on current window which will be the window opener
    driver.switch_to.window(original_window)

    logger.info("Finished Attendance")
    driver.quit()


def mycollegeTab_process(driver: WebDriver, url: str):
    handles = driver.window_handles
    wait = get_driver_wait(driver)

    # Opens a new tab and switches to new tab
    driver.switch_to.new_window('tab')

    # Wait for the new window or tab
    wait.until(EC.new_window_is_opened(handles))

    # Keep track of current tab
    current_tab = driver.current_window_handle

    # Navigate to course url
    driver.get(url)

    # Click on attendance link when available
    click_element_wait_retry(driver, wait, "//a[contains(@class, 'esg-tab__link') and contains(text(),'Attendance')]",
                             "Waiting for Attendance Tab")

    # Find the corresponding Brightspace course
    course_name = driver.find_element(By.XPATH, "//*[@id='section-header']/*[@id='user-profile-name']").text
    logger.info("Course Name: %s" % course_name)
    term = driver.find_element(By.ID, "section-header-term").text
    term_semester, term_year = term.split()

    logger.info("Term Semester: %s | Year: %s" % (term_semester, term_year))

    attendance_records = brightspace_get_student_attendance(driver, course_name, term_semester, term_year)

    logger.info("Attendance Records: %s" % str(attendance_records))

    # Switch back to tab
    driver.switch_to.window(current_tab)

    next_day_students = []

    # For each date update the attendance on MyColleges Faculty page
    for record_date in attendance_records:
        students = attendance_records[record_date]
        # add any students from next day list
        students.extend(next_day_students)
        # Clear the next day student list
        next_day_students = []
        # Sort students in alphabetical order
        students.sort()
        # Format the date to match drop down selection
        formatted_date = get_datetime(record_date).strftime("%-m/%-d/%Y (%A)")

        logger.info("Attendance Date: %s | Name(s): %s " % (formatted_date, " | ".join(students)))

        try:
            # Click on date drop down select
            date_select_id = "event-dates-dropdown"
            click_element_wait_retry(driver, wait, date_select_id, 'Waiting for Select Date Dropdown', By.ID)

            date_select = Select(driver.find_element(By.ID, date_select_id))
            date_select.select_by_visible_text(formatted_date)

            # Click on date drop down select option
            # click_element_wait_retry(driver, wait,
            #                         "//*[@id='event-dates-dropdown']/option[contains(text(),'" + formatted_date + "')]",
            #                         "Waiting for "+formatted_date+" Date Dropdown option")

            wait_for_ajax(driver)
            # satisfied = are_you_satisfied()

            # Update the attendance for each student
            logger.info("Updating Attendance for Date: %s" % formatted_date)
            for student_name in students:
                student_name_parts = student_name.split(",")
                student_first_name = student_name_parts[0].strip()
                student_last_name = student_name_parts[1].strip()
                student_name_formatted = flip_name(student_name)
                logger.info("Present: %s" % student_name_formatted)

                # Set the present for OCLS and OLAB
                success = my_colleges_mark_student_present(driver, student_first_name, student_last_name)
                if success:
                    logger.info("Marked Present: %s" % student_name_formatted)
                else:
                    logger.info("Could Not Mark Present: %s" % student_name_formatted)

        except (NoSuchElementException, TimeoutException) as e:
            logger.info(
                "Cannot update attendance for Date: %s | Dropdown option was not found. | Adding students to the next available date." % formatted_date)
            next_day_students.extend(students)
            logger.info("Present (not recorded for %s): %s" % (formatted_date, " | ".join(students)))

    # TODO: Not sure if this is working as expected
    # Move focus else where so program will continue
    driver.switch_to.window(current_tab)

    # Ask user to review before moving on - give them a chance to review
    # satisfied = are_you_satisfied()

    # Close tab when done
    close_tab(driver)


def my_colleges_mark_student_present(driver: WebDriver, first_name: str, last_name: str, retry=0):
    success = False
    present_value = 'P'
    xpath1_select = ("//table[@id='student-attendance-table']//tr[descendant::div[contains(text(),'"
                     + first_name
                     + "') and contains(text(), '" + last_name + "')]]//td[contains(@data-role,'OCLS')]//select")
    # xpath1_option = xpath1_select + "//option[@value='" + present_value + "']"
    xpath2_select = xpath1_select.replace("OCLS", "OLAB")
    # xpath2_option = xpath1_option.replace("OCLS", "OLAB")

    wait = get_driver_wait(driver)

    try:
        # Click the OCLS select element
        click_element_wait_retry(driver, wait, xpath1_select, "Waiting for OCLS select")
        ocls_select = Select(driver.find_element(By.XPATH, xpath1_select))
        ocls_select.select_by_value(present_value)

        # Then click OCLS select the option
        # selected_item = ocls_select.first_selected_option
        # logger.info("OCLS Selected Option (after click): %s" % selected_item.get_attribute('value'))
        # driver.implicitly_wait(5)  # wait 5 seconds
        wait_for_ajax(driver)

        # Click the OLAB select element
        click_element_wait_retry(driver, wait, xpath2_select, "Waiting for OLAB select")
        olab_select = Select(driver.find_element(By.XPATH, xpath2_select))
        olab_select.select_by_value(present_value)

        # Then click OLAB select the option
        # selected_item = olab_select.first_selected_option
        # logger.info("OLAB Selected Option (after click): %s" % selected_item.get_attribute('value'))
        # driver.implicitly_wait(5)  # wait 5 seconds

        wait_for_ajax(driver)
        success = True

    except NoSuchElementException as e:
        logger.error("Exception: %s" % e)
    except StaleElementReferenceException as se:
        if retry < 3:
            driver.implicitly_wait(5)  # wait 5 seconds
            success = my_colleges_mark_student_present(driver, first_name, last_name, retry + 1)
        else:
            logger.error("Exception (after %s retries): %s" % (str(retry), se))
    except Exception as oe:
        logger.error("Exception: %s" % oe)

    return success


def brightspace_get_student_attendance(driver: WebDriver, course_name: str, term_semester: str, term_year: str) -> dict:
    handles = driver.window_handles
    wait = get_driver_wait(driver)

    driver.switch_to.new_window('tab')

    # Wait for the new window or tab
    # wait.until(EC.number_of_windows_to_be(3))
    wait.until(EC.new_window_is_opened(handles))

    # Keep track of current tab
    current_tab = driver.current_window_handle

    # Navigate to brightspace url
    driver.get(BRIGHTSPACE_URL)

    # Format the search string
    shrt_year = format_year(term_year)
    shrt_sem = first_two_uppercase(term_semester)  # TODO: May need to convert term semester using some other method

    csc_pattern = re.compile(re.escape('CSC-'))
    course_name = csc_pattern.sub("CSC", course_name)
    logger.info("Course Name (changed): %s" % course_name)

    course_search_string = course_name + " - " + shrt_year + shrt_sem
    logger.info("Searching for: %s" % course_search_string)

    # Click on the course menu
    click_element_wait_retry(driver, wait, "d2l-navigation-s-course-menu", "Waiting for Course Menu", By.CLASS_NAME)

    # Get the course url
    course_link = wait.until(
        lambda d: d.find_element(By.XPATH, "//a[contains(text(),'" + course_search_string + "')]"),
        "Waiting for Course Links")
    course_url = course_link.get_attribute("href")
    # course_url = brightspace_url + href_value
    logger.info("Course URL: %s" % course_url)

    # Navigate to course url
    driver.get(course_url)

    # Find the Content link
    content_link = wait.until(
        lambda d: d.find_element(By.XPATH, "//a[@class='d2l-navigation-s-link' and contains(text(),'Content')]"),
        "Waiting for Content Link")
    content_link_url = content_link.get_attribute("href")

    # Navigate to Content url
    driver.get(content_link_url)

    # Find the course Overview Link
    # course_overview_link = wait.until(
    #    lambda d: d.find_element(By.XPATH,
    #                             "//div[contains(@class,'textblock') and contains(text(),'Course Overview')]"),
    #    "Waiting for Course Overview Link")
    # course_overview_link.click()
    click_element_wait_retry(driver, wait, "//div[contains(@class,'textblock') and contains(text(),'Course Overview')]",
                             "Waiting for Course Overview Link",
                             )

    # Find the due date calendar link
    duedate_calendar_link = wait.until(
        lambda d: d.find_element(By.XPATH,
                                 "//a[contains(@class,'d2l-link') and contains(text(),'Due Date Calendar')]"),
        "Waiting for Due Date Calendar Link")
    # duedate_calendar_link = wait.until(EC.element_to_be_clickable(duedate_calendar_link))
    # duedate_calendar_link.click()
    duedate_calendar_url = duedate_calendar_link.get_attribute("href")
    logger.info("Due Date Calendar URL: %s" % duedate_calendar_url)

    # Navigate to Due Date Calendar url
    driver.get(duedate_calendar_url)

    # Switch to Iframe
    iframe = wait.until(lambda d: d.find_element(By.XPATH, "//iframe[contains(@class,'d2l-iframe')]"),
                        "Waiting for Duo Iframe")
    driver.switch_to.frame(iframe)

    # Get the first table element on the page
    tables = wait.until(
        lambda d: d.find_elements(By.XPATH,
                                  "//table"),
        "Waiting for table elements")
    assignment_table = tables[0]

    table_text = '<table>' + assignment_table.get_attribute('innerHTML') + '</table>'
    headers, assignment_table_dict = html_table_to_dict(table_text)
    # logger.info("Assignment Table: %s" % assignment_table_dict)

    # Find Assignments that are due within the last 7 days
    today = DT.date.today()
    yesterday = today - DT.timedelta(days=2)
    week_ago = yesterday - DT.timedelta(days=7)
    logger.info("Getting assignments that opened between %s - %s" % (
        week_ago.strftime("%m/%d/%Y"), yesterday.strftime("%m/%d/%Y")))
    # Check for assignments that can be counted towards attendance
    assignments_towards_attendance = attendance_assignments_from_dict(headers, assignment_table_dict, week_ago,
                                                                      yesterday)

    # Navigate to Content url
    driver.get(content_link_url)

    # Get the Assignments link
    click_element_wait_retry(driver, wait, "//div[contains(@class,'d2l-textblock') and text()='Assignments']",
                             "Waiting for Assignments Link")

    # Wait for page to change to Assignments content
    wait.until(lambda d: driver.find_element(By.XPATH,
                                             "//*[contains(@class, 'd2l-page-title') and contains(text(),'Assignments')]"))

    assignment_urls = []

    # Get Assignments Url
    # - Create xpath for each assignment name
    assignments_towards_attendance_modified = [x.replace("-", "").replace("  ", " ") for x in
                                               assignments_towards_attendance]

    assignments_towards_attendance.extend(assignments_towards_attendance_modified)
    assignments_towards_attendance_modified_2 = [x.replace("Quiz ", "Quiz - ") for x in
                                                 assignments_towards_attendance]

    assignments_towards_attendance.extend(assignments_towards_attendance_modified_2)

    assignments_towards_attendance = get_unique_names(assignments_towards_attendance)
    or_path = "' or text()='".join(assignments_towards_attendance)
    xpath = "//a[contains(@class,'d2l-link') and (text()='" + or_path + "')]"
    logger.info("Searching Xpath: %s" % xpath)

    try:
        a_links = driver.find_elements(By.XPATH, xpath)
        assignment_urls = [x.get_attribute('href') for x in a_links]
    except NoSuchElementException as e:
        logger.debug("Could not find any url links")

    """
    for ata in assignments_towards_attendance:
        # logger.info("Looking for Assignment Link: %s" % ata)

        # Note: Add xpath search for assignment name without dash or double_space
        ata_without_dash = ata.replace("-", "")
        ata_without_dash = ata_without_dash.replace("  ", " ")
        xpath = "//a[contains(@class,'d2l-link') and (text()='" + ata + "' or text()='" + ata_without_dash + "')]"
        logger.info("Searching Xpath: %s" % xpath)
        try:
            a_link = driver.find_element(By.XPATH, xpath)
            a_link_href = a_link.get_attribute("href")
            assignment_urls.append(a_link_href)



        except NoSuchElementException as e:
            logger.debug("Could not find url link for: %s" % ata)

    """

    logger.info("Assignment Link(s):")
    logger.info("\n".join(assignment_urls))

    attendance_records = get_attendance_from_brightspace_urls(driver, assignment_urls)

    # TODO: Check Discussion Boards under Course Tools
    discussion_attendance_records = get_attendance_from_brightspace_discussion_boards(driver)

    # Merge attendance records (this will normalize them also (remove duplicate names and flip names)
    final_attendance_records = get_merged_attendance_dict(attendance_records, discussion_attendance_records)

    # Switch back to tab
    driver.switch_to.window(current_tab)

    # Close tab when done
    close_tab(driver)

    return final_attendance_records


def get_attendance_from_brightspace_discussion_boards(driver: WebDriver) -> dict:
    wait = get_driver_wait(driver)

    discussion_attendance_records = {}

    # # Get the discussion link
    # discussion_link = wait.until(
    #     lambda d: d.find_element(By.XPATH,
    #                              "//d2l-menu-item-link[@text='Discussions' and contains(@class,'d2l-navigation-s-menu-item')]"),
    #     "Waiting for Content Link")
    # discussion_link_url = discussion_link.get_attribute("href")
    #
    # # Navigate to Discussions url
    # driver.get(discussion_link_url)

    # Parse discussions screen

    return discussion_attendance_records


def get_attendance_from_brightspace(driver: WebDriver) -> dict:
    # TODO: Navigate to All Courses

    # For Each Course Navigate to Course Tools - Assignments

    # Find Assignments that were due within the last 7 days

    # Record student names and dates fpr submissions to the dict with coursne name (dict:key) -> date(dict:key) -> list[steudnet names]

    return dict()  # TODO: Fix


def get_attendance_from_brightspace_urls(driver: WebDriver, assignment_urls: list) -> dict:
    # Keep track of current tab
    current_tab = driver.current_window_handle

    attendance_records = {}

    # Visit each assignment url
    for au in assignment_urls:
        # Switch back to tab
        driver.switch_to.window(current_tab)

        handles = driver.window_handles
        driver.switch_to.new_window('tab')
        wait = get_driver_wait(driver)

        # Wait for the new window or tab
        wait.until(EC.new_window_is_opened(handles))

        # Got to assignment url
        driver.get(au)
        # Get the Completion Summary Link
        click_element_wait_retry(driver, wait, "//a[contains(text(),'Completion Summary')]",
                                 "Waiting for Completion Summary Link")

        # Click on the completed link (to narrow down display)
        click_element_wait_retry(driver, wait, "//a[contains(text(),'Completed')]",
                                 "Waiting for Completed Link")
        driver.implicitly_wait(5)  # wait 5 seconds

        # Change per page items to max
        # Click the select element
        select_xpath = "//div[contains(@class,'d2l-numericpager')]/div/select[contains(@class,'d2l-select')]"
        select_option_xpath = select_xpath + "//option"

        select_options = wait.until(
            lambda d: d.find_elements(By.XPATH,
                                      select_option_xpath),
            "Waiting for Select options")

        # Get Max Value
        # option_values = map(lambda x: x.get_attribute('value'), select_options)
        option_values = [x.get_attribute('value') for x in
                         select_options]  # TODO: Check to make sure woring same as above
        max_value = max(option_values)
        # logger.info("Max Value: %s" % str(max_value))

        click_element_wait_retry(driver, wait,
                                 select_xpath,
                                 "Waiting for Max Per Page select")

        select_successful = False
        while not select_successful:
            try:
                select = Select(driver.find_element(By.XPATH, select_xpath))
                select.select_by_value(str(max_value))
                # driver.implicitly_wait(30)  # wait 10 seconds
                wait_for_ajax(driver)
                select_successful = True
            except (NoSuchElementException, ElementNotInteractableException) as ne:
                logger.info("No submissions found for assignment: %s" % au)
                select_successful = True
                # Close tab when done
                close_tab(driver)
                continue
            except StaleElementReferenceException as se:
                pass

        # are_you_satisfied()

        # Find the student names and the dates the for completed assignments
        try:
            student_names = get_elements_text_as_list_wait_stale(wait,
                                                                 "//tr[descendant::div[contains(text(),'Completed')]]/th/div[position()=2]/a",
                                                                 "Waiting for Student Names")
        except NoSuchElementException as ne:
            logger.info("No submissions found for assignment: %s" % au)
            # Close tab when done
            close_tab(driver)
            continue

        completed_dates = get_elements_text_as_list_wait_stale(wait,
                                                               "//div[contains(text(),'Completed')]",
                                                               "Waiting for Completion Dates")

        student_completions_dict = dict(zip(student_names, completed_dates))

        for student_name in student_completions_dict:
            # logger.info("Student Name: %s" % student_name)

            raw_date = student_completions_dict[student_name].replace("Completed", "")
            # logger.info("Completion Date (raw): %s" % raw_date)

            proper_date = get_datetime(raw_date)
            # logger.info("Completion Date (proper): %s" % proper_date.strftime("%m-%d-%Y"))

            proper_date_string = proper_date.strftime("%m-%d-%Y")
            if proper_date_string not in attendance_records:
                attendance_records[proper_date_string] = []

            # Add student attendance to date
            attendance_records.get(proper_date_string).append(student_name)
            # logger.info("Student Name: %s | Attendance Date: %s | Added!!!" % (student_name, proper_date_string))

        # TODO: Need to see if next page > is clickable and continue with those results

        # Close tab when done
        close_tab(driver)

        # headers = ["student_names", "attendance_date"]

        # return df.to_dict()
    return attendance_records


def attendance_assignments_from_dict(headers: dict, assignment_dict_table: dict, start_date: DT.date,
                                     end_date: DT.date) -> list:
    # Return assignments names that are due between the dates passed
    assignments = []

    assignment_header = headers[0]
    assignment_opens_header = headers[1]
    # assignment_due_date_header = headers[2]

    all_assignments = assignment_dict_table.get(assignment_header)
    assignment_opens_dates = assignment_dict_table.get(assignment_opens_header)
    # logger.info('Assignment Open Dates: %s' % assignment_opens_dates)

    for open_index, v in enumerate(assignment_opens_dates):
        # logger.info('Open Index: %s' % open_index)
        open_date = assignment_opens_dates.get(open_index)
        # logger.info('Open Date: %s' % str(open_date))

        proper_open_date = get_datetime(open_date)
        # logger.info('Start Date: %s' % start_date.strftime("%m-%d-%Y"))
        # logger.info('Open Date: %s' % proper_open_date.strftime("%m-%d-%Y"))
        # logger.info('End Date: %s' % end_date.strftime("%m-%d-%Y"))

        if start_date <= proper_open_date.date() <= end_date:
            # logger.info("Check assignment for attendance")
            assignment_text = all_assignments[open_index]
            logger.info(
                "Assignments Text: %s | Open Date: %s" % (assignment_text, proper_open_date.strftime("%m/%d/%Y")))

            for a in assignment_text.split("|"):
                if len(a) > 0:
                    assignments.append(a.strip())

    return assignments


def normalize_attendance_records(attendance_records: dict) -> dict:
    # Sort the records first
    attendance_records = dict(sorted(attendance_records.items()))
    # norm_records = dict(map(lambda kv: (kv[0], get_unique_names(kv[1])), attendance_records.items()))
    norm_records = dict(map(lambda kv: (kv[0], get_unique_names_flip_first_last(kv[1])), attendance_records.items()))
    return norm_records


def get_merged_attendance_dict(d1: dict, d2: dict) -> dict:
    merged_dict = defaultdict(list)

    for d in (d1, d2):  # you can list as many input dicts as you want here
        for key, value in d.items():
            merged_dict[key].extend(value)

    # logger.info("Merged attendance dicts: %s" % str(merged_dict))
    return normalize_attendance_records(merged_dict)
