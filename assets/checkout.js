/* =====================================================================
   CARRELLO E CHECKOUT
   Tutte le cifre qui sotto sono PROVVISORIE: vanno decise da te
   (spedizioni) e confermate dal gestor (tasse).
   I prezzi delle opere in script.js sono intesi SENZA tasse:
   le tasse si aggiungono al checkout in base alla destinazione.
   ===================================================================== */

/* ----- Spedizione -----
   Le tariffe si cambiano dal pannello /admin (file dati/spedizioni.json).
   Le zone seguono quelle di Correos: ogni zona ha l'elenco dei paesi (codici ISO)
   e due servizi; ogni tariffa vale fino a un peso massimo (kg);
   oltre l'ultima fascia si aggiunge "kg_extra" € per ogni kg in più.
   Zone speciali: "canarie" e "spagna" (Spagna si divide col CAP), "mondo" = paesi non elencati. */
let SPEDIZIONE = { imballoKg: 0.5, gratisDa: 0, zone: {}, zonaPaese: {} };
const CARICA_SPEDIZIONI = fetch(BASE + "dati/spedizioni.json", { cache: "no-cache" })
  .then((r) => r.json())
  .then((d) => {
    const servizio = (s = {}) => ({
      tariffe: (s.tariffe || []).map((t) => [Number(t.fino_a_kg), Number(t.prezzo)]).sort((x, y) => x[0] - y[0]),
      kgExtra: Number(s.kg_extra) || 0,
      giorni: s.giorni || "",
    });
    const zone = {}, zonaPaese = {};
    for (const z of d.zone || []) {
      zone[z.codice] = { standard: servizio(z.standard), express: servizio(z.express) };
      for (const p of z.paesi || []) zonaPaese[String(p).trim().toUpperCase()] = z.codice;
    }
    SPEDIZIONE = { imballoKg: Number(d.imballo_kg) || 0, gratisDa: Number(d.gratis_da) || 0, zone, zonaPaese };
  })
  .catch(() => {});

/* ----- Tasse (da far confermare al gestor) -----
   Fuerteventura è nelle Canarie, fuori dall'area IVA UE:
   - destinazione Canarie: IGIC
   - destinazione UE (anche Spagna peninsulare e Baleari): esportazione senza IGIC;
     con IOSS l'IVA del paese di arrivo si incassa al checkout per ordini fino a 150 € di merce,
     sopra i 150 € IVA e dazi li paga il cliente alla consegna
   - fuori UE: IVA/dazi locali pagati dal cliente alla consegna */
const TASSE = {
  igic: 0,             // esente IGIC come autonomo (franquicia); se cambia, es. 0.07 per il 7%
  ioss: true,
  iossSoglia: 150,
  ivaUE: {
    AT: .20, BE: .21, BG: .20, HR: .25, CY: .19, CZ: .21, DK: .25, EE: .24, FI: .255, FR: .20,
    DE: .19, GR: .24, HU: .27, IE: .23, IT: .22, LV: .21, LT: .21, LU: .17, MT: .18, NL: .21,
    PL: .23, PT: .23, RO: .21, SK: .23, SI: .22, ES: .21, SE: .25,
  },
};


