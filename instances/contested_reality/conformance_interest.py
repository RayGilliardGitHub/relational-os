#!/usr/bin/env python3
"""conformance_interest.py — C1-C5 gate over the conflicting-interest fixtures.

Runs the Sprint-0 validator over instances/contested_reality/artifacts/interest/fixtures,
proving the additive conflicting-interest fields (interest objects on relationships, the
shared constraint, the conflict/negotiation/appeal objects on the case, the native
Right type=APPEAL) stay schema-valid with the frozen 49 $defs and the frozen URI cap.

Usage: (from instances/contested_reality)
  /home/rlg/relational-os/.venv/bin/python conformance_interest.py
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPRINT0 = HERE.parents[1] / "schema"
sys.path.insert(0, str(SPRINT0))
import conformance  # noqa: E402

conformance.FIXTURES = HERE / "artifacts/interest/fixtures"
ok = conformance.Conformance().run()
print("\nINTEREST-CONFLICT CONFORMANCE:", "ALL PASS" if ok else "FAILURES PRESENT")
sys.exit(0 if ok else 1)