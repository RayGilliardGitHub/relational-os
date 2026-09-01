# SPRINT 29 — work/2-plan.md  (build run_forecast_per_option_capacity_demo.py)

## Prior state
- Engine change (work/1-plan.md) done: `record_capacity_requirements` recorder + `_per_option_capacity_flags`
  helper + the additive Q7/Q8 `capacity_constraint` block extension; 5 reused orgs still byte-identical.

## This step
Write `run_forecast_per_option_capacity_demo.py` (new, exit 0 = ALL PASS) that:
1. Rebuilds the five Sprint-28 orgs byte-identically via `r26.build_orgs()` (fc, vm, vmc, fl2, deli).
2. Builds two NEW orgs on fresh Substrates that RECORD per-option requirements:
   - `deli-infcap`: DELI relabeled; same VM whole-series band (VM_POINTS, band_variance "all", sigma
     0.18, horizon {0.62,1.02}); `record_capacity(value=500.0, unit="resolutions/day", load=1.3)`;
     `record_capacity_requirements` = {accept-customer-refund:499.0, accept-company-full-payment:499.0,
     external-adjudication:499.0, partial-settlement:200.0, conditional-resolution:200.0,
     request-more-evidence:50.0, escalate:100.0} (baseline `unresolved` NOT recorded). available =
     500.0−1.3=498.7; the three 499.0 options > available -> `capacity_infeasible`; the rest → risk.
     `_capacity_reason` = at-capacity (load 1.3 >= 1.0).
   - `deli-deficit-inf`: DELI relabeled; lower-is-better CO latency series (sigma 8, horizon {12,32});
     `record_capacity(value=30.0, unit="resolutions/day", load=0.9)`; `record_capacity_requirements` =
     {external-adjudication:30.0, accept-company-full-payment:30.0, accept-customer-refund:30.0,
     partial-settlement:20.0, conditional-resolution:20.0, request-more-evidence:10.0, escalate:15.0}.
     available = 30.0−0.9=29.1; the three 30.0 options > available -> `capacity_infeasible`; the rest →
     risk. `_capacity_reason` = deficit (horizon high 32.0 >= capacity value 30.0).
3. Asserts, per items (a)–(g) of plan.md.

## Assertion design (exact deli set)
deli options (8): accept-customer-refund, accept-company-full-payment, partial-settlement,
conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication.
baseline = "unresolved". floor_gated = {accept-customer-refund}, penalty 0.20 → machine-eligible best
and Q8 recommendation = partial-settlement (UNCHANGED). non_baseline = the 7 others.

## Non-headroom / per-option executions to assert
- For both NEW orgs: `capacity_constraint` present on q7 AND q8 (identical), `reason` ==
  at-capacity / deficit, `flag` True, `options_flagged` = {3 capacity_infeasible, 4 capacity_risk},
  baseline NOT in options_flagged, `per_option_requirements` == the recorded dict, `available_capacity`
  == 498.7 / 29.1, and the constraint reason AGREES with the Q9 `capacity_planning_attention` label
  BY CONSTRUCTION.
- Reproducibility assertion: for each NEW org, every `capacity_infeasible` option's recorded
  requirement > available (computed in the runner), every `capacity_risk` option's requirement <=
  available, baseline absent.
- (d) LABEL: for every org (all 7, incl. the two infeasible ones), q7.options (count 8 + uris) +
  q7.machine_eligible_best + q8.recommendation + q8.floor_gated EXACTLY equal to `cockpit_q7q8`;
  q8.recommendation still `partial-settlement` / machine-eligible best `partial-settlement` even when
  SOME option is infeasible.
- (b) Sprint-28 byte-identity on the 5 reused orgs (headroom org still `{reason:"headroom",
  options_flagged:{}}`; 4 no-capacity orgs carry NO `capacity_constraint`; Q3 suffix + Q9
  capacity_planning_attention unchanged).
- (f) determinism (dict + render) on all 7; (g) emit fixtures (incl. the 2 new orgs) + report
  `cockpit-forecast-per-option-capacity.md`.

## Recorded-data provenance
- `deli-infcap` available 498.7 = 500.0 (recorded capacity value) − 1.3 (recorded load); each
  infeasible option's 499.0 is a RECORDED requirement; each risk option's requirement is RECORDED;
  reason from recorded load/band/capacity via the frozen `_capacity_reason`.
- `deli-deficit-inf` available 29.1 = 30.0 − 0.9; infeasible options record 30.0 (> 29.1);
  reason from horizon worst-side high 32.0 >= capacity value 30.0.

## Execution
- Run `python3 run_forecast_per_option_capacity_demo.py` -> RESULT: ALL PASS, exit 0.
- Emits fixtures + report. Then full non-regression re-run is the NEXT step (work/3-plan.md).