#!/usr/bin/env python3
"""Scarica e verifica i pesi dei modelli descritti in models/MANIFEST.yaml.

Principio: un artefatto senza sha256 non si scarica. Un peso sbagliato non da'
errore, da' numeri sbagliati che sembrano giusti — ed e' molto peggio.

    scripts/models/fetch_models.py                 scarica cio' che manca e verifica
    scripts/models/fetch_models.py --verify-only   verifica soltanto
    scripts/models/fetch_models.py --hash FILE     calcola lo sha256 di un file
"""
from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "models/MANIFEST.yaml"


def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def url_for(m: dict, art: dict) -> str:
    src = m["sources"][art["source"]]
    if src["kind"] == "github-release":
        return src["url_template"].format(repo=src["repo"], tag=art["tag"], name=art["name"])
    base = os.path.expandvars(src.get("base_url", ""))
    if not base:
        raise SystemExit(f"sorgente '{art['source']}' non configurata (R2S_MODEL_MIRROR)")
    return base.rstrip("/") + "/" + art["name"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--hash", metavar="FILE")
    ap.add_argument("--role", help="scarica solo gli artefatti di un ruolo")
    a = ap.parse_args()

    if a.hash:
        p = pathlib.Path(a.hash)
        print(f"{sha256(p)}  {p.name}  ({p.stat().st_size} byte)")
        return 0

    m = yaml.safe_load(MANIFEST.read_text())
    dest = ROOT / m["destination"]
    arts = m.get("artifacts") or []
    if a.role:
        arts = [x for x in arts if x.get("role") == a.role]

    if not arts:
        print("MANIFEST: 0 artefatti dichiarati.")
        print("Non e' un errore: nessun peso e' ancora stato prodotto.")
        print("Quando il primo peso esiste, va aggiunto qui con sorgente e sha256,")
        print("altrimenti il numero che produce non e' riproducibile da nessuno.")
        return 0

    dest.mkdir(parents=True, exist_ok=True)
    bad = 0
    for art in arts:
        target = dest / art["name"]
        digest = (art.get("sha256") or "").strip().lower()
        if len(digest) != 64 or set(digest) == {"0"}:
            print(f"FALLITO  {art['name']}: sha256 assente o segnaposto nel MANIFEST")
            bad += 1
            continue
        if not target.exists():
            if a.verify_only:
                print(f"ASSENTE  {art['name']} (scarica con: make models)")
                continue
            url = url_for(m, art)
            print(f"scarico  {art['name']} da {url}")
            rc = subprocess.run(["curl", "-fL", "--retry", "3", "-o", str(target), url]).returncode
            if rc != 0:
                print(f"FALLITO  download di {art['name']}")
                bad += 1
                continue
        actual = sha256(target)
        if actual != digest:
            print(f"FALLITO  {art['name']}: sha256 {actual[:16]}... != atteso {digest[:16]}...")
            print("         Il file non e' quello dichiarato. Non usarlo: i numeri che")
            print("         produrrebbe non sarebbero attribuibili a nulla.")
            bad += 1
        else:
            print(f"OK       {art['name']} ({target.stat().st_size} byte, sha256 verificato)")

    print(f"\n{len(arts) - bad}/{len(arts)} artefatti verificati")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
