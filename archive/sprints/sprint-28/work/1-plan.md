# SPRINT 28 — work/1-plan.md  (build run_forecast_horizon4_demo.py)

## Prior state
- plan.md written; green baseline established (all demos + conformances exit 0; 49 $defs; schema
  JSON hash `7fc38c8c0a6e5b76cd55393f2c732417675b224812970951778853a6677642c4`).
- The engine needs NO change: `_capacity_reason` (deficit > at-capacity > headroom) and the Q7/Q8
  `capacity_constraint` block already implement all three branches; Sprint-27 only proved headroom
  on a real org. This build is recorded data + a runner.

## This step
Write `run_forecast_horizon4_demo.py` (new, exit 0 = ALL PASS) that:
1. Rebuilds the five Sprint-26/27 orgs byte-identically via `r26.build_orgs()` (fc, vm, vmc, fl2,
   deli) — the reused default/headroom/no-capacity/no-band/no-data orgs.
2. Builds two NEW orgs on fresh Substrates:
   - `deli-atcap`: DELI relabeled; record series `metric://deli-atcap/m-on-time` with the SAME 4
     VM points (higher-is-better, band_variance:"all" -> horizon {0.62,1.02}, sigma 0.18) +
     `record_capacity(value=500.0, unit="resolutions/day", load=1.25)` -> reason **at-capacity**.
   - `deli-deficit`: DELI relabeled; record series `metric://deli-deficit/m-latency` with the
     Sprint-23 CO points (lower-is-better, band_variance:"all" -> horizon {12.0,32.0}, sigma 8,
     mean_delta 2 -> projections [20,22,24]) + `record_capacity(value=30.0, unit="resolutions/day",
     load=0.9)` -> horizon worst-side high 32.0 >= capacity value 30.0 -> reason **deficit**.
3. Asserts, per items (a)–(g) of plan.md:
   - (a) full §7L Q1–Q10 cockpit + evidence on all 7 orgs;
   - (b) Sprint-27 byte-identity: the headroom org still `reason:"headroom", options_flagged:{}`;
     the 4 non-capacity orgs carry NO `capacity_constraint`; Q3 horizon suffix + Q9
     capacity_planning_attention unchanged on the reused orgs;
   - (c) non-headroom block fully exercised: `deli-atcap` reason=="at-capacity", `deli-deficit`
     reason=="deficit", flag True, `options_flagged` marks EVERY capacity-consuming non-baseline
     option `capacity_risk`, baseline never flagged, and the reason AGREES with each org's Q9
     `capacity_planning_attention` label BY CONSTRUCTION;
   - (d) marker is a LABEL: for every org (incl. the two non-headroom), q7.options (same count/uris)
     + q7.machine_eligible_best + q8.recommendation + q8.floor_gated EXACTLY equal to
     `cockpit_q7q8` both when capacity_constraint is absent and when it is present (no §6 overrule);
   - (e) superset byte-identity: capacity orgs' Q7/Q8 pre-existing keys intact; every
     capacity_constraint value traces to a recorded field (recorded capacity/load, band_horizon,
     recorded threshold);
   - (f) determinism (dict + render) on all 7 orgs;
   - (g) emit fixtures for the recorded orgs (incl. the 2 new) + `cockpit-forecast-horizon4.md`.

## Non-headroom baseline-vs-flag design (must NOT re-rank)
For deli (DELI config) the options are: accept-customer-refund, accept-company-full-payment,
partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved,
external-adjudication. baseline = "unresolved" (contains "unres"). floor_gated =
{accept-customer-refund} + floor_penalty 0.20. machine-eligible best (top non-gated, highest
utility) = partial-settlement; Q8 recommendation = partial-settlement. These are UNCHANGED by the
capacity_constraint block — assert q7.options == ["...8..."] (8 uris), machine_eligible_best ==
partial-settlement, q8.recommendation == partial-settlement, and options_flagged = every option
EXCEPT "unresolved" = 7 keys all "capacity_risk" (baseline unresolved NOT flagged).

## Recorded-data provenance (a–g proof)
- at-capacity: flag from `load 1.25` recorded; band from recorded VM point variances; capacity
  value 500.0 recorded. reason arithmetically reproduced in the runner.
- deficit: band_horizon.high 32.0 = max over period (projected + sigma) from recorded CO points;
  capacity value 30.0 recorded; 32.0 >= 30.0 -> deficit.

## Execution
- Run `python3 run_forecast_horizon4_demo.py` -> expect RESULT: ALL PASS, exit 0.
- Do NOT touch the engine file. Re-run the full non-regression demo list to confirm unchanged.
- Doc roll-forward is the NEXT work step (work/2-plan.md).