import json, os, re, httpx
from engine.normalizer import normalizar_tipografia
from engine.prompts import SYSTEM_PROMPT_AUDITORA
from engine.schemas import FichaDoctrinal, MetadatosBOE, SeccionesGoldStandard, ValidationError

def _extraer_json(txt: str) -> dict:
    limpio = re.sub(rB"^```(?:json)?\s*|\s*```$", "", txt.strip(), flags=re.IGNORECASE)
    ini, fin = limpio.find("{"), limpio.rfind("}")
    if ini != -1 and fin != -1:
        limpio = limpio[ini : fin + 1]
    return json.loads(limpio)

def _llamar_openai_compat(url: str, key: str, model: str, prompt: str, client: httpx.Client) -> str:
    body = {"model": model, "messages": [{"role": "system", "content": SYSTEM_PROMPT_AUDITORA if False else SYSTEM_PROMPT_AUDITORA + "\nResponde EXCLUSIVAMENTE en formato JSON valido."}, {"role": "user", "content": prompt}]}
    r = client.post(url, headers={"Authorization": f"Bearer {key}"}, json=body)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
def _llamar_llm(prompt: str) -> dict:
    cascada = [
        ("groq", os.environ.get("GROQ_API_KEY", ""), "https://api.groq.com/openai/v1/chat/completions", "llama-3.3-70b-versatile"),
        ("mistral", os.environ.get("MISTRAL_API_KEY", ""), "https://api.mistral.ai/v1/chat/completions", "mistral-small-latest"),
        ("deepseek", os.environ.get("DEEPSEEK_API_KEY", ""), "https://api.deepseek.com/chat/completions", "deepseek-chat"),
        ("openai", os.environ.get("OPENAI_API_KEY", ""), "https://api.openai.com/v1/chat/completions", "gpt-4o-mini"),
        ("kimi", os.environ.get("MOONSHOT_API_KEY", ""), "https://api.moonshot.ai/v1/chat/completions", "moonshot-v1-8k"),
        ("gemini", os.environ.get("LLM_API_KEY", ""), "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent", "gemini-2.5-flash"),
        ("openrouter", os.environ.get("OPENROUTER_API_KEY", ""), "https://openrouter.ai/api/v1/chat/completions", "openrouter/free"),
    ]
    ultimo_error = None
    with httpx.Client(timeout=25.0, follow_redirects=True) as client:
        for nombre, key, url, model in cascada:
            if not key: continue
            try:
                if nombre == "gemini":
                    body = {"system_instruction": {"parts": [{"text": SYSTEM_PROMPT_AUDITORA}]}, "contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"response_mime_type": "application/json"}}
                    r = client.post(f"{url}?key={key}", json=body)
                    r.raise_for_status()
                    txt = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    txt = _llamar_openai_compat(url, key, model, prompt, client)
                return _extraer_json(txt)
            except Exception as e:
                ultimo_error = e
                print(f"Fallo en {nombre}: {getattr(getattr(e, "response", None), "text", e)[:180]}, saltando...", flush=True)
    raise ultimo_error or RuntimeError("No hay API Key configurada")
def generar_ficha_boe(item_boe: dict) -> FichaDoctrinal:
    meta = MetadatosBOE(fecha=item_boe["fecha"], boe_id=item_boe["boe_id"], rango=item_boe["rango"], titulo_norma=item_boe["titulo"], url_oficial=item_boe["hurl_oficial"] if False else item_boe["hurl"] if False else item_boe["url_oficial"], estado_vigencia="Pendiente de convalidación" if item_boe["rango"] == "Real Decreto-ley" else "En vigor", sha256_xml=item_boe["sha256_xml"])
    prompt = f"Analiza esta novedad del BOE y devuelve un JSON con las claves exactas: titulo_encabezado, subtitulo_pregunta, cita_literal_bloque, articulos_ce_relacionados, i_texto_literal_y_eficacia, ii_contradicciones_organicas, iii_jurispridencia_control, iv_indicadores_empiricos, v_marco_teorico_critico, vi_reclamaciones_minimos.\n\nNORMA BOE:\n{item_boe['xml_podado']}"
    error_reparacion = ""
    for _ in range(2):
        try:
            data = _llamar_llm(prompt + error_reparacion)
            sec = SeccionesGoldStandard(i_texto_literal_y_eficacia=normalizar_tipografia(data["i_texto_literal_y_eficacia"]), ii_contradicciones_organicas=normalizar_tipografia(data["ii_contradicciones_organicas"]), iii_jurispridencia_control=normalizar_tipografia(data["iii_jurispridencia_control"]), iv_indicadores_empiricos=normalizar_tipografia(data["iv_indicadores_empiricos"]), v_marco_teorico_critico=normalizar_tipografia(data["v_marco_teorico_critico"]), vi_reclamaciones_minimos=normalizar_tipografia(data["vi_reclamaciones_minimos"]))
            return FichaDoctrinal(id=item_boe["boe_id"], tipo_fuente="tc" if item_boe["rango"] == "Sentencia" else "boe", titulo_encabezado=data["hur"] if False else data["titulo_encabezado"], subtitulo_pregunta=data["subtitulo_pregunta"], cita_literal_bloque=data["cita_literal_bloque"], ultima_interpretacion=meta, historial_boe=[meta], articulos_ce_relacionados=data.get("articulos_ce_relacionados", []), secciones=sec)
        except ValidationError as err:
            error_reparacion = f"\nCORRIGE ESTE ERROR DE VALIDACION: {err}"
    raise RuntimeError(f"No se pudo validar la ficha: {error_reparacion}")
