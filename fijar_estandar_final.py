import re, sqlite3

# 1. Guardar el Golden Standard del Preambulo directamente en la base de datos como referencia calibrada
txt_mc=open("master_core.txt",encoding="utf-8").read()
golden_html=txt_mc[txt_mc.find("<p class=\"pregunta-critica\">"):]
conn = sqlite3.connect("sinstitucion.db")
conn.execute("UPDATE unidades_ce SET analisis_html=?, estado_cache='VIGENTE', fecha_auditoria='27/11/2026 (GOLDEN STANDARD)' WHERE id='PREAMBULO'", (golden_html,))
conn.commit()
conn.close()

# 2. Blindar app.py: conversor HTML obligatorio + orden de cierre estricto para modelos abiertos
s = open("app.py", encoding="utf-8").read()

conv_fn = '''def limpiar_salida_html(t):
    import re
    t = re.sub(r"^```html\\s*|```$", "", t.strip(), flags=re.MULTILINE)
    if "<h4>" not in t:
        out = []
        for l in t.splitlines():
            ls = l.strip()
            if not ls or ls == "---": continue
            if ls.startswith("### ") or ls.startswith("## "): out.append(f"<h4>{ls.lstrip('#').strip()}</h4>")
            elif ls.startswith("> "): out.append(f"<blockquote>{ls[2:]}</blockquote>")
            elif ls.startswith("* ") or ls.startswith("- "): out.append(f"<ul><li>{ls[2:]}</li></ul>")
            else: out.append(f"<p>{ls}</p>")
        t = "\\n".join(out)
    t = re.sub(r"\\*\\*(.+?)\\*\\*", r"<strong>\\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\\1</code>", t)
    return t

'''
if "def limpiar_salida_html" not in s:
    s = s.replace("class SinstitucionHandler", conv_fn + "class SinstitucionHandler")

s = s.replace("html_generado = \"\".join(p.get(\"text\", \"\") for p in data[\"candidates\"][\"content\"][\"parts\"] if not p.get(\"thought\"))",
              "html_generado = limpiar_salida_html(\"\".join(p.get(\"text\", \"\") for p in data[\"candidates\"][\"content\"][\"parts\"] if not p.get(\"thought\")))")

# Reforzar mandato final al usuario para que Gemma/Llama no caigan en tono neutro
s = s.replace("prompt_usuario = f\"PRECEPTO: {titulo} ({bloque})\\nTEXTO OFICIAL BOE:\\n{texto_oficial}\\n\\nFUENTES DOCTRINALES:\\n{citas_rag}\"",
              "prompt_usuario = f\"AUDITA ESTE PRECEPTO SIGUIENDO EXACTAMENTE EL EJEMPLO MAESTRO (6 SECCIONES HTML: I a VI, TONO CRITICO NO NEUTRO, NUNCA MARKDOWN):\\nPRECEPTO: {titulo} ({bloque})\\nTEXTO OFICIAL BOE:\\n{texto_oficial}\\n\\n{citas_rag}\"")

open("app.py", "w", encoding="utf-8").write(s)
print("OK: Golden Standard fijado y conversor HTML blindado en app.py.")
