# Workspace ROS 2 — Jazzy

Ubuntu 24.04 + ROS 2 Jazzy (PROJECT.md §6). Lo scheletro e i contratti sono di
`software-platform`; il contenuto di ogni pacchetto e' del ruolo dichiarato nel
suo `package.xml` (`<r2s_owner>`).

## Costruire

```bash
./scripts/bootstrap.sh     # la prima volta: fa tutto, da zero
make build                 # le volte successive
source install/setup.bash
```

## Pacchetti

| Pacchetto | Tipo | Owner del contenuto | Ruolo nel sistema |
|---|---|---|---|
| `r2s_interfaces` | ament_cmake | software-platform | Contratti di messaggio fra i ruoli. Cambiarli e' una decisione (§3). |
| `r2s_vision` | ament_python | vision-perception | Camera global shutter, YOLO11 su Hailo, `DetectionEvent` |
| `r2s_acoustic` | ament_python | acoustic-perception | Microfono I2S, FFT, classificatore, `AcousticEvent` |
| `r2s_navigation` | ament_python | autonomy | Nav2, slam_toolbox, docking, recupero |
| `r2s_mqtt_bridge` | ament_python | software-platform | Confine verso Home Assistant (§6) |
| `r2s_bringup` | ament_cmake | software-platform | Avvio integrato Unita' A / Unita' B |

I nodi presenti sono **scheletri**: dichiarano i parametri e non fanno lavoro
utile. Sostituiscili, non aggirarli creando un pacchetto parallelo.

## Regole che la CI fa rispettare

- **Le mappe SLAM non entrano nel repository.** Sono la planimetria
  dell'abitazione. `maps/`, `*.pgm`, `*.posegraph` sono bloccati sia da
  `.gitignore` sia da `scripts/ci/check_hygiene.py`.
- **L'audio grezzo non entra.** Nei messaggi viaggiano feature aggregate.
- **I pesi dei modelli non entrano.** Stanno in `models/MANIFEST.yaml` con
  sorgente e sha256, si scaricano con `make models`.
- **Un cambio ai contratti in `r2s_interfaces` richiede una riga nel Decision
  Log** (§3): tre consumatori dipendono da quei tipi.

## Aggiungere un pacchetto

1. `src/r2s_<nome>/` con `package.xml` che dichiara `<r2s_owner>`
2. dipendenze dichiarate in `package.xml` (le installa `rosdep`, non le mani)
3. almeno uno smoke test in `test/` marcato `ci` — deve girare senza hardware
4. se cambia un contratto o l'architettura: riga nel Decision Log
