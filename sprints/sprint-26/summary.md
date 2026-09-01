# SPRINT 26 — SUMMARY

**The §7L Q3 forecast-driven attention now names the recorded horizon-wide band (a shared-constant
suffix, strict-prefix), and Q9 adds a data-only `capacity_planning_attention` REASON derived from a
recorded capacity + recorded load + the horizon band — additively, recorded-data only, byte-identical
for every org that records neither a variance band nor a capacity.**

## What closed
Sprint 25 disclosed in its own findings ("Open issues / next work") the next honest frontier: **the
Q3 forecast-driven attention item's `why` still named only the single worst point + single-worst band
(Sprint-23/24 shape), and the Q9 `band_capacity_attention` was a FLAG that did not drive any recorded
capacity-planning reasoning.** Sprint 26 closes that bounded slice additively.

## What was built (additive, real output)
- **`adjudication_engine._forecast_closure` extended (Q3 attention-why block, the ONLY engine file
  touched).** A module constant **`_HORIZON_BAND_PHRASE`**
  (` — horizon-wide recorded band {lo}…{hi} across {n} projection periods (band_periods/band_horizon,
  same recorded σ)`) is appended to `attention_item["why"]` when a band exists AND the forecast-driven
  attention item was created — AFTER the Sprint-23/24 single-worst band phrase and any Sprint-24
  band_variance source phrase, so the old `why` stays a **strict prefix**. The **do-nothing summary
  reuses the SAME constant**, so Q3/Q6/Q8/do-nothing name the record-wide worst case **verbatim by
  construction**. No-band / no-variance / no-data orgs get NO suffix (unchanged, byte-identical).
- **`adjudication_engine.cockpit_s7l` extended (Q9 block).** ONLY where the org records a numeric
  `capacity` on its authority object AND a band + numeric threshold exist, `q9` gains an additive
  **`capacity_planning_attention`** = `{flag, why}` with ONE deterministic rule from recorded numbers
  only: **at-capacity** when the recorded `load >= 1.0`; **deficit** when the horizon band's worst-side
  magnitude (band_horizon low for higher-is-better, high for lower-is-better) reaches/exceeds the
  recorded capacity VALUE; otherwise **headroom**. `why` states the recorded capacity value/unit/load +
  the horizon-wide band and labels the result as a derived REASON — NEVER a fabricated capacity figure,
  NEVER a directive. An org that records no capacity carries NO such key (byte-identical superset); the
  Sprint-25 `band_capacity_attention` flag is untouched.
- **All frozen functions untouched** (`reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`,
  `_aggregate`, `rank`, `machine_eligible_best`, `render_tradeoff`, `cockpit_q7q8`,
  `render_cockpit_s7l`, `forecast_metric`, `record_metric_series`, `record_capacity`); 49 `$defs`, URI
  cap, SPEC v0.22, `ros/` + schema + sector instances untouched; schema hash `7fc38c8c…`.
- **`run_forecast_horizon2_demo.py` (new, exit 0 = ALL PASS, 63 checks)** drives the same ≥5 fresh
  orgs as Sprint 25 (reusing its builders/constants so the source recorded data is byte-identical):
  - **`deli-forecast`** (higher-is-better deteriorating, recorded variances, NO band_variance): Q3
    `why` == the EXACT pre-Sprint-26 string + the shared suffix (strict-prefix byte-identity):
    `… worst side 0.71 below target 0.95 — horizon-wide recorded band 0.71…0.93 across 3 projection
    periods (band_periods/band_horizon, same recorded σ)`. Iterates the Sprint-23/24 last-point band
    0.71…0.89 (+ band_horizon 0.71…0.93) intact.
  - **`deli-varmax`** (whole-series `band_variance:"all"`, σ0.18): Q3 `why` keeps the single-worst
    band 0.62…0.98 + the `(band_variance all)` source phrase as a strict prefix and ENDS with the
    horizon-wide suffix naming 0.62…1.02 (widens past the single-worst 0.98 — earlier period at +σ).
  - **`deli-varmax-cap`** (same band + a RECORDED capacity 500.0 resolutions/day, load 0.72): Q9 gains
    `capacity_planning_attention` = `{flag: False, why: "capacity-planning: recorded capacity 500.0
    resolutions/day (load 0.72) vs the horizon-wide recorded band 0.62…1.02 across 3 projection
    periods — derived headroom from recorded numbers only (not a directive, no invented capacity)"}`.
  - **`deli-flat2`** (recorded series, NO variance — no-band control) + **`deli`** (no-data): carry NO
    Q3 suffix and NO `capacity_planning_attention` / `band_capacity_attention` (byte-identical).
  - Asserts: full §7L Q1–Q10; the Q3 why strict-prefix + horizon suffix; capacity-planning present
    ONLY on `deli-varmax-cap` and labeled headroom from the recorded numbers; `band_periods` /
    `band_horizon` / `band_capacity_attention` unchanged; determinism (dict + render); no §6 overrule
    (Q8 recommendation unchanged vs `cockpit_q7q8`); no wall-clock / no invented number. Emits
    fixtures + `artifacts/adjudication/reports/cockpit-forecast-horizon2.md`.

