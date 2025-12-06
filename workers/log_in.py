import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def logIn(
    automation:"WebAutomation",
    LOGIN_URL:str = None,
    USERNAME:str = None,
    PASSWORD:str = None,
    timeout:int = 10
    ) -> bool:
    """
    Function to log in the page
        automation -> WebAutomation instance:
            The Selenium driver,
        
        LOGIN_URL -> str, https://campusonline.unir.net/my:
            The login url of the desired page,
        
        USERNAME -> str, your@used.email:
            The email of your account,

        PASSWORD -> str, yourPassword:
            The password of your account,

        timeout -> int, 10:
            Time to wait for elements to load,

        returns -> bool, True or False:
            If it was succesful logging in
    """
    def close_opinator(automation:"WebAutomation", timeout:int = 3) -> bool:
        """
        Function to close the opinator pop-up
            automation -> Selenium driver:
                The Selenium bot driver,

            timeout -> int, 10:
                The time to wait for elements to load,
            
            returns -> bool, True or False:
                If it was succesful finding and closing the opinator pop-up
        """
        try:
            
            automation.wait_and_click(By.XPATH, '//*[@id="opinator-close-button"]')
            print("\033[33m[?] Opinator pop-up detected")
            print("[+] Opinator pop-up closed\033[0m")

            return True

        except Exception:
            print("\033[33m[?] Opinator pop-up not found (this is normal if it's not present)\033[0m")
            
            return False

    def partial_login(automation:"WebAutomation", USERNAME:str = None, PASSWORD:str = None) -> bool:
        """
        Function to enter the user's correct parameters
            automation -> Selenium driver:
                The Selenium bot driver,

        USERNAME -> str, your@used.email:
            The email of your account,

        PASSWORD -> str, yourPassword:
            The password of your account,

        returns -> bool, True or False:
            If it was succesful of not logging in partially
        """
        try:
            if USERNAME:
                print("[+] Entering username")
                automation.type_text(By.ID, "Username", USERNAME)
            if PASSWORD:
                print("[+] Entering password")
                automation.type_text(By.ID, "Password", PASSWORD)

            return True
        except Exception as e:
            print("\033[91m[!] Partial login failed\033[0m")

            return False

    try:
        print(f"[+] Entering login page in: {LOGIN_URL}")
        automation.navigate(LOGIN_URL)

        if USERNAME != None and PASSWORD != None:
            if not LOGIN_URL: raise ValueError("Login URL not provided. Set LOGIN_URL env var or pass --target-url parameter")

            print("[+] Entering username")
            automation.type_text(By.ID, "Username", USERNAME)
            
            print("[+] Entering password")
            automation.type_text(By.ID, "Password", PASSWORD)
            
            print("[+] Clicking login button")
            automation.wait_and_click(By.CSS_SELECTOR, "input.button.primary") #DEBUGGING custom click here
        else:
            if not USERNAME: print(f"\033[33m[*] Username not provided.\n\tManually write the desired USERNAME in the login page or pass --username parameter\033[0m")
            if not PASSWORD: print(f"\033[33m[*] Password not provided.\n\tManually write the desired PASSWORD in the login page or pass --password parameter\033[0m")
            
            if not partial_login(automation, USERNAME, PASSWORD): return False 
            input(f"\033[33m[*] Press Enter to continue after manual login\033[0m")

        # Check for and click the opinator close button if it exists
        if close_opinator(automation, timeout=timeout/5): pass
        else: pass
        
        return True     
    
    except Exception as e:
        print(f"\033[91m[!] Login error: {e}\033[0m")
        
        return False