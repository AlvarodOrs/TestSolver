import argparse

def parse_args() -> argparse.Namespace:
    """
    Simple argument parser to initialize the bot
    Might be extrapolated to all Moodle courses
    """
    p = argparse.ArgumentParser(description="Herramienta para completar los tests de UNIR/Moodle de forma automática")
    
    p.add_argument("--timeout", type=int, default=10, help="Tiempo maximo de esperar a cargar un elemento web")
    p.add_argument("--debug", type=bool, default=False, help="Mostrar debugging o no")
    p.add_argument("--example", action="store_true", help="Este comando te da un ejemplo de como usar la herramienta")

    return p.parse_args()