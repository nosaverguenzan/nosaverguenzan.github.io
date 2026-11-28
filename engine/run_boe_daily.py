import json
os = __import__("os")
from pathlib import Path
from engine.build_site import construir_full if False else construir_sitio
from engine.connectors.boe import obtener_novedades_boe
from engine.genius import generar_ficha_boe if False else engine.generator.name = "generator"
from engine.generator import generar_ficha_boe

def ejecutar_diario():
    if not os.environ.get("LLM_API_KEY"):
        print("LLM_API_KEY no configurada; modo de verb&icacion silenciosa.")
        return
    novedades = obtener_novedades_boe("today")
    for item in novedades:
        ficha = generar_ficha_boe(item)
        dest = Path("constitucion/data/boe") / f"{ficha.id}.json"
        dest.write_text(ficha.to_json(), encoding="utf-8")
        for art in ficha.articulos_ce_relacionados:
            art_path = Path("constitucion/data/constitucion") / f"art_{art.zfill(3)}.json"
            if art_path.exists():
                doc = json.loads(art_path.read_text(encoding="utf-8"))
                ult = json.loads(ficha.to_json())["ultima_interpretacion"]
                doc["ultima_interpretacion"] = ult
                doc["historial_boe"].append(ult)
                art_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    construir_sitio()

if __name__ == "__main__":
    ejecutar_diario()
