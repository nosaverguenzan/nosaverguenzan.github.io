from datetime import date, datetime
import httpx
from engine.config import BOE_DOC_XML_URL, BOE_SUMARIO_URL, BOE_WEB_PUBLICA_URL, EXCLUSIONES_TITULO, RANGOS_RELEVANTES
from engine.normalizer import calcular_sha256, podar_xml_boe

def filtrar_sustancia_normativa(titulo: str, rango: str) -> bool:
    if rango not in RANGOS_RELEVANTES:
        return False
    t = titulo.lower()
    return not any(e.lower() in t for e in EXCLUSIONES_TITULO)

def obtener_novedades_boe(fecha_str: str | None = None) -> list[dict]:
    fecha = date.today() if not fecha_str or fecha_str == "today" else datetime.strptime(fecha_str, "%Y-%m-%d").date()
    url = BOE_SUMARIO_URL.format(fecha=fecha.strftime("%Y%m%d"))
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        r = client.get(url, headers={"Accept": "application/json"})
        if r.status_code == 404:
            return []
        r.raise_for_status()
        return _extraer_items(r.json(), fecha.isoformat(), client)

def _extraer_items(data: dict, fecha: str, client: httpx.Client) -> list[dict]:
    res = []
    diarios = data.get("data", {}).get("sumario", {}).get("diario", [])
    if isinstance(diarios, dict): diarios = [diarios]
    for d in diarios:
        for s in d.get("seccion", []):
            if s.get("@codigo") not in ("1", "T"): continue
            deps = s.get("departamento", [])
            if isinstance(deps, dict): deps = [deps]
            for dep in deps:
                epis = dep.get("epigrafe", [])
                if isinstance(epis, dict): epis = [epis]
                for epi in epis:
                    items = epi.get("item", [])
                    if isinstance(items, dict): items = [items]
                    for it in items:
                        bid = it.get("identificador", "")
                        tit = it.get("titulo", "")
                        rng = epi.get("@nombre", "")
                        if filtrar_sustancia_normativa(tit, rng):
                            x = client.get(BOE_DOC_XML_URL.format(boe_id=bid))
                            x.raise_for_status()
                            res.append({"boe_id": bid, "fecha": fecha, "rango": rng, "titulo": tit, "url_oficial": BOE_WEB_PUBLICA_URL.format(boe_id=bid), "sha256_xml": calcular_sha256(x.text), "xml_podado": podar_xml_boe(x.text)})
    return res
