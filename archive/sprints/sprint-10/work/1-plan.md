# SPRINT 10 — WORK 1 — Build the conflicting-interest experiment runner

## Goal
Write `instances/contested_reality/run_interest_conflict_demo.py` — a self-contained engine (sharing the
Sprint-9 substrate/S5 pattern) that models the remote-work conflict (Scenario B), flags the interest
collision under the shared SLA/staffing/policy constraint, opens a `case://`, records uncertainty,
adjudicates to a defensible determination (middle option) AND to UNRESOLVED, and runs a signed appeal
re-adjudicated by a higher authority.

## Design decisions (additive, no new noun)
- **Interests** = additive `interest` objects on the parties' `relationship://` objects (employee's
  remote-work interest on `relationship://ic/employment`; manager's coverage interest on
  `relationship://ic/contract`). Each carries explicit `stake`, `wants`, `legitimate`, `within_policy`.
- **Shared constraint** = additive `constraint` object on the contract relationship: the 30-min SLA
  (`expectation://ic/sla`), the staffing floor, and the conditional remote-work `policy://ic/remote`.
  Both parties are bound by the same constraint object (chosen scope is the contract relationship).
- **Conflict detection** = deterministic: employee wants remote; manager's binding SLA+floor require
  on-site coverage today; remote-with-no-coverage-plan violates the floor → collision flagged.
- **Case** = `case://ic/remote-conflict` (status OPEN), carrying an additive `conflict` object that
  lists both interests, the constraint, the flag, and the recorded uncertainty (`uncertainty` string).
- **Adjudication** = authorized Manager (authority `authority://ic/adjudicate-remote`, grant
  `determine_remote_arrangement`) decides among {side-employee, side-manager, remote-with-coverage-plan,
  UNRESOLVED}. Two branches:
  - Branch A: the manager chooses the **defensible middle** → remote-with-coverage-plan (employee remote
    3 days/wk + uses 2 unused-leave days; manager guaranteed on-site coverage on the 2 required days to
    meet the SLA). Signed by the adjudicator.
  - Branch B: a variant where staffing data is insufficient/unknown → **UNRESOLVED** (inviolable rule),
    Trust untouched.
- **Appeal** = after Branch A's determination, the employee appeals via `right://ic/emp-appeal`
  (type=APPEAL). The appeal is a **first-class signed event** (`event://ic/appeal`) plus an additive
  `appeal` object recording requester, target determination, ground, status=OPEN→REVIEWED. It is
  **re-adjudicated** by a higher authority (`person://ic/director`, authority `authority://ic/for-appeal`)
  — NOT a silent redo. The director affirms the coverage-plan but grants the employee's leave-use
  explicit (a negotiated adjustment), recorded as a new shared `decision://ic/appeal-decision`.
- **Authority preserved** → every determination/decision carries `authority` + `by` and is signed on the
  ledger (substrate `record(..., signer)`).
- **Schema-safe:** additive fields never use keys ending in `at|time|deadline|expires|expiry|effective|
  due|since` (C2 temporal probe). Use `stake`, `wants`, `coverage_floor`, `response_target_minutes`,
  `arrangement_days`, etc. No new `$def`, no scheme, 49 `$defs` intact, SPEC stays v0.22.

## Conformance
Fork `conformance_dispute.py` → `conformance_interest.py`, pointing `FIXTURES` at the new artifacts dir.
Emit fixtures/ledger/graph with the same grouping pattern so C1–C5 validate the additive fields.