# SPRINT 29 — PROMPT (the honest frontier Sprint 28 left open: the marker can label `capacity_risk`,
# but `capacity_infeasible` is STRUCTURALLY UNREACHABLE because no PER-OPTION capacity requirement is
# ever recorded — the engine compares the org-level recorded `load` / horizon band to the recorded
# capacity VALUE, so it can flag a whole option set as risky, but it can never say a SPECIFIC option is
# infeasible under capacity, and it can never price capacity correctly per option)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 20–28 built the configurable adjudication engine
(`instances/contested_reality/adjudication_engine.py`) that renders the full §7L Q1–Q10 morning
cockpit for ANY configured org, data-only; Sprint 26 added a data-only Q9 `capacity_planning_attention`
reason; Sprint 27 connected the recorded capacity to the Q7/Q8 trade-off as an additive
`capacity_constraint` block ({recorded_capacity, horizon_band, reason, flag, options_flagged, note})
via the shared `_capacity_reason` helper; **Sprint 28 PROVED that marker at its LIMIT** — it drove
real at-capacity (`deli-atcap`, recorded load 1.25) and deficit (`deli-deficit`, horizon high 32.0 >=
recorded capacity value 30.0) orgs and asserted the FULL block (reason + flag True + EVERY
capacity-consuming non-baseline option marked `capacity_risk`, baseline never flagged) while proving
the Q7 `options` + `machine_eligible_best` + Q8 `recommendation`/`floor_gated` stay EXACTLY equal to
`cockpit_q7q8` (the marker is a LABEL — no §6 overrule, no re-rank, no option-removal).
**Sprint 28's own finding (`sprints/sprint-28/notes/findings.md`, "Open issues / next work") discloses
the next honest frontier: the marker still cannot say a SPECIFIC option is `capacity_infeasible`,
because NO PER-OPTION capacity requirement is ever recorded.** Everything the engine labels today is
org-level: the recorded `load` (>= 1.0 -> at-capacity), the horizon band's worst-side vs the recorded
capacity VALUE (-> deficit), and `options_flagged` lumps ALL capacity-consuming non-baseline options
into `capacity_risk`. It can never name a particular option that the recorded capacity cannot
actually run. **A bounded Sprint 29 slice: RECORD a per-option capacity REQUIREMENT** as an additive,
unit-coupled descriptor on the trade-off (per configured option, how much of the recorded capacity
unit that option consumes), and let the engine derive a per-option `capacity_infeasible`/`capacity_risk`
label from that RECORDED number vs the RECORDED available capacity — still a LABEL on the trade-off,
still never a re-rank, never a removal, never an overrule of the §6 human.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7K.1 (Policy,
  Trade-off, Organizational Learning, Forecast, Decision→Expected→Variance→WHY), §7L (the ten morning
  questions), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — esp. `_capacity_reason` (the SHARED
    headroom/at-capacity/deficit rule, Sprint 27/28) + the Q7/Q8 `capacity_constraint` block in
    `cockpit_s7l` (Sprint 27) + the Q9 `capacity_planning_attention` (Sprint 26/27) + `_forecast_closure`
    (the band / `band_horizon`) + the frozen `rank`/`machine_eligible_best`/`render_tradeoff`/
    `cockpit_q7q8`/`reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`.
  - `run_forecast_horizon4_demo.py` (Sprint 28 — the runner that proved the non-headroom limit and
    the two NON-headroom orgs `deli-atcap`/`deli-deficit`), `run_forecast_horizon3_demo.py` (Sprint 27),
    `run_forecast_horizon2_demo.py` (+ its `r26.build_orgs`), `run_forecast_horizon_demo.py`,
    `run_forecast_variance_demo.py`, `run_forecast_capacity_demo.py` — reuse their builders/constants
    (`relabel_to`, `run_one`, `record_series`, `record_capacity`, `_capacity_reason`, the VMC/VM/CO
    points, `rfh.*`, `rfv.*`, `r26.*`).
  - `adjudication_configs.py` (DELI + INSPECT + COVE + the rule library) + `docs/ENGINE-FORECAST-CAPACITY.md`
    (§10–§12, the marker proven at headroom/at-capacity/deficit) + `docs/ENGINE-S7L-COCKPIT.md` (§9–§10)
    + `sprints/sprint-28/{summary.md,notes/findings.md}` + `sprints/sprint-27/notes/findings.md`.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16);
  additive only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get
  one-arg, `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2
  RFC3339 temporal-suffix keys — never name an additive field ending in
  `at|time|deadline|expires|expiry|effective|due|since`, so `capacity_required` / `per_option_capacity`
  are fine but do not invent a key ending in `time`; strict C5 tables, `eng.reconcile(sub, cfg)` ARG
  ORDER, the Sprint-0 venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for
  conformance, runner CWD-sensitivity, `[0]`-indexed `parents`, json round-trip restores `floor_gated`
  sets, float-vs-int formatting, and that the band is a RECORDED-DATA spread, not a confidence
  interval — plus Sprint 28's lesson that the engine `_capacity_reason`+`capacity_constraint` block
  already fully implement all three reasons, so a NEW rule or a NEW recorded descriptor is the point
  of THIS sprint, not a re-run of the existing headroom/at-capacity/deficit proof).

## What Sprint 29 IS and IS NOT
- **IS:** make the recorded capacity PER-OPTION — record, additively on the configured trade-off, a
  per-option capacity requirement (e.g. an additive `capacity_required` field per option: how many
  units of the recorded capacity unit the option consumes to run), and extend the Q7/Q8
  `capacity_constraint` block so `options_flagged` can carry, from recorded numbers only, a
  per-option label: **`capacity_infeasible`** when that option's REQUIREMENT exceeds the AVAILABLE
  capacity (recorded capacity VALUE minus recorded consumed load, unit-coupled by construction) and
  otherwise `capacity_risk` as today. Prove on a real §7L cockpit with NEW orgs that RECORD per-option
  requirements such that SOME option is infeasible and a cheaper one is merely risky, while the Q8
  recommendation / machine-eligible-best / option set stay EXACTLY equal to `cockpit_q7q8`.
- **IS NOT:** a new service, a new URI noun, a schema/`$defs` edit, a Trust change (S5), changing the
  frozen `rank`/`machine_eligible_best`, a **re-ranking / capacity-constrained OPTIMIZATION** that
  makes the MACHINE choose a different option (the §6 human always does; the marker only labels), a
  probabilistic/stochastic forecast, a re-implementation of
  `run_scenario`/`reconcile`/`cockpit_q7q8`/`rank`/`machine_eligible_best`/`render_tradeoff`/`_derive`,
  or fabricated per-option requirements. The per-option requirement MUST be a RECORDED descriptor; the
  engine never invents it.

## The target (what "done" looks like)
1. **A recorded per-option capacity requirement.** Extend the configured org data additively: each
   option may carry an additive `capacity_required` (non-negative; in the SAME unit as the recorded
   authority `capacity`). An org with NO per-option requirements stays byte-identical (today's block);
   an org that records them gains the per-option inference. Keep 49 `$defs` + URI cap + SPEC v0.22.
   (If the cleanest home is a `capacity_requirements` additive map on `cfg`/the option set, choose it
   and document it; the point is the requirement is recorded data, never invented.)
2. **Per-option infeasibility via ONE recorded rule.** In `cockpit_s7l`'s Q7/Q8 `capacity_constraint`
   block, when per-option requirements are recorded, derive the AVAILABLE capacity from recorded
   numbers only (recorded capacity VALUE − recorded `load`, per the recorded unit) and mark an option
   `capacity_infeasible` iff its recorded requirement > available; otherwise keep today's `capacity_risk`
   (and never flag the baseline do-nothing/UNRESOLVED). The whole block stays a LABEL — no option
   removed, no re-rank, no §6 overrule, and the Q8 recommendation/machine-eligible-best remain the
   frozen `rank` output.
3. **New orgs (≥5 fresh) on the full §7L cockpit** in `run_forecast_per_option_capacity_demo.py`
   (new, exit 0 = ALL PASS): reuse the Sprint-28 five byte-identical (`deli-forecast`, `deli-varmax`,
   `deli-varmax-cap`, `deli-flat2`, `deli`) PLUS new orgs that RECORD per-option requirements, e.g.:
   - **`deli-infcap`** — RECORD the at-capacity situation (e.g. capacity 500.0 res/day, recorded
     load 1.3) AND per-option `capacity_required` (e.g. the heavy options require more than the
     available capacity => `capacity_infeasible`, the light/do-nothing baseline requires none =>
     never flagged). Assert the per-option distinction in `options_flagged` (some
     `capacity_infeasible`, some `capacity_risk`, baseline absent) + `reason` still
     `at-capacity`/`deficit` from the org-level rule, + the Q8 recommendation EXACTLY equal to
     `cockpit_q7q8`.
   - optionally **`deli-deficit-inf`** — the deficit situation with per-option requirements.
   Document the exact recorded numbers so the infeasibility is trivially reproducible.
4. **Byte-identity + Sprint-28 regression.** The five reused orgs carry the exact Sprint-28 output
   (the headroom org still `reason:"headroom", options_flagged:{}`; `deli-atcap`/`deli-deficit`
   byte-identical); orgs that record NO per-option requirement keep today's block EXACTLY (a strict
   superset); Q3 horizon suffix + Q9 `capacity_planning_attention` + the org-level reason unchanged;
   full §7L Q1–Q10 on each; determinism (dict + render); no wall-clock / no invented number (every
   `capacity_infeasible`/`capacity_risk` trace to a recorded field). Emit fixtures + report.
5. **Honest docs.** Additive note in `docs/ENGINE-FORECAST-CAPACITY.md` (a §13) + `ENGINE-S7L-COCKPIT.md`
   (§11): the marker can now reach `capacity_infeasible` for a SPECIFIC option from a RECORDED
   per-option requirement, while it is still a label — never a removal, never a re-rank, never an
   overrule; the Q8 recommendation provably stays unchanged even when SOME option is infeasible.
   Extend the §16 verdict: has the marker now reached the recorded per-option limit, and does it still
   never re-rank?
6. **Real output:** new runner ALL PASS; full non-regression green; no new noun, 49 `$defs`, SPEC v0.22.

## Mandatory rules
- **Write-first:** `sprints/sprint-29/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is
  `instances/contested_reality/adjudication_engine.py`, and ONLY to extend the Q7/Q8
  `capacity_constraint` block (or the shared `_capacity_reason`) additively for the NEW recorded
  per-option requirement; keep the frozen functions untouched. Keep 49 `$defs` + URI cap + SPEC v0.22.
  Re-verify `ros/`, the schema hash (`7fc38c8c…`), and the sector instances untouched; the default
  orgs' output must be a strict SUPER SET of Sprint 28 preserving every pre-existing byte.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-28 state): `run_forecast_horizon4_demo.py` + `run_forecast_horizon3_demo.py`
  + `run_forecast_horizon2_demo.py` + `run_forecast_horizon_demo.py` + `run_forecast_variance_all_demo.py`
  + `run_forecast_variance_demo.py` + `run_forecast_direction_demo.py` + `run_forecast_action_demo.py`
  + `run_forecast_capacity_demo.py` + `run_cockpit_s7l_demo.py` + `run_cockpit_q7q8_demo.py` +
  `run_adjudication_engine_demo.py` (plain python3) + the 5 CR conformances (Sprint-0 venv) +
  `build_all.py` + `conformance_all.py` + S5 reference + conformance + agent demo + conformance.
