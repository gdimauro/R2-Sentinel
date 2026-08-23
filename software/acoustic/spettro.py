#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
spettro.py — analisi spettrale della banda 300–800 Hz, R2-Sentinel Unità B.

Quattro cose, tutte necessarie e in quest'ordine di utilità:

  rumore        Caratterizza il rumore di fondo notturno della stanza.
                È il PRIMO dato utile ottenibile: si può produrre domani
                mattina, sulla prima notte, prima di avere una sola zanzara
                annotata. Il rumore di fondo è l'avversario vero — frigorifero,
                ventole, traffico — e definisce il pavimento sotto cui nessun
                classificatore potrà mai scendere.

  firma         Cerca la firma del battito alare: fondamentale in 400–600 Hz
                (§11) con armoniche a 2f e 3f. Le armoniche NON sono un
                dettaglio: sono ciò che distingue una zanzara da una nota di
                un elettrodomestico, e il criterio di FATTO della fase 5 ne
                chiede almeno due documentate.

  ventola       Quantifica in dB quanto la ventola centrifuga da 80 mm
                dell'Unità B invade la banda utile. È il numero che decide se
                serve un ciclo alternato ascolto/aspirazione — questione
                aperta in §10, da chiudere PRIMA che il montante venga
                congelato da `mechatronics`.

  spettrogramma Rendering ASCII, perché matplotlib non è una dipendenza e
                guardare i dati non deve richiedere un'installazione.

Tutti i livelli sono **dBFS**, non dB SPL: manca un riferimento acustico
calibrato (§10). I confronti relativi e i delta on/off sono validi; i valori
assoluti no.

Uso tipico:
    python3 spettro.py rumore ~/r2-sentinel-audio/2026-08-23_camera_*.wav
    python3 spettro.py firma  ~/r2-sentinel-audio/2026-08-23_camera_0130*.wav
    python3 spettro.py ventola --con ventola_on.wav --senza ventola_off.wav
    python3 spettro.py spettrogramma segmento.wav --inizio 120 --durata 30
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
if QUI not in sys.path:
    sys.path.insert(0, QUI)

import dsp as DSP      # noqa: E402
import metadati as MD  # noqa: E402


FS_ANALISI = 6000       # Nyquist 3000 Hz: fondamentale + 2a + 3a armonica
NFFT = 2048             # 341 ms di finestra, 2,93 Hz di risoluzione
BANDA_ZANZARA = (400.0, 600.0)
BANDA_UTILE = (300.0, 800.0)

# Sotto-bande per il referto del rumore di fondo. La scelta non è estetica:
# separa le sorgenti domestiche tipiche dalla banda della zanzara e dalle sue
# armoniche, così il referto dice *quale* rumore dà fastidio e non solo quanto.
SOTTOBANDE = [
    ("20-100 Hz    infrasuoni, HVAC, calpestio", 20, 100),
    ("100-300 Hz   rete 50 Hz e armoniche, motori, voce (f0)", 100, 300),
    ("300-400 Hz   spalla bassa della banda utile", 300, 400),
    ("400-450 Hz   ZANZARA (Culex, basso)", 400, 450),
    ("450-500 Hz   ZANZARA", 450, 500),
    ("500-550 Hz   ZANZARA", 500, 550),
    ("550-600 Hz   ZANZARA (Aedes, alto)", 550, 600),
    ("600-800 Hz   spalla alta, mosche/moscerini", 600, 800),
    ("800-1200 Hz  2a armonica zanzara", 800, 1200),
    ("1200-1800 Hz 3a armonica zanzara", 1200, 1800),
    ("1800-3000 Hz formanti vocali, sibilanti", 1800, 3000),
]


# ==========================================================================
# Caricamento
# ==========================================================================

def espandi(percorsi: list[str]) -> list[str]:
    fuori = []
    for p in percorsi:
        if os.path.isdir(p):
            fuori += [os.path.join(p, f) for f in sorted(os.listdir(p))
                      if f.lower().endswith((".wav", ".flac"))]
        else:
            fuori.append(p)
    if not fuori:
        raise SystemExit("Nessun file audio da analizzare.")
    return fuori


