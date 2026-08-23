#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
genera_test.py — generatore di segnale sintetico di verifica.

A cosa serve. Finché non esiste una notte reale annotata non c'è modo di sapere
se `spettro.py` trova quello che deve trovare o se sta allucinando. Questo
generatore produce un WAV a 48 kHz con **verità nota**: rumore di fondo
domestico plausibile, un ronzio da elettrodomestico, e N "passaggi di zanzara"
a frequenza fondamentale nota con 2a e 3a armonica.

Il file di verità in JSON accanto al WAV permette di misurare recall e falsi
positivi del rilevatore PRIMA di avere dati veri. Non sostituisce le zanzare —
un tono sintetico è molto più pulito di un insetto reale in una stanza reale,
quindi i numeri ottenuti qui sono un limite superiore ottimistico, non una
stima. Serve a scoprire i bug del rilevatore, non a validarlo.

Uso:
    python3 genera_test.py prova.wav --passaggi 6 --durata 120
    python3 spettro.py firma prova.wav
    python3 genera_test.py --verifica prova.wav      # confronta con la verità
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import struct
import sys
import wave

FS = 48000


def genera(percorso: str, durata_s: float, n_passaggi: int, seme: int,
           rumore_db: float, snr_db: float, con_voce: bool) -> dict:
    random.seed(seme)
    n = int(FS * durata_s)

    ampiezza_rumore = 10 ** (rumore_db / 20.0)
    ampiezza_zanzara = ampiezza_rumore * 10 ** (snr_db / 20.0)

    # passaggi: istante, durata, f0 nel range Culex/Aedes (§11)
    passaggi = []
    for _ in range(n_passaggi):
        t0 = random.uniform(2.0, max(3.0, durata_s - 6.0))
        dur = random.uniform(0.6, 3.0)
        f0 = random.uniform(400.0, 600.0)
        passaggi.append({"inizio_s": round(t0, 3), "fine_s": round(t0 + dur, 3),
                         "f0_hz": round(f0, 1)})
    passaggi.sort(key=lambda p: p["inizio_s"])

    # fasi accumulate: l'unico modo corretto di sintetizzare un tono a
    # frequenza variabile. Scrivere sin(2*pi*f(t)*t) è l'errore classico e
    # produce uno sweep enorme invece di un vibrato.
    fasi = [0.0] * n_passaggi
    lp = 0.0
    campioni = []
    fase_voce = 0.0

    for i in range(n):
        t = i / FS
        w = random.uniform(-1.0, 1.0)
        lp = 0.995 * lp + 0.005 * w
        x = ampiezza_rumore * (0.35 * w + 6.0 * lp)          # fondo largo
        x += ampiezza_rumore * 2.0 * math.sin(2 * math.pi * 120.0 * t)  # frigorifero
        x += ampiezza_rumore * 0.8 * math.sin(2 * math.pi * 240.0 * t)

        if con_voce and 0.25 * durata_s < t < 0.25 * durata_s + 4.0:
            # sagoma vocale grezza: f0 ~140 Hz modulata + formanti
            f_voce = 140.0 + 25.0 * math.sin(2 * math.pi * 1.7 * t)
            fase_voce += 2 * math.pi * f_voce / FS
            x += ampiezza_rumore * 3.0 * (math.sin(fase_voce)
                                          + 0.6 * math.sin(3 * fase_voce)
                                          + 0.4 * math.sin(14 * fase_voce)
                                          + 0.3 * math.sin(19 * fase_voce))

        for k, p in enumerate(passaggi):
            if p["inizio_s"] <= t < p["fine_s"]:
                u = (t - p["inizio_s"]) / (p["fine_s"] - p["inizio_s"])
                env = math.sin(math.pi * u) ** 2          # avvicinamento/allontanamento
                # vibrato ±1,5% attorno a f0: una zanzara non è un oscillatore
                f = p["f0_hz"] * (1.0 + 0.015 * math.sin(2 * math.pi * 4.0 * t))
                fasi[k] += 2 * math.pi * f / FS
                ph = fasi[k]
                x += ampiezza_zanzara * env * (
                    1.00 * math.sin(ph)
                    + 0.40 * math.sin(2 * ph + 0.7)
                    + 0.18 * math.sin(3 * ph + 1.9))
            else:
                fasi[k] += 2 * math.pi * p["f0_hz"] / FS   # mantiene continuità

        campioni.append(max(-1.0, min(0.999, x)))

    with wave.open(percorso, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(FS)
        w.writeframes(b"".join(struct.pack("<h", int(v * 32767)) for v in campioni))

    verita = {"file": os.path.basename(percorso), "fs_hz": FS,
              "durata_s": durata_s, "seme": seme,
              "rumore_dbfs": rumore_db, "snr_db": snr_db,
              "voce_sintetica": con_voce, "passaggi": passaggi}
    with open(percorso + ".verita.json", "w", encoding="utf-8") as f:
        json.dump(verita, f, ensure_ascii=False, indent=2)
    return verita


def verifica(percorso_wav: str, tolleranza_hz: float = 15.0) -> int:
    """Confronta l'uscita di spettro.py con la verità nota.

    Tolleranza 15 Hz: è esattamente il ±15 Hz richiesto dal criterio di FATTO
    della fase 5 sulla localizzazione della fondamentale.
    """
    qui = os.path.dirname(os.path.abspath(__file__))
    if qui not in sys.path:
        sys.path.insert(0, qui)
    import spettro  # noqa: E402

    with open(percorso_wav + ".verita.json", encoding="utf-8") as f:
        verita = json.load(f)

    ris = spettro.analizza_file(percorso_wav, 0.0, None, spettro.NFFT, None, 20000)
    eventi = spettro.cerca_firma(ris, 400.0, 600.0, snr_db=10.0,
                                 snr_arm_db=6.0, tol_arm=0.04,
                                 min_armoniche=1, durata_min_s=0.3,
                                 buco_max_frame=2)

    veri = verita["passaggi"]
    trovati = []
    for v in veri:
        migliore = None
        for e in eventi:
            if e["fine_s"] >= v["inizio_s"] and e["inizio_s"] <= v["fine_s"]:
                if migliore is None or e["durata_s"] > migliore["durata_s"]:
                    migliore = e
        trovati.append((v, migliore))

    print()
    print("=" * 74)
    print("  VERIFICA DEL RILEVATORE SU VERITÀ NOTA")
    print("=" * 74)
    print(f"  {'atteso f0':>10}{'trovato f0':>12}{'errore':>9}"
          f"{'t atteso':>10}{'arm':>5}  esito")
    print("  " + "-" * 69)
    ok_rec = 0
    ok_freq = 0
    ok_arm = 0
    for v, e in trovati:
        if e is None:
            print(f"  {v['f0_hz']:>10.1f}{'-':>12}{'-':>9}"
                  f"{v['inizio_s']:>10.2f}{'-':>5}  MANCATO")
            continue
        ok_rec += 1
        err = e["f0_hz"] - v["f0_hz"]
        buono = abs(err) <= tolleranza_hz
        ok_freq += 1 if buono else 0
        ok_arm += 1 if e["n_armoniche"] >= 2 else 0
        print(f"  {v['f0_hz']:>10.1f}{e['f0_hz']:>12.1f}{err:>9.1f}"
              f"{v['inizio_s']:>10.2f}{e['n_armoniche']:>5}  "
              f"{'ok' if buono else 'FUORI ±%.0f Hz' % tolleranza_hz}")

    # falsi positivi: eventi che non si sovrappongono a nessuna verità
    fp = [e for e in eventi
          if not any(e["fine_s"] >= v["inizio_s"] and e["inizio_s"] <= v["fine_s"]
                     for v in veri)]
    n = len(veri)
    durata_h = verita["durata_s"] / 3600.0
    print("  " + "-" * 69)
    print(f"  recall                 {ok_rec}/{n} = {ok_rec/n:.2f}"
          f"   (criterio fase 5: ≥0,90)")
    print(f"  f0 entro ±{tolleranza_hz:.0f} Hz      {ok_freq}/{n}")
    print(f"  con ≥2 armoniche       {ok_arm}/{n}")
    print(f"  falsi positivi         {len(fp)}  "
          f"({len(fp)/durata_h:.2f}/h, criterio fase 5: ≤1/h)")
    for e in fp:
        print(f"      spurio a {e['inizio_s']:.2f} s, f0 {e['f0_hz']:.1f} Hz, "
              f"SNR {e['snr_medio_db']:.1f} dB")
    print("=" * 74)
    print("\n  Segnale SINTETICO: questi numeri sono un limite superiore")
    print("  ottimistico. Non sostituiscono il gate di fase 5, che va misurato")
    print("  su 8 h di registrazione notturna reale non usata in training.\n")
    return 0 if ok_rec == n else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="WAV da generare (o da verificare)")
    ap.add_argument("--verifica", action="store_true",
                    help="non genera: confronta il rilevatore con la verità nota")
    ap.add_argument("--durata", type=float, default=120.0)
    ap.add_argument("--passaggi", type=int, default=6)
    ap.add_argument("--seme", type=int, default=2026)
    ap.add_argument("--rumore-dbfs", type=float, default=-52.0)
    ap.add_argument("--snr-db", type=float, default=18.0,
                    help="quanto la zanzara emerge dal fondo (prova 6, 12, 18)")
    ap.add_argument("--con-voce", action="store_true",
                    help="aggiunge 4 s di voce sintetica, per provare lo "
                         "screening privacy di spettro.py")
    ns = ap.parse_args(argv)

    if ns.verifica:
        return verifica(ns.file)
    v = genera(ns.file, ns.durata, ns.passaggi, ns.seme, ns.rumore_dbfs,
               ns.snr_db, ns.con_voce)
    print(f"Scritto {ns.file}  ({v['durata_s']:.0f} s, {len(v['passaggi'])} passaggi)")
    for p in v["passaggi"]:
        print(f"  {p['inizio_s']:7.2f}–{p['fine_s']:6.2f} s   f0 {p['f0_hz']:6.1f} Hz")
    print(f"Verità: {ns.file}.verita.json")
    print(f"Ora:  python3 genera_test.py {ns.file} --verifica")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
