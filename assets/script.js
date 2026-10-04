/* ===== Lingua della pagina e cartella del sito ===== */
const LINGUA = ["en", "es", "it"].includes(document.documentElement.lang) ? document.documentElement.lang : "en";
const BASE = new URL("../", document.currentScript.src).href; // cartella principale del sito
const LOCALE = { en: "en-IE", es: "es-ES", it: "it-IT" }[LINGUA];

/* ===== Opere =====
   Si gestiscono dal pannello /admin (oppure a mano nel file dati/prodotti.json). */
let PRODOTTI = [];
const CARICA_PRODOTTI = fetch(BASE + "dati/prodotti.json", { cache: "no-cache" })
  .then((r) => r.json())
  .then((d) => { PRODOTTI = (d.prodotti || []).map((p) => ({ ...(p.segnaposto || {}), ...p, id: Number(p.id) })); })
  .catch(() => {});
const urlFoto = (f) => BASE + (f.includes("/") ? f.replace(/^\//, "") : "assets/prodotti/" + f);

const CATEGORIE = {
  quadri: { en: "Wall art", es: "Cuadros", it: "Quadri" },
  mini: { en: "Small pieces", es: "Formatos pequeños", it: "Piccoli formati" },
  oggetti: { en: "Objects", es: "Objetos", it: "Oggetti" },
  regali: { en: "Gift ideas", es: "Ideas de regalo", it: "Idee regalo" },
};

/* Testi usati dallo script */
const TESTI = {
  en: { aggiungi: "Add to cart", aggiunto: (n) => `${n} added to cart`, carrello: (q, t) => `Cart: ${q} items, ${t} (payment not active yet)`, vuoto: "Your cart is empty", gia: "Already in your cart: every piece is unique", venduto: "Sold", grazie: "Thank you! Message received (demo: real sending will be connected later)." },
  es: { aggiungi: "Añadir", aggiunto: (n) => `${n} añadido al carrito`, carrello: (q, t) => `Carrito: ${q} artículos, ${t} (pago aún no activo)`, vuoto: "El carrito está vacío", gia: "Ya está en tu carrito: cada pieza es única", venduto: "Vendido", grazie: "¡Gracias! Mensaje recibido (demostración: el envío real se conectará más adelante)." },
  it: { aggiungi: "Aggiungi", aggiunto: (n) => `${n} aggiunto al carrello`, carrello: (q, t) => `Carrello: ${q} articoli, ${t} (pagamento non ancora attivo)`, vuoto: "Il carrello è vuoto", gia: "È già nel carrello: ogni pezzo è unico", venduto: "Venduto", grazie: "Grazie! Messaggio ricevuto (dimostrazione: l'invio reale verrà collegato più avanti)." },
}[LINGUA];
const nomeDi = (p) => p.nome[LINGUA] || p.nome.en;
const attr = (t) => String(t).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");

/* ===== Segnaposto in stile string art: tavola di legno, chiodi e filo ===== */
function casuale(seme) {
  let s = seme * 9301 + 49297;
  return () => ((s = (s * 9301 + 49297) % 233280) / 233280);
}

const FORME = {
  cerchio: () => Array.from({ length: 40 }, (_, i) => { const a = (i / 40) * Math.PI * 2; return [100 + Math.cos(a) * 58, 100 + Math.sin(a) * 58]; }),
  cuore: () => Array.from({ length: 40 }, (_, i) => {
    const t = (i / 40) * Math.PI * 2;
    return [100 + 3.6 * 16 * Math.sin(t) ** 3, 96 - 3.6 * (13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t))];
  }),
  stella: () => Array.from({ length: 10 }, (_, i) => { const a = (i / 10) * Math.PI * 2 - Math.PI / 2, r = i % 2 ? 26 : 64; return [100 + Math.cos(a) * r, 104 + Math.sin(a) * r]; }),
  vulcano: () => [[30, 160], [82, 62], [118, 62], [170, 160]],
  onda: () => [[30, 150], [30, 110], [50, 78], [80, 58], [112, 56], [138, 70], [150, 92], [138, 110], [120, 102], [118, 120], [140, 138], [170, 150]],
  tavola: () => Array.from({ length: 36 }, (_, i) => { const a = (i / 36) * Math.PI * 2; const x = Math.cos(a) * 24, y = Math.sin(a) * 74; const r = 0.5; return [100 + x * Math.cos(r) - y * Math.sin(r), 100 + x * Math.sin(r) + y * Math.cos(r)]; }),
  isola: () => [[128, 22], [150, 30], [160, 52], [150, 74], [146, 98], [128, 118], [108, 130], [92, 138], [70, 146], [44, 160], [26, 172], [22, 162], [40, 146], [62, 128], [80, 114], [92, 92], [104, 70], [112, 46]],
  van: () => [[34, 146], [34, 84], [44, 66], [120, 64], [140, 70], [160, 98], [168, 104], [168, 146], [150, 146], [146, 134], [130, 134], [126, 146], [76, 146], [72, 134], [56, 134], [52, 146]],
};

/* Distribuisce i chiodi in modo uniforme lungo il contorno */
function chiodi(punti, quanti) {
  const lati = punti.map((p, i) => { const q = punti[(i + 1) % punti.length]; return [p, q, Math.hypot(q[0] - p[0], q[1] - p[1])]; });
  const tot = lati.reduce((s, l) => s + l[2], 0);
  const out = [];
  for (let k = 0; k < quanti; k++) {
    let d = (k / quanti) * tot;
    for (const [p, q, len] of lati) {
      if (d <= len) { const t = d / len; out.push([p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t]); break; }
      d -= len;
    }
  }
  return out;
}

function illustrazione(p) {
  const r = casuale(p.id);
  let venature = "";
  for (let i = 0; i < 14; i++) {
    const x = r() * 200, c = (r() - 0.5) * 30;
    venature += `<path d="M${x} 0 Q${x + c} 100 ${x} 200" stroke="#000" stroke-opacity="${0.04 + r() * 0.06}" stroke-width="${1 + r() * 3}" fill="none"/>`;
  }
  const n = chiodi((FORME[p.forma] || FORME.cerchio)(), 44);
  const passo = 13 + (p.id % 5);
  let fili = "";
  for (let i = 0; i < n.length; i++) {
    const a = n[i], b = n[(i * passo + 7) % n.length], c = n[(i + 1) % n.length];
    fili += `<line x1="${a[0].toFixed(1)}" y1="${a[1].toFixed(1)}" x2="${b[0].toFixed(1)}" y2="${b[1].toFixed(1)}"/>`;
    fili += `<line x1="${a[0].toFixed(1)}" y1="${a[1].toFixed(1)}" x2="${c[0].toFixed(1)}" y2="${c[1].toFixed(1)}" stroke-width="1.6"/>`;
  }
  const teste = n.map(([x, y]) => `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="2.1"/>`).join("");
  return `<svg viewBox="0 0 200 200" role="img" aria-label="${attr(p.nome)}">
    <rect width="200" height="200" fill="${p.legno || "#c9a27a"}"/>${venature}
    <g stroke="${p.filo || "#3f6331"}" stroke-width=".7" stroke-opacity=".85">${fili}</g>
    <g fill="#d9d4cc" stroke="#5b5148" stroke-width=".6">${teste}</g>
  </svg>`;
}

const euro = (n) => n.toLocaleString(LOCALE, { style: "currency", currency: "EUR", minimumFractionDigits: 0, maximumFractionDigits: 2 });

function schedaProdotto(p) {
  return `<article class="prodotto">
    <div class="img">${p.foto ? `<img src="${urlFoto(p.foto)}" alt="${attr(nomeDi(p))}" loading="lazy">` : illustrazione({ ...p, nome: nomeDi(p) })}</div>
    <div class="info">
      <span class="cat">${CATEGORIE[p.cat][LINGUA]}</span>
      <h3>${nomeDi(p)}</h3>
      <div class="riga">
        <span class="prezzo">${euro(p.prezzo)}</span>
        ${p.venduto ? `<button type="button" disabled>${TESTI.venduto}</button>` : `<button type="button" data-aggiungi="${p.id}">${TESTI.aggiungi}</button>`}
      </div>
    </div>
  </article>`;
}

function mostraProdotti(contenitore, elenco) {
  if (contenitore) contenitore.innerHTML = elenco.map(schedaProdotto).join("");
}

/* ===== Carrello (solo dimostrativo, salvato nel browser) ===== */
function leggiCarrello() {
  try { return [...new Set(JSON.parse(localStorage.getItem("fts-carrello")) || [])]; } catch { return []; }
}
function salvaCarrello(c) {
  try { localStorage.setItem("fts-carrello", JSON.stringify(c)); } catch {}
}
function aggiornaConta() {
  const n = leggiCarrello().length;
  document.querySelectorAll(".carrello .conta").forEach((el) => { el.textContent = n; el.hidden = n === 0; });
}
function toast(msg) {
  let t = document.querySelector(".toast");
  if (!t) { t = document.createElement("div"); t.className = "toast"; document.body.appendChild(t); }
  t.textContent = msg;
  t.classList.add("visibile");
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove("visibile"), 2200);
}

