# SPRINT 25 / WORK 1 — PLAN: engine extensions
Extend ONLY `instances/contested_reality/adjudication_engine.py`:
- `_forecast_closure`: inside the existing `if src_variance is not None:` band block, build
  `band_periods` (per-period low/high from sigma on every projected value) + `band_horizon`
  (record-wide min-low/max-high). Ride them on `res` + `res["forecast"]` + `do_nothing` ONLY under
  the existing `if band is not None:` block. Append an additive horizon phrase to the do-nothing
  summary (old string strict prefix).
- `cockpit_s7l`: in the Q9 block, when a band exists AND threshold is numeric, add
  `q9["band_capacity_attention"] = {flag, why, low, high, crosses}` derived only from the horizon
  range + threshold (+ optional recorded-capacity reference string, never invented).

Exit: no new noun; frozen functions untouched; no-variance/no-data orgs byte-identical.