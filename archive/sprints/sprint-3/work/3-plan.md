# SPRINT 3 · SUB-SPRINT 3 — Full S1->S5 loop, conformance, spec update

**DoD:** a harness shows the full S1→S5 cycle on one relationship with signed evidence at each
step, and that the S3-executed outcome feeds the S5 Trust update which re-ranks the next S2 match
(closing the loop).

## Build
- `s3_demo.py` chains the whole loop on the relationship `relationship://qk/cust-cxn`:
  1. **S1** identity/role/authz (Sprint-1 substrate) → **S2** intent/match (initial ranking).
  2. First S5 trust cycle (Sprint-2 state: norcrete LATE→0.528, solarworks ON-TIME→0.708)
     → S2 re-ranks solarworks to #1.
  3. **S3 (this sprint):** second engagement on the same relationship — new intent, S2 match
     (solarworks top), commit solarworks, orchestrate across the 3-worker fleet over the routing
     seam, execute the reversible tasks, escalate the irreversible final-payment to
     `person://qk/approver`, human approves, then execute.
  4. **S5 (2nd cycle):** capture the S3-executed solarworks job OUTCOME (on time → good) as
     evidence://, update scoped trust (0.708 → ~0.806), write it.
  5. **S2 re-rank** under updated Trust → solarworks stays #1 (strengthened) — the loop is closed.
- Checks: `s1`, `roundtrip`, `s5`, `flywheel` (run on the Sprint-2 state = unchanged pass) PLUS
  new `s3`, `escalate`, `loop` checks on the Sprint-3 state.

## Verify
- `run_s3_demo.py` → exit 0, ALL PASS; prints every stage with signed evidence.
- `run_s3_conformance.py` → exit 0 over Sprint-0, -1, -2 fixtures AND the new Sprint-3 fixtures
  (reuse the Sprint-0 validator; repoint FIXTURES per generation — non-regression proven by the
  same gate).
- `SPEC.md` updated ONLY for genuine findings → **0.20**, Version/Review Log appended, URI cap +
  frozen ontology intact, section headings re-verified.