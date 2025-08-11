# argument_handler.py

import argparse

def obtener_argumentos():
    """
    Parsea los argumentos de línea de comandos usando argparse.
    Devuelve un diccionario con las opciones para usar en otros módulos.
    """
    parser = argparse.ArgumentParser(
        description="Herramienta ofensiva de ciberseguridad M4 – Análisis Web"
    )

    parser.add_argument("url", help="URL del sitio objetivo (ej: https://example.com)")
    parser.add_argument("--stealth", action="store_true", help="Modo sigiloso (delay + headers aleatorios)")
    parser.add_argument("--verbose", action="store_true", help="Modo detallado (muestra toda la salida)")
    parser.add_argument("--reporte", action="store_true", help="Generar reporte HTML/TXT al finalizar")
    parser.add_argument("--auth", choices=["jwt", "basic", "cookie"], help="Tipo de autenticación a usar")
    parser.add_argument("--token", help="Token JWT o credencial para autenticación")
    parser.add_argument("--wordlist", help="Ruta personalizada a wordlist", default="subdomains.txt")

    return parser.parse_args()
