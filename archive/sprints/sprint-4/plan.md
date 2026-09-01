# SPRINT 4 — PLAN (Settlement S4 + multi-role / multi-org extension)

**Spec:** v0.20 → v0.21 (target) | **Session:** fresh, memoryless | **Rule:** single-threaded, real tool output only.

## Objectives
Implement §4 S4 Exchange & Settlement (`settle`, `evaluate`) on the Sprint-3 loop end-state,
then extend the loop from customer to a second role (employee) and from private orgs to a
charitable org — carrying ONE relationship through the full S1→S2→S3→S4→S5 loop across TWO
roles and TWO org types, with the §6 human floor still gating irreversible settlement.

## Sub-sprints (each: plan → build → verify)
- **4.1 — S4 settle + evaluate (one relationship).** On the committed + executed + Trust-updated
  solarworks job: record the EXCHANGE as a signed `event://` (type EXCHANGE, §4b Asset Ledger
  title/custody transfer), produce a signed payment obligation (`obligation://`), a receipt
  (`receipt://`), and a reconciliation (`decision://`), then `evaluate()` against the §3.11
  Expectation → a signed OUTCOME `event://` (met|partial|failed) that feeds S5 `capture`/`update`
  → S2 re-ranks. Loop closes WITH settlement in the middle.
- **4.2 — Multi-role (TWO roles on ONE relationship).** The same relationship
  `relationship://qk/cust-cxn` spans customer AND employee roles for the same actor (§3.2,
  §C2: role is an attribute). Role-scoped identity (`resolve_role`), role-scoped authority
  (`authorize_for_role`), and role-scoped Trust keyed `(subject,target,claim,context[?role=…])`
  (§3.14, not a single score). Run a full S1→S5 cycle for the *employee* role and show the
  scoped Trust values are distinct from the customer-role values on the same shared Graph+Ledger.
- **4.3 — Multi-org (TWO org types per relationship).** A private for-profit
  (`org://quoteko`) engages a charitable nonprofit (`org://qk/sunsetshelter`) across the §3.1
  organization-kind attribute (Purpose objects FOR_PROFIT vs NONPROFIT_CHARITABLE),
  purpose-constrained offer/obligation, jurisdiction-appropriate consent/authority. Full
  S1→S5 loop with signed evidence; the IRREVERSIBLE charitable-grant settlement MUST escalate
  to `person://qk/approver` before execution (§6 floor) — proven by Ledger event ORDER.

## Definition of Done
- `artifacts/` holds the extended `ros/` package (`s4.py`), the 4.2/4.3 builders, a demo runner
  and a conformance runner, with **real tool output** (exit 0, ALL PASS).
- Full S1→S2→S3→S4→S5 loop chains ONE relationship across TWO roles (4.2) and TWO org types
  (4.3), signed evidence at every step, §6 human floor gating the irreversible settlement.
- Sprint-0 conformance still exits 0 over ALL FIVE fixture generations (Sprint-0/1/2/3/4).
- `SPEC.md` updated from genuine findings (bumped to 0.21, Version/Review Log appended),
  URI cap / frozen ontology respected.
- `summary.md` written; `sprints/sprint-5/PROMPT.md` written and echoed as the final message.

## Constraints
URI cap + frozen ontology (§7J.11/§C16): NO new URI schemes, NO new nouns. Represent S4 with
existing schemes only: Exchange/Outcome as `event://` (type EXCHANGE/OUTCOME), payment
obligation as `obligation://`, receipt as `receipt://`, reconciliation as `decision://`,
title/custody via `asset://`. Role-qualified context = `relationship://…?role=…` (same scheme,
query param — schema-valid, catalog-safe). Deterministic local logic only (§G.11, no
frontier-API spend). Single-threaded, no subagents. Touch nothing outside
`/home/rlg/relational-os/` except reading the `~/Documents` mirror.