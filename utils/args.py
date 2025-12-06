import argparse

def parse_args() -> argparse.Namespace:
    """
    Simple argument parser to initialize the bot
    Might be extrapolated to all Moodle courses
    """
    p = argparse.ArgumentParser(description="Herramienta para completar los tests de UNIR/Moodle de forma automática")
    
    p.add_argument("--username", type=str, help="El email de tu cuenta de UNIR/Moodle")
    p.add_argument("--password", type=str, help="La contraseña de tu cuenta UNIR/Moodle")
    p.add_argument("--courses", type=str, help="Las materias de las que quieres hacer los tests. NUMEROS EXTRAIDOS DE LA WEB")
    # The two following might be used to adapt the bot for other Moodle courses
    p.add_argument("--target-url", type=str, default="https://campusonline.unir.net/my",
    help="Link de login de UNIR/Moodle (UNIR por defecto)")
    p.add_argument("--courses-url", type=str, default="https://campusonline.unir.net/mod/url/view.php?id=",
    help="Link general de cada curso de UNIR/Moodle (UNIR por defecto)")
    p.add_argument("--example", action="store_true", help="Este comando te da un ejemplo de como usar la herramienta")

    return p.parse_args()