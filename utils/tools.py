try: from utils import args as arg
except ImportError: import args as arg

def beep_sound() -> None:
    import winsound
    frequency = 3000  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

def is_element(element: str, automation) -> bool:
    html = automation.get_page_source()
    return element in html

class ASCII_ART:

    def title() -> None:
        
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

    args = arg.parse_args()
    
    config = {}
    
    if args.username is None or args.password is None: config["AUTOMATED_LOGIN"] = False
    if args.username: config["UNIR_USERNAME"] = args.username
    if args.password: config["UNIR_PASSWORD"] = args.password
    if args.courses: config["UNIR_COURSES"] = args.courses
    if args.example:

        print('\033[33m[?] python main.py --username tu@correo.com --password contraseña1234 --courses 1234,1235,1234\033[0m')
        exit(0)

    return config

def swap_errors_with(original_list: list, new_value: int) -> list:
    
    new_list = []

    for value in original_list:
        if value == 0: new_list.append(new_value)
        else: new_list.append(value)

    return new_list

def dict_to_list(dictionary: dict) -> list:

    new_list = []
    
    for key, value in dictionary.items(): new_list.append(value)
    
    return new_list

def combinate_answers(original_answers: list, binary_answers: list) -> list:
    
    combined = []

    for i in range(len(original_answers)):
        if isinstance(original_answers[i], list) and isinstance(binary_answers[i], list): combined.append(original_answers[i])
        else: combined.append(original_answers[i] * binary_answers[i])
    
    return combined
    
if __name__ == "__main__":
    print(combinate_answers([2, 1, 2, 2, 1, 2, 2, 1, [0, 1], 2], [0, 1, 0, 0, 1, 0, 0, 1, [0, 1], 0]))