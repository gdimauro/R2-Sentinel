#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
registratore.py — banco di registrazione notturna, R2-Sentinel Unità B.

UNA NOTTE PERSA È IRRECUPERABILE. Alla data di scrittura (agosto 2026) la
finestra stagionale delle zanzare in Italia si chiude a settembre/ottobre:
ogni notte non registrata sposta la fase 5 di un anno, non di una settimana.
Tutto in questo file è progettato attorno a quel fatto.

Come è costruito, e perché
--------------------------
* **ffmpeg fa la cattura, Python fa il supervisore.** Il muxer `segment` di
  ffmpeg taglia un flusso di ingresso *continuo*: fra un segmento e il
  successivo non si perde un campione, perché il dispositivo non viene mai
  richiuso. Un anello circolare scritto in Python su PortAudio avrebbe dovuto
  guadagnarsi la stessa proprietà, e sarebbe stato l'unico punto in cui un
  glitch del GIL alle 3 di notte costa una notte.
* **Nessuna dipendenza da installare.** Solo Python 3 di sistema e ffmpeg.
  Niente numpy, niente sounddevice, niente pip. È la ragione per cui si può
  partire stasera e non fra tre giorni.
* **WAV PCM 16 bit, non FLAC.** Il WAV è leggibile dalla libreria standard, la
  durata si ricava esattamente dall'header senza decodificare, e nessun
  encoder può incepparsi a metà notte. Costo: ~2,1 GB per 6 h. La compressione
  in FLAC si fa la mattina dopo (`--comprimi`), quando un errore non costa
  nulla. Verificato in prova: la segmentazione FLAC lascia lo STREAMINFO senza
  numero totale di campioni, cioè durate non affidabili dall'header — un
  motivo in più per non usarla in acquisizione.
* **Il processo si rialza da solo.** Se ffmpeg muore, il supervisore lo
  riavvia entro pochi secondi e ricalcola la durata residua fino all'orario di
  fine. L'interruzione viene registrata come `gap` nei metadati, non nascosta.
* **Watchdog di livello.** Ogni N minuti misura RMS e picco di un segmento
  chiuso. Una notte registrata con il microfono muto o scollegato è persa
  esattamente come una notte non registrata, ma te ne accorgi solo dopo. Qui
  te ne accorgi subito, e in più la serie dei livelli È la caratterizzazione
  del rumore di fondo della stanza.
* **macOS non deve addormentarsi.** Il processo gira sotto `caffeinate -i -m -s`.
  Attenzione: `caffeinate` NON impedisce lo sleep alla chiusura del coperchio.

Vincoli di progetto rispettati qui
----------------------------------
* Privacy (CONTRIBUTING.md): l'audio viene scritto **fuori dal repository**
  (default `~/r2-sentinel-audio`). Il registratore rifiuta di scrivere dentro
  la working copy Git a meno di `--consenti-audio-nel-repo`, perché la history
  di Git non si cancella davvero.
* D-07 (LiFePO4): se questo banco viene reso autonomo e lasciato acceso di
  notte incustodito, l'alimentazione ammessa è LiFePO4. I power bank USB da
  supermercato sono Li-ion NMC e sono **esclusi**. Con il portatile collegato
  alla rete il vincolo non si applica.

Uso minimo:
    python3 registratore.py --prova            # 60 s, verifica la catena
    python3 registratore.py --stanza camera --ore 8
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time

QUI = os.path.dirname(os.path.abspath(__file__))
if QUI not in sys.path:
    sys.path.insert(0, QUI)

import metadati as MD  # noqa: E402
import dsp as DSP      # noqa: E402


FS_RICHIESTO = 48000
BYTE_PER_CAMPIONE = 2
MARGINE_DISCO_BYTE = 2 * 1024 ** 3     # 2 GB di riserva oltre al necessario
SOGLIA_STOP_DISCO_BYTE = 1024 ** 3     # sotto 1 GB liberi si chiude pulito
DIR_AUDIO_DEFAULT = os.path.expanduser("~/r2-sentinel-audio")

_RE_SEGMENTO = re.compile(r"Opening '(?P<f>[^']+)' for writing")


