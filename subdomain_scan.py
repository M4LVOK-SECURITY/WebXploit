# subdomain_scan.py

import socket
import tldextract
import os
import sys

# Verifica si tldextract está instalado, si no, lo instala
try:
    import tldextract
except ImportError:
    print("[!] 'tldextract' no instalado. Instalando automáticamente...")
    os.system(f"{sys.executable} -m pip install tldextract")

def subdomain_scan(domain, wordlist_path="subdomains.txt", verbose=False):
    """
    Escanea posibles subdominios del dominio dado, usando una wordlist.
    Si el subdominio existe, se resuelve la IP.
    :param domain: Dominio objetivo (ej: ejemplo.com)
    :param wordlist_path: Ruta de la lista de subdominios (una por línea)
    :param verbose: Modo detallado (True/False)
    """
    try:
        with open(wordlist_path, 'r') as file:
            subdomains = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] Wordlist no encontrada: {wordlist_path}")
        return

    root_domain = tldextract.extract(domain)
    base_domain = f"{root_domain.domain}.{root_domain.suffix}"

    print(f"\n[+] Escaneando subdominios para: {base_domain}")

    for sub in subdomains:
        full_domain = f"{sub}.{base_domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            print(f"[VALIDO] {full_domain} → {ip}")
        except socket.gaierror:
            if verbose:
                print(f"[X] {full_domain} no resuelve")

# Ejemplo de ejecución directa
if __name__ == "__main__":
    objetivo = input("Dominio objetivo (ejemplo.com): ").strip()
    wordlist = input("Ruta de wordlist [subdomains.txt]: ").strip() or "subdomains.txt"
    modo_verboso = input("¿Modo verbose? (s/n): ").lower() == 's'
    subdomain_scan(objetivo, wordlist, verbose=modo_verboso)
