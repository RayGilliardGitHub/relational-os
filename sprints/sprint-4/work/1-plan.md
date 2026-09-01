# Sprint 4 — work/1-plan (4.1: S4 settle + evaluate, one relationship)

**Input:** Sprint-3 end-state: solarworks job committed + executed + Trust raised to 0.806
(`build_s3`). Reused Sprint-0 schema/validator + Sprint-1/2/3 `ros/` substrate.

**Design — S4 with existing schemes only (no new URI, no new noun):**
- **Exchange** → `event://` with `type: EXCHANGE`; carries the §4b Asset-Ledger title/custody
  delta as `state_update` (`asset://money/…` title moves towards the provider). Envelope fields
  carry §3.9 Value/Cost/Price + settled amount/currency.
- **Payment obligation** → `obligation://` (source VOLUNTARILY_UNDERTAKEN, since it arises from
  the AGREED commitment), subject = the payer, `due_by`.
- **Receipt** → `receipt://` (Appendix C financial scheme; validates as DomainObject).
- **Reconciliation** → `decision://` (Decision $def) matching expected vs actual settled value.
- **Outcome** → `event://` with `type: OUTCOME`, evaluation met|partial|failed against the §3.11
  Expectation.

**Loop closed with settlement:** `evaluate()` OUTCOME → pass as outcome to S5 `capture()`
(anchored evidence) → `verify()` → `update_trust()` (solarworks rises past 0.806) → S2
`match_offers` re-ranks (solarworks stays #1).

**Checks (4.1):** settle produced a signed EXCHANGE event + obligation:// + receipt:// +
reconciliation decision://; evaluate produced a signed OUTCOME (met); the OUTCOME fed an S5
Trust update (solarworks up); next S2 re-rank closed the loop with settlement in the middle;
every graph object reconstructs from ledger `state_update` (roundtrip).