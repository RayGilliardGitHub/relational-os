# SPRINT 31 — plan: inventory the ENTIRE recorded-data §7L decision surface as reason-not-choice, and name the ONE remaining out-of-scope seam (a capacity-constrained OPTIMIZATION that re-ranks for the machine)

## Objective
Sprint 30 closed the label-vs-choice boundary at its sharpest (a RECORDED per-option requirement
makes the machine-eligible best / Q8 recommendation ITSELF `capacity_infeasible`, yet the cockpit
provably still recommends it — `adjudication_engine.py` byte-identical). After six sprints
(20–26 forecast series/variance/band, 27 emergency capacity_constraint, 28 horizon limit,
29 per-option infeasibility, 30 the recommended-option boundary) the whole §7L decision surface is
recorded-data + reason. Sprint 31 makes that the ORGANIZING truth: a survey/boundary runner that, for
a set of orgs, emits a per-org **decision-surface inventory** (`recorded_surface`) proving every
derived label traces to a recorded descriptor and is a REASON, never a CHOICE; totalling the
reason-not-choice proof (Q7 options + machine_eligible_best + Q8 recommendation + floor_gated
EXACTLY == `cockpit_q7q8` for EVERY org); and naming the SOLE remaining out-of-scope separator (a
capacity-constrained OPTIMIZATION that would RE-RANK the recommendation — a policy/user decision,
deliberately NOT built). Positive consolidation, NOT a new capability.

## IS / IS NOT
- **IS**: a new, engine-native-runner `run_recorded_surface_demo.py` (no engine change) that
  (1) drives the eight Sprint-30 orgs byte-identical, plus INSPECT + COVE + one no-data org (new
  labels only), (2) emits a structured `recorded_surface` per org, (3) asserts each derived reason
  traces to a recorded descriptor, (4) proves Q7/Q8 reason-not-choice equality for EVERY org with a
  tally, (5) names the optimization seam exactly, (6) adds additive docs (§15 / §13 / README /
  stress-test / §16) and the roll-forward files.
- **IS NOT**: building the OPTIMIZATION (a re-rank that MOVES the Q8 recommendation is a policy /
  user decision — out of scope); re-implementing `run_scenario`/`reconcile`/`cockpit_q7q8`/`rank`/
  `machine_eligible_best`/`render_tradeoff`/`_derive`/`_aggregate`/`_capacity_reason`/
  `_per_option_capacity_flags`; changing the frozen `rank`; probabilistic/stochastic forecast; a new
  noun / URI / schema / `$defs`; S5 (Trust) change; fabricated descriptors. The recommendation is
  NEVER re-picked by the machine.

## Method / invariants (from the relational-os skill + PROTOCOL)
Single-threaded; plan-before-build; real tool output only; ~$0 (local python3); additive; frozen
ontology / URI cap / 49 `$defs`; SPEC v0.22; Frozen strings: engine hash `a60f8f7…` must stay
unchanged (pure runner + recorded data, as Sprint 30). Footguns to respect: `Graph.get(uri)` one
arg (`(graph.get(u) or {})`); `evidence`/`rules_applied` are arrays; MERGE-not-replace
(`{**graph.get(u), ...}`); no additive key ending in a temporal suffix; runner CWD-sensitivity
(build from `instances/contested_reality`); `relabel_to`/`run_one`/`VM_POINTS`/`CO_POINTS`/`r26.*`/
`r29.*`/`r30.*` reuse; Sprint-0 venv `./sprints/sprint-0/artifacts/.venv/bin/python` for conformance,
absolute venv path; adopt the module-vs-local naming rule (no `G` shadowing).

## Sub-sprints (each gets its own `work/<n>-plan.md` before building)
1. **Green baseline FIRST (Sprint-30 state).** From `instances/contested_reality`: run ALL the prior
   CR demo runners (forecast label-vs-choice, per_option_capacity, horizon4/3/2/horizon,
   variance_all/variance, direction, action, capacity, cockpit_s7l, cockpit_q7q8,
   adjudication_engine) with plain python3; all 5 CR conformances with the Sprint-0 venv;
   `build_all.py` + `conformance_all.py` (12 sectors); S5 reference
   (`sprints/sprint-5/artifacts/run_s5_demo.py` + `run_s5_conformance.py`); agent
   (`instances/agent_demo/run_agent_demo.py` + `conformance_agent.py`). Record every exit code;
   capture `adjudication_engine.py` sha256 `a60f8f7…`, schema sha `7fc38c8c…`, 49 `$defs`, SPEC v0.22.
