# Sprint 4 — work/3-plan (4.3: TWO org types per relationship + §6 floor)

**Input:** 4.2 end-state.

**Design — cross-org relationship carried across the §3.1 org-kind attribute:**
- New relationship `relationship://qk/charity-cxn` between private for-profit `org://quoteko`
  (donor) and charitable nonprofit `org://qk/sunsetshelter` (beneficiary). Org-kind carried as
  Purpose objects (`purpose://qk/pv-quoteko` FOR_PROFIT, `purpose://qk/pv-shelter`
  NONPROFIT_CHARITABLE).
- **Purpose-constrained offer/obligation:** charitable pro-bono offer (price $0; §3.9 Value/Cost
  /Price — cost borne by donor, value to the mission). Obligation VOLUNTARILY_UNDERTAKEN.
- **Jurisdiction-appropriate consent/authority:** `consent://` for the charitable use + donor/
  beneficiary authorities within the charity relationship context.

**Full loop across two org types:** S1 roles + authorize in charity context → S2 intent/match
(solar install at the shelter, scoped Trust) → S3 commit + orchestrate (reversible install
steps auto-run across a worker fleet) + the IRREVERSIBLE **charitable-grant release** escalates
to `person://qk/approver` (§6) → human acknowledges → then executes → S4 settle the charitable
exchange (EXCHANGE + grant obligation + receipt + reconciliation) → S5 capture/verify → charity-
context Trust update → S2 re-ranks.

**§6 floor proof (4.3):** like Sprint 3, from Ledger ORDER alone — `split < esc < hum <
release` — the irreversible cross-org settlement was NOT auto-executed; it ran only after the
approver's signed human DECISION. The floor still gates irreversible settlement between org
types.

**Checks (4.3):** two org kinds present on one relationship; purpose-constrained offer; full
loop closed; irreversible grant settlement gated by the human floor (Ledger order asserted).