# SPRINT 21 — plan

Goal: close the honest frontier Sprint 20 disclosed — the recorded Q6 forecast is COMPUTED and RENDERED
but not CONNECTED to the org's decision surface. Sprint 21 makes the RECORDED forecast DRIVE the
§7L Q3 attention and the Q8 expected-impact / trade-off do-nothing baseline, deterministically and
data-only, with the honest no-data fallback unchanged. No new noun, no §6 overrule.

## Why this is the right next slice
§7K.1's Decision→Expected→Variance→WHY loop and §7J.5 attention exist precisely to turn a measured or
forecast gap into prioritized action. Sprint 20 built `forecast_metric` + `_recorded_metric_with_series`
the engine reads to answer Q6 ("what if we do nothing?"). Sprint 21 is the bounded, additive step that
makes that same recorded projection flow into Q3 ("so it becomes attention") and Q8/trade-off ("and the
do-nothing baseline is priced"), so Q6→Q3→Q8 are connected AS DATA where the data exists.

## What IS / IS NOT (prompt §What Sprint 21 IS and IS NOT)
IS: Q3 gains a **forecast-driven attention item** (tagged `forecast`) when the horizon projection
crosses a recorded threshold; Q8 + the trade-off carry a **projected-cost do-nothing expected-impact**
from the deterministic projection. No-data orgs keep today's Q3/Q8/trade-off exactly.
IS NOT: new service/noun/schema edit; no Trust change; no machine overrule of the §6 human (forecast only
prices attention + do-nothing cost — Q8 recommendation stays the floor-gated machine-eligible best and
the determination stays the `determination_policy` call); no rewrite of the frozen functions
(`reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/`rank`/`machine_eligible_best`/
`render_tradeoff`/`cockpit_q7q8`).

## Files (additive; ONLY the engine file may change engine code)
- `instances/contested_reality/adjudication_engine.py` — the ONE permitted engine edit:
  + a small module-level numeric coerce helper;
  + extend `cockpit_s7l`'s `.q3` (append the forecast-driven attention item when the projection crosses
    a recorded threshold) and `.q8`/trade-off (add additive `forecast` + `do_nothing_expected_impact`
    fields priced from the projection, only when a recorded series exists);
  + extend `render_cockpit_s7l` to render the new Q3 forecast item + the projected-cost do-nothing line
    where present.
  `cockpit_q7q8` is NOT rewritten — the forecast info is added to the `base`-returned `q7`/`q8` dicts
  additively after the delegation, so no-data orgs stay byte-identical.
- `instances/contested_reality/run_forecast_action_demo.py` — NEW runner (exit 0 = ALL PASS).
- Docs (no SPEC bump): `docs/ENGINE-FORECAST-ACTION.md` (new), additive note in
  `docs/ENGINE-FORECAST-CAPACITY.md`, `instances/README.md` Sprint-21 entry,
  `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` ("Update after Sprint 21"),
  `references/` if useful.
- `sprints/sprint-21/{plan.md,work/1-plan.md,notes/findings.md,summary.md}`,
  `sprints/sprint-22/PROMPT.md` (next prompt).

## The threshold rule + do-nothing pricing (state plainly, deterministically)
From a recorded `metric://` realized-vs-expected series + `forecast_metric`:
- **Threshold** (recorded, in order): an explicit **`forecast_threshold`** additive field on the metric
  object → else the metric's own **`target`** → else the **last recorded `actual`** (so a declining
  series with no target still flags). C2-safe key (`forecast_threshold` — not a temporal suffix).
- **Crossing** = any horizon projection lands on the "worse" side of the threshold (for a
  higher-is-better rate metric: `min(projections) < threshold`).
- **Forecast-driven attention** (Q3): when crossing, append
  `{"item": <metric>, "why": "forecast: projected to fall below <threshold> (<source>) — worst
  <min> at period H", "tag": "forecast"}`. This is ATTENTION — never an auto-pick.
- **Do-nothing expected-impact** (Q8 + trade-off): when a recorded series exists, price the do-nothing
  baseline from the projection: a structured `do_nothing_expected_impact` (baseline option, priced=True,
  summary with threshold/on-target vs below, `on_target` bool) + a `forecast` field carrying
  projections/threshold/worst. Below-threshold → "forecast-driven do-nothing cost"; on/above → "labelled
  on-target, no forecast-driven cost". Q8 `recommendation` is UNCHANGED (floor-gated machine-eligible
  best) — the forecast never overrules the §6 pick.

## The ≥3-org proof (runner)
1. **deli-forecast** (Sprint-20, recorded series THAT DETERIORATES: last actual 0.86, mean delta −0.02,
   projections [0.84,0.82,0.8] vs target 0.95) → Q3 gains the `forecast` attention item; Q8/trade-off
   price do-nothing from the projection (below-threshold cost).
2. **a recorded-control** (new, series FLAT/above-target: projections stay ≥ target) → NO forecast
   attention item; do-nothing still priced but **labelled on-target**.
3. **deli** (Sprint-20, no recorded series) → unchanged Q3/Q8/trade-off fallback (byte-identical).
Asserts: full §7L Q1–Q10 on each; Q3 forecast item only on the deteriorating org; Q8 recommendation
identical to `cockpit_q7q8` for every org (no §6 overrule); do-nothing priced from the recorded
projection; agreement between Q3/Q8 projection and `forecast_metric` on the same org; determinism
(cockpit_s7l re-run + render identical); no-data org fallback matching Sprint 20; no wall-clock.
Emits fixtures + a report. Exit 0 = ALL PASS.

## Verification / Definition of Done (all exit 0)
- Green baseline recorded FIRST (DONE — see below under "Baseline").
- New runner ALL PASS; full non-regression green (all 12 CR runners + conformance_adjudication 16 labels
  + `run_cockpit_s7l_demo` + the 4 prior CR demos + conformances + sector `build_all`/`conformance_all` +
  S5 reference + conformance + agent demo + conformance).
- `deli`/`cove` byte-identical up to clock (engine demo run twice, timestamp keys stripped → identical).
- Schema JSON hash `7fc38c8c…`, **49 `$defs`**, **SPEC v0.22**, `ros/` untouched, URI cap, no new noun.

## Baseline (verified before any change)
Demos: run_forecast_capacity, run_cockpit_s7l, adjudication_engine, rule_comparison, rule_authoring,
rule_library, cockpit_q7q8, reconcile_learning, dispute, interest_conflict, tradeoff, full_dispute —
all `RESULT: ALL PASS` exit 0. Conformance_adjudication 16 labels ALL PASS. Sector build_all +
conformance_all ALL PASS. S5 reference demo + conformance ALL PASS. Agent demo + conformance
(conformance_agent.py) ALL PASS. Schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22 (hash `d10f0010…`).

## Sequencing (single-threaded)
1. plan.md + work/1-plan.md
2. engine additive closure (.q3/.q8/render) — `work/2-build.md`
3. runner `run_forecast_action_demo.py` — `work/3-runner.md`
4. run it → ALL PASS; then full non-regression + conformance + byte-identity
5. honest docs + findings + summary + sprint-22 prompt