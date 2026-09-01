#!/usr/bin/env python3
"""Re-run Sprint-0's conformance validator over Sprint-0, Sprint-1, and Sprint-2
fixture generations.

Reuses the Sprint-0 validator verbatim (same code, same schema), repointing its
FIXTURES root at each generation's fixtures in turn, so non-regression is proven
by the exact same gate across all three. Exit 0 = ALL PASS.

Usage:  <sprint0-venv>/bin/python run_s2_conformance.py
"""
import sys
from pathlib import Path

######## import Sprint-0's validator verbatim ########
SPRINT0 = Path("../../sprint-0/artifacts").resolve()
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(SPRINT0))

import conformance  # noqa: E402

ROOTS = [
    ("sprint-0", SPRINT0 / "fixtures"),
    ("sprint-1", HERE.parents[1] / "sprint-1/artifacts/fixtures"),
    ("sprint-2", HERE / "fixtures"),
]

overall = True
for label, root in ROOTS:
    conformance.FIXTURES = root
    name = f"[{label}] {root.relative_to(SPRINT0.parent.parent)}"
    print(f"\n=== {name} ===")
    ok = conformance.Conformance().run()
    overall = overall and ok

print("\nRESULT:", "ALL PASS" if overall else "FAILURES PRESENT")
sys.exit(0 if overall else 1)