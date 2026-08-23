<!-- FILE GENERATO — NON MODIFICARE A MANO.
     Sorgente: software/ros2_ws/src/r2s_mqtt_bridge/config/topics.yaml
     Rigenera con: make mqtt-docs
     La CI fallisce se questo file diverge dalla sorgente. -->

# Interfaccia MQTT — R2-Sentinel

Il livello MQTT e' il **confine fra le due unita' e il mondo** (PROJECT.md §6).
Schema, payload e comportamento in caduta del broker sono definiti **una volta
sola**, nella sorgente citata sopra, e non vanno reinventati da ogni specialista.

- Latenza massima di pubblicazione dello stato: **2.0 s**
- Riconnessione automatica dopo caduta del broker: **<= 30.0 s**
- Verifica: `./scripts/fatto.sh software-platform mqtt`

## Convenzioni
- Pattern: `r2sentinel/{site_id}/{unit_id}/{group}[/{name}]`
- Unita': `unit_a`, `unit_b`
- Codifica: UTF-8 JSON, chiavi snake_case
- Versione di schema dei payload: `1`

### Campi obbligatori in ogni payload JSON

| Campo | Significato |
|---|---|
| `schema_version` | int, uguale a schema_version di questo file |
| `ts` | string ISO-8601 UTC con suffisso Z, orologio del dispositivo |
| `unit` | string, uno di units |
| `seq` | int monotono crescente per topic, riparte da 0 al riavvio |

### Cosa non puo' MAI comparire in un payload

- audio grezzo o suoi campioni (PRIVACY: audio di interni)
- immagini o crop di interni (PRIVACY)
- mappe SLAM o coordinate assolute della planimetria (PRIVACY)
- credenziali di qualsiasi tipo

Non e' una raccomandazione: e' il vincolo di privacy di `CONTRIBUTING.md` e `SAFETY.md` applicato al bus.

## Topic

| Topic | Dir. | QoS | Retain | Sorgente ROS 2 | Frequenza |
|---|---|---|---|---|---|
| `r2sentinel/{site_id}/{unit_id}/availability` | pub | 1 | si | -- (gestito dal client MQTT: LWT + publish a connessione) | a ogni cambio di stato di connessione |
| `r2sentinel/{site_id}/{unit_id}/status` | pub | 1 | si | r2s_interfaces/msg/UnitStatus su /r2s/status | a ogni cambio di stato, e comunque ogni 5 s (heartbeat) |
| `r2sentinel/{site_id}/{unit_id}/event/detection` | pub | 1 | no | r2s_interfaces/msg/DetectionEvent su /r2s/detection | a evento, throttling a 5 Hz |
| `r2sentinel/{site_id}/{unit_id}/event/acoustic` | pub | 1 | no | r2s_interfaces/msg/AcousticEvent su /r2s/acoustic | a evento, throttling a 2 Hz |
| `r2sentinel/{site_id}/{unit_id}/payload/state` | pub | 1 | si | r2s_interfaces/srv/TriggerPayload (esito) + stato interno | a ogni attivazione o inibizione |
| `r2sentinel/{site_id}/{unit_id}/telemetry/battery` | pub | 0 | si | sensor_msgs/msg/BatteryState su /r2s/battery | 0,2 Hz |
| `r2sentinel/{site_id}/{unit_id}/cmd/arm` | sub | 1 | no | -> std_srvs/srv/SetBool interno | su comando dell'utente |
| `r2sentinel/{site_id}/{unit_id}/cmd/payload` | sub | 1 | no | -> r2s_interfaces/srv/TriggerPayload | su comando dell'utente |
| `homeassistant/{component}/r2s_{unit_id}_{object_id}/config` | pub | 1 | si | -- (generato dal bridge all'avvio) | una volta all'avvio e a ogni riconnessione |

### Payload per topic

#### `r2sentinel/{site_id}/{unit_id}/availability`

Home Assistant marca l'entita' non disponibile senza inventare valori.

```
stringa: online | offline
```

#### `r2sentinel/{site_id}/{unit_id}/status`

Stato sintetico dell'unita'. E' il topic su cui si misura la latenza <=2 s.

```
{schema_version, ts, unit, seq, state, state_name, detail,
 battery_v, battery_soc, events_last_hour}
```

#### `r2sentinel/{site_id}/{unit_id}/event/detection`

Rilevamento piccione. NIENTE immagini nel payload.

```
{schema_version, ts, unit, seq, label, confidence,
 bearing_pan_deg, bearing_tilt_deg, range_m}
```

#### `r2sentinel/{site_id}/{unit_id}/event/acoustic`

Firma zanzara classificata. NIENTE audio nel payload.

```
{schema_version, ts, unit, seq, label, confidence,
 fundamental_hz, harmonics_hz, snr_db, fan_overlap_db}
```

#### `r2sentinel/{site_id}/{unit_id}/payload/state`

Tracciabilita' delle attivazioni del payload. `inhibited` e' la traccia dell'interblocco di sicurezza: se e' true il payload non parte, e si sa perche'.

```
{schema_version, ts, unit, seq, payload_kind, active, last_trigger_ts,
 duration_s, reason, inhibited, inhibit_reason}
```

#### `r2sentinel/{site_id}/{unit_id}/telemetry/battery`

Batteria LiFePO4 (D-07). `chemistry` e' pubblicato ed e' atteso `LiFePO4`: un valore diverso e' un difetto di configurazione da segnalare, non da ignorare.

```
{schema_version, ts, unit, seq, voltage_v, current_a, soc, temperature_c, chemistry}
```

#### `r2sentinel/{site_id}/{unit_id}/cmd/arm`

Arma/disarma l'unita' da Home Assistant. I comandi piu' vecchi di command_max_age_s vengono scartati e loggati, mai eseguiti in ritardo.

```
{schema_version, ts, armed: bool, requested_by: string}
```

#### `r2sentinel/{site_id}/{unit_id}/cmd/payload`

Attivazione manuale del payload. `duration_s` e' OBBLIGATORIO e limitato: non esiste un comando di accensione senza durata (SAFETY.md).

```
{schema_version, ts, payload_kind, duration_s, reason, requested_by}
```

#### `homeassistant/{component}/r2s_{unit_id}_{object_id}/config`

Auto-configurazione delle entita' in Home Assistant senza YAML a mano.

```
discovery Home Assistant, vedi https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery
```

## Comportamento in caduta del broker

- **Last Will**: `r2sentinel/{site_id}/{unit_id}/availability` -> `offline` (retain=si, QoS 1). Home Assistant vede l'unita' non disponibile invece di mostrare l'ultimo valore buono come se fosse attuale.
- **Backoff di riconnessione** (secondi): 1, 2, 4, 8, 16, 30 (+ jitter 0.5 s). Il cap coincide con il criterio di riconnessione.
- **Coda eventi**: ring buffer da 100 elementi in RAM, persistenza su disco: no.
- **Comandi in ingresso**: non vengono accodati (`commands_queued=False`) e vengono scartati se piu' vecchi di 5.0 s. Un comando eseguito in ritardo su un attuatore fisico e' un rischio, non un servizio.
- **Alla riconnessione**: ripubblica availability=online e status retained, poi svuota la coda eventi.

## Credenziali

Le credenziali **non stanno nel repository**. Il bridge le legge da `R2S_MQTT_USER` e `R2S_MQTT_PASS`. Un file di credenziali committato fa fallire la CI (`scripts/ci/check_hygiene.py`).
