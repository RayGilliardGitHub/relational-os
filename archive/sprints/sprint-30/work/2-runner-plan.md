# work/2-runner-plan.md — write the new runner `run_forecast_label_vs_choice_demo.py`

## Design (no engine change needed)
Sprint 29's `_per_option_capacity_flags` already labels ANY option (including the recommended one)
`capacity_infeasible` when its recorded requirement > available. So this sprint is pure recorded data +
a new runner + the boundary proof + docs. `adjudication_engine.py` stays byte-identical (hash a60f8f7…).

## New org `deli-recommend-infcap` — exact recorded numbers
DELI relabeled (partial-settlement = machine-eligible best, utility 0.7275, non-gated).
- `record_metric_series`: the Sprint-28/29 whole-series VM points (`rfh.VM_POINTS`), `band_variance:"all"`,
  target 0.95, higher-is-better -> horizon band {0.62, 1.02}.
- `record_capacity(value=500.0, unit="resolutions/day", load=1.3)` -> at-capacity (load 1.3 >= 1.0).
- `record_capacity_requirements` = {partial-settlement:499.0, conditional-resolution:200.0,
  accept-customer-refund:200.0, accept-company-full-payment:200.0, external-adjudication:100.0,
  request-more-evidence:50.0, escalate:80.0}.
  AVAILABLE = 500.0 − 1.3 = **498.7**. **only `partial-settlement` (499.0 > 498.7) -> `capacity_infeasible`**;
  the other 6 (<= 498.7) -> `capacity_risk`; baseline `unresolved` (no recorded requirement) -> NEVER flagged.
  `_capacity_reason`: load 1.3 >= 1.0, worst-side low 0.62 < 500.0 (not deficit) -> **at-capacity**, flag True.

## Assertions (ALL PASS = the sharpest label-vs-choice proof)
1. On `deli-recommend-infcap`: `capacity_constraint.options_flagged["partial-settlement"] ==
   "capacity_infeasible"` (the RECOMMENDED option itself), 6 `capacity_risk`, baseline absent,
   `reason == "at-capacity"`, `available_capacity == 498.7`, `per_option_requirements` == the recorded map.
2. Q8 `recommendation == "partial-settlement"` AND `q7.machine_eligible_best == "partial-settlement"` AND
   the four keys (options count 8 + uris, machine_eligible_best, recommendation, floor_gated) EXACTLY equal
   `cockpit_q7q8` — even though options_flagged marks the recommended option infeasible.
3. `capacity_constraint.note` names the UNCHANGED Q8 + the §6 human (marker labels "recommended option can't
   run"; it does NOT choose a replacement).
4. `reason` == Q9 `capacity_planning_attention` label BY CONSTRUCTION.
5. Byte-identity regression: reuse `r29.build_orgs()` (all 7 Sprint-29 orgs) and assert the reused orgs
   carry EXACT Sprint-29 output (`deli-infcap`/`deli-deficit-inf` byte-identical; `deli-varmax-cap`
   `{reason:"headroom", flag:False, options_flagged:{}}` no per-option keys; 4 no-capacity orgs no
   `capacity_constraint`; Q3 horizon + Q9 unchanged).
6. Determinism (dict + render) for all 8 orgs.
7. Emit fixtures for the new org + `artifacts/adjudication/reports/cockpit-label-vs-choice.md`.

Reuse imports: `run_forecast_per_option_capacity_demo as r29` (its `_new_per_option_org`/builders),
`run_forecast_horizon_demo as rfh`, `adjudication_configs as ac`, `adjudication_engine as eng`.