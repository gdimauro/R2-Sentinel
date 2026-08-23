# Evento acustico prodotto da r2s_acoustic (fase 5).
# Owner del contenuto: acoustic-perception.
# NOTA PRIVACY: questo messaggio trasporta SOLO feature aggregate.
# Non trasporta mai audio grezzo: l'audio di interni non lascia il dispositivo
# (SAFETY.md, CONTRIBUTING.md §Privacy).

builtin_interfaces/Time stamp
string   label                  # "mosquito" | "background"
float32  confidence             # 0.0 - 1.0
float32  fundamental_hz         # fondamentale stimata, banda attesa 400-600 Hz (D-04)
float32[] harmonics_hz          # armoniche identificate
float32  snr_db                 # rapporto segnale/rumore sulla banda utile
float32  fan_overlap_db         # sovrapposizione con lo spettro ventola (§10)
