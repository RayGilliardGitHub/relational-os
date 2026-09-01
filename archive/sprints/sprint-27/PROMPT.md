# SPRINT 27 — PROMPT (the honest frontier Sprint 26 disclosed: the Q9 capacity-planning REASON is
# derived and labeled, but it does not yet reach the §7L Q7/Q8 trade-off — the org that records a
# capacity deficit / at-capacity reason still sees the SAME machine-eligible options)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 20–25 built the configurable adjudication engine
(`instances/contested_reality/adjudication_engine.py`) that renders the full §7L Q1–Q10 morning cockpit
for ANY configured org, data-only; Sprint 23 priced the Q8/trade-off do-nothing expected-impact as a
projected BAND (worst ± the recorded variance); Sprint 24 made the band's variance SOURCE a recorded,
additive `band_variance` parameter; Sprint 25 carried the SAME recorded sigma to EVERY projection period
(`band_periods`) + a record-wide `band_horizon`, fed Q9 as a `band_capacity_attention` flag, and
connected do-nothing pricing to the whole-horizon worst case; Sprint 26 added a Q3 forecast-driven
attention `why` SUFFIX naming the horizon-wide band (shared `_HORIZON_BAND_PHRASE` constant, strict
prefix, verbatim with Q8/do-nothing) AND a Q9 data-only `capacity_planning_attention` REASON
({flag, why}) derived from a recorded numeric `capacity` + recorded `load` + the horizon band.
**Sprint 26's own finding (`sprints/sprint-26/notes/findings.md`, "Open issues / next work") discloses
the next honest frontier: `capacity_planning_attention` is a derived, labeled REASON on Q9, but it does
NOT yet connect to the §7L Q7/Q8 trade-off — an org that records a capacity deficit / at-capacity reason
still sees the SAME machine-eligible options and the SAME Q8 recommendation as if its capacity were
unbounded.** A bounded Sprint 27 slice: make the recorded capacity a data-only **constraint on the
Q7/Q8 trade-off** — where the org records a numeric capacity AND the horizon band + recorded threshold
make a capacity-defining option infeasible (or where a recorded `load` is at/over capacity), annotate
the affected option(s) on the trade-off with an additive data-only `capacity_infeasible`/`capacity_risk`
marker + reason derived from recorded numbers, WITHOUT removing the option (the §6 human still rules) and
WITHOUT changing the Q8 recommendation's ranking (still the frozen `rank`/`machine_eligible_best`).

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7K.1 (Policy,
  Trade-off, Organizational Learning, Forecast, Decision→Expected→Variance→WHY→change-future-policy),
  §7L (the ten morning questions), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — esp. `_forecast_closure` (the band block,
    the Sprint-25 `band_periods`/`band_horizon`, the Sprint-26 `_HORIZON_BAND_PHRASE` + the Q3
    attention suffix) and `cockpit_s7l` (Q3/Q6/Q7/Q8/Q9 + the Sprint-25 `band_capacity_attention` +
    Sprint-26 `capacity_planning_attention`), the frozen functions (`reconcile`, `run_scenario`,
    `_derive`, `SPEC_VOCAB`, `_aggregate`, `rank`, `machine_eligible_best`, `render_tradeoff`,
    `cockpit_q7q8`, `render_cockpit_s7l`, `forecast_metric`, `record_metric_series`,
    `record_capacity`).
  - `run_forecast_horizon2_demo.py` (Sprint 26 runner — the ≥5 orgs, the Q3 strict-prefix + the
    deli-varmax-cap capacity-planning assertions), `run_forecast_horizon_demo.py` (Sprint 25),
    `adjudication_configs.py` (DELI/COVE + variants) + `adjudication_engine.render_tradeoff`/
    `cockpit_q7q8` (how the Q7 options / Q8 recommendation are produced today).
  - `sprints/sprint-26/{summary.md,notes/findings.md}` + `sprints/sprint-25/{summary.md,notes/findings.md}`
    + `docs/ENGINE-FORECAST-VARIANCE.md` + `docs/ENGINE-FORECAST-DIRECTION.md` +
    `docs/ENGINE-FORECAST-ACTION.md` (incl. its Sprint-26 addendum) + `docs/ENGINE-FORECAST-CAPACITY.md`
    (incl. §10) + `docs/ENGINE-S7L-COCKPIT.md`.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16);
  additive only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get
  one-arg, `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2
  RFC3339 temporal-suffix keys — never name an additive field ending in
  `at|time|deadline|expires|expiry|effective|due|since`, so any NEW capacity-constraint key must avoid
  those suffixes, e.g. `capacity_infeasible` is fine; strict C5 tables, `eng.reconcile(sub, cfg)` ARG
  ORDER, the Sprint-0 venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for
  conformance, runner CWD-sensitivity, `[0]`-indexed `parents`, json round-trip restores
  `floor_gated` sets, float-vs-int formatting, and that the band is a RECORDED-DATA spread, NOT a
  confidence interval).

## What Sprint 27 IS and IS NOT
- **IS:** a data-only **capacity-constraint annotation on the §7L Q7/Q8 trade-off**, derived from the
  recorded capacity + recorded load + the horizon band + the recorded threshold, ONLY where the org
  records a numeric capacity. It ADDS an additive marker + reason to the affected option(s) on the
  trade-off (e.g. an option the recorded capacity makes infeasible, or an `at-capacity`/`deficit`-risk
  reason priced from the horizon band) — a label, never a removal and never an overrule. And it carries
  the SAME honest stance as Sprint 26: state the recorded numbers plainly, label the effect as a derived
  REASON, never invent a capacity figure, never issue a directive. Additive and recorded-data only.
- **IS NOT:** a new service, a new URI noun, a schema/`$defs` edit, a Trust change (S5), a change that
  removes an option or overrules the §6 human or the frozen `rank`/`machine_eligible_best`; NOT a
  probabilistic/stochastic forecast; NOT a re-implementation of `run_scenario`/`reconcile`/
  `cockpit_q7q8`/`rank`/`machine_eligible_best`/`render_tradeoff`; NOT a change to the no-capacity /
  no-band / no-data fallback (still byte-identical); NOT a fabricated capacity or a capacity-deficit
  directive (the constraint line states the recorded numbers and labels the effect). No frontier spend.

## The target (what "done" looks like)
1. **Q7 trade-off carries a recorded-capacity constraint marker.** In `cockpit_s7l` (or an additive
   helper IT calls), ONLY when the org records a numeric `capacity` AND a band + numeric threshold
   exist, add an additive marker on the Q7 trade-off (which lives on the `q7` dict, additive) that:
   - names the recorded capacity value/unit/load and the horizon band;
   - marks any option the recorded data makes infeasible — e.g. an option whose required capacity is
     not derivable from recorded data may be labelled `capacity_risk` rather than `capacity_infeasible`
     (choose and document ONE deterministic rule, e.g. a lower-is-better capacity-consumption metric
     whose horizon wide band exceeds the recorded capacity -> deficit/at-capacity -> mark the
     capacity-consuming options as `capacity_infeasible`; otherwise label `capacity_risk`/`headroom`); and
   - NEVER removes the option and NEVER changes the `machine_eligible_best`/Q8 recommendation.
   Design decision to document: whether the marker rides on each option dict or as a parallel
   `capacity_constraint` block on the trade-off — pick one, keep it additive, prefer the parallel block
   so the frozen `rank` output (which owns `options`) is untouched.
2. **Q8 carries the same reason.** Add an additive `capacity_constraint` block on `q8` (next to
   `do_nothing_expected_impact`) stating the recorded capacity + horizon band and a
   headroom / at-capacity / deficit REASON (reuse the Sprint-26 deterministic rule where possible so Q9
   and Q8 agree by construction), explicitly noting the Q8 recommendation is UNCHANGED.
3. **A runner (`run_forecast_horizon3_demo.py`, exit 0 = ALL PASS)** that drives the same ≥5 fresh orgs
   shape as Sprint 26 (`deli-forecast`, `deli-varmax`, `deli-varmax-cap` — which RECORDS a capacity,
   `deli-flat2` no-band control, `deli` no-data) and asserts: full Q1–Q10; the Q3 suffix +
   `capacity_planning_attention` still present/unchanged (Sprint 26 byte-identity); `deli-varmax-cap`'s
   Q7/Q8 now carry the `capacity_constraint` marker/reason (recorded capacity 500.0 resolutions/day,
   load 0.72, horizon band 0.62…1.02 -> headroom, NO option marked infeasible) while the OTHER orgs
   carry NO capacity-constraint key (byte-identical superset); the Q8 `recommendation` and
   `machine_eligible_best` are EQUAL to `cockpit_q7q8`'s for every org (no §6 overrule, no re-rank);
   the option set on Q7 is UNCHANGED (same count/uris); determinism; no wall-clock / no invented number.
   Emit fixtures + report.
4. **Honest docs** — additive note in `docs/ENGINE-FORECAST-CAPACITY.md` (§11) and the trade-off /
   cockpit docs: the capacity-constraint marker/reason on Q7/Q8 is derived from recorded capacity +
   load + the horizon band (never an invented figure, never a directive, never an option removal); the
   byte-identical default; the honest no-capacity / no-band / no-data fallback. Extend the §16 verdict:
   does the recorded capacity now reach the Q7/Q8 trade-off as a data-only REASON, and is the Q8
   recommendation still provably unchanged?
5. **Real output:** new runner ALL PASS; full non-regression green; no new noun, 49 `$defs`, SPEC v0.22.

## Mandatory rules
- **Write-first:** `sprints/sprint-27/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is
  `instances/contested_reality/adjudication_engine.py` (extend `cockpit_s7l`'s Q7/Q8 blocks or add an
  additive helper it calls; keep the frozen functions — ESPECIALLY `cockpit_q7q8`, `rank`,
  `machine_eligible_best`, `render_tradeoff` — untouched). Keep 49 `$defs` + URI cap + SPEC v0.22.
  Re-verify `ros/`, the schema hash (`7fc38c8c…`), and the sector instances untouched; the default orgs'
  output must be a strict SUPERSET of Sprint 26 preserving every pre-existing byte.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-26 state): `run_forecast_horizon2_demo.py` +
  `run_forecast_horizon_demo.py` + `run_forecast_variance_all_demo.py` + `run_forecast_variance_demo.py`
  + `run_forecast_direction_demo.py` + `run_forecast_action_demo.py` + `run_forecast_capacity_demo.py`
  + `run_cockpit_s7l_demo.py` + `run_cockpit_q7q8_demo.py` + `run_adjudication_engine_demo.py` +
  `conformance_adjudication.py` (16 labels) + the 4 prior CR conformances (venv) + `build_all.py` +
  `conformance_all.py` + S5 reference + conformance + `agent_demo`.
