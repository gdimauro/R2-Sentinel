#!/usr/bin/env bash
# Toolchain ESP-IDF per ESP32-S3 (micro-ROS, D-06).
# L'SDK vive FUORI dal repository: ~4 GB fra sorgenti e toolchain non hanno
# nulla da fare in un repo di progetto. La versione e' fissata: una toolchain
# "l'ultima disponibile" non e' riproducibile.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

IDF_VERSION="$(grep -E '^idf_version:' "$ROOT/firmware/toolchain.yaml" | awk '{print $2}')"
IDF_TARGETS="$(grep -E '^targets:' "$ROOT/firmware/toolchain.yaml" | cut -d' ' -f2-)"
IDF_PATH="${IDF_PATH:-$HOME/esp/esp-idf}"

if [[ -d "$IDF_PATH/.git" ]]; then
  CURRENT="$(git -C "$IDF_PATH" describe --tags --abbrev=0 2>/dev/null || echo '?')"
  if [[ "$CURRENT" == "$IDF_VERSION" ]]; then
    skip "ESP-IDF $IDF_VERSION gia' presente in $IDF_PATH"
  else
    warn "ESP-IDF presente ma su $CURRENT, attesa $IDF_VERSION: riallineo"
    git -C "$IDF_PATH" fetch --depth 1 origin "refs/tags/$IDF_VERSION:refs/tags/$IDF_VERSION"
    git -C "$IDF_PATH" checkout -q "$IDF_VERSION"
    git -C "$IDF_PATH" submodule update --init --recursive --depth 1
  fi
else
  mkdir -p "$(dirname "$IDF_PATH")"
  echo "    clono ESP-IDF $IDF_VERSION (alcuni minuti, ~1,5 GB)"
  git clone -q --depth 1 --branch "$IDF_VERSION" --recursive \
      https://github.com/espressif/esp-idf.git "$IDF_PATH"
  ok "ESP-IDF $IDF_VERSION clonato in $IDF_PATH"
fi

"$IDF_PATH/install.sh" $IDF_TARGETS >/dev/null
ok "toolchain installata per: $IDF_TARGETS"

# Riga di ambiente riproducibile: chi apre una shell nuova non deve indovinare.
MARK="# R2-Sentinel ESP-IDF"
if ! grep -q "$MARK" "$HOME/.bashrc" 2>/dev/null; then
  {
    echo ""
    echo "$MARK"
    echo "export IDF_PATH=\"$IDF_PATH\""
    echo "alias get_idf='. \"\$IDF_PATH/export.sh\"'"
  } >> "$HOME/.bashrc"
  ok "aggiunto IDF_PATH e alias get_idf a ~/.bashrc"
fi
