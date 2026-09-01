# SPRINT 30 — PROMPT (the honest frontier Sprint 29 left open: the marker can now NAME a single option
# `capacity_infeasible` from a recorded per-option requirement, but it still never CHOOSES a different
# option — a genuinely capacity-constrained OPTIMIZATION that re-ranks the recommendation stays out of
# scope of the deterministic advisory stance, and a per-option requirement not unit-coupled to the
# recorded capacity remains non-derivable)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 26–29 built the configurable adjudication engine
(`instances/contested_reality/adjudication_engine.py`) that renders the full §7L Q1–Q10 morning cockpit
for ANY configured org, data-only; Sprint 27 added the Q7/Q8 `capacity_constraint` marker; Sprint 28
proved it at its LIMIT (at-capacity / deficit); **Sprint 29 made the recorded capacity PER-OPTION** — a
new REPLAYABLE recorder `record_capacity_requirements(sub, authority_uri, requirements, signer)`
appends an additive `capacity_requirements` map ({option: nonneg amount}) ON THE SAME `authority://`
object that carries the additive `capacity` {value, unit, load}, and the Q7/Q8 `capacity_constraint`
block (via the additive `_per_option_capacity_flags` helper) now labels a SPECIFIC option
`capacity_infeasible` iff its RECORDED requirement > available (= recorded capacity VALUE − recorded
load, same unit), else `capacity_risk`, baseline never flagged, `reason`/`flag` still from the frozen
org-level `_capacity_reason`. Sprint 29 PROVED this on real orgs (`deli-infcap` at-capacity →
available 498.7, heavy 499.0 → `capacity_infeasible`; `deli-deficit-inf` deficit → available 29.1,
heavy 30.0 → `capacity_infeasible`) while asserting Q7 options + machine-eligible best + Q8
recommendation stay EXACTLY equal to `cockpit_q7q8` even when SOME option is infeasible (the marker is
a LABEL — no re-rank, no removal, no §6 overrule).
**Sprint 29's own finding (`sprints/sprint-29/notes/findings.md`, "Open issues / next work") discloses
the honest frontier: the marker still never CHOOSES a different option for the machine — the §6 human
always does — and a per-option requirement NOT unit-coupled to the capacity (no recorded capacity
VALUE/load, or an option with no recorded requirement) stays non-derivable.** Everything Sprint 29
labels is still a REASON: `available` is derived and the per-option flag is derived, but no recorded
data ever RECOMMENDS or RE-RANKS — the Q8 recommendation is provably the frozen `rank` output under
every capacity story.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7K.1 (Policy,
  Trade-off, Organizational Learning, Forecast, Decision→Expected→Variance→WHY), §7L (the ten morning
  questions), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — esp. `record_capacity_requirements`,
    `_per_option_capacity_flags`, `_capacity_reason` (the shared headroom/at-capacity/deficit rule),
    the Q7/Q8 `capacity_constraint` block in `cockpit_s7l` (Sprint 27/28/29), the Q9
    `capacity_planning_attention` (Sprint 26/27), and the frozen `rank`/`machine_eligible_best`/
    `render_tradeoff`/`cockpit_q7q8`/`reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`.
  - `run_forecast_per_option_capacity_demo.py` (Sprint 29 — the runner that PROVED per-option
    infeasibility + the marker-is-a-label equality), `run_forecast_horizon4_demo.py` (Sprint 28),
    `run_forecast_horizon3_demo.py` (Sprint 27), `run_forecast_horizon2_demo.py` (+ its
    `r26.build_orgs`), `run_forecast_horizon_demo.py`, `run_forecast_variance_demo.py`,
    `run_forecast_capacity_demo.py` — reuse their builders/constants (`relabel_to`, `run_one`,
    `record_series`, `record_capacity`, `record_capacity_requirements`, `_per_option_capacity_flags`,
    the VMC/VM/CO points, `rfh.*`, `rfv.*`, `r26.*`).
  - `adjudication_configs.py` (DELI + INSPECT + COVE + the rule library) + `docs/ENGINE-FORECAST-CAPACITY.md`
    (§12–§13, the marker at headroom/at-capacity/deficit/master per-option) + `docs/ENGINE-S7L-COCKPIT.md`
    (§9–§11) + `sprints/sprint-29/{summary.md,notes/findings.md}` + `sprints/sprint-28/notes/findings.md`.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16);
  additive only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get
  one-arg, `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2
  RFC3339 temporal-suffix keys — never name an additive field ending in
  `at|time|deadline|expires|expiry|effective|due|since`; strict C5 tables, `eng.reconcile(sub, cfg)`
  ARG ORDER, the Sprint-0 venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python`
  for conformance, runner CWD-sensitivity, `[0]`-indexed `parents`, json round-trip restores
  `floor_gated` sets, float-vs-int formatting, the band is a RECORDED-DATA spread not a confidence
  interval — plus Sprint 29's lesson that a RECORDED per-option requirement is the new descriptor and
  the per-option helper must not fire for a no-requirements org (byte-identity)).

