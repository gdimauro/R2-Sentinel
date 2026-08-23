# Fascicolo · `acoustic-perception`

**Ambito:** Unità B · **Entra in:** Fase 1

**Mandato:** [`.claude/agents/acoustic-perception.md`](../../../.claude/agents/acoustic-perception.md)

## Ruolo

Firma spettrale del battito alare, FFT, classificatore. E il dataset notturno, vincolato dal calendario.

## Criterio di FATTO

≥20 notti utili da ≥6 h con metadati, di cui ≥5 negative di controllo · recall ≥0,90 · ≤1 falso positivo/ora

## Consegnato

| Cosa | Dove |
|---|---|
| Registratore notturno | `software/acoustic/registratore.py` |
| Analisi spettrale 300–800 Hz | `software/acoustic/spettro.py`, `dsp.py` |
| Schema metadati e indice dataset | `software/acoustic/metadati.py`, `indice.py` |

## Misure prodotte

| Grandezza | Valore | Data | Natura |
|---|---|---|---|
| Notti registrate | **0 / 20** | 2026-08-24 | contatore |

## Blocchi

- ⚠ Microfono non ordinato (A-01) — 12 giorni alla scadenza
- Da separare: latenza di avvio contro gap da riavvio (VRB-2026-0006)

## Verbali in cui è parte

- [VRB-2026-0006](../../verbali/VRB-2026-0006.md)

## Cronologia

| Data | Attività | Esito |
|---|---|---|
| 2026-08-23 | Catena di registrazione | consegnato, in verifica |
