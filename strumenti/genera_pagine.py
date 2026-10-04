# Genera le pagine HTML del sito nelle tre lingue, leggendo i file in dati/.
#   EN (principale) -> cartella principale:  index.html, shop.html ...
#   ES              -> cartella es/
#   IT              -> cartella it/
# I testi, le foto delle sezioni, i social e i partner si cambiano dal pannello /admin
# (file dati/testi/*.json e dati/impostazioni.json).
# Netlify lancia questo script a ogni pubblicazione; in locale lo lancia AVVIA-SITO.bat
# oppure:  python strumenti/genera_pagine.py
import json
from html import escape
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
DATI = RADICE / "dati"
LINGUE = ["en", "es", "it"]          # ordine di priorità
CARTELLA = {"en": "", "es": "es/", "it": "it/"}
PAGINE = ["index", "negozio", "chi-sono", "contatti", "carrello", "checkout", "opera"]
# Nome del file di ogni pagina in ogni lingua
FILE = {
  "en": {"index": "index", "negozio": "shop", "chi-sono": "about", "contatti": "contact", "carrello": "cart", "checkout": "checkout", "opera": "artwork"},
  "es": {"index": "index", "negozio": "tienda", "chi-sono": "sobre-mi", "contatti": "contacto", "carrello": "carrito", "checkout": "pago", "opera": "obra"},
  "it": {"index": "index", "negozio": "negozio", "chi-sono": "chi-sono", "contatti": "contatti", "carrello": "carrello", "checkout": "checkout", "opera": "opera"},
}
# Etichette per l'accessibilità (non visibili)
ARIA = {
  "en": {"carrello": "Cart", "menu": "Open menu", "lingua": "Language"},
  "es": {"carrello": "Carrito", "menu": "Abrir menú", "lingua": "Idioma"},
  "it": {"carrello": "Carrello", "menu": "Apri menu", "lingua": "Lingua"},
}
LOCALE_NUMERI = {"en": ",", "es": ".", "it": "."}   # separatore delle migliaia


def leggi(nome):
    return json.loads((DATI / nome).read_text(encoding="utf-8"))


TESTI = {nome: leggi(f"testi/{nome}.json") for nome in ["comuni", "home", "negozio", "chi-sono", "contatti", "checkout"]}
IMP = leggi("impostazioni.json")

ICONE = {
  "carrello": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 7h12l-1 13H7L6 7z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg>',
  "menu": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
  "vantaggi": [
    '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M7 21c-1-6 1-11 10-16-1 8-4 12-10 16zM7 21l6-8"/></svg>',
    '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 3l8 8M6 5l2-2 4 4-2 2zM12 11l-8 8 1 1 8-8"/></svg>',
    '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/></svg>',
    '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.5 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/></svg>',
  ],
  "social": {
    "instagram": ("Instagram", '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'),
    "facebook": ("Facebook", '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M15 3h-2a4 4 0 0 0-4 4v3H7v4h2v7h4v-7h3l1-4h-4V7a1 1 0 0 1 1-1h2z"/></svg>'),
    "tiktok": ("TikTok", '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 3v11a4 4 0 1 1-4-4"/><path d="M14 3a5 5 0 0 0 5 5"/></svg>'),
  },
}


# ----- Aiuti -----
def e(testo):
    """Testo sicuro dentro l'HTML (i testi arrivano dal pannello)."""
    return escape(str(testo or ""), quote=True)


def paragrafi(testo, rientro="      "):
    blocchi = [b.strip() for b in str(testo or "").replace("\r", "").split("\n\n") if b.strip()]
    return "\n".join(f"{rientro}<p>{e(b).replace(chr(10), '<br>')}</p>" for b in blocchi)


def foto_url(valore):
    """Le foto caricate dal pannello hanno percorsi tipo /assets/foto/x.jpg."""
    return "{P}" + str(valore).lstrip("/")


def media(foto, forma, filo, legno, nome):
    if foto:
        return f'<div class="split-media"><img src="{foto_url(foto)}" alt="{e(nome)}" loading="lazy"></div>'
    return f'<div class="split-media" data-forma="{forma}" data-filo="{filo}" data-legno="{legno}" data-nome="{e(nome)}"></div>'


