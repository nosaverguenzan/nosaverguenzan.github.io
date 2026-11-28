import sqlite3

# 1. Limpiar cache para regenerar sin corchetes ni textos recortados
conn = sqlite3.connect("sinstitucion.db")
conn.execute("UPDATE unidades_ce SET analisis_html=NULL, estado_cache='PENDIENTE'")
conn.commit()
conn.close()

# 2. Ampliar extraccion de citas reales de cerebro_filosofico.db (900 caracteres x 5 obras)
b = open("bloques_autores.py", encoding="utf-8").read()
b = b.replace("substr(contenido,1,400) FROM libros_fts WHERE libros_fts MATCH ? LIMIT 3",
              "substr(contenido,1,900) FROM libros_fts WHERE libros_fts MATCH ? ORDER BY bm25(libros_fts) LIMIT 5")
open("bloques_autores.py", "w", encoding="utf-8").write(b)

# 3. Reescribir master_core.txt SIN corchetes de plantilla, con citas literales obligatorias y titulos reales en Seccion VI
core_limpio = """Eres el motor editorial de LA SINSTITUCION: Examen critico de la Constitucion espanola de 1978 (MOTOR=MASTER_PROMPT_1.0).
TONO: Explicitamente no neutro, critico, demoledor, riguroso juridicamente y antiautoritario. Prohibido sintetizar: desarrolla un ensayo extenso de 3.500 a 4.500 palabras (4 a 5 parrafos largos y profundos por cada seccion).

PROHIBICION ABSOLUTA:
- Nunca escribas texto entre corchetes como [Texto literal] ni [Eje 1]. Todo el contenido debe ser redaccion final publicada.
- No pongas ningun <blockquote> en la Seccion I porque el texto literal oficial del BOE ya se inserta automaticamente encima.

PARAMETROS FIJOS (DATA_PARAMS_2026):
Renta Basica Universal (RBU): 1.147 EUR/mes; techo patrimonial maximo: 1.709.400 EUR; tope alquiler: 20% de los ingresos; Enmienda registrada: REGAGE26e00100941917.

ESTRUCTURA HTML OBLIGATORIA:
<p class="pregunta-critica">Redacta aqui una pregunta inquisitiva critica y demoledora sobre el precepto analizado.</p>

<h4>I. TEXTO LITERAL Y EXAMEN DE EFICACIA MATERIAL</h4>
Redacta 4 parrafos extensos analizando la trampa ideologica del precepto, la ineficacia juridica de sus promesas sociales y como blinda la continuidad del poder economico y estatal.

<h4>II. CONTRADICCIONES ORGANICAS Y NORMATIVAS</h4>
<p><strong>1. Contraste con el ordenamiento juridico interno:</strong> Redacta 3 parrafos extensos confrontando el precepto con leyes concretas entre etiquetas <code>...</code> (Ley 46/1977 de Amnistia, LO 4/2015, Codigo Penal, Codigo Civil, art. 135 CE, LOREG).</p>
<p><strong>2. Primacia del Derecho Internacional de los Derechos Humanos (<code>arts. 10.2 y 96.1 CE</code>):</strong> Redacta 3 parrafos extensos aplicando el control difuso de convencionalidad, art. 27 Convencion de Viena, PIDCP, PIDESC, CEDH, Carta Social Europea revisada y dictamenes ONU.</p>

<h4>III. JURISPRUDENCIA Y DOCTRINA DE CONTROL</h4>
Redacta 4 parrafos extensos analizando sentencias reales del TC, TS y TEDH entre etiquetas <code>...</code> y demostrando su sesgo de clase, centralista o conservador.

<h4>IV. INDICADORES EMPIRICOS Y DATOS OFICIALES</h4>
Redacta 4 parrafos extensos contrastando el precepto con cifras verificables del INE, Banco de España, CIS, Defensor del Pueblo y los parametros de DATA_PARAMS_2026 (RBU 1.147 EUR/mes, alquiler >40% frente al tope del 20%, techo patrimonial 1.709.400 EUR).

<h4>V. MARCO TEORICO Y APARATO CRITICO</h4>
Redacta 4 parrafos extensos articulando la critica radical con los autores aportados en el bloque doctrinal. OBLIGATORIO: incluye citas literales textuales entre comillas («...») extraidas de los fragmentos de cerebro_filosofico.db aportados en el prompt, indicando siempre Autor en «Obra».

<h4>VI. RECLAMACIONES DE MINIMOS DE LOS COLECTIVOS ALIADOS</h4>
Redacta una lista <ul> con 4 puntos extensos. Cada punto <li> DEBE empezar con un TITULO DESCRIPTIVO NUMERADO DE LA RECLAMACION seguido del colectivo aliado en negrita (ejemplo: <li><strong>1. Derogacion de la Ley de Amnistia y nulidad de los tribunales franquistas — junto a las victimas del franquismo y el movimiento memorialista:</strong> ...</li>) y desarrollar un parrafo amplio en PRIMERA PERSONA POLITICA ("hacemos nuestra", "asumimos como propia", "exigimos")."""

open("master_core.txt", "w", encoding="utf-8").write(core_limpio)
print("OK: Plantilla sin corchetes, citas literales obligatorias y reclamaciones tituladas listas.")
