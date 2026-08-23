#!/usr/bin/env bash
# Funzioni condivise dai passi di bootstrap.
set -euo pipefail

ok()   { printf '    [ok]   %s\n' "$*"; }
skip() { printf '    [skip] %s\n' "$*"; }
warn() { printf '    [warn] %s\n' "$*"; }
die()  { printf '    [FAIL] %s\n' "$*"; exit 1; }

SUDO=""
if [[ $EUID -ne 0 ]]; then
  if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; fi
fi
sudo_available() { [[ -n "$SUDO" || $EUID -eq 0 ]]; }

require_ubuntu_2404() {
  [[ -f /etc/os-release ]] || die "non e' un sistema Linux con /etc/os-release"
  . /etc/os-release
  if [[ "${ID:-}" != "ubuntu" || "${VERSION_ID:-}" != "24.04" ]]; then
    warn "atteso Ubuntu 24.04 (PROJECT.md §6), trovato ${PRETTY_NAME:-sconosciuto}"
    warn "proseguo, ma il risultato non e' quello verificato in CI"
  fi
}

APT_UPDATED=0
apt_install() {
  local missing=()
  for p in "$@"; do
    dpkg -s "$p" >/dev/null 2>&1 || missing+=("$p")
  done
  if [[ ${#missing[@]} -eq 0 ]]; then skip "pacchetti apt gia' presenti"; return 0; fi
  if [[ $APT_UPDATED -eq 0 ]]; then $SUDO apt-get update -qq; APT_UPDATED=1; fi
  echo "    installo: ${missing[*]}"
  DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -qq --no-install-recommends "${missing[@]}"
}

repo_root() { cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd; }
