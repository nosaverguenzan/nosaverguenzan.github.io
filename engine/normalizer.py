import hashlib
import re
import xml.etree.ElementTree as ET


def calcular_sha256(contenido: str | bytes) -> str:
    if isinstance(contenido, str):
        contenido = contenido.encode("utf-8")
    return hashlib.sha256(contenido).hexdigest()


def normalizar_tipografia(texto: str) -> str:
    # Convertir comillas rectas en comillas latinas en citas
    texto = re.sub(r'"([^"\n]+)"', r"«\1»", texto)
    # Normalizar puntos suspensivos
    texto = re.sub(r"\.{4,}", "...", texto)
    # Eliminar espacios antes de signos de puntuación
    texto = re.sub(r"\s+([,.;:])", r"\1", texto)
    # Proteger referencias normativas y estadísticas con acentos graves si no lo están
    patrones_norma = [
        r"(?<!`)\b(Ley(?:\s+Orgánica)?\s+\d+/\d{4})\b(?!`)",
        r"(?<!`)\b(Real\s+Decreto-ley\s+\d+/\d{4})\b(?!`)",
        r"(?<!`)\b(STC\s+\d+/\d{4})\b(?!`)",
        r"(?<!`)\b(arts?\.\s+\d+(?:\.\d+)?(?:\s+y\s+\d+(?:\.\d+)?)?\s+CE)\b(?!`)",
    ]
    for patron in patrones_norma:
        texto = re.sub(patron, r"`\1`", texto)
    return texto.strip()


def podar_xml_boe(xml_bruto: str) -> str:
    root = ET.fromstring(xml_bruto)
    partes = []
    for tag in ("titulo", "rango", "fecha_publicacion"):
        nodo = root.find(f".//{tag}")
        if nodo is not None and nodo.text:
            partes.append(f"<{tag}>{nodo.text.strip()}</{tag}>")

    texto_nodo = root.find(".//texto")
    if texto_nodo is not None:
        parrafos = [
            "".join(p.itertext()).strip()
            for p in texto_nodo.findall(".//p")
            if "".join(p.itertext()).strip()
        ]
        partes.append("<contenido>\n" + "\n".join(parrafos) + "\n</contenido>")
    return "\n".join(partes)
