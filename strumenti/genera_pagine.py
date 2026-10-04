# Genera le pagine HTML del sito nelle tre lingue.
#   EN (principale) -> cartella principale:  index.html, shop.html ...
#   ES              -> cartella es/
#   IT              -> cartella it/
# Uso, dalla cartella del sito:  python strumenti/genera_pagine.py
# I testi si cambiano qui sotto (dizionario T), poi si rilancia lo script.
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
LINGUE = ["en", "es", "it"]          # ordine di priorità
CARTELLA = {"en": "", "es": "es/", "it": "it/"}
PAGINE = ["index", "negozio", "chi-sono", "contatti", "carrello", "checkout"]
# Nome del file di ogni pagina in ogni lingua
FILE = {
  "en": {"index": "index", "negozio": "shop", "chi-sono": "about", "contatti": "contact", "carrello": "cart", "checkout": "checkout"},
  "es": {"index": "index", "negozio": "tienda", "chi-sono": "sobre-mi", "contatti": "contacto", "carrello": "carrito", "checkout": "pago"},
  "it": {"index": "index", "negozio": "negozio", "chi-sono": "chi-sono", "contatti": "contatti", "carrello": "carrello", "checkout": "checkout"},
}

T = {
  "en": {
    "desc": "followthesandro: handmade string art on driftwood collected from the beaches of Fuerteventura.",
    "titoli": {"index": "followthesandro · String art on Fuerteventura driftwood", "negozio": "Shop · followthesandro", "chi-sono": "About · followthesandro", "contatti": "Contact · followthesandro", "carrello": "Cart · followthesandro", "checkout": "Checkout · followthesandro"},
    "banner": "Every piece is one of a kind: Fuerteventura wood, nails and thread, all handmade",
    "nav": ["Wall art", "Small pieces", "Objects", "Gift ideas", "Custom", "About", "Contact"],
    "carrello": "Cart", "menu": "Open menu", "lingua": "Language",
    "logo_alt": "follow the Sandro logo: a van made of nails and thread",
    "hero_h1": "String art from the wood <br>the sea gives back",
    "hero_tag": "Handmade · Reclaimed wood · Fuerteventura",
    "hero_btn1": "Discover the works", "hero_btn2": "Create your own piece",
    "nuove_occ": "Fresh from the workshop", "nuove_h2": "Latest works",
    "legno_occ": "The wood", "legno_h2": "Collected on foot, beach after beach",
    "legno_p1": "Every board starts as a piece of wood found on the most remote beaches of Fuerteventura: planks from old boats, crates, branches polished by the Atlantic. Nothing is bought, everything is saved.",
    "legno_p2": "Salt, sun and wind decide the colour and the grain. That is why no two pieces are ever the same.",
    "legno_btn": "My story", "legno_media": "Fuerteventura in string art",
    "proc_occ": "The process", "proc_h2": "From the beach to your wall", "proc_p": "No machines, no prints. Just hands, a hammer and patience.",
    "passi": [("Search", "Miles of empty coastline to find the right wood, brought in by the tide."), ("Recovery", "The wood is cleaned, dried and sanded by hand, without erasing its story."), ("Nails", "Hundreds, sometimes thousands of nails hammered in one by one following the design."), ("Thread", "The thread is pulled tight, nail after nail, until the shape comes to life.")],
    "num_occ": "In numbers", "num_h2": "Millions of nails, one at a time",
    "numeri": [("1,000,000+", "nails hammered by hand"), ("100%", "reclaimed wood"), ("40,000 m", "of thread pulled tight"), ("1", "island, Fuerteventura")],
    "pop_occ": "Most loved", "pop_h2": "Favourite works",
    "mis_occ": "Made to order", "mis_h2": "Your van, your wave, your name",
    "mis_p": "Send me a photo or an idea: your camper van, your surfboard, the island you love, a name or a date. I will turn it into a piece of nails and thread on reclaimed wood.",
    "mis_btn": "Request a custom piece", "mis_media": "Custom van in string art",
    "vantaggi": [("Saved wood", "Recovered from the sea, never cut"), ("Handmade", "Nail after nail"), ("Safe shipping", "Packed with recycled materials"), ("One of a kind", "With a signed certificate")],
    "dove_occ": "Where to find me", "dove_h2": "Markets, surf shops and island friends",
    "foot_p": "Handmade string art on wood the sea leaves on the beaches of Fuerteventura.",
    "foot_h": ["Works", "Help", "More"],
    "foot_aiuto": ["Shipping", "Returns and refunds", "Wood care", "Contact"],
    "foot_altro": ["Island diary", "About", "Custom pieces"],
    "foot_fondo": "© 2026 followthesandro. Handmade in Fuerteventura.",
    "foot_legal": ["Terms and conditions", "Privacy", "Cookies"],
    "neg_h1": "The works", "neg_p": "Every piece is unique: once it is sold, it is gone.", "neg_tutte": "All",
    "chi_h1": "About", "chi_p": "A van, a hammer and a deserted island.",
    "chi_occ": "Hi, I'm Sandro", "chi_h2": "I follow the wood, wherever the sea takes it", "chi_media": "Surfboard in string art",
    "chi_testo": ["A few years ago I loaded up my old green van and drove to Fuerteventura. Between one wave and the next I walked along beaches where there was nobody, and every time I found wood: pieces of boats, worn planks, branches bleached by the sun.",
                  "It felt like a shame to leave them there. So I started carrying them back to the van, sanding them and hammering nails into them, one after another, pulling the thread until a wave, a volcano or the outline of the island appeared.",
                  "Since then I have hammered in more than a million nails, all by hand. Every piece carries a bit of beach and a bit of the journey: if you like, now it can follow you too."],
    "chi_btn": "Write to me",
    "con_h1": "Contact", "con_p": "A piece you have seen, a custom idea or just a hello from the island.",
    "form_nome": "Name", "form_email": "Email", "form_motivo": "What are you interested in",
    "form_opzioni": ["A custom piece", "Information about a work", "Order or shipping", "Collaboration or market"],
    "form_msg": "Tell me your idea (subject, size, thread colours)", "form_invia": "Send message",
    "car_h1": "Your cart", "co_h1": "Checkout", "co_p": "Secure payment · Tracked shipping worldwide",
    "co": {"contatto": "Contact", "email": "Email", "tel": "Phone (for the courier)", "indirizzo": "Shipping address",
           "nome": "First name", "cognome": "Last name", "via": "Street and number", "via2": "Apartment, floor, etc. (optional)",
           "cap": "Postcode", "citta": "City", "prov": "Province / State / Region", "paese": "Country",
           "metodo": "Shipping method", "note": "Notes for the order (optional)",
           "termini": "I accept the terms and conditions of sale", "riepilogo": "Order summary", "paga": "Proceed to payment"},
  },
  "es": {
    "desc": "followthesandro: string art hecho a mano con madera recuperada en las playas de Fuerteventura.",
    "titoli": {"index": "followthesandro · String art con madera de Fuerteventura", "negozio": "Tienda · followthesandro", "chi-sono": "Sobre mí · followthesandro", "contatti": "Contacto · followthesandro", "carrello": "Carrito · followthesandro", "checkout": "Pago · followthesandro"},
    "banner": "Cada pieza es única: madera de Fuerteventura, clavos e hilo, todo hecho a mano",
    "nav": ["Cuadros", "Formatos pequeños", "Objetos", "Ideas de regalo", "A medida", "Sobre mí", "Contacto"],
    "carrello": "Carrito", "menu": "Abrir menú", "lingua": "Idioma",
    "logo_alt": "Logo follow the Sandro: una furgoneta hecha de clavos e hilo",
    "hero_h1": "String art con la madera <br>que el mar devuelve",
    "hero_tag": "Hecho a mano · Madera recuperada · Fuerteventura",
    "hero_btn1": "Descubre las obras", "hero_btn2": "Crea tu obra",
    "nuove_occ": "Recién salidas del taller", "nuove_h2": "Últimas obras",
    "legno_occ": "La madera", "legno_h2": "Recogida a pie, playa tras playa",
    "legno_p1": "Cada tabla nace de un trozo de madera encontrado en las playas más aisladas de Fuerteventura: tablones de viejas barcas, cajas, ramas pulidas por el Atlántico. Nada se compra, todo se salva.",
    "legno_p2": "La sal, el sol y el viento deciden el color y las vetas. Por eso no existen dos obras iguales.",
    "legno_btn": "Mi historia", "legno_media": "Fuerteventura en string art",
    "proc_occ": "El proceso", "proc_h2": "De la playa a tu pared", "proc_p": "Sin máquinas, sin impresiones. Solo manos, martillo y paciencia.",
    "passi": [("Búsqueda", "Kilómetros de costa desierta para encontrar la madera adecuada, traída por la marea."), ("Recuperación", "La madera se limpia, se seca y se lija a mano, sin borrar su historia."), ("Clavos", "Cientos, a veces miles de clavos colocados uno a uno siguiendo el dibujo."), ("Hilo", "El hilo se tensa clavo tras clavo hasta que la forma cobra vida.")],
    "num_occ": "En números", "num_h2": "Millones de clavos, uno a uno",
    "numeri": [("1.000.000+", "clavos colocados a mano"), ("100%", "madera recuperada"), ("40.000 m", "de hilo tensado"), ("1", "isla, Fuerteventura")],
    "pop_occ": "Las más queridas", "pop_h2": "Las obras favoritas",
    "mis_occ": "A medida", "mis_h2": "Tu furgo, tu ola, tu nombre",
    "mis_p": "Mándame una foto o una idea: tu furgoneta, tu tabla de surf, la isla de tu corazón, un nombre o una fecha. La convierto en una obra de clavos e hilo sobre madera recuperada.",
    "mis_btn": "Pide una obra a medida", "mis_media": "Furgoneta a medida en string art",
    "vantaggi": [("Madera salvada", "Recuperada del mar, nunca talada"), ("Hecho a mano", "Clavo a clavo"), ("Envío protegido", "Embalaje con materiales reciclados"), ("Pieza única", "Con certificado firmado")],
    "dove_occ": "Dónde encontrarme", "dove_h2": "Mercadillos, surf shops y amigos de la isla",
    "foot_p": "String art hecho a mano con la madera que el mar deja en las playas de Fuerteventura.",
    "foot_h": ["Obras", "Ayuda", "Más"],
    "foot_aiuto": ["Envíos", "Devoluciones y reembolsos", "Cuidado de la madera", "Contacto"],
    "foot_altro": ["Diario desde la isla", "Sobre mí", "Obras a medida"],
    "foot_fondo": "© 2026 followthesandro. Hecho a mano en Fuerteventura.",
    "foot_legal": ["Términos y condiciones", "Privacidad", "Cookies"],
    "neg_h1": "Las obras", "neg_p": "Cada pieza es única: cuando se vende, no vuelve.", "neg_tutte": "Todas",
    "chi_h1": "Sobre mí", "chi_p": "Una furgoneta, un martillo y una isla desierta.",
    "chi_occ": "Hola, soy Sandro", "chi_h2": "Sigo la madera, allá donde el mar la lleve", "chi_media": "Tabla de surf en string art",
    "chi_testo": ["Hace unos años cargué mi vieja furgoneta verde y llegué a Fuerteventura. Entre ola y ola caminaba por playas donde no había nadie, y cada vez encontraba madera: trozos de barcas, tablas gastadas, ramas blanqueadas por el sol.",
                  "Me parecía una pena dejarlas allí. Así que empecé a llevarlas a la furgo, a lijarlas y a clavarles clavos, uno tras otro, tensando el hilo hasta que aparecía una ola, un volcán o el perfil de la isla.",
                  "Desde entonces he clavado más de un millón de clavos, todos a mano. Cada obra lleva consigo un trozo de playa y un trozo de viaje: si quieres, ahora también puede seguirte a ti."],
    "chi_btn": "Escríbeme",
    "con_h1": "Contacto", "con_p": "Una obra que has visto, una idea a medida o solo un saludo desde la isla.",
    "form_nome": "Nombre", "form_email": "Email", "form_motivo": "Qué te interesa",
    "form_opzioni": ["Una obra a medida", "Información sobre una obra", "Pedido o envío", "Colaboración o mercadillo"],
    "form_msg": "Cuéntame tu idea (tema, medidas, colores del hilo)", "form_invia": "Enviar mensaje",
    "car_h1": "Tu carrito", "co_h1": "Finalizar compra", "co_p": "Pago seguro · Envío con seguimiento a todo el mundo",
    "co": {"contatto": "Contacto", "email": "Email", "tel": "Teléfono (para el mensajero)", "indirizzo": "Dirección de envío",
           "nome": "Nombre", "cognome": "Apellidos", "via": "Calle y número", "via2": "Piso, puerta, etc. (opcional)",
           "cap": "Código postal", "citta": "Ciudad", "prov": "Provincia / Estado / Región", "paese": "País",
           "metodo": "Método de envío", "note": "Notas del pedido (opcional)",
           "termini": "Acepto los términos y condiciones de venta", "riepilogo": "Resumen del pedido", "paga": "Ir al pago"},
  },
  "it": {
    "desc": "followthesandro: string art fatta a mano con legno recuperato sulle spiagge di Fuerteventura.",
    "titoli": {"index": "followthesandro · String art con legno di Fuerteventura", "negozio": "Negozio · followthesandro", "chi-sono": "Chi sono · followthesandro", "contatti": "Contatti · followthesandro", "carrello": "Carrello · followthesandro", "checkout": "Checkout · followthesandro"},
    "banner": "Ogni pezzo è unico: legno di Fuerteventura, chiodi e filo, tutto fatto a mano",
    "nav": ["Quadri", "Piccoli formati", "Oggetti", "Idee regalo", "Su misura", "Chi sono", "Contatti"],
    "carrello": "Carrello", "menu": "Apri menu", "lingua": "Lingua",
    "logo_alt": "Logo follow the Sandro: un van fatto di chiodi e filo",
    "hero_h1": "String art dal legno <br>che il mare restituisce",
    "hero_tag": "Fatto a mano · Legno recuperato · Fuerteventura",
    "hero_btn1": "Scopri le opere", "hero_btn2": "Crea la tua opera",
    "nuove_occ": "Appena uscite dal laboratorio", "nuove_h2": "Ultime opere",
    "legno_occ": "Il legno", "legno_h2": "Raccolto a piedi, spiaggia dopo spiaggia",
    "legno_p1": "Ogni tavola nasce da un pezzo di legno trovato sulle spiagge più isolate di Fuerteventura: assi di vecchie barche, cassette, rami levigati dall'Atlantico. Niente viene comprato, tutto viene salvato.",
    "legno_p2": "Il sale, il sole e il vento decidono il colore e le venature. Per questo non esistono due opere uguali.",
    "legno_btn": "La mia storia", "legno_media": "Fuerteventura in string art",
    "proc_occ": "Il processo", "proc_h2": "Dalla spiaggia alla tua parete", "proc_p": "Nessuna macchina, nessuna stampa. Solo mani, martello e pazienza.",
    "passi": [("Ricerca", "Chilometri di costa deserta per trovare il legno giusto, portato dalla marea."), ("Recupero", "Il legno viene pulito, asciugato e levigato a mano, senza cancellare la sua storia."), ("Chiodi", "Centinaia, a volte migliaia di chiodi piantati uno a uno seguendo il disegno."), ("Filo", "Il filo viene teso chiodo dopo chiodo finché la forma prende vita.")],
    "num_occ": "In numeri", "num_h2": "Milioni di chiodi, uno alla volta",
    "numeri": [("1.000.000+", "chiodi piantati a mano"), ("100%", "legno recuperato"), ("40.000 m", "di filo teso"), ("1", "isola, Fuerteventura")],
    "pop_occ": "Le più amate", "pop_h2": "Le opere preferite",
    "mis_occ": "Su misura", "mis_h2": "Il tuo van, la tua onda, il tuo nome",
    "mis_p": "Mandami una foto o un'idea: il tuo furgone, la tavola da surf, l'isola del cuore, un nome o una data. La trasformo in un'opera di chiodi e filo su legno recuperato.",
    "mis_btn": "Richiedi un'opera su misura", "mis_media": "Van su misura in string art",
    "vantaggi": [("Legno salvato", "Recuperato dal mare, mai tagliato"), ("Fatto a mano", "Chiodo dopo chiodo"), ("Spedizione protetta", "Imballo con materiali riciclati"), ("Pezzo unico", "Con certificato firmato")],
    "dove_occ": "Dove trovarmi", "dove_h2": "Mercatini, surf shop e amici dell'isola",
    "foot_p": "String art fatta a mano con legno che il mare lascia sulle spiagge di Fuerteventura.",
    "foot_h": ["Opere", "Assistenza", "Altro"],
    "foot_aiuto": ["Spedizioni", "Resi e rimborsi", "Cura del legno", "Contatti"],
    "foot_altro": ["Diario dall'isola", "Chi sono", "Opere su misura"],
    "foot_fondo": "© 2026 followthesandro. Fatto a mano a Fuerteventura.",
    "foot_legal": ["Termini e condizioni", "Privacy", "Cookie"],
    "neg_h1": "Le opere", "neg_p": "Ogni pezzo è unico: quando è venduto, non torna più.", "neg_tutte": "Tutte",
    "chi_h1": "Chi sono", "chi_p": "Un van, un martello e un'isola deserta.",
    "chi_occ": "Ciao, sono Sandro", "chi_h2": "Seguo il legno, ovunque il mare lo porti", "chi_media": "Tavola da surf in string art",
    "chi_testo": ["Qualche anno fa ho caricato il mio vecchio van verde e sono arrivato a Fuerteventura. Tra un'onda e l'altra camminavo per spiagge dove non c'era nessuno, e ogni volta trovavo legno: pezzi di barche, assi consumate, rami sbiancati dal sole.",
                  "Mi sembrava un peccato lasciarli lì. Così ho iniziato a portarli nel van, a levigarli e a piantarci dentro chiodi, uno dopo l'altro, tendendo il filo finché non comparivano un'onda, un vulcano, il profilo dell'isola.",
                  "Da allora ho piantato più di un milione di chiodi, tutti a mano. Ogni opera porta con sé un pezzo di spiaggia e un pezzo di viaggio: se vuoi, adesso può seguire anche te."],
    "chi_btn": "Scrivimi",
    "con_h1": "Contatti", "con_p": "Un'opera che hai visto, un'idea su misura o solo un saluto dall'isola.",
    "form_nome": "Nome", "form_email": "Email", "form_motivo": "Cosa ti interessa",
    "form_opzioni": ["Un'opera su misura", "Informazioni su un'opera", "Ordine o spedizione", "Collaborazione o mercatino"],
    "form_msg": "Raccontami la tua idea (soggetto, misure, colori del filo)", "form_invia": "Invia messaggio",
    "car_h1": "Il tuo carrello", "co_h1": "Checkout", "co_p": "Pagamento sicuro · Spedizione tracciata in tutto il mondo",
    "co": {"contatto": "Contatto", "email": "Email", "tel": "Telefono (per il corriere)", "indirizzo": "Indirizzo di spedizione",
           "nome": "Nome", "cognome": "Cognome", "via": "Via e numero civico", "via2": "Interno, scala, ecc. (facoltativo)",
           "cap": "CAP", "citta": "Città", "prov": "Provincia / Stato / Regione", "paese": "Paese",
           "metodo": "Metodo di spedizione", "note": "Note per l'ordine (facoltativo)",
           "termini": "Accetto i termini e le condizioni di vendita", "riepilogo": "Riepilogo ordine", "paga": "Procedi al pagamento"},
  },
}

