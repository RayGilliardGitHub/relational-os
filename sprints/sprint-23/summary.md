# SPRINT 23 — SUMMARY

**The Q8/trade-off do-nothing expected-impact is now priced as a recorded-variance BAND (worst ± σ),
not a single point — additively, from recorded data only, with Sprint-22 single-point behavior kept
byte-identical by default.**

## What closed
Sprint 22 (recorded `direction` → do-nothing priced for both orientations) disclosed in its findings
("Open issues / next work") the next honest frontier: the do-nothing expected-impact was a **single
point** (the worst projected value vs the recorded threshold), IGNORING the RECORDED variance the
engine already computes and renders on Q6. Sprint 23 makes the recorded variance a recorded, additive
input to the do-nothing pricing: when the recorded `metric://` series' last point carries a numeric
`variance`, the closure reports a projected **band** and the Q3 attention / do-nothing summary say the
range — plainly — when the band (not just the point) crosses the threshold.

## What was built (additive, real output)
- **`adjudication_engine._forecast_closure` extended (ONLY engine file touched).** After the Sprint-22
  worst/crossing/direction logic, when `_num(fc["recorded_variance"])` (the LAST recorded point's
  `variance`) is numeric:
  - `sigma = abs(recorded_variance)` (magnitude); `low = worst − sigma`, `high = worst + sigma`
    (exact recorded-data arithmetic, round 4);
  - `crosses` = whether the WORST side crosses the threshold in the metric's direction
    (higher-is-better: `low < threshold`; lower-is-better: `high > threshold`);
  - ADDITIVE keys `band` + `recorded_variance`/`variance` + `expected_last` (the recorded expected last
    value as the anchor) ride on the closure, `q8["forecast"]`, and `do_nothing_expected_impact`;
  - the do-nothing **summary** + Q3 attention **`why`** append an additive phrase naming the band
    (old string stays a strict prefix).
  - When the last point has NO numeric `variance` (or no series): **no** new keys, **no** phrase —
    byte-identical single-point / no-data fallback.
- **`render_cockpit_s7l`:** the Q8 do-nothing line gains an additive band suffix when `dn["band"]`
  exists (no-band orgs: line unchanged). No other edits; all frozen functions
  (`reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/`rank`/`machine_eligible_best`/
  `render_tradeoff`/`cockpit_q7q8`) untouched; 49 `$defs`, URI cap, SPEC v0.22, `ros/` + sector
  instances untouched; template hash `7fc38c8c…` unchanged.
- **`run_forecast_variance_demo.py` (new, exit 0 = ALL PASS)** drives ≥4 orgs on fresh Substrates:
  variance-carriers `deli-forecast` (higher-is-better, band 0.71…0.89 σ0.09, crosses True) and
  `deli-cost` (lower-is-better, band 16.0…32.0 σ8 — high 32.0 above ceiling 16 → a **worse** do-nothing
  than the single point 24.0), a **variance-less control** `deli-flat2` (recorded series, NO variance —
  **exactly** the Sprint-22 single-point output, no additive keys), and the no-data `deli` (unchanged).
  Asserts: full §7L Q1–Q10; band derived ONLY from recorded values; summary surfaces the variance with
  SUPERSET byte-identity (Sprint-22 fields compared with additive keys ignored); control exactly
  single-point; determinism; agreement with `forecast_metric` (incl. its `recorded_variance`); no §6
  overrule (Q8 recommendation unchanged); no wall-clock / no invented variance. Emits fixtures +
  `artifacts/adjudication/reports/cockpit-forecast-variance.md`.
- **`run_forecast_direction_demo.py` (Sprint 22) updated additively** — the only runner with strict
  `==` on the summary/`why` strings; now asserts superset byte-identity (`startswith` of the Sprint-22
  strings + the added band fields). Sprint-21/20 runners unchanged and green.

## §16 verdict
The do-nothing expected-impact now prices the **recorded spread as data WHERE it exists**: worst (per
the recorded `direction`) bounded by the recorded last `variance` (magnitude σ) → `low … high`, the
recorded `expected` last value surfaced as the anchor, and whether the band's worst side crosses the
recorded threshold made explicit on Q3 + the do-nothing summary. Deterministic and data-only (worst +
recorded variance + threshold are the only inputs to low/high/crosses; never the wall-clock, never an
invented variance). **Still not derivable:** a series that does not record a variance cannot be made to
produce a band (correct — the engine reports the recorded reality). This is a **recorded-data spread,
NOT a probability/confidence interval**; a stochastic/adaptive forecast stays out of scope of the
honest deterministic ~$0 stance. The Q8 recommendation is unchanged — the band prices attention and
do-nothing, it never overrules the §6-floor-gated machine-eligible best. The no-variance + no-data
behaviors are byte-identical to Sprint 22.

## Verification (real output, all exit 0)
- New: `run_forecast_variance_demo.py` → **ALL PASS** (27 assertions).
- Sprint 22/21/20: `run_forecast_direction_demo.py` (additive-aware) + `run_forecast_action_demo.py` +
  `run_forecast_capacity_demo.py` → ALL PASS.
- 12 curated C-R demos (adjudication_engine, cockpit_q7q8, cockpit_s7l, dispute, tradeoff,
  reconcile_learning, interest_conflict, full_dispute, rule_authoring, rule_comparison, rule_library) →
  ALL PASS.
- Conformances: `conformance_adjudication` (16 labels) + dispute/interest/lifecycle/tradeoff → ALL PASS.
- Sectors: `instances/build_all.py` (12) + `conformance_all.py` → ALL SECTORS PASS.
- S5 reference `run_s5_demo.py` + `run_s5_conformance.py` → ALL PASS; `agent_demo/run_agent_demo.py` →
  ALL PASS.
- New org fixtures (`deli-flat2`, `deli-forecast`, `deli-cost`) pass the Sprint-0 conformance
  (C1–C5, 26 instances each, 49 `$defs`).
- Template hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` + schema untouched, no new noun.

## Roll-forward
`docs/ENGINE-FORECAST-VARIANCE.md` (new) + additive Sprint-23 notes in
`docs/ENGINE-FORECAST-DIRECTION.md` and `docs/ENGINE-FORECAST-ACTION.md`; `instances/README.md` Sprint-23
entry; `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after Sprint 23"
note. SPEC stayed v0.22 (no normative gap surfaced).