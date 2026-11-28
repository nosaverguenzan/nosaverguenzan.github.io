from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
import json, re
from typing import Any, Literal, Optional
from engine.config import SCHEMA_VERSION
from engine.normalizer import calcular_sha256

class ValidationError(ValueError):
    pass

@dataclass
class MetadatosBOE:
    fecha: str
    boe_id: str
    rango: str
    titulo_norma: str
    url_oficial: str
    estado_vigencia: str
    sha256_xml: str
    fecha_vigor: Optional[str] = None
    fecha_limite_convalidacion: Optional[str] = None

    def __post_init__(self):
        if not re.match(r"^BOE-[A-Z]-\d{4}-\d+$", self.boe_id):
            raise ValidationError(f"boe_id invalido: {self.boe_id}")
        if not self.url_oficial.startswith("https://www.boe.es/"):
            raise ValidationError(f"URL erronea: {self.url_oficial}")
        if self.rango == "Real Decreto-ley" and not self.fecha_limite_convalidacion:
            pub = date.fromisoformat(self.fecha)
            self.fecha_limite_convalidacion = (pub + timedelta(days=30)).isoformat()
@dataclass
class SeccionesGoldStandard:
    i_texto_literal_y_eficacia: str
    ii_contradicciones_organicas: str
    iii_jurispridencia_control: str
    iv_indicadores_empiricos: str
    v_marco_teorico_critico: str
    vi_reclamaciones_minimos: str

    def __post_init__(self):
        for k, v in asdict(self).items():
            if len(v.strip()) < 120: raise ValidationError(k)
            if "http://" in v or "https://" in v or "www." in v: raise ValidationError(k)
        if "..." not in self.v_marco_teorico_critico: raise ValidationError("v")

@dataclass
class FichaDoctrinal:
    id: str
    tipo_fuente: str
    titulo_encabezado: str
    subtitulo_pregunta: str
    cita_literal_bloque: str
    ultima_interpretacion: MetadatosBOE
    secciones: SeccionesGoldStandard
    numero_articulo: Optional[str] = None
    historial_boe: list[MetadatosBOE] = field(default_factory=list)
    articulos_ce_relacionados: list[str] = field(default_factory=list)
    cierre: str = "_______"
    schema_version: str = SCHEMA_VERSION
    sha256_ficha: str = ""
    meta_extensible: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.sha256_ficha:
            self.sha256_ficha = calcular_sha256(json.dumps(asdict(self), sort_keys=True, ensure_ascii=False))

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)
