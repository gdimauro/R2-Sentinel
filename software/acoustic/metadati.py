#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
metadati.py — schema dei metadati per notte di registrazione, R2-Sentinel Unità B.

Principio: **i metadati si raccolgono insieme al segnale, non dopo.**
Temperatura, umidità, finestra aperta o chiusa, persone in stanza sono
irrecuperabili a posteriori: fra tre mesi nessuno ricorderà se la notte del
27 agosto la finestra era aperta, e quella notte diventa un dato muto.

Il BME280 (§5.3) non è ancora montato. Lo schema prevede già i suoi campi e
una serie temporale; nel frattempo `fonte: "manuale"` con una lettura a inizio
e una a fine notte. Quando il sensore arriva cambia solo chi riempie i campi.

Un file JSON per notte, in `dataset/notti/`. Versionato in Git: è testo, piccolo,
diffabile. L'audio NON è versionato e sta fuori dal repository (vedi README).
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import sys

VERSIONE_SCHEMA = "1.0"

QUI = os.path.dirname(os.path.abspath(__file__))
DIR_DATASET = os.path.join(QUI, "dataset")
DIR_NOTTI = os.path.join(DIR_DATASET, "notti")

# Valori ammessi, tenuti qui per non spargere stringhe magiche nel codice.
ANNOTAZIONI = ("positiva", "negativa", "incerta", "da_annotare")
METODI_ANNOTAZIONE = (
    "uditivo",           # sentita ronzare durante la notte
    "punture",           # punture al risveglio
    "conteggio_catture", # trappola svuotata e contata (metodo forte)
    "analisi_offline",   # trovata riascoltando/analizzando lo spettro
    "nessuno",
)
FINESTRA = ("aperta", "chiusa", "zanzariera", "sconosciuta")
PRIVACY_VOCE = ("assente", "presente", "sconosciuto")


