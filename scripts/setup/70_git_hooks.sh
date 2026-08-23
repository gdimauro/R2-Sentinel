#!/usr/bin/env bash
# Hook locali. Sono la barriera che agisce PRIMA che il file entri in history:
# la CI arriva dopo, e a quel punto il commit esiste gia' sulla tua macchina.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

git -C "$ROOT" config core.hooksPath scripts/git-hooks
chmod +x "$ROOT"/scripts/git-hooks/* 2>/dev/null || true
ok "core.hooksPath = scripts/git-hooks (versionati, quindi uguali per tutti)"
