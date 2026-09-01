# SPRINT 29 — work/3-plan.md  (docs + finalization)

## Prior state
- Runner + engine done (work/1-plan.md, work/2-plan.md): `record_capacity_requirements` recorder +
  `_per_option_capacity_flags` helper + the additive Q7/Q8 `capacity_constraint` extension; new
  `run_forecast_per_option_capacity_demo.py` ALL PASS (88 PASS); new-org fixtures pass C1–C5; full
  non-regression green.

## This step
1. Roll forward the docs:
   - `docs/ENGINE-FORECAST-CAPACITY.md` + a §13 (per-option capacity_infeasible).
   - `docs/ENGINE-S7L-COCKPIT.md` + a §11 (Q7/Q8 capacity_constraint per-option label).
   - `instances/README.md` Sprint-29 entry.
   - `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after Sprint 29".
   - The `relational-os` skill's project-note line for Sprint 29 (already captures the frontier).
2. Write `sprints/sprint-29/notes/findings.md` + `sprints/sprint-29/summary.md`.
3. Write the next self-contained prompt at `sprints/sprint-30/PROMPT.md`: the frontier after Sprint 29
   is that per-option infeasibility is now labelled FROM recorded requirements, but the marker never
   CHOOSES / re-ranks, and a per-option requirement not unit-coupled to the capacity stays
   non-derivable.

## Execution
- Verify each doc append landed on the correct unique anchor (re-read after a paged-doc patch — the
  STRESS-TEST "out of" duplication pitfall).
- Final full non-regression re-run to confirm all green; schema hash `7fc38c8c…`; 49 `$defs`; SPEC
  v0.22; `ros/` + schema + configs untouched; ONLY `adjudication_engine.py` modified among committed
  source.