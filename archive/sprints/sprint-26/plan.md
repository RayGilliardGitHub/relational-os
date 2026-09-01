# SPRINT 26 — PLAN

## Mandate (from sprints/sprint-26/PROMPT.md)
Two additive, recorded-data-only closures on `instances/contested_reality/adjudication_engine.py`
(Sprint 25 disclosed both in `notes/findings.md` "Open issues / next work"):

1. **Q3 forecast-driven attention names the horizon-wide range.** In `_forecast_closure`, when a
   band exists AND the attention item was created, APPEND an additive suffix to
   `attention_item["why"]` that names `band_horizon` (e.g.
   ` — horizon-wide recorded band {lo}…{hi} across {n} projection periods
   (band_periods/band_horizon, same recorded σ)`), AFTER the Sprint-23/24/25 single-worst band
   phrase (+ the Sprint-24 band_source phrase) so the old `why` stays a strict prefix. No-band /
   no-data orgs: no suffix (unchanged). The do-nothing summary reuses the SAME constant so
   Q3/Q8/do-nothing agree verbatim by construction.
2. **Q9 data-only capacity-planning attention.** In `cockpit_s7l`'s Q9 block, ONLY when the org
   records a numeric `capacity` on its authority object `AND` a band + numeric threshold exist,
   add an additive **`capacity_planning_attention`** = `{flag, why}`. `flag` = one deterministic
   rule: deficit when the horizon band's worst-side magnitude reaches/exceeds the recorded
   capacity value, or the org is at/over recorded capacity (recorded `load >= 1.0`); otherwise
   headroom. `why` states the recorded numbers plainly (recorded capacity value/unit/load vs the
   horizon-wide band) and labels headroom/at-capacity/deficit as a derived REASON — NEVER a
   fabricated capacity number, NEVER a directive. No capacity recorded → no key (byte-identical).
   Sprint-25 `band_capacity_attention` stays intact (additive superset).

## Files touched (additive only)
- `instances/contested_reality/adjudication_engine.py` — extend `_forecast_closure` (Q3
  attention-why block) + `cockpit_s7l` (Q9 block). Frozen functions untouched.
- `instances/contested_reality/run_forecast_horizon2_demo.py` — NEW runner.
- Docs: `docs/ENGINE-FORECAST-ACTION.md` + `docs/ENGINE-FORECAST-CAPACITY.md` (addenda),
  `instances/README.md`, `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`.
- `sprints/sprint-26/summary.md`, `notes/findings.md`, `sprints/sprint-27/PROMPT.md`.
- No `SPEC.md` bump (v0.22) unless a genuine normative gap surfaces (expected none). 49 `$defs`,
  URI cap, `ros/`, schema hash `7fc38c8c…` unchanged.

## Plan (each sub-step needs work/<n>-plan.md first)
1. Capture green baseline BEFORE edits: Sprint-25/24/23/22 forecast runners +
   `run_cockpit_s7l_demo` + `run_forecast_action_demo` + `run_forecast_capacity_demo` + the 12
   curated C-R demos + `conformance_adjudication` (16 labels) + prior 4 CR conformances +
   `build_all.py`/`conformance_all.py` + S5 reference/conformance + agent demo.
2. Engine edit 1: `_HORIZON_BAND_PHRASE` module constant + Q3 attention `why` suffix in
   `_forecast_closure`; reuse the constant in the do-nothing summary phrase.
3. Engine edit 2: Q9 `capacity_planning_attention` in `cockpit_s7l`'s Q9 block (gated on
   `capacity_recorded` + band + numeric threshold), deterministic deficit/at-capacity/headroom rule.
4. New `run_forecast_horizon2_demo.py`: ≥5 orgs (deli-forecast, deli-varmax, deli-varmax-cap
   [records capacity 500.0/day load 0.72], deli-flat2 no-band control, deli no-data) asserting:
   full Q1–Q10; Q3 why keeps Sprint-23/24/25 string as strict prefix AND now carries the
   horizon-wide range suffix; varmax-cap Q9 gains capacity_planning_attention (why names
   500.0/load 0.72 + horizon band + headroom label); other orgs carry NO such key (byte-identical);
   band_periods/band_horizon/band_capacity_attention unchanged; determinism; no §6 overrule
   (Q8 recommendation unchanged); no wall-clock / no invented number. Emit fixtures + report.
5. Full non-regression re-run (baseline + new) — ALL exit 0.
6. Docs + README + STRESS-TEST + summary + findings + sprint-27 PROMPT.

## Verification / honest §16
- Q3 + Q9 capacity attention now carry the recorded whole-horizon worst case as data where it
  exists (Q3 suffix + capacity-planning reason are derived from recorded series/variance/capacity
  only); capacity planning is a data-only REASON (label), never a fabricated figure or directive.
- Still not derivable: an org with no recorded point variances (no band) and an org that records
  no capacity (no capacity-planning line); this remains a recorded-spread range, NOT a
  probability/confidence interval; a capacity-DEFICIT number beyond the recorded metric is never
  invented.

~$0, single-threaded, real tool output only.