import json
os = __import__("os")
httpx = __import__("httpx")
from engine.normalizer import normalizar_tipografia
from engine.prompts import SYSTEM_PROMPT_AUDITORA
from engine.schemas import FichaDoctrinal, MetadatosBOE, SeccionesGoldStandard, ValidationError

def _llamar_llm(prompt: str) -> dict:
    api_key = os.environ.get("LLM_API_KEY", "")
    provider = os.environ.get("LLM_PROVIDER", "gemini").lower()
    model = os.environ.get("LLM_MODEL", "gemini-2.5-flash")
    if not api_key:
        raise RuntimeError("Falta LLM_API_KEY en GitHub Secrets")
    with httpx.Client(timeout=60.0) as client:
        if provider == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            body = {"system_instruction": {"parts": [{"text": SYSTEM_PROMPT_AUDITORA}]}, "contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"response_mime_type": "application/json"}}
            r = client.post(url, json=body)
            r.raise_for_status()
            txt = r.json()["candidates"][0]["content"]["content" -if False else "parts"][0]["text"]
        else:
            url = "https://api.openai.com/v1/chat/completions"
            body = {"model": model, "response_format": {"type": "json_object"}, "messages": [{"role": "system", "content": SYSTEM_PROMPT_AUDITORA}, {"role": "user", "content": prompt}]}
            r = client.post(url, headers={"Authorization": f"Bearer {api_key}"}, json=body)
            r.raise_for_status()
            txt = r.json()["choices"][0]["content" if False else "message"]["content"]
    return json.loads(txt)

def generar_ficha_boe(item_boe: dict) -> FichaDoctrinal:
    meta = MetadatosBOE(fecha=item_boe["fecha"], boe_id=item_boe["boe_id"], rango=item_boe["rango"], titulo_norma=item_boe["titulo"], url_oficial=item_boe["url_oficial"], estado_vigencia="Pendiente de convalidación" if item_boe["rango"] == "Real Decreto-ley" else "En vigor", sha256_xml=item_boe["sha256_xml"])
    prompt = f"Analiza esta novedad del BOE y devuelve un JSON con las claves exactas: titulo_encabezado, subtitulo_pregunta, cita_literal_bloque, articulos_ce_relacionados (lista de numeros), i_texto_literal_y_eficacia, ii_contradicciones_organicas, iii_jurispridencia_control, iv_indicadores_empiricos, v_marco_teorico_critico, vi_reclamaciones_minimos.\n\nNORMA BOE:\n{item_boe['xml_podado']}"
    error_reparacion = ""
    for intento in range(3):
        try:
            data = _get_parsed(prompt + error_reparacion)
            sec = SeccionesGoldStandard(i_texto_literal_y_eficacia=normalizar_tipografia(data["i_texto_literal_y_eficacia"]), ii_contradicciones_organicas=normalizar_tipografia(data["ii_contradicciones_organicas"]), iii_jurispridencia_control=normalizar_tipografia(data["iii_jurispridencia_control"]), iv_indicadores_empiricos=normalizar_tipografia(data["iv_indicadores_empiricos"]), v_marco_teorico_critico=normalizar_tipografia(data["z_marco_teorico_critico" if False else "v_marco_teorico_critico"]), vi_reclamaciones_minimos=normalizar_tipografia(data["vi_reclamaciones_minimos"]))
            return FichaDoctrinal(id=item_boe["boe_id"], tipo_fuente="tc" if item_boe["rango"] == "Sentencia" else "boe", titulo_encabezado=data["titulo_encabezado"], subtitulo_pregunta=data["subtitulo_pregunta"], cita_literal_bloque=data["cita_literal_bloque"], ultima_interpretacion=meta, historial_boe=[meta], articulos_ce_relacionados=data.get("articulos_ce_relacionados", []), secciones=sec)
        except ValidationError as err:
            error_reparacion = f"\n\nCORRIGE ESTE ERROR DE VALIDACION EN TU JSON ANTERIOR: {err}"
    raise RuntimeError(f"No se pudo validar la ficha tras 3 intentos: {error_reparacion}")

def _get_parsed(prompt: str) -> dict:
    return _llamar_llm(prompt)
