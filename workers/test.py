from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Union
import time
import re

def find_mark(automation:"WebAutomation", timeout:int = 10) -> int:
    """
    Function to find the mark of the test done
        automation -> Selenium driver:
            Selenium's WebAutomation instance,

        timeout -> int, 10:
            Time to wait for elements to load,
            
        returns -> int, 30:
            The mark of the last test
    """
    mark_box = automation.get_text(By.XPATH, "//tr[th[normalize-space()='Calificación']]/td")
    match = re.search(r"\d+\s*%", mark_box)
    
    try: return match.group()

    except Exception as e:
        print(f"\033[91m[!] Error finding mark\033[0m")

        return -1

def find_test_button(automation:"WebAutomation", timeout:int = 10) -> bool:
    """
    Function to find the button to start a test
        automation -> Selenium driver:
            Selenium's WebAutomation instance,

        timeout -> int, 10:
            Time to wait for elements to load,
            
        returns -> bool, True or False:
            If it was able to find the button
    """
    xpaths = [
        "Accede al test",
        "Continuar test",
        "Reintentar test",
    ]
    for xp in xpaths:

        try:
            automation.wait_and_click(By.XPATH, f"//button[text()='{xp}']",timeout/10)
            return True  # Found, exit loop

        except TimeoutException: continue  # Try next XPath
    
    raise Exception("No se encontró ningún botón de test clickeable")
    return False # Useless actually

def get_tests(automation:"WebAutomation", timeout:int = 10) -> list:
    """
    Function to find the url of the tests to do
        automation -> Selenium driver:
            Selenium's WebAutomation instance,

        timeout -> int, 10:
            Time to wait for elements to load,
            
        returns -> list, ["https://...", "https://...", ...]:
            The links to the tests to do
    """
    automation.find_element(By.CLASS_NAME, "activities-list", timeout)

    tests_links = automation.driver.find_elements(By.CSS_SELECTOR, ".activity-carditem[data-component='quiz'] a.stretched-link")

    return [link.get_attribute("href") for link in tests_links]

def get_num_questions(automation:"WebAutomation", timeout:int = 10) -> int:
    """
    Function to find the number of questions in a test
        automation -> Selenium driver:
            Selenium's WebAutomation instance,

        timeout -> int, 10:
            Time to wait for elements to load,
            
        returns -> int, 30:
            The amount of questions a test has
    """
    driver = getattr(automation, "driver", automation)
    WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.que")))

    try: return len(driver.find_elements(By.CSS_SELECTOR, "div.que"))

    except Exception as e:
        print(f"\033[91m[!] Error getting the number of questions\033[0m")

        return -1

