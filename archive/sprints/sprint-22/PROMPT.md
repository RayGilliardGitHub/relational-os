# SPRINT 22 — PROMPT (the honest frontier Sprint 21 disclosed: the forecast→attention crossing test is hardcoded to the higher-is-better direction)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 13–21 built a configurable adjudication engine (`instances/contested_reality/
adjudication_engine.py`) that renders the full §7L Q1–Q10 morning cockpit for ANY configured org,
data-only, and (Sprint 20) answers Q6 forecast + Q9 capacity AS DATA where the data exists, and
(Sprint 21) makes the RECORDED forecast drive Q3 attention + the Q8 do-nothing expected-impact.
**Sprint 21's own finding (see `sprints/sprint-21/notes/findings.md`, "Open issues / next work")
discloses the next honest frontier: the forecast→attention **crossing test is hardcoded to the
higher-is-better / rate case** (`min(projection) < threshold`); a metric where "lower is better" (a
cost, latency, defect rate, or risk) would NOT flag as forecast-driven attention when it deteriorates
by RISING above a recorded ceiling.** Sprint 22 closes that bounded slice: make the crossing **direction
a recorded, additive parameter** so the SAME data-only closure flags attention + prices the do-nothing
cost for BOTH directions — a rate/quality metric (higher-is-better: below-target is bad) AND a
cost/latency/defect metric (lower-is-better: above-ceiling is bad) — deterministically from the recorded
`metric://` series, with the Sprint-21 higher-is-better behavior unchanged (byte-identical default).

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7J.5 (attention), §7K.1
  (Policy, Trade-off, Organizational Learning, Forecast, Decision→Expected→Variance→WHY→change-future-policy),
  §7L (the ten morning questions), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — esp. `_forecast_closure` (Sprint 21: the
    threshold resolution + `crossing = min(projection) < threshold` + the do-nothing summary), the frozen
    functions (`reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`, `rank`,
    `machine_eligible_best`, `render_tradeoff`, `cockpit_q7q8`), and `cockpit_s7l`'s `.q3`/`.q6`/`.q8`.
  - `run_forecast_action_demo.py` (Sprint 21 runner — how the two recorded orgs `deli-forecast` and
    `deli-forecast-flat` + the no-data `deli` prove the closure), `run_forecast_capacity_demo.py`
    (Sprint 20 runner), `adjudication_configs.py` (DELI/COVE/INSPECT + variants).
  - `sprints/sprint-21/{summary.md,notes/findings.md}` + `docs/ENGINE-FORECAST-ACTION.md` and the
    Sprint-21 note in `docs/ENGINE-FORECAST-CAPACITY.md`.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16); additive
  only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get one-arg,
  `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2 RFC3339
  temporal-suffix keys — never name an additive field ending in `at|time|deadline|expires|expiry|effective|
  due|since` — strict C5 tables, `eng.reconcile(sub, cfg)` ARG ORDER, the Sprint-0 venv
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance, runner
  CWD-sensitivity, `[0]`-indexed `parents` for the Sprint-0 path, json round-trip converts `floor_gated`
  sets — restore them).

## What Sprint 22 IS and IS NOT
- **IS:** make the forecast→attention crossing **direction** a recorded, additive parameter, so the
  Sprint-21 closure — a recorded `metric://` series + `forecast_metric` projection — flags **forecast-driven
  Q3 attention and prices the Q8 do-nothing expected-impact for BOTH directions**, deterministically and
  data-only: (i) **higher-is-better** (rate/quality; the Sprint-21 default: `min(projection) < threshold`
  is bad) and (ii) **lower-is-better** (cost/latency/defect/risk: `max(projection) > threshold` is bad).
  The direction is recorded on the `metric://` object as an additive `direction` field (`"higher-is-better"`
  default to keep Sprint-21 behavior byte-identical, or an explicit recorded value), so the same generic
  engine path serves any org that records the metric's direction. The do-nothing summary must report the
  gap in the correct orientation (rate: "below target"; cost/latency: "above ceiling"). Prove it with a
  runner that drives ≥3 orgs: the two Sprint-21 recorded orgs (higher-is-better, unchanged behavior) PLUS a
  new **lower-is-better** org (e.g. `deli-cost` — a recorded cost/latency metric whose projection RISES
  above a recorded ceiling → forecast attention + a projected do-nothing cost on_target=False), plus a
  no-data org, and asserts the full §7L on each plus the projection→attention→expected-impact closure in
  BOTH orientations, determinism, agreement with the recorded series, and no §6 overrule.
- **IS NOT:** a new service, a new URI noun, a schema/`$defs` edit, a Trust change (S5), a change that lets
  the machine overrule the §6 human (the Q8 recommendation stays the §6-floor-gated machine-eligible best
  and the determination stays the `determination_policy` call; the forecast only prices attention +
  do-nothing, never auto-picks), a re-implementation of `run_scenario`/`reconcile`/`cockpit_q7q8`, an
  adaptive/learned forecast model, or any wall-clock/best-guess. No frontier spend.

