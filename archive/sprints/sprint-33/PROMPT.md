# SPRINT 33 — PROMPT (the reference build now has TWO distinct, deliberate decision PATHWAYS — the
# reason-not-choice ADVISORY (Sprint 31 inventory) and the POLICY-authorized capacity-constrained RE-RANK
# (Sprint 32) — this sprint is a POSITIVE CONSOLIDATION: prove the two compose without one silently
# shadowing the other.)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here; read
before acting; never fabricate; **every documented command MUST be run and its real output captured.**
Sprints 20-32 built a configurable adjudication engine (`instances/contested_reality/adjudication_engine.py`)
rendering the full §7L Q1-Q10 morning cockpit data-only, added the recorded `capacity_constraint` marker
(Sprints 27-30: org at-capacity/deficit `_capacity_reason`, then per-option `capacity_infeasible`/`capacity_risk`
from RECORDED `capacity_requirements` via `_per_option_capacity_flags`), positive-inventoried the WHOLE
recorded-data decision surface as reason-not-choice across 11 orgs (Sprint 31: `run_recorded_surface_demo.py`,
NO engine change), and — Sprint 32, by explicit prompt authorization — built the ONE named out-of-scope step:
a **capacity-constrained RE-RANK of the §7L Q8 recommendation for the machine** (`capacity_rerank.py` +
`run_capacity_rerank_demo.py`, NO engine change): a PURE module that, when the machine-eligible best is
`capacity_infeasible` from recorded per-option `capacity_requirements`, picks the highest-utility frozen-`rank`
option that is neither floor-gated nor `capacity_infeasible`, reported as an additive `capacity_rerank` block,
NEVER overwriting the engine's advisory Q8. **Sprint 33 consolidates the now-two-path decision surface.**

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7K.1 (Policy, Trade-off,
  Organizational Learning, Forecast), §7L (the ten morning questions), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output, ~$0,
  additive, never bump SPEC for a capability-only change; consolidation sprints stay at v0.22).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — `rank` (frozen, DO NOT TOUCH),
    `machine_eligible_best`, `reconcile`, `run_scenario`, `cockpit_q7q8`, `cockpit_s7l` (the Q7/Q8
    `capacity_constraint` block + `_per_option_capacity_flags` + `_capacity_reason` + `_forecast_closure`),
    `record_capacity` + `record_capacity_requirements`, `render_cockpit_s7l`, `forecast_metric`.
  - `instances/contested_reality/capacity_rerank.py` — Sprint 32's NEW pure module: `capacity_rerank(cfg, sub,
    *, library=None)` returns the additive `capacity_rerank` block (`needed`, `prior_machine_best`,
    `prior_best_capacity_flag`, `recorded_descriptors`, `available_capacity`, `per_option_requirements`,
    `replacement`, `replacement_is_baseline`, `all_capacity_consuming_infeasible`, `floor_respected`,
    `policy`, `why`) or `needed=False` for unchanged orgs.
  - `run_capacity_rerank_demo.py` (Sprint 32 — the re-rank proof; 13 orgs = 11 Sprint-31 + NEW
    `cove-recommend-infcap` + `deli-all-infeasible`) and `run_recorded_surface_demo.py` (Sprint 31 — the
    reason-not-choice inventory the re-rank must NOT break).
  - `adjudication_configs.py` (DELI + INSPECT + COVE + RULE_LIBRARY).
  - `sprints/sprint-32/{summary.md,notes/findings.md,plan.md}` — the re-rank build, the §16 residual, and the
    "consolidation vs capability" cadence note.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16); additive
  only; single-threaded; plan-before-build; real tool output; ~$0; footguns (`cockpit_q7q8` does NOT carry
  the `capacity_constraint` block — read it from `cockpit_s7l`; `record_metric_series` REQUIRES `name`+`formula`
  in `fields`; `Graph.get` one-arg; `evidence`/`rules_applied` as ARRAYS; `{**graph.get(u), ...}` merge-not-
  replace; C2 temporal-suffix keys; strict C5 tables; `eng.reconcile(sub, cfg)` ARG ORDER; the Sprint-0 venv
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance; runner CWD-sensitivity).

## What Sprint 33 IS and IS NOT
- **IS:** a positive, engine-untouched CONSOLIDATION that makes the **two-path decision surface** — the
  reason-not-choice ADVISORY (Q8 recommendation == frozen `rank`, never re-ranks) AND the POLICY-authorized
  capacity-constrained RE-RANK — compose cleanly and are inventoried/STRESSED as ONE coherent decision
  framework. It proves the two paths never silently interfere (the re-rank never shadows the advisory on the
  default path; the advisory never re-ranks; a re-ranked `replacement` never becomes the machine-eligible
  best of the default path). A survey/audit runner + recorded data ONLY; the engine AND `capacity_rerank.py`
  are provably byte-identical.
- **IS NOT:** a new capability; a change to `rank`/`capacity_rerank`/the engine; a probabilistic/stochastic
  forecast; a new URI/schema/`$defs` edit; a Trust (S5) change; breaking the Sprint-31/32 proofs or any
  reused org's default bytes.

## The target (what "done" looks like)
1. **A new runner** `run_two_path_demo.py` (reuse `run_capacity_rerank_demo`'s 13-org set and
   `r31.build_orgs()`) that, per org, emits a structured **`two_path_surface`** = {label,
   advisory={q7_machine_eligible_best, q8_recommendation, floor_gated, capacity_constraint(options_flagged)},
   rerank={needed, prior, replacement, replacement_is_baseline}, and a PATH label (ADVISORY / RE-RANK /
   no-capacity)} and asserts:
   - **(composition / non-interference)** for every org where the re-rank fires (needed=True), the advisory
     Q8 recommendation STILL == `cockpit_q7q8` (the re-rank did not shadow it) AND the re-ranked
     `replacement` ≠ the advisory Q8 recommendation (they are provably different options) AND `replacement`
     is not the advisory `machine_eligible_best`; for every org where needed=False, `replacement` == the
     advisory Q8 (they agree — one path, unchanged);
   - **(floor integrity)** no advisory or re-rank selection is ever a floor-gated option (asserted against
     `rank`);
   - **(determinism vs history)** re-running gives identical `two_path_surface`; and the Sprint-31
     reason-not-choice tally + the Sprint-32 re-rank results are both reproducible from the SAME recorded
     data in this run (the consolidation is a view over the same data, not a rewrite).
   - **The two-path taxonomy is exhaustive & disjoint** across all orgs: every org is exactly one of
     {ADVISORY-no-capacity (no capacity recorded), ADVISORY-best-runnable (capacity recorded, best NOT
     infeasible), RE-RANK (best infeasible -> replacement)} — no org is two classes.
2. **No engine / no `capacity_rerank.py` change:** both files byte-identical (hash `a60f8f7…` engine +
   `capacity_rerank` sha256 recorded before and after); non-regression green; PROFESSION of the reused orgs'
   default bytes intact.
3. **Honest docs:** additive §17 in `docs/ENGINE-FORECAST-CAPACITY.md`, §15 in `docs/ENGINE-S7L-COCKPIT.md`,
   `instances/README.md` Sprint-33 entry, a stress-test "Update after Sprint 33" note, and an honest §16
   extending the verdict: are the two paths now a single coherent recorded-data decision framework, and what
   is STILL not derivable?
4. **Real output:** new runner ALL PASS; full non-regression green; no new noun; frozen 49 `$defs`; SPEC
   v0.22; `adjudication_engine.py` + `capacity_rerank.py` byte-identical.

## Mandatory rules
- **Write-first:** `sprints/sprint-33/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive/consolidation**: keep frozen functions + `capacity_rerank.py` + the 49 `$defs`/URI cap/SPEC v0.22
  untouched; re-verify `ros/`, schema hash `7fc38c8c…`, sector instances, the Sprint-31/32 reuse bytes, and
  the engine + `capacity_rerank.py` hashes.
