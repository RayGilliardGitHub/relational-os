#!/usr/bin/env python3
"""conformance_dispute.py — C1-C5 gate over the dispute-experiment fixtures.

Runs the Sprint-0 validator over instances/contested_reality/artifacts/fixtures, proving the
additive dispute/epistemic fields (UNDETERMINED / INSUFFICIENT_EVIDENCE / RESOLVED_DETERMINED
via `epistemic_state` + string `resolution`) stay schema-valid and the signed round-trip holds
with the frozen 49 $defs and the frozen Dispute status enum [OPEN, ADJUDICATED, RESOLVED].

Usage: (from instances/contested_reality)
  /home/rlg/relational-os/.venv/bin/python conformance_dispute.py
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPRINT0 = HERE.parents[1] / "schema"
sys.path.insert(0, str(SPRINT0))
import conformance  # noqa: E402

conformance.FIXTURES = HERE / "artifacts/fixtures"
ok = conformance.Conformance().run()
print("\nDISPUTE-DEMO CONFORMANCE:", "ALL PASS" if ok else "FAILURES PRESENT")
sys.exit(0 if ok else 1)