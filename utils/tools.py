try: from utils import args as arg
except ImportError: import args as arg
import winsound
import json

def beep_sound(frequency:int = 3000, duration:int = 1000) -> None:
    """
    Simple sound maker to notify user when the bot is done
    """
    winsound.Beep(frequency, duration)

class ASCII_ART:
    """
    Simple class function to print ASCII art on the terminal, works better in ANSI code supporting terminals (for the text formatting code)
    """
    def title() -> None:
        """
        Prints the program "logo"
        """
        print("\033[95m\n+=======================================+")
        print(r"|   _   _ _   _ ___________             |")
        print(r"|  | | | | \ | |_   _| ___ \            |")
        print(r"|  | | | |  \| | | | | |_/ /            |")
        print(r"|  | | | | . ` | | | |    /             |")
        print(r"|  | |_| | |\  |_| |_| |\ \             |")
        print(r"|   \___/\_| \_/\___/\_| \_|            |")
        print(r"|                                       |")
        print(r"|                                       |")
        print(r"|   _____         _  ______       _     |")
        print(r"|  |_   _|       | | | ___ \     | |    |")
        print(r"|    | | ___  ___| |_| |_/ / ___ | |_   |")
        print(r"|    | |/ _ \/ __| __| ___ \/ _ \| __|  |")
        print(r"|    | |  __/\__ \ |_| |_/ / (_) | |_   |")
        print(r"|    \_/\___||___/\__\____/ \___/ \__|  |")
        print(r"|                                       |")
        print("+=======================================+\n")
        print("By Álvaro d'Ors Nestares\033[0m\n\n")

def setup_config() -> dict:
    """
    Sets up the program variables:
        USERNAME -> str, your@unir.email:
            Bot will use this as your valid UNIR/Moodle email,
        
        PASSWORD -> str, yourpassword:
            Bot will use this as your valid UNIR/Moodle password,
        
        COURSES -> str (of integers), COURSE1,COURSE2...:
            Bot will use those as the desired tests to complete,
        
        LOGIN_URL -> str, https://your.desired.moodle/login/page:  (default, UNIR's one)
            Bot will use this for the login process,

        returns -> dict, {"USERNAME": "your@desired.email", "PASSWORD": "yourPassword", ...}
            The bot configuration parameters
    """
    def _config(filepath:str = 'config.json') -> list:
        config = {}
        with open(filepath, 'r') as file: data = json.load(file)
        for parameter in data: config[parameter] = data[parameter] 
        return config

    args = arg.parse_args() 
    config = _config()
    
    # Updating config
    if args.timeout: config["timeout"] = args.timeout
    if args.debug: config["debug"] = args.debug
    if args.example:
        print('\033[33m[?] python main.py --timeout 10 --debug False\033[0m')
        exit(0)
    return config

def swap_errors_with(original_list:list, new_value:int) -> list:
    """
    Function to overwrite the test incorrect answers with the next desired option:
        original_list -> list, [1, 0, 0, 2, 3]:
            A list containing the last tried answers with 0 for the incorrect solutions,
        
        new_value -> int, 1 for A, 2 for B, 3 for C...:
            The next value to try as an answer,
        
        returns -> list, [1, 4, 4, 2, 3]:
            The original_list with the next value for each 0 (aka, wrong answers)
    """
    new_list = []

    for value in original_list:
        if value == 0: new_list.append(new_value)
        else: new_list.append(value)

    return new_list

def dict_to_list(dictionary:dict) -> list:
    """
    Transforms a dictionary (from test.read_answers()) to a usable list:
        dictionary -> dict, {1: 1, 2: 0, 3: 0, 4: 2, 5: 3}:
            The results after reading test's correction (with 0 for each wrong answer),
        
        returns -> list, [1, 0, 0, 2, 3]:
            The desired dictionary as a list, where the index of a solution is the number of the question
    """
    new_list = []
    
    for key, value in dictionary.items(): new_list.append(value)
    
    return new_list

def combinate_answers(original_answers:list, binary_answers:list) -> list:
    """
    Simple vectorial multiplication:
        original_answers -> list, [1, 3, 3, 2, 3]:
            The list of the last tried answers,

        binary_answers -> list, [1, 0, 0, 1, 1]:
            The list correct or incorrect questions,
        
        returns -> list, [1, 0, 0, 2, 3]:
            The list of the correct answers
    """
    combined = []

    for i in range(len(original_answers)):
        if isinstance(original_answers[i], list) and isinstance(binary_answers[i], list): combined.append(original_answers[i])
        else: combined.append(original_answers[i] * binary_answers[i])
    
    return combined
    
if __name__ == "__main__":
    pass