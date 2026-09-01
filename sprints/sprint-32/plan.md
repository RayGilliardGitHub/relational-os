# SPRINT 32 — plan: the capacity-constrained RE-RANK of the §7L Q8 recommendation for the machine

## Objective
Build, additively and deterministically, the ONE step Sprint 30/31 named and deliberately left
out of scope: a **capacity-constrained OPTIMIZATION that RE-RANKS the Q8 recommendation** for the
machine, BY EXPLICIT PROMPT AUTHORIZATION. It uses exactly the named seam — recorded per-option
`capacity_requirements` (already present) + a deterministic **next-best-non-infeasible rule by the
frozen `rank` utility**. The re-rank CHANGES the Q8 recommendation under an explicit, honest
POLICY label. It is a distinct step: the default advisory path NEVER re-ranks (the Sprint-31
reason-not-choice inventory stays intact).

## Non-negotiables (from PROMPT + skill)
- **Engine byte-identical**: `adjudication_engine.py` sha256 `a60f8f7…` MUST stay unchanged. The
  re-rank is a NEW pure module + a new runner + recorded data (Sprint 29/30/31 proof shape).
- Frozen ontology / URI cap / 49 `$defs`; SPEC stays v0.22 (no normative gap — the re-rank is a
  deliberate authorized POLICY step, not a schema/norm change). `ros/` + schema + sector `configs.py`
  untouched. No new noun (no new URI scheme).
- Single-threaded (no subagents); plan-before-build; real tool output; ~$0.
- Green baseline captured BEFORE any build; full non-regression green AFTER.

## The re-rank rule (pure, deterministic — by the frozen `rank` utility)
Given an org's `cockpit_s7l` q8 `capacity_constraint` block (recorded capacity data):
1. `prior = c.q7.machine_eligible_best` (the frozen `rank`/`machine_eligible_best` output).
2. If `capacity_constraint.options_flagged[prior] != "capacity_infeasible"` → **NO re-rank needed**
   (prior best is runnable); Q8 recommendation stays the frozen `rank` output, byte-identical to
   `cockpit_q7q8`.
3. Else walk the frozen `rank(cfg)` ordering and pick the **first option that is BOTH not
   `floor_gated` AND not `capacity_infeasible`**. This is the highest-utility non-infeasible
   non-gated option — `machine_eligible_best` with the additional recorded-capacity filter.
4. If every capacity-consuming option is infeasible/gated, fall back to the do-nothing/UNRESOLVED
   baseline and **say so** (`replacement_is_baseline` = True).
5. Emit an additive **`capacity_rerank`** block describing: the prior best, why it is infeasible
   from recorded numbers (available = recorded capacity.value − recorded load; option's recorded
   requirement > available), the chosen replacement, the §6 floor respected flag, and that this is
   an authorized POLICY "re-rank for the machine" step. The advisory q8.recommendation is never
   overwritten; the re-ranked selection lives in the block and the runner reports it plainly.

## Chosen org set (from `r31.build_orgs()` + ONE new COVE org)
RE-RANK FIRES (machine best is `capacity_infeasible`):
- `deli-recommend-infcap` → best `partial-settlement`(req 499.0 > avail 498.7) → replacement
  `conditional-resolution` (0.665, next non-gated non-infeasible).
- `inspect-recorded` → best `rework-partial-credit`(499.0 > 498.7) → replacement
  `conditional-accept-with-guarantee` (0.61).
- `cove-recommend-infcap` (NEW label, Sprint-30 pattern) → best `step-therapy-first`
  (req 30.0 > avail 29.1) → replacement `authorize-generic` (0.74).

UNCHANGED (best NOT infeasible — byte-identical to `cockpit_q7q8`): `cove-recorded` (best
`step-therapy-first` = capacity_risk, runnable), `deli-infcap` / `deli-deficit-inf` (best
`partial-settlement` = capacity_risk), `deli-varmax-cap` (headroom), `deli` / `deli-forecast` /
`deli-varmax` / `deli-flat2` / `inspect-nodata` (no recorded capacity → no re-rank possible).

## Sub-sprint breakdown
- 0. **Green baseline** (Sprint-31 state) — all plain-python3 CR demos + the 5 CR conformances +
  `build_all` + `conformance_all` + S5 reference demo + conformance + agent demo + conformance.
- 1. **Build** `capacity_rerank.py` (new pure module): `capacity_rerank(cfg, sub, *, library=None)`.
- 2. **Build** `run_capacity_rerank_demo.py` (new runner): asserts determinism, floor-respect,
  re-ranked==highest non-infeasible non-gated, unchanged orgs byte-identical, reason-not-choice
  inventory intact (r31 still ALL PASS). Emits fixtures for the new org + report.
- 3. **Non-regression + invariants**: rerun the green baseline after the new files; engine hash
  `a60f8f7…`, schema `7fc38c8c…`, 49 `$defs`, SPEC v0.22, no `://qk/` in new fixtures.
- 4. **Honest docs**: `docs/ENGINE-FORECAST-CAPACITY.md` §16, `docs/ENGINE-S7L-COCKPIT.md` §14,
  `instances/README.md` Sprint-32 entry, `STRESS-TEST-SCENARIOS.md` "Update after Sprint 32",
  `sprints/sprint-32/summary.md` + `notes/findings.md`, `sprints/sprint-33/PROMPT.md`.

## Definition of Done (all real, exit 0)
- `run_capacity_rerank_demo.py` → **RESULT: ALL PASS** with the re-rank cases + unchanged
  byte-identity + floor-respect + determinism assertions.
- `run_recorded_surface_demo.py` still **ALL PASS** (the Sprint-31 inventory is NOT broken by the
  new explicit step).
- Full non-regression green after the new files.
- `adjudication_engine.py` sha256 unchanged (`a60f8f7…`); schema `7fc38c8c…`; 49 `$defs`; SPEC v0.22;
  `ros/` + schema + sector `configs.py` untouched; no new noun.