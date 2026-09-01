# SPRINT 28 — PROMPT (the honest frontier Sprint 27 disclosed: the Q7/Q8 `capacity_constraint` marker
# is built and proven only in its headroom branch — a capacity-recording org at headroom shows
# `reason: "headroom", options_flagged: {}` — and the marker's non-headroom branches (at-capacity /
# deficit), while implemented in the shared `_capacity_reason` helper, are NEVER exercised on a real
# org, so the `capacity_risk` flags + the honest "same options, same recommendation" behavior at the
# marker's limit are unproven end-to-end)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 20–27 built the configurable adjudication engine
(`instances/contested_reality/adjudication_engine.py`) that renders the full §7L Q1–Q10 morning
cockpit for ANY configured org, data-only; Sprint 23 priced the Q8/trade-off do-nothing expected-impact
as a projected BAND; Sprint 24 made the band's variance a recorded `band_variance`; Sprint 25 carried
the SAME recorded sigma to EVERY projection period (`band_periods`) + a record-wide `band_horizon`;
Sprint 26 made the Q3 attention `why` name the horizon-wide band (shared `_HORIZON_BAND_PHRASE`) AND
added a data-only Q9 `capacity_planning_attention` REASON ({flag, why}); **Sprint 27 made the recorded
capacity a data-only CONSTRAINT on the Q7/Q8 trade-off** — an additive `capacity_constraint` block on
both `q7` and `q8` ({recorded_capacity, horizon_band, reason, flag, options_flagged, note}) via the
shared `_capacity_reason` helper (headroom / at-capacity / deficit), with the capacity-consuming
non-baseline options marked `capacity_risk` (never `capacity_infeasible`) when not headroom — WITHOUT
removing any option and WITHOUT changing `machine_eligible_best`/the Q8 recommendation.
**Sprint 27's own finding (`sprints/sprint-27/notes/findings.md`, "Open issues / next work") discloses
the next honest frontier: the marker is proven end-to-end ONLY in headroom (`deli-varmax-cap` →
`reason: "headroom", options_flagged: {}`); its at-capacity / deficit branches exist in the helper but
are NEVER exercised on a real org, so (a) the `capacity_risk` flagging, (b) the derived reason itself,
and (c) the honest "the SAME machine-eligible options and the SAME Q8 recommendation remain, correctly,
with only a capacity_risk label" are unproven AS DATA on a living Q1–Q10 cockpit.** A bounded Sprint 28
slice: drive the non-headroom branches on real, recorded-data orgs — an **at-capacity** org (recorded
`load >= 1.0` → `reason: "at-capacity"`) and a **deficit** org (the horizon band's worst-side magnitude
reaches/exceeds the recorded capacity VALUE → `reason: "deficit"`) — and assert the full
`capacity_constraint` block (reason, flag=True, `options_flagged` marking the capacity-consuming
non-baseline options `capacity_risk`) while PROVING the Q7 `options` set and the Q8
`recommendation`/`machine_eligible_best` stay EXACTLY equal to `cockpit_q7q8` (the marker is a LABEL
at its limit, never a re-rank, never an option-removal; the §6 human always rules).

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7K.1 (Policy,
  Trade-off, Organizational Learning, Forecast, Decision→Expected→Variance→WHY), §7L (the ten morning
  questions), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — esp. `_capacity_reason` (the SHARED
    headroom/at-capacity/deficit rule, Sprint 27) + `cockpit_s7l`'s Q7/Q8 Sprint-27 `capacity_constraint`
    block + Q9 `capacity_planning_attention` (Sprint 26) + `_forecast_closure` (the band/`band_horizon`);
    the frozen functions (`reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`, `rank`,
    `machine_eligible_best`, `render_tradeoff`, `cockpit_q7q8`).
  - `run_forecast_horizon3_demo.py` (Sprint 27), `run_forecast_horizon2_demo.py` (Sprint 26),
    `run_forecast_horizon_demo.py` (Sprint 25) — reuse their builders/constants
    (`relabel_to`, `run_one`, `record_series`, `record_capacity`, `_capacity_reason`, the VMC capacity
    values, `r26.build_orgs`/`rfh.*`).
  - `adjudication_configs.py` (DELI + variants) + the `q9`/`q7`/`q8` render usage in
  `adjudication_engine.py` + `docs/ENGINE-FORECAST-CAPACITY.md` (§10 and the Sprint-27 §11) +
    `docs/ENGINE-S7L-COCKPIT.md` (§9) + `sprints/sprint-27/{summary.md,notes/findings.md}`.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16);
  additive only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get
  one-arg, `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2
  RFC3339 temporal-suffix keys — never name an additive field ending in
  `at|time|deadline|expires|expiry|effective|due|since`, so `at_capacity` as a KEY is fine but do not
  invent a key ending in `time`; strict C5 tables, `eng.reconcile(sub, cfg)` ARG ORDER, the Sprint-0
  venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance, runner
  CWD-sensitivity, `[0]`-indexed `parents`, json round-trip restores `floor_gated` sets, float-vs-int
  formatting, and that the band is a RECORDED-DATA spread, not a confidence interval).

## What Sprint 28 IS and IS NOT
- **IS:** demonstrate the Sprint-27 Q7/Q8 `capacity_constraint` marker at its recorded-data LIMIT —
  feel free to add NEW fresh orgs that RECORD an at-capacity (`load >= 1.0`) and a deficit (horizon
  worst-side >= capacity value) situation, so the non-headroom branch of the SHARED `_capacity_reason`
  rule is exercised on a REAL full Q1–Q10 cockpit (reason + flag=True + `options_flagged` marking the
  capacity-consuming non-baseline options `capacity_risk`). It adds ONLY recorded data + a runner
  (and, ONLY if a real gap surfaces, an additive engine tweak — undocumented behavior must be captured
  in findings and, if it is a genuine defect, fixed additively). It asserts the marker is a LABEL AT
  ITS LIMIT: the Q7 `options` set and `machine_eligible_best` and the Q8 `recommendation` are EXACTLY
  equal to `cockpit_q7q8` even at at-capacity / deficit.
- **IS NOT:** a new service, a new URI noun, a schema/`$defs` edit, a Trust change (S5), a change that
  removes an option or overrules the §6 human or the frozen `rank`/`machine_eligible_best`, a
  **re-ranking / capacity-constrained OPTIMIZATION** (the engine never CHOOSES a different option for
  the machine — the §6 human always does), a probabilistic/stochastic forecast, a re-implementation of
  `run_scenario`/`reconcile`/`cockpit_q7q8`/`rank`/`machine_eligible_best`/`render_tradeoff`/`_derive`,
  or a fabricated capacity or per-option requirement. No frontier spend.

## The target (what "done" looks like)
1. **At-capacity and deficit orgs on the full §7L cockpit.** In `run_forecast_horizon4_demo.py` (new,
   exit 0 = ALL PASS), drive ≥5 fresh orgs: the four Sprint-27 ones reused byte-identical
   (`deli-forecast`, `deli-varmax`, `deli-varmax-cap` headroom, `deli` no-data; keep `deli-flat2`
   too as the no-band control if convenient) PLUS a new **`deli-atcap`** org (same whole-series band as
   `deli-varmax` — e.g. `band_variance:"all"`, horizon 0.62…1.02 — with a RECORDED capacity and a
   recorded **`load >= 1.0`**, e.g. load 1.25, so `_capacity_reason` yields **at-capacity**) and/or a
   new **`deli-deficit`** org (a lower-is-better cost/defect metric — `direction:"lower-is-better"` —
   whose horizon band's worst-side HIGH reaches/exceeds a small recorded capacity VALUE, so
   `_capacity_reason` yields **deficit**). Document the exact recorded numbers you choose so the reason
   is trivially reproducible.
2. **The non-headroom block is fully exercised.** For the at-capacity / deficit org(s) assert:
   `q7["capacity_constraint"]` and `q8["capacity_constraint"]` carry `reason` == "at-capacity"/"deficit",
   `flag` is True, and `options_flagged` marks EVERY capacity-consuming NON-baseline option
   `capacity_risk` (and does NOT mark the baseline do-nothing/UNRESOLVED). The `reason` equals the Q9
   `capacity_planning_attention` label BY CONSTRUCTION (shared `_capacity_reason`) — assert the
   agreement on every org that records a capacity.
3. **The marker stays a LABEL at its limit.** For EVERY org (incl. the at-capacity/deficit ones) assert
   the Q7 `options` (same count/uris) + `machine_eligible_best` + the Q8 `recommendation`/`floor_gated`
   are EXACTLY equal to `cockpit_q7q8` (no §6 overrule, no re-rank, no option-removal) — this is the
   honest core of the boundary.
4. **Byte-identity + Sprint-26/27 regression.** The four reused orgs carry the exact Sprint-27 output
   (the headroom org still `reason:"headroom", options_flagged:{}`; the no-capacity orgs carry NO
   `capacity_constraint`); the Q3 horizon suffix + Q9 `capacity_planning_attention` unchanged; full
   §7L Q1–Q10 on each; determinism (dict + render); no wall-clock / no invented number (every
   `capacity_constraint` value traces to a recorded field). Emit fixtures + report.
5. **Honest docs.** Additive note in `docs/ENGINE-FORECAST-CAPACITY.md` (a §12 or extend §11) and the
   trade-off / cockpit doc (`ENGINE-S7L-COCKPIT.md`): the marker is now proven at its limit
   (at-capacity / deficit), as a recorded-data REASON, never a removal, never an overrule, and the Q8
   recommendation provably stays unchanged even when the recorded data shows at-capacity or deficit;
   the byte-identical default; the honest no-capacity fallback. Extend the §16 verdict: has the marker
   now been demonstrated across all three of its derived reasons on real orgs, and is the boundary
   (`capacity_constraint` labels but never re-ranks) confirmed?
6. **Real output:** new runner ALL PASS; full non-regression green; no new noun, 49 `$defs`, SPEC v0.22.

## Mandatory rules
- **Write-first:** `sprints/sprint-28/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is
  `instances/contested_reality/adjudication_engine.py`, and ONLY if a real gap surfaces in the
  non-headroom path (extend `cockpit_s7l`'s Q7/Q8 block or the shared `_capacity_reason` additively);
  keep the frozen functions untouched. Keep 49 `$defs` + URI cap + SPEC v0.22. Re-verify `ros/`, the
  schema hash (`7fc38c8c…`), and the sector instances untouched; the default orgs' output must be a
  strict SUPERSET of Sprint 27 preserving every pre-existing byte.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-27 state): `run_forecast_horizon3_demo.py` + `run_forecast_horizon2_demo.py`
  + `run_forecast_horizon_demo.py` + `run_forecast_variance_all_demo.py` + `run_forecast_variance_demo.py`
  + `run_forecast_direction_demo.py` + `run_forecast_action_demo.py` + `run_forecast_capacity_demo.py`
  + `run_cockpit_s7l_demo.py` + `run_cockpit_q7q8_demo.py` + `run_adjudication_engine_demo.py` +
  `conformance_adjudication.py` (16 labels) + the 4 prior CR conformances (venv) + `build_all.py` +
  `conformance_all.py` + S5 reference + conformance + `agent_demo`.
