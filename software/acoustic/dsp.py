#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dsp.py — primitive di analisi spettrale per R2-Sentinel, Unità B (acustica).

Obiettivo di progetto: girare **oggi**, su un portatile, senza installare nulla.
Quindi tutto è implementato in libreria standard Python 3.8+.
Se `numpy` è presente viene usato automaticamente (10-50x più veloce), ma non è
richiesto: il fallback in Python puro produce gli stessi numeri.

Decodifica audio: delegata a `ffmpeg`, che è già una dipendenza del registratore.
Questo dà gratis il ricampionamento con filtro anti-alias corretto (indispensabile
per scendere da 48 kHz alla banda utile) e la lettura sia di WAV sia di FLAC.
Se ffmpeg manca, c'è un fallback su `wave` + decimazione FIR, solo per WAV PCM.

Convenzione dei livelli: i campioni sono normalizzati in [-1, 1) e tutti i dB
sono **dBFS** (relativi al fondo scala del convertitore), NON dB SPL.
La conversione in SPL assoluti richiede un riferimento acustico calibrato, che
alla data non è in BOM (§10 del PROJECT.md, voce "strumenti di misura").
Non inventare SPL da questi numeri: servono per confronti relativi e per il
delta ventola on/off, che è quello che i criteri di FATTO chiedono davvero.
"""

from __future__ import annotations

import cmath
import math
import os
import shutil
import subprocess
import sys
import wave
from array import array

try:  # accelerazione opzionale
    import numpy as _np
except Exception:  # pragma: no cover
    _np = None


# --------------------------------------------------------------------------
# Utilità generali
# --------------------------------------------------------------------------

def numpy_attivo() -> bool:
    return _np is not None


def ffmpeg_path() -> str | None:
    return shutil.which("ffmpeg")


def ffprobe_path() -> str | None:
    return shutil.which("ffprobe")


def db(x: float, minimo_db: float = -200.0) -> float:
    """Potenza lineare -> dB, con pavimento per evitare log(0)."""
    if x <= 0:
        return minimo_db
    v = 10.0 * math.log10(x)
    return v if v > minimo_db else minimo_db


def prossima_pot2(n: int) -> int:
    p = 1
    while p < n:
        p <<= 1
    return p


# --------------------------------------------------------------------------
# FFT radix-2 iterativa (fallback senza numpy)
# --------------------------------------------------------------------------

_TWIDDLE_CACHE: dict[int, list[complex]] = {}


def _twiddles(n: int) -> list[complex]:
    tw = _TWIDDLE_CACHE.get(n)
    if tw is None:
        tw = [cmath.exp(-2j * math.pi * k / n) for k in range(n // 2)]
        _TWIDDLE_CACHE[n] = tw
    return tw


def fft(x) -> list[complex]:
    """FFT complessa, lunghezza potenza di 2. Cooley-Tukey decimation-in-time."""
    n = len(x)
    if n == 0 or (n & (n - 1)) != 0:
        raise ValueError("la lunghezza della FFT deve essere una potenza di 2")
    a = [complex(v) for v in x]

    # permutazione bit-reverse
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    tw = _twiddles(n)
    lunghezza = 2
    while lunghezza <= n:
        passo = n // lunghezza
        meta = lunghezza >> 1
        for i in range(0, n, lunghezza):
            k = 0
            for m in range(i, i + meta):
                u = a[m]
                v = a[m + meta] * tw[k]
                a[m] = u + v
                a[m + meta] = u - v
                k += passo
        lunghezza <<= 1
    return a


_HANN_CACHE: dict[int, list[float]] = {}


def hann(n: int) -> list[float]:
    w = _HANN_CACHE.get(n)
    if w is None:
        if n == 1:
            w = [1.0]
        else:
            w = [0.5 - 0.5 * math.cos(2.0 * math.pi * i / (n - 1)) for i in range(n)]
        _HANN_CACHE[n] = w
    return w


# --------------------------------------------------------------------------
# Lettura audio
# --------------------------------------------------------------------------

class ErroreAudio(RuntimeError):
    pass


def durata_file_s(percorso: str) -> float | None:
    """Durata in secondi. Per il WAV PCM si calcola esattamente dall'header,
    senza decodificare: è il motivo per cui il registratore scrive WAV."""
    if percorso.lower().endswith(".wav"):
        try:
            with wave.open(percorso, "rb") as w:
                return w.getnframes() / float(w.getframerate())
        except Exception:
            pass
    fp = ffprobe_path()
    if fp:
        try:
            out = subprocess.run(
                [fp, "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=nw=1:nk=1", percorso],
                capture_output=True, text=True, timeout=60,
            )
            v = out.stdout.strip()
            if v and v != "N/A":
                return float(v)
        except Exception:
            pass
    return None


def _leggi_con_ffmpeg(percorso: str, fs_target: int, inizio_s: float,
                      durata_s: float | None):
    exe = ffmpeg_path()
    if not exe:
        raise ErroreAudio("ffmpeg non trovato")
    cmd = [exe, "-v", "error", "-nostdin"]
    if inizio_s > 0:
        cmd += ["-ss", f"{inizio_s:.6f}"]
    cmd += ["-i", percorso]
    if durata_s is not None:
        cmd += ["-t", f"{durata_s:.6f}"]
    cmd += ["-map", "0:a:0", "-ac", "1", "-ar", str(fs_target),
            "-f", "s16le", "-acodec", "pcm_s16le", "-"]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        raise ErroreAudio(
            f"ffmpeg ha fallito su {percorso}: "
            f"{proc.stderr.decode('utf-8', 'replace')[:400]}"
        )
    grezzi = array("h")
    grezzi.frombytes(proc.stdout)
    if sys.byteorder == "big":
        grezzi.byteswap()
    return grezzi


def _leggi_con_wave(percorso: str, fs_target: int, inizio_s: float,
                    durata_s: float | None):
    """Fallback senza ffmpeg: solo WAV PCM 16 bit, decimazione a media mobile.
    L'anti-alias è mediocre rispetto a ffmpeg; usare solo in emergenza."""
    with wave.open(percorso, "rb") as w:
        if w.getsampwidth() != 2:
            raise ErroreAudio("fallback wave: supportato solo PCM 16 bit")
        fs = w.getframerate()
        canali = w.getnchannels()
        n_tot = w.getnframes()
        i0 = min(int(inizio_s * fs), n_tot)
        n_leggi = n_tot - i0 if durata_s is None else min(int(durata_s * fs), n_tot - i0)
        w.setpos(i0)
        crudo = array("h")
        crudo.frombytes(w.readframes(max(0, n_leggi)))
    if sys.byteorder == "big":
        crudo.byteswap()
    if canali > 1:
        crudo = array("h", crudo[0::canali])
    fattore = max(1, int(round(fs / float(fs_target))))
    if fattore == 1:
        return crudo
    fuori = array("h")
    acc = 0
    for i, v in enumerate(crudo):
        acc += v
        if (i + 1) % fattore == 0:
            fuori.append(int(acc / fattore))
            acc = 0
    return fuori


