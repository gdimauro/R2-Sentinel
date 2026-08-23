#!/usr/bin/env bash
# Comando unico per eseguire un criterio di FATTO.
#
#   ./scripts/fatto.sh                    tutto cio' che gira senza banco
#   ./scripts/fatto.sh vision-perception  i criteri di un ruolo
#   ./scripts/fatto.sh --list             elenco con stato
#   ./scripts/fatto.sh --coverage         quanti criteri hanno un comando
#
# Registro: tests/fatto/registry.yaml
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="$(command -v python3)"
exec "$PY" "$ROOT/tests/fatto/runner.py" "$@"
