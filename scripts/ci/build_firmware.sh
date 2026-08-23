#!/usr/bin/env bash
# Il firmware compila da zero con la toolchain fissata. Niente hardware:
# e' una compilazione, non un flash.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
IDF_PATH="${IDF_PATH:-$HOME/esp/esp-idf}"

if [[ ! -f "$IDF_PATH/export.sh" ]]; then
  echo "ESP-IDF non trovato in $IDF_PATH"
  echo "installa con: ./scripts/bootstrap.sh --only idf"
  exit 1
fi
# shellcheck disable=SC1091
set +u; . "$IDF_PATH/export.sh" >/dev/null; set -u

cd "$ROOT/firmware/esp32"
rm -rf build
idf.py --ccache set-target esp32s3 >/dev/null
idf.py --ccache build
SIZE=$(idf.py size 2>/dev/null | grep -i 'Total image size' || true)
echo "OK — firmware compilato da zero. $SIZE"
