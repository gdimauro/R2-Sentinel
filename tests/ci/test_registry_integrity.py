"""Il registro dei criteri di FATTO deve restare coerente.

Se questo test fallisce, il problema non e' un algoritmo: e' che qualcuno ha
aggiunto un criterio senza un modo di eseguirlo, ed e' esattamente la cosa che
l'harness esiste per impedire.
"""
from __future__ import annotations

import pathlib
import re

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
REG = yaml.safe_load((ROOT / "tests/fatto/registry.yaml").read_text())
AGENTS = ROOT / ".claude/agents"


@pytest.mark.ci
def test_ogni_criterio_ha_un_comando():
    senza = [c["id"] for c in REG["criteria"] if not c.get("command")]
    assert not senza, (
        "criteri senza comando eseguibile (vanno segnalati al chief-engineer "
        f"come difetto del mandato): {senza}")


@pytest.mark.ci
def test_id_univoci():
    ids = [c["id"] for c in REG["criteria"]]
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, f"id duplicati: {dup}"


@pytest.mark.ci
def test_campi_obbligatori():
    for c in REG["criteria"]:
        for campo in ("role", "criterio", "kind", "status", "metric"):
            assert campo in c, f"{c['id']}: manca il campo '{campo}'"
        assert c["kind"] in ("ci", "bench", "manual"), c["id"]
        assert c["status"] in ("stub", "implemented"), c["id"]
        assert c["metric"].get("op") in ("<=", "<", ">=", ">", "==", "in"), c["id"]


@pytest.mark.ci
def test_ruoli_esistono_come_agenti():
    for r in REG["roles"]:
        assert (ROOT / r["file"]).exists(), f"file agente mancante: {r['file']}"


@pytest.mark.ci
def test_ogni_ruolo_tecnico_ha_almeno_un_criterio():
    ruoli = {r["id"] for r in REG["roles"]}
    coperti = {c["role"] for c in REG["criteria"]}
    assert ruoli == coperti, f"ruoli senza criteri: {ruoli - coperti}"


@pytest.mark.ci
def test_i_comandi_puntano_a_file_esistenti():
    """Un comando che cita uno script inesistente e' un comando finto.

    Vale solo per i criteri `implemented`: gli stub citano di proposito file
    che l'owner deve ancora scrivere.
    """
    mancanti = []
    for c in REG["criteria"]:
        if c["status"] != "implemented":
            continue
        for tok in re.findall(r"[\w./-]+\.(?:py|sh)", c["command"]):
            if tok.startswith(".venv"):
                continue
            if not (ROOT / tok).exists():
                mancanti.append((c["id"], tok))
    assert not mancanti, f"comandi 'implemented' che citano file inesistenti: {mancanti}"


@pytest.mark.ci
def test_criteri_bench_dichiarano_cosa_serve():
    for c in REG["criteria"]:
        if c["kind"] == "bench":
            assert c.get("requires") or c.get("blocked_by"), (
                f"{c['id']}: prova da banco senza elenco di cio' che serve. "
                "Chi la deve eseguire non puo' indovinarlo.")
