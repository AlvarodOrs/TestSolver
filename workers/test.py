from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def find_mark(wrapper_or_driver, timeout:int=10) -> int:

    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    mark_box = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//tr[th[normalize-space()='Calificación']]/td")))
    
    import re
    match = re.search(r"\d+\s*%", mark_box.text)

    try: return match.group()
    except Exception as e:
        print(f"\033[91m[!] Error finding mark\033[0m")
        return -1

def find_test_button(wrapper_or_driver, timeout:int=10) -> bool:

    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    xpaths = [
        "Accede al test",
        "Continuar test",
        "Reintentar test",
    ]
    
    boton = None
    for xp in xpaths:
        try:
            boton = WebDriverWait(driver, timeout/10).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[text()='{xp}']"))
            )
            break  # lo encontró, salir del loop
        except TimeoutException:
            continue  # probar siguiente XPath
    
    if boton: 
        boton.click()
        return True
    else:
        raise Exception("No se encontró ningún botón de test clickeable")
        return False

def get_tests(wrapper_or_driver, timeout:int=10) -> list:
    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, "activities-list"))
    )

    tests_links = driver.find_elements(By.CSS_SELECTOR,
        ".activity-carditem[data-component='quiz'] a.stretched-link")
    return [link.get_attribute("href") for link in tests_links]

def get_num_questions(wrapper_or_driver, timeout:int=10) -> int:

    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.que")))

    try: return len(driver.find_elements(By.CSS_SELECTOR, "div.que"))

    except Exception as e:
        print(f"\033[91m[!] Error getting the number of questions\033[0m")
        return -1

def get_num_options(wrapper_or_driver, question_indx:int, timeout:int=10) -> int:

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

    except Exception as e:
        print(f"\033[33m[!] Error getting answer options from question #{question_indx}: {e}\nSearching as multi-choice\033[0m")


def solve_question(wrapper_or_driver, question_indx:int, timeout:int=10, answers=None, DEBUGGING:bool=False) -> bool:
    
    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    pregunta = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'que')][.//span[@class='qno' and text()='{question_indx}']]")))
    driver.execute_script("arguments[0].scrollIntoView();", pregunta)

    try:
        pregunta.find_element(By.CSS_SELECTOR, f"input[type='radio'][value='{answers}']").click()
        return True

    except Exception as e:
        if DEBUGGING: print(f"\033[33m[?] Error solving question #{question_indx}: {e}\Trying multi-choice\033[0m")
        return False

def solve_multiple_choice(wrapper_or_driver, question_indx:int, timeout:int=10, answers=None) -> bool:
    
    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    pregunta = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'que')][.//span[@class='qno' and text()='{question_indx}']]")))
    driver.execute_script("arguments[0].scrollIntoView();", pregunta)
    try:
        num_answers = get_num_options(wrapper_or_driver, question_indx=question_indx, timeout=10)
        if isinstance(answers, int): answers = [_ for _ in range(num_answers)]
        for answer in answers:
            try:
                option = pregunta.find_element(By.CSS_SELECTOR,
                    f"div.answer input[type='checkbox'][name*='{question_indx}_choice{answer}']")
                driver.execute_script("arguments[0].scrollIntoView(true);", option)
                option.click()
            except Exception as e: 
                option = pregunta.find_element(By.CSS_SELECTOR,
                    f"div.answer input[type='checkbox'][name*='{question_indx}_choice{answer}']")
                driver.execute_script("arguments[0].scrollIntoView(true);", option)
                driver.execute_script("arguments[0].click();", option)
                print(f"\033[33m[!] Question #{question_indx} is wrong, no correct solution\033[0m")
        return True

    except Exception as e:
        print(f"\033[91m[!] Error solving multi-choice question #{question_indx}: {e}\033[0m")
        return False

def handle_finishing_buttons(wrapper_or_driver, question_indx:int, timeout:int=10, DEBUGGING:bool=False) -> bool:
    
    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    
    try:
        # Submit test
        if DEBUGGING: print(f"[DEBUGGING] Submitting test...")
        submit_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="mod_quiz-next-nav"]'))
        )
        submit_button.click()

        # Send test
        if DEBUGGING: print(f"[DEBUGGING] Sending test...")
        finish_form = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "frm-finishattempt"))
        )
        send_button = finish_form.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
        driver.execute_script("arguments[0].scrollIntoView();", send_button)
        send_button.click()

        # Annoying pop-up
        if DEBUGGING: print(f"[DEBUGGING] Handling pop-up...")
        for i in range(10):
            try:
                popUp_button = WebDriverWait(driver, timeout/3).until(
                    EC.element_to_be_clickable((By.XPATH, f'//*[@id="{i}"]/div/div/div[3]/button[2]'))
                )
                driver.execute_script("arguments[0].scrollIntoView();", popUp_button)
                popUp_button.click()
                if DEBUGGING: print(f"[DEBUGGING] Pop-up handled on attempt {i}")
                break
            except TimeoutException:
                continue
    except Exception as e:
        print(f"\033[91m[!] Error handling finishing buttons in test #{question_indx}\033[0m")

def solve_test(wrapper_or_driver, timeout:int=10, answers=None, DEBUGGING:bool=False) -> int:
    
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

            if not solve_question(wrapper_or_driver, i+1, timeout, answer, DEBUGGING):
                if DEBUGGING: print(f"\033[33m[?] Exception, missing answer box in question #{i+1}\nSolving as multiple choice\033[0m")
                solve_multiple_choice(wrapper_or_driver, i+1, timeout, answer)
        except Exception as e:
            print(f"\033[91m[!] Error in question #{i+1}, not single nor multi-choice question: {e}\033[0m")
        
    handle_finishing_buttons(wrapper_or_driver, i+1, timeout, DEBUGGING)

    return find_mark(wrapper_or_driver, timeout)

def read_answers(wrapper_or_driver, timeout:int=10):
    
    driver = getattr(wrapper_or_driver, "driver", wrapper_or_driver)
    results = {}

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.que"))
    )
    
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
        EC.element_to_be_clickable((By.XPATH, '//*[@id="region-main"]/div[2]/div/a'))
    )
    finish_revision.click()
    return results

if __name__ == "__main__":
    pass