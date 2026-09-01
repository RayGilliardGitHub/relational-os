# SPRINT 34 — work/2-plan: build + run the whole-catalog two-path survey runner

## Goal
Write `run_two_path_catalog_demo.py`: build the 22-org ORG CATALOG fresh in memory (reusing the existing
runner builders/constants — every org is already constructed by an existing CR runner, NOT invented), emit a
`two_path_surface` + PATH class per org (reusing the Sprint-33 `_classify`/`_surface`/`_gated_set`), and
assert the four properties over the WHOLE catalog. Emit `artifacts/adjudication/reports/two-path-catalog.md`.
No engine / no `capacity_rerank.py` / no schema / no SPEC change.

## Catalog construction (build fresh in memory; reuse existing builders — no fixture writes)
- **13-org set**: `r32.build()` (run_capacity_rerank_demo) → deli-forecast, deli-varmax, deli-varmax-cap,
  deli-flat2, deli, deli-infcap, deli-deficit-inf, deli-recommend-infcap, inspect-recorded, cove-recorded,
  inspect-nodata, cove-recommend-infcap, deli-all-infeasible.
- **deli-forecast-flat, deli-cost, deli-cost-flat**: reconstruct exactly as `run_forecast_direction_demo`
  (relabel DELI + `run_one` + `record_series` with the SAME points/fields/direction constants).
- **deli-atcap, deli-deficit**: `run_forecast_horizon4_demo.build_orgs()` keys atcap/deficit.
- **inspect-corroboration, inspect-learn-b, deli-learn**: replicate `run_cockpit_s7l_demo`'s learned-rule
  construction (learn_threshold from LEARN_HYPER + build_learned_library_spec + RULE_LIBRARY inject +
  INSPECT_BATCH_B reconcile + record_learned_rule on inspect-learn-b's own ledger).
- **cove**: the base COVE config (SCENARIOS) through `run_one(ac.COVE)`.

## Assertions over the whole catalog (r33._surface / _classify reused)
- (a) advisory never shadowed: every org's advisory Q8 == `cockpit_q7q8`; needed=True orgs → replacement ≠
  advisory Q8 ≠ machine_eligible_best; needed=False orgs (all, incl. no-capacity) → replacement == advisory Q8.
- (b) exhaustive-disjoint: every org exactly one PATH class; needed == (path == RE-RANK); no-capacity orgs
  carry no capacity_constraint block.
- (c) floor integrity: no advisory Q8 nor re-rank replacement is floor-gated vs `rank` (22/22).
- (d) determinism-vs-history: two_path_surface deterministic on re-run (22/22); Sprint-31 tally 11/11;
  Sprint-32 re-rank results (4) reproduced; Sprint-33 13-org taxonomy {5,4,4} reproduced.

## Expected whole-catalog distribution (asserted, not assumed): 12 ADVISORY-no-capacity / 6
## ADVISORY-best-runnable / 4 RE-RANK = 22.