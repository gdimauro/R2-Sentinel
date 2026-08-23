#!/usr/bin/env bash
# Ambiente Python di piattaforma: strumenti di CI, harness e generatori.
# NON e' l'ambiente di runtime dei nodi ROS (quello usa il python di sistema,
# come vuole ROS 2). Separarli evita la classe di bug "funziona nel venv".
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  ok "creato .venv"
else
  skip ".venv gia' presente"
fi

# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements-dev.txt
ok "dipendenze di piattaforma installate ($(python -V))"
