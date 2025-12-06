"""
AI made code, to save time
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import platform
import subprocess
import time


class WebAutomation:
    """Base class for web automation tasks"""
    def __init__(self, headless:bool = False, browser:str = "chrome"):
        """
        Initialize the web automation driver
            headless -> bool, True or False:
                Run browser in headless mode or not,
            
            browser -> str, chrome:
                Browser to use            
        """
        self.headless = False
        self.browser = browser
        self.driver = None
        self.wait = None
    def start(self) -> "WebAutomation":
        """
        Starts the browser driver
            returns -> self, WebAutomation:
                Selenium's WebAutomation instance
        """
        #if self.browser.lower() == "chrome":
        chrome_options = Options()

        if self.headless: chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)        
        self.wait = WebDriverWait(self.driver, 10)
        return self.driver
    
    def navigate(self, url:str) -> "WebAutomation":
        """
        Navigates to a URL
            url -> str, https://www.google.com:
                The desired url to go to,
            
            returns -> self, WebAutomation:
                Selenium's WebAutomation instance
        """
        if not self.driver: self.start()
        self.driver.get(url)
        return self
    
    def find_element(self, by:By, value:str, timeout:int = 10) -> "WebAutomation":
        """Find an element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    
    def wait_and_click(self, by:By, value:str, timeout:int = 10) -> "WebAutomation":
        """Click an element"""
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        return self
    
    def type_text(
        self,
        by:By,
        value:str,
        text:str,
        timeout:int = 10,
        slow_typing:bool = False
        ) -> "WebAutomation":
        """
        Type text into an input field
            by -> By:
                Selenium By By,

            value -> str, Username:
                Value for the By to search,

            text -> str, pepe:
                Text to type in the desired location,

            timeout -> int, 10:
                Time to wait for elements to load,

            slow_typing: If True, type character by character with delay
        """
        element = self.find_element(by, value, timeout)
        
        # Click the field first to ensure focus
        element.click()
        time.sleep(0.2)
        
        # Clear the field more carefully
        element.clear()
        time.sleep(0.2)
        
        # Sometimes clear() doesn't work well with JavaScript, so try Ctrl+A + Delete
        try:
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            time.sleep(0.1)
        except:
            pass
        
        # Type the text
        if slow_typing:
            # Type character by character (useful for fields with validation)
            for char in text:
                element.send_keys(char)
                time.sleep(0.05)
        else:
            element.send_keys(text)
        
        time.sleep(0.2)
        return self
        
    def get_text(self, by:By, value:str, timeout:int = 10) -> "WebAutomation":
        """Get text from an element"""
        element = self.find_element(by, value, timeout)
        return element.text
    
    
    def custom_close(self) -> "WebAutomation":
        """Safely close the browser and end the WebDriver session"""
        if self.driver:
            try:
                self.driver.quit()
                print("[+] Browser closed successfully")
            except Exception as e:
                print(f"\033[91m[!] Error quitting browser: {e}\033[0m")
                try:
                    print("[+] Quitting failed, trying to close")
                    self.driver.close()
                except Exception as e:
                    print(f"\033[91m[!] Error closing the browser: {e}\033[0m")

            finally:
                self.driver = None

def launch_bot(headless:bool = False, browser:str = "chrome") -> "WebAutomation":
    """
    Launch and return a WebAutomation instance
        headless -> bool, True or False:
            Run browser in headless mode or not,
        
        browser -> str, chrome:
            Browser to use,
        
        returns -> self, WebAutomation:
            Selenium's WebAutomation instance
    """
    bot = WebAutomation(headless=False, browser=browser)
    bot.start()
    return bot