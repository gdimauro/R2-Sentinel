"""Esempio di prova DA BANCO — modello per gli altri agenti.

Copia questo schema: marcatore `bench` + marcatore `hardware(<dispositivo>)`,
misura numerica, soglia presa dal registro dei criteri di FATTO.

In CI questo test viene SALTATO e il motivo compare nel report. Non fallisce e
non passa: dice la verita', cioe' che non e' stato eseguito.
"""
from __future__ import annotations

import pathlib

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]


def soglia(criterio_id: str):
    reg = yaml.safe_load((ROOT / "tests/fatto/registry.yaml").read_text())
    c = next(x for x in reg["criteria"] if x["id"] == criterio_id)
    return c["metric"]


@pytest.mark.bench
@pytest.mark.hardware("esp32")
def test_esempio_misura_da_banco():
    m = soglia("mech-g2-loop-jitter")
    # misura = leggi_jitter_da_analizzatore()
    misura = None
    assert misura is not None, "misura non acquisita"
    assert misura <= m["target"], f"jitter {misura} {m['unit']} > {m['target']}"


@pytest.mark.ci
def test_soglie_leggibili_dal_registro():
    """Questo invece gira ovunque: verifica che il registro sia usabile."""
    m = soglia("mech-g2-loop-jitter")
    assert m["target"] == 100 and m["unit"] == "us"
