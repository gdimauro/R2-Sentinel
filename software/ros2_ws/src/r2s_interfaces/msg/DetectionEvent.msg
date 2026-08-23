# Rilevamento visivo prodotto da r2s_vision (fase 3-4).
# Owner del contenuto: vision-perception. Owner del contratto: software-platform.

builtin_interfaces/Time stamp
string   frame_id          # frame ottico della camera
string   label             # "pigeon" | "unknown"
float32  confidence        # 0.0 - 1.0
# Bounding box in pixel, origine in alto a sinistra
uint16   bbox_x
uint16   bbox_y
uint16   bbox_w
uint16   bbox_h
# Bersaglio in coordinate angolari testa pan-tilt, gradi.
# NaN se la calibrazione non e' disponibile: non inventare uno zero.
float32  bearing_pan_deg
float32  bearing_tilt_deg
float32  range_m           # stima, NaN se non disponibile
