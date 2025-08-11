from datetime import datetime
import hashlib
import html
import socket
import requests
import os

# Crear carpeta de reportes si no existe
os.makedirs("reportes", exist_ok=True)

def generar_hash_integridad(nombre_analista, objetivo, timestamp):
    contenido = f"{nombre_analista}_{objetivo}_{timestamp}"
    return hashlib.sha256(contenido.encode()).hexdigest()

def obtener_info_sitio(objetivo):
    try:
        dominio = objetivo.replace("https://", "").replace("http://", "").split("/")[0]
        ip = socket.gethostbyname(dominio)
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        info = {
            "IP": ip,
            "ISP": geo.get("isp", "Desconocido"),
            "País": geo.get("country", "Desconocido"),
            "Región": geo.get("regionName", "Desconocido"),
            "Ciudad": geo.get("city", "Desconocido"),
            "Latitud": geo.get("lat", "N/A"),
            "Longitud": geo.get("lon", "N/A"),
        }
        return info
    except Exception as e:
        return {"Error": f"No se pudo obtener información del sitio: {e}"}

def clasificar_prioridad(titulo, contenido):
    titulo = titulo.lower()
    contenido = contenido.lower()
    if "sqli" in titulo or "sql" in contenido:
        return 1
    if "vulnerabilidad" in contenido or "riesgo" in contenido or "potencial" in contenido:
        return 1
    elif "token" in contenido or "expuesto" in contenido or "endpoint" in titulo:
        return 2
    elif "detección" in titulo or "headers" in contenido:
        return 3
    else:
        return 4

def etiqueta_prioridad(nivel):
    return {
        1: "🔥 Alta prioridad",
        2: "⚠️ Media prioridad",
        3: "🔎 Baja prioridad",
        4: "ℹ️ Información"
    }.get(nivel, "ℹ️ Información")

def descripcion_prioridad(nivel):
    return {
        1: "Amenazas críticas que podrían comprometer el sistema si no se mitigan.",
        2: "Potenciales vectores de ataque o fugas de información sensibles.",
        3: "Comportamientos inusuales o indicadores de posibles protecciones o WAFs.",
        4: "Resultados informativos o benignos sin indicios de explotación directa."
    }.get(nivel, "Resultado sin clasificación explícita.")

def generar_tabla_resumen(resumen):
    tabla = "<table border='1' cellpadding='6' style='background:#fff;border-collapse:collapse;'>"
    tabla += "<thead><tr style='background:#ddd'><th>Sección</th><th>Prioridad</th><th>Resumen</th></tr></thead><tbody>"
    for sec, etiqueta, desc in resumen:
        tabla += f"<tr><td>{html.escape(sec)}</td><td>{etiqueta}</td><td>{html.escape(desc)}</td></tr>"
    tabla += "</tbody></table>"
    return tabla

