# Sprint 21 — work/2-build: engine additive closure

## Step A — module-level numeric helper
Add after the imports (no function name collisions — check none exists). `_num(x)` -> float or None.

## Step B — refactor `cockpit_s7l` Q6 block to reuse `_recorded_metric_with_series` + `forecast_metric`
Current Q6 block (lines ~915-930) calls `_recorded_metric_with_series(sub)` then `forecast_metric`.
Refactor to compute ONCE, stored in a local `fc_state`, used by BOTH Q6 and the new Q3/Q8 closure so the
two agree by construction.

## Step C — Q3 forecast-driven attention (inside `.q3` construction)
If `series_uri` is set and `min(projected) < threshold`, append:
   {"item": series_uri, "why": "forecast: projected to fall below <threshold> (<src>) — worst <min>
   at period <H>", "tag": "forecast"}
Ensure `q3` count reflects it.

## Step D — Q8 / trade-off do-nothing expected-impact
After `base = cockpit_q7q8(...)` and when a recorded series exists, add additive fields to `base["q8"]`
and `base["q7"]` (do NOT call cockpit_q7q8 differently — just enrich its returned dicts):
   base["q8"]["forecast"] = {...}
   base["q8"]["do_nothing_expected_impact"] = {...}
   base["q7"]["tradeoff_do_nothing_impact"] = <summary string> (rendered line)
Keep them ABSENT when no series (no-data fallback unchanged).

## Step E — render_cockpit_s7l
- Q3 line: already iterates prioritized items; make sure it shows the forecast item's tag/why
  (the existing generic `item — why` already renders it; add an explicit marker if useful).
- Q8 / trade-off: append a line carrying the projected do-nothing cost when `base["q8"]` has
  `do_nothing_expected_impact`.

## Frozen functions — DO NOT TOUCH
`reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`, `rank`, `machine_eligible_best`,
`render_tradeoff`, `cockpit_q7q8`. The ONLY signed-engine function may be modified is `cockpit_s7l` +
`render_cockpit_s7l` (appenditive), plus new module helpers.

## Invariants
49 `$defs`, URI cap, SPEC v0.22, schema hash `7fc38c8c…`, `ros/` untouched, only metric:// (catalog
noun) + additive capacity/forecast_threshold fields, never the wall-clock.