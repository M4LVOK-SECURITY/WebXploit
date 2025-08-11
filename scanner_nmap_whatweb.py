# scanner_nmap_whatweb.py

import subprocess
import shutil
import os
import sys

# Verifica si Nmap está instalado
def verificar_nmap():
    return shutil.which("nmap") is not None

# Verifica si WhatWeb está instalado
def verificar_whatweb():
    return shutil.which("whatweb") is not None

def escanear_con_nmap(dominio, opciones="-sV --top-ports 100", verbose=True):
    """
    Ejecuta un escaneo Nmap sobre el dominio o IP dada.
    :param dominio: IP o dominio objetivo
    :param opciones: Opciones Nmap (ej: -sV -O)
    :param verbose: Muestra la salida en consola
    :return: Resultado como string
    """
    if not verificar_nmap():
        print("[X] Nmap no está instalado o no está en el PATH.")
        return ""

    print(f"[+] Ejecutando Nmap sobre {dominio} con opciones: {opciones}")
    try:
        resultado = subprocess.run(
            ["nmap"] + opciones.split() + [dominio],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if verbose:
            print(resultado.stdout)
        return resultado.stdout
    except Exception as e:
        print(f"[X] Error al ejecutar Nmap: {e}")
        return ""

def escanear_con_whatweb(url, verbose=True):
    """
    Ejecuta WhatWeb sobre un sitio web para detectar tecnologías.
    :param url: URL objetivo (ej: https://ejemplo.com)
    :param verbose: Mostrar salida
    :return: Resultado como string
    """
    if not verificar_whatweb():
        print("[X] WhatWeb no está instalado o no está en el PATH.")
        return ""

    print(f"[+] Ejecutando WhatWeb sobre: {url}")
    try:
        resultado = subprocess.run(
            ["whatweb", "--no-errors", "--color=never", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if verbose:
            print(resultado.stdout)
        return resultado.stdout
    except Exception as e:
        print(f"[X] Error al ejecutar WhatWeb: {e}")
        return ""

# Uso independiente para pruebas
if __name__ == "__main__":
    objetivo = input("Dominio o IP a escanear: ").strip()
    modo = input("¿Qué quieres ejecutar? (nmap/whatweb/ambos): ").strip().lower()

    if modo in ["nmap", "ambos"]:
        escanear_con_nmap(objetivo)

    if modo in ["whatweb", "ambos"]:
        escanear_con_whatweb(f"https://{objetivo}")
