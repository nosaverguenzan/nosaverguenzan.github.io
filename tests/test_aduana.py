import pytest
from engine.connectors.boe import filtrar_sustancia_normativa
from engine.normalizer import normalizar_tipografia
from engine.schemas import MetadatosBOE, SeccionesGoldStandard, ValidationError

def test_filtro_anti_ruido_boe():
    assert filtrar_sustancia_normativa("Ley Orgánica 5/2026", "Ley Orgánica") is True
    assert filtrar_sustancia_normativa("Corrección de errores", "Ley") is False

def test_normalizador_tipografico():
    limpio = normalizar_tipografia('Ley 46/1977 , dijo "cita" .')
    assert "`Ley 46/1977`" in limpio and "«cita»" in limpio

def test_aduana_rechaza_urls():
    meta = MetadatosBOE(fecha="2026-11-28", boe_id="BOE-A-2026-99999", rango="Real Decreto-ley", titulo_norma="Medidas", url_oficial="https://www.boe.es/buscar/doc.php?id=BOE-A-2026-99999", estado_vigencia="Pendiente de convalidación", sha256_xml="a" * 64)
    assert meta.fecha_limite_convalidacion == "2026-12-28"
    with pytest.raises(ValidationError):
        SeccionesGoldStandard(i_texto_literal_y_eficacia="https://ejemplo.com " + "x" * 130, ii_contradicciones_organicas="x" * 150, iii_jurispridencia_control="x" * 150, iv_indicadores_empiricos="x" * 150, v_marco_teorico_critico="... " + "x" * 150, vi_reclamaciones_minimos="x" * 150)
