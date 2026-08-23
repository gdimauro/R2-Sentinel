#!/usr/bin/env python3
"""La nota di conformita' come condizione di merge tracciabile.

`compliance-safety` ha un criterio di FATTO che dice: **0 pull request sul
payload chiuse senza una nota di conformita' nel dossier**. Un criterio del
genere affidato all'abitudine non e' un criterio.

Questo controllo NON entra nel merito (non e' il suo mestiere): verifica solo
che, quando una PR tocca il payload o la sicurezza, esista una traccia della
nota. Il giudizio resta di `compliance-safety`.

Traccia accettata, in ordine di preferenza:
  1. una nota nel dossier: file aggiunto/modificato sotto docs/compliance/
  2. l'etichetta `conformita-ok` sulla PR (apposta da compliance-safety)

Uso: check_compliance_gate.py --diff BASE HEAD
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
import sys

PAYLOAD_PATTERNS = [
    "cad/src/*nozzle*", "cad/src/*ugello*", "cad/src/*girante*", "cad/src/*impeller*",
    "firmware/*/main/*payload*", "firmware/*/main/*valve*", "firmware/*/main/*heater*",
    "software/ros2_ws/src/r2s_interfaces/srv/TriggerPayload.srv",
    "software/**/payload*",
    "hardware/bom/*",
    "SAFETY.md",
    # docs/PROJECT.md NON e' in elenco di proposito: e' toccato da quasi ogni PR
    # (Decision Log) e chiedere una nota di conformita' ogni volta trasformerebbe
    # il gate in rumore. Un controllo che si impara a ignorare non protegge nulla.
]
LABEL = "conformita-ok"


def sh(args: list[str]) -> str:
    return subprocess.run(args, capture_output=True, text=True).stdout


def ref_exists(ref: str) -> bool:
    return subprocess.run(["git", "rev-parse", "--verify", "--quiet", ref],
                          capture_output=True).returncode == 0


def pr_labels() -> list[str]:
    p = os.environ.get("GITHUB_EVENT_PATH")
    if not p or not os.path.isfile(p):
        return []
    try:
        ev = json.load(open(p))
        return [x["name"] for x in ev.get("pull_request", {}).get("labels", [])]
    except Exception:
        return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--diff", nargs=2, metavar=("BASE", "HEAD"), required=True)
    a = ap.parse_args()
    if not ref_exists(a.diff[0]):
        print(f"Conformita': riferimento '{a.diff[0]}' non risolvibile "
              "(esecuzione fuori da una pull request). Controllo non applicabile.")
        return 0
    ref = sh(["git", "merge-base", *a.diff]).strip() or a.diff[0]
    changed = [f for f in sh(["git", "diff", "--name-only", ref, a.diff[1]]).splitlines() if f]

    touched = [f for f in changed if any(fnmatch.fnmatch(f, p) for p in PAYLOAD_PATTERNS)]
    if not touched:
        print("Conformita': la PR non tocca payload/sicurezza, gate non applicabile")
        return 0

    print("La PR tocca payload o sicurezza:")
    for f in touched:
        print(f"  - {f}")

    dossier = [f for f in changed if f.startswith("docs/compliance/")]
    if dossier:
        print("\nOK — nota di conformita' nel dossier: " + ", ".join(dossier))
        return 0

    labels = pr_labels()
    if LABEL in labels:
        print(f"\nOK — etichetta `{LABEL}` presente sulla PR.")
        print("Tracciabile, ma la nota nel dossier resta la forma preferita.")
        return 0

    print("\nFALLITO — manca la traccia della nota di conformita'.")
    print(f"Serve un file sotto docs/compliance/ oppure l'etichetta `{LABEL}` "
          "apposta da compliance-safety.")
    print("Questo controllo non giudica il merito: rende solo il giudizio "
          "una condizione di merge invece che un'abitudine.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
