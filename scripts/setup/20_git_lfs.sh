#!/usr/bin/env bash
# GATE 0 — Git LFS. Senza questo, .gitattributes e' inerte e il primo export
# CAD entra in history come binario grezzo, per sempre.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if ! git lfs version >/dev/null 2>&1; then
  case "$(uname -s)" in
    Linux)
      apt_install git-lfs || true
      if ! git lfs version >/dev/null 2>&1; then
        warn "git-lfs non presente nei repository apt configurati, uso lo script ufficiale"
        curl -fsSL https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | $SUDO bash
        apt_install git-lfs
      fi
      ;;
    Darwin)
      if command -v brew >/dev/null 2>&1; then
        brew install git-lfs
      else
        die "installa Homebrew oppure git-lfs a mano: https://git-lfs.com"
      fi
      ;;
    *) die "piattaforma non gestita per l'installazione di git-lfs" ;;
  esac
fi

git lfs install --skip-repo >/dev/null
git -C "$ROOT" lfs install --local >/dev/null
ok "git-lfs: $(git lfs version | head -1)"

git -C "$ROOT" lfs pull 2>/dev/null || warn "git lfs pull non eseguito (nessun remoto o nessun oggetto)"

bash "$ROOT/scripts/ci/check_lfs.sh" || die "gate 0 non passato"