def analizza_file(percorso: str, inizio: float, durata: float | None,
                  nfft: int, passo_s: float | None, max_frame: int):
    camp, fs = DSP.leggi_audio(percorso, fs_target=FS_ANALISI,
                               inizio_s=inizio, durata_s=durata)
    if len(camp) < nfft:
        return None
    return DSP.analizza(camp, fs, nfft=nfft, sovrapposizione=0.5,
                        passo_s=passo_s, max_frame=max_frame)


# ==========================================================================
# Comando: rumore
# ==========================================================================

def picchi_tonali(freq, spettro_mediano, larghezza_hz=60.0, soglia_db=6.0,
                  n_max=12):
    """Componenti tonali stabili: bin che superano di `soglia_db` la mediana
    del proprio intorno. Sono frigoriferi, alimentatori, ventole — cioè le
    sorgenti che un classificatore ingenuo scambierebbe per battito alare."""
    if len(freq) < 3:
        return []
    df = freq[1] - freq[0]
    raggio = max(3, int(larghezza_hz / df / 2))
    trovati = []
    for i in range(raggio, len(freq) - raggio):
        intorno = [spettro_mediano[j] for j in range(i - raggio, i + raggio + 1)
                   if abs(j - i) > 2]
        m = DSP.mediana(intorno)
        if m <= 0:
            continue
        prom = DSP.db(float(spettro_mediano[i]) / m)
        if prom >= soglia_db:
            trovati.append((float(freq[i]), prom, DSP.db(float(spettro_mediano[i]))))
    # tiene solo i massimi locali fra picchi vicini
    trovati.sort(key=lambda x: -x[1])
    scelti = []
    for f, prom, liv in trovati:
        if all(abs(f - g) > larghezza_hz / 2 for g, _, _ in scelti):
            scelti.append((f, prom, liv))
        if len(scelti) >= n_max:
            break
    return sorted(scelti, key=lambda x: x[0])


def screening_voce(ris, quota_db=10.0):
    """Screening GREZZO della presenza di voce, per la procedura privacy.

    NON è un VAD e non va usato come garanzia. Segnala i frame in cui c'è
    energia simultanea nella banda della fondamentale vocale (100–300 Hz) e in
    quella delle formanti alte/sibilanti (1800–3000 Hz), entrambe sopra la
    mediana notturna. Serve a dire *dove riascoltare*, non a decidere da solo.
    """
    if not ris.potenze:
        return {"frazione_frame": 0.0, "istanti": []}
    p_basse, p_alte = [], []
    for fr in ris.potenze:
        p_basse.append(DSP.potenza_banda(fr, ris.frequenze, 100, 300))
        p_alte.append(DSP.potenza_banda(fr, ris.frequenze, 1800, 3000))
    med_b = DSP.mediana(p_basse) or 1e-30
    med_a = DSP.mediana(p_alte) or 1e-30
    istanti = []
    for i, (b, a) in enumerate(zip(p_basse, p_alte)):
        if DSP.db(b / med_b) > quota_db and DSP.db(a / med_a) > quota_db:
            istanti.append(round(ris.tempi[i], 2))
    return {"frazione_frame": len(istanti) / float(len(ris.potenze)),
            "istanti": istanti[:200]}


