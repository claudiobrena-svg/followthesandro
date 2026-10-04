# followthesandro – sito in locale

Avvio: da questa cartella `python -m http.server 8080`, poi vai su http://localhost:8080

## Lingue (EN principale, poi ES e IT)
- Inglese nella cartella principale: `index.html`, `shop.html`, `about.html`, `contact.html`
- Spagnolo in `es/`: `index.html`, `tienda.html`, `sobre-mi.html`, `contacto.html`
- Italiano in `it/`: `index.html`, `negozio.html`, `chi-sono.html`, `contatti.html`
- Le pagine HTML sono generate da `strumenti/genera_pagine.py`: i testi si cambiano lì, poi `python strumenti/genera_pagine.py`.
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
- Tariffe di spedizione (per zona e peso) e regole delle tasse sono in cima a `assets/checkout.js`: cifre PROVVISORIE.
- Zone: Canarie (CAP 35xxx/38xxx), Spagna peninsulare e Baleari, UE, Europa extra UE, resto del mondo.
- Tasse: nessuna IGIC (esente come autonomo; si riattiva in `TASSE.igic`); IVA del paese UE incassata al checkout fino a 150 € di merce (IOSS); sopra i 150 € e fuori UE le paga il cliente alla consegna. Da far confermare al gestor.
- Il peso di ogni opera (kg, imballata) si imposta nel pannello di gestione.
- Il pagamento non è ancora collegato (prossimo passo: Stripe).

## Altro
- `assets/style.css` – colori e font in cima al file (variabili `:root`)
- `assets/logo.png` – logo con sfondo trasparente (anche `logo-piccolo.png` e `favicon.png`)
- Testi inventati, prezzi e partner sono da confermare. Carrello e form sono dimostrativi.
