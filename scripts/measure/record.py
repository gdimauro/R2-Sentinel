#!/usr/bin/env python3
"""Registrazione di una misura fatta a mano, con verifica automatica della soglia.

Serve ai criteri di FATTO che nessuno strumento puo' eseguire da solo (warping
di un provino, particelle su un foglio, allontanamento di un piccione). La
misura la fa una persona; la soglia la verifica questo comando, e il dato
finisce in un file versionato con data e operatore.

    scripts/measure/record.py --criterio mech-g0-warping --valore 0.22 --note "provino 3"
    scripts/measure/record.py --criterio mech-g0-warping           # rilegge e valuta

Le misure stanno in measurements/<criterio>.yaml: testo, diffabile, revisionabile.
Un numero senza data e senza operatore non e' una misura, e' un ricordo.
"""
from __future__ import annotations
import argparse, datetime, getpass, pathlib, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
REG = yaml.safe_load((ROOT / "tests/fatto/registry.yaml").read_text())
OUT = ROOT / "measurements"


def evaluate(metric: dict, value: float) -> bool:
    op, t = metric.get("op"), metric.get("target")
    if op == "<=":  return value <= t
    if op == "<":   return value < t
    if op == ">=":  return value >= t
    if op == ">":   return value > t
    if op == "==":  return value == t
    if op == "in":  return t[0] <= value <= t[1]
    raise SystemExit(f"operatore non gestito nel registro: {op}")


ap = argparse.ArgumentParser()
ap.add_argument("--criterio", required=True)
ap.add_argument("--valore", type=float)
ap.add_argument("--note", default="")
ap.add_argument("--operatore", default=None)
a = ap.parse_args()

crit = next((c for c in REG["criteria"] if c["id"] == a.criterio), None)
if crit is None:
    sys.exit(f"criterio sconosciuto: {a.criterio}")
metric = crit.get("metric", {})

OUT.mkdir(exist_ok=True)
f = OUT / f"{a.criterio}.yaml"
data = yaml.safe_load(f.read_text()) if f.exists() else {
    "criterio": a.criterio, "ruolo": crit["role"],
    "descrizione": crit["criterio"], "metrica": metric, "misure": []}

if a.valore is not None:
    data["misure"].append({
        "valore": a.valore, "unita": metric.get("unit"),
        "data": datetime.datetime.now().isoformat(timespec="seconds"),
        "operatore": a.operatore or getpass.getuser(),
        "note": a.note})
    f.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
    print(f"registrata: {a.valore} {metric.get('unit','')} in {f.relative_to(ROOT)}")

if not data["misure"]:
    print(f"NON MISURATO — {a.criterio}: nessuna misura registrata.")
    print(f"Soglia attesa: {metric.get('name')} {metric.get('op')} {metric.get('target')}")
    print("Registra con: --valore <numero>")
    sys.exit(1)

vals = [m["valore"] for m in data["misure"]]
ok = [v for v in vals if evaluate(metric, v)]
print(f"{a.criterio}: {len(vals)} misure, {len(ok)} entro soglia "
      f"({metric.get('name')} {metric.get('op')} {metric.get('target')} {metric.get('unit','')})")
for m in data["misure"][-5:]:
    esito = "OK  " if evaluate(metric, m["valore"]) else "FUORI"
    print(f"  {esito} {m['valore']:>8} {m['data']}  {m['operatore']}  {m['note']}")
if len(ok) != len(vals):
    print("\nFALLITO — almeno una misura e' fuori soglia. Non arrotondare: "
          "riporta il fallimento con la causa isolata.")
    sys.exit(1)
