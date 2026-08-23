#!/usr/bin/env bash
# 0 mappe SLAM, riprese di interni, audio o credenziali NELLA HISTORY.
# Non guarda il worktree: guarda tutti i percorsi mai esistiti in un commit.
# E' il controllo che compliance-safety esegue prima di ogni gate.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

PATTERN='\.(pgm|posegraph|pbstream|wav|flac|mp3|ogg|m4a|aac|mp4|mov|mkv|pem|p12|pfx)$|(^|/)(datasets|maps|slam_maps|recordings|capture)/|(^|/)(\.env|secrets\.ya?ml|credentials\.json|id_rsa)$'

echo "Scansione della history: materiale privato mai committato?"
HITS=$(git log --all --pretty=format: --name-only --diff-filter=A \
       | sed '/^$/d' | sort -u | grep -aE "$PATTERN" \
       | grep -v '^tests/fixtures/audio/.*\.synth\.wav$' || true)

if [[ -z "$HITS" ]]; then
  echo "OK — 0 file di materiale privato presenti nella history"
  exit 0
fi

echo
echo "FALLITO — materiale privato trovato in history:"
echo "$HITS" | sed 's/^/  /'
cat <<'MSG'

NON rimuoverlo con un commit successivo: da Git la history non si cancella
davvero e il file resta recuperabile da chiunque abbia un clone.

Procedura: fermati, avvisa il chief-engineer, e si valuta un rewrite della
history (git filter-repo) con reclone obbligatorio per tutti.
Se si tratta di credenziali: REVOCALE subito, sono gia' compromesse.
MSG
exit 1