document.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-aggiungi]");
  if (btn) {
    const p = PRODOTTI.find((x) => x.id === Number(btn.dataset.aggiungi));
    const c = leggiCarrello();
    if (c.includes(p.id)) return toast(TESTI.gia);   // ogni pezzo è unico
    c.push(p.id); salvaCarrello(c);
    aggiornaConta();
    toast(TESTI.aggiunto(nomeDi(p)));
  }
  if (e.target.closest(".menu-toggle")) document.querySelector(".nav").classList.toggle("aperto");
});

/* ===== Contatore animato per i numeri ===== */
function animaNumeri() {
  const els = document.querySelectorAll("[data-conta]");
  if (!els.length) return;
  const avvia = (el) => {
    const fine = Number(el.dataset.conta), suff = el.dataset.suffisso || "", t0 = performance.now();
    const step = (t) => {
      const k = Math.min(1, (t - t0) / 1600), v = Math.round(fine * (1 - (1 - k) ** 3));
      el.textContent = v.toLocaleString(LOCALE) + suff;
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if (!("IntersectionObserver" in window)) return els.forEach(avvia);
  const io = new IntersectionObserver((voci) => voci.forEach((v) => { if (v.isIntersecting) { avvia(v.target); io.unobserve(v.target); } }));
  els.forEach((el) => io.observe(el));
}

/* ===== Avvio pagina ===== */
document.addEventListener("DOMContentLoaded", async () => {
  await CARICA_PRODOTTI;
  mostraProdotti(document.getElementById("ultima-collezione"), PRODOTTI.filter((p) => p.nuovo).slice(0, 4));
  mostraProdotti(document.getElementById("piu-popolari"), PRODOTTI.filter((p) => p.popolare).slice(0, 8));

  const negozio = document.getElementById("negozio");
  if (negozio) {
    const filtri = document.querySelector(".filtri");
    const applica = (cat) => {
      mostraProdotti(negozio, cat === "tutti" ? PRODOTTI : PRODOTTI.filter((p) => p.cat === cat));
      filtri.querySelectorAll("button").forEach((b) => b.classList.toggle("attivo", b.dataset.cat === cat));
    };
    filtri.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (b) { history.replaceState(null, "", "#" + b.dataset.cat); applica(b.dataset.cat); }
    });
    const iniziale = location.hash.slice(1);
    applica(CATEGORIE[iniziale] ? iniziale : "tutti");
    window.addEventListener("hashchange", () => { const h = location.hash.slice(1); if (CATEGORIE[h]) applica(h); });
  }

  const form = document.querySelector("form.form");
  if (form) form.addEventListener("submit", (e) => {
    e.preventDefault();
    form.querySelector(".esito").textContent = TESTI.grazie;
    form.reset();
  });

  document.querySelectorAll("[data-forma]").forEach((el, i) => {
    const d = el.dataset;
    el.innerHTML = illustrazione({ id: 50 + i, forma: d.forma, filo: d.filo, legno: d.legno, nome: d.nome || "" });
  });

  animaNumeri();
  aggiornaConta();
});
