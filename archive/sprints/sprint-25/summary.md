# SPRINT 25 — SUMMARY

**The do-nothing expected-impact now prices the recorded variance across the WHOLE projection
horizon (`band_periods`/`band_horizon`) and feeds §7L Q9 as a capacity-attention flag
(`band_capacity_attention`) — additively, recorded-data only, with the Sprint-23/24 single-point/single-
worst-band behavior kept byte-identical.**

## What closed
Sprint 24 (recorded whole-series `band_variance` source -> single-worst-point do-nothing BAND)
disclosed in its own findings the next honest frontier: **the band was still computed around the SINGLE
worst projected point** — it did not carry the recorded band across ALL projection periods (the whole
horizon's worst-case spread) and did not feed §7L Q9 capacity attention. Sprint 25 closes that bounded
slice additively.

## What was built (additive, real output)
- **`adjudication_engine._forecast_closure` extended (ONLY engine file touched).** When a band exists
  (recorded variance + a recorded `band_variance` source) the closure, `q8["forecast"]`, and
  `do_nothing_expected_impact` each additionally carry:
  - **`band_periods`** = `[{period, low, high}]` for EVERY projection period, `low = projected − sigma`,
    `high = projected + sigma` (the SAME recorded sigma applied per period; exact arithmetic, 4dp);
  - **`band_horizon`** = `{low: min(period lows), high: max(period highs)}` — the record-wide
    whole-horizon worst case.
  - The do-nothing **summary** appends an additive phrase naming the record-wide range (e.g. `—
    horizon-wide recorded band 0.71…0.93 across 3 projection periods (band_periods/band_horizon, same
    recorded σ)`), appended AFTER the Sprint-23/24 single-worst phrase so the old string stays a
    **strict prefix**. The single-worst `band` field is UNCHANGED.
- **`adjudication_engine.cockpit_s7l` extended (Q9 block).** When a band exists AND the recorded
  threshold is numeric, `q9` gains an additive **`band_capacity_attention`** =
  `{flag, why, low, high, crosses}` — a data-only flag of whether the record-wide horizon range signals
  the recorded threshold (higher-is-better: `low < threshold`; lower-is-better: `high > threshold`).
  `why` references any RECORDED capacity (value/unit/load) WITHOUT inventing or mutating a number; if
  none is recorded the flag is still derivable from the band + threshold alone. A no-band / no-variance
  / no-data org carries NO `band_capacity_attention` key (byte-identical).
- **All frozen functions untouched** (`reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`,
  `_aggregate`, `rank`, `machine_eligible_best`, `render_tradeoff`, `cockpit_q7q8`, `render_cockpit_s7l`,
  `forecast_metric`, `record_metric_series`, `record_capacity`); 49 `$defs`, URI cap, SPEC v0.22,
  `ros/` + schema + sector instances untouched; schema hash `7fc38c8c…`.
- **`run_forecast_horizon_demo.py` (new, exit 0 = ALL PASS)** drives ≥5 orgs on fresh Substrates:
  - `deli-forecast` (higher-is-better deteriorating, recorded variances, NO `band_variance`) — the
    Sprint-23/24 last-point band (0.71…0.89 σ0.09) kept **BYTE-IDENTICAL** (verified against
    `run_forecast_variance_demo.py`'s `FC_BAND`), now ALSO carrying additive band_periods + band_horizon
    0.71…0.93 (high widens past the single-worst 0.89) + band_capacity_attention; summary keeps the
    Sprint-23/24 string as a strict prefix.
  - **`deli-varmax`** (whole-series `band_variance:"all"`, σ0.18) — carries band_periods 0.66…1.02 /
    0.64…1.0 / 0.62…0.98 and band_horizon **0.62…1.02**: horizon-wide high **1.02 > single-worst high
    0.98** (WIDENS because period 1's projected 0.84 + σ0.18 = 1.02 sits ABOVE the worst point's own +σ
    band) — the recorded whole-horizon worst case as data.
  - **`deli-varmax-cap`** (same whole-series band + a RECORDED capacity 500.0 resolutions/day, load
    0.72) — the Q9 band_capacity_attention `why` **references the recorded capacity** while the capacity
    object stays intact (never invented/mutated).
  - `deli-flat2` (recorded series, NO variance — no-band control) — **NO** band_periods / band_horizon
    / band_capacity_attention; do-nothing summary byte-identical single-point.
  - `deli` (no-data) — unchanged; no new keys.
  Asserts: full §7L Q1–Q10; `band_periods` = per-period projected ± recorded sigma EXACT arithmetic;
  `band_horizon.low/high` = min/max over those periods (recorded-data only); sigma is STILL exactly a
  recorded point |variance| magnitude (a pure function of the `points` list + the recorded source,
  never invented); default orgs byte-identical superset (only the additive keys); determinism; no §6
  overrule (Q8 recommendation unchanged); no wall-clock. Emits fixtures +
  `artifacts/adjudication/reports/cockpit-forecast-horizon.md`. New org fixtures pass the Sprint-0
  C1–C5 conformance (26 instances each, 49 `$defs`).

## §16 verdict
**The do-nothing price + Q9 capacity-attention now carry the recorded WHOLE-HORIZON worst case AS DATA
where it exists.** The same recorded sigma (one recorded point |variance| magnitude, per the recorded
`band_variance` source) is applied to every projection period -> `band_periods` (per-period low/high) +
`band_horizon` (record-wide min-low/max-high). `band_horizon` can WIDEN beyond the single-worst point's
band when an earlier period at +σ exceeds the worst point's own band — but that is a pure per-period
application of the SAME recorded sigma over recorded projections, NOT a new model, NOT a wider invented
sigma, NOT a confidence interval. Q9's `band_capacity_attention` flag derives data-only from the horizon
range vs the recorded threshold and references any RECORDED capacity without inventing one. The default
(no `band_variance`) is byte-identical to Sprint 23/24 (single-worst `band` field untouched), and a
no-variance series / no-data org carries none of the new keys (byte-identical single-point / unchanged
fallback). The Q8 recommendation is UNCHANGED (the band prices attention + do-nothing; it never overrules
the §6-floor-gated machine-eligible best). **Still not derivable:** an org without recorded point
variances cannot be priced as a band (correct); a capacity-attention NUMBER is never fabricated (the
engine only flags/reasons); and this remains a recorded-spread range, NOT a probabilistic confidence
interval (a stochastic/adaptive forecast stays out of the deterministic ~$0 stance).

## Verification (real output, all exit 0)
- New: `run_forecast_horizon_demo.py` -> **ALL PASS**.
- Full non-regression: `run_forecast_variance_all_demo.py` + `run_forecast_variance_demo.py` +
  `run_forecast_direction_demo.py` + `run_forecast_action_demo.py` + `run_forecast_capacity_demo.py` +
  `run_cockpit_s7l_demo.py` + the 12 curated C-R demos -> ALL PASS.
- Conformances: `conformance_adjudication` (16 labels) + dispute/interest/lifecycle/tradeoff -> ALL PASS;
  the new `deli-varmax-cap` fixtures pass the Sprint-0 C1–C5.
- Sectors: `instances/build_all.py` (12) + `conformance_all.py` -> ALL SECTORS PASS.
- S5 reference `run_s5_demo.py` + `run_s5_conformance.py` -> ALL PASS; `agent_demo/run_agent_demo.py` -> ALL PASS.
- Schema hash `7fc38c8c…` unchanged, 49 `$defs`, SPEC v0.22, `ros/` + schema untouched, no new noun.

## Roll-forward
Additive Sprint-25 addendum (§8) in `docs/ENGINE-FORECAST-VARIANCE.md` + a Sprint-25 §9 note in
`docs/ENGINE-FORECAST-CAPACITY.md`; `instances/README.md` Sprint-25 entry;
`/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after Sprint 25" note.
SPEC stayed v0.22 (no normative gap surfaced).