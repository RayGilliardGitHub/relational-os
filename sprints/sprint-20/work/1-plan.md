# work/1-plan.md — Sprint 20, step 1: the engine additions (append-only)

**Precondition (verified).** Baseline green (all curated runners exit 0, 16-label conformance ALL PASS,
schema v0.22/hash `7fc38c8c…`, 49 $defs). deli/cove fixtures captured for the byte-identical diff.

**What I edit.** ONLY `instances/contested_reality/adjudication_engine.py`, by *appending* new functions at
the module bottom; the frozen functions and their bodies are untouched.

## 1. `forecast_metric(cfg, sub, metric_uri, *, horizon=3)` — deterministic projection
- Read `m = sub.graph.get(metric_uri) or {}` and its `points` (a non-empty list of dicts each carrying an
  `actual`, optional `target`/`expected`/`variance`).
- Absent/invalid series → `{"available": False, "forecast": "cannot project — no recorded realized-vs-expected
  series on metric://…", "metric": metric_uri}`.
- Present → `last_actual` (last point `actual`), `mean_delta` (mean of consecutive de-zeros deltas, 0 if <2
  points), `projections = [{"period": f, "projected": round(last_actual + mean_delta*f, 4)} for f in 1..horizon]`,
  `recorded_variance` = the last point's `variance`.
- Return `{available: True, metric, unit, target, last_actual, mean_delta, horizon, projections,
  recorded_variance, note: "deterministic projection from the recorded series only (holds the recorded trend);
  a projection, not an outcome; never the wall-clock."}`.
- No wall-clock; pure function of the recorded points + horizon.

## 2. `_recorded_metric_with_series(sub)` -> `(metric_uri, metric_obj)`
- Scan `_graph_objects(sub)` for the first object whose URI starts `metric://` AND carries a non-empty
  `points`/`series`/`realized_series` list of dicts. Return `(uri, obj)`; else `(None, {})`. Deterministic
  (first in graph order).

## 3. `record_metric_series(sub, label, metric_uri, *, points, fields, signer)` — replayable recorder
- Validate `points` is a non-empty list of dicts each with an `actual` (and the series must be ordered by
  `period`). Build the `metric://` object: `{uri, name, formula, **fields}` (fields carries unit/target/period/
  source/owner etc., the Metric-required `name`/`formula` MUST be present), `actual` = last point `actual`,
  `variance` = last point `variance`, and the additive `points` list.
- Append ONE signed `event://{label}/record-metric-series` STATE_CHANGE with `state_update=[metric_obj]`.
- **No temporal-suffix keys** in the metric or any point (`period/target/expected/actual/variance/name/formula/
  unit/source/owner` are all C2-safe).

## 4. `record_capacity(sub, authority_uri, *, value, unit, signer, load=None)` — replayable recorder
- Merge-NOT-replace: `obj = {**sub.graph.get(authority_uri), "capacity": {"value": value, "unit": unit,
  "load": load, "status": "recorded"}}`. Append ONE signed `event://…/record-capacity` STATE_CHANGE with
  `state_update=[obj]`. Preserves-unknown (the authority's required fields ride along).
- Keys `value/unit/load/status` are C2-safe.

## 5. Extend `cockpit_s7l` Q6 + Q9 (in-place data reads; function body's Q6/Q9 blocks only)
- **Q6**: if `_recorded_metric_with_series(sub)` yields a metric, call `forecast_metric(cfg, sub, uri,
  horizon=3)` and set `q6 = {forecast_available: True, forecast: <projection>, metric, projections,
  recorded_variance, evidence: "deterministic projection from the recorded realized-vs-expected series on the
  org's own graph"} `. Else keep the existing honest fallback exactly (no-data orgs unchanged).
- **Q9**: read `auth_obj = sub.graph.get(cfg["authority"]["dispute"]) or {}`; if it carries `capacity`, add
  `ownership["capacity"] = auth_obj["capacity"]`, `ownership["capacity_recorded"] = True`, and update the
  `capability` text to include the recorded number+unit; else `capacity_recorded = False` (existing fallback).

## 6. Extend `render_cockpit_s7l` Q6 + Q9 lines only
- Q6: when `forecast_available`, render `Q6 … project → period…  (recorded variance …; holding the trend)`;
  else keep the existing "cannot forecast from recorded data" line verbatim.
- Q9: when `capacity_recorded`, append `capacity {value} {unit} (load {load})`; else keep the existing line.

## Verification for this step
- `python3 run_cockpit_s7l_demo.py` still ALL PASS (additive: no-data orgs fall back exactly as before).
- A standalone smoke (in the runner, step 2) proves forecast/capacity read-back + determinism + agreement +
  fixture conformance for `deli-forecast`, and the no-data `deli` fallback.