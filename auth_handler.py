# auth_handler.py

import base64
import requests
import os
import sys

# Verificación de dependencias
try:
    from requests.structures import CaseInsensitiveDict
except ImportError:
    os.system(f"{sys.executable} -m pip install requests")


def construir_headers_auth(tipo, datos, headers_base=None):
    """
    Genera headers de autenticación compatibles con diferentes tipos:
    - JWT
    - Basic Auth
    - Cookies

    :param tipo: "jwt", "basic" o "cookie"
    :param datos: Diccionario con los valores necesarios según el tipo
    :param headers_base: Headers adicionales opcionales
    :return: Diccionario de headers final
    """
    headers = headers_base.copy() if headers_base else {}

    if tipo == "jwt":
        token = datos.get("token", "")
        headers["Authorization"] = f"Bearer {token}"

    elif tipo == "basic":
        usuario = datos.get("usuario", "")
        password = datos.get("password", "")
        token = base64.b64encode(f"{usuario}:{password}".encode()).decode()
        headers["Authorization"] = f"Basic {token}"

    elif tipo == "cookie":
        cookies = datos.get("cookies", {})
        cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
        headers["Cookie"] = cookie_str

    return headers


def ejemplo_autenticacion():
    """
    Ejemplo de uso de autenticación con los tres tipos en un endpoint protegido.
    """
    url = input("URL protegida: ").strip()
    tipo = input("Tipo de autenticación (jwt/basic/cookie): ").strip().lower()

    if tipo == "jwt":
        token = input("Token JWT: ").strip()
        headers = construir_headers_auth("jwt", {"token": token})

    elif tipo == "basic":
        usuario = input("Usuario: ").strip()
        password = input("Contraseña: ").strip()
        headers = construir_headers_auth("basic", {"usuario": usuario, "password": password})

    elif tipo == "cookie":
        raw = input("Cookies (clave1=valor1; clave2=valor2): ").strip()
        cookies = dict(item.split("=") for item in raw.split("; "))
        headers = construir_headers_auth("cookie", {"cookies": cookies})
    else:
        print("Tipo inválido.")
        return

    try:
        respuesta = requests.get(url, headers=headers, timeout=10)
        print(f"[✓] Código de respuesta: {respuesta.status_code}")
        print("Primeros 300 caracteres del contenido:")
        print(respuesta.text[:300])
    except Exception as e:
        print(f"[X] Error al hacer la solicitud: {e}")


# Si se ejecuta como script
if __name__ == "__main__":
    ejemplo_autenticacion()