def adesso_iso() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def schema_notte_vuoto() -> dict:
    """Struttura completa di una notte. I None sono campi da riempire."""
    return {
        "versione_schema": VERSIONE_SCHEMA,

        # --- identità ------------------------------------------------------
        "id_notte": None,          # es. "2026-08-23_camera-nord_01"
        "sessione_id": None,
        "creato_il": adesso_iso(),
        "aggiornato_il": adesso_iso(),
        "operatore": None,

        # --- tempi ---------------------------------------------------------
        "inizio": None,            # ISO 8601 con offset, ora locale
        "fine": None,
        "durata_richiesta_s": None,
        "durata_audio_s": None,    # somma effettiva dei campioni scritti
        "durata_wall_s": None,     # tempo trascorso fra inizio e fine
        "campioni_totali": None,
        "n_gap": 0,                # interruzioni fra un processo e il successivo
        "gap_totale_s": 0.0,

        # --- catena di acquisizione ---------------------------------------
        "dispositivo": {
            "backend": None,           # avfoundation | alsa | pulse | i2s
            "spec": None,              # stringa passata a ffmpeg
            "nome": None,              # nome leggibile del dispositivo
            "modello_microfono": None, # es. "USB di misura", "ICS-43434"
            "sample_rate_hz": None,
            "sample_rate_nativo_hz": None,
            "ricampionato": False,     # True = il rate nativo non era 48 kHz
            "canali": 1,
            "bit": 16,
            "codec": "pcm_s16le",
            "guadagno_note": None,     # posizione manopola / gain di sistema
            "calibrato": False,        # nessun riferimento SPL disponibile (§10)
        },

        # --- posizione fisica ---------------------------------------------
        "posizione": {
            "stanza": None,
            "altezza_cm": None,        # obiettivo Unità B: ~120 cm (§4.3)
            "distanza_parete_cm": None,
            "supporto": None,          # treppiede | mensola | montante
            "disaccoppiamento": None,  # nulla | gommino | sospensione elastica
            "orientamento": None,
        },

        # --- ambiente (BME280 quando ci sarà) ------------------------------
        "ambiente": {
            "fonte": "manuale",        # manuale | bme280
            "temperatura_c_inizio": None,
            "temperatura_c_fine": None,
            "umidita_pct_inizio": None,
            "umidita_pct_fine": None,
            "pressione_hpa_inizio": None,
            "pressione_hpa_fine": None,
            "serie": [],               # [{"t": iso, "temp_c":, "umid_pct":, "press_hpa":}]
            "finestra": "sconosciuta",
            "persone_presenti": None,
            "animali_presenti": None,
            "luce_accesa": None,
            "condizionatore": None,
            "ventilatore": None,
            "meteo_esterno": None,
        },

        # --- esca / attuatori attivi durante la registrazione --------------
        "esca": {
            "presente": False,
            "tipo": None,              # co2_cartuccia | lievito | resistenza | nessuna
            "temperatura_c": None,
        },
        "ventola_aspirazione": {
            "presente": False,
            "accesa": False,
            "regime_pwm_pct": None,
            "distanza_microfono_cm": None,
        },

        # --- rumore di fondo dichiarato dall'operatore ---------------------
        "rumore": {
            "sorgenti_note": [],       # ["frigorifero", "ventola PC", "traffico"]
            "note": None,
            "rms_dbfs_mediano": None,  # riempito dal watchdog del registratore
            "picco_dbfs": None,
        },

        # --- annotazione ---------------------------------------------------
        "annotazione": {
            "esito": "da_annotare",    # positiva | negativa | incerta | da_annotare
            "controllo_negativo": False,  # notte raccolta DELIBERATAMENTE come controllo
            "metodo": "nessuno",
            "confidenza": None,        # alta | media | bassa
            "n_zanzare_osservate": None,
            "punture_al_risveglio": None,
            "catture_contate": None,
            "annotato_da": None,
            "annotato_il": None,
            "eventi": [],              # [{"file","inizio_s","fine_s","etichetta","f0_hz","confidenza","fonte"}]
            "note": None,
        },

        # --- privacy (CONTRIBUTING.md) -------------------------------------
        "privacy": {
            "voce_riconoscibile": "sconosciuto",
            "revisionato_da": None,
            "revisionato_il": None,
            "azione": "nessuna",       # nessuna | segmenti_eliminati | filtrata_passabanda
            "segmenti_rimossi": [],
            "pubblicabile": False,     # default: NO. Si alza solo dopo revisione.
        },

        # --- validità ai fini del gate di fase 1 ---------------------------
        "utile": None,                 # None = non ancora valutata
        "motivo_scarto": None,

        # --- inventario dei file (audio fuori dal repo) --------------------
        "audio": {
            "cartella": None,          # percorso assoluto, NON dentro il repo
            "formato": "wav",
            "n_file": 0,
            "byte_totali": 0,
            "file": [],                # [{"nome","offset_s","durata_s","byte"}]
        },

        "eventi_sessione": [],         # log del registratore: avvii, crash, riprese
        "note": None,
    }


# --------------------------------------------------------------------------
# I/O
# --------------------------------------------------------------------------

def percorso_notte(id_notte: str) -> str:
    return os.path.join(DIR_NOTTI, f"{id_notte}.json")


def salva(meta: dict, percorso: str | None = None) -> str:
    meta["aggiornato_il"] = adesso_iso()
    p = percorso or percorso_notte(meta["id_notte"])
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, p)   # scrittura atomica: un crash non lascia un JSON monco
    return p


