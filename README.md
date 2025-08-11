# M4 – WebXploit (CLI)

Herramienta educativa para reconocimiento y pruebas básicas de seguridad web y posibles vulnerabilidades:
- Reconocimiento: subdominios, endpoints JS, tecnologías, WHOIS, robots.txt, Nmap, WhatWeb
- Fuzzing y fuerza bruta de parámetros/tokens
- Escaneo de APIs expuestas
- SQLi avanzada multi-vector
- Evasión de detección con headers y delays stealth
- Reportes HTML/TXT con prioridades e información de integridad

> **Aviso**: Úsalo únicamente en sistemas propios o con autorización por escrito el creador no se responsabiliza por el Uso
que se le de a esta Herramienta.

---

## Compatibilidad

- **Linux** y **Windows** soportados.
- Solo opciones que dependen de Nmap o WhatWeb requieren que dichos binarios estén instalados y en el PATH.

---

## Requisitos

- **Python 3.10+**
- Pip y virtualenv
- (Opcional) Nmap y WhatWeb instalados en el sistema
- (Opcional) Usar venv para crea un entorno virtual para el proyecto.
Un entorno virtual es una carpeta aislada que contiene su propia instalación de Python y 
todas las librerías necesarias, sin afectar ni depender de otras instalaciones del sistema. 
---

## Instalación

### Linux
```bash
git clone <REPO>
cd <REPO>
python3 -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt
sudo apt install nmap whatweb
```

### Windows (PowerShell)
```powershell
git clone <REPO>
cd <REPO>
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Para Nmap en Windows: instalar desde la web oficial y agregarlo al PATH.  
Para WhatWeb: usar WSL o instalar Ruby + `gem install whatweb`.

---

## Uso
```bash
# Linux
source .venv/bin/activate
# Windows
.\.venv\Scripts\Activate.ps1

python main.py
```
1. Ingresa la URL objetivo.
2. Selecciona las opciones del menú (ej. `1 2 5 10 13`).

---

## Estructura
```
main.py
recon.py
js_endpoint_scanner.py
subdomain_scan.py
scanner_nmap_whatweb.py
sqli_attack.py
control.py
esqueleto.py
stealth_mode.py
auth_handler.py
report_generator.py
argument_handler.py
subdomains.txt
requirements.txt
Instalacion.txt
```

---

## Licencia
Este proyecto está bajo **MIT License**.  
Puedes usarlo, modificarlo y distribuirlo libremente, incluso con fines comerciales,
 siempre que mantengas el aviso de copyright
 y la licencia en las copias o versiones modificadas.
 By CyberForMx, Siguenos en nuestras redes sociales!
 Tiktok:CyberForMx
---
