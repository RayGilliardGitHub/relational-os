#!/usr/bin/env python3
"""Sprint-5 end-to-end demo: the Business Operating Layer (the product) on Quoteko.

Chains the FULL S1->S5 state -> 5.1 Case-led loop + exception heartbeat + Learning ->
5.2 Goals/Metrics/Priority/Dependency -> 5.3 The Cockpit + §7L ten questions.

Runs the re-used Sprint-1/2/3/4 checks (no regression) AND the Sprint-5 checks
(bol / health / cockpit), emits fixtures, and writes the cockpit report.

Usage:  python3 run_s5_demo.py    (exit 0 = all checks pass)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))  # canonical ros/ at repo root

import s3_demo                                # noqa: E402
import s5_demo                                # noqa: E402
import s4_demo                                # noqa: E402
import bol_demo                               # noqa: E402
from ros import checks                        # noqa: E402


def main() -> int:
    allok = True
    print("=== Sprint 5 — Business Operating Layer (the product) — Quoteko ===\n")

    # ---- full chain: S1->S5 (Sprint-4 state) then the operating layer ----
    sub, before, after = s5_demo.build_s2()      # Sprint-1/2 substrate + S5 loop
    s3_demo.build_s3(sub)                        # Sprint-3 orchestration + human floor
    s4_demo.build_s41(sub); s4_demo.build_s42(sub); s4_demo.build_s43(sub)  # Sprint-4

    print("--- [S1/S2/S3/S4/S5] re-used Sprint-1..4 checks (no regression on the full state) ---")
    for cname in ("s1", "roundtrip", "s5"):
        print(f"\n  [check:{cname}]")
        for name, ok, why in checks.ALL_CHECKS[cname](sub):
            allok = allok and ok
            print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")
    for cname in ("s3", "escalate"):
        print(f"\n  [check:{cname}]")
        for name, ok, why in checks.ALL_CHECKS[cname](sub):
            allok = allok and ok
            print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")
    print("\n  [check:loop]")
    for name, ok, why in checks.loop_check(sub, (sub._meta.get("s3_next_rank") or [])):
        allok = allok and ok
        print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")
    for cname in ("s4", "role", "org"):
        print(f"\n  [check:{cname}]")
        for name, ok, why in getattr(checks, f"{cname}_check")(sub):
            allok = allok and ok
            print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")

    # ---- 5.1 Case-led loop + exception heartbeat + learning ----------------
    s51 = bol_demo.build_s51(sub)
    print("\n======== 5.1  CASE-LED LOOP + EXCEPTION HEARTBEAT + LEARNING ========")
    print(f"exception: expected {s51['exception']['expected']}, actual "
          f"{s51['exception']['actual']}, variance {s51['exception']['variance']} "
          f"({s51['exception']['significance']}) — ledger {s51['exception']['on']}/"
          f"{s51['exception']['total']} on time")
    print(f"case {s51['case']} lifecycle OPEN->TRIAGE->ASSIGNED->IN_PROGRESS->BLOCKED"
          f"->RESOLVED->CLOSED -> final {s51['final_status']}")
    print(f"#8 task {s51['task']} (assigned_to {s51['assigned_to']}, authority "
          f"{s51['authority']}, priority {s51['priority']['score']})")
    fo = s51["follow_on"]
    print(f"verified outcome: rallied {fo['exchange']} outcome {fo['evaluation']} "
          f"(ev {fo['evidence']}); forward on-time {fo['forward_on_time']}; "
          f"solarworks Trust -> {fo['after_trust']}")
    print(f"learning entry {s51['learning']}; policy v{s51['policy_final_version']}")

    # ---- 5.2 Goals / Metrics / Priority / Dependency -----------------------
    s52 = bol_demo.build_s52(sub)
    print("\n======== 5.2  GOALS / METRICS / PRIORITY / DEPENDENCY ========")
    for h in s52["health"]:
        print(f"  health {h['name']}: target {h['target']}, actual {h['actual']}, "
              f"variance {h['variance']} -> {h['status']}")
    print("  priority-ordered attention: " +
          ", ".join(f"{a['uri']}@{a['priority']:.2f}" for a in s52["attention"]))
    print(f"  impact(followup task) -> {s52['impact']['impacted']}")

    # ---- 5.3 The Cockpit + §7L ----------------------------------------------
    cockpit = bol_demo.build_s53(sub)
    print("\n======== 5.3  THE COCKPIT (business health + attention + recommendation) ========")
    print(f"attention_line: {cockpit['attention_line']}")
    print("AI recommendation -> " + cockpit["recommendation"]["summary"] +
          f"  (authority {cockpit['recommendation']['authority_required']}, "
          f"confidence {cockpit['recommendation']['confidence']})")

    print("\n--- emit fixtures + cockpit report ---")
    for name, path in bol_demo.emit_s5_fixtures(sub).items():
        print(f"  wrote {name} -> file://{path}")
    md, jp = bol_demo.write_cockpit_report(cockpit, sub)
    print(f"  cockpit -> file://{md}")
    print(f"  cockpit json -> file://{jp}")

    # ---- Sprint-5 checks -----------------------------------------------------
    print("\n--- Sprint-5 checks ---")
    for cname in ("bol", "health", "cockpit"):
        print(f"\n  [check:{cname}]")
        fn = {"bol": checks.s5_bol_check, "health": checks.business_health_check,
              "cockpit": checks.cockpit_check}[cname]
        for name, ok, why in fn(sub):
            allok = allok and ok
            print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")

    print("\n--- Ledger / Graph wiring ---")
    ok, why = sub.ledger.verify()
    print(f"  ledger hash-chain + signatures: {'OK' if ok else why} | entries {len(sub.ledger.entries)}")
    print(f"  graph current-state objects: {len(sub.graph.objects)}")
    allok = allok and ok
    print("\n  [check:roundtrip] full Sprint-5 state (whole Graph rebuilds from the whole Ledger, §3.16)")
    for name, ok, why in checks.roundtrip_check(sub):
        allok = allok and ok
        print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")

    print("\nRESULT:", "ALL PASS" if allok else "FAILURES PRESENT")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())