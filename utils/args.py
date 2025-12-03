import argparse

def parse_args() -> argparse.Namespace:

    p = argparse.ArgumentParser(description="Herramienta para completar los tests UNIR de forma automática")
    
    p.add_argument("--username", type=str, help="El email de tu cuenta UNIR")
    p.add_argument("--password", type=str, help="La contraseña de tu cuenta UNIR")
    p.add_argument("--courses", type=str, help="De que curso o cursos quieres hacer los tests. NOMBRES EXACTOS A LOS DE LA WEB")
    p.add_argument("--max-tests", type=int, default=15, help="El número máximo de tests a completar por curso (opcional, por defecto 15)")
    p.add_argument("--target-url", type=str, default="https://campusonline.unir.net/my", help="La URL a la que tiene que ir de primeras el bot (opcional)")
    p.add_argument("--menu-xpath", type=str, default='//*[@id="theme_boost-drawers-primarymoremenu"]/div[2]/div/nav/ul', help="La dirección xPath del menu de los cursos (opcional)")
    p.add_argument("--example", action="store_true", help="Este comando te da un ejemplo de como usar la herramienta")

    return p.parse_args()