def get_num_options(wrapper_or_driver:"WebAutomation", question_indx:int, timeout:int = 10) -> int:
    """
    Function to find the number of answers in a question
        wrapper_or_driver -> Selenium driver:
            Selenium's WebAutomation instance,
        
        question_indx -> int, 1:
            The index of the question to retrieve data from,

        timeout -> int, 10:
            Time to wait for elements to load,
            
        returns -> int, 30:
            The amount of answers a question has
    """
    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    pregunta = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'que')][.//span[@class='qno' and text()='{question_indx}']]")))
    
    try: 
        num_options = len(pregunta.find_elements(By.CSS_SELECTOR, "div.answer input[type='radio'][name$='answer']"))

        if num_options > 0: return num_options
        elif num_options == 0:

            try: return len(pregunta.find_elements(By.CSS_SELECTOR, "div.answer input[type='checkbox'][name*='_choice']"))
                
            except Exception as e:
                print(f"\033[33m[!] Error getting answer options from multi-choice question #{question_indx}: {e}\033[0m")

                return -1

    except Exception as e: print(f"\033[33m[!] Error getting answer options from question #{question_indx}: {e}\nSearching as multi-choice\033[0m")

def solve_question(
    wrapper_or_driver:"WebAutomation",
    question_indx:int,
    answers:Union[int, list, None] = None,
    timeout:int = 10,
    DEBUGGING:bool = False
    ) -> bool:
    """
    Function to solve the question of a test
        wrapper_or_driver -> Selenium driver:
            Selenium's WebAutomation instance,

        question_indx -> int, 3:
            The index of the question to solve,

        timeout -> int, 10:
            Time to wait for elements to load,
        
        answers -> int or list, 1 or [1, 0, 0, 2, 3]:
            The next set of answers to try,

        DEBUGGING -> bool, True or False:
            Show debugging logs or not,
            
        returns -> bool, True or False:
            If it was succesful solving the question
    """
    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    pregunta = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'que')][.//span[@class='qno' and text()='{question_indx}']]")))
    driver.execute_script("arguments[0].scrollIntoView();", pregunta)

    try:
        pregunta.find_element(By.CSS_SELECTOR, f"input[type='radio'][value='{answers}']").click()
        return True

    except Exception as e:
        if DEBUGGING: print(f"\033[33m[?] Error solving question #{question_indx}: {e}\nTrying multi-choice\033[0m")
        return False

def solve_multiple_choice(
    wrapper_or_driver:"WebAutomation",
    question_indx:int,
    answers:Union[int, list, None] = None,
    timeout:int = 10
    ) -> bool:
    """
    Function to solve the multi-choice question of a test
        wrapper_or_driver -> Selenium driver:
            Selenium's WebAutomation instance,

        question_indx -> int, 3:
            The index of the question to solve,

        timeout -> int, 10:
            Time to wait for elements to load,

        answers -> int or list, 1 or [[1, 0, 0], 0, 0, 2, 3]:
            The next set of answers to try,

        returns -> bool, True or False:
            If it was succesful solving the multi-choice question
    """
    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    pregunta = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'que')][.//span[@class='qno' and text()='{question_indx}']]")))
    driver.execute_script("arguments[0].scrollIntoView();", pregunta)

    try:
        num_answers = get_num_options(wrapper_or_driver, question_indx=question_indx, timeout=10)
        if isinstance(answers, int): answers = [_ for _ in range(num_answers)]

        for answer in answers:
            try:
                option = pregunta.find_element(By.CSS_SELECTOR, f"div.answer input[type='checkbox'][name*='{question_indx}_choice{answer}']")
                driver.execute_script("arguments[0].scrollIntoView(true);", option)

                option.click()

            except Exception as e: 
                option = pregunta.find_element(By.CSS_SELECTOR, f"div.answer input[type='checkbox'][name*='{question_indx}_choice{answer}']")
                driver.execute_script("arguments[0].scrollIntoView(true);", option)
                
                driver.execute_script("arguments[0].click();", option)
                print(f"\033[33m[!] Question #{question_indx} is wrong, no correct solution\033[0m")

        return True

    except Exception as e:
        print(f"\033[91m[!] Error solving multi-choice question #{question_indx}: {e}\033[0m")

        return False

def handle_finishing_buttons(
    wrapper_or_driver:"WebAutomation",
    question_indx:int,
    timeout:int = 10,
    DEBUGGING:bool = False
    ) -> bool:
    """
    Function to find and click the submitting buttons of a test
        wrapper_or_driver -> Selenium driver:
            Selenium's WebAutomation instance,

        question_indx -> int, 3:
            The index of the question to solve,

        timeout -> int, 10:
            Time to wait for elements to load,

        DEBUGGING -> bool, True or false:
            Show debugging logs or not,
            
        returns -> bool, True or False:
            If it was succesful handling the finishing buttons
    """

    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    
    try:
        # Submit test
        if DEBUGGING: print(f"[DEBUGGING] Submitting test...")
        submit_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="mod_quiz-next-nav"]')))

        submit_button.click()

        # Send test
        if DEBUGGING: print(f"[DEBUGGING] Sending test...")
        finish_form = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "frm-finishattempt")))

        send_button = finish_form.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
        driver.execute_script("arguments[0].scrollIntoView();", send_button)

        send_button.click()

        # Annoying pop-up
        if DEBUGGING: print(f"[DEBUGGING] Handling pop-up...")
        for i in range(10):
            try:
                popUp_button = WebDriverWait(driver, timeout/3).until(
                    EC.element_to_be_clickable((By.XPATH, f'//*[@id="{i}"]/div/div/div[3]/button[2]')))
                driver.execute_script("arguments[0].scrollIntoView();", popUp_button)

                popUp_button.click()

                if DEBUGGING: print(f"[DEBUGGING] Pop-up handled on attempt {i}")

                break
            except TimeoutException: continue
        
        return True

    except Exception as e:
        print(f"\033[91m[!] Error handling finishing buttons in test #{question_indx}\033[0m")
        
        return False

