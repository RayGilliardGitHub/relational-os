# 1.2 PLAN — S2 Intent / Matching (minimum, one domain)

**Spec refs:** §4 S2, §5 (the loop, Trust-weighted matching), §3.14 (scoped Trust),
§7B/§3.19 (human-escalation floor), §3.11 (Expectation for human verification),
Appendix C `offer://`, `service://`; sprint-0 schema.

## Goal
Implement `infer_intent` + `match_offers` for **role=customer**, **domain = Quoteko
quoting/triage**, for fictional `org://quoteko`. Produce ranked matches as **signed
Events** on the shared Ledger; a human verifies (acknowledges) before the match
becomes current state.

## Design
- `artifacts/ros/s2.py`:
  - `infer_intent(subject, evidence)` — from the customer's evidence (a request text +
    context) produce an intent signature (need + capability keys + urgency). Stored as
    part of an `interaction://` (REQUEST) and a `decision://` (intent inference is a
    Decision, per §3.12 — no new URI noun).
  - `match_offers(intent, offers, trust_scores)` — Trust-weighted per §5: for each
    candidate `offer://`, score = fit(intent∩capability) × Trust(subject→provider,
    claim, context), in [0,1]. Return ranked matches. Reject offers below a trust
    floor. **Each match is a signed Event** (type DECISION) on the ledger.
- Human-escalation floor: the ranked candidate is presented to a **human** (customer)
  who acknowledges/accepts via a signed Acknowledgement event `event://…/human-verify`
  (type DECISION, by `person://qk/customer`, an Acknowledgement category). Only after
  this is the match's status committed as current state on the Graph. (Irreversible
  commitment — hiring a contractor — is exactly the case that warrants the floor.)
- Trust-weighted re-rank is visible: two contractors with same capability but
  different Trust yield different order, demonstrable in output.

## DoD (1.2)
- Runnable test `run_s2_demo.py` executes the cycle
  `identity → role → intent → matched offer → human-verified → on the ledger` and prints
  every step + the ranked matches with their trust-weighted scores.
- The resulting ledger + graph + objects validate under Sprint-0 conformance (exit 0).
- Human verification is recorded (a real signed event), not simulated away.