# Link ai profili social (vuoto = non ancora collegato)
SOCIAL = {"Instagram": "https://www.instagram.com/followthesandro/", "Facebook": "", "TikTok": ""}

# Valori numerici dei contatori animati (stesso ordine di "numeri")
CONTATORI = [("1000000", "+"), ("100", "%"), ("40000", " m"), ("1", "")]

ICONE = {
  "carrello": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 7h12l-1 13H7L6 7z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg>',
  "menu": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
  "vantaggi": [
    '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M7 21c-1-6 1-11 10-16-1 8-4 12-10 16zM7 21l6-8"/></svg>',
    '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 3l8 8M6 5l2-2 4 4-2 2zM12 11l-8 8 1 1 8-8"/></svg>',
    '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/></svg>',
    '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.5 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/></svg>',
  ],
  "social": [
    ("Instagram", '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'),
    ("Facebook", '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M15 3h-2a4 4 0 0 0-4 4v3H7v4h2v7h4v-7h3l1-4h-4V7a1 1 0 0 1 1-1h2z"/></svg>'),
    ("TikTok", '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 3v11a4 4 0 1 1-4-4"/><path d="M14 3a5 5 0 0 0 5 5"/></svg>'),
  ],
}


def link_lingua(da, a, pagina):
    """Percorso relativo dalla pagina in lingua `da` alla stessa pagina in lingua `a`."""
    su = "../" if CARTELLA[da] else ""
    return f"{su}{CARTELLA[a]}{FILE[a][pagina]}.html"


