# SPRINT 26 — PROMPT (the honest frontier Sprint 25 disclosed: the Q3 forecast-driven attention item still names only the single worst point + single-worst band, and the Q9 capacity-attention is a FLAG that does not yet drive any recorded capacity-planning guidance)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 20–24 built the configurable adjudication engine
(`instances/contested_reality/adjudication_engine.py`) that renders the full §7L Q1–Q10 morning cockpit
for ANY configured org, data-only; Sprint 22 made the crossing direction a recorded additive parameter
(both orientations); Sprint 23 priced the Q8/trade-off do-nothing expected-impact as a projected BAND
(worst ± the recorded variance); Sprint 24 made the band's variance SOURCE a recorded, additive
`band_variance` parameter on the `metric://` object (absent/`"last"` = last point, byte-identical;
`"all"`/`"minmax"` = the recorded whole-series max |variance|) so an org whose spread WIDENED can price
the band from the recorded worst-case spread; Sprint 25 carried the SAME recorded sigma to EVERY
projection period -> additive `band_periods` (`[{period, low, high}]`, each `projected ± sigma`) +
`band_horizon` (`{low: min period low, high: max period high}` — the record-wide whole-horizon worst
case) on the closure, `q8["forecast"]`, and `do_nothing_expected_impact`, and added a Q9
`band_capacity_attention` flag/reason (horizon range vs the recorded threshold; references any
RECORDED capacity without inventing a number).
**Sprint 25's own finding (`sprints/sprint-25/notes/findings.md`, "Open issues / next work") discloses
the next honest frontier: `band_horizon`/`band_periods` are surfaced on Q6/Q8/do-nothing, but the Q3
forecast-driven attention item's `why` still names the SINGLE worst point + the SINGLE-worst band
(Sprint-23/24 shape) — the horizon-wide worst case is not yet named where the human first looks
(Q3). And the Q9 `band_capacity_attention` is a FLAG that does not yet drive any recorded capacity-
planning guidance.** A bounded Sprint 26 slice: make the Q3 forecast-driven attention `why` carry the
recorded horizon-wide worst case as an additive suffix (strict-prefix), so Q3/Q6/Q8/do-nothing all
agree on the horizon-wide band by construction; and — ONLY where the org records a numeric `capacity`
on its authority object — add a data-only capacity-planning attention flag/reason derived from the
recorded band + recorded threshold + recorded capacity (a plain "at-capacity / headroom / deficit"
reason from recorded numbers), never inventing a capacity value. Still recorded-data only.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7J.5 (attention),
  §7K.1 (Policy, Trade-off, Organizational Learning, Forecast, Decision→Expected→Variance→WHY→change-
  future-policy), §7L (the ten morning questions), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — esp. `_forecast_closure` (the Sprint-23 band
    block `rv = _num(fc.get("recorded_variance"))`; the Sprint-24 `band_variance` source selection
    `bv = str(fap_metric.get("band_variance") or "").strip().lower()`, `snap`; `band = {worst, sigma,
    low, high, crosses}`, the additive `source` + `band_variance` keys; the Sprint-25 `band_periods` +
    `band_horizon` computation + the do-nothing summary's additive horizon-wide phrase; the `available:
    False` no-data path) and `cockpit_s7l` (Q6/Q3/Q8 + the Q9 `q9` ownership/capacity block with
    `q9_capacity`/`capacity_recorded` AND the Sprint-25 `band_capacity_attention`), `record_capacity`
    (the recorded additive `capacity` field on the authority:// object Q9 reads), the frozen functions
    (`reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`, `rank`,
    `machine_eligible_best`, `render_tradeoff`, `cockpit_q7q8`, `render_cockpit_s7l`).
  - `run_forecast_horizon_demo.py` (Sprint 25 runner — the ≥5 orgs, the superset byte-identity
    assertions vs the Sprint-23/24 runners' constants), `run_forecast_variance_all_demo.py` (Sprint 24
    runner), `run_forecast_variance_demo.py` (Sprint 23), `run_forecast_direction_demo.py` (Sprint 22),
    `adjudication_configs.py` (DELI/COVE + variants).
  - `sprints/sprint-25/{summary.md,notes/findings.md}` + `sprints/sprint-24/{summary.md,notes/findings.md}`
    + `sprints/sprint-23/{summary.md,notes/findings.md}` + `docs/ENGINE-FORECAST-VARIANCE.md` (the
    Sprint-23 §7 + Sprint-24 §8 + Sprint-25 §9 addenda — note the doc's addendum numbering) +
    `docs/ENGINE-FORECAST-DIRECTION.md` + `docs/ENGINE-FORECAST-ACTION.md` + `docs/ENGINE-FORECAST-CAPACITY.md`
    + `docs/ENGINE-S7L-COCKPIT.md`.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16);
  additive only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get
  one-arg, `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2
  RFC3339 temporal-suffix keys — never name an additive field ending in
  `at|time|deadline|expires|expiry|effective|due|since`, so `band_periods`/`band_horizon`/
  `band_capacity_attention` are fine and any NEW capacity flag key must also avoid those suffixes;
  strict C5 tables, `eng.reconcile(sub, cfg)` ARG ORDER, the Sprint-0 venv
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance, runner
  CWD-sensitivity, `[0]`-indexed `parents`, json round-trip restores `floor_gated` sets, float-vs-int
  rendering in summary strings, and that the band is a RECORDED-DATA spread, NOT a confidence interval).

