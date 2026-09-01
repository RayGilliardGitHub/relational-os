# SPRINT 31 — PROMPT (the honest frontier Sprint 30 left open: the marker can now say — AS DATA — that
# the RECOMMENDED option is `capacity_infeasible` from a recorded per-option requirement, yet it still
# never CHOOSES a different option for the machine; a genuinely capacity-constrained OPTIMIZATION that
# RE-RANKS the recommendation is a deliberate "re-rank for the machine" capability that stays OUT of scope
# of the deterministic advisory stance unless THIS prompt author explicitly asks for it — so enumerate /
# inventory the whole recorded-data decision surface and prove what is derivable and what is not)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 26–30 built the configurable adjudication engine
(`instances/contested_reality/adjudication_engine.py`) that renders the full §7L Q1–Q10 morning cockpit
for ANY configured org, data-only; Sprint 27 added the Q7/Q8 `capacity_constraint` marker; Sprint 28
proved it at its LIMIT (at-capacity / deficit); Sprint 29 made the recorded capacity PER-OPTION — a
REPLAYABLE recorder `record_capacity_requirements(sub, authority_uri, requirements, signer)` appends an
additive `capacity_requirements` map on the SAME `authority://` object as the recorded `capacity`, and
the Q7/Q8 `capacity_constraint` block (via the additive `_per_option_capacity_flags` helper) labels a
SPECIFIC option `capacity_infeasible` iff its RECORDED requirement > available (= recorded capacity
VALUE − recorded load, same unit), else `capacity_risk`, baseline never flagged; **Sprint 30 proved the
SHARPEST label-vs-choice boundary** — a NEW org `deli-recommend-infcap`
(`run_forecast_label_vs_choice_demo.py`, NO engine change, `adjudication_engine.py` hash `a60f8f7…`
identical) RECORDS a per-option requirement that makes the frozen machine-eligible best / Q8
recommendation ITSELF (`partial-settlement`) `capacity_infeasible` (recorded 499.0 > available 498.7)
yet the cockpit provably STILL recommends `partial-settlement` — exactly `cockpit_q7q8`, no re-rank, no
§6 overrule — the marker is a REASON, never a CHOICE.
**Sprint 30's own finding (`sprints/sprint-30/notes/findings.md`, "Open issues / next work") discloses
the honest frontier: the marker labels — at its sharpest it labels the RECOMMENDED option — but it still
never CHOOSES a different option for the machine; a capacity-constrained OPTIMIZATION that RE-RANKS the
recommendation would be a deliberate "re-rank for the machine" capability (the missing piece is a
deterministic next-best-non-infeasible rule by the frozen `rank` utility), which stays OUT of scope of
the deterministic advisory stance unless the prompt author asks for it.** Everything the engine ever
labels is still a REASON derived from recorded numbers; no recorded data ever RECOMMENDS or RE-RANKS.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7K.1 (Policy, Trade-off,
  Organizational Learning, Forecast, Decision→Expected→Variance→WHY), §7L (the ten morning questions),
  §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output, ~$0,
  additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — esp. `record_capacity` +
    `record_capacity_requirements` (the replayable recorders), `_per_option_capacity_flags` +
    `_capacity_reason` (the shared headroom/at-capacity/deficit + per-option infeasibility rules),
    `_forecast_closure` (the band / `band_horizon` / `do_nothing` expected-impact), the Q7/Q8
    `capacity_constraint` block in `cockpit_s7l` (Sprint 27/28/29), the Q9 `capacity_planning_attention`
    (Sprint 26/27), and the frozen `rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`/
    `reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/`forecast_metric`.
  - `run_forecast_label_vs_choice_demo.py` (Sprint 30 — the runner that proved the RECOMMENDED option is
    `capacity_infeasible` + the marker-is-a-reason-not-a-choice equality), `run_forecast_per_option_capacity_demo.py`
    (Sprint 29), `run_forecast_horizon4_demo.py` (Sprint 28), `run_forecast_horizon3_demo.py` (Sprint 27),
    `run_forecast_horizon2_demo.py` (+ its `r26.build_orgs`), `run_forecast_horizon_demo.py`,
    `run_forecast_variance_demo.py`, `run_forecast_capacity_demo.py`, `run_forecast_direction_demo.py`,
    `run_forecast_action_demo.py`, `run_cockpit_s7l_demo.py`, `run_cockpit_q7q8_demo.py` — reuse their
    builders/constants (`relabel_to`, `run_one`, `record_series`, `record_capacity`,
    `record_capacity_requirements`, the VMC/VM/CO points, `rfh.*`, `rfv.*`, `r26.*`, `r29.*`, `r30.*`).
  - `adjudication_configs.py` (DELI + INSPECT + COVE + the rule library) + `docs/ENGINE-FORECAST-CAPACITY.md`
    (§12–§14) + `docs/ENGINE-S7L-COCKPIT.md` (§10–§12) + `sprints/sprint-30/{summary.md,notes/findings.md}`
    + `sprints/sprint-29/notes/findings.md`.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16);
  additive only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get one-arg,
  `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2 RFC3339 temporal-
  suffix keys — never name an additive field ending in `at|time|deadline|expires|expiry|effective|due|
  since`; strict C5 tables, `eng.reconcile(sub, cfg)` ARG ORDER, the Sprint-0 venv
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance, runner CWD-
  sensitivity, `[0]`-indexed `parents`, json round-trip restores `floor_gated` sets, float-vs-int
  formatting, and that the band is a RECORDED-DATA spread not a confidence interval — plus the Sprint-30
  lesson that a RECORDED per-option requirement can make the RECOMMENDED option `capacity_infeasible`
  while the Q8 recommendation provably stays the frozen `rank` output).

