#!/usr/bin/env python3
"""Esecutore dei criteri di FATTO.

Un criterio di FATTO che nessuno sa come rieseguire e' un aneddoto. Questo
runner e' il comando unico con cui ogni ruolo esegue il proprio.

Regole di condotta di questo strumento, in ordine di importanza:

  1. Uno stub non passa mai. Se il test non e' ancora scritto, lo stato e'
     NON IMPLEMENTATO, non "verde". Un verde falso e' peggio di un rosso.
  2. Una prova da banco senza banco viene SALTATA in modo esplicito, con il
     motivo e l'elenco di cio' che manca. Mai fallita in silenzio, mai passata.
  3. Un criterio bloccato da una questione aperta (§10) lo dice.

Uso:
    tests/fatto/runner.py                     tutto cio' che gira senza banco
    tests/fatto/runner.py mechatronics        un ruolo
    tests/fatto/runner.py --id plat-gate0-lfs un criterio
    tests/fatto/runner.py --list              elenco con stato, non esegue
    tests/fatto/runner.py --coverage          copertura per ruolo
    R2S_BENCH=1 tests/fatto/runner.py ...     include le prove da banco
    R2S_MANUAL=1 tests/fatto/runner.py ...    include i protocolli manuali
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
import time

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "tests/fatto/registry.yaml"

C = {
    "PASS": "\033[32m", "FAIL": "\033[31m", "SKIP": "\033[33m",
    "STUB": "\033[35m", "OFF": "\033[0m", "B": "\033[1m",
}
if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    C = {k: "" for k in C}


def load() -> dict:
    return yaml.safe_load(REGISTRY.read_text())


def target(m: dict) -> str:
    t = m.get("target")
    if isinstance(t, list):
        t = f"[{t[0]}, {t[1]}]"
    return f"{m.get('name')} {m.get('op')} {t} {m.get('unit', '')}".strip()


def decide(c: dict, bench: bool, manual: bool, run_stubs: bool) -> tuple[str, str]:
    """Ritorna (azione, motivo). azione: run | skip | stub."""
    if c.get("kind") == "bench" and not bench:
        req = ", ".join(c.get("requires", [])) or "banco di prova"
        return "skip", f"richiede il banco ({req}); R2S_BENCH=1 per eseguirla"
    if c.get("kind") == "manual" and not manual:
        return "skip", "protocollo umano; R2S_MANUAL=1 per registrare la misura"
    if c.get("status") != "implemented" and not run_stubs:
        return "stub", "test non ancora scritto — owner: " + c["role"]
    return "run", ""


def run_one(c: dict, timeout: int) -> tuple[str, float, str]:
    t0 = time.time()
    try:
        p = subprocess.run(["bash", "-c", c["command"]], cwd=ROOT,
                           capture_output=True, text=True, timeout=timeout)
        out = (p.stdout + p.stderr)[-4000:]
        return ("PASS" if p.returncode == 0 else "FAIL"), time.time() - t0, out
    except subprocess.TimeoutExpired:
        return "FAIL", time.time() - t0, f"timeout dopo {timeout}s"
    except Exception as e:  # noqa: BLE001
        return "FAIL", time.time() - t0, f"errore di esecuzione: {e}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("role", nargs="?", help="ruolo da eseguire (default: tutti)")
    ap.add_argument("--id", help="un solo criterio")
    ap.add_argument("--gate", help="filtra per gate")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--coverage", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="stub e criteri saltati contano come fallimento")
    ap.add_argument("--run-stubs", action="store_true",
                    help="esegue anche i comandi ancora stub (per verificarne l'esistenza)")
    ap.add_argument("--timeout", type=int, default=1800)
    a = ap.parse_args()

    reg = load()
    crit = reg["criteria"]
    roles = [r["id"] for r in reg["roles"]]

    if a.coverage:
        return coverage(reg, a.json)

    sel = crit
    if a.role:
        if a.role not in roles:
            print(f"ruolo sconosciuto: {a.role}\nruoli: {', '.join(roles)}", file=sys.stderr)
            return 2
        sel = [c for c in sel if c["role"] == a.role]
    if a.id:
        sel = [c for c in sel if c["id"] == a.id]
    if a.gate:
        sel = [c for c in sel if str(c.get("gate")) == a.gate]
    if not sel:
        print("nessun criterio corrisponde al filtro", file=sys.stderr)
        return 2

    bench = os.environ.get("R2S_BENCH") == "1"
    manual = os.environ.get("R2S_MANUAL") == "1"

    if a.list:
        print(f"{C['B']}{'ID':28} {'RUOLO':20} {'TIPO':7} {'STATO':16} CRITERIO{C['OFF']}")
        for c in sel:
            st = c.get("status", "?")
            col = C["PASS"] if st == "implemented" else C["STUB"]
            print(f"{c['id']:28} {c['role']:20} {c.get('kind','?'):7} "
                  f"{col}{st:16}{C['OFF']} {c['criterio'][:70]}")
            if c.get("blocked_by"):
                print(f"{'':28} {C['SKIP']}bloccato: {c['blocked_by'].strip()}{C['OFF']}")
        return 0

    results = []
    print(f"{C['B']}Criteri di FATTO — {len(sel)} selezionati "
          f"(banco: {'incluso' if bench else 'escluso'}, "
          f"manuali: {'inclusi' if manual else 'esclusi'}){C['OFF']}\n")

    for c in sel:
        action, why = decide(c, bench, manual, a.run_stubs)
        if action == "run":
            status, dt, out = run_one(c, a.timeout)
        elif action == "skip":
            status, dt, out = "SKIP", 0.0, why
        else:
            status, dt, out = "STUB", 0.0, why
        results.append({"id": c["id"], "role": c["role"], "status": status,
                        "seconds": round(dt, 1), "metric": target(c.get("metric", {})),
                        "detail": out.strip()[-500:], "command": c["command"]})
        print(f"{C[status]}{status:5}{C['OFF']}  {c['id']:28} {c['role']:20} "
              f"{dt:5.1f}s  {target(c.get('metric', {}))}")
        if status == "FAIL":
            for ln in out.strip().splitlines()[-12:]:
                print(f"        | {ln}")
            print(f"        riesegui con: {c['command']}")
        elif status in ("SKIP", "STUB"):
            print(f"        {why}")
            if c.get("blocked_by"):
                print(f"        bloccato da: {c['blocked_by'].strip()}")

    n = {k: sum(1 for r in results if r["status"] == k)
         for k in ("PASS", "FAIL", "SKIP", "STUB")}
    print(f"\n{C['B']}Esito{C['OFF']}: {C['PASS']}{n['PASS']} passati{C['OFF']}, "
          f"{C['FAIL']}{n['FAIL']} falliti{C['OFF']}, "
          f"{C['SKIP']}{n['SKIP']} saltati (banco/manuale){C['OFF']}, "
          f"{C['STUB']}{n['STUB']} non implementati{C['OFF']}")

    if a.json:
        (ROOT / "reports").mkdir(exist_ok=True)
        p = ROOT / "reports/fatto.json"
        p.write_text(json.dumps({"summary": n, "results": results}, indent=2))
        print(f"report: {p.relative_to(ROOT)}")

    if n["FAIL"]:
        return 1
    if a.strict and (n["STUB"] or n["SKIP"]):
        print("--strict: stub e criteri saltati contano come fallimento")
        return 1
    return 0


def coverage(reg: dict, as_json: bool) -> int:
    rows = []
    for r in reg["roles"]:
        cs = [c for c in reg["criteria"] if c["role"] == r["id"]]
        with_cmd = [c for c in cs if c.get("command")]
        impl = [c for c in cs if c.get("status") == "implemented"]
        blocked = [c for c in cs if c.get("blocked_by")]
        rows.append({"ruolo": r["id"], "criteri": len(cs), "con_comando": len(with_cmd),
                     "implementati": len(impl), "bloccati": len(blocked)})
    if as_json:
        print(json.dumps(rows, indent=2))
    else:
        print(f"{C['B']}{'RUOLO':22} {'CRITERI':>8} {'CON COMANDO':>12} "
              f"{'IMPLEMENTATI':>13} {'BLOCCATI':>9}{C['OFF']}")
        for x in rows:
            print(f"{x['ruolo']:22} {x['criteri']:8} {x['con_comando']:12} "
                  f"{x['implementati']:13} {x['bloccati']:9}")
    missing = [x["ruolo"] for x in rows if x["con_comando"] < x["criteri"]]
    covered = sum(1 for x in rows if x["criteri"] and x["con_comando"] == x["criteri"])
    print(f"\nCopertura: {covered}/{len(rows)} ruoli hanno un comando per OGNI criterio")
    if missing:
        print("Ruoli con criteri senza comando (da segnalare al chief-engineer): "
              + ", ".join(missing))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
