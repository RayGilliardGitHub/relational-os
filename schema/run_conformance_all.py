#!/usr/bin/env python3
"""Canonical conformance gate — validate all six fixture generations (gen-0..5) with ONE validator.

The validator lives at schema/conformance.py; the fixture corpus lives at data/fixtures/gen-{0..4}
(gen-5 is the reference build's produced corpus at reference/fixtures). This is the deployment
(sprint-free) successor to the per-sprint run_sN_conformance.py. Exit 0 = ALL PASS.
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # schema/
ROOT = HERE.parent                               # repo root
sys.path.insert(0, str(HERE))                    # find conformance.py

import conformance  # noqa: E402

ROOTS = [
    ("gen-0", ROOT / "data/fixtures/gen-0"),
    ("gen-1", ROOT / "data/fixtures/gen-1"),
    ("gen-2", ROOT / "data/fixtures/gen-2"),
    ("gen-3", ROOT / "data/fixtures/gen-3"),
    ("gen-4", ROOT / "data/fixtures/gen-4"),
    ("gen-5", ROOT / "reference/fixtures"),
]

def main() -> int:
    overall = True
    for label, root in ROOTS:
        conformance.FIXTURES = root
        print(f"\n=== [{label}] {root} ===")
        ok = conformance.Conformance().run()
        overall = overall and ok
    print("\nRESULT:", "ALL PASS" if overall else "FAILURES PRESENT")
    return 0 if overall else 1

if __name__ == "__main__":
    sys.exit(main())