## What Sprint 31 IS and IS NOT
- **IS:** make the label-vs-choice boundary the ORGANIZING truth of a full INVENTORY of the recorded-data
  decision surface — because the honest frontier after Sprint 30 is not "add a capability" but "prove the
  whole recorded surface is now inventoried and every derivation is labeled a REASON, never a CHOICE."
  Concretely, a Sprint-31 survey/boundary runner that, for a set of orgs (the eight from Sprint 30 or a
  deliberately broader set incl. INSPECT + COVE + a no-data org), emits a per-org **decision-surface
  inventory** (`recorded_surface`): which recorded descriptors are present (recorded `metric://` series
  with point-`variance`/`band_variance`, a recorded authority `capacity`, recorded per-option
  `capacity_requirements`, the recorded `floor_gated`/weights/rule), which derived REASON each produced
  (Q3 forecast attention + why, Q6 projection + band, Q7/Q8 `capacity_constraint` reason + per-option
  flags, Q9 capacity-planning label, Q8 do-nothing expected-impact), and — crucially — what is DERIVABLE
  vs NOT derivable from that org's recorded data alone, each mapped to a runnable assertion. Prove with
  real orgs that: (a) every label on the surface derives from a recorded descriptor and is a REASON; (b)
  no recorded data ever re-ranks the Q8 recommendation (Q8 stays `cockpit_q7q8` for every org — including
  the Sprint-30 org where the recommended option is `capacity_infeasible`); (c) the ONLY un-derivable,
  out-of-scope frontier left is the deliberate "re-rank for the machine" OPTIMIZATION, which is named with
  its exact seam (a deterministic next-best-non-infeasible rule by the frozen `rank` utility) and left
  out. This is a positive consolidation: after six sprints the whole §7L decision surface is recorded-data
  + reason, and Sprint 31 proves that in ONE comprehensive, auditable run.
- **IS NOT:** implementing the OPTIMIZATION (a capacity-constrained re-rank that changes the Q8
  recommendation is explicitly a policy / user decision, NOT in scope of the deterministic advisory
  stance — do not build it); a re-implementation of `run_scenario`/`reconcile`/`cockpit_q7q8`/`rank`/
  `machine_eligible_best`/`render_tradeoff`/`_derive`/`_capacity_reason`/`_per_option_capacity_flags`;
  changing the frozen `rank`; making the MACHINE choose a different option; probabilistic/stochastic
  forecast; a new service / URI noun / schema / `$defs` edit; Trust (S5) change; fabricated descriptors.
  If the prompt author later wants the OPTIMIZATION built, THAT is a deliberate "re-rank for the machine"
  capability change with its own authorization — not something this inventory quietly slips in.

