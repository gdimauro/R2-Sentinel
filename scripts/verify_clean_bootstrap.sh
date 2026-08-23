#!/usr/bin/env bash
# =============================================================================
# Verifica della riproducibilita' su macchina VERGINE.
#
# "Funziona sulla mia macchina" e' esattamente il fallimento che questo script
# esiste per intercettare: il container non ha ROS, non ha python di progetto,
# non ha ESP-IDF, non ha nulla se non git.
#
# Il criterio chiede DUE esecuzioni riuscite, non una: la prima puo' riuscire
# per un residuo di cache locale, la seconda no.
#
#   scripts/verify_clean_bootstrap.sh              2 esecuzioni, tutto
#   scripts/verify_clean_bootstrap.sh --runs 1     una sola
#   scripts/verify_clean_bootstrap.sh --fast       salta ESP-IDF (~1,5 GB)
# =============================================================================
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNS=2
BOOT_ARGS=""
BUDGET_MIN=30

while [[ $# -gt 0 ]]; do
  case "$1" in
    --runs) RUNS="$2"; shift ;;
    --fast) BOOT_ARGS="--skip-idf" ;;
    *) echo "opzione sconosciuta: $1"; exit 2 ;;
  esac
  shift
done

command -v docker >/dev/null || { echo "serve docker per questa verifica"; exit 1; }

echo "Costruisco l'immagine vergine Ubuntu 24.04..."
docker build -q -f "$ROOT/docker/ubuntu2404-clean.Dockerfile" -t r2s-clean:latest "$ROOT" >/dev/null

FAILED=0
for i in $(seq 1 "$RUNS"); do
  echo
  echo "=============================================================="
  echo " Esecuzione $i/$RUNS su container vergine (budget ${BUDGET_MIN} min)"
  echo "=============================================================="
  T0=$(date +%s)
  # Il repo entra come sorgente di clone, non come bind mount scrivibile:
  # cosi' il container non eredita .venv, install/, build/ della tua macchina.
  if docker run --rm -v "$ROOT:/src:ro" r2s-clean:latest bash -lc "
      set -e
      git clone -q /src /home/dev/R2-Sentinel 2>/dev/null || {
        mkdir -p /home/dev/R2-Sentinel && cp -r /src/. /home/dev/R2-Sentinel/ ; }
      cd /home/dev/R2-Sentinel
      rm -rf .venv software/ros2_ws/build software/ros2_ws/install software/ros2_ws/log
      ./scripts/bootstrap.sh --yes $BOOT_ARGS
      . software/ros2_ws/install/setup.bash
      ros2 pkg list | grep -c '^r2s_' | xargs -I{} echo 'pacchetti r2s_ visibili: {}'
  "; then
    DT=$(( $(date +%s) - T0 ))
    printf "esecuzione %d: RIUSCITA in %dm %ds" "$i" $((DT/60)) $((DT%60))
    if (( DT > BUDGET_MIN * 60 )); then
      printf "  -- FUORI BUDGET (> %d min)\n" "$BUDGET_MIN"; FAILED=1
    else
      printf "  -- entro budget\n"
    fi
  else
    echo "esecuzione $i: FALLITA"
    FAILED=1
  fi
done

echo
if [[ $FAILED -eq 0 ]]; then
  echo "OK — $RUNS/$RUNS esecuzioni riuscite su ambiente vergine, entro ${BUDGET_MIN} min"
else
  echo "FALLITO — la riproducibilita' non e' dimostrata."
  echo "Non aggiustare a mano nel container: correggi scripts/bootstrap.sh."
fi
exit $FAILED