def leggi_audio(percorso: str, fs_target: int = 6000, inizio_s: float = 0.0,
                durata_s: float | None = None):
    """Restituisce (campioni_float_normalizzati, fs effettivo).

    fs_target di default 6000 Hz: Nyquist 3000 Hz, che copre la fondamentale
    400-600 Hz e almeno la 2a e 3a armonica anche nel caso peggiore (600 Hz
    -> 1200 e 1800 Hz). Scendere sotto perderebbe le armoniche, che il criterio
    di FATTO della fase 5 richiede esplicitamente.
    """
    if not os.path.isfile(percorso):
        raise ErroreAudio(f"file inesistente: {percorso}")
    try:
        grezzi = _leggi_con_ffmpeg(percorso, fs_target, inizio_s, durata_s)
    except ErroreAudio:
        if not percorso.lower().endswith(".wav"):
            raise
        grezzi = _leggi_con_wave(percorso, fs_target, inizio_s, durata_s)
    if _np is not None:
        camp = _np.frombuffer(grezzi.tobytes(), dtype="<i2").astype("float64") / 32768.0
    else:
        camp = [v / 32768.0 for v in grezzi]
    return camp, fs_target


# --------------------------------------------------------------------------
# Spettri
# --------------------------------------------------------------------------

class RisultatoSpettro:
    """Contenitore dei frame spettrali di un segmento.

    - frequenze: centro di ogni bin, Hz
    - potenze: lista di frame; ogni frame è la PSD (potenza lineare, dBFS^2)
    - tempi: istante centrale di ogni frame, s dall'inizio della porzione letta
    """

    __slots__ = ("frequenze", "potenze", "tempi", "fs", "nfft", "risoluzione_hz")

    def __init__(self, frequenze, potenze, tempi, fs, nfft):
        self.frequenze = frequenze
        self.potenze = potenze
        self.tempi = tempi
        self.fs = fs
        self.nfft = nfft
        self.risoluzione_hz = fs / float(nfft)

    def __len__(self):
        return len(self.potenze)


