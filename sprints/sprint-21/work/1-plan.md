# Sprint 21 — work/1-plan: forecast → attention → expected-impact closure

Before building, lock the design decisions (state plainly, deterministic, data-only, additive).

## The engine closure (additive, in `adjudication_engine.py` only)
1. Add a small module-level numeric-coerce helper `_num(x)` (used for the recorded threshold).
2. In `cockpit_s7l`, after `_recorded_metric_with_series(sub)` gives a series:
   - compute `fc = forecast_metric(cfg, sub, series_uri, horizon=3)` (already done for Q6, reuse + store);
   - resolve the **recorded threshold**: `metric_obj.get("forecast_threshold")` if numeric, else
     `metric_obj.get("target")` if numeric, else `fc["last_actual"]`; record the source key
     (`forecast_threshold` / `target` / `last-actual`).
   - **crossing** = `min(p["projected"] for p in fc["projections"]) < threshold`.
3. `.q3`: when a recorded series exists AND crossing, append a forecast-driven attention item:
   `{"item": <series_uri>, "why": "forecast: projected to fall below <threshold> (<src>) — worst
   <min> at period <H>", "tag": "forecast"}`. (Attention only — never an auto-pick.)
4. `.q8` + trade-off: when a recorded series exists, add additive fields to the `base`-returned
   `q8` dict (NOT rewritten `cockpit_q7q8` — add after delegation): a structured `forecast` block
   (projections, threshold, source, worst, crossing) and a `do_nothing_expected_impact` (baseline,
   priced=True, `on_target` bool, summary string). When NOT crossing → on-target labelled, still priced.
5. `render_cockpit_s7l`: render the new Q3 forecast item (already covered by iterating `prioritized`
   — explicitly include `tag`) + a Q8/trade-off line carrying the projected-cost do-nothing where present.

## Do-nothing pricing rule (deterministic from recorded data only)
- do-nothing baseline = the `unresolved`/`do-nothing` option in `cfg["options"]` (already the baseline).
- expected-impact of doing nothing = the projected trajectory: if crossing, "forecast-driven do-nothing
  cost: <metric> projects to worst <min> (period <H>) below target <threshold> — doing nothing risks
  <gap>"; else "on-target: projection stays at/above <threshold> — no forecast-driven cost". Never the
  wall-clock, never an invented number; a projection, not an outcome.
- Q8 recommendation is UNCHANGED (= `cockpit_q7q8`'s machine-eligible best). The forecast only prices
  attention + do-nothing cost, never overrules the §6 floor.

## Threshold C2-safety
`forecast_threshold` is a valid additive field on the `metric://` object (does not end in a temporal
suffix). Existing metric points keys (`period`/`target`/`expected`/`actual`/`variance`) unchanged.

## Runner (run_forecast_action_demo.py)
Three orgs on fresh Substrates:
- `deli-forecast` (Sprint-20 recorded deteriorating series: pts actuals [0.92,0.90,0.87,0.86] target
  0.95 → projection [0.84,0.82,0.8], crossover) → Q3 forecast item + projected do-nothing cost.
- `deli-forecast-flat` (NEW control): recorded series FLAT/above-target (e.g. actuals [0.96,0.97,0.96,
  0.96] target 0.95 → projection ≈ 0.96 stays at/above) → NO forecast attention, do-nothing priced +
  labelled on-target.
- `deli` (no-data control) → unchanged Q3/Q8/trade-off fallback (byte-identical to Sprint 20).
Asserts (all PASS → exit 0):
  (a) full §7L Q1–Q10 on each org;
  (b) deteriorating org: q3 has a `forecast`-tagged item; q8 has `do_nothing_expected_impact`
      priced with `on_target=False`; projection == hand-computed;
  (c) flat control: q3 has NO `forecast` item; q8 do-nothing priced with `on_target=True`;
  (d) deli: q3 unchanged, q8 unchanged (no forecast fields), fallback identical to Sprint 20;
  (e) determinism: cockpit_s7l + render identical on re-run (all 3 orgs);
  (f) agreement: Q8 `forecast` projections == `forecast_metric` == hand-computed from recorded points;
  (g) no §6 overrule: q8 recommendation == `cockpit_q7q8` recommendation for every org;
  (h) no wall-clock (all from recorded values);
  (i) fixtures emitted for the two recorded orgs + report.