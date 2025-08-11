"""
main.py – Lanzador principal de la herramienta ofensiva M4 – WebXploit

Este script coordina todos los módulos de reconocimiento, análisis y evasión:
- Subdomain scan
- JS endpoint extraction
- WhatWeb y Nmap scan
- Fuzzing de parámetros y fuerza bruta
- Detección de WAFs y evasión
- Autenticación personalizada
- Inyección SQL
- Generación de reportes HTML y TXT

Desarrollado por M4 – Uso ético y educativo
"""

import os
from datetime import datetime
from subdomain_scan import subdomain_scan
from js_endpoint_scanner import analizar_js_scripts
from scanner_nmap_whatweb import escanear_con_nmap, escanear_con_whatweb
from stealth_mode import generar_headers_sigilosos, aplicar_delay_sigiloso
from auth_handler import construir_headers_auth
from report_generator import generar_reporte_html, generar_reporte_txt


def mostrar_menu():
    print("\n\U0001f6e1\ufe0f Herramienta ofensiva M4 – WebXploit by M4")
    print("\n📂 RECONOCIMIENTO")
    print(" 1) Escaneo de Subdominios         - Encuentra subdominios activos del sitio")
    print(" 2) Endpoints en Scripts JS        - Extrae rutas ocultas y APIs de archivos JS")
    print(" 3) WhatWeb                        - Detecta tecnologías del sitio")
    print(" 4) Nmap                           - Escaneo de puertos y servicios")
    print("\n⚔️ ATAQUE Y ANÁLISIS")
    print(" 5) Fuzzing de parámetros          - Inyecta payloads en parámetros GET")
    print(" 6) Fuerza bruta de tokens API     - Busca tokens válidos con wordlist")
    print(" 7) Fuzz combinado (parámetros)    - Ataque mixto con payloads y fuerza bruta")
    print(" 8) Scan de APIs expuestas         - Detecta tokens, claves y datos sensibles")
    print("\n🧱 EVASIÓN Y SIGILO")
    print(" 9) Evasión de detección           - Bypasses contra WAFs y firewalls")
    print("10) Modo Stealth                   - Delays aleatorios y headers rotativos")
    print("\n🔐 AUTENTICACIÓN")
    print("11) Autenticación personalizada    - JWT, Basic Auth o Cookies")
    print("\n💉 INYECCIÓN SQL")
    print("12) SQLi – Inyección avanzada      - Automatización de pruebas SQLi reales")
    print("\n📄 REPORTES Y LOGS")
    print("13) Generar reporte HTML/TXT       - Exporta resultados profesionales")
    print("\n🎛️ OPCIONES GENERALES")
    print("14) Modo Verbose/Debug             - Muestra salida detallada y procesos")
    print("\n🗂️ SELECCIONES RÁPIDAS")
    print("99) Ejecutar TODO")
    print("98) Solo RECONOCIMIENTO (1-4)")
    print("97) Solo ATAQUE (5-8,12)")
    print("96) Solo EVASIÓN (9-10)")


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\U0001f6e1\ufe0f Herramienta ofensiva M4 – WebXploit by M4\n")

    url = input("🔎 Introduce la URL del objetivo (ej: https://ejemplo.com): ").strip()
    analista = input("🧑‍💼 Nombre del analista/investigador: ").strip()

    mostrar_menu()
    seleccion_raw = input("\nEscribe los números separados por espacios (ej: 1 2 4 5 8 10 13): ").strip().split()

    seleccion = []
    for op in seleccion_raw:
        if op == "99":
            seleccion = list(range(1, 15))
            break
        elif op == "98":
            seleccion.extend([1, 2, 3, 4])
        elif op == "97":
            seleccion.extend([5, 6, 7, 8, 12])
        elif op == "96":
            seleccion.extend([9, 10])
        elif op.isdigit():
            seleccion.append(int(op))

    seleccion = sorted(set(seleccion))
    secciones_reporte = []

    verbose = 14 in seleccion
    stealth = 10 in seleccion

    headers = generar_headers_sigilosos() if stealth else {"User-Agent": "Mozilla/5.0"}

    if 11 in seleccion:
        tipo = input("Tipo de autenticación (jwt/basic/cookie): ").strip()
        if tipo == "jwt":
            token = input("Token JWT: ").strip()
            headers = construir_headers_auth("jwt", {"token": token})
        elif tipo == "basic":
            user = input("Usuario: ").strip()
            pwd = input("Contraseña: ").strip()
            headers = construir_headers_auth("basic", {"usuario": user, "password": pwd})
        elif tipo == "cookie":
            raw = input("Cookies (clave1=valor1; clave2=valor2): ").strip()
            cookies = dict(item.split("=") for item in raw.split("; "))
            headers = construir_headers_auth("cookie", {"cookies": cookies})
            
    if 1 in seleccion:
        print("⏳ Ejecutando escaneo de subdominios...")
        try:
            resultado = subdomain_scan(url, verbose=verbose)
            secciones_reporte.append(("Subdominios detectados", "\n".join(resultado) if resultado else "Ninguno"))
        except Exception as e:
            secciones_reporte.append(("Subdominios", f"Error: {e}"))

    if 2 in seleccion:
        print("⏳ Analizando scripts JS...")
        try:
            hallazgos = analizar_js_scripts(url, verbose=verbose)
            secciones_reporte.append(("JS Endpoints encontrados", "\n".join(hallazgos) if hallazgos else "Ninguno"))
        except Exception as e:
            secciones_reporte.append(("JS Endpoints", f"Error: {e}"))

    if 3 in seleccion:
        print("⏳ Ejecutando WhatWeb...")
        try:
            resultado = escanear_con_whatweb(url, verbose=verbose)
            secciones_reporte.append(("Resultado WhatWeb", resultado))
        except Exception as e:
            secciones_reporte.append(("WhatWeb", f"Error: {e}"))

    if 4 in seleccion:
        print("⏳ Ejecutando Nmap...")
        try:
            dominio = url.replace("https://", "").replace("http://", "").split("/")[0]
            resultado = escanear_con_nmap(dominio, verbose=verbose)
            secciones_reporte.append(("Resultado Nmap", resultado))
        except Exception as e:
            secciones_reporte.append(("Nmap", f"Error: {e}"))

    if 5 in seleccion and 7 not in seleccion:
        print("⏳ Fuzzing de parámetros...")
        try:
            from control import fuzzparameter
            import io
            import sys
            salida = io.StringIO()
            sys_stdout_original = sys.stdout
            sys.stdout = salida
            fuzzparameter(url)
            sys.stdout = sys_stdout_original
            resultado_fuzz = salida.getvalue()
            secciones_reporte.append(("Fuzzing de parámetros", resultado_fuzz.strip()))
        except Exception as e:
            secciones_reporte.append(("Fuzzing de parámetros", f"Error: {e}"))

    if 6 in seleccion and 7 not in seleccion:
        print("⏳ Fuerza bruta de tokens API...")
        try:
            from control import bruteforcefuzz
            params = ["api_key", "access_token", "auth", "key"]
            wordlist = ["admin", "12345", "password", "secret", "qwerty"]
            import io
            import sys
            salida = io.StringIO()
            sys_stdout_original = sys.stdout
            sys.stdout = salida
            bruteforcefuzz(url, params, wordlist)
            sys.stdout = sys_stdout_original
            resultado_brute = salida.getvalue()
            secciones_reporte.append(("Fuerza bruta de tokens API", resultado_brute.strip()))
        except Exception as e:
            secciones_reporte.append(("Fuerza bruta de tokens API", f"Error: {e}"))

    if 7 in seleccion:
        print("⏳ Fuzz combinado (parámetros y fuerza bruta)...")
        try:
            from control import fuzzparameter, bruteforcefuzz
            params = ["api_key", "access_token", "auth", "key"]
            wordlist = ["admin", "12345", "password", "secret", "qwerty"]
            import io
            import sys
            salida = io.StringIO()
            sys_stdout_original = sys.stdout
            sys.stdout = salida
            fuzzparameter(url)
            bruteforcefuzz(url, params, wordlist)
            sys.stdout = sys_stdout_original
            resultado_combined = salida.getvalue()
            secciones_reporte.append(("Fuzz combinado", resultado_combined.strip()))
        except Exception as e:
            secciones_reporte.append(("Fuzz combinado", f"Error: {e}"))

    if 8 in seleccion:
        print("⏳ Analizando APIs en scripts JS...")
        try:
            resultado = analizar_js_scripts(url, verbose=verbose)
            contenido = "\n".join(resultado) if resultado else "No se detectaron endpoints."
            secciones_reporte.append(("APIs expuestas en JS", contenido))
        except Exception as e:
            secciones_reporte.append(("APIs expuestas", f"Error: {e}"))

    if 9 in seleccion:
        print("⏳ Evasión de detección...")
        try:
            from control import evadedetection
            import io
            import sys
            salida = io.StringIO()
            sys_stdout_original = sys.stdout
            sys.stdout = salida
            evadedetection(url)
            sys.stdout = sys_stdout_original
            resultado_evasion = salida.getvalue()
            secciones_reporte.append(("Evasión de detección", resultado_evasion.strip()))
        except Exception as e:
            secciones_reporte.append(("Evasión de detección", f"Error: {e}"))

    if 10 in seleccion:
        print("⏳ Aplicando Modo Stealth...")
        try:
            headers = generar_headers_sigilosos()
            aplicar_delay_sigiloso(verbose=True)
            headers_str = "\n".join(f"{k}: {v}" for k, v in headers.items())
            secciones_reporte.append(("Modo Stealth (headers generados)", headers_str))
        except Exception as e:
            secciones_reporte.append(("Modo Stealth", f"Error: {e}"))

    
    if 12 in seleccion:
        print("⏳ Ejecutando inyección SQL avanzada (modo pro)...")
        try:
            from sqli_attack import analizar_todos_vectores
            import io
            import sys
            salida = io.StringIO()
            sys_stdout_original = sys.stdout
            sys.stdout = salida
            analizar_todos_vectores(url, headers=headers)
            sys.stdout = sys_stdout_original
            resultado_sqli = salida.getvalue()
            secciones_reporte.append(("Inyección SQL Avanzada (SQLi Pro)", resultado_sqli.strip()))
        except Exception as e:
            secciones_reporte.append(("Inyección SQL", f"Error: {e}"))

    if 13 in seleccion:
        if verbose: print(" [13] Generando reporte HTML/TXT...")
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        dominio_base = url.replace("https://", "").replace("http://", "").split("/")[0].replace('.', '_')
        nombre_archivo = f"reporte_{dominio_base}_{fecha_actual}"
        try:
            generar_reporte_html(nombre_archivo, "Análisis Web – Herramienta M4", secciones_reporte, analista, url)
            generar_reporte_txt(nombre_archivo, secciones_reporte, analista, url)
        except Exception as e:
            print(f"[ERROR] No se pudo generar el reporte: {e}")

    print("\n✅ Análisis completado. Gracias por usar la herramienta M4.")


if __name__ == "__main__":
    main()
