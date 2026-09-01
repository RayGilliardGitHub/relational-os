#!/usr/bin/env python3
"""Sprint-4 end-to-end demo: Settlement (S4) + multi-role (4.2) + multi-org (4.3).

Chains the FULL S1->S5 loop: Sprint-1/2 substrate + S5 loop -> Sprint-3 orchestration +
human floor -> 4.1 settle + evaluate -> 4.2 two roles on one relationship -> 4.3 two org
types + §6 floor gating the irreversible settlement.

Runs the re-used Sprint-1/2/3 checks (no regression) AND the Sprint-4 checks (s4/role/org),
then emits fixtures.

Usage:  python3 run_s4_demo.py    (exit 0 = all checks pass)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import s3_demo                                # noqa: E402
import s5_demo                                # noqa: E402
import s4_demo                                # noqa: E402
from ros import checks                        # noqa: E402


def main() -> int:
    allok = True
    print("=== Sprint 4 — Settlement (S4) + multi-role + multi-org (Quoteko) ===\n")

    # ---- full chain: S1->S5 (Sprint-3 state) then S4 settlement + extensions ----
    sub, before, after = s5_demo.build_s2()      # Sprint-1/2 substrate + S5 loop
    s3_demo.build_s3(sub)                        # Sprint-3 orchestration + human floor

    print("--- [S1/S2/S5/S3] re-used Sprint-1/2/3 checks (no regression on the full state) ---")
    for cname in ("s1", "roundtrip", "s5"):
        print(f"\n  [check:{cname}]")
        for name, ok, why in checks.ALL_CHECKS[cname](sub):
            allok = allok and ok
            print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")
    print("\n  [check:flywheel]")
    for name, ok, why in checks.flywheel_check(sub, before, after):
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

    # ---- 4.1 settle + evaluate -------------------------------------------------
    s41 = s4_demo.build_s41(sub)
    print("\n========================== 4.1  SETTLEMENT ON THE COMPLETED JOB ==========================")
    print("relationship://qk/cust-cxn  solarworks job committed+executed+Trusted (0.806)")
    print(f"S4  settle                   {s41['exchange']}  (EXCHANGE event://, signed)")
    print(f"    Asset Ledger title move  {s41['asset']}  (title -> org://qk/solarworks, §4b)")
    print(f"    payment obligation       {s41['obligation']}  (VOLUNTARILY_UNDERTAKEN)")
    print(f"    receipt                  {s41['receipt']}   reconciliation  {s41['reconciliation']}")
    print(f"S4  evaluate                 {s41['outcome']}  ({s41['evaluation']}) vs expectation")
    print(f"S5  capture settled OUTCOME  -> {s41['evidence']}  Trust {s41['trust_before']} -> {s41['trust_after']}")
    print(f"S2  next cycle re-rank       {[(m['offer'], round(m['score'],3)) for m in s41['next_rank']]} "
          f"<- loop closed WITH settlement in the middle")

    # ---- 4.2 two roles on one relationship -------------------------------------
    s42 = s4_demo.build_s42(sub)
    print("\n========================== 4.2  TWO ROLES ON ONE RELATIONSHIP ==========================")
    print(f"role customer={s42['role_customer']}, employee={s42['role_employee']} on relationship://qk/cust-cxn (§3.2/§C2)")
    a = s42["authz"]
    print(f"role-scoped authz:  employee grant submit_timesheet={a['employee']['submit_timesheet']}, "
          f"receive_payroll={a['employee']['receive_payroll']}, request_quote_DENIED={a['employee']['request_quote_denied']}; "
          f"customer grant request_quote={a['customer']['request_quote']}, receive_payroll_DENIED={a['customer']['receive_payroll_denied']}")
    print(f"S2  employee match          {[(m['offer'], round(m['score'],3)) for m in s42['emp_match']]}")
    print(f"S3  commit + execute        {s42['commitment']}  worker step {s42['pay_action']}")
    print(f"S4  settle payroll          {s42['settle']}  -> outcome {s42['outcome']} ({s42['outcome_eval']})")
    print(f"S5  employee-role Trust     {s42['emp_trust_before']} -> {s42['emp_trust_after']} "
          f"on context 'relationship://qk/cust-cxn?role=employee'")
    print(f"    customer-role Trust     solarworks unTouched = {s42['customer_trust_untouched']} "
          f"(scoped per role, §3.14)")

    # ---- 4.3 two org types + §6 floor ------------------------------------------
    s43 = s4_demo.build_s43(sub)
    print("\n========================== 4.3  TWO ORG TYPES + §6 FLOOR ==========================")
    print(f"org-kind attribute (§3.1):  org://quoteko = {s43['org_kind']['quoteko']}, "
          f"sunsetshelter = {s43['org_kind']['sunsetshelter']}")
    print(f"roles: donor={s43['donor_role']}, beneficiary={s43['beneficiary_role']} on relationship://qk/charity-cxn")
    print(f"S3  orchestrate: reversible steps {s43['reversible_steps']} auto-run")
    print(f"§6  IRREVERSIBLE charitable grant -> {s43['escalation']} -> {s43['human']} (NOT auto-run) -> {s43['grant_executed']}")
    print(f"S4  settle charitable exchange   {s43['settle']}  (pro bono price 0; cost borne by donor, §3.9)")
    print(f"    outcome                      {s43['outcome']}  ({s43['outcome_eval']})")
    print(f"S5  charity-context Trust        {s43['charity_trust_before']} -> {s43['charity_trust_after']} (shelter)")

    # ---- Sprint-4 checks -------------------------------------------------------
    print("\n--- Sprint-4 checks ---")
    for cname in ("s4", "role", "org"):
        print(f"\n  [check:{cname}]")
        fn = {"s4": checks.s4_check, "role": checks.role_check,
              "org": checks.org_check}[cname]
        for name, ok, why in fn(sub):
            allok = allok and ok
            print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")

    print("\n--- Ledger / Graph wiring ---")
    ok, why = sub.ledger.verify()
    print(f"  ledger hash-chain + signatures: {'OK' if ok else why} | entries {len(sub.ledger.entries)}")
    print(f"  graph current-state objects: {len(sub.graph.objects)}")
    allok = allok and ok
    print("\n  [check:roundtrip] full S4 state (whole Graph rebuilds from the whole Ledger, §3.16)")
    for name, ok, why in checks.roundtrip_check(sub):
        allok = allok and ok
        print(f"    [{'PASS' if ok else 'FAIL'}] {name}  — {why}")

    print("\n--- emit fixtures ---")
    for name, path in s4_demo.emit_s4_fixtures(sub).items():
        print(f"  wrote {name} -> file://{path}")

    print("\nRESULT:", "ALL PASS" if allok else "FAILURES PRESENT")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())