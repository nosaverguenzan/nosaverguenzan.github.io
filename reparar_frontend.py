h = open("index.html", encoding="utf-8").read()
i = h.find("<script>")
j = h.find("</script>") + 9

script_limpio = """<script>
let catalogo = [];
async function init() {
  const r = await fetch('/api/catalogo');
  const d = await r.json();
  catalogo = d.unidades || [];
  renderSelector(catalogo);
  mostrarGuiaInicio();
}
function renderSelector(lista) {
  const sel = document.getElementById('selectorUnidad');
  sel.innerHTML = '<option value="GUIA_INICIO">— Guia de Uso y Presentacion de la Herramienta —</option>' +
    lista.map(u => `<option value="${u.id}">${u.titulo} (${u.bloque})</option>`).join('');
}
function mostrarGuiaInicio() {
  document.getElementById('docBloque').textContent = "PRESENTACION · MOTOR MASTER PROMPT 1.0";
  document.getElementById('docTitulo').textContent = "Guia de Uso: Auditor Constitucional Interactivo";
  document.getElementById('docContenido').innerHTML = `<p class="pregunta-critica">¿Que es esta herramienta y como auditar cualquier precepto de la Constitucion de 1978?</p>
    <h4>I. PROPOSITO DE LA PLATAFORMA</h4><p><strong>LA SINSTITUCION</strong> somete las <strong>185 unidades normativas</strong> de la Constitucion espanola a un examen material, juridico y antiautoritario en seis secciones calibradas bajo el <strong>Master Prompt 1.0</strong>.</p>
    <h4>II. USO RAPIDO</h4><ul><li><strong>1. Elige un precepto:</strong> Selecciona cualquier articulo o disposicion en el desplegable superior.</li><li><strong>2. Consulta o audita:</strong> Los preceptos auditados abren al instante; pulsa <strong>Auditar</strong> para regenerar en vivo.</li><li><strong>3. Exporta:</strong> Pulsa <strong>PDF</strong> para descargar el expediente maquetado.</li></ul>`;
  document.getElementById('selloBOE').textContent = "Base de datos: 185 unidades CE sincronizadas con BOE";
}
async function cargarUnidad(uid, forzar=false) {
  if (!uid || uid === 'GUIA_INICIO') { mostrarGuiaInicio(); return; }
  const selTxt = document.getElementById('selectorUnidad').selectedOptions[0]?.text || uid;
  document.getElementById('docBloque').textContent = "EN CURSO · MASTER PROMPT 1.0";
  document.getElementById('docTitulo').textContent = selTxt;
  document.getElementById('docContenido').innerHTML = "<p>Ejecutando auditoria bajo Master Prompt 1.0...</p>";
  try {
    const res = await fetch(`/api/unidad/${uid}?forzar=${forzar}`);
    const data = await res.json();
    if (!res.ok) {
      document.getElementById('docContenido').innerHTML = `<div class="callout-info">${data.detail || 'Error del servidor'}</div>`;
      return;
    }
    document.getElementById('docBloque').textContent = `${data.bloque} · ${data.origen}`;
    document.getElementById('docTitulo').textContent = data.titulo;
    document.getElementById('docContenido').innerHTML = data.analisis_html;
    document.getElementById('selloBOE').textContent = `SHA-256 BOE: ${(data.hash_texto||'').substring(0,16)}... · Fecha: ${data.fecha_auditoria}`;
  } catch (e) {
    document.getElementById('docContenido').innerHTML = `<div class="callout-info">Error de red: ${e}</div>`;
  }
}
async function sincronizarBOE() {
  document.getElementById('selloBOE').textContent = "Verificando BOE...";
  const r = await fetch('/api/sincronizar-boe', {method: 'POST'});
  const d = await r.json();
  document.getElementById('selloBOE').textContent = d.mensaje;
}
document.getElementById('buscador').addEventListener('input', e => {
  const q = e.target.value.toLowerCase();
  renderSelector(catalogo.filter(u => u.titulo.toLowerCase().includes(q) || u.bloque.toLowerCase().includes(q)));
});
document.getElementById('selectorUnidad').addEventListener('change', e => cargarUnidad(e.target.value, false));
init();
</script>"""

open("index.html", "w", encoding="utf-8").write(h[:i] + script_limpio + h[j:])
print("OK: Frontend sincronizado con /api/unidad/")
