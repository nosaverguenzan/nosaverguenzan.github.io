import sqlite3, re

conn = sqlite3.connect("sinstitucion.db")
conn.execute("UPDATE unidades_ce SET analisis_html=NULL, estado_cache='PENDIENTE'")
conn.commit()
conn.close()

# 1. Guardar el MASTER PROMPT 1.0 autentico (Secciones 1 a 4 + Golden Standard)
master_1_0 = """MÁSTER PROMPT 1.0 — «LA SINSTITUCIÓN» (VERSION 1.0 PRODUCCIÓN FINAL CONSOLIDADA | REGISTRO: REGAGE26e00100941917).
POSICIONAMIENTO EPISTEMOLÓGICO EXPLÍCITAMENTE NO NEUTRO: Auditoría material, jurídica y antiautoritaria de la Constitución Española de 1978 desde las realidades sociales excluidas del pacto transicional.

PARÁMETROS OFICIALES (DATA_PARAMS_2026):
- REGISTRO_ENMIENDA: REGAGE26e00100941917 (UNA_en_blanco.pdf)
- RBU_MENSUAL: 1.147 euros mensuales (universal, incondicional e individual)
- TECHO_PATRIMONIAL: 1.709.400 euros (límite máximo de acumulación patrimonial neta)
- TOPE_ALQUILER: 20 % de los ingresos (frente a la confiscación actual >40 %)

REGLAS INVIOLABLES DE RIGOR Y RENDERIZADO (PROMPT_1 A PROMPT_9):
1. Protección Tipográfica Anti-Hipervínculos: Encierra TODA referencia normativa (<code>Ley 46/1977</code>, <code>STC 36/1981</code>, <code>art. 10.2 CE</code>) y toda operación estadística oficial (<code>Encuesta de Condiciones de Vida</code>, <code>Informe Anual del Defensor del Pueblo</code>) en etiquetas <code>...</code>. Prohibido incluir URLs, enlaces o etiquetas internas.
2. Separación estricta Lex Lata vs. Lex Ferenda: Secciones II y III operan exclusivamente sobre derecho vigente (ordenamiento interno y control difuso de convencionalidad ex <code>arts. 10.2 y 96.1 CE</code>). El programa constituyente completo de 9 macro-ejes queda reservado EN EXCLUSIVA al Artículo 168 CE.
3. Formato obligatorio de citas doctrinales (Sección V): Cita siempre bajo el orden estricto Autor en «Obra», SIN APLICAR NEGRITAS a los nombres de autores ni a los títulos, apoyándote en los extractos de cerebro_filosofico.db aportados.
4. Protocolo de Abstención: Si una cifra, sentencia o cita no consta con certeza verificada, queda prohibido inventarla: sustitúyela por el análisis estructural del mecanismo jurídico o márcala con [DATO_PENDIENTE_VERIFICACION].
5. Exclusión Absoluta: Prohibido incluir fuerzas armadas, cuerpos policiales o aparatos coercitivos como sujetos protegidos o legitimadores.
6. Cierre en seco (EOF): Termina exactamente con <p>_______</p> sin despedidas ni comentarios posteriores.

MATRIZ DE LOS 15 ÁMBITOS DE COLECTIVOS ALIADOS (SECCIÓN 3.1):
(01) Movimiento libertario y autónomo; (02) Movimiento republicano y víctimas del franquismo; (03) Infancia, juventud y generaciones futuras; (04) Personas mayores y en situación de dependencia; (05) Mujeres y feminismos de base; (06) Colectivo LGTBIQA+ y disidencias sexogenéricas; (07) Personas con discapacidad y neurodivergentes; (08) Pueblo gitano, personas migrantes y racializadas; (09) Pueblos sin Estado, mundo rural y bienes comunales; (10) Movimientos ecologistas, antinucleares y ecosistemas; (11) Animales no humanos y movimiento antiespecista; (12) Objetores, insumisos, población reclusa y sin hogar; (13) Movimientos sociales, mareas y defensa de la vivienda; (14) Libertades digitales y soberanía tecnológica; (15) Movimientos anticoloniales y solidaridad internacional (Sáhara Occidental, Palestina)."""

with open("master_core.txt", "w", encoding="utf-8") as f:
    f.write(master_1_0)

# 2. Actualizar app.py con Nivel A / B / C manteniendo SIEMPRE las 6 secciones romanas del Master Prompt 1.0
s = open("app.py", encoding="utf-8").read()
i = s.find("import re as _re")
j = s.find("ahora_ts = time.time()")

