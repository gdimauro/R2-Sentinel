#!/usr/bin/env python3
"""Controlli di igiene del repository R2-Sentinel.

Trasforma in controllo automatico le regole che CONTRIBUTING.md affida alla
diligenza umana. Una regola ricordata viene violata; una regola che fa fallire
la PR no.

Regole applicate (ognuna ha un id stabile, citabile in una PR):
  R1  pesi di modelli   (*.pt *.pth *.onnx *.hef *.engine *.tflite)
  R2  dataset           (qualsiasi percorso sotto datasets/)
  R3  mappe SLAM        (*.pgm *.posegraph *.pbstream, directory maps/)
  R4  audio e video     (registrazioni di interni)
  R5  credenziali       (per nome file e per contenuto)
  R6  export CAD non passati da Git LFS   <-- gate 0
  R7  binari > 5 MB fuori da LFS
  R8  immagini/registrazioni sotto directory di acquisizione

Modi d'uso:
    check_hygiene.py --staged                 # hook pre-commit
    check_hygiene.py --diff origin/main HEAD  # CI su pull request
    check_hygiene.py --worktree               # tutto cio' che e' tracciato
    check_hygiene.py --paths a b c            # file espliciti (per i test)

Uscita: 0 pulito, 1 violazioni, 2 errore interno.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Iterable

MAX_BINARY_BYTES = 5 * 1024 * 1024        # criterio: 0 binari > 5 MB fuori LFS
MAX_LFS_POINTER_BYTES = 200               # un puntatore LFS sta sotto 200 byte
LFS_MAGIC = b"version https://git-lfs.github.com/spec/v1"

WEIGHT_EXT = {".pt", ".pth", ".onnx", ".hef", ".engine", ".tflite", ".trt"}
SLAM_EXT = {".pgm", ".posegraph", ".pbstream", ".serialized"}
AUDIO_EXT = {".wav", ".flac", ".mp3", ".ogg", ".m4a", ".aac", ".opus", ".raw"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".heic"}
CAD_BINARY_EXT = {".step", ".stp", ".stl", ".3mf", ".f3d", ".iges", ".igs", ".gcode"}

CAPTURE_DIRS = {"recordings", "capture", "raw", "notturne", "riprese"}

CRED_NAME_PATTERNS = [
    ".env", ".env.*", "secrets.yaml", "secrets.yml", "secret.yaml",
    "*.pem", "*.p12", "*.pfx", "*.jks", "id_rsa", "id_rsa.*", "id_ed25519",
    "credentials.json", "credentials.yaml", "*.credentials", "*_credentials*",
    ".netrc", ".pgpass", "*.keystore",
]
# *.key e' ambiguo (esistono .key non segreti): lo trattiamo con il contenuto.

# Regex sul CONTENUTO dei file di testo. Volutamente poche e specifiche:
# un controllo che urla a ogni commit viene disattivato dopo tre giorni.
CRED_CONTENT = [
    (re.compile(rb"-----BEGIN (RSA |EC |OPENSSH |PGP |DSA )?PRIVATE KEY-----"),
     "chiave privata in chiaro"),
    (re.compile(rb"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{36,}"), "token GitHub"),
    (re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{10,}"), "token Slack"),
    (re.compile(rb"(?i)\b(password|passwd|passphrase|mqtt_pass|api[_-]?key|"
                rb"secret[_-]?key|auth[_-]?token)\b\s*[:=]\s*"
                rb"['\"]?(?!\s*$)(?!\$\{)(?!<)(?!\.\.\.)(?!x{3,})(?!CHANGEME)"
                rb"(?!changeme)(?!TODO)[A-Za-z0-9_\-/+.!@#]{8,}"),
     "credenziale in chiaro (password/api key/token)"),
]

# Estensioni per cui un contenuto binario grosso e' atteso e legittimo se e solo
# se passa da LFS. Tutto il resto sopra soglia e' un errore a prescindere.
TEXTLIKE_EXT = {
    ".md", ".txt", ".py", ".c", ".h", ".cpp", ".hpp", ".yaml", ".yml", ".json",
    ".toml", ".cfg", ".ini", ".xml", ".sh", ".bash", ".cmake", ".rst", ".csv",
    ".launch", ".urdf", ".xacro", ".sql", ".js", ".ts", ".html", ".css", ".svg",
}

ALLOWLIST_FILE = ".ci-hygiene-allow"


@dataclass
class Violation:
    rule: str
    path: str
    message: str
    fix: str

    def line(self) -> str:
        return f"  [{self.rule}] {self.path}\n        {self.message}\n        -> {self.fix}"


@dataclass
class Ctx:
    root: pathlib.Path
    rev: str | None            # None = leggi dal filesystem; altrimenti da git
    allow: list[tuple[str, str]] = field(default_factory=list)

    def is_allowed(self, path: str) -> str | None:
        for pattern, reason in self.allow:
            if fnmatch.fnmatch(path, pattern):
                return reason
        return None


def run(args: list[str], root: pathlib.Path) -> str:
    return subprocess.run(args, cwd=root, check=True, capture_output=True,
                          text=True).stdout


def read_blob(ctx: Ctx, path: str, limit: int | None = None) -> bytes:
    """Contenuto del file cosi' come finirebbe in history (non dal worktree)."""
    if ctx.rev is None:
        p = ctx.root / path
        if not p.is_file():
            return b""
        with open(p, "rb") as fh:
            return fh.read(limit) if limit else fh.read()
    spec = f"{ctx.rev}:{path}" if ctx.rev != ":0" else f":{path}"
    r = subprocess.run(["git", "show", spec], cwd=ctx.root, capture_output=True)
    if r.returncode != 0:
        return b""
    return r.stdout[:limit] if limit else r.stdout