def analizza(campioni, fs: int, nfft: int = 2048, sovrapposizione: float = 0.5,
             passo_s: float | None = None, max_frame: int = 4000) -> RisultatoSpettro:
    """Spettro a finestra scorrevole (Hann, normalizzata in ampiezza).

    nfft 2048 @ 6000 Hz = finestra 341 ms, risoluzione 2,93 Hz.
    Il criterio di FATTO chiede la fondamentale entro ±15 Hz: 2,93 Hz di bin,
    più l'interpolazione parabolica del picco, danno margine abbondante.
    Finestre più lunghe risolverebbero meglio in frequenza ma spalmerebbero
    nel tempo i passaggi brevi della zanzara, che durano frazioni di secondo.
    """
    n = len(campioni)
    if n < nfft:
        return RisultatoSpettro([], [], [], fs, nfft)

    if passo_s is not None:
        salto = max(1, int(round(passo_s * fs)))
    else:
        salto = max(1, int(nfft * (1.0 - sovrapposizione)))

    n_frame_teorici = 1 + (n - nfft) // salto
    if n_frame_teorici > max_frame:
        salto = max(salto, (n - nfft) // max(1, max_frame - 1))
        n_frame_teorici = 1 + (n - nfft) // salto

    w = hann(nfft)
    # normalizzazione per finestra: preserva la potenza del segnale
    norm = 1.0 / (sum(v * v for v in w) or 1.0)

    frequenze = [i * fs / float(nfft) for i in range(nfft // 2 + 1)]
    potenze = []
    tempi = []

    if _np is not None:
        arr = _np.asarray(campioni, dtype="float64")
        wn = _np.asarray(w, dtype="float64")
        for k in range(n_frame_teorici):
            i0 = k * salto
            blocco = arr[i0:i0 + nfft]
            if blocco.shape[0] < nfft:
                break
            spettro = _np.fft.rfft(blocco * wn)
            p = (spettro.real ** 2 + spettro.imag ** 2) * norm
            potenze.append(p)
            tempi.append((i0 + nfft / 2.0) / fs)
    else:
        for k in range(n_frame_teorici):
            i0 = k * salto
            blocco = campioni[i0:i0 + nfft]
            if len(blocco) < nfft:
                break
            fin = [blocco[i] * w[i] for i in range(nfft)]
            spet = fft(fin)
            p = [(spet[i].real ** 2 + spet[i].imag ** 2) * norm
                 for i in range(nfft // 2 + 1)]
            potenze.append(p)
            tempi.append((i0 + nfft / 2.0) / fs)

    return RisultatoSpettro(frequenze, potenze, tempi, fs, nfft)


def _percentile_lista(valori_ordinati, q: float) -> float:
    if not valori_ordinati:
        return 0.0
    if q <= 0:
        return valori_ordinati[0]
    if q >= 1:
        return valori_ordinati[-1]
    pos = q * (len(valori_ordinati) - 1)
    lo = int(math.floor(pos))
    hi = min(lo + 1, len(valori_ordinati) - 1)
    frazione = pos - lo
    return valori_ordinati[lo] * (1 - frazione) + valori_ordinati[hi] * frazione


def statistiche_per_bin(ris: RisultatoSpettro, quantili=(0.5, 0.95)) -> dict:
    """Per ogni bin di frequenza: percentili sulla durata analizzata.

    La MEDIANA è il rumore di fondo della stanza: gli eventi rari (una zanzara
    che passa, uno scricchiolio) non la spostano. Il p95 mostra invece l'attività.
    La differenza p95-mediana è l'indicatore di quanto "vive" quella banda.
    """
    if not ris.potenze:
        return {"quantili": {}, "n_frame": 0}
    n_bin = len(ris.frequenze)
    fuori = {q: [0.0] * n_bin for q in quantili}
    if _np is not None:
        m = _np.vstack(ris.potenze)
        for q in quantili:
            fuori[q] = list(_np.quantile(m, q, axis=0))
    else:
        for b in range(n_bin):
            colonna = sorted(frame[b] for frame in ris.potenze)
            for q in quantili:
                fuori[q][b] = _percentile_lista(colonna, q)
    return {"quantili": fuori, "n_frame": len(ris.potenze)}


def indice_banda(frequenze, f_min: float, f_max: float):
    i0 = 0
    while i0 < len(frequenze) and frequenze[i0] < f_min:
        i0 += 1
    i1 = i0
    while i1 < len(frequenze) and frequenze[i1] <= f_max:
        i1 += 1
    return i0, max(i1, i0 + 1)


def potenza_banda(potenze_frame, frequenze, f_min: float, f_max: float) -> float:
    i0, i1 = indice_banda(frequenze, f_min, f_max)
    if _np is not None and not isinstance(potenze_frame, list):
        return float(potenze_frame[i0:i1].sum())
    return float(sum(potenze_frame[i0:i1]))


def picco_interpolato(potenze_frame, frequenze, f_min: float, f_max: float):
    """Picco nella banda, con interpolazione parabolica in dominio log.

    Restituisce (frequenza_hz, potenza_lineare, indice_bin) oppure None.
    L'interpolazione è ciò che porta l'incertezza della fondamentale sotto la
    risoluzione del bin: senza, con bin da 2,93 Hz l'errore massimo sarebbe
    ±1,5 Hz già di per sé accettabile, ma su picchi larghi il centroide conta.
    """
    i0, i1 = indice_banda(frequenze, f_min, f_max)
    if i1 - i0 < 1:
        return None
    migliore = i0
    valore = potenze_frame[i0]
    for i in range(i0 + 1, i1):
        if potenze_frame[i] > valore:
            valore = potenze_frame[i]
            migliore = i
    if valore <= 0:
        return None
    df = frequenze[1] - frequenze[0] if len(frequenze) > 1 else 1.0
    f = frequenze[migliore]
    if 0 < migliore < len(potenze_frame) - 1:
        a = db(float(potenze_frame[migliore - 1]))
        b = db(float(potenze_frame[migliore]))
        c = db(float(potenze_frame[migliore + 1]))
        den = (a - 2 * b + c)
        if abs(den) > 1e-12:
            delta = 0.5 * (a - c) / den
            if -1.0 < delta < 1.0:
                f = frequenze[migliore] + delta * df
    return f, float(valore), migliore


def mediana(valori):
    v = sorted(valori)
    if not v:
        return 0.0
    n = len(v)
    return v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2])


# --------------------------------------------------------------------------
# Livello di un file (usato dal watchdog del registratore)
# --------------------------------------------------------------------------

def livello_wav(percorso: str, max_secondi: float = 5.0):
    """(rms_dbfs, picco_dbfs, n_campioni) leggendo solo l'inizio del file.

    Volutamente basato su `wave` puro: deve funzionare anche se ffmpeg si è
    piantato, perché serve proprio a scoprire che la notte sta andando persa.
    """
    with wave.open(percorso, "rb") as w:
        if w.getsampwidth() != 2:
            raise ErroreAudio("atteso PCM 16 bit")
        fs = w.getframerate()
        canali = w.getnchannels()
        n = min(w.getnframes(), int(max_secondi * fs))
        dati = array("h")
        dati.frombytes(w.readframes(n))
    if sys.byteorder == "big":
        dati.byteswap()
    if canali > 1:
        dati = array("h", dati[0::canali])
    if not dati:
        return -200.0, -200.0, 0
    somma = 0.0
    picco = 0
    for v in dati:
        somma += float(v) * v
        av = -v if v < 0 else v
        if av > picco:
            picco = av
    rms = math.sqrt(somma / len(dati)) / 32768.0
    pk = picco / 32768.0
    return (20 * math.log10(rms) if rms > 0 else -200.0,
            20 * math.log10(pk) if pk > 0 else -200.0,
            len(dati))
