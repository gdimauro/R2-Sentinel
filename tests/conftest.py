"""Regole comuni a tutti i test.

La regola che conta: un test che richiede hardware assente viene SALTATO con il
motivo scritto, mai fallito e mai passato di nascosto.
"""
from __future__ import annotations

import os

import pytest

HW_ENV = {
    "hailo": "R2S_HW_HAILO",
    "esp32": "R2S_HW_ESP32",
    "lidar": "R2S_HW_LIDAR",
    "camera": "R2S_HW_CAMERA",
    "mic": "R2S_HW_MIC",
    "anemometro": "R2S_HW_ANEMOMETRO",
    "broker": "R2S_MQTT_HOST",
}


def pytest_report_header(config):  # noqa: ARG001
    bench = os.environ.get("R2S_BENCH") == "1"
    present = [k for k, e in HW_ENV.items() if os.environ.get(e)]
    return [
        f"R2-Sentinel: banco {'ABILITATO' if bench else 'disabilitato'} "
        f"(R2S_BENCH={'1' if bench else '0'})",
        f"hardware dichiarato presente: {', '.join(present) if present else 'nessuno'}",
    ]


def pytest_collection_modifyitems(config, items):  # noqa: ARG001
    bench_on = os.environ.get("R2S_BENCH") == "1"
    manual_on = os.environ.get("R2S_MANUAL") == "1"
    for item in items:
        if "bench" in item.keywords and not bench_on:
            item.add_marker(pytest.mark.skip(
                reason="prova da banco: serve hardware. Abilita con R2S_BENCH=1"))
        if "manual" in item.keywords and not manual_on:
            item.add_marker(pytest.mark.skip(
                reason="protocollo umano. Abilita con R2S_MANUAL=1"))
        for mark in item.iter_markers(name="hardware"):
            dev = mark.args[0] if mark.args else "?"
            env = HW_ENV.get(dev, f"R2S_HW_{dev.upper()}")
            if not os.environ.get(env):
                item.add_marker(pytest.mark.skip(
                    reason=f"richiede '{dev}': dichiaralo presente con {env}=1"))