## What Sprint 26 IS and IS NOT
- **IS:** (1) an additive Q3 forecast-driven attention `why` SUFFIX naming the recorded horizon-wide
  range (`band_horizon`) — appended so the Sprint-23/24/25 single-worst why stays a strict prefix —
  so the human sees the same record-wide worst case at Q3 that Q6/Q8/do-nothing already carry; (2) a
  data-only capacity-planning attention flag/reason on Q9 that, ONLY where the org records a numeric
  `capacity` on its authority object, derives a plain at-capacity / headroom / deficit reason from the
  recorded band + recorded threshold + recorded capacity — a flag/reason, never an invented capacity
  number. Both additive and recorded-data only.
- **IS NOT:** a new service, a new URI noun, a schema/`$defs` edit, a Trust change (S5), a change that
  lets the machine overrule the §6 human; NOT a probabilistic/stochastic forecast or any variability not
  present as a recorded point value; NOT a re-implementation of `run_scenario`/`reconcile`/
  `cockpit_q7q8`; NOT a change to the no-variance / no-data fallback (still byte-identical); NOT a
  fabricated capacity value or a capacity-deficit directive — the capacity-planning line states the
  recorded numbers plainly and labels headroom/deficit as a derived REASON, never as an instruction or
  an invented figure. No frontier spend.

## The target (what "done" looks like)
1. **Q3 attention names the horizon-wide range.** In `_forecast_closure`, when a band exists AND the
   forecast-driven attention item was created, APPEND an additive suffix to `attention_item["why"]`
   that names `band_horizon` (e.g. ` — horizon-wide recorded band {lo}…{hi} across {n} projection
   periods`), appended AFTER the Sprint-23/24/25 single-worst-band phrase so the old `why` stays a
   strict prefix (same prefix-preservation rule the do-nothing summary already uses). No-band / no-data
   orgs: unchanged (no suffix). The do-nothing summary may optionally reuse the same constant so
   Q3/Q8/do-nothing agree verbatim.
2. **Q9 data-only capacity-planning attention.** In `cockpit_s7l`'s Q9 block, ONLY when the org records
   a numeric `capacity` on its authority object (`capacity_recorded` is True) AND a band + numeric
   threshold exist, add an additive **`capacity_planning_attention`** to `q9`:
   `{flag: bool, why: string}` — `flag` = whether the recorded capacity is exceeded by the horizon
   worst case OR the horizon band signals the threshold (choose and document ONE deterministic rule,
   e.g. deficit when the recorded capacity value < the horizon band's worst-side magnitude; headroom
   when it is well above); `why` states the recorded numbers plainly (recorded capacity vs the
   horizon-wide band) and labels headroom vs at-capacity vs deficit as a derived REASON — NEVER a
   fabricated capacity number, NEVER a directive. If no capacity is recorded, no
   `capacity_planning_attention` key (byte-identical). Keep the Sprint-25 `band_capacity_attention`
   flag field intact (additive superset).
