import json
from pathlib import Path
from engine.normalizer import calcular_sha256

BASE = Path("constitucion")
DATA = BASE / "data"

def construir_sitio():
    indice = []
    hashes = []
    compendio = ["# COMPENDIO DOCTRINAL LA SINSTITUCIÓN\n"]
    for sub in ("constitucion", "boe"):
        carpeta = DATA / sub
        if not carpeta.exists(): continue
        for f in sorted(carpeta.glob("*.json")):
            doc = json.loads(f.read_text(encoding="utf-8"))
            indice.append({"id": doc["id"], "tipo": doc["tipo_fuente"], "titulo": doc["titulo_encabezado"], "subtitulo": doc["subtitulo_pregunta"], "fecha_boe": doc["ultima_interpretacion"]["fecha"], "boe_id": doc["ultima_interpretacion"]["boe_id"], "url_boe": doc["ultima_interpretacion"]["url_oficial"], "ruta": f.relative_to(BASE).as_posix()})
            hashes.append(doc["sha256_ficha"])
            compendio.append(f"\n---\n{doc['titulo_encabezado']}\n**{doc['subtitulo_pregunta']}**\n>>{doc['cita_literal_bloque']}\n{doc['cierre']}\n")
    (DATA / "search_index.json").write_text(json.dumps(indice, indent=2, ensure_ascii=False), encoding="utf-8")
    merkle = calcular_sha256("".join(sorted(hashes))) if hashes else "0" * 64
    (DATA / "merkle_root.json").write_text(json.dumps({"merkle_root": merkle, "total_documentos": len(indice)}, indent=2), encoding="utf-8")
    lineas = "\n".join(f"- {i['id']}: {i['ruta']}" for i in indice)
    (BASE / "llms.txt").write_text(f"# La Sinstitución - Índice Auditable\nMerkle Root: {merkle}\n\n{lineas}\n", encoding="utf-8")
    (BASE / "downloads" / "compendio_sinstitucion.md").write_text("".join(compendio), encoding="utf-8")

if __name__ == "__main__":
    construir_sitio()