def _ora() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _log(msg: str) -> None:
    print(f"[{_dt.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


# ==========================================================================
# Dispositivi di ingresso
# ==========================================================================

def backend_predefinito() -> str:
    if sys.platform == "darwin":
        return "avfoundation"
    if shutil.which("pactl") or os.path.exists("/run/pulse"):
        return "pulse"
    return "alsa"


def elenca_dispositivi(backend: str) -> None:
    exe = DSP.ffmpeg_path()
    if not exe:
        raise SystemExit("ffmpeg non trovato nel PATH.")
    if backend == "avfoundation":
        print("Dispositivi audio di ingresso (macOS / avfoundation):\n")
        out = subprocess.run([exe, "-hide_banner", "-f", "avfoundation",
                              "-list_devices", "true", "-i", ""],
                             capture_output=True, text=True)
        testo = out.stderr
        dentro = False
        for riga in testo.splitlines():
            if "AVFoundation audio devices" in riga:
                dentro = True
                continue
            if dentro:
                m = re.search(r"\[(\d+)\]\s+(.*)$", riga)
                if not m:
                    break
                print(f"  --dispositivo :{m.group(1)}    {m.group(2)}")
        print("\nEsempio:  --dispositivo :1")
    elif backend == "pulse":
        subprocess.run(["pactl", "list", "short", "sources"])
        print("\nEsempio:  --dispositivo alsa_input.usb-....analog-stereo")
    else:
        if shutil.which("arecord"):
            subprocess.run(["arecord", "-l"])
        print("\nEsempio:  --dispositivo hw:1,0")


def _ingresso_ffmpeg(backend: str, spec: str, forza_rate: bool) -> list[str]:
    """Argomenti di INPUT. Nota: avfoundation NON accetta -ar in ingresso
    (verificato su ffmpeg 8.0.1: 'Option sample_rate not found'), quindi si
    prende il rate nativo del dispositivo e lo si verifica."""
    base = ["-thread_queue_size", "4096", "-f", backend]
    if backend in ("alsa", "pulse") and forza_rate:
        base += ["-ar", str(FS_RICHIESTO), "-ac", "1"]
    return base + ["-i", spec]


def sonda_dispositivo(backend: str, spec: str) -> dict:
    """Apre il dispositivo per ~1 s e ne ricava rate nativo, canali, livello.

    Serve a fallire ORA e non alle 3 di notte: microfono staccato, permesso
    microfono negato a Terminale, indice sbagliato.
    """
    exe = DSP.ffmpeg_path()
    cmd = [exe, "-hide_banner", "-loglevel", "info", "-nostdin"]
    cmd += _ingresso_ffmpeg(backend, spec, forza_rate=False)
    cmd += ["-t", "1.0", "-f", "null", "-"]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    err = out.stderr
    info = {"ok": out.returncode == 0, "stderr": err.strip()[-800:],
            "rate_nativo": None, "canali": None, "nome": None}
    m = re.search(r"Audio:\s*\S+.*?,\s*(\d+)\s*Hz,\s*([a-z0-9.()]+)", err)
    if m:
        info["rate_nativo"] = int(m.group(1))
        canali_txt = m.group(2)
        info["canali"] = 1 if "mono" in canali_txt else (
            2 if "stereo" in canali_txt else None)
    return info


def nome_dispositivo(backend: str, spec: str) -> str | None:
    if backend != "avfoundation":
        return spec
    exe = DSP.ffmpeg_path()
    out = subprocess.run([exe, "-hide_banner", "-f", "avfoundation",
                          "-list_devices", "true", "-i", ""],
                         capture_output=True, text=True)
    idx = spec.lstrip(":").strip()
    dentro = False
    for riga in out.stderr.splitlines():
        if "AVFoundation audio devices" in riga:
            dentro = True
            continue
        if dentro:
            m = re.search(r"\[(\d+)\]\s+(.*)$", riga)
            if not m:
                break
            if m.group(1) == idx:
                return m.group(2).strip()
    return None


# ==========================================================================
# Sessione di registrazione
# ==========================================================================

class Sessione:
    def __init__(self, ns: argparse.Namespace):
        self.ns = ns
        self.ferma = threading.Event()
        self.proc: subprocess.Popen | None = None
        self.proc_lock = threading.Lock()
        self.segmenti_visti: list[tuple[str, str]] = []   # (iso, percorso)
        self.eventi: list[dict] = []
        self.livelli: list[dict] = []
        self.n_riavvii = 0
        self.motivo_fine = "completata"

    # ---------------------------------------------------------------- eventi
    def evento(self, tipo: str, **kw) -> None:
        e = {"t": _ora(), "tipo": tipo}
        e.update(kw)
        self.eventi.append(e)
        if tipo not in ("segmento_aperto",):
            _log(f"{tipo}: " + " ".join(f"{k}={v}" for k, v in kw.items()))

    # ------------------------------------------------------------- comando
    def comando_ffmpeg(self, durata_s: float, dir_audio: str, prefisso: str) -> list[str]:
        exe = DSP.ffmpeg_path()
        cmd = [exe, "-hide_banner", "-loglevel", "info", "-nostats"]
        cmd += _ingresso_ffmpeg(self.ns.backend, self.ns.dispositivo,
                                forza_rate=True)
        cmd += ["-t", f"{durata_s:.3f}", "-map", "0:a:0", "-ac", "1"]
        if self.ricampiona:
            cmd += ["-ar", str(FS_RICHIESTO)]
        modello = os.path.join(dir_audio, prefisso + "_%Y%m%dT%H%M%S.wav")
        cmd += ["-c:a", "pcm_s16le",
                "-f", "segment",
                "-segment_time", str(int(self.ns.segmento_s)),
                "-reset_timestamps", "1",
                "-segment_format", "wav",
                "-strftime", "1",
                modello]
        if sys.platform == "darwin" and shutil.which("caffeinate") \
                and not self.ns.no_caffeinate:
            # -i no idle sleep, -m no disk sleep, -s no system sleep su rete
            cmd = ["caffeinate", "-i", "-m", "-s"] + cmd
        return cmd

    # -------------------------------------------------------- lettore stderr
    def _leggi_stderr(self, proc: subprocess.Popen) -> None:
        for riga_b in iter(proc.stderr.readline, b""):
            riga = riga_b.decode("utf-8", "replace").rstrip()
            if not riga:
                continue
            m = _RE_SEGMENTO.search(riga)
            if m:
                self.segmenti_visti.append((_ora(), m.group("f")))
                continue
            basso = riga.lower()
            if any(k in basso for k in ("error", "invalid", "failed",
                                        "cannot", "overrun", "drop")):
                self.evento("ffmpeg_msg", testo=riga[:300])

    # ------------------------------------------------------------- watchdog
    def _watchdog(self, dir_audio: str) -> None:
        intervallo = max(30, int(self.ns.intervallo_controllo))
        bassi_consecutivi = 0
        while not self.ferma.wait(intervallo):
            try:
                file_wav = sorted(
                    f for f in os.listdir(dir_audio) if f.endswith(".wav"))
                if len(file_wav) < 2:
                    continue
                # il penultimo è sicuramente chiuso; l'ultimo è in scrittura
                candidato = os.path.join(dir_audio, file_wav[-2])
                rms, picco, n = DSP.livello_wav(candidato, max_secondi=5.0)
                self.livelli.append({"t": _ora(), "file": file_wav[-2],
                                     "rms_dbfs": round(rms, 1),
                                     "picco_dbfs": round(picco, 1)})
                _log(f"livello  RMS {rms:6.1f} dBFS   picco {picco:6.1f} dBFS "
                     f"   segmenti {len(file_wav)}")
                if rms < self.ns.soglia_silenzio_dbfs:
                    bassi_consecutivi += 1
                    if bassi_consecutivi == 2:
                        self.evento("ALLARME_SILENZIO", rms_dbfs=round(rms, 1),
                                    nota="microfono muto/scollegato? la notte "
                                         "sta andando persa")
                else:
                    bassi_consecutivi = 0
                if picco > -0.5:
                    self.evento("avviso_clipping", picco_dbfs=round(picco, 1))

                libero = shutil.disk_usage(dir_audio).free
                if libero < SOGLIA_STOP_DISCO_BYTE:
                    self.motivo_fine = "disco_pieno"
                    self.evento("STOP_DISCO", liberi_mb=int(libero / 1024 ** 2))
                    self.ferma.set()
                    self._chiudi_ffmpeg()
            except Exception as exc:                     # mai far cadere la notte
                self.evento("watchdog_errore", errore=repr(exc)[:200])

    # ---------------------------------------------------------------- stop
    def _chiudi_ffmpeg(self) -> None:
        with self.proc_lock:
            p = self.proc
        if p is None or p.poll() is not None:
            return
        try:
            p.stdin.write(b"q")     # 'q' = uscita pulita, scrive i trailer WAV
            p.stdin.flush()
        except Exception:
            pass
        try:
            p.wait(timeout=15)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            except Exception:
                p.terminate()

    # ------------------------------------------------------------- ciclo
    def esegui(self, dir_audio: str, prefisso: str, durata_totale_s: float) -> None:
        t_fine = time.time() + durata_totale_s
        wd = threading.Thread(target=self._watchdog, args=(dir_audio,),
                              daemon=True)
        wd.start()

        backoff = 2.0
        while not self.ferma.is_set():
            restante = t_fine - time.time()
            if restante < 30:
                break
            cmd = self.comando_ffmpeg(restante, dir_audio, prefisso)
            self.evento("avvio_ffmpeg", restante_s=int(restante),
                        tentativo=self.n_riavvii + 1)
            t0 = time.time()
            try:
                with self.proc_lock:
                    self.proc = subprocess.Popen(
                        cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                        stderr=subprocess.PIPE, start_new_session=True)
                    p = self.proc
                th = threading.Thread(target=self._leggi_stderr, args=(p,),
                                      daemon=True)
                th.start()
                rc = p.wait()
                th.join(timeout=5)
            except Exception as exc:
                self.evento("errore_avvio", errore=repr(exc)[:300])
                rc = -999

            durata_run = time.time() - t0
            if self.ferma.is_set():
                break
            if time.time() >= t_fine - 30:
                self.evento("fine_regolare", rc=rc, durata_run_s=int(durata_run))
                break

            # uscita prematura: si riparte
            self.n_riavvii += 1
            self.evento("INTERRUZIONE", rc=rc, durata_run_s=int(durata_run),
                        riavvio_fra_s=backoff)
            if durata_run < 5:
                backoff = min(backoff * 2, 60.0)   # guasto persistente
            else:
                backoff = 2.0
            if self.n_riavvii > 200:
                self.motivo_fine = "troppi_riavvii"
                self.evento("RESA", nota="oltre 200 riavvii, si interrompe")
                break
            if self.ferma.wait(backoff):
                break

        self.ferma.set()
        self._chiudi_ffmpeg()


# ==========================================================================
# Inventario e chiusura
# ==========================================================================

def inventario(dir_audio: str, prefisso: str) -> dict:
    file_ord = sorted(f for f in os.listdir(dir_audio)
                      if f.startswith(prefisso) and f.endswith(".wav"))
    voci = []
    offset = 0.0
    byte_tot = 0
    campioni = 0
    for nome in file_ord:
        p = os.path.join(dir_audio, nome)
        byte = os.path.getsize(p)
        try:
            import wave
            with wave.open(p, "rb") as w:
                n = w.getnframes()
                fs = w.getframerate()
            d = n / float(fs)
        except Exception:
            d = max(0.0, (byte - 44) / float(FS_RICHIESTO * BYTE_PER_CAMPIONE))
            n = int(d * FS_RICHIESTO)
        voci.append({"nome": nome, "offset_s": round(offset, 3),
                     "durata_s": round(d, 3), "byte": byte})
        offset += d
        byte_tot += byte
        campioni += n
    return {"cartella": dir_audio, "formato": "wav", "n_file": len(voci),
            "byte_totali": byte_tot, "file": voci,
            "_durata_s": offset, "_campioni": campioni}


def comprimi_in_flac(dir_audio: str, prefisso: str, elimina_wav: bool) -> None:
    """Converte i WAV della notte in FLAC verificando che sia bit-exact.

    Da lanciare la mattina dopo. FLAC è lossless: il dato non si degrada, e
    l'occupazione scende a circa un terzo. Se il confronto MD5 del PCM decodificato
    non torna, il WAV NON viene cancellato.
    """
    exe = DSP.ffmpeg_path()
    import hashlib
    file_wav = sorted(f for f in os.listdir(dir_audio)
                      if f.startswith(prefisso) and f.endswith(".wav"))
    if not file_wav:
        print("Nessun WAV da comprimere.")
        return
    risparmio = 0
    for nome in file_wav:
        src = os.path.join(dir_audio, nome)
        dst = src[:-4] + ".flac"
        if os.path.exists(dst):
            continue
        r = subprocess.run([exe, "-v", "error", "-nostdin", "-i", src,
                            "-c:a", "flac", "-compression_level", "8", dst],
                           capture_output=True)
        if r.returncode != 0:
            print(f"  ! errore su {nome}: {r.stderr.decode()[:200]}")
            continue

        def md5_pcm(path: str) -> str:
            pr = subprocess.run([exe, "-v", "error", "-nostdin", "-i", path,
                                 "-f", "s16le", "-"], capture_output=True)
            return hashlib.md5(pr.stdout).hexdigest()

        if md5_pcm(src) != md5_pcm(dst):
            print(f"  ! {nome}: FLAC NON bit-exact, WAV conservato")
            os.remove(dst)
            continue
        risparmio += os.path.getsize(src) - os.path.getsize(dst)
        if elimina_wav:
            os.remove(src)
        print(f"  ✓ {nome} -> {os.path.basename(dst)}")
    print(f"Spazio risparmiato: {risparmio / 1024**2:.0f} MB")


# ==========================================================================
# Interazione iniziale
# ==========================================================================

def _chiedi(testo: str, default=None, conv=str):
    if default is not None:
        testo = f"{testo} [{default}]: "
    else:
        testo = f"{testo}: "
    try:
        v = input(testo).strip()
    except EOFError:
        return default
    if not v:
        return default
    try:
        return conv(v)
    except ValueError:
        print("  valore non valido, ignorato")
        return default


def raccogli_metadati_iniziali(ns: argparse.Namespace, meta: dict) -> None:
    """Il momento in cui i metadati si raccolgono è ORA, non domani."""
    if ns.non_interattivo:
        return
    print("\n--- Condizioni della notte (Invio per saltare) ---")
    amb = meta["ambiente"]
    pos = meta["posizione"]
    if pos["stanza"] is None:
        pos["stanza"] = _chiedi("Stanza", ns.stanza)
    pos["altezza_cm"] = _chiedi("Altezza del microfono da terra (cm)",
                                pos["altezza_cm"] or 120, float)
    pos["supporto"] = _chiedi("Supporto (treppiede/mensola/montante)",
                              pos["supporto"] or "mensola")
    amb["temperatura_c_inizio"] = _chiedi("Temperatura ora (°C)",
                                          amb["temperatura_c_inizio"], float)
    amb["umidita_pct_inizio"] = _chiedi("Umidità relativa ora (%)",
                                        amb["umidita_pct_inizio"], float)
    f = _chiedi("Finestra (aperta/chiusa/zanzariera)", amb["finestra"])
    if f in MD.FINESTRA:
        amb["finestra"] = f
    amb["persone_presenti"] = _chiedi("Persone che dormiranno in stanza",
                                      amb["persone_presenti"], int)
    amb["condizionatore"] = _chiedi("Condizionatore acceso? (si/no)",
                                    "no") in ("si", "sì", "s", "y")
    amb["ventilatore"] = _chiedi("Ventilatore acceso? (si/no)",
                                 "no") in ("si", "sì", "s", "y")
    sorgenti = _chiedi("Sorgenti di rumore note (virgole)", "")
    if sorgenti:
        meta["rumore"]["sorgenti_note"] = [s.strip() for s in sorgenti.split(",")
                                           if s.strip()]
    meta["operatore"] = _chiedi("Operatore", meta["operatore"] or
                                os.environ.get("USER"))
    print("-------------------------------------------------\n")


# ==========================================================================
# main
# ==========================================================================

def costruisci_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="registratore.py",
        description="Registratore notturno 48 kHz per il dataset zanzare "
                    "(R2-Sentinel, fase 1).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Esempi:\n"
               "  python3 registratore.py --elenca-dispositivi\n"
               "  python3 registratore.py --prova\n"
               "  python3 registratore.py --stanza camera --ore 8\n"
               "  python3 registratore.py --stanza soggiorno --ore 8 "
               "--controllo-negativo\n")
    ap.add_argument("--stanza", default=None, help="nome della stanza")
    ap.add_argument("--ore", type=float, default=8.0,
                    help="durata in ore (default 8; il gate ne chiede ≥6)")
    ap.add_argument("--fino-alle", default=None,
                    help="orario di fine HH:MM; ha la precedenza su --ore")
    ap.add_argument("--dispositivo", default=None,
                    help="specifica ffmpeg del dispositivo (es. ':1', 'hw:1,0')")
    ap.add_argument("--backend", default=None,
                    choices=("avfoundation", "alsa", "pulse"))
    ap.add_argument("--dir-audio", default=DIR_AUDIO_DEFAULT,
                    help=f"cartella audio, FUORI dal repo (default {DIR_AUDIO_DEFAULT})")
    ap.add_argument("--segmento-s", type=int, default=600,
                    help="durata dei segmenti in secondi (default 600)")
    ap.add_argument("--microfono", default=None,
                    help="modello del microfono, per i metadati")
    ap.add_argument("--controllo-negativo", action="store_true",
                    help="notte di controllo: nessuna zanzara attesa (ne servono ≥5)")
    ap.add_argument("--intervallo-controllo", type=int, default=300,
                    help="secondi fra due misure di livello (default 300)")
    ap.add_argument("--soglia-silenzio-dbfs", type=float, default=-72.0,
                    help="sotto questo RMS scatta l'allarme microfono muto")
    ap.add_argument("--non-interattivo", action="store_true",
                    help="non chiede nulla: usare solo con cron/systemd")
    ap.add_argument("--no-caffeinate", action="store_true",
                    help="non impedire lo sleep (sconsigliato su macOS)")
    ap.add_argument("--consenti-audio-nel-repo", action="store_true",
                    help="PERICOLOSO: permette di scrivere audio dentro il repo Git")
    ap.add_argument("--prova", action="store_true",
                    help="registrazione di prova da 60 s, per verificare la catena")
    ap.add_argument("--elenca-dispositivi", action="store_true")
    ap.add_argument("--comprimi", metavar="PREFISSO", default=None,
                    help="converte in FLAC i WAV di una sessione già chiusa")
    ap.add_argument("--elimina-wav", action="store_true",
                    help="con --comprimi: cancella i WAV dopo verifica bit-exact")
    return ap


