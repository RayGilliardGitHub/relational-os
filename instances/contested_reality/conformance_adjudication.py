#!/usr/bin/env python3
"""conformance_adjudication.py — C1-C5 gate over the Sprint-13 configurable-adjudication-engine
fixtures. Runs the Sprint-0 validator over instances/contested_reality/artifacts/adjudication/
fixtures/{deli,cove}, proving the additive engine fields (epistemic_status on claims, reliability/
supports on evidence, dispute lifecycle/epistemic/determination/resolution_type, additive
learned_weights + realized_cost on the decision) stay schema-valid with the FROZEN 49 $defs + URI
cap (no schema edit). Both supported orgs emit their own fixtures; each is validated.

Usage: (from instances/contested_reality)
  /home/rlg/relational-os/.venv/bin/python conformance_adjudication.py
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPRINT0 = HERE.parents[1] / "schema"
sys.path.insert(0, str(SPRINT0))
import conformance  # noqa: E402

overall = True
labels = ("deli", "cove", "inspect-best", "inspect-anchor", "inspect-rec",
          "inspect-anchor-spec", "inspect-rec-spec", "inspect-majority",
          # Sprint 16: rule-library reuse + the new bayesian-combine primitive fixtures
          "inspect-majority-lib", "deli-majority", "inspect-corroboration",
          "cove-corroboration", "inspect-max098",
          # Sprint 17: decision learning at the reconcile layer — the learning episode (A), the
          # second/future dispute driven under the learned rule (B), and the cross-org reuse.
          "inspect-learn-a", "inspect-learn-b", "deli-learn")
for label in labels:
    fx = HERE / "artifacts/adjudication/fixtures" / label
    if not (fx / "ledger").exists():
        print(f"[{label}] fixtures missing (run run_adjudication_engine_demo.py first)")
        overall = False
        continue
    conformance.FIXTURES = fx
    ok = conformance.Conformance().run()
    overall &= ok
    print(f"[{label}] ADJUDICATION-ENGINE CONFORMANCE -> {'ALL PASS' if ok else 'FAILURES'}")

print("\nADJUDICATION-ENGINE CONFORMANCE:", "ALL PASS" if overall else "FAILURES PRESENT")
sys.exit(0 if overall else 1)