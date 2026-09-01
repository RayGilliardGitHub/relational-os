# SPRINT 4 — FINDINGS (feeds the v0.21 spec update)

Collected during the S4 Exchange & Settlement + multi-role / multi-org build (Quoteko scene).
Real tool output only. All executed single-threaded; no subagents; ~$0 local computation.

## F1 — Settlement builds entirely on existing contracts; no schema or ontology extension (confirms §4 S4 / §4b / URI cap)
`settle()` and `evaluate()` run using ONLY the Sprint-0 `$defs` and existing URI schemes:
- **Exchange** = an existing `event://` with `type: EXCHANGE` (the Event `type` enum already
  carries EXCHANGE/OUTCOME); the §4b Asset-Ledger title/custody transfer is recorded as
  `asset://` state (kind MONEY, title moves to the provider — a transfer of title, not a copy).
- **Payment obligation** = an existing `obligation://` (source `VOLUNTARILY_UNDERTAKEN`,
  arising from the AGREED commitment).
- **Receipt** = the existing `receipt://` financial scheme (Appendix C §C4; validates as a
  DomainObject).
- **Reconciliation** = an existing `decision://` (Decision $def: expected vs actual matched).
- **Outcome** = an existing `event://` with `type: OUTCOME`, evaluation met|partial|failed.
The schema (`49 $defs`) and validator are UNCHANGED; conformance re-validates over FIVE
generations: Sprint-0 **156**, Sprint-1 **28**, Sprint-2 **35**, Sprint-3 **55**, Sprint-4
**174** — ALL PASS, exit 0. Identity universal / context relationship-specific (§3.2) and
scoped Trust (§3.14) confirmed end-to-end. No new nouns, no new URI schemes (cap held).

## F2 — "Every settlement artifact is a signed Ledger event" holds via the signed EXCHANGE event's embedded state (additive clarification to §4 S4)
The quietest way to make each settlement artifact signed-history is to carry all of them
(asset, obligation, receipt, reconciliation, exchange event) as the embedded `state_update`
of ONE signed EXCHANGE ledger event — the event's signature covers the whole canonical
payload, so every artifact is signed, and the Graph round-trip reconstructs all of them from
the history (§3.16). **Addressed** by a normative sentence in §4 S4: settlement artifacts are
carried by the signed EXCHANGE event's state per the standard state-delta convention.

## F3 — Role as an attribute extends to TWO roles on ONE relationship with no new identity (§3.2/§C2) — role-qualified context is a query param on the SAME scheme (additive clarification)
The same actor is customer AND employee on `relationship://qk/cust-cxn`; role-scoped
authority is a `role -> authority://` map carried on the relationship envelope
(`authority_by_role`), and role-scoped Trust keys on `context = relationship://…?role=employee`
— a **query param on the SAME relationship scheme** (schema-valid `uri` pattern, catalog-safe,
NOT a new URI). Customer-role Trust (solarworks, roofing claim) and employee-role Trust
(Quoteko, payroll claim) are independent scoped values on the same shared Graph+Ledger.
**Addressed** by a normative sentence in §3.2: role-scoping of a context may be carried as a
query-qualified URI on the same relationship scheme; it is not a new scheme and does not
create a second identity.

## F4 — Organization-kind is an attribute carried by the Purpose `$def` (FOR_PROFIT / NONPROFIT_CHARITABLE), and purpose-constrains the offer (§3.1/§3.9 confirmed)
Actor `$def` has no kind; kind is carried by `purpose://` (Purpose `kind` enum). A private
for-profit (`org://quoteko`) engaging a charitable nonprofit (`org://qk/sunsetshelter`)
carries the relationship across the kind attribute, with a purpose-constrained pro-bono offer
(price 0; cost borne by the donor — Value/Cost/Price, §3.9). No spec change; confirms the
existing model.

## F5 — The §6 human floor still gates IRRREVERSIBLE settlement between org types, auditable from Ledger ORDER alone (confirms, no change)
The charitable-grant release (`release_charitable_grant`, irreversible/unknowable-cost) was
NOT auto-executed — the signed event ORDER on the append-only Ledger proves it
(`split@52 < esc@55 < hum@56 < release@57`): the irreversible ACTION sits strictly after the
approver's signed human DECISION, which follows an escalation DECISION. Same auditable-order
property as Sprint 3 (F4), now demonstrated for cross-org settlement. The copied S3 `risk`
map was extended additive-only with the scenario actions (payroll + charity install steps
reversible; `release_charitable_grant` irreversible).

## Net spec impact (v0.20 -> v0.21)
- URI cap and frozen ontology: **unchanged, respected** — no new nouns, no new URI schemes.
- Schema (`sprints/sprint-0/artifacts/schema/`): **NOT extended**; validator unchanged
  (still v0.17 artifacts, 49 $defs). Conformance over all five generations exits 0.
- Three additive normative clarifications:
  1. §4 S4 — every settlement artifact is signed via the signed EXCHANGE event's embedded
     state (F2).
  2. §3.2 — role-qualified context may be a query param on the same relationship scheme,
     not a new identity/scheme (F3).
  3. §3.14 — role-scoped Trust confirmed: distinct scoped values (subject,target,claim,
     context[?role]) coexist on the same relationship (F3/F4).
- Version bumped to **0.21**; Version/Review Log entry appended.