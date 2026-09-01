# work/1-band-engine-extend.md — extend `_forecast_closure` + `render_cockpit_s7l` (additive)

## What changes in `adjudication_engine.py`
- `_forecast_closure`: after `worst`/`crossing`, compute the recorded-variance band ONLY when the last
  recorded point carries a numeric `variance` (`_num(fc["recorded_variance"])` is not None):
  `sigma = abs(rv)` (magnitude), `low = round(worst - sigma, 4)`, `high = round(worst + sigma, 4)`,
  `crosses` = worst-side crossing in the metric's direction (
  higher-is-better: `low < threshold`; lower-is-better: `high > threshold`).
  - When a band exists: add ADDITIVE keys `recorded_variance`+`band`+`expected_last` on the closure and
    `q8["forecast"]`, and `variance`+`band`+`expected_last` on `do_nothing_expected_impact`; APPEND a
    band phrase to the do-nothing `summary` (old string stays a strict prefix) and to the Q3 attention
    `why` (attention item only exists when crossing).
  - When NO band (no variance on last point / non-numeric): NO new keys, NO phrase — byte-identical.
- `render_cockpit_s7l`: the Q8 do-nothing line gains an additive ` | recorded band low…high (± σ s,
  crosses=…)` suffix only when `dn["band"]` exists (no-band orgs: line unchanged).

## Frozen / untouched
`reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`, `rank`, `machine_eligible_best`,
`render_tradeoff`, `cockpit_q7q8`, `forecast_metric`, `record_metric_series`, `record_capacity`.
Spec/schema/ros/instances untouched.

## Verification
After patch: re-run Sprint-22/21/20 runners + spot-check a variance org and a no-data org manually.