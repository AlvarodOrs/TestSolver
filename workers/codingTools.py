# workers/codingTools.py

import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def list_clickable_menu_links(driver, menu_xpath=None, timeout=5):
    """
    Scan the navigation menu and print all <a> elements with their text,
    visibility, enabled status, and XPath for debugging. Also writes clickable links to output.txt.

    Args:
        driver: Selenium WebDriver instance
        menu_xpath: XPath to the menu container (defaults to MENU_XPATH env var)
        timeout: Max seconds to wait for the menu to appear
    """
    from selenium.common.exceptions import TimeoutException

    if menu_xpath is None:
        menu_xpath = os.getenv("MENU_XPATH")
        if not menu_xpath:
            print("MENU_XPATH not defined in environment variables")
            return

    try:
        menu_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, menu_xpath))
        )
    except TimeoutException:
        print(f"Menu element not found at {menu_xpath}")
        return

    links = menu_element.find_elements(By.TAG_NAME, "a")
    print(f"Found {len(links)} links in the menu:\n")
    clickable_list = []
    xpath_list = []
    for i, link in enumerate(links, start=1):
        text = link.text.strip()
        displayed = link.is_displayed()
        enabled = link.is_enabled()
        rect = link.rect
        clickable = displayed and enabled and rect['width'] > 0 and rect['height'] > 0
        element_id = link.get_attribute("id")
        xpath = f"//*[@id='{element_id}']" if element_id else f"//a[.//span[contains(normalize-space(text()), '{text}')]]"
        if clickable:
            clickable_list.append(f"{i}. Text: '{text}' | Displayed: {displayed} | Enabled: {enabled} | Clickable: {clickable} | XPath: {xpath}")
            if element_id:
                xpath_list.append(f"//*[@id='{element_id}']")

    # Append clickable links to output.txt
    with open("output.txt", "a", encoding="utf-8") as f:
        for line in clickable_list:
            f.write(line + "\n")
    return xpath_list

def get_course_xpath(driver, course_name, timeout=5):
    """
    Find the XPath of a course link by its text.

    Args:
        driver: Selenium WebDriver instance
        course_name: Text of the course
        timeout: Max seconds to wait for the element to appear

    Returns:
        str: XPath to the course element, or None if not found
    """
    try:
        # Wait until the element is present in the DOM (clickable not required)
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//a[.//span[contains(normalize-space(text()), '{course_name}')]]")
            )
        )
        # Return its XPath using the ID or reconstruct
        element_id = element.get_attribute("id")
        if element_id:
            xpath = f"//*[@id='{element_id}']"
        else:
            # fallback: use text-based XPath
            xpath = f"//a[.//span[contains(normalize-space(text()), '{course_name}')]]"
        return xpath
    except Exception as e:
        print(f"Could not find course: {course_name}. Error: {e}")
        return None

def expand_parent_menu(driver, parent_text, timeout=5):
    """
    Expand a parent menu item if it contains the given text.

    Args:
        driver: Selenium WebDriver instance
        parent_text: Text of the parent menu to expand
    """
    try:
        parent = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[contains(@class,'localboostnavigationcollapsibleparent') "
                           f"and .//span[contains(normalize-space(text()), '{parent_text}')]]")
            )
        )
        parent.click()
        # Optional: small wait to allow children to render
        WebDriverWait(driver, 1)
        print(f"Expanded parent menu: {parent_text}")
        return True
    except Exception:
        # Parent may already be expanded or not exist
        return False

def easy_click(driver, xpath, timeout=10):
    """
    Safely find an element by XPath and click it.

    Args:
        driver: Selenium WebDriver instance
        xpath: XPath of the element to click
        timeout: Max seconds to wait for element to be clickable
    """
    try:
        print(f"Looking for element: {xpath}")
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        # Scroll element into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()
        print(f"Clicked element: {xpath}")
        return True
    except Exception as e:
        print(f"Could not click element: {xpath}. Error: {e}")
        return False
