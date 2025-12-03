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
    
    def __init__(self, headless=False, browser="chrome"):
        """
        Initialize the web automation driver
        
        Args:
            headless: Run browser in headless mode (no GUI)
            browser: Browser to use ('chrome' or 'firefox')
        """
        self.headless = False
        self.browser = browser
        self.driver = None
        self.wait = None
        
    def start(self):
        """Start the browser driver"""
        if self.browser.lower() == "chrome":
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            raise ValueError(f"Browser {self.browser} not supported yet")
        
        self.wait = WebDriverWait(self.driver, 10)
        return self.driver
    
    def navigate(self, url):
        """Navigate to a URL"""
        if not self.driver:
            self.start()
        self.driver.get(url)
        return self
    
    def find_element(self, by, value, timeout=10):
        """Find an element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    
    def click(self, by, value, timeout=10):
        """Click an element"""
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        return self
    
    def type_text(self, by, value, text, timeout=10, slow_typing=False):
        """
        Type text into an input field
        
        Args:
            by: Selenium By locator
            value: Value for the locator
            text: Text to type
            timeout: Timeout for finding element
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
    
    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present"""
        return self.find_element(by, value, timeout)
    
    def get_text(self, by, value, timeout=10):
        """Get text from an element"""
        element = self.find_element(by, value, timeout)
        return element.text
    
    def get_page_source(self):
        """Get the full page source"""
        return self.driver.page_source
    
    def get_current_url(self):
        """Get the current page URL"""
        return self.driver.current_url
    
    def custom_close(self):
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

def launch_bot(headless=False, browser="chrome"):
    """
    Launch and return a WebAutomation instance
    
    Args:
        headless: Run browser in headless mode
        browser: Browser to use
        
    Returns:
        WebAutomation instance
    """
    bot = WebAutomation(headless=False, browser=browser)
    bot.start()
    return bot