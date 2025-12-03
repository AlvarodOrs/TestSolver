from workers import bot_launcher, log_in, test
from utils import tools
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def enter_UNIR(automation, AUTOMATED_LOGIN, UNIR_USERNAME, UNIR_PASSWORD, LOGIN_URL, MENU_XPATH):
    # Step 1: Login
    print("[+] Entering UNIR")
    login_success = log_in.logIn(automation, login_url=LOGIN_URL, automated_login=AUTOMATED_LOGIN, username=UNIR_USERNAME, password=UNIR_PASSWORD)
    if not login_success:
        print("\n[-] Login failed. Check your credentials and try again")
        return

def iterate_tests(automation, page, DEBUGGING=False):
    
    tests_urls = test.get_tests(automation, timeout=10)
    print(f", {len(tests_urls)} tests found")
    tests = automation.driver.find_elements(By.XPATH, "//span[@class='text-activityname' and contains(text(), 'Test Tema')]")
    _indx = 0
    for test_url in tests_urls:
        _indx += 1
        print(f"    \033[4m[+] Going to test number {_indx}\033[0m")
        
        automation.navigate(test_url)
        
        test_results = []
        
        default_answer = 0
        available_answer_options = ['a', 'b', 'c', 'd', 'e']
        
        while 0 in test_results or not test_results:
            
            if not test.find_test_button(automation, timeout=10):
                print(f"[!] Can't find test button")
            answer_letter = available_answer_options[default_answer]
            print(f"       [+] Completing with {answer_letter.upper()}'s", end="")

            if DEBUGGING: print(f"[DEBUGGING]")
            
            if not test_results:

                print(f": {test.solve_test(automation, timeout=10, answers=default_answer, DEBUGGING=False)} correct")
                
                binary_answers = test.read_answers(automation, timeout=10)
                if DEBUGGING: print(f"[DEBUGGING] raw binary answers: {binary_answers}")
                
                binary_answers = tools.dict_to_list(binary_answers)
                
                test_results = binary_answers
                if DEBUGGING: print(f"[DEBUGGING] processed binary answers: {binary_answers}")
            else:
                
                if DEBUGGING: print(f"[DEBUGGING] test_results: {test_results}")
                
                new_answers = tools.swap_errors_with(test_results, default_answer+1)
                if DEBUGGING: print(f"[DEBUGGING] new_answers: {new_answers}")
                
                print(f": {test.solve_test(automation, timeout=10, answers=new_answers, DEBUGGING=False)} correct")
                
                binary_answers = test.read_answers(automation, timeout=10)
                if DEBUGGING: print(f"[DEBUGGING]e] raw binary answers: {binary_answers}")
                binary_answers = tools.dict_to_list(binary_answers)
                if DEBUGGING: print(f"[DEBUGGING]e] processed binary answers: {binary_answers}")
                test_results = tools.combinate_answers(new_answers, binary_answers)
                # COMPARE NEW_ANSWERS AND RESPUESTAS_BINARIO TO UPDATE test_results
            default_answer += 1
            if DEBUGGING: print(f"[DEBUGGING] Completed {test_url} with {default_answer}")
        # if 0 in test_results:
        #     print("[?] Missing option D answers, completing them now")
        #     test_results = tools.swap_errors_with(test_results, 4)
        #     test.find_test_button(automation, timeout=10)
        #     test.solve_test(automation, timeout=10, anwers=test_results, DEBUGGING=True)
        # if 0 in test_results or -1 in test_results:
        #     print(f"\033[91m[!] More than 4 options found in test #{i} of course #{page}, try that one manually\033[0m")
        # print(f"            [+] Correct answers: {test_results}")
        print(f"[+] Test #{_indx+1} completed")
    print("\033[1m[+] Course completed\033[0m")
        
def iterate_courses(automation, UNIR_COURSES):
    for course_id in UNIR_COURSES.split(','):
    
        print(f"\n\033[4m[+] Entering course: {course_id}\033[0m", end="")
    
        automation.navigate(f"https://campusonline.unir.net/mod/url/view.php?id={course_id}")
    
        actividades = WebDriverWait(automation.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="proeduca-courseuppermenu-nav-tabs"]/li[8]/a'))
        )
    
        actividades.click()
    
        
        iterate_tests(automation, course_id, DEBUGGING=False)
        
    print("\n[+] All courses completed")
        

def main():
    """Main function to orchestrate bot operations"""
    # Launch the bot
    AUTOMATED_LOGIN = True
    cfg = tools.setup_config()
    tools.ASCII_ART.title()
    if "UNIR_USERNAME" in cfg: UNIR_USERNAME = cfg["UNIR_USERNAME"]
    if "UNIR_PASSWORD" in cfg: UNIR_PASSWORD = cfg["UNIR_PASSWORD"]
    if "UNIR_COURSES" in cfg: UNIR_COURSES = cfg["UNIR_COURSES"]
    if "AUTOMATED_LOGIN" in cfg: AUTOMATED_LOGIN = cfg["AUTOMATED_LOGIN"]
    if "LOGIN_URL" in cfg: LOGIN_URL = cfg["LOGIN_URL"]
    if "MENU_XPATH" in cfg: MENU_XPATH = cfg["MENU_XPATH"]
    
    print(f"[+] Running bot for user: {UNIR_USERNAME}")
    automation = bot_launcher.launch_bot(headless=False)
    try:
        enter_UNIR(automation, AUTOMATED_LOGIN, UNIR_USERNAME, UNIR_PASSWORD, LOGIN_URL, MENU_XPATH)
        
        iterate_courses(automation, UNIR_COURSES)
        
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        automation.custom_close()
        print("\n[+] Bot finished execution")


if __name__ == "__main__":
    main()
