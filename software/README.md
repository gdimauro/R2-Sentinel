# software/

| Directory | Contenuto | Owner |
|---|---|---|
| `ros2_ws/` | Workspace ROS 2 Jazzy, i sei pacchetti `r2s_*` | vedi tabella nel suo README |
| `vision/` | Strumenti di visione fuori da ROS: training, export HEF, valutazione | vision-perception |
| `acoustic/` | DSP e dataset notturno: indice, annotazioni, classificatore | acoustic-perception |

Tutto cio' che serve per costruire e verificare sta in `Makefile` e in
`scripts/`. Vedi [docs/PLATFORM.md](../docs/PLATFORM.md).

**Non committare**: pesi (`*.pt`, `*.onnx`, `*.hef`), dataset, mappe SLAM,
audio, credenziali. La CI fa fallire la PR, ma la history non si ripulisce dopo.
