#!/usr/bin/env python3
"""build_all_agents.py — run the real-LLM agent pathway across all 12 sector configs.

For each config in configs.SECTORS: build the sector scene, inject the local-model's #8
recommendation + evidence-verify (both advisory decision://), assert the §6 floor order, the
advisory-only boundary, and the deterministic trust formula. exit 0 = every sector ALL PASS.

Usage:  (from instances/)  python3 build_all_agents.py        exit 0 = ALL SECTORS PASS
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import configs                       # noqa: E402
from agent_demo import run_agent_demo as rad  # noqa: E402


def main() -> int:
    print("=== RelationalOS — real-LLM agent pathway across all sector families ===\n")
    allok = True
    rows = []
    for label in configs.SECTORS:
        try:
            ok, *_ = rad.run_agent_sector(label)
        except Exception as e:  # noqa: BLE001
            ok = False
            print(f"  [{label:6}] EXCEPTION: {e}")
        allok &= ok
        rows.append((label, ok))
        print(f"  [{label:6}] -> {'ALL PASS' if ok else 'FAILURES'}\n")
    print("--- summary ---")
    for label, ok in rows:
        print(f"  {label:6} {'PASS' if ok else 'FAIL'}")
    print("\nRESULT:", "ALL SECTORS PASS" if allok else "FAILURES PRESENT")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())