def comando_rumore(ns) -> int:
    file_lista = espandi(ns.file)
    aggregato = None
    n_frame_tot = 0
    voce_frazioni = []
    durata_tot = 0.0

    for p in file_lista:
        ris = analizza_file(p, ns.inizio, ns.durata, ns.nfft, ns.passo_s,
                            ns.max_frame)
        if ris is None or not ris.potenze:
            print(f"  (saltato, troppo corto) {os.path.basename(p)}")
            continue
        st = DSP.statistiche_per_bin(ris, quantili=(0.5, 0.95))
        voce_frazioni.append(screening_voce(ris)["frazione_frame"])
        n_frame_tot += st["n_frame"]
        durata_tot += (ris.tempi[-1] - ris.tempi[0]) if len(ris.tempi) > 1 else 0.0
        if aggregato is None:
            aggregato = {"freq": ris.frequenze,
                         "mediana": list(st["quantili"][0.5]),
                         "p95": list(st["quantili"][0.95]),
                         "n": 1}
        else:
            # media delle mediane dei singoli file: sufficiente e robusta,
            # evita di tenere in memoria tutti i frame della notte
            for i in range(len(aggregato["mediana"])):
                aggregato["mediana"][i] += st["quantili"][0.5][i]
                aggregato["p95"][i] += st["quantili"][0.95][i]
            aggregato["n"] += 1
        print(f"  analizzato {os.path.basename(p)}  ({st['n_frame']} frame)")

    if aggregato is None:
        print("Nessun file analizzabile.")
        return 1
    n = aggregato["n"]
    med = [v / n for v in aggregato["mediana"]]
    p95 = [v / n for v in aggregato["p95"]]
    freq = aggregato["freq"]

    print()
    print("=" * 76)
    print("  RUMORE DI FONDO NOTTURNO — livelli in dBFS (non SPL, non calibrato)")
    print("=" * 76)
    print(f"  file analizzati {len(file_lista)}   frame {n_frame_tot}   "
          f"risoluzione {FS_ANALISI/ns.nfft:.2f} Hz")
    print()
    print(f"  {'banda':<44}{'mediana':>9}{'p95':>9}{'p95-med':>9}")
    print("  " + "-" * 71)
    referto_bande = []
    for etichetta, f0, f1 in SOTTOBANDE:
        pm = DSP.potenza_banda(med, freq, f0, f1)
        pp = DSP.potenza_banda(p95, freq, f0, f1)
        dm, dp = DSP.db(pm), DSP.db(pp)
        marca = " <<<" if 400 <= f0 < 600 else ""
        print(f"  {etichetta:<44}{dm:>9.1f}{dp:>9.1f}{dp-dm:>9.1f}{marca}")
        referto_bande.append({"banda": etichetta, "f_min": f0, "f_max": f1,
                              "mediana_db": round(dm, 2), "p95_db": round(dp, 2)})

    pm_z = DSP.db(DSP.potenza_banda(med, freq, *BANDA_ZANZARA))
    pm_u = DSP.db(DSP.potenza_banda(med, freq, *BANDA_UTILE))
    print("  " + "-" * 71)
    print(f"  {'BANDA ZANZARA 400-600 Hz (pavimento di rumore)':<44}{pm_z:>9.1f}")
    print(f"  {'BANDA UTILE 300-800 Hz':<44}{pm_u:>9.1f}")

    print("\n  Componenti tonali stabili (le sorgenti da battere):")
    picchi = picchi_tonali(freq, med, soglia_db=ns.soglia_tonale)
    if not picchi:
        print("    nessuna emergenza tonale sopra "
              f"{ns.soglia_tonale:.0f} dB — stanza acusticamente pulita")
    for f, prom, liv in picchi:
        nota = ""
        if abs(f % 50.0) < 3 or abs(50.0 - (f % 50.0)) < 3:
            nota = "  (multiplo di 50 Hz: rete elettrica)"
        if BANDA_ZANZARA[0] <= f <= BANDA_ZANZARA[1]:
            nota += "  *** DENTRO LA BANDA ZANZARA ***"
        print(f"    {f:7.1f} Hz   prominenza {prom:5.1f} dB   livello {liv:6.1f} dBFS{nota}")

    fv = sum(voce_frazioni) / len(voce_frazioni) if voce_frazioni else 0.0
    print(f"\n  Screening voce (grezzo): {fv*100:.2f}% dei frame sospetti.")
    if fv > 0.005:
        print("    -> riascoltare quei tratti PRIMA di condividere qualunque audio.")
    print("=" * 76)
    print()

    referto = {"tipo": "rumore", "file": file_lista, "n_frame": n_frame_tot,
               "fs_analisi_hz": FS_ANALISI, "nfft": ns.nfft,
               "bande": referto_bande,
               "banda_zanzara_400_600_db": round(pm_z, 2),
               "banda_utile_300_800_db": round(pm_u, 2),
               "picchi_tonali": [{"hz": round(f, 1), "prominenza_db": round(pr, 1),
                                  "livello_db": round(lv, 1)} for f, pr, lv in picchi],
               "frazione_frame_sospetti_voce": round(fv, 5)}
    _scrivi_uscite(ns, referto, None)
    return 0


