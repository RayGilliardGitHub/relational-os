# SPRINT 5 — SUB-SPRINT 5.3 PLAN  (The Cockpit + §7L answered with evidence)

## Goal
Produce the **cockpit** output for Quoteko: business health, prioritized attention (the
"seven things today", §7J.2), and an **AI recommendation carrying the authority it
requires** (§7J.9). Answer the **§7L ten morning questions** with cited ledger/graph
evidence; §7L #8 becomes **assigned, authorized Task** work that closes in a **verified,
learned outcome** (#10); #9 (who does it + authority/capacity) and #10 (did it work +
learning) are answered.

## What will be built
- `cockpit_generator()` — renders the Monday-morning screen from the ledger/graph:
  - **Business-health panel** (metrics: target/actual/variance/status) — from 5.2.
  - **Prioritized attention** — ordered list of exceptions/cases/tasks with priority.
  - **AI recommendation** (#8) with the authority required (delegation/authority refs).
- `answer_ten(bolt)` — a structured, evidence-cited answer to each §7L question. Q6 uses
  forecast ("if nothing changes", §7K.1); Q7 lists options incl. do-nothing + trade-off;
  Q8 -> the assigned Task; Q9 owner + authority + capacity; Q10 verified outcome + Learning.
- Written report artifacts: `artifacts/reports/cockpit.md` + `cockpit.json`.

## Verification (5.3 DoD)
`cockpit_check` asserts: health panel present; attention is priority-ordered; the #8
recommendation is a real assigned `task://` with an authority/delegation; #10's verified
outcome + Learning entry exist on the ledger; the report file was written. Conformance
over all SIX generations exits 0.

## Outputs
`file:///home/rlg/relational-os/sprints/sprint-5/artifacts/reports/cockpit.md` and
`cockpit.json`; `run_s5_demo.py` prints the cockpit screen + the ten answers.