def solve_test(
    wrapper_or_driver:"WebAutomation",
    answers:Union[int, list, None] = None,
    timeout:int = 10,
    DEBUGGING:bool = False
    ) -> int:
    """
    Function to solve the multi-choice question of a test
        wrapper_or_driver -> Selenium driver:
            Selenium's WebAutomation instance,

        timeout -> int, 10:
            Time to wait for elements to load,

        answers -> int or list, 1 or [1, 0, 0, 2, 3]:
            The next set of answers to try,

        DEBUGGING -> bool, True or false:
            Show debugging logs or not,
            
        returns -> int, 30:
            The mark after completing a test
    """
    num_questions = get_num_questions(wrapper_or_driver, timeout)
    if isinstance(answers, int): answer = answers

    for i in range(num_questions):

        try:
            num_options = get_num_options(wrapper_or_driver, i+1)

            if DEBUGGING: print(f"[DEBUGGING] Question #{i+1}/{num_questions} has {num_options}")
            
            if isinstance(answers, list):
                if isinstance(answers[i], list): answer = answers[i]
                elif isinstance(answers[i], int): answer = answers[i] - 1

            if DEBUGGING: print(f"[DEBUGGING] Answering with {answer}, from {type(answers)} variable")
            if not isinstance(answer, list):

                if answer > num_options:
                        answer = answers_options
                        print(f"\033[91m[!] Not enough options in question #{i+1}, selecting last option instead of {answer}\033[0m")

            if not solve_question(wrapper_or_driver=wrapper_or_driver, question_indx=i+1, answers=answer, timeout=timeout, DEBUGGING=DEBUGGING):

                if DEBUGGING: print(f"\033[33m[?] Exception, missing answer box in question #{i+1}\nSolving as multiple choice\033[0m")
                solve_multiple_choice(wrapper_or_driver=wrapper_or_driver, question_indx=i+1, answers=answer, timeout=timeout)

        except Exception as e:
            print(f"\033[91m[!] Error in question #{i+1}, not single nor multi-choice question: {e}\033[0m")
        
    handle_finishing_buttons(wrapper_or_driver, i+1, timeout, DEBUGGING)

    return find_mark(wrapper_or_driver, timeout)

def read_answers(wrapper_or_driver:"WebAutomation", timeout:int=10) -> dict:
    """
    Function to read the solutions of a test
        wrapper_or_driver -> Selenium driver:
            Selenium's WebAutomation instance,

        timeout -> int, 10:
            Time to wait for elements to load,
            
        returns -> dict, {1: 1, 2: 0...}:
            The answers of each question; if correct, the last tried answer, otherwise, 0
    """
    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    results = {}

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.que")))
    
    questions = driver.find_elements(By.CSS_SELECTOR, "div.que")
    
    for question in questions:

        try:
            q_number = int(question.find_element(By.CSS_SELECTOR, "h3.no span.qno").text)
            
            # Detectar si es múltiple o única
            is_multiple = len(question.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")) > 0
            
            # Buscar todas las opciones de respuesta
            answer_divs = question.find_elements(By.CSS_SELECTOR, "div.answer > div[class^='r']")
            
            correct_indices = []
            
            for idx, answer_div in enumerate(answer_divs):
                # Buscar imagen con alt="Correcta" o title="Correcta"
                icons = answer_div.find_elements(By.CSS_SELECTOR, "img.icon")

                for icon in icons:

                    if icon.get_attribute("alt") == "Correcta" or icon.get_attribute("title") == "Correcta":
                        if not is_multiple: idx=1
                        correct_indices.append(idx)
                        break
            
            if is_multiple: results[q_number] = correct_indices  # Lista para múltiple
            else: results[q_number] = correct_indices[0] if correct_indices else 0  # Índice único
                
        except Exception as e:
            print(f"\033[91m[!] Error en pregunta: {e}\033[0m")
            continue
    
    finish_revision = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="region-main"]/div[2]/div/a')))

    finish_revision.click()

    return results

if __name__ == "__main__":
    pass