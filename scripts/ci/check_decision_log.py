#!/usr/bin/env python3
"""Una PR che cambia un'architettura senza aggiornare il Decision Log e'
incompleta (CONTRIBUTING.md). Qui la regola diventa automatica.

Cosa conta come "cambio di architettura": i percorsi elencati in ARCH_PATTERNS.
Sono i punti in cui una modifica cambia un contratto fra ruoli, non
l'implementazione di uno solo. Modificare l'interno di un nodo non richiede una
decisione; cambiare un messaggio che tre nodi consumano si'.

Cosa conta come "aggiornare il Decision Log": una riga aggiunta o modificata in
docs/PROJECT.md che inizia con `| D-NN |` dentro la §3.

Deroga: un commit della PR con il trailer
    Decision-Log-Exempt: <motivo di almeno 20 caratteri>
La deroga non e' silenziosa: viene stampata nel log della CI.

Uso: check_decision_log.py --diff BASE HEAD
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
import sys

ARCH_PATTERNS = [
    # contratti fra ruoli
    "software/ros2_ws/src/r2s_interfaces/msg/*",
    "software/ros2_ws/src/r2s_interfaces/srv/*",
    "software/ros2_ws/src/*/package.xml",
    "software/ros2_ws/src/r2s_mqtt_bridge/config/topics.yaml",
    # piattaforma e riproducibilita'
    ".gitattributes",
    ".gitignore",
    "scripts/bootstrap.sh",
    "scripts/setup/*",
    ".github/workflows/*",
    "docker/*",
    "models/MANIFEST.yaml",
    "tests/fatto/registry.yaml",
    # struttura del firmware
    "firmware/*/CMakeLists.txt",
    "firmware/*/main/CMakeLists.txt",
    "firmware/*/sdkconfig.defaults",
    # sicurezza: qui il Decision Log non e' burocrazia
    "SAFETY.md",
]

DECISION_ROW = re.compile(r"^\+\s*\|\s*D-\d+\s*\|")
EXEMPT = re.compile(r"^Decision-Log-Exempt:\s*(.+)$", re.MULTILINE)


def sh(args: list[str]) -> str:
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--diff", nargs=2, metavar=("BASE", "HEAD"), required=True)
    a = ap.parse_args()
    base, head = a.diff
    ref = sh(["git", "merge-base", base, head]).strip() or base

    changed = [f for f in sh(
        ["git", "diff", "--name-only", "--diff-filter=ACMRD", ref, head]
    ).splitlines() if f.strip()]

    arch = [f for f in changed
            if any(fnmatch.fnmatch(f, p) for p in ARCH_PATTERNS)]

    if not arch:
        print("Decision Log: nessun file architetturale toccato, controllo non applicabile")
        return 0

    print("File architetturali modificati:")
    for f in arch:
        print(f"  - {f}")

    project_diff = sh(["git", "diff", "-U0", ref, head, "--", "docs/PROJECT.md"])
    rows = [ln for ln in project_diff.splitlines() if DECISION_ROW.match(ln)]

    if rows:
        print(f"\nOK — Decision Log aggiornato ({len(rows)} riga/righe D-NN):")
        for r in rows:
            print("  " + r[:160])
        return 0

    msgs = sh(["git", "log", "--format=%B", f"{ref}..{head}"])
    m = EXEMPT.search(msgs)
    if m and len(m.group(1).strip()) >= 20:
        print(f"\nDEROGA accettata — Decision-Log-Exempt: {m.group(1).strip()}")
        print("La deroga resta nel log della CI e nella history dei commit.")
        return 0
    if m:
        print(f"\nDeroga RIFIUTATA: motivo troppo corto ({m.group(1).strip()!r}). "
              "Servono almeno 20 caratteri di motivazione.")

    print("\nFALLITO — architettura modificata senza una riga nel Decision Log.")
    print("Aggiungi a docs/PROJECT.md §3 una riga nel formato:")
    print("  | D-NN | Decisione | Perche', e cosa e' stato scartato | AAAA-MM-GG |")
    print("Il valore di questo repository e' nel 'perche'', non nel 'cosa' "
          "(CONTRIBUTING.md).")
    print("Se la modifica davvero non e' una decisione, aggiungi al commit il "
          "trailer:\n  Decision-Log-Exempt: <motivo, almeno 20 caratteri>")
    return 1


if __name__ == "__main__":
    sys.exit(main())
