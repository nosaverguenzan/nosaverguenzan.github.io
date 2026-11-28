let indice = [];
let vistaRapida = false;
asociarEventos();
iniciarWeb();

async function iniciarWeb() {
  try {
    const r = await fetch("./data/search_index.json");
    indice = await r.json();
    renderizarLista(indice);
    const params = new URLSearchParams(window.location.search);
    const idInicial = params.get("doc") || (indice[0] ? indice[0].id : null);
    if (idInicial) await cargarDocumento(idInicial);
  } catch (e) {
    document.getElementById("contenido-ficha").textContent = "Error cargando indice: " + e.message;
  }
}

function renderizarLista(lista) {
  const cont = document.getElementById("lista-resultados") || document.getElementById("lista-resultados");
  cont.textContent = "";
  lista.forEach(item => {
    const btn = document.createElement("button");
    btn.className = "btn";
    btn.style.margin = "0.2rem";
    btn.textContent = `${item.titulo} (${item.boe_id})`;
    btn.onclick = () => cargarDocumento(item.id);
    cont.appendChild(btn);
  });
}

async function cargarDocumento(id) {
  const item = indice.find(x => x.id === id);
  if (!item) return;
  const r = await fetch("./" + item.ruta);
  const doc = await r.json();
  const cont = document.getElementById("contenido-ficha");
  cont.textContent = "";

  const h1 = document.createElement("h2");
  h1.textContent = doc.titulo_encabezado.replace(/^#+\s*/, "");
  cont.appendChild(h1);

  const sub = document.createElement("p");
  sub.style.fontWeight = "bold";
  sub.textContent = doc.subtitulo_pregunta;
  cont.appendChild(sub);

  const boe = document.createElement("div");
  boe.className = "banda-boe";
  const u = doc.ultima_interpretacion;
  boe.textContent = `Ultima interpretacion BOE: ${u.fecha} | Estado: ${u.estado_vigencia} | Referencia: `;
  const a = document.createElement("a");
  a.href = u.url_oficial;
  a.target = "_blank";
  a.rel = "noopener noreferrer";
  a.textContent = u.boe_id;
  boe.appendChild(a);
  cont.appendChild(boe);

  const cita = document.createElement("blockquote");
  cita.className = "cita-literal";
  cita.textContent = doc.cita_literal_bloque;
  cont.appendChild(cita);

  const titulosSec = {
    i_texto_literal_y_eficacia: "I. TEXTO LITERAL Y EXAMEN DE EFACIA material",
    ii_contradicciones_organicas: "II. CONTRADICCIONES ORGÁNICAS Y NORMATIVAS",
    iii_jurispridencia_control: "III. JURISPRUDENCIA Y DOCTRINA DE CONTROL",
    iv_indicadores_empiricos: "IV. INDICADORES EMPÍRICOS Y DATOS OFICIALES",
    v_marco_teorico_critico: "V. MARCO TEÓRICO Y APARATO CRÍTICO",
    vi_reclamaciones_minimos: "VI.
RECLAMACIONES DE MÍNIMOS"
  };

  Object.entries(doc.secciones).forEach(([k, v], idx) => {
    if (vistaRapida&& idx !== 0 && idx !== 5) return;
    const bloq = document.createElement("div");
    bloq.className = "seccion-bloque";
    const h3 = document.createElement("h3");
    h3.textContent = titulosSec[k];
    const p = document.createElement("p");
    p.style.whiteSpace = "pre-line";
    p.textContent = v;
    bloq.appendChild(h3);
    bloq.appendChild(p);
    cont.appendChild(bloq);
  });

  const cierre = document.createElement("p");
  cierre.className = "cierre";
  cierre.textContent = doc.cierre;
  cont.appendChild(cierre);

  const hash = document.createElement("div");
  hash.className = "hash-bar";
  hash.textContent = `Verificacion SHA256: ${doc.sha256_ficha}`;
  cont.appendChild(hash);
}

function asociarEventos() {
  document.getElementById("btn-imprimir").onclick = () => window.print();
  document.getElementById("btn-imprimir-ia").onclick = () => window.print();
  document.getElementById("btn-vista").onclick = () => {
    vistaRapida = !vistaRapida;
    const params = new URLSearchParams(window.location.search);
    const id = params.get("doc") || (indice[0] ? indice[0].id : null);
    if (id) cargarDocumento(id);
  };
  document.getElementById("tab-docs").onclick = () => {
    document.getElementById("panel-docs").classList.remove("oculto");
    document.getElementById("panel-consultor").classList.add("oculto");
  };
  document.getElementById("tab-ia").onclick = () => {
    document.getElementById("panel-consultor").classList.remove("oculto");
    document.getElementById("panel-docs").classList.add("oculto");
  };
  document.getElementById("buscador").oninput = (e) => {
    const q = e.target.value.toLowerCase();
    renderizarLista(indice.filter(x => x.titulo.toLowerCase().includes(q) || x.boe_id.toLowerCase().includes(q)));
  };
  document.getElementById("btn-copiar-prompt").onclick = () => {
    const txt = document.getElementById("input-ia").value;
    const prompt = `Actua como Auditora Constitucional Forense de La Sinstitucion (GOLD STRANDARD, 6 secciones romanas, cero URLs, citas Autor en "Obra" con ..., parametros 2026: REGAGE26e00100941917, 1.147 euros mensuales, 1.709.400 euros, 20% alquiler) y analiza el siguiente texto:\n\n${txt}`; 
    navigator.clipboard.writeText(prompt);
    document.getElementById("salida-ia").textContent = "Prompt copiado al portapapeles. Pegalo en tu motor IA para obtener el Gold Standard.\n\n" + prompt;
  };
}
