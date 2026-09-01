# SPRINT 27 — SUMMARY

**The recorded capacity now reaches the §7L Q7/Q8 trade-off as a data-only REASON: where the org
records a numeric `capacity`, both Q7 and Q8 carry an additive `capacity_constraint` marker — naming
the recorded capacity value/unit/load + the horizon-wide recorded band and deriving ONE reason
(headroom / at-capacity / deficit) from recorded numbers only — WITHOUT removing any option,
WITHOUT changing the Q8 recommendation's ranking, and NEVER overruling the §6 human.**

## What closed
Sprint 26 disclosed in its own findings ("Open issues / next work") the next honest frontier: the Q9
`capacity_planning_attention` is a derived, labeled REASON, **but it does NOT connect to the §7L
Q7/Q8 trade-off** — an org that records a capacity deficit / at-capacity reason still sees the SAME
machine-eligible options and the SAME Q8 recommendation as if its capacity were unbounded. Sprint 27
closes that bounded slice additively.

## What was built (additive, real output)
- **A shared deterministic rule, `_capacity_reason(capacity_obj, band_horizon, direction)`** — extracted
  from the Sprint-26 Q9 `capacity_planning_attention` rule (headroom / at-capacity when recorded
  `load >= 1.0` / deficit when the horizon band's worst-side magnitude reaches/exceeds the recorded
  capacity VALUE), so the Q9 reason and the new Q7/Q8 reason AGREE BY CONSTRUCTION. The Sprint-26 Q9
  block inside `cockpit_s7l` was refactored to call it — output provably byte-identical
  (`run_forecast_horizon2_demo.py` still ALL PASS).
- **`cockpit_s7l` gains an additive Sprint-27 block.** ONLY where the org records a numeric `capacity`
  AND a band + numeric threshold exist, BOTH **`q7`** and **`q8`** carry an additive
  **`capacity_constraint`** block (a PARALLEL block — the frozen `rank`-owned `options`/`tradeoff` and
  the `cockpit_q7q8` bytes are untouched), per the prompt's preferred design:
  `recorded_capacity` (value/unit/load AS RECORDED), `horizon_band` ({low,high} = the closure
  `band_horizon`), `reason`, `flag`, `options_flagged`, `note`. In headroom no option is flagged; at
  at-capacity/deficit the capacity-consuming (non-baseline) options are marked `capacity_risk` — NEVER
  `capacity_infeasible` (no per-option capacity requirement is ever recorded, so infeasibility is
  never derivable); the baseline (do-nothing/UNRESOLVED) is never flagged. It never removes an option,
  never changes `machine_eligible_best`/the Q8 recommendation.
- **Frozen functions untouched** (`reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`,
  `rank`, `machine_eligible_best`, `render_tradeoff`, `cockpit_q7q8`, `render_cockpit_s7l`);
  49 `$defs`, URI cap, SPEC v0.22, `ros/` + schema + sector instances untouched; schema hash
  `7fc38c8c…`; no new noun; the new keys are C2-safe.
- **`run_forecast_horizon3_demo.py` (new, exit 0 = ALL PASS)** drives the SAME ≥5 fresh orgs as
  Sprint 26 (reusing `r26.build_orgs()` so the source recorded data is byte-identical):
  - **`deli-varmax-cap`** (recorded capacity 500.0 resolutions/day, load 0.72, horizon band 0.62…1.02)
    carries `capacity_constraint` on BOTH `q7` and `q8`:
    `{recorded_capacity: "500.0 resolutions/day (load 0.72)", horizon_band: {low: 0.62, high: 1.02},
    reason: "headroom", flag: false, options_flagged: {}, note: "…UNCHANGED…human always rules"}` —
    headroom (load < 1.0 AND horizon worst-side 0.62 < capacity 500.0) → **NO option marked
    infeasible**. The Q8 `reason` equals the Q9 `capacity_planning_attention` label by construction.
  - **`deli-forecast`** (band, NO capacity), **`deli-varmax`** (band, NO capacity), **`deli-flat2`**
    (no-band control), **`deli`** (no-data): carry **NO** `capacity_constraint` key on `q7` or `q8`
    (byte-identical superset).
  - Asserts: full Q1–Q10; the Q3 horizon suffix + Q9 `capacity_planning_attention` still present /
    UNCHANGED (Sprint-26 byte-identity); the marker present on ONLY `deli-varmax-cap` and never on the
    others; per every org Q7 `options` (count + uris) + Q8 `recommendation`/`machine_eligible_best`
    EQUAL to `cockpit_q7q8` (no §6 overrule, no re-rank); pre-existing Q7/Q8 keys intact; determinism
    (dict + render); no wall-clock / no invented number (the marker's `recorded_capacity` == the graph
    field, `horizon_band` == the closure `band_horizon`); and a helper-level at-capacity/deficit check
    proving the non-headroom branch is not vacuous. Emits fixtures +
    `artifacts/adjudication/reports/cockpit-forecast-horizon3.md`.

