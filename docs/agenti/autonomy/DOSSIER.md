# Fascicolo · `autonomy`

**Ambito:** Unità B · **Entra in:** Fase 7 · consultato in F1

**Mandato:** [`.claude/agents/autonomy.md`](../../../.claude/agents/autonomy.md)

## Ruolo

ROS 2 Jazzy, Nav2, slam_toolbox, fusione LIDAR/ToF/IMU, docking. Entra in fase 1 per consegnare i vincoli prima che il telaio si congeli.

## Criterio di FATTO

20/20 agganci al dock entro ±5 mm e ±3° · SLAM ≥60 m² con chiusura d'anello ≤10 cm · 0 collisioni e 0 cadute su 2 h

## Consegnato

| Cosa | Dove |
|---|---|
| Vincoli meccanici della base mobile | `docs/interfaces/VINCOLI-BASE-MOBILE.md` |

## Misure prodotte

| Grandezza | Valore | Data | Natura |
|---|---|---|---|
| Braccio di stabilità con 1 pazza | **40–90 mm (non 150)** | 2026-08-23 | calcolato, verificato dal coordinamento |
| Spinta che rovescia il robot | **530–900 g a 1,15 m** | 2026-08-23 | calcolato, verificato |
| Trazione del 30:1 contro soglia 15 mm | **33 N contro 51 richiesti** | 2026-08-23 | calcolato, verificato |

## Blocchi

- Rilievo dell'abitazione mancante (A-18)
- Decisione sul montante da 120 cm (A-17)

## Verbali in cui è parte

- [VRB-2026-0005](../../verbali/VRB-2026-0005.md)

## Cronologia

| Data | Attività | Esito |
|---|---|---|
| 2026-08-23 | Vincoli del telaio | consegnato con 3 contestazioni |