def generar_reporte_html(nombre_archivo, titulo, secciones, analista, objetivo):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hash_integridad = generar_hash_integridad(analista, objetivo, timestamp)
    sitio_info = obtener_info_sitio(objetivo)
    archivo_html = f"reportes/{nombre_archivo}.html"

    secciones_clasificadas = [(titulo, contenido, clasificar_prioridad(titulo, contenido)) for titulo, contenido in secciones]
    secciones_ordenadas = sorted(secciones_clasificadas, key=lambda x: x[2])
    resumen_tabla = [(t, etiqueta_prioridad(n), descripcion_prioridad(n)) for t, _, n in secciones_ordenadas]

    with open(archivo_html, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang='es'>
<head>
    <meta charset='UTF-8'>
    <title>{titulo}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f9f9f9; }}
        h1 {{ color: #2c3e50; }}
        .info, .hash, .extra {{ background: #eef; padding: 10px; margin-bottom: 10px; border-radius: 6px; }}
        .seccion {{ margin-top: 25px; }}
        pre {{ background: #222; color: #0f0; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        .prioridad1 pre {{ background: #300; color: #f88; }}
        .prioridad2 pre {{ background: #443300; color: #ffcc00; }}
        .prioridad3 pre {{ background: #003344; color: #6cf; }}
        .prioridad4 pre {{ background: #eee; color: #222; }}
        footer {{ text-align: center; font-size: 14px; margin-top: 40px; color: #555; }}
        .reco {{ background: #fef7e0; padding: 12px; border-left: 5px solid #ffa500; border-radius: 5px; }}
        .btn-descargar {{
            display: inline-block; padding: 10px 15px; background: #2c3e50; color: #fff; text-decoration: none; border-radius: 4px; margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>{titulo}</h1>
    <div class='info'>
        <strong>Analista:</strong> {analista}<br>
        <strong>Fecha y Hora:</strong> {timestamp}<br>
        <strong>Objetivo:</strong> {objetivo}
    </div>
    <div class='extra'>
        <strong>Información del Sitio:</strong><br>""")
        for k, v in sitio_info.items():
            f.write(f"        {k}: {html.escape(str(v))}<br>\n")

        f.write(f"""    </div>
    <div class='hash'>
        <strong>Hash SHA256 de integridad:</strong><br>
        <code>{hash_integridad}</code>
    </div>
    <h2>📊 Resumen del análisis por prioridad</h2>
    {generar_tabla_resumen(resumen_tabla)}
""")

        for titulo, contenido, nivel in secciones_ordenadas:
            contenido_escapado = html.escape(contenido)
            etiqueta = etiqueta_prioridad(nivel)
            descripcion = descripcion_prioridad(nivel)
            f.write(f"""
    <div class='seccion prioridad{nivel}'>
        <h2>{etiqueta} – {html.escape(titulo)}</h2>
        <small>{descripcion}</small>
        <pre>{contenido_escapado}</pre>
    </div>
""")

        f.write("""
    <h2>🛡️ Recomendaciones generales</h2>
    <div class='reco'>
        <ul>
            <li><strong>SQLi detectada:</strong> Implementa validaciones estrictas del lado del servidor, ORMs seguros y evita concatenar entradas en consultas SQL.</li>
            <li><strong>Tokens expuestos:</strong> Revoca y regenera los tokens afectados. Usa almacenamiento seguro (HTTPOnly, Secure, SameSite).</li>
            <li><strong>Headers débiles:</strong> Agrega cabeceras de seguridad como Content-Security-Policy, X-Frame-Options, HSTS.</li>
            <li><strong>Mejoras en CORS:</strong> Restringe orígenes permitidos, evita comodines, y valida métodos y encabezados permitidos.</li>
            <li><strong>Automatización:</strong> Considera implementar escaneo por lotes o sobre múltiples URLs automáticamente.</li>
        </ul>
    </div>

    <a href="#" class="btn-descargar" onclick="window.print()">🖨️ Exportar como PDF</a>

    <footer>
        <p>🔒 Reporte generado por <strong>M4LVOK SECURITY</strong> – Todos los derechos reservados.</p>
    </footer>
</body>
</html>""")

    print(f"[✓] Reporte HTML generado: {archivo_html}")

def generar_reporte_txt(nombre_archivo, secciones, analista, objetivo):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hash_integridad = generar_hash_integridad(analista, objetivo, timestamp)
    sitio_info = obtener_info_sitio(objetivo)
    archivo_txt = f"reportes/{nombre_archivo}.txt"

    with open(archivo_txt, "w", encoding="utf-8") as f:
        f.write("=== REPORTE DE ANÁLISIS M4 – WebXploit ===\n")
        f.write(f"Analista: {analista}\n")
        f.write(f"Fecha y Hora: {timestamp}\n")
        f.write(f"Objetivo: {objetivo}\n")
        f.write(f"Hash de integridad (SHA256): {hash_integridad}\n")
        f.write("=" * 50 + "\n\n")

        f.write("--- Información del sitio ---\n")
        for k, v in sitio_info.items():
            f.write(f"{k}: {v}\n")

        f.write("\n--- Resultados ---\n\n")
        for titulo, contenido in secciones:
            contenido_limpio = contenido.replace("\x1b[33m", "").replace("\x1b[0m", "")
            f.write(f"[+] {titulo.upper()}\n{contenido_limpio}\n\n")

        f.write("=== Recomendaciones generales ===\n")
        f.write("- En caso de SQLi: usar validación de entrada y ORMs seguros.\n")
        f.write("- Revocar tokens expuestos y reforzar cookies.\n")
        f.write("- Fortalecer cabeceras HTTP de seguridad.\n")
        f.write("- Corregir políticas de CORS permisivas.\n")
        f.write("- Automatizar auditorías para múltiples URLs.\n")

    print(f"[✓] Reporte TXT generado: {archivo_txt}")