const T_CO = {
  en: {
    vuoto: "Your cart is empty.", torna: "Browse the works", rimuovi: "Remove", subtotale: "Subtotal",
    notaTasse: "Shipping and taxes are calculated at checkout.", vaiCheckout: "Go to checkout",
    spedizione: "Shipping", tasse: "Taxes", totale: "Total", scegliPaese: "Choose a country",
    standard: "Standard", express: "Express", giorni: (g) => `${g} working days`, gratis: "Free",
    serveIndirizzo: "Enter country and postcode to see the shipping options.",
    igic: "IGIC Canary Islands (7%)", iva: (p) => `VAT ${p}% (destination country)`,
    notaIoss: "VAT of the destination country is included: nothing more to pay on delivery.",
    notaSoglia: "Orders over €150 shipped to the EU: VAT and any duties are paid by the customer on delivery.",
    notaMondo: "Shipping outside the EU: any import taxes and duties are paid by the customer on delivery.",
    notaCanarie: "Delivery within the Canary Islands: IGIC included.",
    paga: "Proceed to payment", demoPaga: "Payment is not connected yet: this is a preview of the checkout.",
    errori: "Please fill in the highlighted fields.", unico: "One of a kind", giaNelCarrello: "Already in your cart: every piece is unique.",
  },
  es: {
    vuoto: "Tu carrito está vacío.", torna: "Ver las obras", rimuovi: "Quitar", subtotale: "Subtotal",
    notaTasse: "Envío e impuestos se calculan en el pago.", vaiCheckout: "Finalizar compra",
    spedizione: "Envío", tasse: "Impuestos", totale: "Total", scegliPaese: "Elige un país",
    standard: "Estándar", express: "Urgente", giorni: (g) => `${g} días laborables`, gratis: "Gratis",
    serveIndirizzo: "Indica país y código postal para ver las opciones de envío.",
    igic: "IGIC Canarias (7%)", iva: (p) => `IVA ${p}% (país de destino)`,
    notaIoss: "El IVA del país de destino está incluido: no pagarás nada más en la entrega.",
    notaSoglia: "Pedidos de más de 150 € con destino a la UE: el IVA y los posibles aranceles los paga el cliente en la entrega.",
    notaMondo: "Envíos fuera de la UE: los posibles impuestos y aranceles de importación los paga el cliente en la entrega.",
    notaCanarie: "Entrega dentro de Canarias: IGIC incluido.",
    paga: "Ir al pago", demoPaga: "El pago aún no está conectado: esta es una vista previa del checkout.",
    errori: "Completa los campos marcados.", unico: "Pieza única", giaNelCarrello: "Ya está en tu carrito: cada pieza es única.",
  },
  it: {
    vuoto: "Il carrello è vuoto.", torna: "Guarda le opere", rimuovi: "Rimuovi", subtotale: "Subtotale",
    notaTasse: "Spedizione e tasse vengono calcolate al checkout.", vaiCheckout: "Vai al checkout",
    spedizione: "Spedizione", tasse: "Tasse", totale: "Totale", scegliPaese: "Scegli un paese",
    standard: "Standard", express: "Express", giorni: (g) => `${g} giorni lavorativi`, gratis: "Gratis",
    serveIndirizzo: "Inserisci paese e CAP per vedere le opzioni di spedizione.",
    igic: "IGIC Canarie (7%)", iva: (p) => `IVA ${p}% (paese di destinazione)`,
    notaIoss: "L'IVA del paese di destinazione è inclusa: alla consegna non paghi altro.",
    notaSoglia: "Ordini sopra i 150 € verso l'UE: IVA ed eventuali dazi li paga il cliente alla consegna.",
    notaMondo: "Spedizioni fuori UE: eventuali tasse e dazi di importazione li paga il cliente alla consegna.",
    notaCanarie: "Consegna nelle Canarie: IGIC incluso.",
    paga: "Procedi al pagamento", demoPaga: "Il pagamento non è ancora collegato: questa è un'anteprima del checkout.",
    errori: "Completa i campi evidenziati.", unico: "Pezzo unico", giaNelCarrello: "È già nel carrello: ogni pezzo è unico.",
  },
}[LINGUA];

/* ----- Calcoli ----- */
function zonaDi(paese, cap) {
  if (paese === "ES") {
    const pr = String(cap || "").trim().slice(0, 2);
    if (pr === "35" || pr === "38") return "canarie";
    return "spagna";
  }
  return SPEDIZIONE.zonaPaese[paese] || "mondo";
}

/* Come Correos: si paga il maggiore tra peso reale e peso volumetrico (L × A × P in cm ÷ 6000) */
function pesoTassabile(p) {
  const m = p.pacco || {};
  const volumetrico = (Number(m.lunghezza) || 0) * (Number(m.larghezza) || 0) * (Number(m.altezza) || 0) / 6000;
  return Math.max(Number(p.peso) || 1, volumetrico);
}