## §16 verdict
**Q3 and Q9 capacity attention now carry the recorded whole-horizon worst case AS DATA where it
exists.** Q3's forecast-driven attention `why` appends the exact `band_horizon` range (same shared
constant as the do-nothing summary -> verbatim by construction) behind the Sprint-23/24/25
single-worst phrase, which stays a strict prefix — so the human's FIRST attention line and the
Q8/do-nothing pricing finally agree on the record-wide worst case. Where the org records a numeric
`capacity`, Q9's `capacity_planning_attention` states the recorded capacity value/unit/load vs the
horizon-wide band and labels headroom / at-capacity / deficit as a derived REASON from recorded
numbers only — never an invented figure, never a directive. The default is byte-identical except the
additive Q3 suffix (band orgs) and the capacity-only `capacity_planning_attention` key; a no-capacity /
no-band / no-data org carries neither. The Q8 recommendation is UNCHANGED — attention + capacity
reasoning never overrule the §6-floor-gated machine-eligible best. **Still not derivable:** an org with
no recorded point variances cannot be priced as a band (correct); an org that records no capacity gets
no capacity-planning line (correct); and this remains a recorded-spread range, NOT a probabilistic
confidence interval (a stochastic/adaptive forecast stays out of the deterministic ~$0 stance).

## Verification (real output, all exit 0)
- New: `run_forecast_horizon2_demo.py` -> **ALL PASS** (63 checks).
- Full non-regression: `run_forecast_horizon_demo.py` + `run_forecast_variance_all_demo.py` +
  `run_forecast_variance_demo.py` + `run_forecast_direction_demo.py` + `run_forecast_action_demo.py` +
  `run_forecast_capacity_demo.py` + `run_cockpit_s7l_demo.py` + `run_cockpit_q7q8_demo.py` +
  `run_adjudication_engine_demo.py` -> ALL PASS.
- Conformances: `conformance_adjudication` (16 labels) + dispute/interest/lifecycle/tradeoff -> ALL
  PASS; the new `deli-forecast`/`deli-varmax`/`deli-varmax-cap`/`deli-flat2` fixtures each pass the
  Sprint-0 C1–C5 (26 instances, 49 `$defs`) — the new `capacity_planning_attention` keys are C2-safe.
- Sectors: `instances/build_all.py` (12) + `conformance_all.py` -> ALL SECTORS PASS.
- S5 reference `run_s5_demo.py` -> ALL PASS; `agent_demo/run_agent_demo.py` +
  `agent_demo/conformance_agent.py` -> ALL PASS.
- Schema hash `7fc38c8c…` unchanged, 49 `$defs`, SPEC v0.22, `ros/` + schema untouched, no new noun.

## Roll-forward
Additive Sprint-26 addendum in `docs/ENGINE-FORECAST-ACTION.md` + `docs/ENGINE-FORECAST-CAPACITY.md`
(§10); `instances/README.md` Sprint-26 entry;
`/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after Sprint 26" note;
Sprint-26 addendum in the `relational-os` skill's `references/forecast-action-closure.md`.
SPEC stayed v0.22 (no normative gap surfaced).