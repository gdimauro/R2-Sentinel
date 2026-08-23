#!/usr/bin/env bash
# =============================================================================
# GATE 0 — Git LFS operativo.
#
# Non verifica un'opinione: verifica che un .step committato diventi davvero un
# puntatore < 200 byte. Se git-lfs non e' installato, .gitattributes e' inerte e
# il primo export CAD entra in history come binario grezzo, per sempre.
#
# Uso:   scripts/ci/check_lfs.sh            verifica ambiente + history
#        scripts/ci/check_lfs.sh --prove    esegue la prova end-to-end in un
#                                           repository temporaneo usa-e-getta
# Uscita: 0 gate passato, 1 gate fallito.
# =============================================================================
set -uo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
FAIL=0
PROVE=0
[[ "${1:-}" == "--prove" ]] && PROVE=1

ok()   { printf '  OK    %s\n' "$1"; }
bad()  { printf '  FAIL  %s\n' "$1"; FAIL=1; }
info() { printf '        %s\n' "$1"; }

echo "GATE 0 — Git LFS"

# 1. binario presente ---------------------------------------------------------
if command -v git-lfs >/dev/null 2>&1 || git lfs version >/dev/null 2>&1; then
  ok "git-lfs installato: $(git lfs version 2>/dev/null | head -1)"
else
  bad "git-lfs NON installato"
  info "macOS:  brew install git-lfs && git lfs install"
  info "Ubuntu: sudo apt-get install -y git-lfs && git lfs install"
  info "Finche' manca, .gitattributes e' inerte: NON committare export CAD."
fi

# 2. filtri configurati -------------------------------------------------------
if git config --get filter.lfs.clean >/dev/null 2>&1; then
  ok "filtri lfs configurati (git lfs install eseguito)"
else
  bad "filtri lfs non configurati per questo utente/repo"
  info "esegui: git lfs install"
fi

# 3. .gitattributes instrada gli export CAD -----------------------------------
for ext in step stp stl 3mf f3d; do
  attr=$(git -C "$ROOT" check-attr filter -- "cad/export/prova.$ext" | awk '{print $NF}')
  if [[ "$attr" == "lfs" ]]; then
    ok ".$ext instradato in LFS da .gitattributes"
  else
    bad ".$ext NON instradato in LFS (filter=$attr)"
  fi
done

# 4. nessun export CAD gia' committato come binario grezzo --------------------
BAD_CAD=0
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  head=$(git -C "$ROOT" show "HEAD:$f" 2>/dev/null | head -c 45)
  if [[ "$head" != "version https://git-lfs.github.com/spec/v1" ]]; then
    bad "export CAD in history NON come puntatore LFS: $f"
    BAD_CAD=$((BAD_CAD + 1))
  fi
done < <(git -C "$ROOT" ls-files '*.step' '*.stp' '*.stl' '*.3mf' '*.f3d' '*.STEP' '*.STL' 2>/dev/null)
if [[ $BAD_CAD -eq 0 ]]; then
  ok "0 export CAD binari committati fuori da LFS"
else
  info "NON rimuoverli con un commit successivo: serve un rewrite della history."
  info "Fermati e avvisa il chief-engineer."
fi

# 5. prova end-to-end ---------------------------------------------------------
if [[ $PROVE -eq 1 ]]; then
  echo
  echo "Prova end-to-end su repository temporaneo"
  if ! git lfs version >/dev/null 2>&1; then
    bad "impossibile eseguire la prova: git-lfs assente"
  else
    TMP="$(mktemp -d)"
    trap 'rm -rf "$TMP"' EXIT
    (
      set -e
      cd "$TMP"
      git init -q .
      git config user.email ci@r2-sentinel.local
      git config user.name  "R2S CI"
      git lfs install --local >/dev/null
      cp "$ROOT/.gitattributes" .
      mkdir -p cad/export
      # 1 MB di finto STEP: se entra grezzo, l'oggetto pesa ~1 MB
      head -c 1048576 /dev/urandom | base64 > cad/export/prova_gate0.step
      git add .gitattributes cad/export/prova_gate0.step
      git commit -qm "prova gate 0"
      SIZE=$(git cat-file -s "HEAD:cad/export/prova_gate0.step")
      LISTED=$(git lfs ls-files | grep -c prova_gate0.step || true)
      echo "        oggetto in history: ${SIZE} byte; git lfs ls-files: ${LISTED} voce/i"
      [[ "$LISTED" -ge 1 ]] || { echo "PROVA-FAIL: non elencato da git lfs ls-files"; exit 1; }
      [[ "$SIZE" -lt 200 ]] || { echo "PROVA-FAIL: oggetto di $SIZE byte, atteso < 200"; exit 1; }
    )
    if [[ $? -eq 0 ]]; then
      ok "prova end-to-end superata: puntatore < 200 byte, elencato da git lfs ls-files"
    else
      bad "prova end-to-end fallita"
    fi
  fi
fi

echo
if [[ $FAIL -eq 0 ]]; then
  echo "GATE 0: PASSATO"
else
  echo "GATE 0: NON PASSATO — bloccante per la fase 1 (D-09, export STEP+STL)"
fi
exit $FAIL
