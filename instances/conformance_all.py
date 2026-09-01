#!/usr/bin/env python3
"""Conformance gate for every sector instance (run with the Sprint-0 venv interpreter).

Reuses the Sprint-0 conformance validator VERBATIM over each sector's emitted fixtures
(04-audit.md's procedure, applied per sector). Exit 0 = every sector ALL PASS (C1-C5).

Usage:  /home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python conformance_all.py
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPRINT0 = HERE.parents[0] / "sprints/sprint-0/artifacts"
sys.path.insert(0, str(SPRINT0))
sys.path.insert(0, str(HERE))

import conformance  # noqa: E402
import configs     # noqa: E402

overall = True
for label in configs.SECTORS:
    fx = HERE / label / "artifacts/fixtures"
    if not (fx / "ledger").exists():
        print(f"[{label}] fixtures missing (run build_all.py first)")
        overall = False
        continue
    conformance.FIXTURES = fx
    ok = conformance.Conformance().run()
    overall &= ok
    print(f"[{label}] -> {'ALL PASS' if ok else 'FAILURES'}")

print("\nSECTOR CONFORMANCE:", "ALL SECTORS PASS" if overall else "FAILURES PRESENT")
sys.exit(0 if overall else 1)