def numero(valore, l):
    v = float(valore or 0)
    testo = f"{int(v):,}" if v == int(v) else f"{v:,}"
    return testo.replace(",", LOCALE_NUMERI[l])


def link_lingua(da, a, pagina):
    """Percorso relativo dalla pagina in lingua `da` alla stessa pagina in lingua `a`."""
    su = "../" if CARTELLA[da] else ""
    return f"{su}{CARTELLA[a]}{FILE[a][pagina]}.html"


def titolo_pagina(l, pagina):
    tc = TESTI["checkout"][l]
    return {
        "index": TESTI["home"][l]["titolo_pagina"], "negozio": TESTI["negozio"][l]["titolo_pagina"],
        "chi-sono": TESTI["chi-sono"][l]["titolo_pagina"], "contatti": TESTI["contatti"][l]["titolo_pagina"],
        "carrello": tc["carrello_titolo_pagina"], "checkout": tc["titolo_pagina"], "opera": tc["opera_titolo_pagina"],
    }[pagina]


# ----- Parti comuni -----
def testa(l, pagina, c):
    alternative = "\n".join(
        f'<link rel="alternate" hreflang="{x}" href="{link_lingua(l, x, pagina)}">' for x in LINGUE
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{link_lingua(l, "en", pagina)}">'
    extra = '<script src="{P}assets/checkout.js" defer></script>\n' if pagina in ("carrello", "checkout") else ""
    return f"""<!doctype html>
<html lang="{l}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titolo_pagina(l, pagina))}</title>
<meta name="description" content="{e(c['descrizione_sito'])}">
{alternative}
<link rel="icon" type="image/png" href="{{P}}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&family=Karla:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{P}}assets/style.css">
<script src="{{P}}assets/script.js" defer></script>
{extra}</head>
<body>
<div class="banner">{e(c['banner'])}</div>
"""


def intestazione(l, pagina, c):
    m = c["menu"]
    voci = [("negozio.html#quadri", m["quadri"], ""), ("negozio.html#mini", m["mini"], ""), ("negozio.html#oggetti", m["oggetti"], ""),
            ("negozio.html#regali", m["regali"], ""), ("contatti.html#personalizza", m["su_misura"], ""),
            ("chi-sono.html", m["chi_sono"], "nav-secondaria"), ("contatti.html", m["contatti"], "nav-secondaria")]
    nav = ""
    for href, testo, cls in voci:
        attivo = (pagina == "chi-sono" and href == "chi-sono.html") or (pagina == "contatti" and href == "contatti.html")
        classi = " ".join(x for x in [cls, "attivo" if attivo else ""] if x)
        nav += f'      <a href="{href}" class="{classi}">{e(testo)}</a>\n'
    corrente = ' class="attiva" aria-current="true"'
    lingue = "".join(
        f'<a href="{link_lingua(l, x, pagina)}" hreflang="{x}" lang="{x}"{corrente if x == l else ""}>{x.upper()}</a>'
        for x in LINGUE
    )
    a = ARIA[l]
    return f"""<header class="header">
  <div class="container">
    <a class="logo" href="index.html"><img src="{{P}}assets/logo-piccolo.png" alt="">followthe<span>sandro</span></a>
    <nav class="nav">
{nav}    </nav>
    <div class="azioni">
      <div class="lingue" role="navigation" aria-label="{a['lingua']}">{lingue}</div>
      <a class="carrello" href="carrello.html" aria-label="{a['carrello']}">
        {ICONE['carrello']}
        <span class="conta" hidden>0</span>
      </a>
      <button class="menu-toggle" type="button" aria-label="{a['menu']}">
        {ICONE['menu']}
      </button>
    </div>
  </div>
</header>
<main>
"""


def piede(c):
    m, f = c["menu"], c["footer"]
    social = []
    for chiave, (nome, svg) in ICONE["social"].items():
        url = (IMP.get("social") or {}).get(chiave)
        if url:
            social.append(f'          <a href="{e(url)}" aria-label="{nome}" target="_blank" rel="noopener">{svg}</a>')
    return f"""</main>
<footer class="footer">
  <div class="container">
    <div class="colonne">
      <div>
        <a class="logo" href="index.html"><img src="{{P}}assets/logo-piccolo.png" alt="">followthe<span>sandro</span></a>
        <p style="margin-top:12px">{e(f['testo'])}</p>
        <div class="social">
{chr(10).join(social)}
        </div>
      </div>
      <div>
        <h4>{e(f['titolo_opere'])}</h4>
        <ul>
          <li><a href="negozio.html#quadri">{e(m['quadri'])}</a></li>
          <li><a href="negozio.html#mini">{e(m['mini'])}</a></li>
          <li><a href="negozio.html#oggetti">{e(m['oggetti'])}</a></li>
          <li><a href="negozio.html#regali">{e(m['regali'])}</a></li>
        </ul>
      </div>
      <div>
        <h4>{e(f['titolo_assistenza'])}</h4>
        <ul>
          <li><a href="#">{e(f['spedizioni'])}</a></li>
          <li><a href="#">{e(f['resi'])}</a></li>
          <li><a href="#">{e(f['cura_legno'])}</a></li>
          <li><a href="contatti.html">{e(f['contatti'])}</a></li>
        </ul>
      </div>
      <div>
        <h4>{e(f['titolo_altro'])}</h4>
        <ul>
          <li><a href="#">{e(f['diario'])}</a></li>
          <li><a href="chi-sono.html">{e(f['chi_sono'])}</a></li>
          <li><a href="contatti.html#personalizza">{e(f['su_misura'])}</a></li>
        </ul>
      </div>
    </div>
    <div class="fondo">
      <span>{e(f['copyright'])}</span>
      <div><a href="#">{e(f['termini'])}</a><a href="#">{e(f['privacy'])}</a><a href="#">{e(f['cookie'])}</a></div>
    </div>
  </div>
</footer>
</body>
</html>
"""


# ----- Pagine -----
def corpo_index(l):
    h = TESTI["home"][l]
    hen = TESTI["home"]["en"]           # le foto sono uguali in tutte le lingue
    passi = "\n".join(f'      <div class="passo"><h3>{e(p["titolo"])}</h3><p>{e(p["testo"])}</p></div>' for p in h["passi"])
    numeri = "\n".join(
        f'      <div class="numero"><strong data-conta="{n["valore"]}"'
        + (f' data-suffisso="{e(n["suffisso"])}"' if n.get("suffisso") else "")
        + f'>{numero(n["valore"], l)}{e(n.get("suffisso", ""))}</strong><span>{e(n["etichetta"])}</span></div>'
        for n in h["numeri"]
    )
    vantaggi = "\n".join(
        f'    <div class="vantaggio">{ICONE["vantaggi"][i % 4]}<strong>{e(v["titolo"])}</strong><span>{e(v["testo"])}</span></div>'
        for i, v in enumerate(h["vantaggi"])
    )
    partner = ""
    for p in IMP.get("partner") or []:
        dentro = f'<img src="{foto_url(p["logo"])}" alt="{e(p["nome"])}">' if p.get("logo") else e(p["nome"])
        partner += (f'<a href="{e(p["link"])}" target="_blank" rel="noopener">{dentro}</a>' if p.get("link") else f"<span>{dentro}</span>")
    video = IMP.get("video") or {}
    sorgente_video = f'\n    <source src="{foto_url(video["file"])}" type="video/mp4">' if video.get("file") else ""
    opacita = video.get("opacita", 0.28)
    titolo = e(h["hero_titolo"]).replace("\n", " <br>")
    return f"""
<section class="hero" style="--video-opacita: {opacita}">
  <video class="hero-video" autoplay muted loop playsinline preload="auto" aria-hidden="true" tabindex="-1">{sorgente_video}
    <source src="{{P}}assets/video/segnaposto.webm" type="video/webm">
  </video>
  <div class="container">
    <img class="logo-grande" src="{{P}}assets/logo.png" alt="follow the Sandro">
    <h1>{titolo}</h1>
    <p class="tagline">{e(h['hero_sottotitolo'])}</p>
    <div class="cta">
      <a class="btn" href="negozio.html">{e(h['hero_pulsante_1'])}</a>
      <a class="btn secondario" href="contatti.html#personalizza">{e(h['hero_pulsante_2'])}</a>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="titolo-sezione">
      <span class="occhiello">{e(h['nuove_occhiello'])}</span>
      <h2>{e(h['nuove_titolo'])}</h2>
    </div>
    <div class="griglia" id="ultima-collezione"></div>
  </div>
</section>

<section class="sfondo-sabbia">
  <div class="container split">
    {media(hen.get('legno_foto'), 'isola', '#2a211b', '#d8b98f', h['legno_titolo'])}
    <div class="split-testo">
      <span class="occhiello">{e(h['legno_occhiello'])}</span>
      <h2>{e(h['legno_titolo'])}</h2>
{paragrafi(h['legno_testo'])}
      <a class="btn" href="chi-sono.html">{e(h['legno_pulsante'])}</a>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="titolo-sezione">
      <span class="occhiello">{e(h['processo_occhiello'])}</span>
      <h2>{e(h['processo_titolo'])}</h2>
      <p>{e(h['processo_testo'])}</p>
    </div>
    <div class="passi">
{passi}
    </div>
  </div>
</section>

<section class="sfondo-scuro">
  <div class="container">
    <div class="titolo-sezione">
      <span class="occhiello" style="color:var(--arancio)">{e(h['numeri_occhiello'])}</span>
      <h2>{e(h['numeri_titolo'])}</h2>
    </div>
    <div class="numeri">
{numeri}
    </div>
  </div>
</section>

<section class="sfondo-sabbia">
  <div class="container">
    <div class="titolo-sezione">
      <span class="occhiello">{e(h['preferite_occhiello'])}</span>
      <h2>{e(h['preferite_titolo'])}</h2>
    </div>
    <div class="griglia" id="piu-popolari"></div>
  </div>
</section>

<section>
  <div class="container split inverti">
    {media(hen.get('misura_foto'), 'van', '#3f6331', '#c9a27a', h['misura_titolo'])}
    <div class="split-testo">
      <span class="occhiello">{e(h['misura_occhiello'])}</span>
      <h2>{e(h['misura_titolo'])}</h2>
{paragrafi(h['misura_testo'])}
      <a class="btn" href="contatti.html#personalizza">{e(h['misura_pulsante'])}</a>
    </div>
  </div>
</section>

<section class="sfondo-sabbia">
  <div class="container vantaggi">
{vantaggi}
  </div>
</section>

<section>
  <div class="container">
    <div class="titolo-sezione">
      <span class="occhiello">{e(h['partner_occhiello'])}</span>
      <h2>{e(h['partner_titolo'])}</h2>
    </div>
    <div class="loghi">{partner}</div>
  </div>
</section>
"""


def corpo_negozio(l):
    n, m = TESTI["negozio"][l], TESTI["comuni"][l]["menu"]
    return f"""
<div class="intestazione-pagina"><div class="container"><h1>{e(n['titolo'])}</h1><p>{e(n['sottotitolo'])}</p></div></div>
<section>
  <div class="container">
    <div class="filtri">
      <button data-cat="tutti">{e(n['filtro_tutte'])}</button>
      <button data-cat="quadri">{e(m['quadri'])}</button>
      <button data-cat="mini">{e(m['mini'])}</button>
      <button data-cat="oggetti">{e(m['oggetti'])}</button>
      <button data-cat="regali">{e(m['regali'])}</button>
    </div>
    <div class="griglia" id="negozio"></div>
  </div>
</section>
"""


def corpo_chi_sono(l):
    c = TESTI["chi-sono"][l]
    return f"""
<div class="intestazione-pagina"><div class="container"><h1>{e(c['titolo'])}</h1><p>{e(c['sottotitolo'])}</p></div></div>
<section>
  <div class="container split">
    {media(TESTI['chi-sono']['en'].get('foto'), 'tavola', '#3f6331', '#b8875a', c['titolo_sezione'])}
    <div class="split-testo testo-lungo">
      <span class="occhiello">{e(c['occhiello'])}</span>
      <h2>{e(c['titolo_sezione'])}</h2>
{paragrafi(c['testo'])}
      <a class="btn" href="contatti.html">{e(c['pulsante'])}</a>
    </div>
  </div>
</section>
"""


def corpo_contatti(l):
    c = TESTI["contatti"][l]
    opzioni = "\n".join(f"          <option>{e(o)}</option>" for o in c["motivi"])
    return f"""
<div class="intestazione-pagina"><div class="container"><h1>{e(c['titolo'])}</h1><p>{e(c['sottotitolo'])}</p></div></div>
<section id="personalizza">
  <div class="container">
    <form class="form">
      <label>{e(c['campo_nome'])} <input name="nome" required></label>
      <label>{e(c['campo_email'])} <input type="email" name="email" required></label>
      <label>{e(c['campo_motivo'])}
        <select name="motivo">
{opzioni}
        </select>
      </label>
      <label>{e(c['campo_messaggio'])} <textarea name="messaggio" required></textarea></label>
      <button class="btn" type="submit">{e(c['pulsante'])}</button>
      <p class="esito" aria-live="polite"></p>
    </form>
  </div>
</section>
"""


def corpo_carrello(l):
    return f"""
<div class="intestazione-pagina"><div class="container"><h1>{e(TESTI['checkout'][l]['carrello_titolo'])}</h1></div></div>
<section>
  <div class="container" id="carrello-pagina" data-negozio="negozio.html" data-checkout="checkout.html"></div>
</section>
"""


def corpo_checkout(l):
    t = TESTI["checkout"][l]
    c = {k: e(v) for k, v in t["etichette"].items()}
    return f"""
<div class="intestazione-pagina"><div class="container"><h1>{e(t['titolo'])}</h1><p>{e(t['sottotitolo'])}</p></div></div>
<section>
  <div class="container checkout-layout">
    <form class="form form-checkout" id="form-checkout" data-negozio="negozio.html" novalidate>
      <fieldset>
        <legend>{c['contatto']}</legend>
        <label>{c['email']} <input type="email" name="email" autocomplete="email" required></label>
        <label>{c['tel']} <input type="tel" name="telefono" autocomplete="tel" required></label>
      </fieldset>
      <fieldset>
        <legend>{c['indirizzo']}</legend>
        <label>{c['paese']} <select name="paese" autocomplete="country" required></select></label>
        <div class="due">
          <label>{c['nome']} <input name="nome" autocomplete="given-name" required></label>
          <label>{c['cognome']} <input name="cognome" autocomplete="family-name" required></label>
        </div>
        <label>{c['via']} <input name="indirizzo" autocomplete="address-line1" required></label>
        <label>{c['via2']} <input name="indirizzo2" autocomplete="address-line2"></label>
        <div class="tre">
          <label>{c['cap']} <input name="cap" autocomplete="postal-code" required></label>
          <label>{c['citta']} <input name="citta" autocomplete="address-level2" required></label>
          <label>{c['prov']} <input name="provincia" autocomplete="address-level1"></label>
        </div>
      </fieldset>
      <fieldset>
        <legend>{c['metodo']}</legend>
        <div id="opzioni-spedizione"></div>
      </fieldset>
      <label>{c['note']} <textarea name="note" rows="3"></textarea></label>
      <label class="spunta"><input type="checkbox" name="termini" required> {c['termini']}</label>
      <button class="btn" type="submit">{c['paga']}</button>
      <p class="esito" aria-live="polite"></p>
    </form>
    <aside class="riepilogo">
      <h2>{c['riepilogo']}</h2>
      <div id="riepilogo-ordine"></div>
    </aside>
  </div>
</section>
"""


def corpo_opera(l):
    return """
<section>
  <div class="container" id="scheda-opera" data-negozio="negozio.html"></div>
</section>
"""


CORPI = {"index": corpo_index, "negozio": corpo_negozio, "chi-sono": corpo_chi_sono, "contatti": corpo_contatti,
         "carrello": corpo_carrello, "checkout": corpo_checkout, "opera": corpo_opera}

for l in LINGUE:
    c = TESTI["comuni"][l]
    cartella = RADICE / CARTELLA[l]
    cartella.mkdir(exist_ok=True)
    prefisso = "../" if CARTELLA[l] else ""
    for pagina in PAGINE:
        html = testa(l, pagina, c) + intestazione(l, pagina, c) + CORPI[pagina](l) + piede(c)
        html = html.replace("{P}", prefisso)
        for chiave in ["negozio", "chi-sono", "contatti", "carrello", "checkout"]:   # link interni -> nomi file della lingua
            html = html.replace(f'="{chiave}.html', f'="{FILE[l][chiave]}.html')
        nome = FILE[l][pagina] + ".html"
        (cartella / nome).write_text(html, encoding="utf-8")
        print("scritto", CARTELLA[l] + nome)
