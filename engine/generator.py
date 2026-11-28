import json
import os
import re
from urllib.parse import urlunsplit
import httpx
from engine.normalizer import normalizar_tipografia
from engine.prompts import SYSTEM_PROMPT_AUDITORA
from engine.schemas import FichaDoctrinal, MetadatosBOE, SeccionesGoldStandard, ValidationError

U_GROQ = urlunsplit(("https", "://groq.com", "/openai/v1/chat/completions", "", ""))
U_GROQ_M = urlunsplit(("https", "://groq.com", "/openai/v1/models", "", ""))
U_GEM = urlunsplit(("https", "://googleapis.com", "/v1beta/models", "", ""))
U_OR = urlunsplit(("https", "openrouter.ai", "/api/v1/chat/completions", "", ""))
U_OR_M = urlunsplit(("https", "openrouter.ai", "/api/v1/models", "", ""))


def _extraer_json(txt: str) -> dict:
    limpio = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt.strip(), flags=re.IGNORECASE)
    ini, fin = limpio.find("{"), limpio.rfind("}")
    if ini != -1 and fin != -1:
        limpio = limpio[ini : fin + 1]
    return json.loads(limpio)


def _llamar_oai(url: str, key: str, model: str, prompt: str, client: httpx.Client) -> str:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT_AUDITORA + "\nDevuelve solo JSON valido."},
            {"role": "user", "content": prompt},
        ],
    }
    r = client.post(url, headers={"Authorization": f"Bearer {key}"}, json=body)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def _llamar_llm(prompt: str) -> dict:
    grq = os.environ.get("GROQ_API_KEY", "")
    gem = os.environ.get("LLM_API_KEY", "")
    opr = os.environ.get("OPENROUTER_API_KEY", "")
    ultimo_error = None
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        if grq:
            try:
                rm = client.get(U_GROQ_M, headers={"Authorization": f"Bearer {grq}"})
                rm.raise_for_status()
                mods = [m["id"] for m in rm.json()["data"] if "llama" in m["id"].lower() or "qwen" in m["id"].lower()]
                m = mods[0] if mods else "llama-3.1-8b-instant"
                print(f"Groq -> {m}", flush=True)
                return _extraer_json(_llamar_oai(U_GROQ, grq, m, prompt, client))
            except Exception as e:
                ultimo_error = e
                print(f"Fallo Groq: {e}", flush=True)
        if gem:
            try:
                rm = client.get(f"{U_GEM}?key={gem}")
                rm.raise_for_status()
                mods = [m["name"] for m in rm.json()["models"] if "generateContent" in m.get("supportedGenerationMethods", []) and "flash" in m["name"].lower()]
                m = mods[0] if mods else "models/gemini-2.5-flash-lite"
                print(f"Gemini -> {m}", flush=True)
                u = urlunsplit(("https", "://googleapis.com", f"/v1beta/{m}:generateContent", f"key={gem}", ""))
                body = {"system_instruction": {"parts": [{"text": SYSTEM_PROMPT_AUDITORA}]}, "contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"response_mime_type": "application/json"}}
                r = client.post(u, json=body)
                r.raise_for_status()
                return _extraer_json(r.json()["candidates"][0]["content"]["parts"][0]["text"])
            except Exception as e:
                ultimo_error = e
                print(f"Fallo Gemini: {e}", flush=True)
        if opr:
            try:
                rm = client.get(U_OR_M)
                rm.raise_for_status()
                mods = [m["id"] for m in rm.json()["data"] if m["id"].endswith(":free")]
                m = mods[0] if mods else "google/gemma-3-27b-it:free"
                print(f"OpenRouter -> {m}", flush=True)
                return _extraer_json(_llamar_oai(U_OR, opr, m, prompt, client))
            except Exception as e:
                ultimo_error = e
                print(f"Fallo OpenRouter: {e}", flush=True)
    raise ultimo_error or RuntimeError("Sin API disponible")


def generar_ficha_boe(item_boe: dict) -> FichaDoctrinal:
    meta = MetadatosBOE(fecha=item_boe["fecha"], boe_id=item_boe["boe_id"], rango=item_boe["rango"], titulo_norma=item_boe["titulo"], url_oficial=item_boe["url_oficial"], estado_vigencia="Pendiente de convalidación" if item_boe["rango"] == "Real Decreto-ley" else "En vigor", sha256_xml=item_boe["sha256_xml"])
    prompt = f"Analiza esta novedad del BOE y devuelve JSON con las claves exactas: titulo_encabezado, subtitulo_pregunta, cita_literal_bloque, articulos_ce_relacionados, i_texto_literal_y_eficacia, ii_contradicciones_organicas, iii_jurisprudencia_control, iv_indicadores_empiricos, v_marco_teorico_critico, vi_reclamaciones_minimos.\n\nNORMA BOE:\n{item_boe['xml_podado']}"
    error_reparacion = ""
    for _ in range(2):
        try:
            data = _llamar_llm(prompt + error_reparacion)
            sec = SeccionesGoldStandard(i_texto_literal_y_eficacia=normalizar_tipografia(data["i_texto_literal_y_eficacia"]), ii_contradicciones_organicas=normalizar_tipografia(data["ii_contradicciones_organicas"]), iii_jurisprudencia_control=normalizar_tipografia(data["iii_jurisprudencia_control"]), iv_indicadores_empiricos=normalizar_tipografia(data["iv_indicadores_empiricos"]), v_marco_teorico_critico=normalizar_tipografia(data["v_marco_teorico_critico"]), vi_reclamaciones_minimos=normalizar_tipografia(data["vi_reclamaciones_minimos"]))
            return FichaDoctrinal(id=item_boe["boe_id"], tipo_fuente="tc" if item_boe["rango"] == "Sentencia" else "boe", titulo_encabezado=data["titulo_encabezado"], subtitulo_pregunta=data["subtitulo_pregunta"], cita_literal_bloque=data["cita_literal_bloque"], ultima_interpretacion=meta, historial_boe=[meta], articulos_ce_relacionados=data.get("articulos_ce_relacionados", []), secciones=sec)
        except ValidationError as err:
            error_reparacion = f"\nCORRIGE ESTE ERROR: {err}"
    raise RuntimeError(f"No se pudo validar: {error_reparacion}")
