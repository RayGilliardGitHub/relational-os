#!/usr/bin/env python3
"""conformance_tradeoff.py — C1-C5 gate over the trade-off / business-model fixtures.

Runs the Sprint-0 validator over instances/contested_reality/artifacts/tradeoff/fixtures,
proving the Sprint-11 additive fields (shared constraint/interest objects on relationships, the
conflict object on the case, the additive `recommendation` envelope in the frozen `Recommendation`
$def shape incl. `tradeoff` + machine-readable `json` ranking, `UNRESOLVED`/`epistemic_state`)
stay schema-valid with the frozen 49 $defs and the frozen URI cap — no schema edit, no new noun.

Usage: (from instances/contested_reality)
  /home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python conformance_tradeoff.py
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPRINT0 = HERE.parents[1] / "sprints/sprint-0/artifacts"
sys.path.insert(0, str(SPRINT0))
import conformance  # noqa: E402

conformance.FIXTURES = HERE / "artifacts/tradeoff/fixtures"
ok = conformance.Conformance().run()
print("\nTRADE-OFF CONFORMANCE:", "ALL PASS" if ok else "FAILURES PRESENT")
sys.exit(0 if ok else 1)