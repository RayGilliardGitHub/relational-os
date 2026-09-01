# SPRINT 23 — PLAN

**Goal:** the Q8/trade-off do-nothing expected-impact prices a projected BAND (worst ± recorded
variance) instead of a single point, while the Sprint-22 single-point output stays byte-identical by
default (no recorded variance -> unchanged; the variance-carrying orgs GAIN additive `variance`/`band`
fields + an additive summary phrase, everything pre-existing preserved).

**Scope (additive only):** modify `instances/contested_reality/adjudication_engine.py` —
`_forecast_closure` (band compute + additive keys + extended summary/why) and `render_cockpit_s7l`
(additive band suffix on the Q8 do-nothing line). Frozen functions untouched. 49 `$defs`, URI cap,
SPEC v0.22, `ros/` + schema untouched.

## Baseline (verified 2026-09-01, all exit 0)
Sprint-22 `run_forecast_direction_demo.py`, Sprint-21 `run_forecast_action_demo.py`, Sprint-20
`run_forecast_capacity_demo.py`, the 12 curated C-R demos, `run_cockpit_s7l_demo.py`,
`conformance_adjudication.py` (16 labels), `conformance_{dispute,interest,lifecycle,tradeoff}.py`,
`instances/build_all.py` + `conformance_all.py`, Sprint-5 reference `run_s5_demo.py` +
`run_s5_conformance.py`, `instances/agent_demo/run_agent_demo.py`. Schema JSON hash `7fc38c8c…` 49
$defs, SPEC v0.22.

## Design
- `rc = _num(fc["recorded_variance"])` (last recorded point's `variance`) — None => no band (byte-identical).
- When numeric: `sigma = abs(rc)` (magnitude), `low = worst - sigma`, `high = worst + sigma`
  (round 4), `crosses` = worst-side crossing in the metric's direction
  (higher-is-better: `low < threshold`; lower-is-better: `high > threshold`).
- Additive keys on the closure, `q8["forecast"]`, and `do_nothing_expected_impact`:
  `recorded_variance` (closure/forecast) / `variance` (do_nothing), `band = {worst,sigma,low,high,crosses}`,
  and `expected_last` (the recorded expected last value as the anchor). Only present when `band` exists.
- Summary + Q3 attention `why` append an additive band phrase (old string stays a strict prefix).
- No-data (available=False) path and no-variance control: byte-identical.

## Steps
1. plan.md (this) + work/1-<step>-plan.md before each build.
2. Patch `_forecast_closure` (band + additive keys + summary/why phrase).
3. Patch `render_cockpit_s7l` (additive band suffix on Q8 do-nothing line).
4. New runner `run_forecast_variance_demo.py` (>=4 orgs: deli-forecast, deli-flat2 variance-less
   control, deli-cost, deli) with the full assertion set + fixtures + report.
5. Update `run_forecast_direction_demo.py` (the ONLY runner with strict `==` on summary/why) to
   additive-aware superset checks (old assertion strings become prefix checks; additive keys asserted).
6. Docs: `docs/ENGINE-FORECAST-VARIANCE.md` + additive notes in `docs/ENGINE-FORECAST-DIRECTION.md`;
   `instances/README.md` entry; `STRESS-TEST-SCENARIOS.md` note.
7. Non-regression: re-run the whole baseline + new runner; verify schema hash, ros/, SPEC, sectors.
8. `sprints/sprint-23/summary.md` + `notes/findings.md`; write `sprints/sprint-24/PROMPT.md`.

## DoD
All the above green (exit 0); superset byte-identity on deli-forecast/forecast-flat (pre-existing
fields/lines unchanged, additive keys/phrase added); variance-less control exactly single-point;
recorded-data-only derivation; no §6 overrule; no new noun; SPEC v0.22; 49 `$defs`.