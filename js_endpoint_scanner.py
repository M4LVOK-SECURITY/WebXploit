# js_endpoint_scanner.py

import os
import sys
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from stealth_mode import generar_headers_sigilosos  # ✅ Importamos headers stealth

# Lista de patrones típicos que podríamos querer encontrar
ENDPOINT_PATTERNS = [
    r"/api/\w+",
    r"/auth/\w+",
    r"/v1/\w+",
    r"/users/\w+",
    r"/admin/\w+",
    r"/wp-json/\w+",
    r"[A-Za-z0-9_-]{10,}\.(php|asp|aspx|jsp)",
    r"[A-Za-z0-9_-]{16,}\.(js|json)",
    r"[A-Za-z0-9]{20,}",  # posibles tokens, claves
]

def analizar_js_scripts(url, verbose=False):
    """
    Extrae y analiza scripts JS de una página en busca de endpoints, rutas o claves sospechosas.
    :param url: Página objetivo
    :param verbose: Si True, muestra todos los scripts externos encontrados
    """
    print(f"\n[+] Analizando scripts JS en: {url}")
    headers = generar_headers_sigilosos()

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[X] Error al acceder a la página: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')

    encontrados = []

    for script in scripts:
        src = script.get('src')
        if src:
            full_url = urljoin(url, src)
            try:
                r = requests.get(full_url, headers=headers, timeout=10)
                if r.status_code == 200:
                    contenido = r.text
                    if verbose:
                        print(f"[✓] Analizando script: {full_url}")
                    encontrados += buscar_patrones(contenido, full_url)
            except Exception as e:
                print(f"[!] Error al descargar JS externo: {full_url} → {e}")
        else:
            contenido = script.string
            if contenido:
                encontrados += buscar_patrones(contenido, f"{url} (embebido)")

    if encontrados:
        print(f"\n[✓] Patrones sospechosos encontrados:")
        for item in encontrados:
            print(f" ↳ {item}")
    else:
        print("[!] No se encontraron endpoints sospechosos.")

    return encontrados

def buscar_patrones(contenido, fuente):
    """
    Busca los patrones definidos en un bloque de texto.
    :param contenido: Texto del JS
    :param fuente: URL o contexto donde se encontró
    :return: Lista de coincidencias encontradas
    """
    hallazgos = []
    for patron in ENDPOINT_PATTERNS:
        coincidencias = re.findall(patron, contenido)
        for match in coincidencias:
            hallazgos.append(f"{match} (en: {fuente})")
    return hallazgos

# Uso independiente
if __name__ == "__main__":
    objetivo = input("URL del sitio a escanear (ej: https://ejemplo.com): ").strip()
    verbose = input("¿Mostrar todos los scripts? (s/n): ").lower().startswith('s')
    analizar_js_scripts(objetivo, verbose=verbose)
