# Fascicolo · `software-platform`

**Ambito:** Trasversale · **Entra in:** Fase 0 · bloccante F1

**Mandato:** [`.claude/agents/software-platform.md`](../../../.claude/agents/software-platform.md)

## Ruolo

La base software che tutti consumano e nessuno costruiva: workspace ROS 2, riproducibilità, CI, harness dei criteri di FATTO, Git LFS, integrazione MQTT.

## Criterio di FATTO

Git LFS operativo prima di ogni export CAD · da git clone a workspace compilato in ≤30 min con un comando, provato 2 volte su ambiente vergine · CI che rifiuta pesi, dataset e STEP fuori LFS, 4/4 controlli provati

## Consegnato

| Cosa | Dove |
|---|---|
| Workspace ROS 2, 6 pacchetti | `software/ros2_ws/src/` |
| CI e controlli di igiene | `.github/workflows/` |
| Harness dei criteri di FATTO | `scripts/fatto.sh`, `tests/fatto/` |
| Contratto MQTT | `docs/interfaces/MQTT.md` |
| Piattaforma e riproducibilità | `docs/PLATFORM.md` |

## Misure prodotte

*Nessuna.*

## Blocchi

- ⚠ git-lfs non installato (A-02) — gate 0 non superabile
- Riproducibilità non verificabile su macOS

## Verbali in cui è parte

*Nessuno.*

## Cronologia

| Data | Attività | Esito |
|---|---|---|
| 2026-08-23 | Base software | consegnato, in verifica |
