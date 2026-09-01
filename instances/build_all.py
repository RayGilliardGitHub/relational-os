#!/usr/bin/env python3
"""Build and verify every sector instance (plain python3).

For each sector config in configs.SECTORS: build the S1->S5 chain + BOL via
sector_scene.build_scene, run the generic integrity checks, emit fixtures/ledger/graph,
and write the cockpit + §7L report under instances/<label>/artifacts.

Usage:  (from instances/)  python3 build_all.py     exit 0 = every sector ALL PASS
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[0]))

import sector_scene as ss            # noqa: E402
import configs                       # noqa: E402
from ros.substrate import Substrate  # noqa: E402


def main() -> int:
    allok = True
    print("=== RelationalOS sector instances (multi-sector dogfood) ===\n")
    rows = []
    for label, cfg in configs.SECTORS.items():
        sub = Substrate(ledger_uri=f"db://ledger/{label}-2026")
        ss.build_scene(cfg, sub)
        outdir = HERE / label
        ss.emit(sub, outdir)
        ss.write_cockpit(sub, outdir)
        ss.write_branding(sub, outdir)
        checks = ss.run_checks(sub, outdir)
        ok = all(c[1] for c in checks)
        allok &= ok
        print(f"[{label:6}] {cfg['sector']:26} {cfg['company_name']:22} "
              f"ledger {len(sub.ledger.entries):3} graph {len(sub.graph.objects):3} "
              f"-> {'ALL PASS' if ok else 'FAILURES'}")
        for name, cok, why in checks:
            if not cok:
                print(f"         [FAIL] {name}  — {why}")
            elif ok:
                print(f"         [PASS] {name}")
        rows.append((label, len(sub.ledger.entries), len(sub.graph.objects), ok))
    print("\n--- summary ---")
    for label, le, go, ok in rows:
        print(f"  {label:6} ledger={le:3} graph={go:3} {'PASS' if ok else 'FAIL'}")
    print("\nRESULT:", "ALL SECTORS PASS" if allok else "FAILURES PRESENT")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())