## The target (what "done" looks like)
1. **A decision-surface inventory runner** `run_recorded_surface_demo.py` (new, exit 0 = ALL PASS): for
   a set of orgs (reuse `r30.build_orgs()`'s eight + INSPECT + COVE + one no-data org), emit a structured
   `recorded_surface` dict per org: {label, present_recorded={metric_series/point_variance/band_variance/
   capacity/capacity_requirements/floor_gated/weights/reconcile_rule}, derived_reasons={Q3_forecast/
   Q6_projection/Q7Q8_capacity_constraint/Q9_capacity/Q8_do_nothing_impact}, derivable_universe=
   [sorted list of every derived reason], not_derivable=[the named optimization seam + any descriptor the
   org does not record]} and assert, per org, that every derived label traces to a recorded descriptor.
2. **The reason-not-choice proof, totalled.** In the same runner, for EACH org assert Q7 `options` +
   `machine_eligible_best` + Q8 `recommendation` + `floor_gated` EXACTLY equal `cockpit_q7q8` — and print
   a tally (e.g. "8/8 orgs: the marker never re-ranks; includes the org where the RECOMMENDED option is
   `capacity_infeasible`." Report the Sprint-30 org explicitly in that tally.
3. **The frontier, named exactly.** In the report + §16: state plainly that the ONLY remaining
   out-of-scope step is a capacity-constrained OPTIMIZATION that RE-RANKS the recommendation for the
   machine; it would need (recorded per-option requirements — already present — + a deterministic
   next-best-non-infeasible rule by the frozen `rank` utility), it CHANGES the Q8 recommendation, and it
   is a policy / user decision, NOT a label, deliberately NOT built here. No recorded data will ever
   re-rank.
4. **Byte-identity + Sprint-30 regression.** Reuse the eight Sprint-30 orgs byte-identical (the new
   runner's `capacity_constraint` blocks / `cockpit_q7q8` equalities are a strict superset; nothing
   changes on any reused org). Add INSPECT + COVE + a no-data org as NEW orgs only if the inventory
   genuinely needs them (name them, do not overwrite existing fixture dirs). Determinism (dict + render).
   Emit fixtures + report.
5. **Honest docs.** Additive note in `docs/ENGINE-FORECAST-CAPACITY.md` (a §15) + `docs/ENGINE-S7L-COCKPIT.md`
   (a §13): the whole recorded-data decision surface is now inventoried as reason-not-choice; no recorded
   data ever re-ranks; the optimization seam is named. Extend the §16 verdict — has Sprint 31 proved the
   surface is fully recorded-data + reason? what is still not derivable?
6. **Real output:** new runner ALL PASS; full non-regression green; no new noun, 49 `$defs`, SPEC v0.22;
   `adjudication_engine.py` may be touched ONLY additively `if a genuine defect/need surfaces` — prefer a
   pure runner + recorded data, as Sprint 30 did (NO engine change).

## Mandatory rules
- **Write-first:** `sprints/sprint-31/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** prefer a new runner + recorded data, as Sprint 30 did (engine hash `a60f8f7…` stayed
  identical). If the ONLY engine file you touch is `instances/contested_reality/adjudication_engine.py`,
  touch it only additively for a genuine need. Keep frozen functions untouched; keep 49 `$defs` + URI
  cap + SPEC v0.22. Re-verify `ros/`, the schema hash (`7fc38c8c…`), and the sector instances untouched;
  the reused orgs' output must be a strict SUPER SET of Sprint 30 preserving every pre-existing byte.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-30 state): `run_forecast_label_vs_choice_demo.py` +
  `run_forecast_per_option_capacity_demo.py` + `run_forecast_horizon4_demo.py` +
  `run_forecast_horizon3_demo.py` + `run_forecast_horizon2_demo.py` + `run_forecast_horizon_demo.py` +
  `run_forecast_variance_all_demo.py` + `run_forecast_variance_demo.py` + `run_forecast_direction_demo.py`
  + `run_forecast_action_demo.py` + `run_forecast_capacity_demo.py` + `run_cockpit_s7l_demo.py` +
  `run_cockpit_q7q8_demo.py` + `run_adjudication_engine_demo.py` (plain python3) + the 5 CR conformances
  (Sprint-0 venv) + `build_all.py` + `conformance_all.py` + S5 reference (`sprints/sprint-5/artifacts/`)
  + conformance + agent demo (`instances/agent_demo/`) + conformance.
- New assertions ALL PASS (above). Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema
  clean; schema hash `7fc38c8c…`.

## Documentation (roll-forward)
- Additive note in `docs/ENGINE-FORECAST-CAPACITY.md` + `docs/ENGINE-S7L-COCKPIT.md`; append a Sprint-31
  entry to `instances/README.md`; append an "Update after Sprint 31" note to
  `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; reference the new build in
  `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-31/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize, per org, the decision-surface inventory assertion THIS sprint made
(which recorded descriptors are present, which derived REASON each produced, and the derivable-vs-not-
derivable boundary), the reason-not-choice tally (how many orgs proved Q8 == `cockpit_q7q8`, including
the Sprint-30 org where the RECOMMENDED option is `capacity_infeasible`), the byte-identical default
(the reused Sprint-30 orgs keep every pre-existing byte), that this is generic + additive (recorded
`metric://` series + recorded point-`variance` + the recorded `band_variance` source + a recorded
authority `capacity` + a recorded per-option `capacity_required` descriptor; no new noun, frozen 49
`$defs`, and — if unchanged — `adjudication_engine.py` byte-identical), the honest §16 verdict on whether
the whole recorded-data decision surface is now inventoried as reason-not-choice WHILE the Q8
recommendation provably stays the frozen `rank` output — and what is still NOT derivable (the ONE
remaining out-of-scope step: a capacity-constrained OPTIMIZATION that RE-RANKS the recommendation for the
machine, a deliberate "re-rank for the machine" policy / user decision whose seam is recorded per-option
requirements + a deterministic next-best-non-infeasible rule by the frozen `rank` utility; plus a
per-option requirement NOT unit-coupled to the recorded capacity / an option with no recorded
requirement) — and the verified build + conformance commands. Write the **next** sprint's self-contained
prompt at `sprints/sprint-32/PROMPT.md`.

NOTE: after Sprint 31 the frontier is the boundary itself — the deterministic advisory stance can label
the recommended option `capacity_infeasible` from recorded data, it can inventory the entire recorded
decision surface as reason-not-choice, but it cannot and must not choose the replacement for the §6
human. A genuinely capacity-constrained OPTIMIZATION that MOVES the recommendation is a POLICY / user
request, not a label, and stays firmly out of scope unless the prompt author explicitly asks to build it
(a deliberate "re-rank for the machine" capability change). Be honest about that in the §16 verdict.