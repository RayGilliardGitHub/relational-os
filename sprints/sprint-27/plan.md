# SPRINT 27 — PLAN (capacity-constraint annotation on the §7L Q7/Q8 trade-off)

**Objective.** Sprint 26's Q9 `capacity_planning_attention` (a data-only capacity REASON) does not
reach the §7L Q7/Q8 trade-off: an org that records a capacity deficit / at-capacity reason still sees
the SAME machine-eligible options and the SAME Q8 recommendation as if its capacity were unbounded.
Sprint 27 closes a bounded slice additively: **where the org records a numeric `capacity`, make that
recorded capacity a data-only constraint on the Q7/Q8 trade-off** — an additive **`capacity_constraint`**
marker + reason on the affected option(s), derived from recorded numbers only, WITHOUT removing any
option (the §6 human always rules) and WITHOUT changing the Q8 recommendation's ranking.

## Core design decision (documented, chosen)
**Prefer the parallel block, not per-option mutation.** The frozen `rank` function owns `cfg`
`options` + the ranked list; `cockpit_q7q8`/`render_tradeoff` build the `q7.options`/`q7.tradeoff`
bytes. To keep those untouched (frozen output byte-identical), the capacity constraint rides as a
**parallel additive `capacity_constraint` block on `q7` and on `q8`** (next to
`do_nothing_expected_impact`), plus a lightweight per-option map `options_flagged: {option: marker}`
INSIDE that block (not on the option dicts themselves). This satisfies the prompt's stated preference.

## The ONE deterministic rule (documented, reused from Sprint 26)
Reuse the exact Sprint-26 `capacity_planning_attention` rule so **Q8's reason and Q9's reason agree
by construction** — extract it into a shared additive helper `_capacity_reason(capacity_obj, bh,
direction)` returning `(label, flag)`:
- **headroom** (default) — the recorded load `< 1.0` AND the horizon band's worst-side magnitude
  (`low` for higher-is-better, `high` for lower-is-better) `<=` the recorded capacity VALUE, OR the
  comparison is not derivable (no numeric load / capacity / worst-side).
- **at-capacity** — recorded `load >= 1.0`.
- **deficit** — the horizon band's worst-side magnitude `>=` the recorded capacity VALUE.

**Per-option flags (`options_flagged`).** The ONLY recorded capacity-consumption datum is the org-level
`load`; NO per-option capacity requirement is ever recorded, so the engine can NEVER derive
`capacity_infeasible` — it only ever marks a non-baseline (capacity-consuming) option
**`capacity_risk`** when the recorded numbers signal at-capacity or deficit. In **headroom** no option
is flagged (`options_flagged: {}`). The baseline (`do-nothing`/`unresolved`) consumes no capacity and is
never flagged. This is the honest, deterministic, non-vacuous rule: for `deli-varmax-cap`
(capacity 500.0/day, load 0.72, band 0.62…1.02) → **headroom, NO option flagged** (as the prompt's
runner target states).

## Numbered sub-sprints
0. **Baseline green (done).** Captured Sprint-26 state: all CR runners + 5 conformances (venv) +
   `build_all`/`conformance_all` + S5 reference demo/conformance + agent demo/conformance → all exit 0;
   schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22.
1. **Engine change (additive).** In `adjudication_engine.py`:
   - add `_capacity_reason(capacity_obj, bh, direction)` (the shared deterministic rule);
   - refactor the Sprint-26 Q9 `capacity_planning_attention` block to call it (output byte-identical,
     Q8↔Q9 agree by construction);
   - add a **Sprint-27** block in `cockpit_s7l` (after the Q9 capacity blocks, before Q10) computing a
     `capacity_constraint` block and assigning `q7["capacity_constraint"] = cc` and
     `q8["capacity_constraint"] = cc` ONLY where the org records a numeric capacity + band + numeric
     threshold.
   - Frozen functions untouched; no new noun; 49 `$defs`; C2-safe keys
     (`capacity_constraint`, `recorded_capacity`, `horizon_band`, `reason`, `options_flagged`, `note`,
     `flag` — none ends in `at|time|deadline|expires|expiry|effective|due|since`).
2. **Runner `run_forecast_horizon3_demo.py`** driving the ≥5 fresh orgs (`deli-forecast`,
   `deli-varmax`, `deli-varmax-cap`, `deli-flat2`, `deli` — reusing Sprint-25/26 builders/constants so
   source recorded data is byte-identical) and asserting: full Q1–Q10; Q3 suffix +
   `capacity_planning_attention` still present/unchanged (Sprint-26 byte-identity); `deli-varmax-cap`
   Q7/Q8 carry `capacity_constraint` (recorded capacity 500.0/load 0.72/band 0.62…1.02 → headroom, NO
   option flagged); the OTHER orgs carry NO `capacity_constraint` key (byte-identical superset); Q8
   `recommendation`/`machine_eligible_best` EQUAL to `cockpit_q7q8` for every org (no §6 overrule, no
   re-rank); Q7 option set UNCHANGED (same count/uris); Q8 `capacity_constraint.reason` == Q9
   `capacity_planning_attention` label; determinism; no wall-clock; a helper-level at-capacity/deficit
   check proving the non-headroom branch is not vacuous. Emits fixtures + report.
3. **Non-regression.** Re-run the FULL baseline (all CR runners, 5 conformances, build_all,
   conformance_all, S5, agent) → all exit 0; schema hash unchanged; `ros/` + schema + sector configs
   untouched; new-org fixtures pass Sprint-0 C1–C5.
4. **Docs.** Additive §11 in `docs/ENGINE-FORECAST-CAPACITY.md`; trade-off/cockpit note
   (`ENGINE-Q7Q8-COCKPIT.md` or `ENGINE-S7L-COCKPIT.md`); `instances/README.md` Sprint-27 entry;
   "Update after Sprint 27" note in `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`.
   Do NOT bump SPEC unless a genuine normative gap surfaces (log if so).
5. **Close.** `sprints/sprint-27/summary.md` + `notes/findings.md`; write `sprints/sprint-28/PROMPT.md`.

## Definition of Done (all real exit-0 output)
- New `run_forecast_horizon3_demo.py` → **ALL PASS** (≥ the required assertions above).
- Full non-regression suite → **ALL PASS**; SPEC v0.22; 49 `$defs`; schema hash `7fc38c8c…`; `ros/` +
  schema + sector `configs.py` untouched.
- **Superset byte-identity:** the capacity-recording org unchanged except the additive
  `capacity_constraint` block on Q7/Q8; the variance-carrying no-capacity orgs and the variance-less
  control + no-data org unchanged (carry NO `capacity_constraint` key). Every new value derived from
  recorded series + recorded variance + recorded capacity only.

## Exit criteria / honest boundary
- The marker is a LABEL + reason on the trade-off; it never removes an option, never changes
  `machine_eligible_best`/Q8 recommendation, never overrules the §6 human, and never fabricates a
  capacity number or a per-option requirement. A genuinely capacity-constrained optimization that
  RE-RANKS the recommendation stays out of scope (the deterministic advisory stance) → honest §16
  boundary into Sprint 28.