# ENGINE-FORECAST-VARIANCE — recorded-variance projected band for the do-nothing expected-impact (Sprint 23, + Sprint 24 whole-series source)

**Scope.** Sprint 22 made the crossing **direction** a recorded parameter so the Q8/trade-off
do-nothing expected-impact is priced for BOTH orientations (rate/quality falling below target;
cost/latency/defect/risk rising above ceiling) — but its own finding (`sprint-22/notes/findings.md`,
"Open issues / next work") disclosed the next honest frontier: **the do-nothing expected-impact was
priced as a SINGLE POINT gap** (the worst projected value vs the recorded threshold), IGNORING the
**RECORDED variance** the engine already computes and renders on Q6. **Sprint 23 closes that bounded
slice** additively: when the recorded `metric://` series' last point carries a numeric `variance`, the
Q8/trade-off do-nothing expected-impact is priced as a projected **BAND** (worst ± the recorded
variance as a magnitude) — `low … high` — surfaced on the closure, `q8["forecast"]`,
`do_nothing_expected_impact`, and the do-nothing summary + Q3 attention `why`. A series with **no**
recorded variance, or a no-data org, keeps the Sprint-22 output **byte-identical**.

This document states the band rule (which recorded variance is used, how `low`/`high` are derived,
when `crosses` flips), the honest no-data AND no-variance fallback, how it is generic + additive,
how it is **not** a probability/confidence claim, and the §16 verdict.

---

## 1. The band rule (which recorded variance, and how the band is derived)

From the Sprint-22 `_forecast_closure` the engine already computes `worst` (per the recorded
`direction`) and resolves the recorded `threshold` + `crossing`; `forecast_metric` already returns the
last recorded point's `variance` as `recorded_variance`. Sprint 23 adds, **only when that recorded
variance is a numeric value**:

- **`recorded_variance`** = `forecast_metric.recorded_variance` = `_num(last recorded point's
  `variance`)`. It is the **last recorded point's** variance (a recorded historical spread), never an
  invented/averaged variance over the whole series.
