# WORK 1/1 PLAN — engine `_forecast_closure` band_variance source selection

**Task.** Extend `_forecast_closure`'s Sprint-23 band block in `adjudication_engine.py` to read a
recorded, additive `band_variance` source parameter on the `metric://` object and select the band's
sigma from it, still recorded-data only. This is the ONLY engine-file change for Sprint 24.

**Inputs to the band block (already available):**
- `fc = forecast_metric(...)` -> `recorded_variance` (last point's variance) + `points` list.
- `worst`, `thr`, `direction` computed earlier in `_forecast_closure`.
- `fap_metric` = the recorded `metric://` object -> carries the additive `band_variance` field.

**Design of the patch (additive):**
1. Determine the source choice:
   - `bv = fap_metric.get("band_variance")` -> normalized `str(...).strip().lower()`.
   - None / "" / "last" / unknown -> `source = "last-point"`, sigma from `rv` (the last point),
     EXACTLY Sprint 23.
   - "all" or "minmax" -> `source = bv`, sigma = `max(|variance|)` over the recorded `points`
     (only recorded point values), via the same `_num` numeric coercion so a non-numeric point
     variance is skipped.
2. `sigma = round(abs(selected_variance), 4)`; `low = worst - sigma`; `high = worst + sigma`
   (round 4); `crosses` worst-side in the direction — UNCHANGED semantics.
3. `band = {worst, sigma, low, high, crosses}` — and ADD `source` to the band dict ONLY when the
   source is a whole-series choice ("all"/"minmax"), so the default (no `band_variance` recorded)
   band stays byte-identical (no `source` key -> Sprint-23 bytes preserved).
4. The band, recorded_variance, expected_last, and (when whole-series) `source` ride on the closure,
   `q8["forecast"]`, and `do_nothing` when a band exists (unchanged gating).
5. When a whole-series source is active, the do-nothing summary + Q3 attention `why` band phrase
   gains an honest source marker (e.g. "σ recorded whole-series max") so the recorded data origin is
   named — additive, old phrase stays a strict prefix.

**Frozen / untouched:** `reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`, `rank`,
`machine_eligible_best`, `render_tradeoff`, `cockpit_q7q8`, `cockpit_s7l`, `render_cockpit_s7l`,
`forecast_metric`, `record_metric_series`. `record_metric_series.fields` allows a `band_variance`
field (pass it via `fields=`, lands additive on the metric object; `variance`/`points`/`actual` are
reserved in that function, `band_variance` is not).

**C2 safety:** `band_variance` does not end in a temporal suffix — safe. `source` is a band-internal
key, not an object field — safe.

**Verify after edit:** `python3 -c "import ast;ast.parse(open('adjudication_engine.py').read())"` and
re-run Sprint-23 `run_forecast_variance_demo.py` (must stay ALL PASS — default byte-identity).