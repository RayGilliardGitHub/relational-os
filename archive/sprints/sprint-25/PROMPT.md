# SPRINT 25 — PROMPT (the honest frontier Sprint 24 disclosed: the recorded whole-series band still prices only the SINGLE worst projected point; it does not carry the band across ALL projection periods or onto Q9 capacity)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 20–24 built the configurable adjudication engine (`instances/contested_reality/
adjudication_engine.py`) that renders the full §7L Q1–Q10 morning cockpit for ANY configured org,
data-only; Sprint 22 made the crossing direction a recorded additive parameter (both orientations);
Sprint 23 priced the Q8/trade-off do-nothing expected-impact as a projected BAND (worst ± the recorded
variance); Sprint 24 made the band's variance SOURCE a recorded, additive `band_variance` parameter on
the `metric://` object (absent/`"last"` = the last point's variance, byte-identical to Sprint 23;
`"all"`/`"minmax"` = the recorded whole-series max |variance| across the recorded points) so an org
whose spread WIDENED over time can price the band from the recorded worst-case spread.
**Sprint 24's own finding (`sprints/sprint-24/notes/findings.md`, "Open issues / next work") discloses
the next honest frontier: the projected BAND is still computed around the SINGLE worst projected point
at the do-nothing line — it does not aggregate a band across ALL projection periods (the whole horizon's
worst-case spread), and it does not feed §7L Q9 capacity attention.** Sprint 25 closes that bounded
slice: make the do-nothing price + a Q9 capacity-attention signal carry the horizon-wide recorded
worst-case (the recorded band applied to every projection period, not just the single worst), still
recorded-data only, no invented number.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7J.5 (attention), §7K.1
  (Policy, Trade-off, Organizational Learning, Forecast, Decision→Expected→Variance→WHY→change-future-policy),
  §7L (the ten morning questions), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — esp. `_forecast_closure` (the Sprint-23 band
    block: `rv = _num(fc.get("recorded_variance"))`; the Sprint-24 `band_variance` source selection
    `bv = str(fap_metric.get("band_variance") or "").strip().lower()`, `snap`; `band = {worst, sigma,
    low, high, crosses}`, the additive `source` + `band_variance` keys, the summary + attention-`why`
    band phrases, and the `available: False` no-data path), `cockpit_s7l` (Q6/Q3/Q8 + the Q9 `q9`
    ownership/capacity block with `q9_capacity`/`capacity_recorded`), `record_capacity` (the recorded
    additive `capacity` field on the authority:// object Q9 reads), the frozen functions
    (`reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`, `rank`,
    `machine_eligible_best`, `render_tradeoff`, `cockpit_q7q8`).
  - `run_forecast_variance_all_demo.py` (Sprint 24 runner — the ≥4 orgs, the superset byte-identity
    assertions vs the Sprint-23 runner's constants), `run_forecast_variance_demo.py` (Sprint 23),
    `run_forecast_direction_demo.py` (Sprint 22), `adjudication_configs.py` (DELI/COVE + variants).
  - `sprints/sprint-24/{summary.md,notes/findings.md}` + `sprints/sprint-23/{summary.md,notes/findings.md}`
    + `docs/ENGINE-FORECAST-VARIANCE.md` (the Sprint-24 §7 addendum) + `docs/ENGINE-FORECAST-DIRECTION.md`
    + `docs/ENGINE-FORECAST-CAPACITY.md` + `docs/ENGINE-S7L-COCKPIT.md`.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16);
  additive only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get
  one-arg, `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2
  RFC3339 temporal-suffix keys — never name an additive field ending in
  `at|time|deadline|expires|expiry|effective|due|since` (so `band_variance` is fine, `variance_at` is
  not); strict C5 tables, `eng.reconcile(sub, cfg)` ARG ORDER, the Sprint-0 venv
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance, runner
  CWD-sensitivity, `[0]`-indexed `parents`, json round-trip restores `floor_gated` sets, float-vs-int
  rendering in summary strings (a threshold 16 renders "16.0"), and that the band is a RECORDED-DATA
  spread, NOT a confidence interval).

## What Sprint 25 IS and IS NOT
- **IS:** a recorded-data horizon-wide do-nothing price + a Q9 capacity-attention signal that apply
  the recorded band spread to EVERY projection period (a per-period low/high from the same recorded
  sigma), not only the single worst point; reported additively. The whole-horizon worst-case (the
  record-wide low and high across ALL periods) becomes the explicit do-nothing range, still derived
  ONLY from recorded series values + the recorded `band_variance` source (last-point or whole-series),
  + the recorded threshold. Every projected value and every band bound stays a pure function of the
  recorded points + the recorded source — no invented number, no cross-period aggregation that
  produces a non-recorded sigma.
- **IS NOT:** a new service, a new URI noun, a schema/`$defs` edit, a Trust change (S5), a change that
  lets the machine overrule the §6 human; NOT a probabilistic/stochastic forecast or any variability
  not present as a recorded point value; NOT a re-implementation of `run_scenario`/`reconcile`/
  `cockpit_q7q8`; NOT a change to the no-variance / no-data fallback (still byte-identical single-point
  / unchanged); NOT a Q9 capacity NUMBER that the engine invents (any Q9 capacity-attention must be a
  flag/reason derived from the recorded band + the recorded threshold, never a fabricated capacity
  value). No frontier spend.

## The target (what "done" looks like)
1. **Horizon-wide band on the do-nothing price.** In `_forecast_closure`'s band block, when a band
   exists (recorded variance + a recorded `band_variance` source), ADD additive keys carrying the
   per-period band across the projection horizon AND the record-wide range:
   - `band_periods = [{period, low, high}]` — for EVERY projection period, the same recorded sigma
     applied to that period's projected value (`low = projected − sigma`, `high = projected + sigma`);
   - `band_horizon = {low: min(period lows), high: max(period highs)}` — the record-wide worst-case
     range across ALL periods (still only from recorded values + the recorded sigma);
   - `do_nothing_expected_impact` and `q8["forecast"]` carry these additive keys; the do-nothing
     summary appends an additive phrase naming the horizon-wide range (old single-worst band string
     stays a strict prefix). The single-worst `band` field (Sprint-23/24) is UNCHANGED — additive only.
2. **Q9 capacity-attention from the recorded band.** In `cockpit_s7l`'s Q9 block, when a band exists
   AND the recorded threshold is numeric, ADD an additive `band_capacity_attention` field to `q9`:
   `{flag: bool, why: string, low/high/crosses}` that says whether the record-wide HORIZON range (or,
   if a recorded capacity exists, whether the projection's worst side still crosses) signals the
   recorded threshold — a data-only attention/flag for capacity, NEVER an invented capacity number.
   Official policy: if the org records a `capacity` on its authority object (Sprint 20), the Q9
   `band_capacity_attention.why` can reference the recorded capacity but must NOT invent/mutate it;
   if none, the flag is still derivable from the recorded band + threshold alone. No-data / no-band
   orgs: no `band_capacity_attention` key (byte-identical).
3. **A runner (`run_forecast_horizon_demo.py`, exit 0 = ALL PASS)** that drives ≥4 fresh orgs: the
   Sprint-24 `deli-varmax` (whole-series `band_variance:"all"`, band 0.62…0.98) — asserted to ALSO
   carry the new `band_periods`/`band_horizon` (horizon-wide high > the single-worst high because an
   EARLIER period's projected value at `worst + sigma` can exceed the single-worst point's band when
   the horizon trends), the Sprint-23 `deli-forecast` (last-point default — horizon-wide still a pure
   per-period band), the no-band control `deli-flat2` (recorded series, NO variance — NO new keys,
   byte-identical to Sprint-22 single-point), and the no-data `deli`. Asserts:
   full Q1–Q10 on each; `band_periods` = [period → projected ± recorded sigma] EXACT arithmetic;
   `band_horizon.low/high` = min/max over those periods (recorded-data only); `sigma` is STILL exactly
   one of the recorded point |variance| magnitudes (a pure function of the `points` list + the recorded
   source, never invented); the default orgs are byte-identical to Sprint 23/24 except for the additive
   `band_periods`/`band_horizon`/`band_capacity_attention` keys (every pre-existing field preserved);
   determinism; no §6 overrule (Q8 recommendation unchanged); no wall-clock. Emit fixtures + a report.
4. **Honest docs** — an additive note in `docs/ENGINE-FORECAST-VARIANCE.md` (and the capacity doc if
   useful): the horizon-wide band is a per-period application of the SAME recorded sigma (a recorded
   spread, not a new model), when the band_horizon WIDENS beyond the single-worst point and why that
   is still a recorded-data spread not a confidence interval, the byte-identical default, and the
   honest no-variance / no-data fallback. Extend the §16 verdict: does the do-nothing + capacity
   attention now carry the recorded whole-horizon worst-case as data where it exists?
5. **Real output:** new runner ALL PASS; full non-regression green; no new noun, 49 `$defs`, SPEC v0.22.

## Mandatory rules
- **Write-first:** `sprints/sprint-25/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is
  `instances/contested_reality/adjudication_engine.py` (extend `_forecast_closure`'s band block to add
  the horizon-wide keys + `cockpit_s7l`'s Q9 block to add `band_capacity_attention`; keep the frozen
  functions untouched). Keep 49 `$defs` + URI cap + SPEC v0.22. Re-verify `ros/`, the schema hash
  (`7fc38c8c…`), and the sector instances untouched; the default orgs' output must be a strict SUPERSET
  of Sprint 23/24 preserving every pre-existing byte.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-24 state): `run_forecast_variance_all_demo.py` + `run_forecast_variance_demo.py`
  + `run_forecast_direction_demo.py` + `run_forecast_action_demo.py` + `run_forecast_capacity_demo.py`
  + the 12 curated C-R runners + `run_cockpit_s7l_demo.py`, `conformance_adjudication.py` (16 labels),
  the 4 prior CR conformances, `build_all.py` + `conformance_all.py`, S5 reference + conformance,
  `agent_demo`.