# ==========================================================================
# Comando: firma
# ==========================================================================

def cerca_firma(ris, f_min, f_max, snr_db, snr_arm_db, tol_arm,
                min_armoniche, durata_min_s, buco_max_frame,
                rifiuto_voce_db=4.0):
    """Rileva i tratti in cui c'è un tono in banda con struttura armonica.

    Metodo: pavimento di rumore per-bin = mediana temporale del file stesso.
    Scelta deliberata rispetto a un pavimento assoluto: il livello di fondo di
    una stanza cambia di notte in notte e di casa in casa, e una soglia fissa
    in dBFS sarebbe tarata su un solo salotto. La mediana temporale è immune
    agli eventi rari — cioè proprio alle zanzare, che sono rare per definizione.

    Reiettore di voce (`rifiuto_voce_db`). Misurato su segnale sintetico: la
    struttura armonica NON basta a distinguere una zanzara da una vocale umana,
    perché le armoniche di una voce a 140 Hz cadono in pieno nella banda
    400–600 Hz e sono altrettanto regolari. Restava l'unico falso positivo
    anche portando la soglia SNR a 16 dB. Discriminante che funziona: la voce
    porta con sé la propria fondamentale in 100–300 Hz, la zanzara no. Un frame
    in cui la banda 100–300 Hz è elevata di più di `rifiuto_voce_db` sopra la
    propria mediana notturna viene scartato.
    Separazione misurata sul sintetico: voce +4,7 dB mediani, zanzara +0,0 dB.
    DA RIVALIDARE su audio reale: in una stanza vera quella banda contiene
    anche frigorifero e traffico, e la normalizzazione sulla mediana ne
    assorbe solo la parte stazionaria.
    """
    st = DSP.statistiche_per_bin(ris, quantili=(0.5,))
    if not st["n_frame"]:
        return []
    pavimento = st["quantili"][0.5]
    freq = ris.frequenze

    if rifiuto_voce_db > 0:
        p_basse = [DSP.potenza_banda(fr, freq, 100, 300) for fr in ris.potenze]
        med_basse = DSP.mediana(p_basse) or 1e-30
    else:
        p_basse, med_basse = None, 1.0

    def snr_in(fr, centro, tolleranza):
        p = DSP.picco_interpolato(fr, freq, centro * (1 - tolleranza),
                                  centro * (1 + tolleranza))
        if p is None:
            return None, None
        f_pic, pot, idx = p
        base = float(pavimento[idx]) or 1e-30
        return f_pic, DSP.db(pot / base)

    candidati = []
    n_scartati_voce = 0
    for i, fr in enumerate(ris.potenze):
        if p_basse is not None and DSP.db(p_basse[i] / med_basse) > rifiuto_voce_db:
            n_scartati_voce += 1
            continue
        p = DSP.picco_interpolato(fr, freq, f_min, f_max)
        if p is None:
            continue
        f0, pot, idx = p
        base = float(pavimento[idx]) or 1e-30
        s0 = DSP.db(pot / base)
        if s0 < snr_db:
            continue
        armoniche = []
        for k in (2, 3, 4):
            if k * f0 > ris.fs / 2.0 * 0.95:
                break
            fk, sk = snr_in(fr, k * f0, tol_arm)
            if sk is not None and sk >= snr_arm_db:
                armoniche.append({"k": k, "hz": round(fk, 1), "snr_db": round(sk, 1)})
        if len(armoniche) < min_armoniche:
            continue
        candidati.append({"i": i, "t": ris.tempi[i], "f0": f0, "snr": s0,
                          "armoniche": armoniche})

    # raggruppa i frame contigui in eventi
    eventi = []
    gruppo = []
    for c in candidati:
        if gruppo and c["i"] - gruppo[-1]["i"] > buco_max_frame + 1:
            eventi.append(gruppo)
            gruppo = []
        gruppo.append(c)
    if gruppo:
        eventi.append(gruppo)

    passo_t = (ris.tempi[1] - ris.tempi[0]) if len(ris.tempi) > 1 else 0.0
    fuori = []
    for g in eventi:
        durata = (g[-1]["t"] - g[0]["t"]) + passo_t
        if durata < durata_min_s:
            continue
        f0s = [c["f0"] for c in g]
        f0_med = DSP.mediana(f0s)
        var = sum((x - f0_med) ** 2 for x in f0s) / len(f0s)
        n_arm_max = max(len(c["armoniche"]) for c in g)
        arm_rappr = max((c["armoniche"] for c in g), key=len)
        fuori.append({
            "inizio_s": round(g[0]["t"] - passo_t / 2, 3),
            "fine_s": round(g[-1]["t"] + passo_t / 2, 3),
            "durata_s": round(durata, 3),
            "f0_hz": round(f0_med, 1),
            "f0_min_hz": round(min(f0s), 1),
            "f0_max_hz": round(max(f0s), 1),
            "f0_dispersione_hz": round(math.sqrt(var), 2),
            "snr_medio_db": round(sum(c["snr"] for c in g) / len(g), 1),
            "n_armoniche": n_arm_max,
            "armoniche": arm_rappr,
            "n_frame": len(g),
        })
    if fuori:
        fuori[0]["_frame_scartati_voce"] = n_scartati_voce
    return fuori


