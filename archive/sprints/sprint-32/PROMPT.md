# SPRINT 32 — PROMPT (the honest frontier Sprint 31 just closed the INVENTORY on: the whole recorded-
# data §7L decision surface is provably reason-not-choice across 11 orgs, and the ONE remaining
# out-of-scope step is now NAMED EXACTLY — a capacity-constrained OPTIMIZATION that RE-RANKS the Q8
# recommendation for the machine. Sprint 30/31 stated such an optimization is a deliberate
# "re-rank for the machine" POLICY / user decision, NOT a label, that stays OUT of scope UNLESS THIS
# prompt author explicitly asks for it. THIS prompt is that ask — so Sprint 32 builds it, additively,
# with the frozen `rank` untouched and the reason-not-choice inventory preserved.)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 20-31 built a configurable adjudication engine (`instances/contested_reality/
adjudication_engine.py`) that renders the full §7L Q1-Q10 morning cockpit data-only; Sprints 27-30
added the recorded `capacity_constraint` marker (org-level at-capacity/deficit `_capacity_reason`,
then per-option `capacity_infeasible`/`capacity_risk` from RECORDED `capacity_requirements` via
`_per_option_capacity_flags`, then the SHARPEST boundary — Sprint 30's org `deli-recommend-infcap`
where the machine-eligible best / Q8 recommendation ITSELF is `capacity_infeasible` yet the Q8
recommendation provably STAYS the frozen `rank` output); Sprint 31 (`run_recorded_surface_demo.py`,
NO engine change) positively inventoried the WHOLE recorded-data decision surface as reason-not-choice
across 11 orgs (present_recorded / derived_reasons / derivable_universe / not_derivable) and named the
ONLY remaining out-of-scope step: **a capacity-constrained OPTIMIZATION that RE-RANKS the Q8
recommendation for the machine** — a deliberate "re-rank for the machine" POLICY / user decision, whose
seam is recorded per-option `capacity_requirements` (already present) + a deterministic
next-best-non-infeasible rule by the frozen `rank` utility (the only missing piece), and which CHANGES
the Q8 recommendation. **That is exactly what Sprint 32 builds, because this prompt explicitly asks
for it.**

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7K.1 (Policy,
  Trade-off, Organizational Learning, Forecast), §7L (the ten morning questions), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  ~$0, additive, never bump SPEC for a capability-only change — BUT this sprint DOES add a capability,
  the deliberate re-rank optimization; if a genuine normative gap surfaces for labeling it distinctly,
  log it and argue it, do not auto-bump).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — `rank` (frozen, DO NOT TOUCH),
    `machine_eligible_best`, `reconcile`, `run_scenario`, `cockpit_q7q8`, `cockpit_s7l` (incl. the
    Q7/Q8 `capacity_constraint` block + `_per_option_capacity_flags` + `_capacity_reason` +
    `_forecast_closure`), `record_capacity` + `record_capacity_requirements` (the replayable recorders),
    `render_cockpit_s7l`, `render_tradeoff`, `forecast_metric`.
  - `run_recorded_surface_demo.py` (Sprint 31 — the inventory the new optimization must NOT break),
    `run_forecast_label_vs_choice_demo.py` (Sprint 30 — the sharpest label-vs-choice proof),
    `run_forecast_per_option_capacity_demo.py` (Sprint 29), `run_forecast_horizon4_demo.py` (Sprint 28),
    `adjudication_configs.py` (DELI + INSPECT + COVE + RULE_LIBRARY).
  - `sprints/sprint-31/{summary.md,notes/findings.md,plan.md}` — the exact seam text, the 11-org set, and
    the byte-identity + reason-not-choice guarantees that must survive.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16);
  additive only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get
  one-arg, `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2 temporal-
  suffix keys on additive fields, strict C5 tables, `eng.reconcile(sub, cfg)` ARG ORDER, the Sprint-0
  venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance, runner
  CWD-sensitivity, `[0]`-indexed `parents`, json round-trip restores `floor_gated` sets).

## What Sprint 32 IS and IS NOT
- **IS:** a deliberate, additively-built, deterministic **capacity-constrained RE-RANK of the §7L Q8
  recommendation for the machine**, using the named seam — recorded per-option `capacity_requirements`
  + a deterministic next-best-non-infeasible rule by the FROZEN `rank` utility. It respects the §6
  floor, never invents a requirement, never touches frozen functions, and preserves EVERY byte of the
  Sprint-31 reason-not-choice inventory (the marker stays a REASON; the re-rank is the NEW explicit
  step on top). It says plainly, per re-ranked org: "the recorded capacity says the machine's prior
  best can't run under capacity, so the machine, BY AUTHORIZED POLICY, picks the highest-utility option
  that is not `capacity_infeasible`".
- **IS NOT:** a change to the frozen `rank`; a removal/§6-overrule of the floor-gated set; inventing a
  requirement the org did not record; a probabilistic/stochastic forecast; a new URI/schema/`$defs`
  edit; a Trust (S5) change; breaking the Sprint-31 inventory proof or the byte-identity of reused orgs
  on their DEFAULT (non-re-ranked) path.