2. **Design + build `run_recorded_surface_demo.py`.** New orgs (name, do not overwrite fixture dirs):
   `inspect-recorded` (INSPECT relabel + recorded metric series + authority `capacity` + per-option
   `capacity_requirements`), `cove-recorded` (COVE relabel + same), and one no-data org
   `inspect-nodata` (INSPECT relabel, NO recorded series/capacity/requirements). Reuse the eight
   Sprint-30 orgs byte-identical. Emit `recorded_surface` per org:
   `{label, present_recorded={metric_series, point_variance, band_variance, capacity,
   capacity_requirements, floor_gated, weights, reconcile_rule}, derived_reasons={Q3_forecast,
   Q6_projection, Q7Q8_capacity_constraint, Q9_capacity, Q8_do_nothing_impact}, derivable_universe=[
   sorted derived reasons], not_derivable=[named optimization seam + any descriptor NOT recorded]}`.
   Per-org assertion: every present derived reason traces to a recorded descriptor. Then the
   reason-not-choice proof for EVERY org: `q7.options`+`machine_eligible_best`+`q8.recommendation`+
   `floor_gated` EXACTLY == `cockpit_q7q8`, with a printed tally (`N/N orgs: the marker never
   re-ranks; includes the org where the RECOMMENDED option is capacity_infeasible` — name the
   Sprint-30 `deli-recommend-infcap` org explicitly). Determinism (dict + render) on re-run. Emit
   fixtures for the NEW orgs + the engine-native report
   `artifacts/adjudication/reports/cockpit-recorded-surface-inventory.md`. Exit 0 = ALL PASS.
3. **Run + verify.** New runner ALL PASS; full non-regression still green; byte-identity of the
   reused orgs (the new runner's capacity blocks / equalities are a strict superset); engine hash
   `a60f8f7…` unchanged; schema `7fc38c8c…`; 49 `$defs`; SPEC v0.22; `ros/` + schema + sector
   `configs.py` untouched; no `://qk/` in config-driven fixtures.
4. **DOCUMENT (additive).** `docs/ENGINE-FORECAST-CAPACITY.md` §15 + `docs/ENGINE-S7L-COCKPIT.md`
   §13 (the surface is now inventoried reason-not-choice; no recorded data ever re-ranks; the
   optimization seam is named); extend the §16 verdict; `instances/README.md` Sprint-31 entry;
   `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after Sprint 31" note;
   reference the new runner in `references/` if useful. NO SPEC bump (v0.22) unless a genuine
   normative gap surfaces (log then).
5. **Roll forward.** `sprints/sprint-31/summary.md` + `notes/findings.md`; write the next self-contained
   `sprints/sprint-32/PROMPT.md`.

## Definition of Done (all real exit-0 output)
- Green baseline captured FIRST (Sprint-30 state) — every prior demo + conformance + sector + S5 + agent.
- `python3 run_recorded_surface_demo.py` → **RESULT: ALL PASS** (the inventory + reason-not-choice
  tally + frontier naming; new orgs named; determinism).
- Reason-not-choice tally prints explicitly — every org Q8 == `cockpit_q7q8`, Sprint-30
  `deli-recommend-infcap` (recommended option capacity_infeasible) named in the tally.
- Non-regression full green after the new runner; `adjudication_engine.py` hash `a60f8f7…` unchanged;
  schema `7fc38c8c…`; 49 `$defs`; SPEC v0.22; `ros/` + schema + sector configs untouched; reused
  orgs byte-identical (strict superset).
- Honest §16 verdict: the surface is fully recorded-data + reason WHILE Q8 provably stays the frozen
  `rank` output; the ONE remaining out-of-scope step (capacity-constrained OPTIMIZATION that re-ranks,
  a policy/user decision; + a per-option requirement not unit-coupled / an option with no recorded
  requirement) is named, not built.
- All four doc files rolled forward; summary/findings/PROMPT-32 written.