def comando_firma(ns) -> int:
    file_lista = espandi(ns.file)
    tutti = []
    for p in file_lista:
        ris = analizza_file(p, ns.inizio, ns.durata, ns.nfft, None, ns.max_frame)
        if ris is None or not ris.potenze:
            continue
        ev = cerca_firma(ris, ns.f_min, ns.f_max, ns.snr, ns.snr_armoniche,
                         ns.tolleranza_armonica, ns.min_armoniche,
                         ns.durata_min, ns.buco_max)
        for e in ev:
            e["file"] = os.path.basename(p)
        tutti += ev
        durata_file = (ris.tempi[-1] - ris.tempi[0]) if len(ris.tempi) > 1 else 0
        print(f"  {os.path.basename(p):<44} {len(ev):>4} eventi "
              f"su {durata_file/60:.1f} min")

    print()
    print("=" * 86)
    print("  CANDIDATI FIRMA BATTITO ALARE — banda "
          f"{ns.f_min:.0f}-{ns.f_max:.0f} Hz, SNR ≥ {ns.snr:.0f} dB, "
          f"≥{ns.min_armoniche} armonica/he")
    print("=" * 86)
    if not tutti:
        print("  Nessun candidato. Non è una notizia cattiva: su una notte di")
        print("  controllo negativo è esattamente il risultato atteso.")
    else:
        print(f"  {'file':<30}{'t_ini':>9}{'durata':>8}{'f0':>9}"
              f"{'disp':>7}{'SNR':>7}{'arm':>5}")
        print("  " + "-" * 81)
        for e in tutti:
            print(f"  {e['file'][:29]:<30}{e['inizio_s']:>9.2f}{e['durata_s']:>8.2f}"
                  f"{e['f0_hz']:>9.1f}{e['f0_dispersione_hz']:>7.2f}"
                  f"{e['snr_medio_db']:>7.1f}{e['n_armoniche']:>5}")
        f0s = [e["f0_hz"] for e in tutti]
        print("  " + "-" * 81)
        print(f"  eventi {len(tutti)}   f0 mediana {DSP.mediana(f0s):.1f} Hz   "
              f"intervallo {min(f0s):.1f}–{max(f0s):.1f} Hz")
        con2 = sum(1 for e in tutti if e["n_armoniche"] >= 2)
        print(f"  eventi con ≥2 armoniche: {con2}/{len(tutti)} "
              "(il criterio di fase 5 chiede ≥2 armoniche documentate)")
    print("=" * 86)
    print("\n  ATTENZIONE: questi sono CANDIDATI, non zanzare. Vanno confermati")
    print("  all'ascolto prima di diventare annotazioni. Un tono stabile a f0")
    print("  costante per minuti è quasi certamente un elettrodomestico: la")
    print("  zanzara passa, si avvicina e si allontana, e la sua f0 oscilla.\n")

    if ns.scrivi_eventi:
        p = MD.percorso_notte(ns.scrivi_eventi)
        if not os.path.isfile(p):
            print(f"  ! notte inesistente: {p}", file=sys.stderr)
            return 1
        meta = MD.carica(p)
        for e in tutti:
            meta["annotazione"]["eventi"].append({
                "file": e["file"], "inizio_s": e["inizio_s"],
                "fine_s": e["fine_s"], "etichetta": "candidato_zanzara",
                "f0_hz": e["f0_hz"], "n_armoniche": e["n_armoniche"],
                "snr_db": e["snr_medio_db"], "confidenza": "da_confermare",
                "fonte": "spettro.py/firma",
            })
        MD.salva(meta, p)
        print(f"  Scritti {len(tutti)} candidati in {p}")
        print("  Restano etichettati 'da_confermare': l'ascolto è tuo.\n")

    _scrivi_uscite(ns, {"tipo": "firma", "parametri": vars(ns), "eventi": tutti},
                   tutti)
    return 0


