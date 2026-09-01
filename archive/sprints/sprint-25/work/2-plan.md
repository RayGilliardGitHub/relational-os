# SPRINT 25 / WORK 2 — PLAN: runner
New `instances/contested_reality/run_forecast_horizon_demo.py`, exit 0 = ALL PASS, drives ≥5 fresh
orgs (≥4 required):
- `deli-forecast` (Sprint-23/24 default last-point band) — byte-identical superset, NOW also carries
  additive `band_periods`/`band_horizon` (+ `band_capacity_attention` on q9).
- `deli-varmax` (whole-series `band_variance:"all"`, band 0.62…0.98) — also carries band_periods/
  band_horizon with horizon-wide high 1.02 > single-worst high 0.98 (widening because an EARLIER
  period sits higher).
- `deli-varmax-cap` (same whole-series band + a RECORDED capacity) — proves `why` references the
  recorded capacity without inventing it.
- `deli-flat2` (recorded series, NO variance — no-band control) — NO new keys, byte-identical
  single-point output.
- `deli` (no-data) — unchanged; no band_capacity_attention, no band_periods, no band_horizon.
Asserts: full Q1–Q10; band_periods = per-period projected ± sigma EXACT arithmetic; band_horizon =
min/max over those periods (recorded-data only); sigma is still exactly a recorded point |variance|
magnitude; default orgs byte-identical to Sprint 23/24 except the additive keys; determinism; no §6
overrule (Q8 rec unchanged); no wall-clock. Emits fixtures + report.

Exit criteria: real output, RESULT ALL PASS, exit 0.