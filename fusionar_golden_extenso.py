import sqlite3

conn = sqlite3.connect("sinstitucion.db")
conn.execute("UPDATE unidades_ce SET analisis_html=NULL, estado_cache='PENDIENTE'")
conn.commit()
conn.close()

s = open("app.py", encoding="utf-8").read()
i = s.find("recl_exactas = obtener_reclamaciones_exactas")
j = s.find("if groq_key and SinstitucionHandler.pausados")

bloque_fusion = '''recl_exactas = obtener_reclamaciones_exactas(uid, titulo)
            p1 = f"""MANTEN EXACTAMENTE LA ESTRUCTURA GOLDEN STANDARD (SECCIONES I A III) PARA: {titulo} ({bloque})
TEXTO OFICIAL BOE (ya insertado arriba, no lo repitas): {texto_oficial}

USA SOLO HTML LIMPIO (NUNCA MARKDOWN ###, **, >) Y EXPLAYATE CON RIGOR DOCTORAL (4 PARRAFOS LARGOS POR SECCION):
<p class="pregunta-critica">Redacta aqui una pregunta inquisitiva critica y demoledora sobre el precepto.</p>
<h4>I. TEXTO LITERAL Y EXAMEN DE EFICACIA MATERIAL</h4>
Redacta 4 parrafos extensos analizando la trampa ideologica del precepto, la ineficacia juridica de sus promesas sociales y su subordinacion al poder estatal y patrimonial.
<h4>II. CONTRADICCIONES ORGANICAS Y NORMATIVAS</h4>
<p><strong>1. Contraste con el ordenamiento juridico interno:</strong> Redacta 3 parrafos extensos confrontando el precepto con leyes concretas entre etiquetas <code>...</code> (Codigo Civil arts. 348, 1091, 1255, 1911, 7.2; Codigo Penal arts. 11, 245.2, 311-318, 404, 432, 490.3, 491, 542, 550, 557; Ley 46/1977; LO 4/2015; arts. 53.3, 86 y 135 CE).</p>
<p><strong>2. Primacia del Derecho Internacional de los Derechos Humanos (<code>arts. 10.2 y 96.1 CE</code>):</strong> Redacta 3 parrafos extensos aplicando el control difuso de convencionalidad (art. 31 Ley 25/2014, arts. 26-27 Convencion de Viena, PIDCP, PIDESC, CEDH, CDFUE, Carta Social Europea Revisada y dictamenes de Comites ONU).</p>
<h4>III. JURISPRUDENCIA Y DOCTRINA DE CONTROL</h4>
Redacta 4 parrafos extensos analizando resoluciones concretas y verificadas del TC (v.g. STC 36/1981, STC 140/2018), TS, TEDH, TJUE y Comites de la ONU entre etiquetas <code>...</code>, demostrando como blindan el regimen."""

            p2 = f"""CONTINUA EXACTAMENTE CON LA ESTRUCTURA GOLDEN STANDARD (SECCIONES IV A VI) PARA: {titulo} ({bloque})
FUENTES DOCTRINALES DE CEREBRO_FILOSOFICO.DB:
{citas_rag}

RECLAMACIONES Y COLECTIVOS VINCULADOS:
{recl_exactas}

USA SOLO HTML LIMPIO (NUNCA MARKDOWN) Y EXPLAYATE CON MAXIMA PROFUNDIDAD:
<h4>IV. INDICADORES EMPIRICOS Y DATOS OFICIALES</h4>
Redacta 4 parrafos extensos contrastando el precepto con cifras verificables de Eurostat, INE, Banco de España, IGAE, CGPJ, FGE, CIS y Defensor del Pueblo: tasa AROPE >26%, esfuerzo en alquiler >40% frente al tope del 20%, concentracion patrimonial frente al techo de 1.709.400 EUR (SMI anual 17.094 EUR x 100), RBU de 1.147 EUR/mes, y la asimetria temporal entre celeridad punitiva contra poblacion vulnerable y dilaciones >8 anos en delitos de cuello blanco.
<h4>V. MARCO TEORICO Y APARATO CRITICO</h4>
Redacta 4 parrafos extensos en prosa doctoral continua aplicando el Protocolo de Cita Organica Avanzada con citas literales entre comillas («...») extraidas de los autores aportados y de la critica radical (Proudhon, Bakunin, Kropotkin, Stirner, Rocker, Cappelletti, Pi y Margall, Goldman, Bookchin, Althusser, Foucault, Radbruch), indicando siempre Autor en «Obra».
<h4>VI. RECLAMACIONES DE MINIMOS DE LOS COLECTIVOS ALIADOS</h4>
Redacta una lista <ul> con 4 puntos extensos titulando y numerando cada reclamacion junto al colectivo aliado (ejemplo: <li><strong>1. Titulo completo de la reclamacion — junto al colectivo afectado:</strong> ...</li>) en PRIMERA PERSONA POLITICA ("hacemos nuestra", "asumimos como propia", "exigimos"), integrando tambien las pautas de litigacion tecnica (Lex Lata) y la apertura del art. 168 CE hacia los 5 ejes post-constituyentes (minimos garantizados, techo 1.709.400 EUR con Proof of Human, red rural ecologica, subordinacion libre de la IA y autogestion comunal). Exclusivamente colectivos oprimidos (prohibido incluir cuerpos policiales o militares)."""

            '''

open("app.py", "w", encoding="utf-8").write(s[:i] + bloque_fusion + s[j:])
print("OK: Estructura Golden Standard (I a VI) fusionada con profundidad extendida.")