# ==========================================================================
# Comando: ventola
# ==========================================================================

def comando_ventola(ns) -> int:
    """Quantifica l'autocontaminazione della ventola dell'Unità B (§10)."""
    def spettro_mediano(percorso):
        ris = analizza_file(percorso, ns.inizio, ns.durata, ns.nfft, None,
                            ns.max_frame)
        if ris is None or not ris.potenze:
            raise SystemExit(f"File troppo corto o illeggibile: {percorso}")
        st = DSP.statistiche_per_bin(ris, quantili=(0.5,))
        return ris.frequenze, st["quantili"][0.5], st["n_frame"]

    freq, s_on, n_on = spettro_mediano(ns.con)
    _, s_off, n_off = spettro_mediano(ns.senza)

    print()
    print("=" * 76)
    print("  AUTOCONTAMINAZIONE DELLA VENTOLA — delta ON/OFF in dB")
    print("=" * 76)
    print(f"  ventola ON  : {os.path.basename(ns.con)}  ({n_on} frame)")
    print(f"  ventola OFF : {os.path.basename(ns.senza)}  ({n_off} frame)")
    print()
    print(f"  {'banda':<44}{'OFF':>8}{'ON':>8}{'delta':>8}")
    print("  " + "-" * 68)
    righe = []
    for etichetta, f0, f1 in SOTTOBANDE:
        p_on = DSP.db(DSP.potenza_banda(s_on, freq, f0, f1))
        p_off = DSP.db(DSP.potenza_banda(s_off, freq, f0, f1))
        print(f"  {etichetta:<44}{p_off:>8.1f}{p_on:>8.1f}{p_on-p_off:>8.1f}")
        righe.append({"banda": etichetta, "off_db": round(p_off, 2),
                      "on_db": round(p_on, 2), "delta_db": round(p_on - p_off, 2)})

    z_on = DSP.db(DSP.potenza_banda(s_on, freq, *BANDA_ZANZARA))
    z_off = DSP.db(DSP.potenza_banda(s_off, freq, *BANDA_ZANZARA))
    delta = z_on - z_off
    print("  " + "-" * 68)
    print(f"  {'BANDA ZANZARA 400-600 Hz':<44}{z_off:>8.1f}{z_on:>8.1f}{delta:>8.1f}")
    print()
    print("  Componenti tonali introdotte dalla ventola:")
    for f, prom, liv in picchi_tonali(freq, s_on, soglia_db=ns.soglia_tonale):
        dentro = "  *** IN BANDA ZANZARA ***" if BANDA_ZANZARA[0] <= f <= BANDA_ZANZARA[1] else ""
        print(f"    {f:7.1f} Hz   prominenza {prom:5.1f} dB{dentro}")

    print()
    print("  LETTURA DEL RISULTATO (soglie proposte, da validare con il")
    print("  chief-engineer e con payload-fluidics):")
    if delta < 3:
        esito = "trascurabile"
        print("    delta < 3 dB  -> ascolto e aspirazione possono convivere.")
    elif delta < 10:
        esito = "marginale"
        print("    3-10 dB       -> convivenza possibile ma la sensibilità cala:")
        print("                     serve rimisurare la recall con ventola accesa.")
    else:
        esito = "bloccante"
        print("    > 10 dB       -> la ventola COPRE la zanzara. Serve un ciclo")
        print("                     alternato ascolto/aspirazione. È un vincolo di")
        print("                     sistema: va concordato con payload-fluidics e")
        print("                     registrato nel Decision Log §3 prima di")
        print("                     congelare il montante.")
    print("=" * 76)
    print()

    _scrivi_uscite(ns, {"tipo": "ventola", "con": ns.con, "senza": ns.senza,
                        "bande": righe, "delta_banda_zanzara_db": round(delta, 2),
                        "esito": esito}, righe)
    return 0


