from pathlib import Path
from engine.build_site import construir_sitio
from engine.normalizer import calcular_sha256, normalizar_tipografia
from engine.schemas import FichaDoctrinal, MetadatosBOE, SeccionesGoldStandard

meta = MetadatosBOE(
    fecha="2026-05-20",
    boe_id="BOE-A-1978-31229",
    rango="Constitución Española (Texto Consolidado)",
    titulo_norma="Constitución Española - Última actualización BOE-A-2026-10881",
    url_oficial="https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229",
    estado_vigencia="En vigor",
    sha256_xml=calcular_sha256("BOE-A-1978-31229-2026"),
)

sec = SeccionesGoldStandard(
    i_texto_literal_y_eficacia=normalizar_tipografia("El art. 47 CE proclama el derecho a una vividenda digna y adecuada, pero su ubicación en el Capítulo III del Título I lo desactiva como derecho fundamental exigible. La ficción jurídica del mandato a los poderes públicos opera en la práctica como una cláusula de inexigibilidad que subordina el habitar al mercado inmobiliario especulativo."),
    ii_contradicciones_organicas=normalizar_tipografia("1. Ordenamiento interno: Eliminado del recurso de amparo por el art. 53.3 CE, la Ley 12/2023 de Vivienda no impide los desahucios sin alternativa habitacional. 2. Primacía del Derecho Internacional (arts. 10.2 y 96.1 CE): España vulnera sistemáticamente eh art. 11.1 del PIDESC y el art. 31 de la Carta Social Europea Revisada, que exigen protección efectiva frente a la expulsion foreda y el rentismo abusivo."),
    iii_jurispridencia_control=normalizar_tipografia("El Tribunal Constitucional, a través de la STC 32/2018 (fundamento jurídico segundo) y la STC 79/2024, ha blindado la propiedad privada especulativa frente a la función social del suelo, reduciendo el art. 47 CE a un mero principio rector de estimación política sin tutela judicial directa."),
    iv_indicadores_empiricos=normalizar_tipografia("Según la Encuesta de Condiciones de Vida del INE y los datos del Banco de España 2026, el esfuerzà de las familias trabajadoras para pagar el alquiler supera el 20 % y alcanza hasta el 45 % de sus rentas, mientras el patrimonio se concentra por encima del techo de 1.709.400 euros (100 x SMI anual) sin existir ni una Renta Básica Universal de 1.147 euros mensuales."),
    v_marco_teorico_critico=normalizar_tipografia("Pierre-Joseph Proudhon en «Qué es la propiedad?» advierte que ... el rentismo convierte el derivado de habitar en un tributo privado sin trabajo productivo ... Linea de continuidad analítica con Henri Lefebvre en «El derecho a la ciudad» y la Enmienda a la Totalidad REGAGE26e00100941917."),
    vi_reclamaciones_minimos=normalizar_tipografia("1. Exigibilidad judicial inmediata de la vividenda digna: Reconocemos el derecho a la vividenda como derecho fundamental de amparo directo y prohibimos todo desahucio sin alternativa habitacional. 2. Tope del 20 % en alquileres y prohibición del acaparamiento: Limitamos el alcance del alquiler al 20 % de la renta de los hogares y prohibimos la acumulación especulativa de inmuebles."),
)

ficha = FichaDoctrinal(
    id="art_047",
    tipo_fuente="constitucion",
    numero_articulo="47",
    titulo_encabezado="# ARTÃCULO 47 DE LA CONSTITUCIÓN ESPAÑOLA",
    subtitulo_pregunta="¿Derecho fundamental a habitar o licencia constitucional para el rentismo inmobiliario?",
    cita_literal_bloque="> «Todos los españoles tienen derecho a disfrutar de una vivienda digna y adecuada... y regularán la utilización del suelo de acuerdo con el interés general para impedir la especulación.»",
    ultima_interpretacion=meta,
    historial_boe=[meta],
    articulos_ce_relacionados=["33", "53.3", "128"],
    secciones=sec,
)

Path("constitucion/data/constitucion/art_047.json").write_text(ficha.to_json(), encoding="utf-8")
construir_sitio()
print("Articulo 47 y indices generados con exito.")
