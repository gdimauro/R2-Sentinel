#!/usr/bin/env bash
# =============================================================================
# R2-Sentinel — bootstrap unico.
#
#   git clone ... && cd R2-Sentinel && ./scripts/bootstrap.sh
#
# Da macchina Ubuntu 24.04 pulita a workspace ROS 2 Jazzy compilato e toolchain
# ESP-IDF pronta. Nessun passo manuale, nessun wiki da leggere.
# Budget: <= 30 min su connessione domestica.
#
# Idempotente: rieseguirlo su una macchina gia' pronta salta cio' che c'e' gia'.
#
# Opzioni:
#   --skip-ros        non installa ROS 2 (utile in container che lo ha gia')
#   --skip-idf        non installa ESP-IDF (CI dei soli test host)
#   --skip-build      non compila il workspace
#   --only <passo>    esegue un solo passo: system|lfs|ros|idf|python|ws|hooks
#   --yes             non fa domande (default in CI)
#   --help
#
# Ogni passo e' anche uno script a se' in scripts/setup/: se qualcosa fallisce
# si rilancia quel passo soltanto, non tutto.
# =============================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export R2S_ROOT="$ROOT"

SKIP_ROS=0; SKIP_IDF=0; SKIP_BUILD=0; ONLY=""; ASSUME_YES=0
[[ -n "${CI:-}" ]] && ASSUME_YES=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-ros)   SKIP_ROS=1 ;;
    --skip-idf)   SKIP_IDF=1 ;;
    --skip-build) SKIP_BUILD=1 ;;
    --only)       ONLY="$2"; shift ;;
    --yes|-y)     ASSUME_YES=1 ;;
    --help|-h)    sed -n '2,30p' "$0"; exit 0 ;;
    *) echo "opzione sconosciuta: $1"; exit 2 ;;
  esac
  shift
done
export ASSUME_YES

T0=$(date +%s)
step_start=0

banner() { printf '\n\033[1m=== %s\033[0m\n' "$*"; }
note()   { printf '    %s\n' "$*"; }
fail()   { printf '\n\033[31mFALLITO: %s\033[0m\n' "$*"; exit 1; }

run_step() {
  local id="$1" title="$2" script="$3"
  if [[ -n "$ONLY" && "$ONLY" != "$id" ]]; then return 0; fi
  banner "$title"
  step_start=$(date +%s)
  bash "$ROOT/scripts/setup/$script" || fail "passo '$id' ($script)"
  note "passo '$id' completato in $(( $(date +%s) - step_start ))s"
}

# --- controllo piattaforma --------------------------------------------------
OS="$(uname -s)"
if [[ "$OS" != "Linux" ]]; then
  cat <<EOF

ATTENZIONE — questo bootstrap ha come bersaglio Ubuntu 24.04 (PROJECT.md §6).
Sei su: $OS.

ROS 2 Jazzy e ESP-IDF non vengono installati qui. Su macOS/Windows usa il
container di riferimento, che e' la stessa cosa che gira in CI:

    make docker-shell        # apre una Ubuntu 24.04 con il repo montato
    make verify-clean        # bootstrap completo in un container vergine

Procedo con i soli passi indipendenti dalla piattaforma (python + hook git).
EOF
  SKIP_ROS=1; SKIP_IDF=1; SKIP_BUILD=1
  export R2S_HOST_ONLY=1
fi

# --- passi ------------------------------------------------------------------
[[ "$OS" == "Linux" ]] && run_step system "1/6 Dipendenze di sistema"      10_system.sh
run_step lfs    "2/6 Git LFS (gate 0)"                                     20_git_lfs.sh
[[ $SKIP_ROS  -eq 0 ]] && run_step ros    "3/6 ROS 2 Jazzy"                30_ros2.sh
run_step python "4/6 Ambiente Python di piattaforma"                       40_python.sh
[[ $SKIP_IDF  -eq 0 ]] && run_step idf    "5/6 Toolchain ESP-IDF"          50_esp_idf.sh
[[ $SKIP_BUILD -eq 0 ]] && run_step ws    "6/6 Build del workspace ROS 2"  60_workspace.sh
run_step hooks  "hook git locali"                                          70_git_hooks.sh

ELAPSED=$(( $(date +%s) - T0 ))
banner "Bootstrap completato in $((ELAPSED / 60))m $((ELAPSED % 60))s"

cat <<EOF

Cosa e' pronto:
  - workspace ROS 2:   source software/ros2_ws/install/setup.bash
  - ambiente python:   source .venv/bin/activate
  - ESP-IDF:           source \${IDF_PATH:-\$HOME/esp/esp-idf}/export.sh
  - hook pre-commit:   attivo (blocca i commit che violano CONTRIBUTING.md)

Prossimi comandi utili:
  make check           controlli di igiene + lint (quello che gira in CI)
  make test            test che NON richiedono hardware
  ./scripts/fatto.sh   esegue il criterio di FATTO di un ruolo

Se qualcosa qui sopra non e' vero, questo bootstrap ha un difetto:
segnalalo a software-platform invece di aggiustarlo a mano sulla tua macchina.
EOF
