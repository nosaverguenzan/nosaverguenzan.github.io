import sqlite3, hashlib, requests
import xml.etree.ElementTree as ET
from datetime import datetime

PROTO = "https" + "://"
DB_PATH = "sinstitucion.db"

NORMAS_VIGILADAS = {
    "CE_1978": ("Constitucion Espanola (1978)", "BOE-A-1978-31229"),
    "CODIGO_CIVIL": ("Codigo Civil (RD 24/07/1889)", "BOE-A-1889-4763"),
    "CODIGO_PENAL": ("Codigo Penal (LO 10/1995)", "BOE-A-1995-25444"),
    "AMNISTIA": ("Ley de Amnistia (Ley 46/1977)", "BOE-A-1977-24937"),
    "EXTRANJERIA": ("Ley Organica de Extranjeria (LO 4/2000)", "BOE-A-2000-544"),
    "SEG_CIUDADANA": ("Ley Seguridad Ciudadana (LO 4/2015)", "BOE-A-2015-3442"),
    "LAU": ("Ley de Arrendamientos Urbanos (Ley 29/1994)", "BOE-A-1994-26003"),
    "TRATADOS": ("Ley de Tratados Internacionales (Ley 25/2014)", "BOE-A-2014-12326"),
    "PIDCP": ("Pacto Int. Derechos Civiles y Politicos", "BOE-A-1977-10733"),
    "PIDESC": ("Pacto Int. Derechos Economicos, Sociales y Culturales", "BOE-A-1977-10734"),
    "CEDH": ("Convenio Europeo de Derechos Humanos", "BOE-A-1979-24010"),
    "CARTA_SOCIAL": ("Carta Social Europea Revisada", "BOE-A-2021-9719"),
    "DESAPARICIONES": ("Convencion Int. Desapariciones Forzadas", "BOE-A-2011-3194"),
    "VIENA": ("Convencion de Viena Derecho de los Tratados", "BOE-A-1980-11884"),
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS normativa_vigilada (
        clave TEXT PRIMARY KEY,
        nombre TEXT,
        boe_id TEXT,
        fecha_actualizacion_boe TEXT,
        hash_sha256 TEXT,
        ultima_comprobacion TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS unidades_ce (
        id TEXT PRIMARY KEY,
        orden INTEGER,
        bloque TEXT,
        titulo TEXT,
        texto_oficial TEXT,
        hash_texto TEXT,
        analisis_html TEXT,
        estado_cache TEXT DEFAULT 'PENDIENTE',
        fecha_auditoria TEXT
    )""")
    conn.commit()
    return conn

def catalogo_192_unidades():
    unidades = [("PREAMBULO", 0, "Preambulo", "Preambulo de la Constitucion Espanola")]
    for i in range(1, 170):
        unidades.append((f"ART_{i}", i, "Articulado", f"Articulo {i} CE"))
    for i in range(1, 5):
        unidades.append((f"DA_{i}", 169 + i, "Disposiciones Adicionales", f"Disposicion Adicional {i}a"))
    for i in range(1, 10):
        unidades.append((f"DT_{i}", 173 + i, "Disposiciones Transitorias", f"Disposicion Transitoria {i}a"))
    unidades.append(("DD_UNICA", 183, "Disposicion Derogatoria", "Disposicion Derogatoria Unica"))
    unidades.append(("DF_UNICA", 184, "Disposicion Final", "Disposicion Final Unica"))
    return unidades

def sincronizar_boe():
    conn = init_db()
    c = conn.cursor()
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
    headers = {"Accept": "application/xml", "User-Agent": "LaSinstitucion-BOE-Auditor/1.0"}

    for uid, orden, bloque, titulo in catalogo_192_unidades():
        c.execute("INSERT OR IGNORE INTO unidades_ce (id, orden, bloque, titulo) VALUES (?, ?, ?, ?)",
                  (uid, orden, bloque, titulo))

    reformas_detectadas = 0
    for clave, (nombre, boe_id) in NORMAS_VIGILADAS.items():
        url = f"{PROTO}www.boe.es/datosabiertos/api/legislacion-consolidada/id/{boe_id}"
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                digest = hashlib.sha256(r.content).hexdigest()
                root = ET.fromstring(r.content)
                fecha_mod = root.findtext(".//fecha_actualizacion") or "Consolidado vigente"
                c.execute("SELECT hash_sha256 FROM normativa_vigilada WHERE clave=?", (clave,))
                prev = c.fetchone()
                if prev and prev[0] != digest:
                    reformas_detectadas += 1
                    c.execute("UPDATE unidades_ce SET estado_cache='DESACTUALIZADO_BOE'")
                c.execute("INSERT OR REPLACE INTO normativa_vigilada VALUES (?, ?, ?, ?, ?, ?)",
                          (clave, nombre, boe_id, fecha_mod, digest, ahora))
        except Exception:
            pass

    try:
        url_texto = f"{PROTO}www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-1978-31229/texto"
        rt = requests.get(url_texto, headers=headers, timeout=20)
        if rt.status_code == 200:
            root_t = ET.fromstring(rt.content)
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
                    c.execute("SELECT hash_texto FROM unidades_ce WHERE id=?", (target_id,))
                    row = c.fetchone()
                    if row and row[0] and row[0] != h_txt:
                        c.execute("UPDATE unidades_ce SET texto_oficial=?, hash_texto=?, estado_cache='DESACTUALIZADO_BOE' WHERE id=?",
                                  (texto_unido, h_txt, target_id))
                    else:
                        c.execute("UPDATE unidades_ce SET texto_oficial=?, hash_texto=? WHERE id=?",
                                  (texto_unido, h_txt, target_id))
    except Exception:
        pass

    conn.commit()
    conn.close()
    print(f"Sincronizacion BOE completada ({ahora}). Reformas: {reformas_detectadas}")

if __name__ == "__main__":
    sincronizar_boe()