## The target (what "done" looks like)
1. An additive **directional crossing** in `_forecast_closure`: read a recorded `direction` off the
   `metric://` object (`"higher-is-better"` default; explicit `"lower-is-better"` for cost/latency/defect/
   risk), and compute crossing per direction (`min < threshold` for higher-is-better; `max > threshold` for
   lower-is-better). The do-nothing summary + gap orientation follow the direction. The recorded threshold
   resolution from Sprint 21 is unchanged (`forecast_threshold` additive field → metric `target` → last
   recorded `actual`).
2. **Sprint-21 higher-is-better behavior is byte-identical** (default `direction` == `"higher-is-better"`):
   the two recorded orgs `deli-forecast`/`deli-forecast-flat` and the no-data `deli` keep their exact Q3/Q8/
   trade-off output.
3. A runner (`run_forecast_direction_demo.py`, exit 0 = ALL PASS) that drives ≥4 orgs: the Sprint-21
   `deli-forecast` (higher-is-better, deteriorating), `deli-forecast-flat` (higher-is-better, on-target), a
   NEW **lower-is-better** org whose projection RISES above a recorded ceiling (e.g. `deli-cost`: a recorded
   `metric://deli-cost/m-latency` cost/latency series whose actuals 12/14/16/18 ms with a ceiling/`target`
   16 ms project to 18/20/22 → `max > ceiling` → forecast attention + a projected do-nothing cost
   on_target=False), and the no-data `deli`. Asserts: full §7L Q1–Q10 on each; the higher-is-better orgs are
   byte-identical to Sprint 21; the lower-is-better org's Q3 carries the `[forecast]` item + Q8/trade-off
   prices do-nothing in the RISING orientation (on_target=False); determinism; agreement between the
   projection used in Q3/Q8 and `forecast_metric`; no §6 overrule (Q8 recommendation unchanged). Optionally
   include a second lower-is-better control whose projection stays below the ceiling (no forecast attention,
   do-nothing on_target=True) to mirror the Sprint-21 flat control. Emit fixtures + a report.
4. **Honest docs** (`docs/ENGINE-FORECAST-DIRECTION.md` + an additive note in `docs/ENGINE-FORECAST-ACTION.md`):
   the directional crossing rule (which recorded `direction`/threshold combination flags a forecast-driven
   attention item; how the do-nothing baseline is priced in each orientation) and the honest no-data
   fallback, plus a §16-style verdict: does the forecast→action closure now serve BOTH directions as data —
   and what is still not derivable?
5. **Real output:** new runner ALL PASS; full non-regression green; no new noun, 49 `$defs`, SPEC v0.22.

## Mandatory rules
- **Write-first:** `sprints/sprint-22/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is
  `instances/contested_reality/adjudication_engine.py` (extend `_forecast_closure`'s crossing + summary and
  `render_cockpit_s7l` if needed — do NOT rewrite `reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/
  `_aggregate`/`rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`, frozen). Keep 49 `$defs` +
  URI cap + SPEC v0.22. Re-verify `ros/`, the schema hash (`7fc38c8c…`), and the sector instances
  untouched. deli/cove byte-identical up to the clock, AND the two Sprint-21 recorded orgs' Q3/Q8 unchanged
  (direction default).
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-21 state): `run_forecast_action_demo.py` (Sprint 21) + `run_forecast_capacity_demo.py`
  + the 12 curated C-R runners + `run_cockpit_s7l_demo.py`, `conformance_adjudication.py` (16 labels), the 4
  prior CR demos + conformances, `build_all.py` + `conformance_all.py`, S5 reference + conformance,
  `agent_demo` + conformance.
- New assertions ALL PASS (above). Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema clean.
- **Byte-identity:** the two Sprint-21 recorded orgs' Q3/Q8/trade-off unchanged (direction default); every
  projection/expected-impact derived from recorded series values only (no wall-clock / no invented number).

## Documentation (roll-forward)
- Add `docs/ENGINE-FORECAST-DIRECTION.md`; append a Sprint-22 entry to `instances/README.md`; append an
  "Update after Sprint 22" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; append
  an additive note to `docs/ENGINE-FORECAST-ACTION.md` (the crossing test now honors a recorded direction);
  reference the new build in `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-22/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize what the directional crossing reports per org (the recorded
`direction` + threshold rule that flags a forecast-driven Q3 attention item; how the do-nothing baseline is
priced in each orientation; the honest no-data fallback; that the higher-is-better default keeps Sprint 21
byte-identical), how it is generic + additive (recorded `metric://` series + a recorded `direction` field +
`forecast_metric`, no new noun, frozen 49 `$defs`), the ≥3/4-org proof (higher-is-better deteriorating +
on-target unchanged from Sprint 21; a new lower-is-better rising-cost org → forecast attention + projected
do-nothing cost; no-data fallback), the honest §16 verdict on whether the forecast→attention→expected-impact
closure now serves BOTH directions as data where the data exists, and the verified build + conformance
commands. Write the **next** sprint's self-contained prompt at `sprints/sprint-23/PROMPT.md`.