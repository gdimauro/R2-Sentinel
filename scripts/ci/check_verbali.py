#!/usr/bin/env python3
"""Verifica l'immutabilità degli atti protocollati.

Fallisce se: un verbale è stato modificato dopo la protocollazione, un numero
manca, o un verbale non è a registro. È la garanzia che rende il registro un
protocollo e non una cartella di appunti.
"""
import hashlib, io, os, re, sys

RAD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(RAD, "docs", "verbali")
REG = os.path.join(DIR, "REGISTRO.md")

def impronta(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]

def main():
    if not os.path.isdir(DIR):
        print("nessun archivio verbali: niente da verificare")
        return 0
    err = []
    testo = io.open(REG, encoding="utf-8").read() if os.path.exists(REG) else ""
    a_registro = dict(re.findall(r"\| \[(VRB-\d{4}-\d{4})\].*?\| `([0-9a-f]{16})` \|", testo))
    su_disco = {f[:-3] for f in os.listdir(DIR) if re.match(r"VRB-\d{4}-\d{4}\.md$", f)}

    for num in sorted(su_disco):
        p = os.path.join(DIR, num + ".md")
        if num not in a_registro:
            err.append(f"{num}: sul disco ma NON a registro")
        elif a_registro[num] != impronta(p):
            err.append(f"{num}: MODIFICATO dopo la protocollazione "
                       f"(atteso {a_registro[num]}, trovato {impronta(p)}). "
                       f"Un atto protocollato non si corregge: emetterne uno nuovo che lo rettifichi.")
    for num in a_registro:
        if num not in su_disco:
            err.append(f"{num}: a registro ma il file NON esiste")

    # Un numero di protocollo assegnato a un modulo vuoto è peggio di un numero
    # non assegnato: il registro certifica l'immutabilità di una pagina bianca e
    # dichiara istruito un atto che non esiste. Difetto rilevato il 2026-08-24,
    # dopo che 5 atti su 8 erano stati protocollati e annunciati come completi.
    SEZIONI = ("## Fatto", "## Posizione di chi solleva", "## Dispositivo", "## Effetti")
    for num in sorted(su_disco):
        testo = io.open(os.path.join(DIR, num + ".md"), encoding="utf-8").read()
        vuote = []
        for i, sez in enumerate(SEZIONI):
            if sez not in testo:
                vuote.append(sez + " (assente)")
                continue
            corpo = testo.split(sez, 1)[1].split("\n## ", 1)[0]
            if len(corpo.strip()) < 40:
                vuote.append(sez)
        if vuote:
            err.append(f"{num}: MODULO VUOTO — sezioni non compilate: {', '.join(vuote)}. "
                       f"Un numero di protocollo su un atto non istruito non vale nulla.")
        if "esito: in attesa" in testo and len(testo) < 1200:
            err.append(f"{num}: esito «in attesa» su un atto senza istruttoria.")

    # buchi nella numerazione
    for anno in {n[4:8] for n in su_disco}:
        nn = sorted(int(n[9:]) for n in su_disco if n[4:8] == anno)
        mancanti = [i for i in range(1, (nn[-1] if nn else 0) + 1) if i not in nn]
        if mancanti:
            err.append(f"{anno}: numeri mancanti {mancanti} — la serie non ha buchi")

    if err:
        print("REGISTRO DI PROTOCOLLO — VERIFICA FALLITA\n")
        for e in err: print("  ✗ " + e)
        return 1
    print(f"registro coerente: {len(su_disco)} atti, impronte verificate")
    return 0

if __name__ == "__main__":
    sys.exit(main())
