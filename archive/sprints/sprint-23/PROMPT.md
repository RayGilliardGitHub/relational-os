# SPRINT 23 — PROMPT (the honest frontier Sprint 22 disclosed: the do-nothing expected-impact is a single point gap that ignores the RECORDED variance it displays on Q6)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 13–22 built a configurable adjudication engine (`instances/contested_reality/
adjudication_engine.py`) that renders the full §7L Q1–Q10 morning cockpit for ANY configured org,
data-only; Sprint 21 made the RECORDED forecast drive Q3 attention + the Q8 do-nothing baseline, and
Sprint 22 made the crossing **direction** a recorded, additive parameter so the closure serves BOTH
orientations (rate/quality falling below target; cost/latency rising above ceiling). **Sprint 22's own
finding (see `sprints/sprint-22/notes/findings.md`, "Open issues / next work") discloses the next honest
frontier: the do-nothing expected-impact is priced as a SINGLE POINT gap (worst projected value vs the
recorded threshold) that IGNORES the RECORDED variance the engine already computes and renders on Q6.**
Sprint 22 closes that bounded slice: make the **RECORDED variance a recorded, additive input to the
do-nothing pricing**, so the Q8/trade-off prices a **projected band** (worst ± recorded variance) rather
than a single point — with the Sprint-22 single-point behavior unchanged (byte-identical default).

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7J.5 (attention), §7K.1
  (Policy, Trade-off, Organizational Learning, Forecast, Decision→Expected→Variance→WHY→change-future-policy),
  §7L (the ten morning questions), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — esp. `_forecast_closure` (Sprint 22: the
    recorded `direction` branch + single-point `worst`/gap/summary + the additive `direction` key), the
    frozen functions (`reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`, `rank`,
    `machine_eligible_best`, `render_tradeoff`, `cockpit_q7q8`), and `forecast_metric` (which already
    returns `recorded_variance` = the last recorded point's `variance`).
  - `run_forecast_direction_demo.py` (Sprint 22 runner — the higher/lower/controls/no-data org set, the
    byte-identical assertions), `run_forecast_action_demo.py` (Sprint 21), `run_forecast_capacity_demo.py`
    (Sprint 20), `adjudication_configs.py` (DELI/COVE + variants).
  - `sprints/sprint-22/{summary.md,notes/findings.md}` + `sprints/sprint-21/{summary.md,notes/findings.md}`
    + `docs/ENGINE-FORECAST-DIRECTION.md` and the Sprint-22 note in `docs/ENGINE-FORECAST-ACTION.md`.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16); additive
  only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get one-arg,
  `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2 RFC3339
  temporal-suffix keys — never name an additive field ending in `at|time|deadline|expires|expiry|effective|
  due|since` — strict C5 tables, `eng.reconcile(sub, cfg)` ARG ORDER, the Sprint-0 venv
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance, runner
  CWD-sensitivity, `[0]`-indexed `parents` for the Sprint-0 path, json round-trip converts `floor_gated`
  sets — restore them, and the Sprint-22 float-vs-int nuance in summary strings: a threshold 16 renders
  "16.0", so keep any string assertions in the runner matching the float rendering).

## What Sprint 23 IS and IS NOT
- **IS:** the Q8/trade-off **do-nothing expected-impact** for a crossing series now prices a **projected
  BAND** derived from the recorded series — `worst` (per the recorded `direction`) and the recorded
  variance (the `recorded_variance` `forecast_metric` already returns, i.e. the last recorded point's
  `variance`) — reported as an honest projected range (`worst − σ … worst + σ`, or `worst ± σ`), with the
  recorded **expected** last value surfaced as the anchor, all from recorded data. When the RANGE crosses
  the threshold (the band, not just the point, is bad), the Q3 attention item and the do-nothing cost
  say so plainly. The additive `variance`/`band` keys ride on the closure, `q8["forecast"]`, and
  `do_nothing_expected_impact`; the Sprint-22 **single-point** fields stay byte-identical by default.
- **IS NOT:** a new service, a new URI noun, a schema/`$defs` edit, a Trust change (S5), a change that lets
  the machine overrule the §6 human; NOT an invented/imaginary variance (only a RECORDED point variance is
  used; a series with NO recorded variance keeps the single-point behavior); NOT a probabilistic/stochastic
  forecast (the variance is a recorded historical spread, used to bound the deterministic projection, NOT a
  confidence interval from a model); NOT a re-implementation of `run_scenario`/`reconcile`/`cockpit_q7q8`;
  NOT any wall-clock/best-guess. No frontier spend.

## The target (what "done" looks like)
1. An additive **recorded-variance band** in `_forecast_closure`: when a recorded series exists and its
   last recorded point carries a `variance`, report `band = {worst, sigma, low, high, crosses}` where
   `worst` is per the recorded `direction`, `sigma` = the recorded variance (a magnitude), `low = worst −
   sigma`, `high = worst + sigma` (numeric, deterministic), and `crosses` = whether the WORST side of the
   band crosses the threshold in the metric's direction (for higher-is-better `low < threshold`; for
   lower-is-better `high > threshold`). The do-nothing summary + the Q3 attention `why` are extended to
   mention the recorded variance/band when present. **A series with NO recorded variance on the last point,
   or no recordable numeric variance, keeps the Sprint-22 single-point output byte-identical.**