- New assertions ALL PASS (above). Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema
  clean; template hash `7fc38c8c…`.
- **Superset byte-identity:** the variance-carrying orgs and the capacity-recording org unchanged except
  the additive capacity-constraint marker/reason on Q7/Q8 (and ONLY on the capacity-recording org); the
  variance-less control + no-data org unchanged. Every new value derived from recorded series values +
  recorded variance + recorded capacity only.

## Documentation (roll-forward)
- Additive note in `docs/ENGINE-FORECAST-CAPACITY.md` (§11) + whichever trade-off/cockpit doc the
  marker lands on; append a Sprint-27 entry to `instances/README.md`; append an "Update after Sprint 27"
  note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; reference the new build in
  `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-27/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize, per org, the Q7/Q8 capacity-constraint marker/reason (which
recorded numbers became it, when the org records a capacity vs when it does not, the byte-identical
default), that this is generic + additive (recorded `metric://` series + recorded point-`variance` +
the recorded `band_variance` source + a recorded authority `capacity`; no new noun, frozen 49 `$defs`),
the ≥4-org proof (default byte-identity vs a widening whole-series org vs the capacity-recording org vs
variance-less control vs no-data), the honest §16 verdict on whether the recorded capacity now reaches
the Q7/Q8 trade-off as a data-only REASON while the Q8 recommendation provably stays unchanged — and what
is still not derivable — and the verified build + conformance commands. Write the **next** sprint's
self-contained prompt at `sprints/sprint-28/PROMPT.md`.

NOTE: the "what is left" frontier after THIS sprint is whatever the capacity-constraint marker itself
surfaces (e.g. it still does not CHOOSE a different option for the machine — the §6 human always does —
and a genuinely capacity-constrained optimization that changes the recommendation stays out of scope of
the deterministic advisory stance). Be honest about that in the §16 verdict.