# ==========================================================================
# Comando: spettrogramma
# ==========================================================================

SCALA = " .:-=+*#%@"


def comando_spettrogramma(ns) -> int:
    ris = analizza_file(ns.file[0], ns.inizio, ns.durata, ns.nfft, None,
                        ns.max_frame)
    if ris is None or not ris.potenze:
        print("File troppo corto.")
        return 1
    i0, i1 = DSP.indice_banda(ris.frequenze, ns.f_min_vista, ns.f_max_vista)
    n_col = min(ns.colonne, len(ris.potenze))
    passo = max(1, len(ris.potenze) // n_col)
    colonne = list(range(0, len(ris.potenze), passo))[:n_col]

    valori = []
    for b in range(i0, i1):
        riga = [DSP.db(float(ris.potenze[c][b])) for c in colonne]
        valori.append(riga)
    piatti = [v for r in valori for v in r]
    lo = sorted(piatti)[int(0.10 * (len(piatti) - 1))]
    hi = sorted(piatti)[int(0.999 * (len(piatti) - 1))]
    span = max(1e-6, hi - lo)

    print()
    print(f"  Spettrogramma  {os.path.basename(ns.file[0])}   "
          f"{ns.f_min_vista:.0f}-{ns.f_max_vista:.0f} Hz   "
          f"scala {lo:.0f}..{hi:.0f} dBFS   '{SCALA}'")
    print()
    for b in range(i1 - i0 - 1, -1, -1):
        f = ris.frequenze[i0 + b]
        etichetta = f"{f:6.0f} |" if (i0 + b) % 4 == 0 else "       |"
        riga = "".join(
            SCALA[min(len(SCALA) - 1, max(0, int((v - lo) / span * (len(SCALA) - 1))))]
            for v in valori[b])
        marca = " <" if BANDA_ZANZARA[0] <= f <= BANDA_ZANZARA[1] else ""
        print(etichetta + riga + marca)
    t0 = ris.tempi[colonne[0]]
    t1 = ris.tempi[colonne[-1]]
    print("       +" + "-" * len(colonne))
    print(f"        {t0:.1f} s" + " " * max(0, len(colonne) - 16) + f"{t1:.1f} s")
    print("\n  ('<' = banda 400-600 Hz del battito alare)\n")
    return 0


# ==========================================================================
# Uscite
# ==========================================================================

def _scrivi_uscite(ns, referto: dict, righe_csv) -> None:
    if getattr(ns, "json", None):
        with open(ns.json, "w", encoding="utf-8") as f:
            json.dump(referto, f, ensure_ascii=False, indent=2, default=str)
            f.write("\n")
        print(f"  referto JSON -> {ns.json}")
    if getattr(ns, "csv", None) and righe_csv:
        campi = sorted({k for r in righe_csv for k in r.keys()})
        with open(ns.csv, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campi, extrasaction="ignore")
            w.writeheader()
            for r in righe_csv:
                w.writerow({k: (json.dumps(v, ensure_ascii=False)
                                if isinstance(v, (list, dict)) else v)
                            for k, v in r.items()})
        print(f"  referto CSV  -> {ns.csv}")


# ==========================================================================
# main
# ==========================================================================

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="spettro.py",
        description="Analisi spettrale 300-800 Hz per il dataset zanzare.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def comuni(p, con_file=True):
        if con_file:
            p.add_argument("file", nargs="+", help="file WAV/FLAC o cartelle")
        p.add_argument("--inizio", type=float, default=0.0, help="offset in s")
        p.add_argument("--durata", type=float, default=None, help="durata in s")
        p.add_argument("--nfft", type=int, default=NFFT)
        p.add_argument("--max-frame", type=int, default=4000,
                       help="tetto ai frame per file (protegge il fallback "
                            "senza numpy dai tempi biblici)")
        p.add_argument("--json", default=None, help="scrive il referto in JSON")
        p.add_argument("--csv", default=None, help="scrive le righe in CSV")

    r = sub.add_parser("rumore", help="caratterizza il rumore di fondo")
    comuni(r)
    r.add_argument("--passo-s", type=float, default=1.0,
                   help="un frame ogni N secondi (default 1,0)")
    r.add_argument("--soglia-tonale", type=float, default=6.0,
                   help="prominenza minima in dB per dichiarare un tono")

    f = sub.add_parser("firma", help="cerca la firma del battito alare")
    comuni(f)
    f.add_argument("--f-min", type=float, default=BANDA_ZANZARA[0])
    f.add_argument("--f-max", type=float, default=BANDA_ZANZARA[1])
    f.add_argument("--snr", type=float, default=10.0,
                   help="SNR minimo della fondamentale sul pavimento, dB")
    f.add_argument("--snr-armoniche", type=float, default=6.0)
    f.add_argument("--tolleranza-armonica", type=float, default=0.04,
                   help="tolleranza relativa nella ricerca di k*f0 (default 4%%)")
    f.add_argument("--min-armoniche", type=int, default=1,
                   help="armoniche richieste per accettare un frame")
    f.add_argument("--durata-min", type=float, default=0.3,
                   help="durata minima di un evento, s")
    f.add_argument("--buco-max", type=int, default=2,
                   help="frame mancanti tollerati dentro un evento")
    f.add_argument("--scrivi-eventi", default=None, metavar="ID_NOTTE",
                   help="aggiunge i candidati ai metadati della notte")

    v = sub.add_parser("ventola", help="delta ON/OFF della ventola in banda utile")
    comuni(v, con_file=False)
    v.add_argument("--con", required=True, help="registrazione con ventola accesa")
    v.add_argument("--senza", required=True, help="registrazione con ventola spenta")
    v.add_argument("--soglia-tonale", type=float, default=6.0)

    s = sub.add_parser("spettrogramma", help="rendering ASCII della banda utile")
    comuni(s)
    s.add_argument("--colonne", type=int, default=110)
    s.add_argument("--f-min-vista", type=float, default=BANDA_UTILE[0])
    s.add_argument("--f-max-vista", type=float, default=BANDA_UTILE[1])

    ns = ap.parse_args(argv)
    if not DSP.ffmpeg_path():
        print("Nota: ffmpeg assente. Funzionerà solo su WAV PCM, con "
              "decimazione approssimativa.", file=sys.stderr)
    if not DSP.numpy_attivo():
        print("Nota: numpy assente, si usa la FFT in Python puro (funziona, "
              "ma è lenta). `pip install numpy` la accelera di ~30x.\n",
              file=sys.stderr)

    return {"rumore": comando_rumore, "firma": comando_firma,
            "ventola": comando_ventola,
            "spettrogramma": comando_spettrogramma}[ns.cmd](ns)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
