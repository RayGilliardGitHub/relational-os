#!/usr/bin/env python3
"""Sprint-3 end-to-end demo: Orchestration (S3) + human floor on the Quoteko scene.

Demonstrates the FULL §5 loop on one relationship (relationship://qk/cust-cxn):
  S1 identity/role/authz -> S2 intent/match -> first S5 trust cycle (Sprint-2)
  -> S3 commit + execute across the agent fleet over the routing seam
     (reversible steps auto-run; the irreversible release_final_payment escalates to
      person://qk/approver, whose signed decision enumerates alternatives and commits it)
  -> 2nd S5 update from the S3-executed outcome -> S2 re-ranks the NEXT cycle (flywheel closed).

Runs the Sprint-2 checks (s1/roundtrip/s5/flywheel) on the Sprint-2 state AND the new
Sprint-3 checks (s3/escalate/loop) on the added state, then emits fixtures.

Usage:  <sprint0-venv>/bin/python run_s3_demo.py    (exit 0 = all checks pass)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import s5_demo                                # noqa: E402
import s3_demo                                # noqa: E402
from ros import checks                        # noqa: E402


def main() -> int:
    allok = True
    print("=== Sprint 3 — Orchestration (S3) + human-escalation floor (Quoteko) ===\n")

    # ---- Sprint-2 state first (reuse the prior harness, unchanged) ----------
    sub, before, after = s5_demo.build_s2()

    print("--- [S1/S2/S5] Sprint-2 checks on the pre-S3 state ---")
    for cname in ("s1", "roundtrip", "s5"):
        print(f"\n  [check:{cname}]")
        for name, ok, why in checks.ALL_CHECKS[cname](sub):
            allok = allok and ok
            print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")
    print("\n  [check:flywheel]")
    for name, ok, why in checks.flywheel_check(sub, before, after):
        allok = allok and ok
        print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")

    # ---- extend through the S3 cycle + 2nd S5 update + next S2 rank ---------
    summary = s3_demo.build_s3(sub)

    print("\n========================= FULL S1->S5 LOOP (ONE RELATIONSHIP) =========================")
    print("relationship: file://relationship://qk/cust-cxn   customer: person://qk/customer")
    print(f"\nS1  identity/role/authz     resolved via Sprint-1 substrate (person://qk/customer)")
    print(f"S2  intent                  {summary['intent2']['need']} urgency={summary['intent2']['urgency']}")
    print(f"    matched (Trust-weighted) {[(m['provider'], round(m['score'],3)) for m in summary['match2']]}")

    print("\nS3  commit                   agreement -> "
          f"{summary['commitment']['uri']} ({summary['commitment']['status']})")
    print("    orchestrate the fleet    split decision://qk/s3-split-c-solarworks")
    for t in summary["tasks"]:
        rev = "REVERSIBLE" if (t["reversible"] and t["cost_knowable"]) else "IRREVERSIBLE"
        print(f"        - {t['task_id']} {t['action']}  [{t['worker']} @ {t['tier']}]  {rev}")
    print(f"    worker steps executed    {summary['executed']}")
    print(f"    IRREVERSIBLE step        {summary['escalated']['task_id']} {summary['escalated']['action']} "
          f"-> ESCALATED to person://qk/approver (NOT auto-executed)")
    print(f"    human acknowledged       {summary['human_decision']} (alternatives enumerated)")
    print(f"    then executed            {summary['final_event']}")

    print(f"\nS5  capture S3-executed outcome -> {summary['evidence2']['uri']} "
          f"(verity {summary['evidence2']['verity']})")
    t2 = summary["trust2"]
    print(f"    Trust update             solarworks {t2['expected']:.0f}-> {t2['score']} "
          f"(outcome={t2['outcome']:.0f}, alpha={t2['alpha']})")
    print(f"\nS2  next cycle re-rank       {[(m['provider'], round(m['score'],3)) for m in summary['next_rank']]} "
          f"<- loop closed (S3 outcome -> S5 Trust -> re-ranks S2)")

    # ---- Sprint-3 checks on the added state ---------------------------------
    print("\n--- Sprint-3 checks ---")
    for cname in ("s3", "escalate"):
        print(f"\n  [check:{cname}]")
        for name, ok, why in checks.ALL_CHECKS[cname](sub):
            allok = allok and ok
            print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")
    print("\n  [check:loop]")
    for name, ok, why in checks.loop_check(sub, summary["next_rank"]):
        allok = allok and ok
        print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")

    print("\n--- Ledger / Graph wiring ---")
    ok, why = sub.ledger.verify()
    print(f"  ledger hash-chain + signatures: {'OK' if ok else why} | entries {len(sub.ledger.entries)}")
    print(f"  graph current-state objects: {len(sub.graph.objects)}")
    allok = allok and ok

    print("\n--- emit fixtures ---")
    for name, path in s3_demo.emit_s3_fixtures(sub).items():
        print(f"  wrote {name} -> file://{path}")

    print("\nRESULT:", "ALL PASS" if allok else "FAILURES PRESENT")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())