- New assertions ALL PASS (above). Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema
  clean; template hash `7fc38c8c…`.
- **Superset byte-identity:** the Sprint-23/24 variance-carrying orgs (`deli-forecast`, `deli-varmax`,
  `deli-cost`) and the variance-less control + no-data org unchanged except for the additive
  `band_periods`/`band_horizon` (when a band exists) and `band_capacity_attention` (when a band +
  threshold exist). Every new value derived from recorded series values + a recorded variance only.

## Documentation (roll-forward)
- Additive note in `docs/ENGINE-FORECAST-VARIANCE.md`; append a Sprint-25 entry to `instances/README.md`;
  append an "Update after Sprint 25" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`;
  reference the new build in `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-25/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize, per org, the horizon-wide band source and why (which recorded
value became `sigma`, how `band_periods`/`band_horizon` are derived, when `band_horizon` WIDENS beyond
the single-worst band, the byte-identical default + capacity-attention flag), that this is generic +
additive (recorded `metric://` series + recorded point-`variance` values + the recorded `band_variance`
source, no new noun, frozen 49 `$defs`), the ≥4-org proof (default byte-identity vs a widening
whole-series org vs variance-less control vs no-data), the honest §16 verdict on whether the do-nothing
price + Q9 capacity-attention now carry the recorded whole-horizon worst-case as data where it exists —
and what is still not derivable — and the verified build + conformance commands. Write the **next**
sprint's self-contained prompt at `sprints/sprint-26/PROMPT.md`.