- **`sigma`** = the same recorded variance taken as a **magnitude** (`abs(recorded_variance)`).
- **`low`** = `worst − sigma`, **`high`** = `worst + sigma` (exact recorded-data arithmetic, rounded to
  4dp, deterministic — the projection's worst point bounded by the recorded spread).
- **`crosses`** — whether the **WORST side** of the band crosses the threshold in the metric's
  direction:
  - higher-is-better (rate/quality): `low < threshold` — the band's low (worst) end is below the target;
  - lower-is-better (cost/latency/defect/risk): `high > threshold` — the band's high (worst) end is
    above the ceiling.

The recorded `expected` last value is surfaced as the **anchor** (`expected_last`). When the band
exists, the Q8/trade-off do-nothing **summary** and the Q3 attention **`why`** append an **additive
phrase** naming the band (e.g. `recorded band 0.71…0.89 (± σ 0.09); worst side 0.71 below target
0.95 — the whole recorded spread is priced as bad`), so the expected-impact is reported as a range,
not a single point. Every pre-existing Sprint-22 single-point field/string stays byte-identical (the
band phrase is appended; `worst`/`gap`/`threshold`/`crossing`/`on_target`/the single-point summary
portion are unchanged).

## 2. What it is NOT

- **Not a probability / confidence interval:** the variance is a **recorded historical spread**, used
  to bound the deterministic last-actual + mean-delta projection — it is not a model's confidence
  interval, not a standard deviation of a stochastic forecast, and carries no probability claim.
- **Not an invented variance:** only a **recorded** point variance is used. A series whose last point
  has no numeric `variance` keeps the single-point output.
- **Not a fuller forecast model:** the projection is still the deterministic Sprint-20/21/22
  last-actual + mean-delta. The band only surfaces the recorded spread around the deterministic worst.
- **Not a schema/service/trust change:** no new noun, 49 `$defs`, SPEC v0.22, `ros/` + sector
  instances untouched; `reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/`rank`/
  `machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8` frozen.

## 3. Which recorded variance, and the honest no-variance + no-data fallback

- **No recorded series** (`_recorded_metric_with_series` finds none): `available: False`, Q6 cannot
  forecast, no attention item, no do-nothing band — **byte-identical to Sprint 20–22**.
- **Recorded series, last point has NO `variance` (or a non-numeric one):** `recorded_variance` is
  `None`, the band is **absent**, and the closure / `q8["forecast"]` / `do_nothing_expected_impact`
  carry **no** new keys and the summary is **unchanged** — **exactly the Sprint-22 single-point
  output**.
- **Recorded series, last point HAS a numeric `variance`:** the band is present and the closure, the
  q8 `forecast` block, and the do-nothing block each gain additive `band` (+ `recorded_variance`/
  `variance` + `expected_last`), and the summary/attention-why append the band phrase. Everything
  pre-existing is preserved (superset, additive).

## 4. How it is generic + additive

One identical engine path — an org that records a realized-vs-expected `metric://` series whose last
point records a `variance` gets the band priced; an org that does not keeps the exact prior output.
The `band`/`variance`/`expected_last` are **additive keys** on the closure / `q8["forecast"]` /
`do_nothing_expected_impact`; the recorded `variance` is a per-point additive key on the `metric://`
series (already a data field, no schema edit). No new URI noun, 49 `$defs`, SPEC v0.22, `ros/` +
sector instances untouched (only `adjudication_engine.py`'s `_forecast_closure` + `render_cockpit_s7l`
extended additively; all frozen functions untouched). The C2 RFC3339 temporal probe is unharmed: the
additive keys carry no `at|time|deadline|expires|expiry|effective|due|since` suffix.

## 5. The ≥4-org proof (`run_forecast_variance_demo.py`, exit 0 = ALL PASS)

| org | direction | series | band | do-nothing |
|---|---|---|---|---|
| `deli-forecast` | higher-is-better (default) | **deteriorating**, variances `-0.03/…/-0.09` | `0.71…0.89` σ0.09, crosses **True** | priced bad; **superset** of Sprint-22 (single-point fields identical, band added) |
| `deli-flat2` | higher-is-better (default) | recorded, **NO `variance` on any point** | **absent** | **exactly** Sprint-22 single-point (no additive keys, summary byte-identical) |
| `deli-cost` | lower-is-better (explicit) | **rising**, variances `2/4/6/8` | `16.0…32.0` σ8, crosses **True** | high 32.0 above ceiling 16 → prices a **worse** do-nothing than the single point 24.0 |
| `deli` | — | **no recorded series** | absent | unchanged fallback (no forecast/do-nothing) |

Asserted: full §7L Q1–Q10 on each; band derived only from recorded values (worst + recorded variance +
threshold; `low`/`high` exact arithmetic); on the variance orgs the summary surfaces the recorded
variance while every pre-existing single-point field/branch stays byte-identical (Sprint-22 fields
compared with the additive keys ignored) and the Q3 attention `why` names the band; the variance-less
control is EXACTLY the single-point output; determinism on re-run; agreement of the Q3/Q8 projection
with `forecast_metric` (incl. its `recorded_variance`); no §6 overrule (Q8 recommendation unchanged);
no wall-clock / no invented variance. Emits fixtures + `artifacts/adjudication/reports/`
`cockpit-forecast-variance.md`; the new orgs' fixtures pass the Sprint-0 conformance (C1–C5, 49 `$defs`).

## 6. Honest §16 verdict — does the do-nothing expected-impact now price the recorded spread as data where it exists?

**Yes, as data, where the data exists.** For any org that records a realized-vs-expected `metric://`
series whose last point records a numeric `variance`, the Q8/trade-off do-nothing expected-impact is
now priced as a **projected band** (worst ± the recorded variance as a magnitude) — `low … high`, the
recorded `expected` last value surfaced as the anchor, and whether the worst side of the band crosses
the recorded threshold made explicit on the Q3 attention `why` and the do-nothing summary. It is
deterministic and data-only: worst, the recorded variance, and the threshold are the only inputs to
`low`/`high`/`crosses`; never the wall-clock, never an invented variance. **What is still not
derivable:** a series that does **not** record a variance cannot be made to produce a band — the
engine reports the recorded reality and does not manufacture a spread (correct behavior); and this is
**not** a probabilistic confidence interval — a stochastic/adaptive forecast, or a variance derived
from anything beyond a recorded point, remains out of scope of the honest, deterministic, ~$0 stance.
The Q8 recommendation is unchanged: the band prices attention and the do-nothing baseline; it never
overrules the §6-floor-gated machine-eligible best.

*(Evidence: all assertions are real exit-0 output from `run_forecast_variance_demo.py` (ALL PASS), the
Sprint-22 `run_forecast_direction_demo.py` (additive-aware, ALL PASS), the Sprint-21/20 runners, and
the Sprint-0 conformance over the new orgs' fixtures; SPEC v0.22, 49 `$defs`, `ros/` + schema
untouched, no new noun.)*

---

## 7. SPRINT 24 ADDENDUM — the recorded whole-series band-variance SOURCE

**Residual seam closed.** Sprint 23's own finding disclosed that the band used **only the LAST recorded
point's `variance`** — a series whose RECORDED `variance` changed across its points (widened or
narrowed spread) was collapsed to the final variance in the band, ignoring the recorded whole-series
spread. Sprint 24 closes that bounded slice by making the band's variance source a **recorded, additive
`band_variance` parameter on the `metric://` object**:

