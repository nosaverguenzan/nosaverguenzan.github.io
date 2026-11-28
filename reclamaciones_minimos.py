RECLAMACIONES_POR_BLOQUE = {
    "SOBERANIA": """
- Movimiento republicano y plataformas pro-proceso constituyente: Hacemos nuestra la exigencia de abolicion de la institucion monarquica, supresion de la inviolabilidad regia (art. 56.3 CE) y de los delitos de injurias a la Corona (arts. 490.3 y 491 CP), restitucion publica del patrimonio real y apertura del procedimiento agravado del art. 168 CE para un proceso constituyente libre.
- Victimas del franquismo y movimiento memorialista: Exigimos la derogacion inmediata de la Ley 46/1977 de Amnistia, la nulidad de pleno derecho de los tribunales y sentencias de la dictadura y el enjuiciamiento efectivo de los crimenes de lesa humanidad.""",
    "PROPIEDAD": """
- Mareas sociales, sindicatos de clase y plataformas por la Renta Basica: Hacemos nuestra la exigencia de implantacion de una Renta Basica Universal individual e incondicional de 1.147 EUR/mes, fijacion de un techo patrimonial maximo de 1.709.400 EUR, derogacion del art. 135 CE y de la LO 2/2012 de Estabilidad Presupuestaria, y subordinacion de toda propiedad privada a la funcion social real.""",
    "REPRESION": """
- Colectivos antirrepresivos, abogacia critica y movimientos sociales: Exigimos la derogacion integra de la Ley Organica 4/2015 de proteccion de la seguridad ciudadana (Ley Mordaza), la supresion de la Audiencia Nacional como tribunal de excepcion heredero del TOP, la prohibicion de identificaciones por perfil etnico y la abolicion de la prision permanente revisable.""",
    "TERRITORIO": """
- Pueblos sin Estado, asambleas municipalistas y movimiento confederado: Asumimos como propio el reconocimiento del derecho inalienable de autodeterminacion de los pueblos, la libre federacion de municipios y territorios desde abajo sin tutela estatal y la derogacion del art. 155 CE.""",
    "PATRIARCADO": """
- Feminismos de base, colectivos LGTBIQ+ y trabajadoras del hogar y cuidados: Hacemos nuestra la exigencia de reconocimiento y remuneracion publica del trabajo reproductivo y de cuidados, equiparacion laboral plena sin brecha salarial, abolicion de la ley de extranjeria para trabajadoras internas y garantia efectiva de derechos sexuales y reproductivos en la sanidad publica.""",
    "ECOLOGIA": """
- Movimiento por la vivienda (PAH / Sindicatos de Inquilinas) y ecologismo social: Exigimos la prohibicion legal de todos los desahucios sin alternativa habitacional, limitacion del alquiler al 20% de los ingresos (o de la RBU de 1.147 EUR/mes), expropiacion de vivienda vacia de grandes tenedores y recuperacion de montes y bienes comunales frente al extractivismo.""",
    "EDUCACION": """
- Comunidad educativa critica, movimiento laicista y prensa independiente: Exigimos la supresion de los conciertos educativos privados y de los Acuerdos con la Santa Sede de 1979, una educacion publica, laica y autogestionada libre de adoctrinamiento estatal, y el fin de los oligopolios mediaticos.""",
    "RUPTURA": """
- Movimiento libertario y asambleas populares constituyentes: Hacemos nuestra la impugnacion integral del cerrojo del Titulo X (arts. 166-169 CE) y de la Disposicion Derogatoria Unica que mantuvo intacta la legalidad ordinaria franquista, exigiendo un proceso constituyente popular de base que sustituya el Estado centralizado por una federacion libre de comunas."""
}

def obtener_reclamaciones_exactas(uid, titulo):
    t = (uid + " " + titulo).upper()
    k = "PROPIEDAD" if any(x in t for x in ["31","33","35","38","128","135"]) else ("REPRESION" if any(x in t for x in ["17","24","25","117"]) else ("TERRITORIO" if any(x in t for x in ["ART_2","137","143","149","155","DA_","DT_"]) else ("PATRIARCADO" if any(x in t for x in ["14","32","39"]) else ("ECOLOGIA" if any(x in t for x in ["45","47","132"]) else ("EDUCACION" if any(x in t for x in ["16","20","27"]) else ("RUPTURA" if any(x in t for x in ["166","167","168","169","DD_","DF_"]) else "SOBERANIA"))))))
    return RECLAMACIONES_POR_BLOQUE[k]
