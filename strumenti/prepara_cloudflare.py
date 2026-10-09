# Copia nella cartella "pubblico/" solo i file del sito da pubblicare su Cloudflare.
# Su Cloudflare il comando di build è:
#   python3 strumenti/genera_pagine.py && python3 strumenti/prepara_cloudflare.py
import shutil
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
USCITA = RADICE / "pubblico"
DA_COPIARE = ["assets", "dati", "admin", "es", "it", "_headers"]

if USCITA.exists():
    shutil.rmtree(USCITA)
USCITA.mkdir()
for f in RADICE.glob("*.html"):
    shutil.copy2(f, USCITA / f.name)
for nome in DA_COPIARE:
    sorgente = RADICE / nome
    if sorgente.is_dir():
        shutil.copytree(sorgente, USCITA / nome)
    elif sorgente.exists():
        shutil.copy2(sorgente, USCITA / nome)
print("pronti", sum(1 for p in USCITA.rglob("*") if p.is_file()), "file in", USCITA.name)