- **absent / `"last"` / unknown** → `source = "last-point"` (Sprint-23 default). `sigma = abs(last
  recorded point's `variance`)`. **BYTE-IDENTICAL to Sprint 23** — the default orgs' band carries **no
  `source` key** (so their bytes are unchanged).
- **`"all"`** → the recorded **whole-series** choice: `sigma = max(|variance|)` across the recorded
  points (the largest recorded magnitude). The band dict gains `source: "all"`.
- **`"minmax"`** → a defined recorded whole-series rule; implemented here as the recorded min–max
  spread, taken as **the max |variance| magnitude** across the recorded points (still a recorded point
  magnitude — see §7.2). `source: "minmax"`.

When a whole-series choice is active, the closure, `q8["forecast"]`, and `do_nothing_expected_impact`
each also gain an additive `band_variance` key (= the recorded source string), and the do-nothing
summary + Q3 attention `why` append an honest phrase naming that source (e.g. `— band σ from the
recorded whole-series max |variance| (band_variance all)`), so the recorded origin is explicit.

### 7.1 Which recorded value becomes sigma (per source)
| `band_variance` | sigma (the recorded magnitude used) | source emitted |
|---|---|---|
| *(absent)* / `"last"` | `abs(last recorded point's variance)` | *(none — Sprint-23 byte-identical)* |
| `"all"` / `"minmax"` | `max( abs(recorded point variance) over the recorded points )` | `"all"` / `"minmax"` |

`low = worst − sigma`, `high = worst + sigma`, `crosses` worst-side in the metric's direction — all
unchanged semantics; only the recorded magnitude that produces `sigma` is selected by the source.

### 7.2 What it still is / is NOT
- **What it is:** sigma is always a recorded **point** variance magnitude; `recorded_variance` on the
  closure/`q6` still reports the **last** point's variance (matching `forecast_metric`), while the
  band's `sigma` uses the recorded whole-series max when selected. So an org whose measured spread
  **WIDENED** over time can price a do-nothing band from the recorded **worst-case** spread, and one
  that **converged** can tighten it — still honest: only recorded point values feed it.
- **What it is NOT:** not a probability/confidence interval; not a model-derived or interpolated
  variance; not the wall-clock; never a sigma that is not a recorded point magnitude. `"minmax"`
  selects a recorded magnitude (the max |variance|), it does not compute a new spread between two
  values.
- **Generic + additive:** one engine path; the ONLY engine file touched is `_forecast_closure`;
  no new noun, 49 `$defs`, SPEC v0.22, `ros/` + sector instances untouched. `band_variance` is C2-safe
  (no `at|time|deadline|expires|expiry|effective|due|since` suffix).

