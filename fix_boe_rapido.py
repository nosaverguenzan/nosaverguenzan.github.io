import sqlite3, hashlib, requests
import xml.etree.ElementTree as ET

PROTO = "https" + "://"
DB_PATH = "sinstitucion.db"
url_texto = f"{PROTO}www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-1978-31229/texto"
headers = {"Accept": "application/xml", "User-Agent": "Mozilla/5.0"}

print("Descargando texto integro de la Constitucion desde BOE...")
rt = requests.get(url_texto, headers=headers, timeout=20)
print("Estado HTTP:", rt.status_code)

if rt.status_code == 200:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    root_t = ET.fromstring(rt.content)
    actualizados = 0
    for bloque_xml in root_t.findall(".//bloque"):
        bid = bloque_xml.attrib.get("id", "").upper()
        parrafos = ["".join(p.itertext()).strip() for p in bloque_xml.findall(".//p")]
        texto_unido = "\n\n".join(p for p in parrafos if p)
        if not texto_unido:
            continue
        target_id = None
        if bid == "PR":
            target_id = "PREAMBULO"
        elif bid.startswith("A") and bid[1:].isdigit():
            target_id = f"ART_{int(bid[1:])}"
        elif bid.startswith("DA"):
            num = "".join(ch for ch in bid if ch.isdigit()) or "1"
            target_id = f"DA_{num}"
        elif bid.startswith("DT"):
            num = "".join(ch for ch in bid if ch.isdigit()) or "1"
            target_id = f"DT_{num}"
        elif bid.startswith("DD"):
            target_id = "DD_UNICA"
        elif bid.startswith("DF"):
            target_id = "DF_UNICA"

        if target_id:
            h_txt = hashlib.sha256(texto_unido.encode("utf-8")).hexdigest()
            c.execute("UPDATE unidades_ce SET texto_oficial=?, hash_texto=? WHERE id=?",
                      (texto_unido, h_txt, target_id))
            actualizados += 1
    conn.commit()
    conn.close()
    print(f"OK: {actualizados} unidades actualizadas con su texto literal oficial del BOE.")
