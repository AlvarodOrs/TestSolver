from workers import bot_launcher, log_in, test
from utils import tools
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def enter_log_in_page(
    automation:"WebAutomation",
    LOGIN_URL:str = None,
    USERNAME:str = None,
    PASSWORD:str = None,
    timeout:int = 10
    ) -> bool:
    """
    Starts the bot with the following parameters:
        automation -> WebAutomation:
            Selenium's WebAutomation instance,

        LOGIN_URL -> string, https://your.desired.moodle/login/page:  (default, UNIR's one)
            Bot will use this for the login process,
        
        USERNAME -> string, your@unir.email:
            Bot will use this as your valid UNIR/Moodle email,
        
        PASSWORD -> string, yourpassword:
            Bot will use this as your valid UNIR/Moodle password,
        
        timeout -> int, 10:
            Time to wait for elements to load,
        
        returns -> bool, True or False:
            If it was succesful entering             
    """
    print("[+] Entering login page")
    return log_in.logIn(automation=automation, LOGIN_URL=LOGIN_URL, USERNAME=USERNAME, PASSWORD=PASSWORD, timeout=timeout)
        
def iterate_tests(automation:"WebAutomation", timeout:int = 10, DEBUGGING:bool = False) -> bool:
    """
    The bot iterates through all the available tests in a course:
        automation -> Selenium driver:
            The Selenium web driver,

        timeout -> int, 10:
            The time to wait for elements to load,

        DEBUGGING -> bool, True or False:
            Show debugging logs or not,
            
        returns -> bool, True or False:
            If it was succesful iterating the tests           
    """
    tests_urls = test.get_tests(automation, timeout=timeout)
    print(f", {len(tests_urls)} tests found")
    tests = automation.driver.find_elements(By.XPATH, "//span[@class='text-activityname' and contains(text(), 'Test Tema')]")
    _indx = 0
    tests_urls = tests_urls[-1:]
    for test_url in tests_urls:
        _indx += 1
        print(f"    \033[4m[+] Going to test number {_indx}: {test_url}\033[0m")
        
        automation.navigate(test_url)
        
        test_results = []
        mark = "0%"
        default_answer = 0
        available_answer_options = ['a', 'b', 'c', 'd', 'e']
        while 0 in test_results or not test_results:

            #break #Debugging


            if not test.find_test_button(automation=automation, timeout=timeout):
                print(f"[!] Can't find test button")
            answer_letter = available_answer_options[default_answer]
            print(f"       [+] Completing with {answer_letter.upper()}'s", end="")

            if DEBUGGING: print(f"[DEBUGGING]")
            
            if not test_results:
                mark = test.solve_test(automation, answers=default_answer, timeout=timeout, DEBUGGING=DEBUGGING)
                print(f": {mark} correct")
                
                binary_answers = test.read_answers(automation, timeout=timeout)
                if DEBUGGING: print(f"[DEBUGGING] raw binary answers: {binary_answers}")
                
                binary_answers = tools.dict_to_list(binary_answers)
                
                test_results = binary_answers
                if DEBUGGING: print(f"[DEBUGGING] processed binary answers: {binary_answers}")
            else:
                
                if DEBUGGING: print(f"[DEBUGGING]else] test_results: {test_results}")
                
                new_answers = tools.swap_errors_with(test_results, default_answer+1)
                if DEBUGGING: print(f"[DEBUGGING]else] new_answers: {new_answers}")
                
                mark = test.solve_test(automation, timeout=10, answers=new_answers, DEBUGGING=False)
                print(f": {mark} correct")
                
                binary_answers = test.read_answers(automation, timeout=timeout)
                if DEBUGGING: print(f"[DEBUGGING]else] raw binary answers: {binary_answers}")
                binary_answers = tools.dict_to_list(binary_answers)
                if DEBUGGING: print(f"[DEBUGGING]else] processed binary answers: {binary_answers}")
                test_results = tools.combinate_answers(new_answers, binary_answers)
                # COMPARE NEW_ANSWERS AND RESPUESTAS_BINARIO TO UPDATE test_results
            default_answer += 1
            if DEBUGGING: print(f"[DEBUGGING] Completed {test_url} with {default_answer}")
        print(f"    [+] Test #{_indx} completed: {int(mark[:-1])/10}/10")
    print("\033[1m[+] Course completed\033[0m")
    return True
        
def iterate_courses(automation:"WebAutomation", COURSES_HOME_URL:str = None, COURSES:str = None, timeout:int = 10, DEBUGGING:bool = False) -> bool:
    try:
        for course_id in COURSES.split(','):
        
            print(f"\n\033[4m[+] Entering course: {course_id}\033[0m", end="")
            
            automation.navigate(f"{COURSES_HOME_URL}{course_id}")
            
            actividades = WebDriverWait(automation.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="proeduca-courseuppermenu-nav-tabs"]/li[8]/a')))
        
            actividades.click()
        
            if not iterate_tests(automation=automation, timeout=timeout, DEBUGGING=DEBUGGING): print(f"\033[91m[!] Error iterating test in course {course_id}\033[0m")
            
        print("\n[+] All courses completed")
    
        return True
    except Exception as e:
        print(f"\n\033[91m[!] Error occurred while iterating courses:\n\t{e}\033[0m")

        return False
        

def main():
    """
    Main function to orchestrate bot operations
    """
    os.system("")

    # ASCII art
    tools.ASCII_ART.title()

    # Launch the bot
    config = tools.setup_config()

    if "USERNAME" in config: USERNAME = config["USERNAME"]
    if "PASSWORD" in config: PASSWORD = config["PASSWORD"]
    if "COURSES" in config: COURSES = config["COURSES"]
    if "LOGIN_URL" in config: LOGIN_URL = config["LOGIN_URL"]
    if "COURSES_HOME_URL" in config: COURSES_HOME_URL = config["COURSES_HOME_URL"]
    timeout = 10
    DEBUGGING = False

    if not COURSES:
        print(f"\033[91m[!] No courses detected, please check the parameters\033[0m")
        return

    if USERNAME: nickname = f"user: {USERNAME}"
    else: nickname = "anonymous user"
    print(f"[+] Running bot for {nickname}")

    automation = bot_launcher.launch_bot(headless=False)
    try:
        if not enter_log_in_page(automation=automation, LOGIN_URL=LOGIN_URL, USERNAME=USERNAME, PASSWORD=PASSWORD, timeout=timeout): print("\n\033[91m[!] Login failed. Check your credentials and try again\033[0m")

        if not iterate_courses(automation=automation, COURSES_HOME_URL=COURSES_HOME_URL, COURSES=COURSES, timeout=timeout, DEBUGGING=DEBUGGING): print("\n\033[91m[!] Course iteration failed. Check logs and try again\033[0m")
        
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        automation.custom_close()
        print("\n[+] Bot finished execution")


if __name__ == "__main__":
    main()
