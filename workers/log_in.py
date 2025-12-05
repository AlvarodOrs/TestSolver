import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def logIn(
    automation,                     
    login_url:str=None,
    username:str=None,
    password:str=None,
    automated_login:bool=True,
    timeout:int=10
    ) -> bool:
    """
    Function to log in the page
        automation -> WebAutomation instance:
            The Selenium driver,
        
        login_url -> string, https://campusonline.unir.net/my:
            The log in url of the desired page,
        
        username -> string, your@used.email:
            The email of your account,

        password -> string, yourPassword:
            The password of your account,
        
        automated_login -> bool, True or False:
            Allow the bot to log in for you,

        timeout -> int, 10:
            Time to wait for elements,

        returns -> bool, True or False:
            If it is succesful logging in
    """
    def close_opinator(wrapper_or_driver, timeout:int=3) -> bool:
        """
        Function to close the opinator pop-up
            wrapper_or_driver -> Selenium driver:
                The Selenium bot driver,

            timeout -> int, 10:
                The time to wait for elements to load,
            
            returns -> bool, True or False:
                If it was an opinator to close
        """
        try:
            close_button = WebDriverWait(wrapper_or_driver.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="opinator-close-button"]'))
            )
            print("\033[33m[?] Opinator pop-up detected")
            close_button.click()
            print("[+] Opinator pop-up closed\033[0m")

            return True

        except Exception:
            print("\033[33m[?] Opinator pop-up not found (this is normal if it's not present)\033[0m")
            
            return False

    try:
        print(f"[+] Entering login page in: {login_url}")
        automation.navigate(login_url)
        WebDriverWait(automation.driver, timeout).until(
            EC.presence_of_element_located((By.ID, "Username"))
        )

        if automated_login:
            if not login_url: raise ValueError("Login URL not provided. Set LOGIN_URL env var or pass login_url parameter")
            if not username: raise ValueError("Username not provided. Set UNIR_USERNAME env var or pass username parameter")
            if not password: raise ValueError("Password not provided. Set UNIR_PASSWORD env var or pass password parameter")
                                                
            print("[+] Entering username")
            automation.type_text(By.ID, "Username", username)
            
            print("[+] Entering password")
            automation.type_text(By.ID, "Password", password)
            
            print("[+] Clicking login button")
            automation.click(By.CSS_SELECTOR, "input.button.primary")
        else: input("\033[92m[*] Press Enter to continue after manual login\033[0m")

        # Check for and click the opinator close button if it exists
        if close_opinator(automation, timeout): pass
        else: pass
        
        return True     
    
    except Exception as e:
        print(f"\033[91m[!] Login error: {e}\033[0m")
        
        return False