import requests
import platform
import socket
from bs4 import BeautifulSoup
import os
import psutil
import getpass
from colorama import Fore, Style
from urllib.parse import urljoin, urlparse
import ssl
import tldextract
import whois
import nmap
from stealth_mode import generar_headers_sigilosos  # ✅ NUEVO

# Usaremos estos headers para todas las solicitudes
HEADERS_STEALTH = generar_headers_sigilosos()

def getsysteminfo(url):
    print(f"{Fore.CYAN}[+] Obteniendo información avanzada del sitio web: {url}{Style.RESET_ALL}")

    try:
        response = requests.get(url, headers=HEADERS_STEALTH, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Error al acceder al sitio: {e}{Style.RESET_ALL}")
        return

    try:
        beauti = BeautifulSoup(response.text, 'html.parser')
        title = beauti.title.string.strip() if beauti.title and beauti.title.string else "No disponible"
        domain = tldextract.extract(url)
        hostname = domain.domain + '.' + domain.suffix
        parsed_url = urlparse(url)

        print(f"{Fore.GREEN}Título:{Style.RESET_ALL} {title}")
        print(f"{Fore.GREEN}Dominio principal:{Style.RESET_ALL} {hostname}")
        print(f"{Fore.GREEN}Ruta de acceso:{Style.RESET_ALL} {parsed_url.path}")
        print(f"{Fore.GREEN}Protocolo usado:{Style.RESET_ALL} {parsed_url.scheme}")
        print(f"{Fore.GREEN}Cabeceras HTTP:{Style.RESET_ALL}")
        for key, value in response.headers.items():
            print(f"  {Fore.YELLOW}{key}:{Style.RESET_ALL} {value}")

        techs = []
        if 'X-Powered-By' in response.headers:
            techs.append(response.headers['X-Powered-By'])
        if beauti.find("meta", attrs={"name": "generator"}):
            techs.append(beauti.find("meta", attrs={"name": "generator"}).get("content", ""))

        if techs:
            print(f"{Fore.BLUE}Tecnologías detectadas:{Style.RESET_ALL} {', '.join(techs)}")
        else:
            print(f"{Fore.YELLOW}No se detectaron tecnologías explícitas.{Style.RESET_ALL}")

        try:
            whoisdata = whois.whois(hostname)
            print(f"{Fore.GREEN}Información WHOIS:{Style.RESET_ALL}")
            for key, value in whoisdata.items():
                print(f"  {Fore.YELLOW}{key}:{Style.RESET_ALL} {value}")
        except Exception as e:
            print(f"{Fore.RED}[!] No se pudo obtener la información WHOIS: {e}{Style.RESET_ALL}")

        cdn = None
        if 'cf-ray' in response.headers:
            cdn = 'Cloudflare'
        elif 'akamai' in response.headers:
            cdn = 'Akamai'

        if cdn:
            print(f"{Fore.GREEN}CDN detectado:{Style.RESET_ALL} {cdn}")
        else:
            print(f"{Fore.YELLOW}No se detectó CDN.{Style.RESET_ALL}")

        try:
            ip = socket.gethostbyname(hostname)
            print(f"{Fore.GREEN}IP del servidor:{Style.RESET_ALL} {ip}")
        except Exception:
            print(f"{Fore.RED}[!] No se pudo obtener la IP del dominio.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[!] Error al procesar la página web: {e}{Style.RESET_ALL}")


def getwebsiteinfo(url):
    print(f"{Fore.CYAN}[*] Analizando: {url}{Style.RESET_ALL}")

    try:
        response = requests.get(url, headers=HEADERS_STEALTH, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Error al intentar acceder a la página: {e}{Style.RESET_ALL}")
        return

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        headers = response.headers
        technologies = []
        js_files = []
        links = []

        title = soup.title.string.strip() if soup.title and soup.title.string else "No se pudo obtener el título"
        print(f"{Fore.GREEN}[+] Título de la página:{Style.RESET_ALL} {title}")

        print(f"\n{Fore.MAGENTA}[*] Cabeceras de la respuesta HTTP:{Style.RESET_ALL}")
        for key, value in headers.items():
            print(f"{Fore.YELLOW}{key}:{Style.RESET_ALL} {value}")

        print(f"\n{Fore.MAGENTA}[*] Tecnologías detectadas:{Style.RESET_ALL}")
        if "X-Powered-By" in headers:
            technologies.append(headers["X-Powered-By"])
        if "Server" in headers:
            technologies.append(headers["Server"])

        for meta in soup.find_all("meta"):
            if meta.get("name", "").lower() == "generator":
                technologies.append(meta.get("content"))

        if technologies:
            for tech in technologies:
                print(f"{Fore.GREEN}[+] {tech}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[-] No se detectaron tecnologías específicas.{Style.RESET_ALL}")

        print(f"\n{Fore.MAGENTA}[*] Scripts JavaScript detectados:{Style.RESET_ALL}")
        for script in soup.find_all("script"):
            src = script.get("src")
            if src:
                js_files.append(src)
                print(f"{Fore.CYAN}- {src}{Style.RESET_ALL}")

        print(f"\n{Fore.MAGENTA}[*] Enlaces encontrados en la página:{Style.RESET_ALL}")
        for link in soup.find_all("a", href=True):
            links.append(link["href"])
            print(f"{Fore.BLUE}- {link['href']}{Style.RESET_ALL}")

        print(f"\n{Fore.MAGENTA}[*] Información de SSL (si aplica):{Style.RESET_ALL}")
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    print(
                        f"{Fore.GREEN}[+] Certificado válido emitido por:{Style.RESET_ALL} {cert['issuer'][0][0]} {cert['issuer'][0][1]}")
        except Exception as ssl_err:
            print(f"{Fore.YELLOW}[-] No se pudo verificar el certificado SSL o no aplica: {ssl_err}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[!] Error al procesar la página web: {e}{Style.RESET_ALL}")


def getserverip(url):
    print(f"{Fore.CYAN}[*] Analizando servidor de: {url}{Style.RESET_ALL}")

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname if parsed.scheme else urlparse("http://" + url).hostname

        ips = socket.gethostbyname_ex(hostname)
        ip_list = ips[2]

        print(f"{Fore.GREEN}[+] IP(s) del servidor:{Style.RESET_ALL}")
        for ip in ip_list:
            print(f"{Fore.YELLOW}- {ip}{Style.RESET_ALL}")

            try:
                geo = requests.get(f"http://ip-api.com/json/{ip}", headers=HEADERS_STEALTH).json()
                if geo['status'] == 'success':
                    print(f"{Fore.MAGENTA}    ↳ ISP: {geo['isp']}, País: {geo['country']}, Región: {geo['regionName']}, Ciudad: {geo['city']}{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}    ↳ Latitud: {geo['lat']}, Longitud: {geo['lon']}, ASN: {geo['as']}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}    ↳ No se pudo obtener información geográfica para {ip}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error al consultar la API de geolocalización: {e}{Style.RESET_ALL}")

            try:
                ptr = socket.gethostbyaddr(ip)
                print(f"{Fore.CYAN}    ↳ Nombre PTR (DNS inverso): {ptr[0]}{Style.RESET_ALL}")
            except socket.herror:
                print(f"{Fore.YELLOW}    ↳ No hay nombre PTR disponible para {ip}{Style.RESET_ALL}")

    except Exception as err:
        print(f"{Fore.RED}[!] Error al obtener IP del servidor: {err}{Style.RESET_ALL}")


def getrobotstxt(url):
    robotsurl = urljoin(url, "/robots.txt")
    print(f"{Fore.CYAN}[*] Accediendo a: {robotsurl}{Style.RESET_ALL}")

    try:
        response = requests.get(robotsurl, headers=HEADERS_STEALTH, timeout=10)
        if response.status_code != 200:
            print(f"{Fore.YELLOW}[-] No se encontró robots.txt en el servidor.{Style.RESET_ALL}")
            return

        content = response.text
        print(f"{Fore.GREEN}[+] Contenido de robots.txt detectado:{Style.RESET_ALL}\n")
        print(content)

        disallowed = []
        sitemaps = []
        flagged = []

        keywords_sospechosas = ['admin', 'login', 'backup', 'private', 'test', 'dev', 'config', 'db', 'panel']

        for line in content.splitlines():
            line = line.strip()
            if line.startswith("Disallow:"):
                path = line.split(":")[1].strip()
                full_url = urljoin(url, path)
                disallowed.append(full_url)
                if any(kw in path.lower() for kw in keywords_sospechosas):
                    flagged.append(full_url)
            elif line.startswith("Sitemap:"):
                sitemaps.append(line.split(":", 1)[1].strip())

        if disallowed:
            print(f"\n{Fore.MAGENTA}[*] Rutas Disallow encontradas:{Style.RESET_ALL}")
            for ruta in disallowed:
                print(f"{Fore.YELLOW}- {ruta}{Style.RESET_ALL}")

        if flagged:
            print(f"\n{Fore.RED}[!] Rutas sospechosas encontradas:{Style.RESET_ALL}")
            for ruta in flagged:
                print(f"{Fore.RED}- {ruta}{Style.RESET_ALL}")

        if sitemaps:
            print(f"\n{Fore.BLUE}[*] Sitemaps detectados:{Style.RESET_ALL}")
            for sitemap in sitemaps:
                print(f"{Fore.BLUE}- {sitemap}{Style.RESET_ALL}")

        with open("robots_detectado.txt", "w", encoding="utf-8") as f:
            f.write(content)
            print(f"\n{Fore.GREEN}[✓] Contenido guardado en robots_detectado.txt{Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Error de red al acceder a robots.txt: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error general: {e}{Style.RESET_ALL}")