## What Sprint 30 IS and IS NOT
- **IS:** be honest that the per-option-capacity frontier is now CLOSED (the marker names an infeasible
  option from recorded data) and that the remaining scope is choice/optimization — a bounded slice that
  STAYS within the deterministic advisory stance. Concretely: (a) demonstrate the marker is a REASON
  never a CHOICE by driving a NEW org story where the recorded per-option requirements CLEARLY show the
  machine-eligible best is itself `capacity_infeasible` and the org STILL recommends it (the §6 human
  must rule) — proving the deterministic advisory stance holds at its sharpest; OR (b) if the prompt
  author wants the next build to be a genuinely capacity-constrained OPTIMIZATION, call it out as the
  SPLIT decision: deterministic advisory (marker never re-ranks) vs choosing-an-option (which would
  CHANGE the Q8 recommendation and is NOT what a label does). The point of Sprint 30 is to EITHER
  prove the sharpest label-vs-choice boundary on a real org, OR to explicitly name the out-of-scope
  optimization frontier and close the sprint as a boundary proof + honest §16.
  THIS PROMPT REQUIRES: (1) read Sprint 29's finding about "still never CHOOSES"; (2) build a NEW org
  (or reuse) where the recorded per-option requirement makes the frozen machine-eligible best
  (partial-settlement) `capacity_infeasible` (e.g. a per-option requirement for partial-settlement >
  available) and assert the cockpit STILL recommends partial-settlement (exactly `cockpit_q7q8`) —
  the marker labels "this recommended option cannot run under recorded capacity" WITHOUT choosing a
  replacement; (3) an explicit NOTE where summary §16 says what a capacity-constrained OPTIMIZATION
  WOULD need (per-option requirements + a deterministic re-rank rule, e.g. next-best-non-infeasible by
  recorded utility) and why it stays out of the advisory stance unless the prompt author asks for it.
- **IS NOT:** a re-implementation of `run_scenario`/`reconcile`/`cockpit_q7q8`/`rank`/
  `machine_eligible_best`/`render_tradeoff`/`_derive`; changing the frozen `rank`; making the MACHINE
  choose a different option (a capacity-constrained OPTIMIZATION that re-ranks the recommendation is
  explicitly OUT of scope of the deterministic advisory stance — the §6 human always rules);
  probabilistic/stochastic forecast; a new service / URI noun / schema / `$defs` edit; Trust (S5)
  change; fabricated per-option requirements. The new org's per-option requirement MUST be recorded;
  the engine never invents it.

## The target (what "done" looks like)
1. **A real "recommended option is infeasible" org story.** New or reused org (e.g. `deli-recommend-infcap`):
   it RECORDS per-option requirements such that the frozen machine-eligible best / Q8 recommendation
   (partial-settlement) has a recorded requirement > available => `capacity_infeasible` on THAT option,
   while some other option remains `capacity_risk` or `capacity_infeasible`. Document the exact recorded
   numbers.
2. **The marker-is-a-reason-not-a-choice proof.** On that org assert: q7.options (count + uris) +
   q7.machine_eligible_best + q8.recommendation + floor_gated EXACTLY equal `cockpit_q7q8`; the Q8
   recommendation is STILL partial-settlement even though `options_flagged` marks partial-settlement
   `capacity_infeasible`; the `capacity_constraint` `note` names the UNCHANGED Q8 + the §6 human. The
   marker LABELS "this recommended option cannot run"; it does NOT pick a replacement.
3. **The optimization frontier, named honestly.** In the report + §16: state plainly that a
   capacity-constrained OPTIMIZATION that RE-RANKS the recommendation is out of scope of the
   deterministic advisory stance, and spell out what it WOULD need if ever wanted (recorded per-option
   requirements + a deterministic next-best-non-infeasible rule by the frozen `rank` utility) — but
   that choosing a different option for the machine is a policy decision, not a label.
