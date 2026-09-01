#!/usr/bin/env python3
"""Northglen Bank instance — conformance gate (Sprint-0 validator over the finance fixtures).

Reuses the Sprint-0 conformance validator VERBATIM, repointing its FIXTURES root at the
Northglen instance's fixtures, and runs checks C1-C5. This is the documented audit
(04-audit.md) applied to a new, non-Quoteko instance — the dogfood of the audit manual.

Usage:  /home/rlg/relational-os/.venv/bin/python run_fin_conformance.py
Exit 0 = ALL PASS over the financial instance's fixtures.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPRINT0 = HERE.parents[1] / "schema"  # ../../sprints/sprint-0/artifacts
sys.path.insert(0, str(SPRINT0))

import conformance  # noqa: E402

# point the validator at THIS instance's fixtures
conformance.FIXTURES = HERE / "artifacts/fixtures"

ok = conformance.Conformance().run()
print("\nNORTHGLEN CONFORMANCE:", "ALL PASS" if ok else "FAILURES PRESENT")
sys.exit(0 if ok else 1)