2. **Sprint-22 behavior is byte-identical by default:** the two higher-is-better recorded orgs
   (`deli-forecast`/`deli-forecast-flat` — the Sprint-21/22 series each carry a numeric `variance`, so they
   will GAIN the band fields — but the single-point worst/gap/threshold/crossing/on_target/summary-the-portions
   that already exist must remain IDENTICAL; only new additive `variance`/`band` fields + an additive
   summary phrase are added). The no-data `deli` is untouched.
3. A runner (`run_forecast_variance_demo.py`, exit 0 = ALL PASS) that drives ≥4 orgs on fresh Substrates:
   the Sprint-22 `deli-forecast` (higher-is-better deteriorating, recorded variances present), a NEW
   **variance-less control** (a recorded series with NO recorded variance on its points, e.g. `deli-flat2` —
   must stay single-point, no band), the Sprint-22 `deli-cost` (lower-is-better rising, recorded variances
   present → band high above the ceiling prices a worse do-nothing than the single point alone), and the
   no-data `deli`. Asserts: full §7L Q1–Q10 on each; the band is derived ONLY from recorded values (worst,
   recorded variance, threshold; low/high are exact recorded-data arithmetic); on the variance-carrying
   orgs the do-nothing summary surfaces the recorded variance while keeping every pre-existing
   single-point field/branch byte-identical (compare against the Sprint-22 runner's dicts/tests with the
   additive keys ignored); the variance-less control is EXACTLY the single-point output; determinism;
   agreement of the projection used in Q3/Q8 with `forecast_metric` (and its `recorded_variance`); no §6
   overrule (Q8 recommendation unchanged); no wall-clock. Emit fixtures + a report.
4. **Honest docs** (`docs/ENGINE-FORECAST-VARIANCE.md` + an additive note in
   `docs/ENGINE-FORECAST-DIRECTION.md`): the band rule (which recorded variance is used, how `low`/`high`
   are derived, when `crosses` flips, how it is NOT a probability/confidence claim), the honest no-data AND
   no-variance fallback, and a §16-style verdict: does the do-nothing expected-impact now price the
   recorded spread — and what is still not derivable?
5. **Real output:** new runner ALL PASS; full non-regression green; no new noun, 49 `$defs`, SPEC v0.22.

## Mandatory rules
- **Write-first:** `sprints/sprint-23/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is
  `instances/contested_reality/adjudication_engine.py` (extend `_forecast_closure`'s band + summary and
  `render_cockpit_s7l` if needed — do NOT rewrite `reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/
  `_aggregate`/`rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`, frozen). Keep 49 `$defs` +
  URI cap + SPEC v0.22. Re-verify `ros/`, the schema hash (`7fc38c8c…`), and the sector instances
  untouched; the newly rendered lines for the existing recorded orgs must be a strict SUPERSET that
  preserves every pre-existing byte (only ADDITIVE keys/phrases).
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-22 state): `run_forecast_direction_demo.py` (Sprint 22) +
  `run_forecast_action_demo.py` (Sprint 21) + `run_forecast_capacity_demo.py` + the 12 curated C-R
  runners + `run_cockpit_s7l_demo.py`, `conformance_adjudication.py` (16 labels), the 4 prior CR demos +
  conformances, `build_all.py` + `conformance_all.py`, S5 reference + conformance, `agent_demo` +
  conformance.
- New assertions ALL PASS (above). Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema clean.
- **Superset byte-identity:** the two Sprint-22 recorded orgs' pre-existing Q3/Q8/trade-off fields/lines
  unchanged (only new additive `variance`/`band` fields + additive summary phrase added); a no-variance
  control stays exactly single-point; every projection/expected-impact derived from recorded series values +
  recorded variance only (no wall-clock / no invented number).

## Documentation (roll-forward)
- Add `docs/ENGINE-FORECAST-VARIANCE.md`; append a Sprint-23 entry to `instances/README.md`; append an
  "Update after Sprint 23" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`;
  append an additive note to `docs/ENGINE-FORECAST-DIRECTION.md` (and, if useful, `docs/ENGINE-FORECAST-ACTION.md`);
  reference the new build in `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-23/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize what the recorded-variance band reports per org (the recorded
variance source, how `low`/`high`/`crosses` are derived, when it is byte-identical single-point, the honest
no-data AND no-variance fallback, and that this is a recorded-data band, NOT a confidence interval), how it
is generic + additive (recorded `metric://` series + recorded point `variance` + `forecast_metric`'s
`recorded_variance`, no new noun, frozen 49 `$defs`), the ≥4-org proof (variance-carriers vs variance-less
control vs no-data; superset byte-identity), the honest §16 verdict on whether the do-nothing
expected-impact now prices the recorded spread as data where it exists, and the verified build + conformance
commands. Write the **next** sprint's self-contained prompt at `sprints/sprint-24/PROMPT.md`.