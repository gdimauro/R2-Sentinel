#!/usr/bin/env python3
"""Genera docs/interfaces/MQTT.md da topics.yaml.

Il documento non si scrive a mano: si rigenera. `design-docs` lo CONSUMA
(D-15: gli artefatti automatici si consumano, non si trascrivono).

Uso:
    python3 scripts/gen/gen_mqtt_docs.py            # scrive il file
    python3 scripts/gen/gen_mqtt_docs.py --check    # fallisce se e' obsoleto
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "software/ros2_ws/src/r2s_mqtt_bridge/config/topics.yaml"
OUT = ROOT / "docs/interfaces/MQTT.md"

HEADER = """<!-- FILE GENERATO — NON MODIFICARE A MANO.
     Sorgente: software/ros2_ws/src/r2s_mqtt_bridge/config/topics.yaml
     Rigenera con: make mqtt-docs
     La CI fallisce se questo file diverge dalla sorgente. -->

# Interfaccia MQTT — R2-Sentinel

Il livello MQTT e' il **confine fra le due unita' e il mondo** (PROJECT.md §6).
Schema, payload e comportamento in caduta del broker sono definiti **una volta
sola**, nella sorgente citata sopra, e non vanno reinventati da ogni specialista.

- Latenza massima di pubblicazione dello stato: **{lat} s**
- Riconnessione automatica dopo caduta del broker: **<= {rec} s**
- Verifica: `./scripts/fatto.sh software-platform mqtt`

"""


def build(doc: dict) -> str:
    c = doc["conventions"]
    b = doc["broker"]
    out = [HEADER.format(lat=c["time_budget"]["status_max_latency_s"],
                         rec=c["time_budget"]["reconnect_max_s"])]

    out.append("## Convenzioni\n")
    out.append(f"- Pattern: `{c['pattern']}`\n")
    out.append(f"- Unita': {', '.join('`%s`' % u for u in c['units'])}\n")
    out.append(f"- Codifica: {c['encoding']}\n")
    out.append(f"- Versione di schema dei payload: `{doc['schema_version']}`\n\n")

    out.append("### Campi obbligatori in ogni payload JSON\n\n")
    out.append("| Campo | Significato |\n|---|---|\n")
    for k, v in c["mandatory_payload_fields"].items():
        out.append(f"| `{k}` | {v} |\n")
    out.append("\n### Cosa non puo' MAI comparire in un payload\n\n")
    for f in c["forbidden_payload_content"]:
        out.append(f"- {f}\n")
    out.append("\nNon e' una raccomandazione: e' il vincolo di privacy di "
               "`CONTRIBUTING.md` e `SAFETY.md` applicato al bus.\n\n")

    out.append("## Topic\n\n")
    out.append("| Topic | Dir. | QoS | Retain | Sorgente ROS 2 | Frequenza |\n")
    out.append("|---|---|---|---|---|---|\n")
    for t in doc["topics"]:
        out.append("| `{topic}` | {d} | {q} | {r} | {s} | {rate} |\n".format(
            topic=t["topic"], d="pub" if t["direction"] == "publish" else "sub",
            q=t["qos"], r="si" if t["retain"] else "no",
            s=t["ros_source"], rate=t["rate"]))

    out.append("\n### Payload per topic\n\n")
    for t in doc["topics"]:
        out.append(f"#### `{t['topic']}`\n\n")
        out.append(f"{t['purpose']}\n\n")
        out.append(f"```\n{t['payload'].strip()}\n```\n\n")

    out.append("## Comportamento in caduta del broker\n\n")
    d = b["disconnect_behaviour"]
    lw = d["last_will"]
    out.append(f"- **Last Will**: `{lw['topic']}` -> `{lw['payload']}` "
               f"(retain={'si' if lw['retain'] else 'no'}, QoS {lw['qos']}). "
               "Home Assistant vede l'unita' non disponibile invece di mostrare "
               "l'ultimo valore buono come se fosse attuale.\n")
    out.append(f"- **Backoff di riconnessione** (secondi): "
               f"{', '.join(str(x) for x in d['reconnect_backoff_s'])} "
               f"(+ jitter {d['reconnect_jitter_s']} s). Il cap coincide con il "
               "criterio di riconnessione.\n")
    q = d["queue"]
    out.append(f"- **Coda eventi**: ring buffer da {q['events_max']} elementi in RAM, "
               f"persistenza su disco: {'si' if q['persist_to_disk'] else 'no'}.\n")
    out.append(f"- **Comandi in ingresso**: non vengono accodati "
               f"(`commands_queued={q['commands_queued']}`) e vengono scartati se "
               f"piu' vecchi di {q['command_max_age_s']} s. Un comando eseguito in "
               "ritardo su un attuatore fisico e' un rischio, non un servizio.\n")
    out.append(f"- **Alla riconnessione**: {d['on_reconnect']}.\n")

    out.append("\n## Credenziali\n\n")
    out.append("Le credenziali **non stanno nel repository**. Il bridge le legge da "
               f"{' e '.join('`%s`' % e for e in b['credentials_env'])}. "
               "Un file di credenziali committato fa fallire la CI "
               "(`scripts/ci/check_hygiene.py`).\n")
    return "".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="non scrive: esce 1 se il file generato e' obsoleto")
    a = ap.parse_args()
    doc = yaml.safe_load(SRC.read_text())
    new = build(doc)
    if a.check:
        old = OUT.read_text() if OUT.exists() else ""
        if old != new:
            print("FAIL: docs/interfaces/MQTT.md non e' allineato a topics.yaml.\n"
                  "      Rigeneralo con: make mqtt-docs", file=sys.stderr)
            return 1
        print("OK: MQTT.md allineato alla sorgente")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(new)
    print(f"scritto {OUT.relative_to(ROOT)} ({len(doc['topics'])} topic)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
