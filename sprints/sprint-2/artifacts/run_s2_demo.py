#!/usr/bin/env python3
"""Sprint-2 end-to-end demo: Trust engine (S5) minimum on the Quoteko scene.

Demonstrates: capture + verify one outcome class, update + persist scoped Trust,
and the §5 flywheel — Trust re-ranks S2 results. Runs self-authored checks
(S1 substrate, S5 capture/verify/update, flywheel) + emits fixtures.

Usage:  <sprint0-venv>/bin/python run_s2_demo.py    (exit 0 = all checks pass)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import s5_demo                                # noqa: E402
from ros.s2 import S2Service                  # noqa: E402
from ros import checks                        # noqa: E402


def main() -> int:
    print("=== Sprint 2 — S5 Trust engine minimum (Quoteko) ===")
    sub, before, after = s5_demo.build_s2()
    ctx = s5_demo.CTX
    cfg = __import__("ros.s5", fromlist=["config_defaults"]).config_defaults()

    def trust(name):
        o = sub.graph.get(f"trust://qk/t-{name}")
        return o["score"] if o else None

    print("\n--- 2.1 S5 capture + verify (outcome class: on-time completion) ---")
    for job in ("norcrete", "solarworks"):
        ev = sub.graph.get(f"evidence://qk/job-{job}")
        cl = sub.graph.get(f"claim://qk/job-{job}")
        print(f"  {job}: evidence://qk/job-{job} kind={ev['kind']} verity={ev['verity']}")
        print(f"         claim={cl['statement']!r}")
        comp = sub.graph.get(f"event://qk/outcome-{job}")
        print(f"         outcome {job}: on_time={comp['on_time']} "
              f"actual={comp['actual_completed_at']} vs dl={comp['committed_deadline']}")

    print("\n--- 2.2 Trust update (scoped, clamped, persisted) ---")
    print(f"  alpha={cfg['alpha']} expectation={cfg['expectation']} recency={cfg['recency']}")
    print(f"  norcrete (bad)   : 0.92 -> {trust('norcrete'):.3f}   (delta "
          f"{0.5*(0.0-cfg['expectation'])*0.98:+.3f})")
    print(f"  solarworks (good): 0.61 -> {trust('solarworks'):.3f}   (delta "
          f"{0.5*(1.0-cfg['expectation'])*0.98:+.3f})")
    print(f"  generalco (other claim): {trust('generalco'):.2f} (untouched -> scope, not global)")

    print("\n--- 2.3 Flywheel: Trust re-ranks S2 ---")
    print(f"  BEFORE ranking: {[(m['provider'], m['score']) for m in before]}")
    print(f"  AFTER  ranking: {[(m['provider'], m['score']) for m in after]}")

    print("\n--- Ledger / Graph wiring ---")
    print(f"  ledger events: {len(sub.ledger.entries)} | head_hash {sub.ledger.head_hash[:12]}…")
    print(f"  graph current-state objects: {len(sub.graph.objects)}")

    print("\n--- checks ---")
    allok = True
    for cname in ("s1", "roundtrip", "s5"):
        print(f"\n  [check:{cname}]")
        res = checks.ALL_CHECKS[cname](sub)
        for name, ok, why in res:
            allok = allok and ok
            print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")
    print("\n  [check:flywheel]")
    for name, ok, why in checks.flywheel_check(sub, before, after):
        allok = allok and ok
        print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")

    print("\n--- emit fixtures ---")
    for name, path in s5_demo.emit_s2_fixtures(sub).items():
        print(f"  wrote {name} -> file://{path}")

    print("\nRESULT:", "ALL PASS" if allok else "FAILURES PRESENT")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())