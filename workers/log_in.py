import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def logIn(
    automation,              # WebAutomation instance
    login_url=None,          # URL of the login page
    username=None,           # Username to login
    password=None,           # Password to login
    username_selector=None,  # Selector for username field
    password_selector=None,  # Selector for password field
    submit_selector=None,    # Selector for submit button
    automated_login=True     # Whether to use automated login or manual
    ) -> bool:

    try:

        if automated_login:

            if not login_url: raise ValueError("Login URL not provided. Set LOGIN_URL env var or pass login_url parameter")
            if not username: raise ValueError("Username not provided. Set UNIR_USERNAME env var or pass username parameter")
            if not password: raise ValueError("Password not provided. Set UNIR_PASSWORD env var or pass password parameter")
        
        print(f"[+] Entering login page in: {login_url}")
        automation.navigate(login_url)
        WebDriverWait(automation.driver, 10).until(
            EC.presence_of_element_located((By.ID, "Username"))
        )

        if automated_login:

            username_by = By.ID
            username_value = "Username"
            password_by = By.ID
            password_value = "Password"
            submit_by = By.CSS_SELECTOR
            submit_value = "input.button.primary"
            
            # Use custom selectors if provided (format: "id:username" or "name:username" or "xpath://input[@type='text']")
            if username_selector: username_by, username_value = _parse_selector(username_selector)
            if password_selector: password_by, password_value = _parse_selector(password_selector)
            if submit_selector: submit_by, submit_value = _parse_selector(submit_selector)
                        
            print("[+] Entering username")
            automation.type_text(username_by, username_value, username)
            
            print("[+] Entering password")
            automation.type_text(password_by, password_value, password)
            
            print("[+] Clicking login button")
            automation.click(submit_by, submit_value)
        else:
            input("\033[92m[*] Press Enter to continue after manual login\033[0m")

        # Check for and click the opinator close button if it exists
        try:
            close_button = WebDriverWait(automation.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="opinator-close-button"]'))
            )
            print("\033[33m[?] Opinator pop-up detected\033[0m")
            close_button.click()
            print("[+] Opinator pop-up closed")

        except Exception:
            # Element not found, which is fine - it might not always be present
            print("\033[33m[?] Opinator pop-up not found (this is normal if it's not present)\033[0m")
        
        return True     
    except Exception as e:
        print(f"\033[91m[!] Login error: {e}\033[0m")
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
    # Default to ID if no prefix
    else: return By.ID, selector