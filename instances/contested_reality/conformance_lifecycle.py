#!/usr/bin/env python3
"""conformance_lifecycle.py — C1-C5 gate over the full contested-reality lifecycle fixtures.

Runs the Sprint-0 validator over instances/contested_reality/artifacts/lifecycle/fixtures,
proving the Sprint-12 additive fields stay schema-valid with the frozen 49 $defs + URI cap
(no schema edit): epistemic_status on claims; reliability/supports/provenance on evidence;
interests/obligations/constraints/available_resolutions on the dispute; lifecycle/epistemic/
determination/resolution_type/reopened; appeal->reopen->reassess chains; trust error-vs-deception;
UNRESOLVED. Includes the full dispute lifecycle state-machine walk for C5.

Usage: (from instances/contested_reality)
  /home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python conformance_lifecycle.py
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPRINT0 = HERE.parents[1] / "sprints/sprint-0/artifacts"
sys.path.insert(0, str(SPRINT0))
import conformance  # noqa: E402

conformance.FIXTURES = HERE / "artifacts/lifecycle/fixtures"
ok = conformance.Conformance().run()
print("\nLIFECYCLE CONFORMANCE:", "ALL PASS" if ok else "FAILURES PRESENT")
sys.exit(0 if ok else 1)