def carica(percorso: str) -> dict:
    with open(percorso, encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------
# Validazione
# --------------------------------------------------------------------------

DURATA_MINIMA_UTILE_S = 6 * 3600
FS_RICHIESTO = 48000


def valida(meta: dict) -> list[str]:
    """Errori bloccanti per il conteggio del gate di fase 1."""
    e: list[str] = []
    g = meta.get

    if not g("id_notte"):
        e.append("id_notte mancante")
    if not g("inizio"):
        e.append("inizio mancante")

    d = meta.get("dispositivo", {})
    if d.get("sample_rate_hz") != FS_RICHIESTO:
        e.append(f"sample rate {d.get('sample_rate_hz')} != {FS_RICHIESTO} Hz richiesti")
    if d.get("ricampionato"):
        e.append("audio ricampionato: il rate nativo del dispositivo non era 48 kHz")

    dur = g("durata_audio_s")
    if dur is None:
        e.append("durata_audio_s non calcolata")
    elif dur < DURATA_MINIMA_UTILE_S:
        e.append(f"durata {dur/3600:.2f} h < 6 h richieste")

    a = meta.get("ambiente", {})
    if a.get("temperatura_c_inizio") is None:
        e.append("temperatura di inizio mancante (BME280 o manuale)")
    if a.get("umidita_pct_inizio") is None:
        e.append("umidità di inizio mancante (BME280 o manuale)")
    if a.get("finestra") in (None, "sconosciuta"):
        e.append("stato finestra non registrato")

    ann = meta.get("annotazione", {})
    if ann.get("esito") not in ("positiva", "negativa", "incerta"):
        e.append("annotazione presenza/assenza non ancora fatta")
    if ann.get("esito") == "negativa" and not ann.get("controllo_negativo"):
        e.append("notte negativa ma non marcata come controllo deliberato "
                 "(annotazione.controllo_negativo)")

    p = meta.get("privacy", {})
    if p.get("voce_riconoscibile") == "sconosciuto":
        e.append("revisione privacy non fatta (privacy.voce_riconoscibile)")

    return e


def avvertimenti(meta: dict) -> list[str]:
    """Non bloccano il conteggio, ma degradano la qualità del dato."""
    w: list[str] = []
    if (meta.get("n_gap") or 0) > 0:
        w.append(f"{meta['n_gap']} interruzione/i, {meta.get('gap_totale_s', 0):.1f} s persi")
    r = meta.get("rumore", {})
    if r.get("rms_dbfs_mediano") is not None and r["rms_dbfs_mediano"] < -75:
        w.append(f"livello medio molto basso ({r['rms_dbfs_mediano']:.1f} dBFS): "
                 "microfono muto o guadagno insufficiente?")
    if r.get("picco_dbfs") is not None and r["picco_dbfs"] > -1.0:
        w.append(f"picco a {r['picco_dbfs']:.1f} dBFS: probabile clipping")
    pos = meta.get("posizione", {})
    if pos.get("altezza_cm") is not None and pos["altezza_cm"] < 100:
        w.append(f"microfono a {pos['altezza_cm']} cm: le zanzare stanno in alto "
                 "(§4.3 prevede ~120 cm)")
    if meta.get("privacy", {}).get("voce_riconoscibile") == "presente" \
            and meta.get("privacy", {}).get("azione") == "nessuna":
        w.append("voce riconoscibile presente e nessuna azione di mitigazione")
    return w


# --------------------------------------------------------------------------
# CLI di annotazione — pensata per il mattino dopo, mezzo addormentati
# --------------------------------------------------------------------------

def _cerca_notte(chiave: str) -> str:
    if os.path.isfile(chiave):
        return chiave
    p = percorso_notte(chiave)
    if os.path.isfile(p):
        return p
    if os.path.isdir(DIR_NOTTI):
        cand = [f for f in sorted(os.listdir(DIR_NOTTI))
                if f.endswith(".json") and chiave in f]
        if len(cand) == 1:
            return os.path.join(DIR_NOTTI, cand[0])
        if len(cand) > 1:
            raise SystemExit("Chiave ambigua, corrispondono:\n  " + "\n  ".join(cand))
    raise SystemExit(f"Notte non trovata: {chiave}")


def _main(argv: list[str]) -> int:
    import argparse
    ap = argparse.ArgumentParser(
        description="Ispeziona e annota i metadati di una notte.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("mostra", help="stampa i metadati e la validazione")
    m.add_argument("notte")

    a = sub.add_parser("annota", help="chiude l'annotazione di una notte")
    a.add_argument("notte")
    a.add_argument("--esito", choices=("positiva", "negativa", "incerta"), required=True)
    a.add_argument("--controllo-negativo", action="store_true",
                   help="la notte è stata raccolta DELIBERATAMENTE come controllo")
    a.add_argument("--metodo", choices=METODI_ANNOTAZIONE, default="uditivo")
    a.add_argument("--confidenza", choices=("alta", "media", "bassa"), default="media")
    a.add_argument("--zanzare", type=int, default=None)
    a.add_argument("--punture", type=int, default=None)
    a.add_argument("--catture", type=int, default=None)
    a.add_argument("--da", default=os.environ.get("USER"))
    a.add_argument("--note", default=None)

    v = sub.add_parser("privacy", help="registra l'esito della revisione privacy")
    v.add_argument("notte")
    v.add_argument("--voce", choices=PRIVACY_VOCE, required=True)
    v.add_argument("--azione", choices=("nessuna", "segmenti_eliminati",
                                        "filtrata_passabanda"), default="nessuna")
    v.add_argument("--da", default=os.environ.get("USER"))

    b = sub.add_parser("ambiente", help="inserisce a mano i dati ambientali (finché manca il BME280)")
    b.add_argument("notte")
    b.add_argument("--temp-inizio", type=float)
    b.add_argument("--temp-fine", type=float)
    b.add_argument("--umid-inizio", type=float)
    b.add_argument("--umid-fine", type=float)
    b.add_argument("--finestra", choices=FINESTRA)
    b.add_argument("--persone", type=int)
    b.add_argument("--sorgenti-rumore", default=None,
                   help="elenco separato da virgole, es. 'frigorifero,ventola PC'")

    u = sub.add_parser("utile", help="marca la notte come utile o scartata")
    u.add_argument("notte")
    u.add_argument("--si", dest="utile", action="store_true")
    u.add_argument("--no", dest="utile", action="store_false")
    u.add_argument("--motivo", default=None)
    u.set_defaults(utile=True)

    ns = ap.parse_args(argv)
    p = _cerca_notte(ns.notte)
    meta = carica(p)

    if ns.cmd == "mostra":
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        err = valida(meta)
        avv = avvertimenti(meta)
        print("\n--- validazione ---")
        print("BLOCCANTI:" if err else "BLOCCANTI: nessuno")
        for x in err:
            print("  ✗", x)
        if avv:
            print("AVVERTIMENTI:")
            for x in avv:
                print("  !", x)
        return 0

    if ns.cmd == "annota":
        ann = meta["annotazione"]
        ann["esito"] = ns.esito
        ann["controllo_negativo"] = bool(ns.controllo_negativo) or ns.esito == "negativa" and ann.get("controllo_negativo", False)
        if ns.controllo_negativo:
            ann["controllo_negativo"] = True
        ann["metodo"] = ns.metodo
        ann["confidenza"] = ns.confidenza
        if ns.zanzare is not None:
            ann["n_zanzare_osservate"] = ns.zanzare
        if ns.punture is not None:
            ann["punture_al_risveglio"] = ns.punture
        if ns.catture is not None:
            ann["catture_contate"] = ns.catture
        ann["annotato_da"] = ns.da
        ann["annotato_il"] = adesso_iso()
        if ns.note:
            ann["note"] = ns.note

    elif ns.cmd == "privacy":
        meta["privacy"]["voce_riconoscibile"] = ns.voce
        meta["privacy"]["azione"] = ns.azione
        meta["privacy"]["revisionato_da"] = ns.da
        meta["privacy"]["revisionato_il"] = adesso_iso()
        meta["privacy"]["pubblicabile"] = (ns.voce == "assente")

    elif ns.cmd == "ambiente":
        amb = meta["ambiente"]
        for campo, val in (("temperatura_c_inizio", ns.temp_inizio),
                           ("temperatura_c_fine", ns.temp_fine),
                           ("umidita_pct_inizio", ns.umid_inizio),
                           ("umidita_pct_fine", ns.umid_fine),
                           ("persone_presenti", ns.persone)):
            if val is not None:
                amb[campo] = val
        if ns.finestra:
            amb["finestra"] = ns.finestra
        if ns.sorgenti_rumore:
            meta["rumore"]["sorgenti_note"] = [
                s.strip() for s in ns.sorgenti_rumore.split(",") if s.strip()]

    elif ns.cmd == "utile":
        meta["utile"] = ns.utile
        meta["motivo_scarto"] = ns.motivo if not ns.utile else None

    salva(meta, p)
    err = valida(meta)
    print(f"Aggiornato: {p}")
    if err:
        print("Manca ancora per il conteggio del gate:")
        for x in err:
            print("  ✗", x)
    else:
        print("✓ notte completa e conteggiabile")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
