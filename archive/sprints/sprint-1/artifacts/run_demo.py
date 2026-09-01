#!/usr/bin/env python3
"""Sprint-1 end-to-end demo: identity -> intent -> matched offer -> human-verified
-> on the ledger, then run the self-authored S1 and round-trip checks.

Usage:  <sprint0-venv>/bin/python run_demo.py
Exit 0 = all checks pass.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from ros.substrate import Substrate          # noqa: E402
from ros.s1 import S1Service                  # noqa: E402
from ros.s2 import S2Service                  # noqa: E402
import make_fixtures as mf                    # noqa: E402
from ros import checks                        # noqa: E402


def main() -> int:
    print("=== Sprint 1 — S1 substrate + S2 Intent/Matching (Quoteko) ===")
    sub = mf.build()
    m = sub._meta

    print("\n--- S1 substrate (thin) ---")
    print(f"  resolve_identity('qk-customer-8832') -> {m['identity']}")
    print(f"  authenticate -> verif_score {m['authn_score']}")
    print(f"  resolve_role  -> {m['role']} (relationship://qk/cust-cxn)")
    print(f"  authorize('request_quote') -> {m['perm']}")

    print("\n--- S2 Intent / Matching (Trust-weighted, floor 0.5) ---")
    print(f"  intent: {m['intent']['need']} | urgency={m['intent']['urgency']} | keys={m['intent']['capability_keys']}")
    for r in m["matches"]:
        print(f"    rank {r['score']:.2f}  {r['offer']}  (fit {r['fit']:.2f} x trust {r['trust']:.2f})")
    print(f"  rejected (trust floor): {m['rejected']} trust=0.42 < 0.5")
    print(f"  human accepted: {m['top']['offer']} -> commit status {m['offer_status']}")

    print("\n--- Ledger / Graph wiring ---")
    print(f"  ledger events: {len(sub.ledger.entries)} | head_hash {sub.ledger.head_hash[:12]}…")
    print(f"  graph current-state objects: {len(sub.graph.objects)}")

    print("\n--- emit fixtures ---")
    for name, path in mf.write_fixtures(sub).items():
        print(f"  wrote {name} -> file://{path}")

    # self-authored checks
    allok = True
    for cname, fn in checks.ALL_CHECKS.items():
        print(f"\n  [check:{cname}]")
        res = fn(sub) if cname == "s1" else fn(sub)
        for name, ok, why in res:
            allok = allok and ok
            print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")

    print("\nRESULT:", "ALL PASS" if allok else "FAILURES PRESENT")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())