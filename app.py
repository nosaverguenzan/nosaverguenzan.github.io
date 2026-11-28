import os, re, json, time, sqlite3, urllib.parse, requests
from datetime import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from boe_sync_db import init_db, sincronizar_boe, DB_PATH
from bloques_autores import obtener_bloque_doctrinal

if os.path.exists(".env"):
    for ln in open(".env", encoding="utf-8"):
        if "=" in ln and not ln.strip().startswith("#"):
            k, v = ln.strip().split("=", 1)
            os.environ[k] = v.strip("\"'")

def limpiar_salida_html(t):
    t = re.sub(r"^```html\s*|```$", "", t.strip(), flags=re.MULTILINE)
    if "<h4>" not in t:
        out = []
        for l in t.splitlines():
            ls = l.strip()
            if not ls or ls == "---": continue
            if ls.startswith("### ") or ls.startswith("## "): out.append(f"<h4>{ls.lstrip('#').strip()}</h4>")
            elif ls.startswith("> "): out.append(f"<blockquote>{ls[2:]}</blockquote>")
            elif ls.startswith("* ") or ls.startswith("- "): out.append(f"<ul><li>{ls[2:]}</li></ul>")
            else: out.append(f"<p>{ls}</p>")
        t = "\n".join(out)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t

class SinstitucionHandler(BaseHTTPRequestHandler):
    pausados = {}

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        if path == "/":
            with open("index.html", "rb") as f:
                html = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
            return

        if path == "/api/catalogo":
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id, bloque, titulo, estado_cache FROM unidades_ce ORDER BY orden ASC")
            items = [{"id": r.__getitem__(0), "bloque": r.__getitem__(1), "titulo": r.__getitem__(2), "estado": r.__getitem__(3)} for r in c.fetchall()]
            conn.close()
            self.send_json({"unidades": items})
            return

        if path.startswith("/api/unidad/"):
            uid = path.split("/api/unidad/")[-1]
            forzar = "true" in params.get("forzar", []) == "true"
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id, bloque, titulo, texto_oficial, hash_texto, analisis_html, estado_cache, fecha_auditoria FROM unidades_ce WHERE id=?", (uid,))
            row = c.fetchone()
            if not row:
                conn.close()
                self.send_json({"detail": "Unidad no encontrada"}, 404)
                return

            uid, bloque, titulo, texto_oficial, hash_texto, analisis_html, estado_cache, fecha_auditoria = row

            if analisis_html and estado_cache == "VIGENTE" and not forzar:
                conn.close()
                self.send_json({"id": uid, "bloque": bloque, "titulo": titulo, "texto_oficial": texto_oficial or "", "hash_texto": hash_texto or "BOE_VERIFICADO", "analisis_html": analisis_html, "fecha_auditoria": fecha_auditoria, "origen": "CACHE_MASTER_1_0"})
                return

            sys_prompt = open("master_core.txt", encoding="utf-8").read()
            citas_rag = obtener_bloque_doctrinal(uid, titulo)
            m_num = re.search(r"ART_(\d+)", uid)
            num_art = int(m_num.group(1)) if m_num else 0
            es_nivel_a = (uid in ["PREAMBULO", "DD_UNICA"] or (1 <= num_art <= 57) or (135 == num_art) or (166 <= num_art <= 169))
            densidad_txt = "NIVEL A (ALTA DENSIDAD): Desarrollo exhaustivo y extenso (3-4 parrafos densos por seccion) en las 6 secciones romanas." if es_nivel_a else "NIVEL B/C (DENSIDAD ORGANICA/TECNICA): Analisis riguroso y directo manteniendo intactas las 6 secciones romanas."

            p1 = f"""EJECUTA PRIMERA MITAD (SUBTITULO + SECCIONES I A III) DEL MASTER PROMPT 1.0 PARA: {titulo} ({bloque}).
{densidad_txt}
TEXTO OFICIAL BOE (ya mostrado arriba en pantalla, no lo repitas en blockquote): {texto_oficial}

USA EXCLUSIVAMENTE HTML LIMPIO (NUNCA MARKDOWN ###, **, >):
<p class="pregunta-critica">Subtitulo formulado como pregunta critica inquisitiva, respetuosa y no neutral que sintetice la contradiccion estructural central del precepto.</p>
<h4>I. TEXTO LITERAL Y EXAMEN DE EFICACIA MATERIAL</h4>
<p>Critica de eficacia material: como opera el precepto en la realidad social, que ficciones juridicas encubre y a que sectores excluye.</p>
<h4>II. CONTRADICCIONES ORGANICAS Y NORMATIVAS</h4>
<p><strong>1. Contraste con el ordenamiento juridico interno:</strong> Leyes organicas, codigos y reglamentos vigentes que vacian o restringen el precepto (protegidos con <code>...</code>).</p>
<p><strong>2. Primacia del Derecho Internacional de los Derechos Humanos (<code>arts. 10.2 y 96.1 CE</code>):</strong> Tratados ratificados, <code>Convencion de Viena</code>, <code>PIDCP</code>, <code>PIDESC</code>, <code>CEDH</code>, <code>Carta Social Europea</code> y obligacion judicial de ejercer el control difuso de convencionalidad.</p>
<h4>III. JURISPRUDENCIA Y DOCTRINA DE CONTROL</h4>
<p>Resoluciones clave del Tribunal Constitucional, Tribunal Supremo y organos supranacionales (TEDH, Comites de la ONU, Comite Europeo de Derechos Sociales) protegidas en <code>...</code> con su doctrina exacta."""

            sec6_inst = "<p>Despliega integramente en lista <ul> los 9 Macro-Ejes Post-Constituyentes del Master Prompt 1.0 en primera persona politica plural («hacemos nuestra», «exigimos», «asumimos como propio»).</p>" if uid == "ART_168" else "<p>Selecciona UNICAMENTE los 4 o 5 colectivos de la Matriz Aliada (15 Ambitos) directamente golpeados por las clausulas de este articulo especifico. Redacta en lista <ul> cada punto titulando la clausula criticada + el colectivo aliado en negrita y desarrollando sus exigencias de minimos en primera persona politica plural («hacemos nuestra», «exigimos», «asumimos como propio»).</p>"

            p2 = f"""CONTINUA SEGUNDA MITAD (SECCIONES IV A VI + CIERRE _______) DEL MASTER PROMPT 1.0 PARA: {titulo} ({bloque}).
{densidad_txt}
EXTRACTOS DOCTRINALES DE CEREBRO_FILOSOFICO.DB:
{citas_rag}

USA EXCLUSIVAMENTE HTML LIMPIO (NUNCA MARKDOWN):
<h4>IV. INDICADORES EMPIRICOS Y DATOS OFICIALES</h4>
<p>Contrasta las promesas del articulo con estadisticas verificadas nombrando la institucion emisora y encerrando en <code>...</code> cada informe oficial (<code>Encuesta de Condiciones de Vida</code> del INE, Banco de Espana, CIS, <code>Informe Anual del Defensor del Pueblo</code>) junto con DATA_PARAMS_2026 (RBU 1.147 euros/mes, techo patrimonial 1.709.400 euros, alquiler topado al 20 %).</p>
<h4>V. MARCO TEORICO Y APARATO CRITICO</h4>
<p>Articula la fundamentacion filosofica, historica y antiautoritaria citando las obras aportadas bajo el formato estricto: Autor en «Obra» (PROHIBIDO poner negritas a los autores ni a los titulos).</p>
<h4>VI. RECLAMACIONES DE MINIMOS DE LOS COLECTIVOS ALIADOS</h4>
{sec6_inst}
<p>_______</p>"""

            ahora_ts = time.time()
            groq_key = os.environ.get("GROQ_API_KEY", "")
            gemini_key = os.environ.get("GEMINI_API_KEY", "")
            texto_final_ia = ""

            if groq_key and self.pausados.get("groq", 0) < ahora_ts:
                gh = ".".join(["api", "groq", "com"])
                ug = "https" + f"://{gh}/openai/v1/chat/completions"
                hg = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                try:
                    mg = requests.get("https" + f"://{gh}/openai/v1/models", headers=hg, timeout=10).json().get("data", [])
                    mod_g = next((x["id"] for x in mg if not any(k in x["id"] for k in ["guard", "whisper", "tts"]) and any(k in x["id"] for k in ["llama-3.3-70b", "llama-4", "llama-3.1-70b", "70b", "120b", "qwen"])), next(iter(mg))["id"])
                    r1 = requests.post(ug, headers=hg, json={"model": mod_g, "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": p1}], "max_tokens": 4096, "temperature": 0.35}, timeout=40)
                    if r1.status_code == 200:
                        t1 = r1.json()["choices"].__getitem__(0)["message"]["content"]
                        r2 = requests.post(ug, headers=hg, json={"model": mod_g, "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": p2}], "max_tokens": 4096, "temperature": 0.35}, timeout=40)
                        t2 = r2.json()["choices"].__getitem__(0)["message"]["content"] if r2.status_code == 200 else ""
                        texto_final_ia = t1 + "\n" + t2
                        print(f"[MOTOR OK] Groq {mod_g} (Master Prompt 1.0)")
                    else:
                        print("[GROQ AVISO]", r1.status_code, r1.text[:200])
                        self.pausados["groq"] = ahora_ts + 60
                except Exception as e:
                    print("[GROQ ERR]", e)
                    self.pausados["groq"] = ahora_ts + 60


if __name__ == "__main__":
    init_db()
    server = ThreadingHTTPServer(("0.0.0.0", 8000), SinstitucionHandler)
    print("Servidor MASTER PROMPT 1.0 activo en http://127.0.0.1:8000")
    server.serve_forever()
