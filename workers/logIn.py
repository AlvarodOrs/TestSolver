"""
Login Worker Module
Handles web login automation
"""

import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def logIn(automation, login_url=None, username=None, password=None, username_selector=None, password_selector=None, submit_selector=None, automated_login=True):
    """
    Log in to a website
    
    Args:
        automation: WebAutomation instance
        login_url: URL of the login page (defaults to LOGIN_URL env var)
        username: Username to login (defaults to UNIR_USERNAME env var)
        password: Password to login (defaults to UNIR_PASSWORD env var)
        username_selector: Selector for username field (defaults to By.ID, "username")
        password_selector: Selector for password field (defaults to By.ID, "password")
        submit_selector: Selector for submit button (defaults to By.ID, "login")
    
    Returns:
        bool: True if login successful, False otherwise
    """
    try:
        login_url = login_url or os.getenv("LOGIN_URL")
        if automated_login:
            # Get credentials from parameters or environment variables
            username = username or os.getenv("UNIR_USERNAME")
            password = password or os.getenv("UNIR_PASSWORD")
        
            if not login_url:
                raise ValueError("Login URL not provided. Set LOGIN_URL env var or pass login_url parameter")
            if not username:
                raise ValueError("Username not provided. Set UNIR_USERNAME env var or pass username parameter")
            if not password:
                raise ValueError("Password not provided. Set UNIR_PASSWORD env var or pass password parameter")
        
        # Navigate to login page
        print(f"Navigating to login page: {login_url}")
        automation.navigate(login_url)
        time.sleep(5)  # Wait for page to load
        if automated_login:
            # Default selectors
            username_by = By.ID
            username_value = "Username"  # Best: ID is unique and fastest
            password_by = By.ID
            password_value = "Password"
            submit_by = By.CSS_SELECTOR  # Button has class="button primary", no ID
            submit_value = "input.button.primary"  # CSS selector for submit button
            
            # Use custom selectors if provided (format: "id:username" or "name:username" or "xpath://input[@type='text']")
            if username_selector:
                username_by, username_value = _parse_selector(username_selector)
            if password_selector:
                password_by, password_value = _parse_selector(password_selector)
            if submit_selector:
                submit_by, submit_value = _parse_selector(submit_selector)
                        
            # Verify the username was entered correctly
            print("Entering username...")
            automation.type_text(username_by, username_value, username)
            time.sleep(0.75)
            
            # Fill in password
            print("Entering password...")
            automation.type_text(password_by, password_value, password)
            time.sleep(0.75)
            
            # Click login button
            print("Clicking login button...")
            automation.click(submit_by, submit_value)
            time.sleep(2)  # Wait for login to process
        else:
            input("Press Enter to continue...")
        print("Login completed!")
        
        # Check for and click the opinator close button if it exists
        try:
            close_button = automation.find_element(By.XPATH, '//*[@id="opinator-close-button"]', timeout=3)
            print("Found opinator close button, clicking it...")
            close_button.click()
            time.sleep(1)  # Wait a moment after clicking
            print("Close button clicked successfully!")
        except Exception:
            # Element not found, which is fine - it might not always be present
            print("Opinator close button not found (this is normal if it's not present)")
        
        return True
        
    except Exception as e:
        print(f"Login error: {e}")
        return False


def _parse_selector(selector):
    """
    Parse selector string into By type and value
    Format: "id:value", "name:value", "xpath:value", "css:value", "class:value"
    """
    if ":" in selector:
        selector_type, value = selector.split(":", 1)
        selector_map = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "link": By.LINK_TEXT,
            "partial_link": By.PARTIAL_LINK_TEXT
            }
        by_type = selector_map.get(selector_type.lower(), By.ID)
        return by_type, value
    else:
        # Default to ID if no prefix
        return By.ID, selector
