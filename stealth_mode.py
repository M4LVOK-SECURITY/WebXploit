# stealth_mode.py

import random
import time

# Lista de headers falsos para simular tráfico humano
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6)...',
    'Mozilla/5.0 (Linux; Android 10; Pixel 4 XL)...',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0)...',
    'Mozilla/5.0 (X11; Linux x86_64)...',
]

REFERERS = [
    'https://www.google.com/',
    'https://www.bing.com/',
    'https://www.reddit.com/',
    'https://news.ycombinator.com/',
    'https://duckduckgo.com/',
]

ACCEPT_ENCODINGS = ['gzip, deflate', 'identity', 'br']

def generar_headers_sigilosos():
    """
    Crea un diccionario de headers HTTP que simulan tráfico humano.
    """
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": random.choice(REFERERS),
        "Accept-Encoding": random.choice(ACCEPT_ENCODINGS),
        "Accept-Language": "en-US,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",  # Do Not Track
    }

def aplicar_delay_sigiloso(min_delay=1.0, max_delay=4.0, verbose=False):
    """
    Aplica un delay aleatorio entre cada solicitud (modo stealth).
    """
    delay = round(random.uniform(min_delay, max_delay), 2)
    if verbose:
        print(f"[STEALTH] Durmiendo {delay} segundos para evadir detección...")
    time.sleep(delay)

# Ejemplo de integración simple
if __name__ == "__main__":
    for _ in range(5):
        headers = generar_headers_sigilosos()
        aplicar_delay_sigiloso(verbose=True)
        print(headers)
