#!/usr/bin/env python3
"""Verifica che un artefatto di consegna esista e non sia un guscio vuoto.

Alcuni criteri di FATTO sono consegne, non misure: "budget d'errore scritto e
concordato", "nota consegnata a mechatronics", "spettro ventola consegnato".
Questo comando le rende verificabili senza entrare nel merito del contenuto:
il merito e' di chi la scrive e di chi la riceve.

Fallisce se: il file manca, e' piu' corto di --min-words, oppure contiene ancora
un marcatore TODO/TBD/da definire.
"""
from __future__ import annotations
import argparse, pathlib, re, sys

MARKERS = re.compile(r"\b(TODO|TBD|FIXME|da definire|da decidere|XXX)\b", re.I)

ap = argparse.ArgumentParser()
ap.add_argument("path")
ap.add_argument("--min-words", type=int, default=120)
a = ap.parse_args()

root = pathlib.Path(__file__).resolve().parents[2]
p = root / a.path

if not p.exists():
    print(f"FALLITO — artefatto mancante: {a.path}")
    print("Il criterio di FATTO non e' soddisfatto finche' questo file non esiste.")
    sys.exit(1)

text = p.read_text(errors="ignore")
words = len(text.split())
problems = []
if words < a.min_words:
    problems.append(f"troppo breve: {words} parole, attese >= {a.min_words}")
m = MARKERS.search(text)
if m:
    ln = text[:m.start()].count("\n") + 1
    problems.append(f"marcatore non risolto '{m.group(0)}' a riga {ln}")

if problems:
    print(f"FALLITO — {a.path}:")
    for x in problems:
        print("  - " + x)
    sys.exit(1)
print(f"OK — {a.path} presente ({words} parole, nessun marcatore aperto)")