function prezzoSpedizione({ tariffe, kgExtra }, kg) {
  for (const [max, prezzo] of tariffe) if (kg <= max) return prezzo;
  const [max, prezzo] = tariffe[tariffe.length - 1];
  return Math.round((prezzo + Math.ceil(kg - max) * kgExtra) * 100) / 100;
}

function articoliCarrello() {
  return leggiCarrello().map((id) => PRODOTTI.find((p) => p.id === id)).filter((p) => p && !p.venduto);
}

function calcola(articoli, paese, cap, servizio) {
  const subtotale = articoli.reduce((s, p) => s + p.prezzo, 0);
  const r = { subtotale, spedizione: null, tasse: 0, etichettaTasse: "", nota: "", opzioni: [] };
  if (!paese) return { ...r, totale: subtotale };
  const zona = zonaDi(paese, cap);
  const kg = articoli.reduce((s, p) => s + pesoTassabile(p), 0) + SPEDIZIONE.imballoKg;
  r.opzioni = ["standard", "express"].map((tipo) => {
    const z = SPEDIZIONE.zone[zona] && SPEDIZIONE.zone[zona][tipo];
    if (!z || !z.tariffe.length) return null;
    let prezzo = prezzoSpedizione(z, kg);
    if (tipo === "standard" && SPEDIZIONE.gratisDa && subtotale >= SPEDIZIONE.gratisDa) prezzo = 0;
    return { tipo, prezzo, giorni: z.giorni };
  }).filter(Boolean);
  if (!r.opzioni.length) return { ...r, totale: subtotale };
  const scelta = r.opzioni.find((o) => o.tipo === servizio) || r.opzioni[0];
  r.servizio = scelta.tipo;
  r.spedizione = scelta.prezzo;
  const base = subtotale + r.spedizione;
  if (zona === "canarie") {
    if (TASSE.igic) { r.tasse = base * TASSE.igic; r.etichettaTasse = T_CO.igic; r.nota = T_CO.notaCanarie; }
  } else if (TASSE.ivaUE[paese]) {
    if (TASSE.ioss && subtotale <= TASSE.iossSoglia) {
      const aliquota = TASSE.ivaUE[paese];
      r.tasse = base * aliquota; r.etichettaTasse = T_CO.iva(+(aliquota * 100).toFixed(1)); r.nota = T_CO.notaIoss;
    } else r.nota = T_CO.notaSoglia;
  } else r.nota = T_CO.notaMondo;
  r.tasse = Math.round(r.tasse * 100) / 100;
  r.totale = base + r.tasse;
  return r;
}

/* ----- Pagina carrello ----- */
function mostraCarrello(el) {
  const articoli = articoliCarrello();
  if (!articoli.length) {
    el.innerHTML = `<div class="carrello-vuoto"><p>${T_CO.vuoto}</p><a class="btn" href="${el.dataset.negozio}">${T_CO.torna}</a></div>`;
    return;
  }
  const { subtotale } = calcola(articoli);
  el.innerHTML = `<div class="carrello-layout">
    <ul class="righe-carrello">${articoli.map((p) => `<li>
      <div class="miniatura">${p.foto ? `<img src="${urlFoto(p.foto)}" alt="">` : illustrazione({ ...p, nome: nomeDi(p) })}</div>
      <div><strong>${nomeDi(p)}</strong><span>${CATEGORIE[p.cat][LINGUA]} · ${T_CO.unico}</span></div>
      <span class="prezzo">${euro(p.prezzo)}</span>
      <button type="button" class="rimuovi" data-rimuovi="${p.id}">${T_CO.rimuovi}</button>
    </li>`).join("")}</ul>
    <aside class="riepilogo">
      <div class="riga-totale"><span>${T_CO.subtotale}</span><strong>${euro(subtotale)}</strong></div>
      <p class="nota">${T_CO.notaTasse}</p>
      <a class="btn" href="${el.dataset.checkout}">${T_CO.vaiCheckout}</a>
    </aside>
  </div>`;
}