3. **A runner (`run_forecast_horizon2_demo.py`, exit 0 = ALL PASS)** that drives the same ≥5 fresh orgs
   shape as Sprint 25 (`deli-forecast`, `deli-varmax`, `deli-varmax-cap` — which RECORDS a capacity,
   `deli-flat2` no-band control, `deli` no-data) and asserts: full Q1–Q10 on each; the Q3 attention why
   KEEPS the Sprint-23/24/25 string as a strict prefix AND now carries the horizon-wide range suffix;
   `deli-varmax-cap`'s Q9 gains `capacity_planning_attention` whose `why` states the recorded capacity
   (500.0 resolutions/day, load 0.72) + the horizon band and labels headroom/deficit from recorded
   numbers only; the other orgs carry NO `capacity_planning_attention` key (byte-identical superset);
   `band_periods`/`band_horizon`/`band_capacity_attention` still present and unchanged; determinism; no
   §6 overrule (Q8 recommendation unchanged); no wall-clock / no invented number. Emit fixtures + report.
4. **Honest docs** — additive note in `docs/ENGINE-FORECAST-ACTION.md` (Q3 attention) and
   `docs/ENGINE-FORECAST-CAPACITY.md` (Q9 capacity-planning): the Q3 why now names the horizon-wide
   range (strict prefix), the capacity-planning flag/reason is a derived REASON from recorded numbers
   (never an invented capacity value), the byte-identical default, and the honest no-variance / no-data
   fallback. Extend the §16 verdict: does Q3 + Q9 now carry the recorded whole-horizon worst case as
   data where it exists, and is capacity attention a data-only reason, not a fabricated figure?
5. **Real output:** new runner ALL PASS; full non-regression green; no new noun, 49 `$defs`, SPEC v0.22.

## Mandatory rules
- **Write-first:** `sprints/sprint-26/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is
  `instances/contested_reality/adjudication_engine.py` (extend `_forecast_closure`'s Q3-attention-why
  block + `cockpit_s7l`'s Q9 block; keep the frozen functions untouched). Keep 49 `$defs` + URI cap +
  SPEC v0.22. Re-verify `ros/`, the schema hash (`7fc38c8c…`), and the sector instances untouched; the
  default orgs' output must be a strict SUPERSET of Sprint 25 preserving every pre-existing byte.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-25 state): `run_forecast_horizon_demo.py` +
  `run_forecast_variance_all_demo.py` + `run_forecast_variance_demo.py` + `run_forecast_direction_demo.py`
  + `run_forecast_action_demo.py` + `run_forecast_capacity_demo.py` + the 12 curated C-R runners +
  `run_cockpit_s7l_demo.py`, `conformance_adjudication.py` (16 labels), the 4 prior CR conformances,
  `build_all.py` + `conformance_all.py`, S5 reference + conformance, `agent_demo`.
- New assertions ALL PASS (above). Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema
  clean; template hash `7fc38c8c…`.
- **Superset byte-identity:** the Sprint-23/24/25 variance-carrying orgs (`deli-forecast`, `deli-varmax`,
  `deli-cost`, and now `deli-varmax-cap`) and the variance-less control + no-data org unchanged except
  for the additive Q3-attention-`why` suffix and, on the capacity-recording org only,
  `capacity_planning_attention`. Every new value derived from recorded series values + recorded variance
  + recorded capacity only.

## Documentation (roll-forward)
- Additive note in `docs/ENGINE-FORECAST-ACTION.md` + `docs/ENGINE-FORECAST-CAPACITY.md`; append a
  Sprint-26 entry to `instances/README.md`; append an "Update after Sprint 26" note to
  `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; reference the new build in
  `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-26/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize, per org, the Q3-attention horizon-wide suffix + the Q9
capacity-planning flag/reason (which recorded numbers became the reason, when the org records a
capacity vs when it does not, the byte-identical default), that this is generic + additive (recorded
`metric://` series + recorded point-`variance` values + the recorded `band_variance` source + a
recorded authority `capacity`; no new noun, frozen 49 `$defs`), the ≥4-org proof (default byte-identity
vs a widening whole-series org vs a capacity-recording org vs variance-less control vs no-data), the
honest §16 verdict on whether Q3 + Q9 capacity attention now carry the recorded whole-horizon worst case
as data where it exists and whether capacity planning is a data-only REASON not a fabricated figure — and
what is still not derivable — and the verified build + conformance commands. Write the **next** sprint's
self-contained prompt at `sprints/sprint-27/PROMPT.md`.