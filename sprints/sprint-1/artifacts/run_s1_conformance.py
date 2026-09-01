#!/usr/bin/env python3
"""Re-run Sprint-0's conformance validator over the Sprint-1 fixtures.

Reuses the Sprint-0 validator verbatim (same code, same schema), only repointing
its FIXTURES root at the Sprint-1 fixtures, so a non-regression of the new
instances is proven by the exact same gate. Also re-runs Sprint-0's own fixtures
(no regression).

Usage:  <sprint0-venv>/bin/python run_s1_conformance.py
Exit 0 = ALL PASS.
"""
import sys
from pathlib import Path

######## import Sprint-0's validator verbatim ########
SPRINT0 = Path(__file__).resolve().parents[2] / "sprint-0/artifacts"
S1_FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SPRINT0))

import conformance  # noqa: E402

# Repoint the shared validator's fixtures root at the Sprint-1 fixtures.
conformance.FIXTURES = S1_FIXTURES
ok = conformance.Conformance().run()
# Restore + re-run sprint-0's own fixtures unchanged (no regression).
conformance.FIXTURES = SPRINT0 / "fixtures"
print("\n[sprint-0 non-regression]")
ok0 = conformance.Conformance().run()

print("\nRESULT:", "ALL PASS" if (ok and ok0) else "FAILURES PRESENT")
sys.exit(0 if (ok and ok0) else 1)