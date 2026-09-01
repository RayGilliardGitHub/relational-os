# 2.1-PLAN — S5 capture + verify (one outcome class)

## Goal
Prove the front of the S5 loop: turn a raw outcome into **signed evidence://**, then
verify a **claim://** against that evidence per §3.17 — degree Y under procedure Z,
never a capital-T "truth".

## Design
Outcome class (ONE crisp, objective): **"contracting roofing job completed by its
committed deadline (on-time completion)"** — verifiable by an anchored completion
record (`actual_completed_at` vs `committed_deadline`). Two instances in the Quoteko
customer relationship `relationship://qk/cust-cxn`:
- `org://qk/norcrete` — completed **late**  → not on time (outcome 0.0)
- `org://qk/solarworks` — completed **on time** → on time (outcome 1.0)

This choice exercises both signs of the trust flywheel on two contractors that share
the same fit and claim (so the re-rank in 2.3 is purely Trust-driven).

## Steps (in `artifacts/ros/s5.py`)
1. `_ev(...)` event builder consistent with Sprint-1 `make_fixtures` (universal tracer
   fields, `state_update` embedded).
2. `capture(sub, outcome, provenance, signer) -> (evidence_obj, on_time)`:
   build an anchored completion Event (type OUTCOME) + an `evidence://` object
   (`kind=ANCHORED`, `source`=provenance source, `verity{procedure,confidence}`,
   `captured_at`); record both as a signed OUTCOME ledger event; return the evidence
   + objective on_time flag.
3. `make_expectation(...)` → `expectation://` per §3.11 (subject, condition, metric,
   threshold, deadline, evidence_required).
4. `verify(evidence_obj, statement) -> verified` — returns
   `{claim, degree, procedure, supported}` with `degree = verity.confidence`,
   `procedure = verity.procedure`. Explicitly returns a degree + procedure, not a
   boolean truth declaration (§3.17).
5. `outcome_score(on_time) -> float` — 1.0 if on time else 0.0 (objective).

## Done
- Real `evidence://`, `expectation://`, `claim://`, and OUTCOME `event://` produced and
  signed on the shared Graph + Ledger; `verify` returns a bounded degree + procedure;
  the verified `claim://` references the `evidence://` and the relationship context.
- Capture + verify run in the harness with real output.