## The target (what "done" looks like)
1. **A new runner** `run_capacity_rerank_demo.py` (reuse `r31.build_orgs()`'s 11 orgs and the Sprint-29/30
   builders) that, for a chosen set of orgs that RECORD per-option requirements making the machine best
   `capacity_infeasible` (at minimum `deli-recommend-infcap`; add INSPECT/COVE variants), computes the
   re-ranked recommendation: from the frozen `rank` utility ordering, the highest-utility option NOT
   labeled `capacity_infeasible`; unreachable if all capacity-consuming options are infeasible (then
   fall back to the do-nothing/UNRESOLVED baseline and SAY so). Emit a structured
   `capacity_rerank` block on Q8 (additive), with the `why` naming: the prior machine best, why it is
   infeasible from recorded numbers, the chosen next-best-not-infeasible, and that this is a POLICY /
   "re-rank for the machine" step. Assert: the re-rank is deterministic, respects the floor-gated set
   (a floor-gated option is never auto-picked), the re-ranked Q8 == the highest non-infeasible
   non-gated utility option, and on orgs where the prior best is NOT infeasible the Q8 recommendation
   is UNCHANGED (= `cockpit_q7q8`, byte-identical).
2. **The re-rank is generic + additive + engine-additive-if-needed:** prefer a pure runner + recorded
   data as Sprint 29/30/31 did; touch `adjudication_engine.py` ONLY additively if a genuine, small need
   surfaces (e.g. a helper), keeping frozen functions byte-identical.
3. **Non-regression + inventory preserved:** the Sprint-31 runner still ALL PASS (reason-not-choice
   tally intact; the re-rank is an EXPLICIT separate step, not a silent change); the reused orgs keep
   every pre-existing byte on their default path; full non-regression green; 49 `$defs`, SPEC v0.22,
   `ros/` + schema + sector configs untouched.
4. **Honest docs:** additive section in `docs/ENGINE-FORECAST-CAPACITY.md` (a §16) + `docs/ENGINE-S7L-COCKPIT.md`
   (a §14) + `instances/README.md` + a stress-test "Update after Sprint 32" note — the re-rank is now a
   deliberate, recorded-data capacity-constrained optimization that CHANGES the Q8 recommendation under
   explicit policy; the reason-not-choice inventory stands for the default advisory path; extend the §16
   verdict: is the frontier (a re-ranked recommendation under recorded capacity) now derivable, and what
   is still not derivable?
5. **Real output:** new runner ALL PASS; full non-regression green; no new noun; frozen 49 `$defs`;
   SPEC v0.22; `adjudication_engine.py` byte-identical if untouched.

## Mandatory rules
- **Write-first:** `sprints/sprint-32/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive**: keep frozen functions and the 49 `$defs`/URI cap/SPEC v0.22 untouched; re-verify `ros/`,
  schema hash (`7fc38c8c…`), sector instances, and the Sprint-31 reuse bytes.
- **Single-threaded** per PROTOCOL — no subagents. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-31 state): `run_recorded_surface_demo.py` + `run_forecast_label_vs_choice_demo.py`
  + `run_forecast_per_option_capacity_demo.py` + `run_forecast_horizon4_demo.py` + `run_forecast_horizon3_demo.py`
  + `run_forecast_horizon2_demo.py` + `run_forecast_horizon_demo.py` + `run_forecast_variance_all_demo.py`
  + `run_forecast_variance_demo.py` + `run_forecast_direction_demo.py` + `run_forecast_action_demo.py`
  + `run_forecast_capacity_demo.py` + `run_cockpit_s7l_demo.py` + `run_cockpit_q7q8_demo.py` +
  `run_adjudication_engine_demo.py` (plain python3) + the 5 CR conformances (Sprint-0 venv) +
  `build_all.py` + `conformance_all.py` + S5 reference + conformance + agent demo + conformance.
- New `run_capacity_rerank_demo.py` ALL PASS (the re-rank + the not-infeasible-unchanged byte-identity +
  floor-respect + determinism assertions).
- Full non-regression green after the new runner; SPEC v0.22; 49 `$defs`; `ros/` + schema clean;
  schema hash `7fc38c8c…`.

## Documentation (roll-forward)
- Additive note in `docs/ENGINE-FORECAST-CAPACITY.md` + `docs/ENGINE-S7L-COCKPIT.md`; a Sprint-32 entry in
  `instances/README.md`; an "Update after Sprint 32" note in
  `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; reference the new build in
  `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-32/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize, per re-ranked org, which recorded descriptors made the machine's
prior best `capacity_infeasible`, the re-ranked recommendation via the deterministic next-best-not-
infeasible rule by the frozen `rank` utility, that the §6 floor is respected (no floor-gated option is
auto-picked), that orgs whose best is NOT infeasible keep the Q8 recommendation UNCHANGED (= `cockpit_q7q8`,
byte-identical), that this is a deliberate POLICY "re-rank for the machine" step distinct from the
reason-not-choice advisory label (which still stands on the default path — the Sprint-31 inventory is
intact), the byte-identical default (the reused orgs keep every pre-existing byte on their default path;
no new noun; frozen 49 `$defs`; if unchanged, `adjudication_engine.py` byte-identical), the honest §16
verdict on whether the ONE remaining frontier (a capacity-constrained, re-ranked Q8 recommendation under
recorded capacity) is now derivable WHILE the deterministic advisory label-vs-choice boundary still holds —
and what is STILL not derivable (probabilistic/stochastic forecast; a per-option requirement not
unit-coupled to the recorded capacity / an option with no recorded requirement — the engine never invents
one) — and the verified build + conformance commands. Write the **next** sprint's self-contained prompt
at `sprints/sprint-33/PROMPT.md`.

NOTE: after Sprint 32 the deterministic advisory stance can still label the recommended option
`capacity_infeasible` from recorded data (a REASON, never a CHOICE on the advisory path), AND — by this
explicit prompt authorization — a separate, deliberate "re-rank for the machine" OPTIMIZATION can compute
a capacity-constrained replacement from recorded data under POLICY. Keep the two provably distinct: the
advisory path never re-ranks (Sprint-31 inventory intact); the re-rank path is the authorized capability
this prompt builds. Be honest about which path changed the recommendation and why.