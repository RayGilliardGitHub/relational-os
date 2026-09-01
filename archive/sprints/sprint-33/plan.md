# SPRINT 33 — plan: consolidate the now-TWO-path decision surface (reason-not-choice ADVISORY + POLICY re-rank) as ONE coherent, provably-composable framework

## Objective
Sprint 31 positively inventoried the WHOLE recorded-data §7L decision surface as reason-not-choice
(11 orgs, NO engine change): the Q8 recommendation provably == the frozen `rank` output; the marker is a
REASON, never a CHOICE. Sprint 32, by explicit prompt authorization, added the ONE named out-of-scope step:
a PURE, additive `capacity_rerank.py` module that, when the machine-eligible best is `capacity_infeasible`
from RECORDED per-option `capacity_requirements`, RE-RANKS the Q8 recommendation for the machine by the
frozen `rank` utility, under an explicit POLICY label, NEVER overwriting the engine's advisory Q8. **Sprint
33 consolidates the now-two-path decision surface** (advisory ≠ re-rank) as ONE coherent decision framework,
and PROVES the two paths never silently interfere. It is a survey/audit runner + recorded data ONLY —
engine and `capacity_rerank.py` byte-identical; no new capability.

## Non-negotiables (from PROMPT + skill)
- **Engine byte-identical**: `adjudication_engine.py` sha256 prefix `a60f8f7…` AND `capacity_rerank.py`
  sha256 (`f7c6a185…`) BOTH recorded before + after; neither file changes.
- **No new capability / no schema / no norm change**: frozen ontology / URI cap / 49 `$defs`; SPEC stays
  v0.22; `ros/` + schema + sector `configs.py` untouched; no new noun; no `://qk/` in new fixtures.
- **Reused orgs byte-identical**: the 11 Sprint-31 orgs + the 2 new Sprint-32 orgs keep every byte; the
  consolidation is a VIEW over the SAME recorded data, not a rewrite.
- Single-threaded (no subagents); plan-before-build (this plan + `work/<n>-plan.md` per step); real tool
  output; ~$0. Raymond: clean English, absolute `file://` paths, report status at each long step.

## The build: ONE new runner `run_two_path_demo.py` (reuses `r32.build()` = 13-org set, engine + rerank untouched)
Reuse Sprint 32's 13-org set (`run_capacity_rerank_demo.build()`, which itself calls `r31.build_orgs()`),
and for each org emit a structured **`two_path_surface`**:
  {label,
   advisory={q7_machine_eligible_best, q8_recommendation (== the engine's advisory, the frozen rank output),
             floor_gated, capacity_constraint(options_flagged)},
   rerank={needed, prior_machine_best, replacement, replacement_is_baseline},
   path: one of {ADVISORY-no-capacity, ADVISORY-best-runnable, RE-RANK}}
and assert (ALL PASS):
- **composition / non-interference**: for every org where rerank.needed=True the advisory Q8 recommendation
  STILL == `cockpit_q7q8` (the re-rank never shadows it) AND rerank.replacement ≠ advisory Q8 recommendation
  (provably different options) AND replacement ≠ advisory machine_eligible_best; for every org where
  needed=False replacement == advisory Q8 (they agree — one path, unchanged).
- **floor integrity**: no advisory or re-rank selection is ever a floor-gated option (asserted against `rank`).
- **determinism vs history**: re-running gives identical `two_path_surface`; AND the Sprint-31 reason-not-choice
  tally (11/11) + the Sprint-32 re-rank results are BOTH reproducible from the SAME recorded data in this run
  (synth the r31 tally + r32 re-rank from the same orgs and assert equality of the previously-recorded
  results — the consolidation is a view, not a rewrite).
- **exhaustive-disjoint taxonomy**: every org is exactly one of {ADVISORY-no-capacity, ADVISORY-best-runnable,
  RE-RANK}; no org is two classes; every org is classified.

## Chosen org set + expected paths (from `r32.build()` = r31's 11 + covr + dai)
RE-RANK (machine best capacity_infeasible -> replacement):
- `deli-recommend-infcap`: partial-settlement -> conditional-resolution
- `inspect-recorded`: rework-partial-credit -> conditional-accept-with-guarantee
- `cove-recommend-infcap` (S32 new): step-therapy-first -> authorize-generic
- `deli-all-infeasible` (S32 new): unresolved baseline (replacement_is_baseline True, all_capacity_consuming_infeasible)
ADVISORY-best-runnable (capacity recorded, best NOT infeasible -> advisory == replacement):
- `cove-recorded` (step-therapy-first = capacity_risk, runnable), `deli-infcap`, `deli-deficit-inf`,
  `deli-varmax-cap`
ADVISORY-no-capacity (no recorded capacity -> no re-rank; advisory == replacement):
- `deli`, `deli-forecast`, `deli-varmax`, `deli-flat2`, `inspect-nodata`

## Sub-sprint breakdown
- 0. **Green baseline FIRST** (Sprint-32 state): all plain-python3 CR demos (incl. `run_recorded_surface_demo.py`,
   the Sprint-31-state forecast demos, `run_cockpit_s7l/q7q8`, `run_adjudication_engine_demo`, and `run_capacity_rerank_demo.py`)
   + all 5 CR conformances (Sprint-0 venv) + `build_all` + `conformance_all` + S5 reference demo + conformance +
   agent demo + conformance.
- 1. Record invariants BEFORE: engine `a60f8f7…`, `capacity_rerank.py` `f7c6a185…`, schema hash, 49 `$defs`,
   SPEC v0.22, reused-org default bytes (fixture dir hashes).
- 2. **Build** `run_two_path_demo.py` (write `work/1-plan.md` first): the `two_path_surface` + the four
   assertion groups + report under `artifacts/adjudication/reports/two-path.md`.
- 3. **Run** `run_two_path_demo.py` -> `RESULT: ALL PASS`.
- 4. **Non-regression + invariants AFTER**: re-run the green baseline; re-hash engine + `capacity_rerank.py`
   (byte-identical), schema, 49 `$defs`; confirm reused-org fixture bytes unchanged.
- 5. **Honest docs**: additive §17 `docs/ENGINE-FORECAST-CAPACITY.md`, §15 `docs/ENGINE-S7L-COCKPIT.md`,
   `instances/README.md` Sprint-33 entry, `STRESS-TEST-SCENARIOS.md` "Update after Sprint 33",
   `sprints/sprint-33/summary.md` + `notes/findings.md`, update the `relational-os` skill note,
   write `sprints/sprint-34/PROMPT.md`.

## Definition of Done (all real, exit 0)
- Green baseline (Sprint-32 state) FIRST; `run_two_path_demo.py` ALL PASS (composition/non-interference +
  floor-integrity + exhaustive-disjoint + determinism-vs-history); full non-regression green AFTER.
- `adjudication_engine.py` sha256 `a60f8f7…` UNCHANGED + `capacity_rerank.py` sha256 `f7c6a185…` UNCHANGED
  (record both); schema `34264934…`; 49 `$defs`; SPEC v0.22; reused-org bytes intact; no new noun.