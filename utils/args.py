import argparse

def parse_args() -> argparse.Namespace:

    p = argparse.ArgumentParser(description="Herramienta para completar los tests UNIR de forma automática")
    
    p.add_argument("--username", type=str, help="El email de tu cuenta UNIR")
    p.add_argument("--password", type=str, help="La contraseña de tu cuenta UNIR")
    p.add_argument("--courses", type=str, help="De que curso o cursos quieres hacer los tests. NOMBRES EXACTOS A LOS DE LA WEB")
    p.add_argument("--example", action="store_true", help="Este comando te da un ejemplo de como usar la herramienta")

    return p.parse_args()