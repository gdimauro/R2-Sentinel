#!/usr/bin/env bash
# =============================================================================
# 0 file binari > 5 MB nella history fuori da Git LFS.
#
# Rieseguibile: scandisce TUTTI gli oggetti raggiungibili, non solo HEAD.
# Un file grosso rimosso con un commit successivo resta negli oggetti: e'
# esattamente il caso che questo script deve trovare.
#
# Uso: scripts/ci/check_history_binaries.sh [soglia_MB]
# =============================================================================
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"
LIMIT_MB="${1:-5}"
LIMIT=$((LIMIT_MB * 1024 * 1024))
cd "$ROOT"

echo "Scansione history: oggetti > ${LIMIT_MB} MB non-LFS"

TMP="$(mktemp)"; trap 'rm -f "$TMP"' EXIT

# blob -> dimensione -> percorso (l'ultimo percorso noto per quell'oggetto)
git rev-list --objects --all 2>/dev/null \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk -v lim="$LIMIT" '$1=="blob" && $3>lim {print $2, $3, $4}' > "$TMP"

COUNT=0
while read -r sha size path; do
  [[ -z "${sha:-}" ]] && continue
  head=$(git cat-file -p "$sha" 2>/dev/null | head -c 45)
  if [[ "$head" == "version https://git-lfs.github.com/spec/v1" ]]; then
    continue   # puntatore LFS: legittimo
  fi
  printf '  FAIL  %8.1f MB  %s  (%s)\n' "$(echo "$size" | awk '{print $1/1048576}')" "${path:-<orfano>}" "${sha:0:12}"
  COUNT=$((COUNT + 1))
done < "$TMP"

echo
if [[ $COUNT -eq 0 ]]; then
  echo "OK — 0 binari > ${LIMIT_MB} MB fuori da LFS nella history"
  exit 0
fi
echo "FALLITO — $COUNT oggetti oltre soglia fuori da LFS."
echo "Un commit di rimozione NON li toglie dalla history: serve un rewrite"
echo "(git filter-repo) concordato con il chief-engineer, e tutti i cloni"
echo "esistenti vanno rifatti. Prima di procedere, avvisa."
exit 1
