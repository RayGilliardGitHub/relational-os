#!/usr/bin/env python3
"""RelationalOS — canonical green-gate test suite (plain python3; ~$0).

Runs the WHOLE reference build from the repo root and asserts every step exits 0 + the
frozen invariants still hold. This is the reorg's canonical test suite: `tests/`. It is
location-independent (every path is anchored to __file__), so it works from the repo root
OR any deep cwd — the reorg fixed the CWD-bound conformance scripts.

Usage:  python3 tests/run_checks.py        (from the repo root)   → exit 0 = ALL PASS
        python3 /home/rlg/relational-os/tests/run_checks.py        (from anywhere)

Steps (the documented green gate):
  1.  canonical `ros/` package imports from the repo root;
  2.  canonical `ros/` is FLAT byte-identical to archive/sprints/sprint-5/artifacts/ros/;
  3.  frozen invariants: schema 34264934…(yaml)/7fc38c8c(json), 49 $defs, SPEC v0.22,
      engine a60f8f7…, capacity_rerank.py f7c6a185…;
  4.  daily cockpit (S1-S5 + BOL): reference/ python3 run_s5_demo.py;
  5.  conformance all-six generations: schema/run_conformance_all.py (the .venv interpreter);
  6.  sectors: instances/ build_all.py (python3) + conformance_all.py (venv);
  7.  contested_reality: the 20 canonical CR demos (python3) + the 5 CR conformances (venv);
  8.  S5 reference demo + agent demo + their conformances.

Prints `RESULT: ALL PASS` (exit 0) or `FAILURES PRESENT` (exit 1). Pure subprocess + assertions.
No network; no pip; demos are deterministic local python.
"""
from __future__ import annotations
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent        # .../relational-os/tests
ROOT = HERE.parent                             # .../relational-os
VENV = ROOT / ".venv/bin/python"
CR = ROOT / "instances/contested_reality"
S5 = ROOT / "reference"
INST = ROOT / "instances"
AGENT = ROOT / "instances/agent_demo"

_OK = True
_TOTAL = 0

def _report(name, cond, why=""):
    global _OK, _TOTAL
    _OK &= bool(cond); _TOTAL += 1
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")

def _run(cmd, cwd=None, venv=False, name=""):
    """Run cmd in cwd; assert exit 0. Returns True on success."""
    c = [str(VENV) if venv and cmd[0] == "python3" else cmd[0]] + cmd[1:]
    try:
        r = subprocess.run(c, cwd=str(cwd), capture_output=True, text=True, timeout=900)
    except Exception as e:
        _report(f"{name}: crashed ({type(e).__name__})", False, str(e)); return False
    tail = (r.stdout.strip().splitlines() or [""])[-1][:80]
    _report(f"{name} (exit {r.returncode})", r.returncode == 0, f"last={tail}")
    return r.returncode == 0

def _sha8(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:8]


def main() -> int:
    print("=== RelationalOS reorg green-gate test suite (from repo root) ===\n")

    # ---- 1-3 canonical layout + frozen invariants ------------------------------------------------
    print("-- canonical layout + frozen invariants --")
    # import ros from repo root
    ok = subprocess.run(["python3", "-c",
                         "import sys; sys.path.insert(0, sys.argv[1]); import ros; print(ros.__file__)",
                         str(ROOT)], capture_output=True, text=True).returncode == 0
    _report("canonical `ros/` package imports from the repo root", ok)
    # ros byte-identity vs sprint-5 canonical
    same = all(_sha8(f) == _sha8(ROOT / "archive/sprints/sprint-5/artifacts/ros" / f.name)
               for f in (ROOT / "ros").glob("*.py"))
    _report("canonical `ros/` FLAT byte-identical to archive/sprints/sprint-5/artifacts/ros/", same)
    # frozen invariants
    yaml_h = _sha8(ROOT / "schema/relational-os.schema.yaml")
    json_h = _sha8(ROOT / "schema/relational-os.schema.json")
    _report("schema hash 34264934…(.yaml)/7fc38c8c(.json)", yaml_h == "34264934" and json_h == "7fc38c8c",
            f"yaml={yaml_h} json={json_h}")
    nd = len(json.load(open(ROOT / "schema/relational-os.schema.json"))["$defs"])
    _report("49 $defs", nd == 49, f"live={nd}")
    mver = re.search(r"Version:\s*\**\s*([0-9.]+)", (ROOT / "SPEC.md").read_text())
    _report("SPEC v0.22", bool(mver) and mver.group(1) == "0.22", f"live={mver.group(1) if mver else None}")
    _report("adjudication_engine.py a60f8f7…", _sha8(CR / "adjudication_engine.py") == "a60f8f71")
    _report("capacity_rerank.py f7c6a185…", _sha8(CR / "capacity_rerank.py") == "f7c6a185")

    # ---- 4-8 the green gate ----------------------------------------------------------------------
    print("\n-- daily cockpit (S1-S5 + BOL) --")
    _run(["python3", "run_s5_demo.py"], cwd=S5, name="s5 daily cockpit")

    print("\n-- conformance all-six generations (Sprint-0 venv) --")
    _run(["python3", "run_conformance_all.py"], cwd=ROOT / "schema", venv=True, name="conformance all-six")

    print("\n-- sectors (instances/) --")
    _run(["python3", "build_all.py"], cwd=INST, name="build_all (12 sectors)")
    _run(["python3", "conformance_all.py"], cwd=INST, venv=True, name="conformance_all (12 sectors)")

    print("\n-- contested_reality: 20 canonical CR demos (python3) --")
    CR_DEMOS = [
        "run_adjudication_engine_demo.py", "run_cockpit_s7l_demo.py", "run_cockpit_q7q8_demo.py",
        "run_forecast_action_demo.py", "run_forecast_capacity_demo.py", "run_forecast_direction_demo.py",
        "run_forecast_horizon_demo.py", "run_forecast_horizon2_demo.py", "run_forecast_horizon3_demo.py",
        "run_forecast_horizon4_demo.py", "run_forecast_label_vs_choice_demo.py",
        "run_forecast_per_option_capacity_demo.py", "run_forecast_variance_demo.py",
        "run_forecast_variance_all_demo.py", "run_capacity_rerank_demo.py", "run_recorded_surface_demo.py",
        "run_two_path_demo.py", "run_two_path_catalog_demo.py", "run_reproducibility_demo.py",
        "run_corpus_consistency_demo.py",
    ]
    for d in CR_DEMOS:
        _run(["python3", d], cwd=CR, name=d)

    print("\n-- contested_reality: 5 CR conformances (venv) --")
    for c in ["conformance_adjudication.py", "conformance_dispute.py", "conformance_interest.py",
              "conformance_lifecycle.py", "conformance_tradeoff.py"]:
        _run(["python3", c], cwd=CR, venv=True, name=c)

    print("\n-- agent demo + S5 reference --")
    _run(["python3", "run_agent_demo.py"], cwd=AGENT, name="agent demo")
    _run(["python3", "conformance_agent.py"], cwd=AGENT, venv=True, name="agent conformance")

    print("\n-- financial legacy instance (not part of a numbered gate; added post-reorg) --")
    _run(["python3", "fin_demo.py"], cwd=ROOT / "instances/financial", name="fin_demo")
    _run(["python3", "run_fin.py"], cwd=ROOT / "instances/financial", name="run_fin")
    _run(["python3", "run_fin_conformance.py"], cwd=ROOT / "instances/financial", venv=True,
         name="run_fin_conformance")

    print(f"\n{_TOTAL} checks; RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(main())