def main(argv: list[str]) -> int:
    ns = costruisci_parser().parse_args(argv)
    ns.backend = ns.backend or backend_predefinito()

    if not DSP.ffmpeg_path():
        print("ERRORE: ffmpeg non è nel PATH.\n"
              "  macOS:  brew install ffmpeg\n"
              "  Debian/Ubuntu:  sudo apt install ffmpeg", file=sys.stderr)
        return 2

    if ns.elenca_dispositivi:
        elenca_dispositivi(ns.backend)
        return 0

    dir_audio = os.path.abspath(os.path.expanduser(ns.dir_audio))

    if ns.comprimi:
        comprimi_in_flac(dir_audio, ns.comprimi, ns.elimina_wav)
        return 0

    # --- guardia privacy: l'audio non entra nella working copy Git ---------
    radice_repo = os.path.abspath(os.path.join(QUI, "..", ".."))
    if not ns.consenti_audio_nel_repo and \
            (dir_audio == radice_repo or dir_audio.startswith(radice_repo + os.sep)):
        print("ERRORE: --dir-audio punta dentro il repository Git.\n"
              "  L'audio notturno di un'abitazione non va nella working copy: "
              "la history di Git non si cancella davvero (CONTRIBUTING.md).\n"
              f"  Usa una cartella esterna, es. {DIR_AUDIO_DEFAULT}",
              file=sys.stderr)
        return 2

    if ns.dispositivo is None:
        print("Nessun dispositivo indicato. Dispositivi disponibili:\n")
        elenca_dispositivi(ns.backend)
        print("\nRilancia con  --dispositivo <spec>")
        return 2

    # --- durata -----------------------------------------------------------
    if ns.prova:
        durata_s = 60.0
    elif ns.fino_alle:
        oh, om = (int(x) for x in ns.fino_alle.split(":"))
        adesso = _dt.datetime.now()
        fine = adesso.replace(hour=oh, minute=om, second=0, microsecond=0)
        if fine <= adesso:
            fine += _dt.timedelta(days=1)
        durata_s = (fine - adesso).total_seconds()
    else:
        durata_s = ns.ore * 3600.0

    # --- preflight --------------------------------------------------------
    print("=" * 68)
    print("  R2-Sentinel — banco acustico, fase 1 (raccolta dataset zanzare)")
    print("=" * 68)
    _log(f"backend={ns.backend}  dispositivo={ns.dispositivo}")
    _log("sondaggio del dispositivo...")
    sonda = sonda_dispositivo(ns.backend, ns.dispositivo)
    if not sonda["ok"]:
        print("\nERRORE: il dispositivo non si apre.\n" + sonda["stderr"],
              file=sys.stderr)
        print("\nCause tipiche: indice sbagliato, microfono scollegato, "
              "permesso Microfono negato al Terminale "
              "(Impostazioni > Privacy e sicurezza > Microfono).", file=sys.stderr)
        return 2

    rate_nativo = sonda["rate_nativo"]
    ricampiona = (rate_nativo is not None and rate_nativo != FS_RICHIESTO)
    if rate_nativo is None:
        _log("ATTENZIONE: rate nativo non determinato, si forza 48 kHz")
        ricampiona = True
    elif ricampiona:
        print(f"\nATTENZIONE: il dispositivo campiona nativamente a {rate_nativo} Hz.\n"
              f"  Verrà ricampionato a {FS_RICHIESTO} Hz, ma NON è vero audio a 48 kHz:\n"
              "  i metadati lo segneranno e `valida()` scarterà la notte dal conteggio\n"
              "  del gate. Imposta il dispositivo a 48 kHz (macOS: Utility Audio MIDI)\n"
              "  prima di dedicargli una notte.\n")
    else:
        _log(f"rate nativo {rate_nativo} Hz — corretto, nessun ricampionamento")

    os.makedirs(dir_audio, exist_ok=True)
    necessari = int(durata_s * FS_RICHIESTO * BYTE_PER_CAMPIONE * 1.02)
    liberi = shutil.disk_usage(dir_audio).free
    _log(f"disco: servono ~{necessari/1024**3:.1f} GB, liberi {liberi/1024**3:.1f} GB")
    if liberi < necessari + MARGINE_DISCO_BYTE:
        print("\nERRORE: spazio su disco insufficiente "
              f"(servono {necessari/1024**3:.1f} GB + 2 GB di margine).",
              file=sys.stderr)
        return 2

    # --- metadati ---------------------------------------------------------
    ora_avvio = _dt.datetime.now().astimezone()
    stanza_slug = (ns.stanza or "stanza").lower().replace(" ", "-")
    # la notte si data al giorno in cui INIZIA la sera: prima delle 12 appartiene
    # alla notte precedente, altrimenti due file per la stessa notte
    giorno = ora_avvio.date() if ora_avvio.hour >= 12 else \
        (ora_avvio - _dt.timedelta(days=1)).date()
    base_id = f"{giorno.isoformat()}_{stanza_slug}"
    id_notte = base_id
    n = 1
    while os.path.exists(MD.percorso_notte(id_notte)):
        n += 1
        id_notte = f"{base_id}_{n:02d}"
    prefisso = id_notte + ("_prova" if ns.prova else "")

    meta = MD.schema_notte_vuoto()
    meta["id_notte"] = id_notte
    meta["sessione_id"] = ora_avvio.strftime("%Y%m%dT%H%M%S")
    meta["inizio"] = ora_avvio.isoformat(timespec="seconds")
    meta["durata_richiesta_s"] = round(durata_s, 1)
    meta["operatore"] = os.environ.get("USER")
    meta["posizione"]["stanza"] = ns.stanza
    meta["dispositivo"].update({
        "backend": ns.backend,
        "spec": ns.dispositivo,
        "nome": nome_dispositivo(ns.backend, ns.dispositivo),
        "modello_microfono": ns.microfono,
        "sample_rate_hz": FS_RICHIESTO,
        "sample_rate_nativo_hz": rate_nativo,
        "ricampionato": bool(ricampiona),
        "canali": 1, "bit": 16, "codec": "pcm_s16le",
    })
    if ns.controllo_negativo:
        meta["annotazione"]["controllo_negativo"] = True
        meta["annotazione"]["note"] = ("Notte pianificata come controllo negativo: "
                                       "va comunque annotata al risveglio.")

    raccogli_metadati_iniziali(ns, meta)
    percorso_meta = MD.salva(meta)     # salvato SUBITO: un crash lascia traccia
    _log(f"metadati: {percorso_meta}")
    _log(f"audio:    {dir_audio}/{prefisso}_*.wav")

    fine_prevista = ora_avvio + _dt.timedelta(seconds=durata_s)
    print()
    _log(f"REGISTRAZIONE AVVIATA — fine prevista {fine_prevista.strftime('%H:%M:%S')} "
         f"({durata_s/3600:.2f} h)")
    _log("Ctrl-C chiude in modo pulito e conserva quanto registrato.")
    if ns.controllo_negativo:
        _log(">>> NOTTE DI CONTROLLO NEGATIVO <<<")
    print()

    ses = Sessione(ns)
    ses.ricampiona = ricampiona

    def _segnale(signum, frame):
        ses.motivo_fine = "interrotta_da_operatore"
        ses.evento("SIGNAL", segnale=signum)
        ses.ferma.set()
        ses._chiudi_ffmpeg()

    signal.signal(signal.SIGINT, _segnale)
    signal.signal(signal.SIGTERM, _segnale)

    t0 = time.time()
    try:
        ses.esegui(dir_audio, prefisso, durata_s)
    finally:
        ora_fine = _dt.datetime.now().astimezone()
        inv = inventario(dir_audio, prefisso)
        durata_audio = inv.pop("_durata_s")
        campioni = inv.pop("_campioni")
        wall = time.time() - t0

        meta = MD.carica(percorso_meta)
        meta["fine"] = ora_fine.isoformat(timespec="seconds")
        meta["durata_audio_s"] = round(durata_audio, 2)
        meta["durata_wall_s"] = round(wall, 2)
        meta["campioni_totali"] = campioni
        meta["n_gap"] = ses.n_riavvii
        meta["gap_totale_s"] = round(max(0.0, wall - durata_audio), 2)
        meta["audio"] = inv
        meta["eventi_sessione"] = ses.eventi
        if ses.livelli:
            meta["rumore"]["rms_dbfs_mediano"] = round(
                DSP.mediana([x["rms_dbfs"] for x in ses.livelli]), 1)
            meta["rumore"]["picco_dbfs"] = round(
                max(x["picco_dbfs"] for x in ses.livelli), 1)
            meta["rumore"]["serie_livelli"] = ses.livelli
        meta["note"] = (meta.get("note") or "") + f" [fine: {ses.motivo_fine}]"
        MD.salva(meta, percorso_meta)

        print()
        print("=" * 68)
        _log(f"FINE ({ses.motivo_fine})")
        print(f"  audio utile     : {durata_audio/3600:.2f} h "
              f"({inv['n_file']} segmenti, {inv['byte_totali']/1024**3:.2f} GB)")
        print(f"  tempo trascorso : {wall/3600:.2f} h")
        print(f"  interruzioni    : {ses.n_riavvii}  "
              f"(persi {meta['gap_totale_s']:.1f} s)")
        if ses.livelli:
            print(f"  rumore di fondo : RMS mediano "
                  f"{meta['rumore']['rms_dbfs_mediano']} dBFS, "
                  f"picco {meta['rumore']['picco_dbfs']} dBFS")
        print(f"  metadati        : {percorso_meta}")
        print("=" * 68)
        if not ns.prova:
            print("\nAL RISVEGLIO, obbligatorio — senza questo la notte non conta:\n"
                  f"  python3 metadati.py ambiente {id_notte} --temp-fine 24.5 "
                  "--umid-fine 60\n"
                  f"  python3 metadati.py annota {id_notte} --esito positiva "
                  "--metodo uditivo\n"
                  f"  python3 metadati.py privacy {id_notte} --voce assente\n"
                  f"  python3 metadati.py utile {id_notte} --si\n"
                  f"  python3 indice.py aggiorna\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