### 7.3 The ≥4-org proof (`run_forecast_variance_all_demo.py`, exit 0 = ALL PASS)
`deli-forecast` (deteriorating, recorded variances, **no** `band_variance` → last-point band
byte-identical to Sprint 23, no `source`), **`deli-varmax`** (NEW, records `band_variance:"all"`, last
|variance| 0.03 small but an earlier recorded |variance| 0.18 larger → sigma = recorded max 0.18 →
band **0.62…0.98 WIDENS** vs the last-point 0.77…0.83; `source:"all"`, `band_variance` rides the
closure/q8/do_nothing, summary + attention-why name it), `deli-cost` (lower-is-better rising, recorded
variances, **no** `band_variance` → byte-identical), and the no-data `deli`. Asserts full Q1–Q10;
sigma is a recorded point magnitude; default orgs byte-identical to Sprint 23 (superset, only the
additive `source` on the whole-series band); whole-series sigma == recorded max |variance| and
low/high/crosses exact arithmetic; determinism; agreement with `forecast_metric` (its
`recorded_variance` == last point) + hand-computed whole-series max; no §6 overrule; no wall-clock.
The new `deli-varmax` fixtures pass the Sprint-0 C1–C5 conformance (26 instances, 49 `$defs`).

### 7.4 Honest §16 verdict (Sprint 24)
**Yes — the do-nothing band now prices the recorded WORST-CASE whole-series spread AS DATA where the
org records it.** An org whose recorded spread widened over time can set `band_variance:"all"` and the
Q8/trade-off do-nothing band is priced from the recorded worst-case (largest recorded |variance|)
instead of only the last point, with the recorded source named additively. It is deterministic and
data-only — the source, every candidate sigma, and low/high/crosses derive exclusively from recorded
point values + the recorded `band_variance` choice; never the wall-clock, never an invented or
interpolated number. The **default (no `band_variance` recorded) is byte-identical to Sprint 23**, and
a no-variance series / no-data org keeps the single-point / fallback unchanged. The Q8 recommendation
is UNCHANGED (the band prices attention + do-nothing; it never overrules the §6-floor-gated
machine-eligible best). **What is still not derivable:** an org that records **no** point variances
cannot be priced as a band (correct — the engine reports the recorded reality); an org that records a
`band_variance` but no per-point variances falls back to the last point (still a recorded value); and
this is a recorded-spread range, NOT a probabilistic confidence interval (a stochastic/adaptive
forecast stays out of the deterministic ~$0 stance).

---

## 8. SPRINT 25 ADDENDUM — the horizon-wide band + Q9 capacity-attention

**Residual seam closed.** Sprint 24's own finding disclosed that the projected band was still computed
around the **SINGLE worst projected point** at the do-nothing line — it did not aggregate a band across
ALL projection periods (the whole horizon's worst-case spread) and did not feed §7L Q9 capacity
attention. Sprint 25 closes that bounded slice additively by applying the **SAME recorded sigma to
EVERY projection period** and surfacing the record-wide worst case as data.

### 8.1 The horizon-wide band (in `_forecast_closure`)
When a band exists (recorded variance + a recorded `band_variance` source resolves to a sigma that is
exactly one recorded point |variance| magnitude), the closure, `q8["forecast"]`, and
`do_nothing_expected_impact` each additionally carry:
- **`band_periods`** = `[{period, low, high}]` for EVERY projection period, `low = projected − sigma`,
  `high = projected + sigma` (the same recorded sigma applied per period; exact arithmetic, 4dp).
- **`band_horizon`** = `{low: min(period lows), high: max(period highs)}` — the record-wide
  whole-horizon worst case.

The do-nothing **summary** appends an additive phrase naming the horizon-wide range (e.g. `— horizon-wide
recorded band 0.71…0.93 across 3 projection periods (band_periods/band_horizon, same recorded σ)`),
appended AFTER the Sprint-23/24 single-worst band phrase so the old string stays a strict prefix.
`band_horizon` can **WIDEN beyond the single-worst point's band** when an EARLIER projection period's
value at its own ± sigma exceeds the worst point's high (e.g. a deteriorating rate whose earlier
periods sit higher), yet every bound remains a pure function of the recorded series values + the
recorded sigma + the recorded threshold — a recorded-data spread, NOT a new model and not a wider,
invented sigma.