- New assertions ALL PASS (above). Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema
  clean; schema hash `7fc38c8c…`.
- **Superset byte-identity:** the Sprint-27 orgs unchanged except any NEW org added; every new value
  derived from recorded series values + recorded variance + recorded capacity only.

## Documentation (roll-forward)
- Additive note in `docs/ENGINE-FORECAST-CAPACITY.md` + whichever trade-off/cockpit doc the marker
  lands on; append a Sprint-28 entry to `instances/README.md`; append an "Update after Sprint 28" note
  to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; reference the new build in
  `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-28/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize, per org, the Q7/Q8 `capacity_constraint` marker/reason at its
LIMIT (which recorded numbers became the at-capacity/deficit reason, the `capacity_risk` flags on the
capacity-consuming non-baseline options, the baseline never flagged), the byte-identical default, that
this is generic + additive (recorded `metric://` series + recorded point-`variance` + the recorded
`band_variance` source + a recorded authority `capacity`; no new noun, frozen 49 `$defs`), the ≥5-org
proof (default byte-identity vs headroom vs at-capacity vs deficit vs no-data), the honest §16 verdict
on whether the marker is now demonstrated across ALL its derived reasons on real orgs WHILE the Q8
recommendation provably stays unchanged even at at-capacity/deficit — and what is still not derivable
— and the verified build + conformance commands. Write the **next** sprint's self-contained prompt at
`sprints/sprint-29/PROMPT.md`.

NOTE: the "what is left" frontier after THIS sprint is whatever the marker's non-headroom limit surfaces
(the marker still never CHOOSES a different option — the §6 human always does — and a genuinely
capacity-constrained optimization that changes the recommendation stays out of scope of the
deterministic advisory stance; likewise, `capacity_infeasible` stays unreachable until a RECORDED
per-option capacity requirement exists). Be honest about that in the §16 verdict.