/* ----- Pagina checkout ----- */
function avviaCheckout(form) {
  const articoli = articoliCarrello();
  const box = document.getElementById("riepilogo-ordine");
  if (!articoli.length) {
    form.closest(".checkout-layout").innerHTML = `<div class="carrello-vuoto"><p>${T_CO.vuoto}</p><a class="btn" href="${form.dataset.negozio}">${T_CO.torna}</a></div>`;
    return;
  }
  const select = form.elements.paese;
  const nomi = new Intl.DisplayNames([LINGUA], { type: "region" });
  const codici = [...new Set([...Object.keys(TASSE.ivaUE), ...Object.keys(SPEDIZIONE.zonaPaese)])].filter((c) => nomi.of(c) && nomi.of(c) !== c);
  select.innerHTML = `<option value="">${T_CO.scegliPaese}</option>` + codici
    .map((c) => [c, nomi.of(c)]).sort((a, b) => a[1].localeCompare(b[1], LINGUA))
    .map(([c, n]) => `<option value="${c}">${n}</option>`).join("");

  const aggiorna = () => {
    const r = calcola(articoli, select.value, form.elements.cap.value, form.querySelector("[name=servizio]:checked")?.value);
    const opz = document.getElementById("opzioni-spedizione");
    opz.innerHTML = r.opzioni.length
      ? r.opzioni.map((o) => `<label class="opzione"><input type="radio" name="servizio" value="${o.tipo}"${o.tipo === r.servizio ? " checked" : ""} required>
          <span><strong>${T_CO[o.tipo]}</strong><small>${T_CO.giorni(o.giorni)}</small></span><b>${o.prezzo ? euro(o.prezzo) : T_CO.gratis}</b></label>`).join("")
      : `<p class="nota">${T_CO.serveIndirizzo}</p>`;
    box.innerHTML = `<ul class="righe-riepilogo">${articoli.map((p) => `<li><span>${nomeDi(p)}</span><span>${euro(p.prezzo)}</span></li>`).join("")}</ul>
      <div class="riga-totale"><span>${T_CO.subtotale}</span><span>${euro(r.subtotale)}</span></div>
      <div class="riga-totale"><span>${T_CO.spedizione}</span><span>${r.spedizione === null ? "—" : r.spedizione ? euro(r.spedizione) : T_CO.gratis}</span></div>
      ${r.etichettaTasse ? `<div class="riga-totale"><span>${r.etichettaTasse}</span><span>${euro(r.tasse)}</span></div>` : ""}
      <div class="riga-totale grande"><span>${T_CO.totale}</span><strong>${euro(r.totale)}</strong></div>
      ${r.nota ? `<p class="nota">${r.nota}</p>` : ""}`;
  };
  form.addEventListener("input", aggiorna);
  form.addEventListener("change", aggiorna);
  aggiorna();

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const esito = form.querySelector(".esito");
    if (!form.checkValidity()) { form.classList.add("validato"); esito.textContent = T_CO.errori; return; }
    esito.textContent = T_CO.demoPaga;
  });
  form.querySelector("[type=submit]").addEventListener("click", () => form.classList.add("validato"));
}

document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-rimuovi]");
  if (!b) return;
  salvaCarrello(leggiCarrello().filter((id) => id !== Number(b.dataset.rimuovi)));
  aggiornaConta();
  mostraCarrello(document.getElementById("carrello-pagina"));
});

document.addEventListener("DOMContentLoaded", async () => {
  await Promise.all([CARICA_PRODOTTI, CARICA_SPEDIZIONI]);
  const c = document.getElementById("carrello-pagina");
  if (c) mostraCarrello(c);
  const f = document.getElementById("form-checkout");
  if (f) avviaCheckout(f);
});
