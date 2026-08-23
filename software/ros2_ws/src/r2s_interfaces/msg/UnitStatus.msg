# Stato sintetico di una unita'. E' il messaggio che il bridge MQTT pubblica
# verso Home Assistant (§6). Schema dei topic: docs/interfaces/MQTT.md,
# generato da software/ros2_ws/src/r2s_mqtt_bridge/config/topics.yaml.

builtin_interfaces/Time stamp

uint8 UNIT_A=0        # balcone, fissa pan-tilt
uint8 UNIT_B=1        # interno, mobile
uint8 unit

uint8 STATE_BOOT=0
uint8 STATE_IDLE=1
uint8 STATE_ARMED=2
uint8 STATE_ACTING=3
uint8 STATE_DEGRADED=4
uint8 STATE_FAULT=5
uint8 STATE_SAFE=6    # arresto sicuro, richiede intervento
uint8 state

string   detail            # testo breve, mai dati personali
float32  battery_v         # LiFePO4 (D-07), NaN se alimentata da rete
float32  battery_soc       # 0.0 - 1.0, NaN se non stimabile
uint32   events_last_hour
