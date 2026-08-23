#!/usr/bin/env python3
"""0 topic MQTT non documentati.

Cerca nel codice ogni stringa che assomiglia a un topic del progetto e verifica
che corrisponda a una voce di topics.yaml. Il contrario di "documentare dopo":
se il topic non e' nello schema, la CI non lo lascia passare.

Uso: check_mqtt_topics.py [--root PATH]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml

TOPIC_LITERAL = re.compile(r"""["']((?:r2sentinel|homeassistant)/[^"'\s]*)["']""")
SCAN_SUFFIXES = {".py", ".c", ".cpp", ".h", ".hpp", ".yaml", ".yml", ".json", ".sh"}
SKIP_DIRS = {".git", "build", "install", "log", ".venv", "node_modules", "graft",
             "__pycache__", "artifacts", "reports"}


def to_regex(pattern: str) -> re.Pattern:
    """`r2sentinel/{site_id}/{unit_id}/status` -> regex con segmenti liberi."""
    out = []
    for part in pattern.split("/"):
        if "{" in part:
            out.append(re.sub(r"\{[a-z_]+\}", "[^/]+", re.escape(part)
                              .replace(r"\{", "{").replace(r"\}", "}")))
        else:
            out.append(re.escape(part))
    return re.compile("^" + "/".join(out) + "$")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    a = ap.parse_args()
    root = pathlib.Path(a.root or pathlib.Path(__file__).resolve().parents[2])
    schema = root / "software/ros2_ws/src/r2s_mqtt_bridge/config/topics.yaml"
    doc = yaml.safe_load(schema.read_text())
    known = [(t["topic"], to_regex(t["topic"])) for t in doc["topics"]]

    found: dict[str, list[str]] = {}
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix not in SCAN_SUFFIXES:
            continue
        if SKIP_DIRS & set(p.relative_to(root).parts):
            continue
        if p.resolve() == schema.resolve():
            continue
        try:
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        for m in TOPIC_LITERAL.finditer(text):
            found.setdefault(m.group(1), []).append(str(p.relative_to(root)))

    unknown = {t: locs for t, locs in found.items()
               if not any(rx.match(t) for _, rx in known)}

    print(f"Topic MQTT: {len(known)} documentati, {len(found)} usati nel codice")
    if not unknown:
        print("OK — 0 topic non documentati")
        return 0
    print(f"\nFALLITO — {len(unknown)} topic non presenti in topics.yaml:")
    for t, locs in sorted(unknown.items()):
        print(f"  {t}\n        usato in: {', '.join(sorted(set(locs)))}")
    print("\nAggiungi il topic a "
          "software/ros2_ws/src/r2s_mqtt_bridge/config/topics.yaml e rigenera la "
          "documentazione con `make mqtt-docs`. Lo schema e' la sorgente, non il codice.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
