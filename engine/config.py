SCHEMA_VERSION = "1.0"

DATA_PARAMS_2026 = {
    "registro_enmienda": "REGAGE26e00100941917",
    "rbu_mensual": "1.147 euros mensuales",
    "techo_acumulacion": "1.709.400 euros",
    "tope_alquiler": "20 %",
}

BOE_SUMARIO_URL = "https://boe.es{fecha}"
BOE_DOC_XML_URL = "https://boe.es{boe_id}"
BOE_CONSOLIDADA_URL = "https://boe.es{boe_id}/texto"
BOE_WEB_PUBLICA_URL = "https://boe.es{boe_id}"

RANGOS_RELEVANTES = [
    "Ley Orgánica",
    "Ley",
    "Real Decreto-ley",
    "Real Decreto Legislativo",
    "Sentencia",
    "Declaración",
]

EXCLUSIONES_TITULO = [
    "Corrección de errores",
    "Corrección de erratas",
    "tipos de interés",
    "Extracto",
]
