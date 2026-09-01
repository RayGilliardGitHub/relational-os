# SPRINT 24 — SUMMARY

**The do-nothing band's variance SOURCE is now a recorded, additive `band_variance` parameter on the
`metric://` object — the band can price the recorded whole-series worst-case spread where the org
records it, while the Sprint-23 last-point default stays byte-identical.**

## What closed
Sprint 23 (recorded last-point variance -> do-nothing projected BAND) disclosed in its own findings
("Open issues / next work") the next honest frontier: **the band used only the LAST recorded point's
`variance`**, so a series whose RECORDED `variance` changed across its points (widened or narrowed
spread) was collapsed to the final variance in the band. Sprint 24 closes that bounded slice by making
the band's variance source a **recorded, additive `band_variance` parameter**: absent / `"last"` /
unknown -> the last recorded point's variance (Sprint-23 default, **byte-identical**); `"all"` /
`"minmax"` -> the recorded **whole-series** choice (`max(|variance|)` over the recorded points). An
org whose measured spread WIDENED over time can price a do-nothing band from the recorded worst-case
spread, and one that CONVERGED can tighten it — still recorded-data only (every possible sigma is a
recorded point variance magnitude, never invented, never the wall-clock).

## What was built (additive, real output)
- **`adjudication_engine._forecast_closure` extended (ONLY engine file touched).** The Sprint-23 band
  block now reads a recorded `band_variance` field on the metric object and selects the band's sigma:
  - absent / `"last"` / unknown -> `source = "last-point"`, sigma from the last recorded point's
    `variance` — EXACTLY Sprint 23, **byte-identical**.
  - `"all"` / `"minmax"` -> `source = bv`, sigma = `max(|variance|)` over the recorded `points` (only
    recorded point values, via the same `_num` numeric coercion).
  - `band = {worst, sigma, low, high, crosses}` carries `source: "all"`/`"minmax"` ONLY when a
    whole-series choice is active; the default orgs' band has NO `source` (bytes preserved).
  - When whole-series is active, the closure, `q8["forecast"]`, and `do_nothing_expected_impact` each
    gain an additive `band_variance` key, and the do-nothing summary + Q3 attention `why` append an
    honest phrase naming the source (`— band σ from the recorded whole-series max |variance|
    (band_variance all)`).
  - `render_cockpit_s7l` unchanged (already renders the band generically). All frozen functions
    (`reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/`rank`/`machine_eligible_best`/
    `render_tradeoff`/`cockpit_q7q8`/`cockpit_s7l`/`forecast_metric`/`record_metric_series`) untouched;
    49 `$defs`, URI cap, SPEC v0.22, `ros/` + sector instances untouched; schema hash `7fc38c8c…`.
- **`run_forecast_variance_all_demo.py` (new, exit 0 = ALL PASS, 56 assertions)** drives ≥4 orgs on
  fresh Substrates:
  - `deli-forecast` (higher-is-better deteriorating, recorded variances, NO `band_variance`) — asserted
    **byte-identical to Sprint 23** (band 0.71…0.89 σ0.09, NO `source` key; the summary/attention fields
    compared against `run_forecast_variance_demo.py`'s constants with the additive `source` ignored).
  - **`deli-varmax`** (NEW: records `band_variance:"all"`, last |variance| 0.03 SMALL but an EARLIER
    recorded |variance| 0.18 LARGER) — sigma = recorded max |variance| 0.18, band **0.62…0.98 WIDENS**
    vs the Sprint-23 last-point 0.77…0.83; `source:"all"`, `band_variance` rides closure/q8/do_nothing,
    summary + attention-why name it.
  - `deli-cost` (lower-is-better rising, recorded variances, NO `band_variance`) — asserted
    **byte-identical to Sprint 23** (band 16.0…32.0 σ8, NO `source`).
  - `deli` (no-data) — unchanged Q3/Q8/trade-off fallback.
  Asserts: full §7L Q1–Q10 on each; sigma is EXACTLY a recorded point |variance| magnitude (a pure
  function of the `points` list, never invented); default orgs superset byte-identical (only the
  additive `source` on the whole-series band); whole-series sigma == recorded max |variance| and
  low/high/crosses exact recorded-data arithmetic; determinism; agreement with `forecast_metric` (its
  `recorded_variance` == last point) + hand-computed whole-series max; no §6 overrule (Q8
  recommendation unchanged); no wall-clock. Emits fixtures +
  `artifacts/adjudication/reports/cockpit-forecast-variance-all.md`.

## §16 verdict
**The do-nothing band now prices the recorded WORST-CASE whole-series spread AS DATA where the org
records it.** An org that records a realized-vs-expected `metric://` series whose points carry numeric
`variance` values AND records `band_variance:"all"` (or `"minmax"`) gets the Q8/trade-off do-nothing
band priced from the largest recorded |variance| across the recorded points (worst per the recorded
`direction` ± sigma -> low…high), with the recorded source named additively and the recorded
`expected` last value as the anchor. It is deterministic and data-only: the source, every candidate
sigma, and low/high/crosses derive exclusively from recorded point values + the recorded
`band_variance` choice — never the wall-clock, never an invented/interpolated number. The default (no
`band_variance` recorded) is **byte-identical to Sprint 23**, and a no-variance series / no-data org
keeps the single-point / fallback unchanged. The Q8 recommendation is UNCHANGED (the band prices
attention + do-nothing, it never overrules the §6-floor-gated machine-eligible best). **Still not
derivable:** an org that records no point variances cannot be priced as a band (correct); an org that
records `band_variance` but no per-point variances falls back to the last point (still a recorded
value); and this is a recorded-spread range, NOT a probabilistic confidence interval (a
stochastic/adaptive forecast stays out of the deterministic ~$0 stance).

## Verification (real output, all exit 0)
- New: `run_forecast_variance_all_demo.py` -> **ALL PASS (56 assertions)**.
- Sprint 23/22/21/20 runners: `run_forecast_variance_demo.py` + `run_forecast_direction_demo.py` +
  `run_forecast_action_demo.py` + `run_forecast_capacity_demo.py` + `run_cockpit_s7l_demo.py` -> ALL PASS.
- 16 C-R demos (adjudication_engine, cockpit_q7q8, cockpit_s7l, dispute, tradeoff, reconcile_learning,
  interest_conflict, full_dispute, rule_authoring, rule_comparison, rule_library, + the 5 forecast
  runners) -> ALL PASS.
- Conformances: `conformance_adjudication` (16 labels) + dispute/interest/lifecycle/tradeoff -> ALL PASS.
- Sectors: `instances/build_all.py` (12) + `conformance_all.py` -> ALL SECTORS PASS.
- S5 reference `run_s5_demo.py` + `run_s5_conformance.py` -> ALL PASS; `agent_demo/run_agent_demo.py` -> ALL PASS.
- New org fixture `deli-varmax` passes the Sprint-0 C1–C5 conformance (26 instances, 49 `$defs`).
- Schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` + schema untouched, no new noun.

## Roll-forward
Additive Sprint-24 addendum (§7) in `docs/ENGINE-FORECAST-VARIANCE.md` + additive notes in
`docs/ENGINE-FORECAST-DIRECTION.md`; `instances/README.md` Sprint-24 entry;
`/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after Sprint 24" note.
SPEC stayed v0.22 (no normative gap surfaced).