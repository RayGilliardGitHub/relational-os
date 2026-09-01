# SPRINT 4 — SUMMARY

**Project:** RelationalOS | **Spec:** v0.20 → **v0.21** | **Date:** 2026-09-01
**Result:** Sprint 4 complete — Exchange & Settlement (S4) built and **verified** end-to-end,
plus the multi-role (customer+employee) and multi-org (private+charitable) extension, with
ONE relationship chained through the full S1→S5 loop on a shared Graph + Ledger and the §6
human floor still gating irreversible settlement. Conformance exits 0 over all FIVE
generations.

## What was built (all under `sprints/sprint-4/artifacts/`)
Extends the Sprint-3 `ros/` package (copied per contract, not a git import) with the S4
service and the extension builders:

- **S4 Exchange & Settlement — `ros/s4.py`.** `settle()` records the exchange per §4b as an
  `event://` (type EXCHANGE) carrying the Asset-Ledger title/custody delta (`asset://`, title
  moves to the provider — a transfer, not a copy), with the payment `obligation://`
  (`VOLUNTARILY_UNDERTAKEN`), `receipt://` (Appendix C §C4), and reconciliation `decision://`
  all riding that SAME signed EXCHANGE event's state. `evaluate()` emits an `event://`
  OUTCOME (met | partial | failed) against the §3.11 Expectation. Also adds
  role-scoped identity (`resolve_role_named`) and role-scoped authority
  (`authorize_for_role`) via a role→authority map on the relationship envelope.

- **4.1 — settle + evaluate on the Sprint-3 end-state.** The committed + executed +
  Trust-updated solarworks job settled (price/value $18,900): signed EXCHANGE event +
  asset // obligation // receipt // reconciliation; `evaluate` → OUTCOME (met); the settled
  OUTCOME fed S5 capture/verify → Trust update (solarworks 0.806→0.904) → S2 re-ranked
  solarworks #1. **The §5 loop closed WITH settlement in the middle.**

- **4.2 — TWO roles on ONE relationship (customer + employee).** The same actor is both
  customer and employee on `relationship://qk/cust-cxn` (§3.2/§C2 — role is an attribute,
  no second identity). Role-scoped authz proven both ways (employee grants
  submit_timesheet/receive_payroll but DENIES request_quote; customer grants request_quote
  but DENIES receive_payroll). Role-scoped Trust keyed `context =
  relationship://qk/cust-cxn?role=employee` (§3.14) — the employee-role Trust rose 0.5→0.598
  while the customer-role Trust (solarworks) stayed untouched at 0.904. A full S1→S5 loop
  for the employee role (payroll micro-task auto-ran; payroll exchange settled; Trust
  updated; next match re-ranked) closed on the same shared Graph + Ledger.

- **4.3 — TWO org types on ONE relationship (private + charitable) + §6 floor.** A private
  for-profit (`org://quoteko`, Purpose FOR_PROFIT) engaged a charitable nonprofit
  (`org://qk/sunsetshelter`, NONPROFIT_CHARITABLE) across the §3.1 org-kind attribute, with a
  purpose-constrained pro-bono offer (price 0, cost borne by the donor — §3.9) and
  jurisdiction-appropriate consent/authority. Full S1→S5 loop with signed evidence; the
  IRREVERSIBLE charitable-grant release (`release_charitable_grant`) escalated to
  `person://qk/approver` and was NOT auto-executed — proven from Ledger ORDER alone
  (`split@52 < esc@55 < hum@56 < release@57`). Charity-context Trust rose 0.5→0.598.

## Verified output (ran this sprint, real tool output)
`python3 run_s4_demo.py` → **exit 0, ALL PASS**:
- All re-used Sprint-1/2/3 checks pass unchanged on the full state (s1, roundtrip, s5,
  flywheel, s3, escalate, loop).
- New Sprint-4 checks: `s4` (8/8: signed EXCHANGE event; obligation+receipt+reconciliation
  ride the signed EXCHANGE event; asset title/custody moved; payment obligation; OUTCOME met;
  solarworks Trust up; next S2 re-rank solarworks #1), `role` (6/6: two roles on one
  relationship; role-scoped authz grants and denies per role; employee-role Trust updated on
  `?role=employee`; customer-role Trust untouched; employee loop closed with S4 in the
  middle), `org` (7/7: org-kind FOR_PROFIT vs NONPROFIT_CHARITABLE; purpose-constrained
  pro-bono offer; charity Trust up; §6 floor gates the irreversible settlement by Ledger
  ORDER; single post-human grant release; human decision signed + alternative-enumerating;
  cross-org loop closed).
- Full-state round-trip: **122 graph objects rebuilt from 64 ledger events** (exit 0).

`<sprint0-venv>/bin/python run_s4_conformance.py` → **exit 0**: Sprint-0 **156**, Sprint-1
**28**, Sprint-2 **35**, Sprint-3 **55**, Sprint-4 **174** instances — ALL PASS, one shared
validator (no regression over any generation).

## What the spec gained (v0.20 → v0.21)
- **URI cap / frozen ontology respected** — no new nouns, no new URI schemes. Schema artifacts
  unchanged (49 `$defs`); validator unmodified.
- Three genuine, additive normative clarifications:
  1. **§4 S4** — every settlement artifact is covered by the signed EXCHANGE event's embedded
     state (full findings F2; the state-delta convention makes "every settlement artifact a
     signed Ledger event" checkable).
  2. **§3.2** — role-scoping a context is a query-qualified URI on the SAME relationship
     scheme (`relationship://…?role=employee`), not a new identity/scheme (F3).
  3. **§3.14** — distinct role-scoped Trust values coexist on the same relationship (F3/F4).
- Full findings: `sprints/sprint-4/notes/findings.md` (F1–F5). Version bumped 0.20→0.21;
  Version/Review Log appended.

## Open issues / notes
- The demo additions' S3 `risk` map was extended additive-only in the copied package (payroll
  + charity-install steps reversible; `release_charitable_grant` irreversible). Deterministic
  local logic only (§G.11); no frontier-API spend (~$0). Single-threaded, no subagents.
- 4.2 and 4.3 each satisfy their sub-DoD on one relationship (1 rel × 2 roles; 1 rel × 2 org
  types); together they satisfy the compressed DoD ("one relationship across two roles and
  two org types") in the harness, both carrying full authenticated/authorized/settled loops.
- Release mirror (`~/Documents/ai-relational-os-spec.md/.pdf`) not re-synced (optional,
  consistent with Sprints 1–3).
- DoD for the FINAL sprint is the Business Operating Layer (Sprint 5): Case, Goal/Metric,
  Task/Work Queue, Exception, Priority/Attention, Dependency, and the §7L cockpit.

## Hand-off
`/home/rlg/relational-os/sprints/sprint-5/PROMPT.md` written and echoed as this sprint's
final message. Ready for a fresh `/new` session to run Sprint 5 (Business Operating Layer)
against the now-**0.21** spec.