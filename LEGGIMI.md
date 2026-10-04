# followthesandro – sito in locale

Avvio: da questa cartella `python -m http.server 8080`, poi vai su http://localhost:8080

## Lingue (EN principale, poi ES e IT)
- Inglese nella cartella principale: `index.html`, `shop.html`, `about.html`, `contact.html`
- Spagnolo in `es/`: `index.html`, `tienda.html`, `sobre-mi.html`, `contacto.html`
- Italiano in `it/`: `index.html`, `negozio.html`, `chi-sono.html`, `contatti.html`
- Le pagine HTML sono generate da `strumenti/genera_pagine.py` leggendo `dati/testi/*.json` e `dati/impostazioni.json` (Netlify lo fa a ogni pubblicazione; in locale lo fa `AVVIA-SITO.bat`). Le pagine generate non sono salvate su GitHub.
- Testi (3 lingue), foto delle sezioni, video, social, partner e tariffe di spedizione si cambiano dal pannello /admin.
- I nomi delle opere (tre lingue) si cambiano dal pannello; i testi del carrello sono in `assets/script.js` e `assets/checkout.js`.

## Opere, foto e prezzi: pannello di gestione
- Doppio clic su `AVVIA-SITO.bat`: si aprono sito e pannello (http://localhost:8080/admin), clic su "Accedi".
- Negozio → Opere in vendita: aggiungi, modifica, riordina (trascinando) o elimina le opere; trascina le foto nel campo Foto; poi "Pubblica" → "Pubblica ora".
- I dati finiscono in `dati/prodotti.json`, le foto in `assets/prodotti/`.
- Ogni opera ha un "Numero opera" unico: non cambiarlo dopo averlo messo (serve al carrello).
- "Venduto" lascia l'opera visibile ma non acquistabile.
- Online il pannello va collegato all'hosting (es. Netlify + GitHub): impostazione `backend` in `admin/config.yml`.

## Video di sfondo della home
- Metti il video in `assets/video/sfondo.mp4` (senza audio, 10–20 secondi in loop, 1280×720, sotto i 5 MB).
- Finché non c'è, si vede `segnaposto.webm` (animazione provvisoria).
- La trasparenza si regola in `assets/style.css` con `--video-opacita` (0 = invisibile, 1 = pieno).

## Carrello e checkout
- Pagine: `cart.html` / `checkout.html` (EN), `es/carrito.html` / `es/pago.html`, `it/carrello.html` / `it/checkout.html`
- Tariffe di spedizione: pannello → Impostazioni → Tariffe di spedizione (file `dati/spedizioni.json`). Sono quelle del listino Correos 2026 Canarie (Paq Estándar / Paq Premium, nazionale e internazionale), con le zone di Correos. Regole delle tasse in cima a `assets/checkout.js`.
- Zone Correos: Canarie (CAP 35/38), Spagna peninsulare e Baleari, Portogallo, Europa 1-2-3, America, Asia, Oceania, Africa, più "mondo" per i paesi non elencati.
- Tasse: nessuna IGIC (esente come autonomo; si riattiva in `TASSE.igic`); IVA del paese UE incassata al checkout fino a 150 € di merce (IOSS); sopra i 150 € e fuori UE le paga il cliente alla consegna. Da far confermare al gestor.
- Per ogni opera nel pannello: peso del pacco pronto e misure del pacco (cm). Il checkout usa il maggiore tra peso reale e volumetrico (L×A×P ÷ 6000), come Correos.
- Il pagamento non è ancora collegato (prossimo passo: Stripe).

## Altro
- `assets/style.css` – colori e font in cima al file (variabili `:root`)
- `assets/logo.png` – logo con sfondo trasparente (anche `logo-piccolo.png` e `favicon.png`)
- Testi inventati, prezzi e partner sono da confermare. Carrello e form sono dimostrativi.
