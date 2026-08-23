#!/usr/bin/env python3
"""Assegna il prossimo numero di protocollo e crea il verbale.

Il numero si ricava dai file esistenti, non da un contatore separato: un
contatore può divergere dall'archivio, i file no.
"""
import argparse, hashlib, io, os, re, sys
from datetime import date

RAD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAD, "docs", "verbali")
REG = os.path.join(DIR, "REGISTRO.md")
TIPI = ("contestazione", "decisione", "gate", "accettazione-rischio", "emendamento")

def impronta(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]

def prossimo(anno):
    n = 0
    for f in os.listdir(DIR):
        m = re.match(rf"VRB-{anno}-(\d{{4}})\.md$", f)
        if m:
            n = max(n, int(m.group(1)))
    return n + 1

def rigenera_registro():
    righe = []
    for f in sorted(os.listdir(DIR)):
        if not re.match(r"VRB-\d{4}-\d{4}\.md$", f):
            continue
        p = os.path.join(DIR, f)
        testo = io.open(p, encoding="utf-8").read()
        campo = lambda k: (re.search(rf"^{k}:\s*(.+)$", testo, re.M) or [None, "—"])[1].strip()
        righe.append((f[:-3], campo("data"), campo("tipo"), campo("oggetto"),
                      campo("esito"), impronta(p)))
    out = ["# Registro di protocollo", "",
           "Indice degli atti. **Le impronte SHA-256 rendono verificabile",
           "l'immutabilità**: `scripts/ci/check_verbali.py` fallisce se un verbale",
           "già protocollato viene modificato. Un atto sbagliato non si corregge:",
           "si emette un nuovo verbale che lo rettifica.", "",
           f"Atti protocollati: **{len(righe)}**", "",
           "| Protocollo | Data | Tipo | Oggetto | Esito | Impronta |",
           "|---|---|---|---|---|---|"]
    for r in righe:
        out.append("| [{0}]({0}.md) | {1} | {2} | {3} | {4} | `{5}` |".format(*r))
    io.open(REG, "w", encoding="utf-8").write("\n".join(out) + "\n")
    return len(righe)

def main():
    ap = argparse.ArgumentParser(description="Protocolla un nuovo verbale.")
    ap.add_argument("titolo", nargs="?")
    ap.add_argument("--tipo", choices=TIPI)
    ap.add_argument("--parti", default="")
    ap.add_argument("--riferimenti", default="")
    ap.add_argument("--solo-registro", action="store_true",
                    help="rigenera REGISTRO.md senza creare nulla")
    ns = ap.parse_args()

    os.makedirs(DIR, exist_ok=True)
    if ns.solo_registro:
        print(f"registro rigenerato: {rigenera_registro()} atti")
        return 0
    if not (ns.titolo and ns.tipo):
        ap.error("servono titolo e --tipo")

    anno = date.today().year
    num = f"VRB-{anno}-{prossimo(anno):04d}"
    p = os.path.join(DIR, num + ".md")
    io.open(p, "w", encoding="utf-8").write(f"""---
protocollo: {num}
data: {date.today().isoformat()}
tipo: {ns.tipo}
parti: [{ns.parti}]
oggetto: {ns.titolo}
riferimenti: [{ns.riferimenti}]
esito: in attesa
---

# {num} · {ns.titolo}

## Fatto

## Posizione di chi solleva

## Verifica indipendente

## Posizione contraria

## Dispositivo

## Effetti
""")
    rigenera_registro()
    print(f"{num} creato: {p}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