## §16 verdict
**Yes — the recorded capacity now reaches the Q7/Q8 trade-off as a data-only REASON, and the Q8
recommendation provably stays unchanged.** Where the org records a numeric `capacity` (+ a band +
numeric threshold), both the Q7 trade-off and the Q8 line name the recorded capacity value/unit/load
and the horizon-wide recorded band, mark any capacity-consuming option the recorded numbers put at- or
over-capacity as `capacity_risk`, and derive ONE deterministic reason (headroom / at-capacity /
deficit) that BY CONSTRUCTION equals the Q9 `capacity_planning_attention` label. It is a LABEL — never
a removal, never a directive, never an overrule: the option set is byte-identical, `machine_eligible_best`
and the Q8 recommendation are asserted EQUAL to `cockpit_q7q8` for every org, and the §6 human always
rules. The default is byte-identical: a no-capacity / no-band / no-data org carries no
`capacity_constraint` key. **Still not derivable:** the marker does not CHOOSE a different option for
the machine (the §6 human always does), and a genuinely capacity-constrained optimization that
**re-ranks** the recommendation stays out of scope of the deterministic advisory stance — the engine
can never reach `capacity_infeasible` without a RECORDED per-option capacity requirement (it never
invents one), and an org with no recorded point variances cannot be priced as a band (correct).

## Verification (real output, all exit 0)
- New: `run_forecast_horizon3_demo.py` -> **ALL PASS** (all curated checks).
- Full non-regression: `run_forecast_horizon2_demo.py` + `run_forecast_horizon_demo.py` +
  `run_forecast_variance_all_demo.py` + `run_forecast_variance_demo.py` + `run_forecast_direction_demo.py`
  + `run_forecast_action_demo.py` + `run_forecast_capacity_demo.py` + `run_cockpit_s7l_demo.py` +
  `run_cockpit_q7q8_demo.py` + `run_adjudication_engine_demo.py` -> ALL PASS.
- Conformances: `conformance_adjudication` (16 labels) + dispute/interest/lifecycle/tradeoff -> ALL
  PASS; the four recorded-org fixtures each pass the Sprint-0 C1–C5 (26 instances, 49 `$defs`) — the
  new `capacity_constraint` keys are C2-safe.
- Sectors: `instances/build_all.py` (12) + `conformance_all.py` -> ALL SECTORS PASS.
- S5 reference `run_s5_demo.py` + `run_s5_conformance.py` -> ALL PASS; agent demo + conformance ->
  ALL PASS.
- Schema hash `7fc38c8c…` unchanged, 49 `$defs`, SPEC v0.22, `ros/` + schema untouched, no new noun.

## Roll-forward
Additive §11 in `docs/ENGINE-FORECAST-CAPACITY.md`; §9 in `docs/ENGINE-S7L-COCKPIT.md`;
`instances/README.md` Sprint-27 entry; "Update after Sprint 27" note in
`/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; Sprint-27 addendum in the
`relational-os` skill's `references/forecast-action-closure.md`. SPEC stayed v0.22 (no normative gap
surfaced).