### 8.2 Q9 capacity-attention (in `cockpit_s7l`)
When a band exists AND the recorded threshold is numeric, `q9` gains an additive
**`band_capacity_attention`** = `{flag, why, low, high, crosses}`. The flag is data-only: whether the
record-wide HORIZON range's worst side signals the recorded threshold (higher-is-better: `low <
threshold`; lower-is-better: `high > threshold`). `why` states that as a plain reason and **references
any RECORDED `capacity`** on the authority object (value/unit/load) WITHOUT inventing or mutating a
capacity number; if none is recorded the flag is still derivable from the band + threshold alone. A
no-band / no-variance / no-data org carries **no** `band_capacity_attention` key (byte-identical).

### 8.3 What it still is / is NOT
- **What it is:** per-period bounds from the same recorded sigma, a record-wide horizon worst case as
  data, and a Q9 capacity-attention FLAG (never a fabricated capacity number).
- **What it is NOT:** not a probability/confidence interval; not a model-derived or interpolated
  sigma; not the wall-clock; not an overrule of the §6 pick or floor-gated recommendation; not a
  change to the no-variance / no-data fallback (still byte-identical single-point / unchanged).
- **Generic + additive:** one engine path; the ONLY engine file touched is
  `adjudication_engine.py` (`_forecast_closure`'s band block + `cockpit_s7l`'s Q9 block); all frozen
  functions untouched; no new noun, 49 `$defs`, SPEC v0.22. New additive keys carry no
  `at|time|deadline|expires|expiry|effective|due|since` suffix (C2-safe).

### 8.4 The ≥4-org proof (`run_forecast_horizon_demo.py`, exit 0 = ALL PASS)
| org | band source | horizon result | Q9 capacity-attention |
|---|---|---|---|
| `deli-forecast` | last-point (Sprint-23 byte-identical) | band_periods ± σ0.09; horizon 0.71…0.93 (high widens past single 0.89) | present, flag True, why data-only |
| `deli-varmax` | whole-series `"all"` (σ0.18) | band_periods 0.66…1.02 / 0.64…1.0 / 0.62…0.98; horizon 0.62…1.02 (**high 1.02 > single-worst 0.98** — earlier period at +σ) | present, flag True, why data-only |
| `deli-varmax-cap` | whole-series `"all"` + RECORDED capacity 500.0 res/day (load 0.72) | same band_periods/horizon | why REFERENCES the recorded capacity; capacity intact (never mutated) |
| `deli-flat2` | NO variance (no-band control) | **NO** band_periods / band_horizon / cap-attention; summary byte-identical single-point | absent |
| `deli` | no data | unchanged fallback, no new keys | absent |

Asserts: full Q1–Q10 on each; `band_periods` = per-period projected ± recorded sigma EXACT;
`band_horizon.low/high` = min/max over those periods (recorded-data only); sigma still exactly a
recorded point |variance| magnitude (never invented); default orgs byte-identical to Sprint 23/24
except the additive `band_periods`/`band_horizon`/`band_capacity_attention` keys; determinism; no §6
overrule (Q8 recommendation unchanged); no wall-clock. Emits fixtures +
`artifacts/adjudication/reports/cockpit-forecast-horizon.md`; new org fixtures pass the Sprint-0
C1–C5 conformance (26 instances, 49 `$defs`).

### 8.5 Honest §16 verdict (Sprint 25)
**Yes — the do-nothing price + Q9 capacity-attention now carry the recorded whole-horizon worst case
AS DATA where it exists.** The same recorded sigma is applied to every projection period
(band_periods) and the record-wide horizon worst case (band_horizon = min low / max high) is surfaced
explicitly on the closure, `q8["forecast"]`, and `do_nothing_expected_impact`; it may WIDEN beyond the
single-worst point's band when an earlier period at +σ exceeds the worst point's high, but that is
still a pure per-period application of the SAME recorded sigma over recorded values — NOT a new model,
NOT a wider invented sigma, NOT a confidence interval. Q9's `band_capacity_attention` flag derives
data-only from the horizon range vs the recorded threshold and references any RECORDED capacity
without inventing a number. The default (no `band_variance`) is byte-identical to Sprint 23/24, and a
no-variance series / no-data org carries none of the new keys (byte-identical single-point / unchanged
fallback). The Q8 recommendation is UNCHANGED (the band prices attention + do-nothing; it never
overrules the §6-floor-gated machine-eligible best). **Still not derivable:** an org without recorded
point variances cannot be priced as a band (correct); a capacity-attention NUMBER is never fabricated
(the engine only flags/reasons); and this remains a recorded-spread range, NOT a probabilistic
confidence interval (a stochastic/adaptive forecast stays out of the deterministic ~$0 stance).