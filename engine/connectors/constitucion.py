import json
os = __import__("os")
from pathlib import Path
from engine.build_site import construir_sitio
from engine.normalizer import calcular_sha256, normalizar_tipografia
from engine.schemas import FichaDoctrinal, MetadatosBOE, SeccionesGoldStandard
from engine.generator import _llamar_llm

def generar_lote(desde: int = 1, hasta: int = 10):
    if not os.environ.get("LLM_API_KEY"):
        raise RuntimeError("Falta LLM_API_KEY en GitHub Secrets")
    meta = MetadatosBOE(fecha="2026-05-20", boe_id="BOE-A-1978-31229", rango="Constitucion Espanola", titulo_norma="Constitucion Espanola (BOE-A-2026-10881)", url_oficial="https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229", estado_vigencia="En vigor", sha256_xml=calcular_sha256("BOE-A-1978-31229"))
    for n in range(desde, hasta + 1):
        dest = Path("constitucion/data/constitucion") / f"art_{str(n).zfill(3)}.json"
        if dest.exists(): continue
        data = _get_art(n)
        sec = SeccionesGoldStandard(i_texto_literal_y_eficacia=normalizar_tipografia(data["i_texto_literal_y_eficacia"]), ii_contradicciones_organicas=normalizar_tipografia(data["ii_contradicciones_organicas"]), iii_jurispridencia_control=normalizar_tipografia(data["iii_jurispridencia_control"]), iv_indicadores_empiricos=normalizar_tipografia(data["iv_indicadores_empiricos"]), v_marco_teorico_critico=normalizar_tipografia(data["v_marco_teorico_critico"]), vi_reclamaciones_minimos=normalizar_tipografia(data["vi_reclamaciones_minimos"]))
        f = FichaDoctrinal(id=f"art_{str(n).zfill(3)}", tipo_fuente="constitucion", numero_articulo=str(n), titulo_encabezado=data["titulo_encabezado"], subtitulo_pregunta=data["subtitulo_pregunta"], cita_literal_bloque=data["cita_literal_bloque"], ultima_interpretacion=meta, historial_boe=[meta], secciones=sec)
        dest.write_text(f.to_json(), encoding="utf-8")
    construir_sitio()

def _get_art(n: int) -> dict:
    return _llamar_llm(f"Audita el articulo {n} de la Constitucion Espanola de 1978 con las claves JSON: titulo_encabezado, subtitulo_pregunta, cita_literal_bloque, i_texto_literal_y_eficacia, ii_contradicciones_organicas, iii_jurispridencia_control, iv_indicadores_empiricos, v_marco_teorico_critico, vi_reclamaciones_minimos.")

if __name__ == "__main__":
    generar_lote(1, 10)
