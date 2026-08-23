#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
indice.py — indice versionato del dataset notturno, R2-Sentinel Unità B.

Cosa entra in Git e cosa no
---------------------------
* **In Git:** `dataset/notti/*.json` (un file per notte) e `dataset/indice.csv`
  (generato, una riga per notte). Sono testo, piccoli, diffabili, e sono ciò
  che rende il dataset ricostruibile e verificabile da un terzo.
* **Fuori da Git:** l'audio. Registrazioni notturne fatte dentro casa non
  entrano nella working copy (CONTRIBUTING.md — la history non si cancella).

Il gate di fase 1 è un contatore, non del codice:
    ≥20 notti utili, ciascuna ≥6 h continue, 48 kHz, con metadati ambientali,
    di cui ≥5 negative raccolte deliberatamente come controllo.
Questo strumento conta quelle notti secondo regole esplicite, così che
"siamo a 14 su 20" sia un fatto verificabile e non un'impressione.

Uso:
    python3 indice.py aggiorna     # rigenera indice.csv e stampa lo stato
    python3 indice.py stato        # solo lo stato, non scrive
    python3 indice.py verifica     # controlla che l'audio esista ancora
"""

from __future__ import annotations

import csv
import json
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
if QUI not in sys.path:
    sys.path.insert(0, QUI)

import metadati as MD  # noqa: E402

PERCORSO_CSV = os.path.join(MD.DIR_DATASET, "indice.csv")
PERCORSO_JSON = os.path.join(MD.DIR_DATASET, "indice.json")

OBIETTIVO_NOTTI = 20
OBIETTIVO_NEGATIVE = 5
ORE_MINIME = 6.0

COLONNE = [
    "id_notte", "data", "stanza", "inizio", "fine",
    "durata_h", "fs_hz", "ricampionato", "n_gap", "gap_s",
    "temp_inizio_c", "temp_fine_c", "umid_inizio_pct", "umid_fine_pct",
    "fonte_ambiente", "finestra", "persone", "altezza_cm",
    "esito", "controllo_negativo", "metodo_annotazione", "confidenza",
    "n_eventi_zanzara", "rms_mediano_dbfs", "picco_dbfs",
    "sorgenti_rumore", "voce_riconoscibile", "pubblicabile",
    "utile", "conteggiabile", "motivo_non_conteggiabile",
    "n_file", "gb", "cartella_audio",
]


def _get(d: dict, *chiavi, default=None):
    cur = d
    for k in chiavi:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    return cur


def carica_notti() -> list[dict]:
    if not os.path.isdir(MD.DIR_NOTTI):
        return []
    fuori = []
    for nome in sorted(os.listdir(MD.DIR_NOTTI)):
        if not nome.endswith(".json"):
            continue
        try:
            fuori.append(MD.carica(os.path.join(MD.DIR_NOTTI, nome)))
        except Exception as exc:
            print(f"  ! {nome}: JSON illeggibile ({exc})", file=sys.stderr)
    return fuori


def conteggiabile(meta: dict) -> tuple[bool, str]:
    """Regola unica di conteggio per il gate di fase 1."""
    if meta.get("utile") is False:
        return False, "scartata: " + (meta.get("motivo_scarto") or "senza motivo")
    err = MD.valida(meta)
    if err:
        return False, "; ".join(err)
    if meta.get("utile") is None:
        return False, "non ancora marcata utile (metadati.py utile ... --si)"
    return True, ""


def riga(meta: dict) -> dict:
    ok, motivo = conteggiabile(meta)
    dur = meta.get("durata_audio_s")
    byte = _get(meta, "audio", "byte_totali", default=0) or 0
    eventi = _get(meta, "annotazione", "eventi", default=[]) or []
    return {
        "id_notte": meta.get("id_notte"),
        "data": (meta.get("inizio") or "")[:10],
        "stanza": _get(meta, "posizione", "stanza", default=""),
        "inizio": meta.get("inizio"),
        "fine": meta.get("fine"),
        "durata_h": round(dur / 3600.0, 3) if dur else "",
        "fs_hz": _get(meta, "dispositivo", "sample_rate_hz", default=""),
        "ricampionato": _get(meta, "dispositivo", "ricampionato", default=""),
        "n_gap": meta.get("n_gap", ""),
        "gap_s": meta.get("gap_totale_s", ""),
        "temp_inizio_c": _get(meta, "ambiente", "temperatura_c_inizio", default=""),
        "temp_fine_c": _get(meta, "ambiente", "temperatura_c_fine", default=""),
        "umid_inizio_pct": _get(meta, "ambiente", "umidita_pct_inizio", default=""),
        "umid_fine_pct": _get(meta, "ambiente", "umidita_pct_fine", default=""),
        "fonte_ambiente": _get(meta, "ambiente", "fonte", default=""),
        "finestra": _get(meta, "ambiente", "finestra", default=""),
        "persone": _get(meta, "ambiente", "persone_presenti", default=""),
        "altezza_cm": _get(meta, "posizione", "altezza_cm", default=""),
        "esito": _get(meta, "annotazione", "esito", default=""),
        "controllo_negativo": _get(meta, "annotazione", "controllo_negativo",
                                   default=False),
        "metodo_annotazione": _get(meta, "annotazione", "metodo", default=""),
        "confidenza": _get(meta, "annotazione", "confidenza", default=""),
        "n_eventi_zanzara": len(eventi),
        "rms_mediano_dbfs": _get(meta, "rumore", "rms_dbfs_mediano", default=""),
        "picco_dbfs": _get(meta, "rumore", "picco_dbfs", default=""),
        "sorgenti_rumore": "|".join(_get(meta, "rumore", "sorgenti_note",
                                         default=[]) or []),
        "voce_riconoscibile": _get(meta, "privacy", "voce_riconoscibile", default=""),
        "pubblicabile": _get(meta, "privacy", "pubblicabile", default=False),
        "utile": meta.get("utile"),
        "conteggiabile": ok,
        "motivo_non_conteggiabile": motivo,
        "n_file": _get(meta, "audio", "n_file", default=0),
        "gb": round(byte / 1024 ** 3, 3),
        "cartella_audio": _get(meta, "audio", "cartella", default=""),
    }


def stato(righe: list[dict]) -> dict:
    valide = [r for r in righe if r["conteggiabile"]]
    negative = [r for r in valide
                if r["esito"] == "negativa" and r["controllo_negativo"]]
    positive = [r for r in valide if r["esito"] == "positiva"]
    incerte = [r for r in valide if r["esito"] == "incerta"]
    ore = sum(float(r["durata_h"]) for r in valide if r["durata_h"] != "")
    return {
        "notti_conteggiabili": len(valide),
        "obiettivo_notti": OBIETTIVO_NOTTI,
        "notti_negative_controllo": len(negative),
        "obiettivo_negative": OBIETTIVO_NEGATIVE,
        "notti_positive": len(positive),
        "notti_incerte": len(incerte),
        "notti_registrate_totali": len(righe),
        "ore_utili": round(ore, 2),
        "gate_fase1_chiuso": (len(valide) >= OBIETTIVO_NOTTI
                              and len(negative) >= OBIETTIVO_NEGATIVE),
    }


def _barra(n: int, tot: int, larghezza: int = 30) -> str:
    pieni = min(larghezza, int(round(larghezza * n / float(tot)))) if tot else 0
    return "[" + "#" * pieni + "." * (larghezza - pieni) + "]"


def stampa_stato(righe: list[dict]) -> None:
    s = stato(righe)
    print()
    print("=" * 68)
    print("  GATE FASE 1 — RACCOLTA DATASET ZANZARE")
    print("=" * 68)
    print(f"  Notti utili        {_barra(s['notti_conteggiabili'], OBIETTIVO_NOTTI)}"
          f"  {s['notti_conteggiabili']:>3} / {OBIETTIVO_NOTTI}")
    print(f"  di cui negative    {_barra(s['notti_negative_controllo'], OBIETTIVO_NEGATIVE)}"
          f"  {s['notti_negative_controllo']:>3} / {OBIETTIVO_NEGATIVE}")
    print(f"  ore utili totali   {s['ore_utili']:.1f} h")
    print(f"  notti registrate   {s['notti_registrate_totali']} "
          f"(positive {s['notti_positive']}, negative {s['notti_negative_controllo']}, "
          f"incerte {s['notti_incerte']})")
    print(f"  gate chiuso        {'SÌ' if s['gate_fase1_chiuso'] else 'NO'}")

    non_conta = [r for r in righe if not r["conteggiabile"]]
    if non_conta:
        print("\n  Notti che NON contano ancora:")
        for r in non_conta:
            print(f"    - {r['id_notte']}: {r['motivo_non_conteggiabile']}")
    print("=" * 68)
    print()


def scrivi_indice(righe: list[dict]) -> None:
    os.makedirs(MD.DIR_DATASET, exist_ok=True)
    with open(PERCORSO_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLONNE, extrasaction="ignore")
        w.writeheader()
        for r in sorted(righe, key=lambda x: (x["inizio"] or "")):
            w.writerow(r)
    with open(PERCORSO_JSON, "w", encoding="utf-8") as f:
        json.dump({"versione_schema": MD.VERSIONE_SCHEMA,
                   "stato": stato(righe),
                   "notti": sorted(righe, key=lambda x: (x["inizio"] or ""))},
                  f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Scritti:\n  {PERCORSO_CSV}\n  {PERCORSO_JSON}")


def verifica_audio(notti: list[dict]) -> int:
    """L'indice punta a file fuori dal repo: qui si controlla che ci siano ancora."""
    problemi = 0
    for meta in notti:
        cartella = _get(meta, "audio", "cartella")
        if not cartella:
            continue
        for voce in _get(meta, "audio", "file", default=[]) or []:
            p = os.path.join(cartella, voce["nome"])
            alt = p[:-4] + ".flac" if p.endswith(".wav") else None
            if os.path.exists(p):
                continue
            if alt and os.path.exists(alt):
                continue
            print(f"  MANCA  {meta['id_notte']}  {voce['nome']}")
            problemi += 1
    print("Verifica audio: " + ("tutto presente" if not problemi
                                else f"{problemi} file mancanti"))
    return problemi


def main(argv: list[str]) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("comando", nargs="?", default="stato",
                    choices=("aggiorna", "stato", "verifica"))
    ns = ap.parse_args(argv)

    notti = carica_notti()
    righe = [riga(m) for m in notti]

    if ns.comando == "verifica":
        return 1 if verifica_audio(notti) else 0
    if ns.comando == "aggiorna":
        scrivi_indice(righe)
    stampa_stato(righe)
    if ns.comando == "aggiorna":
        print("Ricordati di versionare l'indice:\n"
              "  git add software/acoustic/dataset/\n"
              "  (l'audio resta fuori dal repo — verifica il diff prima del commit)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