4. **Byte-identity + Sprint-29 regression.** The reused orgs carry the EXACT Sprint-29 output
   (headroom org `{reason:"headroom", options_flagged:{}}`, no per-option keys; `deli-infcap` /
   `deli-deficit-inf` byte-identical; the 4 no-capacity orgs carry NO `capacity_constraint`); a
   no-requirements org keeps today's block exactly (strict superset); Q3 horizon suffix + Q9
   `capacity_planning_attention` + the org-level reason unchanged; full §7L Q1–Q10 on each; determinism
   (dict + render); no wall-clock / no invented number. Emit fixtures + report.
5. **Honest docs.** Additive note in `docs/ENGINE-FORECAST-CAPACITY.md` (a §14) + `ENGINE-S7L-COCKPIT.md`
   (§12): the marker is a REASON never a CHOICE — the sharpest boundary, "the recorded capacity says the
   recommended option can't run", is now demonstrated AS DATA, while the Q8 recommendation provably
   stays the frozen `rank` output; a capacity-constrained OPTIMIZATION that re-ranks stays out of the
   deterministic advisory stance. Extend the §16 verdict.
6. **Real output:** new runner ALL PASS; full non-regression green; no new noun, 49 `$defs`, SPEC v0.22.

## Mandatory rules
- **Write-first:** `sprints/sprint-30/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is
  `instances/contested_reality/adjudication_engine.py`, and ONLY additively if a genuine defect/need
  surfaces; prefer recorded data + a runner. Keep frozen functions untouched; keep 49 `$defs` + URI
  cap + SPEC v0.22. Re-verify `ros/`, the schema hash (`7fc38c8c…`), and the sector instances
  untouched; the default orgs' output must be a strict SUPER SET of Sprint 29 preserving every
  pre-existing byte.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-29 state): `run_forecast_per_option_capacity_demo.py` +
  `run_forecast_horizon4_demo.py` + `run_forecast_horizon3_demo.py` + `run_forecast_horizon2_demo.py` +
  `run_forecast_horizon_demo.py` + `run_forecast_variance_all_demo.py` + `run_forecast_variance_demo.py`
  + `run_forecast_direction_demo.py` + `run_forecast_action_demo.py` + `run_forecast_capacity_demo.py` +
  `run_cockpit_s7l_demo.py` + `run_cockpit_q7q8_demo.py` + `run_adjudication_engine_demo.py` (plain
  python3) + the 5 CR conformances (Sprint-0 venv) + `build_all.py` + `conformance_all.py` + S5
  reference + conformance + agent demo + conformance.
- New assertions ALL PASS (above). Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema
  clean; schema hash `7fc38c8c…`.

## Documentation (roll-forward)
- Additive note in `docs/ENGINE-FORECAST-CAPACITY.md` + `docs/ENGINE-S7L-COCKPIT.md`; append a Sprint-30
  entry to `instances/README.md`; append an "Update after Sprint 30" note to
  `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; reference the new build in
  `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-30/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize, per org, the sharpest label-vs-choice assertion this sprint made
(which RECORDED per-option requirement made WHICH recommended option `capacity_infeasible`, the
available-capacity arithmetic, that the Q8 recommendation STILL equals `cockpit_q7q8` — the marker is a
REASON, never a CHOICE), the byte-identical default (orgs that record no per-option requirement keep
Sprint-29's block exactly), that this is generic + additive (recorded `metric://` series + recorded
point-`variance` + the recorded `band_variance` source + a recorded authority `capacity` + a recorded
per-option `capacity_required` descriptor; no new noun, frozen 49 `$defs`), the honest §16 verdict on
whether the marker now reaches the RECORDED per-option limit WHILE the Q8 recommendation provably
stays unchanged — and what is still not derivable (a capacity-constrained OPTIMIZATION that RE-RANKS
the recommendation for the machine stays out of scope of the deterministic advisory stance; the marker
never CHOOSES; a per-option requirement that is NOT unit-coupled to the recorded capacity / an option
with no recorded requirement remains non-derivable) — and the verified build + conformance commands.
Write the **next** sprint's self-contained prompt at `sprints/sprint-31/PROMPT.md`.

NOTE: the "what is left" frontier after THIS sprint is the boundary itself — the deterministic advisory
stance can label an option (even the recommended one) as capacity-infeasible from recorded data, but it
cannot and must not choose the replacement for the §6 human. A genuinely capacity-constrained
OPTIMIZATION that moves the recommendation is a POLICY / user request, not a label, and stays firmly
out of scope unless the prompt author explicitly asks to build it (which would be a deliberate
"re-rank for the machine" capability change). Be honest about that in the §16 verdict.