bloque_1_0 = '''import re as _re
            m_num = _re.search(r"ART_(\\d+)", uid)
            num_art = int(m_num.group(1)) if m_num else 0
            es_nivel_a = (uid in ["PREAMBULO", "DD_UNICA"] or num_art in)
            es_nivel_b = (not es_nivel_a) and ((1 <= num_art <= 169) and num_art not in)

            densidad_txt = (
                "NIVEL A (ALTA DENSIDAD DOGMÁTICA/MATERIAL): Desarrollo exhaustivo y extenso (3-4 párrafos densos por sección) en las 6 secciones romanas."
                if es_nivel_a else (
                "NIVEL B (DENSIDAD ORGÁNICA MEDIA): Análisis estructural riguroso centrado en bloqueos democráticos y controles institucionales manteniendo las 6 secciones romanas."
                if es_nivel_b else
                "NIVEL C (PRECEPTO PROCEDIMENTAL/TÉCNICO): Síntesis precisa y directa sin relleno retórico, manteniendo intacta la estructura de 6 secciones romanas."
            ))

            p1 = f"""EJECUTA PRIMERA MITAD (SUBTÍTULO + SECCIONES I A III) DEL MÁSTER PROMPT 1.0 PARA: {titulo} ({bloque}).
{densidad_txt}
TEXTO OFICIAL BOE (ya mostrado arriba en pantalla, no lo repitas en blockquote): {texto_oficial}

USA EXCLUSIVAMENTE HTML LIMPIO (NUNCA MARKDOWN ###, **, >):
<p class="pregunta-critica">Subtítulo formulado como pregunta crítica inquisitiva, respetuosa y no neutral que sintetice la contradicción estructural central del precepto.</p>
<h4>I. TEXTO LITERAL Y EXAMEN DE EFICACIA MATERIAL</h4>
<p>Crítica de eficacia material: cómo opera el precepto en la realidad social, qué ficciones jurídicas encubre y a qué sectores excluye.</p>
<h4>II. CONTRADICCIONES ORGÁNICAS Y NORMATIVAS</h4>
<p><strong>1. Contraste con el ordenamiento jurídico interno:</strong> Leyes orgánicas, códigos y reglamentos vigentes que vacían o restringen el precepto (protegidos con <code>...</code>).</p>
<p><strong>2. Primacía del Derecho Internacional de los Derechos Humanos (<code>arts. 10.2 y 96.1 CE</code>):</strong> Tratados ratificados, <code>Convención de Viena</code>, <code>PIDCP</code>, <code>PIDESC</code>, <code>CEDH</code>, <code>Carta Social Europea</code> y obligación judicial de ejercer el control difuso de convencionalidad.</p>
<h4>III. JURISPRUDENCIA Y DOCTRINA DE CONTROL</h4>
<p>Resoluciones clave del Tribunal Constitucional, Tribunal Supremo y órganos supranacionales (TEDH, Comités de la ONU, Comité Europeo de Derechos Sociales) protegidas en <code>...</code> con su doctrina exacta."""

            p2 = f"""CONTINÚA SEGUNDA MITAD (SECCIONES IV A VI + CIERRE _______) DEL MÁSTER PROMPT 1.0 PARA: {titulo} ({bloque}).
{densidad_txt}
EXTRACTOS DOCTRINALES DE CEREBRO_FILOSOFICO.DB:
{citas_rag}

USA EXCLUSIVAMENTE HTML LIMPIO (NUNCA MARKDOWN):
<h4>IV. INDICADORES EMPÍRICOS Y DATOS OFICIALES</h4>
<p>Contrasta las promesas del artículo con estadísticas verificadas nombrando la institución emisora y encerrando en <code>...</code> cada informe oficial (<code>Encuesta de Condiciones de Vida</code> del INE, Banco de España, CIS, <code>Informe Anual del Defensor del Pueblo</code>) junto con DATA_PARAMS_2026 (RBU 1.147 euros/mes, techo patrimonial 1.709.400 euros, alquiler topado al 20 %).</p>
<h4>V. MARCO TEÓRICO Y APARATO CRÍTICO</h4>
<p>Articula la fundamentación filosófica, histórica y antiautoritaria citando las obras aportadas bajo el formato estricto: Autor en «Obra» (PROHIBIDO poner negritas a los autores ni a los títulos).</p>
<h4>VI. RECLAMACIONES DE MÍNIMOS DE LOS COLECTIVOS ALIADOS</h4>
{"<p>Despliega íntegramente en lista <ul> los 9 Macro-Ejes Post-Constituyentes del Máster Prompt 1.0 en primera persona política plural («hacemos nuestra», «exigimos», «asumimos como propio»).</p>" if uid == "ART_168" else "<p>Selecciona ÚNICAMENTE los 4 o 5 colectivos de la Matriz Aliada (15 Ámbitos) directamente golpeados por las cláusulas de este artículo específico. Redacta en lista <ul> cada punto titulando la cláusula criticada + el colectivo aliado en negrita y desarrollando sus exigencias de mínimos en primera persona política plural («hacemos nuestra», «exigimos», «asumimos como propio»).</p>"}
<p>_______</p>"""

            '''

s = s[:i] + bloque_1_0 + s[j:]
s = s.replace("t2 = \"\"\n                        if p2:", "r2 = requests.post(ug, headers=hg, json={\"model\": mod_g, \"messages\": [{\"role\": \"system\", \"content\": sys_prompt}, {\"role\": \"user\", \"content\": p2}], \"max_tokens\": 4096, \"temperature\": 0.35}, timeout=40)\n                        t2 = r2.json()[\"choices\"].__getitem__(0)[\"message\"][\"content\"] if r2.status_code == 200 else \"\"\n                        if False:")
open("app.py", "w", encoding="utf-8").write(s)
print("OK: MÁSTER PROMPT 1.0 (Edición Oficial de Distribución) instalado con precisión quirúrgica.")
