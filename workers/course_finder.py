"""
Course Finder Module
Finds and clicks on specific courses in the navigation menu
"""

import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from workers.codingTools import list_clickable_menu_links, get_course_xpath, expand_parent_menu, easy_click

def click_course_by_name(driver, course_name, timeout=10):
    """
    Find a course by name and click it.

    Args:
        driver: Selenium WebDriver instance
        course_name: Text of the course to click
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[.//span[contains(normalize-space(text()), '{course_name}')]]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        print(f"Clicked course: {course_name}")
        return True
    except Exception as e:
        print(f"Could not click course: {course_name}. Error: {e}")
        return False


def find_and_click_courses(driver, menu_xpath=None, wait_time=2):
    """
    Find courses in the navigation menu and click on each one.

    Args:
        driver: Selenium WebDriver instance
        menu_xpath: XPath to the menu element (defaults to MENU_XPATH env var)
        wait_time: Optional initial wait before starting

    Returns:
        dict: Results with course name as key and click status
    """
    results = {}

    # Optional initial wait
    if wait_time > 0:
        import time
        time.sleep(wait_time)
    list_clickable_menu_links(driver)
    pass
    # Get menu XPath
    if menu_xpath is None:
        menu_xpath = os.getenv("MENU_XPATH")
        if not menu_xpath:
            print("MENU_XPATH not defined in environment variables")
            return results

    # Get courses list from env
    courses_to_find = json.loads(os.getenv("MY_COURSES", "[]"))
    if not courses_to_find:
        print("No courses specified in MY_COURSES environment variable")
        return results

    for course in courses_to_find:
        print(f"Searching for course: {course}")
        # Optional: expand parent menu if needed
        # Click the course
        _tempList = []
        easy_click(driver, _temp)
        course_xpath = get_course_xpath(driver, course)
        print(f"Found {course}")
        driver.find_element(By.XPATH, f"{course_xpath}").click()
        print(f"Clicked {course}")
        clicked = click_course_by_name(driver, course)
        results[course] = "clicked" if clicked else "not found or clickable"

    return results


def save_course_data(data, filename="courses_data.json"):
    """
    Save course data to a JSON file.

    Args:
        data: Data to save (dict or list)
        filename: Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Course data saved to {filename}")
    except Exception as e:
        print(f"Error saving course data: {e}")