- **Single-threaded** per PROTOCOL — no subagents. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-32 state): `run_capacity_rerank_demo.py` + `run_recorded_surface_demo.py` +
  the Sprint-31-state demos (`run_forecast_label_vs_choice_demo.py`, `run_forecast_per_option_capacity_demo.py`,
  `run_forecast_horizon4_demo.py`, `run_forecast_horizon3_demo.py`, `run_forecast_horizon2_demo.py`,
  `run_forecast_horizon_demo.py`, `run_forecast_variance_all_demo.py`, `run_forecast_variance_demo.py`,
  `run_forecast_direction_demo.py`, `run_forecast_action_demo.py`, `run_forecast_capacity_demo.py`,
  `run_cockpit_s7l_demo.py`, `run_cockpit_q7q8_demo.py`, `run_adjudication_engine_demo.py` — plain python3)
  + the 5 CR conformances (Sprint-0 venv) + `build_all.py` + `conformance_all.py` + S5 reference demo +
  conformance + agent demo + conformance.
- New `run_two_path_demo.py` ALL PASS (composition/non-interference + floor-integrity + exhaustive-disjoint
  + determinism-vs-history assertions).
- Full non-regression green after the new runner; SPEC v0.22; 49 `$defs`; `ros/` + schema clean; schema hash
  `7fc38c8c…`; engine `a60f8f7…` AND `capacity_rerank.py` sha256 byte-identical (record both).

## Documentation (roll-forward)
- Additive note in `docs/ENGINE-FORECAST-CAPACITY.md` + `docs/ENGINE-S7L-COCKPIT.md`; a Sprint-33 entry in
  `instances/README.md`; an "Update after Sprint 33" note in
  `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; summarize in
  `sprints/sprint-33/summary.md` + `notes/findings.md`. Do NOT bump SPEC (v0.22) unless a genuine normative
  gap surfaces. The `relational-os` skill's Sprint-33 note should be updated.
- Write `sprints/sprint-33/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize, per org, its PATH class (ADVISORY-no-capacity / ADVISORY-best-runnable
/ RE-RANK), the composition proof (the re-rank never shadows the advisory — re-ranked `replacement` is a
different option from the advisory Q8 recommendation where the machine best is infeasible, and identical to
it where needed=False), the floor integrity, the exhaustive-disjoint taxonomy, that the two paths compose
into ONE coherent recorded-data decision framework without either silently overriding the other (the
Sprint-31 reason-not-choice inventory AND the Sprint-32 re-rank both reproduced from the same recorded data),
the byte-identical default (engine `a60f8f7…` + `capacity_rerank.py` sha256 unchanged; reused orgs keep every
byte; no new noun; frozen 49 `$defs`), the honest §16 verdict on whether the two-path decision surface is
now a single coherent framework WHILE the deterministic advisory label-vs-choice boundary still holds — and
what is STILL not derivable (a probabilistic/stochastic forecast; a per-option requirement NOT unit-coupled
to the recorded capacity value / an option with no recorded requirement — the machine never invents one; and
any choice the §6 human must make that recorded data cannot machine-decide — the re-rank is POLICY-authorized,
not a claim of objective best) — and the verified build + conformance commands. Write the **next** sprint's
self-contained prompt at `sprints/sprint-34/PROMPT.md` (which must reference only absolute paths and the
current SPEC.md).