def blob_size(ctx: Ctx, path: str) -> int:
    if ctx.rev is None:
        p = ctx.root / path
        return p.stat().st_size if p.is_file() else 0
    spec = f"{ctx.rev}:{path}" if ctx.rev != ":0" else f":{path}"
    r = subprocess.run(["git", "cat-file", "-s", spec], cwd=ctx.root,
                       capture_output=True, text=True)
    return int(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else 0


def is_lfs_pointer(data: bytes) -> bool:
    return data.startswith(LFS_MAGIC)


def load_allowlist(root: pathlib.Path) -> list[tuple[str, str]]:
    """Deroghe esplicite. Ogni riga: <glob> <TAB o spazi> <motivo>.

    Senza motivo la riga viene rifiutata: una deroga senza perche' e' un buco.
    """
    f = root / ALLOWLIST_FILE
    out: list[tuple[str, str]] = []
    if not f.exists():
        return out
    for n, raw in enumerate(f.read_text().splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or len(parts[1].strip()) < 10:
            print(f"ATTENZIONE: {ALLOWLIST_FILE}:{n} deroga senza motivo, ignorata: {line}",
                  file=sys.stderr)
            continue
        out.append((parts[0], parts[1].strip()))
    return out


# --------------------------------------------------------------------------- #
# Regole
# --------------------------------------------------------------------------- #

def check_file(ctx: Ctx, path: str) -> list[Violation]:
    v: list[Violation] = []
    p = pathlib.PurePosixPath(path)
    ext = p.suffix.lower()
    parts = set(p.parts)
    lower_parts = {x.lower() for x in p.parts}

    # -- R1 pesi di modelli ------------------------------------------------- #
    if ext in WEIGHT_EXT:
        v.append(Violation(
            "R1", path,
            f"peso di modello ({ext}) nel diff: i pesi stanno fuori dal repository",
            "rimuovilo dal commit, pubblicalo nella release e registralo in "
            "models/MANIFEST.yaml con lo sha256 (`make models-manifest`)"))

    # -- R2 dataset --------------------------------------------------------- #
    if "datasets" in parts or path.startswith("datasets/"):
        v.append(Violation(
            "R2", path,
            "file sotto datasets/: i dataset non stanno nel repository",
            "tienilo fuori dal worktree o sotto un percorso ignorato; "
            "descrivi provenienza e checksum in models/MANIFEST.yaml"))

    # -- R3 mappe SLAM ------------------------------------------------------ #
    if ext in SLAM_EXT or (lower_parts & {"maps", "slam_maps", "mappe"}):
        v.append(Violation(
            "R3", path,
            "mappa SLAM o suo derivato: e' la planimetria dell'abitazione "
            "(CONTRIBUTING.md §Privacy)",
            "NON committarlo. Se e' gia' in history NON rimuoverlo con un altro "
            "commit: segnalalo al chief-engineer, serve un rewrite della history"))
    if ext in {".yaml", ".yml"} and p.stem.lower().startswith(("map", "mappa")):
        v.append(Violation(
            "R3", path,
            "metadato di mappa SLAM (map*.yaml): stessa categoria della mappa",
            "tienilo fuori dal repository insieme al .pgm corrispondente"))

    # -- R4 audio e video --------------------------------------------------- #
    if ext in AUDIO_EXT or ext in VIDEO_EXT:
        synth_ok = (path.startswith("tests/fixtures/audio/")
                    and path.endswith(".synth.wav")
                    and blob_size(ctx, path) < 1024 * 1024)
        if not synth_ok:
            v.append(Violation(
                "R4", path,
                "audio o video: il progetto registra dentro casa, questo materiale "
                "non entra mai in history (SAFETY.md, CONTRIBUTING.md §Privacy)",
                "tienilo nello storage locale dell'unita'; in repository vanno solo "
                "feature aggregate. Fixture sintetiche: tests/fixtures/audio/*.synth.wav <1 MB"))

    # -- R8 directory di acquisizione --------------------------------------- #
    if (lower_parts & CAPTURE_DIRS) and ext in (IMAGE_EXT | AUDIO_EXT | VIDEO_EXT):
        v.append(Violation(
            "R8", path,
            "materiale acquisito sotto una directory di ripresa/registrazione",
            "queste directory restano fuori dal repository per costruzione"))

    # -- R5 credenziali per nome -------------------------------------------- #
    name = p.name
    if name != ".env.example" and any(fnmatch.fnmatch(name, pat) for pat in CRED_NAME_PATTERNS):
        v.append(Violation(
            "R5", path,
            f"nome di file tipico di credenziali ({name})",
            "usa variabili d'ambiente (R2S_MQTT_USER/R2S_MQTT_PASS) o un file "
            "fuori dal worktree; committa al massimo un .env.example senza valori"))

    # -- R6 export CAD non passato da LFS ----------------------------------- #
    if ext in CAD_BINARY_EXT:
        head = read_blob(ctx, path, 512)
        size = blob_size(ctx, path)
        if not is_lfs_pointer(head):
            v.append(Violation(
                "R6", path,
                f"export CAD di {size} byte committato come binario grezzo, "
                "non come puntatore Git LFS (GATE 0)",
                "installa e inizializza git-lfs (`brew install git-lfs && git lfs install`), "
                "poi `git rm --cached <file> && git add <file>` e verifica con "
                "`git lfs ls-files`. Se e' gia' in history serve un rewrite: "
                "fermati e avvisa il chief-engineer"))
        elif size > MAX_LFS_POINTER_BYTES:
            v.append(Violation(
                "R6", path,
                f"puntatore LFS anomalo: {size} byte (atteso < {MAX_LFS_POINTER_BYTES})",
                "verifica lo stato di git-lfs su questa macchina"))

    # -- R5 credenziali per contenuto + R7 binari grossi -------------------- #
    size = blob_size(ctx, path)
    head = read_blob(ctx, path, 4096)
    pointer = is_lfs_pointer(head)

    if size > MAX_BINARY_BYTES and not pointer:
        v.append(Violation(
            "R7", path,
            f"file di {size / 1024 / 1024:.1f} MB fuori da Git LFS "
            f"(soglia {MAX_BINARY_BYTES // 1024 // 1024} MB)",
            "instradalo in LFS aggiungendo il pattern a .gitattributes, oppure "
            "tienilo fuori dal repository. La history non si ripulisce dopo"))

    if not pointer and (ext in TEXTLIKE_EXT or ext == "" or ext == ".key"):
        data = read_blob(ctx, path)
        if b"\x00" not in data[:8192]:
            for rx, what in CRED_CONTENT:
                m = rx.search(data)
                if m:
                    ln = data[:m.start()].count(b"\n") + 1
                    v.append(Violation(
                        "R5", f"{path}:{ln}",
                        f"{what} nel contenuto del file",
                        "sostituisci con una variabile d'ambiente o un segnaposto; "
                        "se il segreto e' reale REVOCALO: e' gia' compromesso"))
                    break
    return v


def list_files(ctx: Ctx, mode: str, base: str | None, head: str | None,
               paths: list[str] | None) -> list[str]:
    if mode == "paths":
        return list(paths or [])
    if mode == "staged":
        out = run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"], ctx.root)
    elif mode == "diff":
        merge_base = subprocess.run(["git", "merge-base", base, head], cwd=ctx.root,
                                    capture_output=True, text=True)
        ref = merge_base.stdout.strip() or base
        out = run(["git", "diff", "--name-only", "--diff-filter=ACMR", ref, head], ctx.root)
    else:  # worktree
        out = run(["git", "ls-files"], ctx.root)
    return [x for x in out.splitlines() if x.strip()]


def main(argv: Iterable[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--staged", action="store_true")
    g.add_argument("--worktree", action="store_true")
    g.add_argument("--diff", nargs=2, metavar=("BASE", "HEAD"))
    g.add_argument("--paths", nargs="+")
    ap.add_argument("--root", default=None)
    ap.add_argument("--json", action="store_true", help="output machine-readable")
    a = ap.parse_args(list(argv) if argv is not None else None)

    root = pathlib.Path(a.root or os.environ.get("R2S_ROOT")
                        or subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                          capture_output=True, text=True).stdout.strip()
                        or ".").resolve()

    if a.staged:
        mode, rev, base, head = "staged", ":0", None, None
    elif a.diff:
        mode, rev, base, head = "diff", a.diff[1], a.diff[0], a.diff[1]
    elif a.paths:
        mode, rev, base, head = "paths", None, None, None
    else:
        mode, rev, base, head = "worktree", None, None, None

    ctx = Ctx(root=root, rev=rev, allow=load_allowlist(root))

    try:
        files = list_files(ctx, mode, base, head, a.paths)
    except subprocess.CalledProcessError as e:
        print(f"errore git: {e.stderr}", file=sys.stderr)
        return 2

    violations: list[Violation] = []
    waived: list[tuple[Violation, str]] = []
    for f in files:
        for v in check_file(ctx, f):
            reason = ctx.is_allowed(v.path.split(":")[0])
            if reason:
                waived.append((v, reason))
            else:
                violations.append(v)

    if a.json:
        print(json.dumps({
            "files_checked": len(files),
            "violations": [vars(v) for v in violations],
            "waived": [{"violation": vars(v), "reason": r} for v, r in waived],
        }, indent=2))
        return 1 if violations else 0

    print(f"igiene repository: {len(files)} file esaminati (modo: {mode})")
    for v, r in waived:
        print(f"  DEROGA [{v.rule}] {v.path} — {r}")
    if not violations:
        print("OK — nessuna violazione")
        return 0

    by_rule: dict[str, list[Violation]] = {}
    for v in violations:
        by_rule.setdefault(v.rule, []).append(v)
    print(f"\nFALLITO — {len(violations)} violazioni in {len(by_rule)} regole\n")
    for rule in sorted(by_rule):
        for v in by_rule[rule]:
            print(v.line())
        print()
    print("Nessuna di queste e' una formalita': da Git la history non si cancella "
          "davvero.\nSe il file e' gia' stato spinto, avvisa il chief-engineer prima "
          "di rimuoverlo con un commit.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