- New assertions ALL PASS (above). Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema
  clean; schema hash `7fc38c8c…`.

## Documentation (roll-forward)
- Additive note in `docs/ENGINE-FORECAST-CAPACITY.md` + the trade-off/cockpit doc; append a Sprint-29
  entry to `instances/README.md`; append an "Update after Sprint 29" note to
  `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; reference the new build in
  `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-29/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize, per org, the new per-option `capacity_infeasible` label (which
RECORDED per-option requirements + which available-capacity arithmetic became an infeasible option vs
a merely risky one, the baseline never flagged, the org-level reason preserved), the byte-identical
default (orgs that record no per-option requirement keep today's block exactly), that this is generic +
additive (recorded `metric://` series + recorded point-`variance` + the recorded `band_variance` source
+ a recorded authority `capacity` + a NEW recorded per-option `capacity_required` descriptor; no new
noun, frozen 49 `$defs`), the ≥5-org proof (default byte-identity vs headroom vs at-capacity vs deficit
vs per-option-infeasible vs no-data), the honest §16 verdict on whether the marker now reaches the
recorded per-option limit WHILE the Q8 recommendation provably stays unchanged — and what is still not
derivable (a capacity-constrained OPTIMIZATION that re-ranks for the machine stays out of scope; a
per-option requirement that is not unit-coupled to the capacity remains non-derivable) — and the
verified build + conformance commands. Write the **next** sprint's self-contained prompt at
`sprints/sprint-30/PROMPT.md`.

NOTE: the "what is left" frontier after THIS sprint is whatever the per-option requirement surfaces
(the marker can now name a single infeasible option from a recorded requirement, but it still never
CHOOSES a different option — the §6 human always does — and a genuinely capacity-constrained
optimization that changes the recommendation stays out of scope of the deterministic advisory stance).
Be honest about that in the §16 verdict.