def testa(l, pagina, b):
    alternative = "\n".join(
        f'<link rel="alternate" hreflang="{x}" href="{link_lingua(l, x, pagina)}">' for x in LINGUE
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{link_lingua(l, "en", pagina)}">'
    extra = '<script src="{P}assets/checkout.js" defer></script>\n' if pagina in ("carrello", "checkout") else ""
    return f"""<!doctype html>
<html lang="{l}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{b['titoli'][pagina]}</title>
<meta name="description" content="{b['desc']}">
{alternative}
<link rel="icon" type="image/png" href="{{P}}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&family=Karla:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{P}}assets/style.css">
<script src="{{P}}assets/script.js" defer></script>
{extra}</head>
<body>
<div class="banner">{b['banner']}</div>
"""


def intestazione(l, pagina, b):
    n = b["nav"]
    voci = [("negozio.html#quadri", n[0], ""), ("negozio.html#mini", n[1], ""), ("negozio.html#oggetti", n[2], ""),
            ("negozio.html#regali", n[3], ""), ("contatti.html#personalizza", n[4], ""),
            ("chi-sono.html", n[5], "nav-secondaria"), ("contatti.html", n[6], "nav-secondaria")]
    nav = ""
    for href, testo, cls in voci:
        attivo = (pagina == "chi-sono" and href == "chi-sono.html") or (pagina == "contatti" and href == "contatti.html")
        classi = " ".join(c for c in [cls, "attivo" if attivo else ""] if c)
        nav += f'      <a href="{href}" class="{classi}">{testo}</a>\n'
    corrente = ' class="attiva" aria-current="true"'
    lingue = "".join(
        f'<a href="{link_lingua(l, x, pagina)}" hreflang="{x}" lang="{x}"{corrente if x == l else ""}>{x.upper()}</a>'
        for x in LINGUE
    )
    return f"""<header class="header">
  <div class="container">
    <a class="logo" href="index.html"><img src="{{P}}assets/logo-piccolo.png" alt="">followthe<span>sandro</span></a>
    <nav class="nav">
{nav}    </nav>
    <div class="azioni">
      <div class="lingue" role="navigation" aria-label="{b['lingua']}">{lingue}</div>
      <a class="carrello" href="carrello.html" aria-label="{b['carrello']}">
        {ICONE['carrello']}
        <span class="conta" hidden>0</span>
      </a>
      <button class="menu-toggle" type="button" aria-label="{b['menu']}">
        {ICONE['menu']}
      </button>
    </div>
  </div>
</header>
<main>
"""


def piede(b):
    n = b["nav"]
    social = "\n".join(
        f'          <a href="{SOCIAL[nome]}" aria-label="{nome}" target="_blank" rel="noopener">{svg}</a>' if SOCIAL.get(nome)
        else f'          <a href="#" aria-label="{nome}">{svg}</a>'
        for nome, svg in ICONE["social"])
    aiuto = b["foot_aiuto"]
    altro = b["foot_altro"]
    legal = b["foot_legal"]
    return f"""</main>
<footer class="footer">
  <div class="container">
    <div class="colonne">
      <div>
        <a class="logo" href="index.html"><img src="{{P}}assets/logo-piccolo.png" alt="">followthe<span>sandro</span></a>
        <p style="margin-top:12px">{b['foot_p']}</p>
        <div class="social">
{social}
        </div>
      </div>
      <div>
        <h4>{b['foot_h'][0]}</h4>
        <ul>
          <li><a href="negozio.html#quadri">{n[0]}</a></li>
          <li><a href="negozio.html#mini">{n[1]}</a></li>
          <li><a href="negozio.html#oggetti">{n[2]}</a></li>
          <li><a href="negozio.html#regali">{n[3]}</a></li>
        </ul>
      </div>
      <div>
        <h4>{b['foot_h'][1]}</h4>
        <ul>
          <li><a href="#">{aiuto[0]}</a></li>
          <li><a href="#">{aiuto[1]}</a></li>
          <li><a href="#">{aiuto[2]}</a></li>
          <li><a href="contatti.html">{aiuto[3]}</a></li>
        </ul>
      </div>
      <div>
        <h4>{b['foot_h'][2]}</h4>
        <ul>
          <li><a href="#">{altro[0]}</a></li>
          <li><a href="chi-sono.html">{altro[1]}</a></li>
          <li><a href="contatti.html#personalizza">{altro[2]}</a></li>
        </ul>
      </div>
    </div>
    <div class="fondo">
      <span>{b['foot_fondo']}</span>
      <div><a href="#">{legal[0]}</a><a href="#">{legal[1]}</a><a href="#">{legal[2]}</a></div>
    </div>
  </div>
</footer>
</body>
</html>
"""


def corpo_index(b):
    passi = "\n".join(f'      <div class="passo"><h3>{t}</h3><p>{d}</p></div>' for t, d in b["passi"])
    numeri = "\n".join(
        f'      <div class="numero"><strong data-conta="{v}"' + (f' data-suffisso="{s}"' if s else "")
        + f'>{testo}</strong><span>{etichetta}</span></div>'
        for (v, s), (testo, etichetta) in zip(CONTATORI, b["numeri"])
    )
    vantaggi = "\n".join(
        f'    <div class="vantaggio">{svg}<strong>{t}</strong><span>{d}</span></div>'
        for svg, (t, d) in zip(ICONE["vantaggi"], b["vantaggi"])
    )
    return f"""
<section class="hero">
  <!-- Video di sfondo in trasparenza: metti il tuo file in assets/video/sfondo.mp4 -->
  <video class="hero-video" autoplay muted loop playsinline preload="auto" aria-hidden="true" tabindex="-1">
    <source src="{{P}}assets/video/sfondo.mp4" type="video/mp4">
    <source src="{{P}}assets/video/segnaposto.webm" type="video/webm">
  </video>
  <div class="container">
    <img class="logo-grande" src="{{P}}assets/logo.png" alt="{b['logo_alt']}">
    <h1>{b['hero_h1']}</h1>
    <p class="tagline">{b['hero_tag']}</p>
    <div class="cta">
      <a class="btn" href="negozio.html">{b['hero_btn1']}</a>
      <a class="btn secondario" href="contatti.html#personalizza">{b['hero_btn2']}</a>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="titolo-sezione">
      <span class="occhiello">{b['nuove_occ']}</span>
      <h2>{b['nuove_h2']}</h2>
    </div>
    <div class="griglia" id="ultima-collezione"></div>
  </div>
</section>

<section class="sfondo-sabbia">
  <div class="container split">
    <div class="split-media" data-forma="isola" data-filo="#2a211b" data-legno="#d8b98f" data-nome="{b['legno_media']}"></div>
    <div class="split-testo">
      <span class="occhiello">{b['legno_occ']}</span>
      <h2>{b['legno_h2']}</h2>
      <p>{b['legno_p1']}</p>
      <p>{b['legno_p2']}</p>
      <a class="btn" href="chi-sono.html">{b['legno_btn']}</a>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="titolo-sezione">
      <span class="occhiello">{b['proc_occ']}</span>
      <h2>{b['proc_h2']}</h2>
      <p>{b['proc_p']}</p>
    </div>
    <div class="passi">
{passi}
    </div>
  </div>
</section>

<section class="sfondo-scuro">
  <div class="container">
    <div class="titolo-sezione">
      <span class="occhiello" style="color:var(--arancio)">{b['num_occ']}</span>
      <h2>{b['num_h2']}</h2>
    </div>
    <div class="numeri">
{numeri}
    </div>
  </div>
</section>

<section class="sfondo-sabbia">
  <div class="container">
    <div class="titolo-sezione">
      <span class="occhiello">{b['pop_occ']}</span>
      <h2>{b['pop_h2']}</h2>
    </div>
    <div class="griglia" id="piu-popolari"></div>
  </div>
</section>

<section>
  <div class="container split inverti">
    <div class="split-media" data-forma="van" data-filo="#3f6331" data-legno="#c9a27a" data-nome="{b['mis_media']}"></div>
    <div class="split-testo">
      <span class="occhiello">{b['mis_occ']}</span>
      <h2>{b['mis_h2']}</h2>
      <p>{b['mis_p']}</p>
      <a class="btn" href="contatti.html#personalizza">{b['mis_btn']}</a>
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
      <span class="occhiello">{b['dove_occ']}</span>
      <h2>{b['dove_h2']}</h2>
    </div>
    <div class="loghi"><span>Partner 1</span><span>Partner 2</span><span>Partner 3</span><span>Partner 4</span><span>Partner 5</span></div>
  </div>
</section>
"""


def corpo_negozio(b):
    n = b["nav"]
    return f"""
<div class="intestazione-pagina"><div class="container"><h1>{b['neg_h1']}</h1><p>{b['neg_p']}</p></div></div>
<section>
  <div class="container">
    <div class="filtri">
      <button data-cat="tutti">{b['neg_tutte']}</button>
      <button data-cat="quadri">{n[0]}</button>
      <button data-cat="mini">{n[1]}</button>
      <button data-cat="oggetti">{n[2]}</button>
      <button data-cat="regali">{n[3]}</button>
    </div>
    <div class="griglia" id="negozio"></div>
  </div>
</section>
"""


def corpo_chi_sono(b):
    paragrafi = "\n".join(f"      <p>{p}</p>" for p in b["chi_testo"])
    return f"""
<div class="intestazione-pagina"><div class="container"><h1>{b['chi_h1']}</h1><p>{b['chi_p']}</p></div></div>
<section>
  <div class="container split">
    <div class="split-media" data-forma="tavola" data-filo="#3f6331" data-legno="#b8875a" data-nome="{b['chi_media']}"></div>
    <div class="split-testo testo-lungo">
      <span class="occhiello">{b['chi_occ']}</span>
      <h2>{b['chi_h2']}</h2>
{paragrafi}
      <a class="btn" href="contatti.html">{b['chi_btn']}</a>
    </div>
  </div>
</section>
"""


def corpo_contatti(b):
    opzioni = "\n".join(f"          <option>{o}</option>" for o in b["form_opzioni"])
    return f"""
<div class="intestazione-pagina"><div class="container"><h1>{b['con_h1']}</h1><p>{b['con_p']}</p></div></div>
<section id="personalizza">
  <div class="container">
    <form class="form">
      <label>{b['form_nome']} <input name="nome" required></label>
      <label>{b['form_email']} <input type="email" name="email" required></label>
      <label>{b['form_motivo']}
        <select name="motivo">
{opzioni}
        </select>
      </label>
      <label>{b['form_msg']} <textarea name="messaggio" required></textarea></label>
      <button class="btn" type="submit">{b['form_invia']}</button>
      <p class="esito" aria-live="polite"></p>
    </form>
  </div>
</section>
"""


def corpo_carrello(b):
    return f"""
<div class="intestazione-pagina"><div class="container"><h1>{b['car_h1']}</h1></div></div>
<section>
  <div class="container" id="carrello-pagina" data-negozio="negozio.html" data-checkout="checkout.html"></div>
</section>
"""


def corpo_checkout(b):
    c = b["co"]
    return f"""
<div class="intestazione-pagina"><div class="container"><h1>{b['co_h1']}</h1><p>{b['co_p']}</p></div></div>
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


CORPI = {"index": corpo_index, "negozio": corpo_negozio, "chi-sono": corpo_chi_sono, "contatti": corpo_contatti,
         "carrello": corpo_carrello, "checkout": corpo_checkout}

for l in LINGUE:
    b = T[l]
    cartella = RADICE / CARTELLA[l]
    cartella.mkdir(exist_ok=True)
    prefisso = "../" if CARTELLA[l] else ""
    for pagina in PAGINE:
        html = testa(l, pagina, b) + intestazione(l, pagina, b) + CORPI[pagina](b) + piede(b)
        html = html.replace("{P}", prefisso)
        for chiave in ["negozio", "chi-sono", "contatti", "carrello", "checkout"]:   # link interni -> nomi file della lingua
            html = html.replace(f'="{chiave}.html', f'="{FILE[l][chiave]}.html')
        nome = FILE[l][pagina] + ".html"
        (cartella / nome).write_text(html, encoding="utf-8")
        print("scritto", CARTELLA[l] + nome)
