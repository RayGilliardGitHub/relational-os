# SPRINT 24 — PROMPT (the honest frontier Sprint 23 disclosed: the recorded-variance band uses only the LAST recorded point's variance, collapsing any whole-series recorded spread)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 20–23 built the configurable adjudication engine (`instances/contested_reality/
adjudication_engine.py`) that renders the full §7L Q1–Q10 morning cockpit for ANY configured org,
data-only; Sprint 22 made the crossing direction a recorded, additive parameter (both orientations);
Sprint 23 made the RECORDED variance a recorded, additive input to the Q8/trade-off do-nothing pricing
so a crossing series prices a projected BAND (worst ± the recorded variance) instead of a single point.
**Sprint 23's own finding (`sprints/sprint-23/notes/findings.md`, "Open issues / next work") discloses
the next honest frontier: the band uses ONLY the LAST recorded point's `variance` — a series whose
RECORDED `variance` changed across its points (widened or narrowed spread) is collapsed to the final
variance in the band, ignoring the recorded whole-series spread.** Sprint 24 closes that bounded slice:
make the band's variance source a **recorded, additive parameter** on the `metric://` object — the
last point's variance (today's Sprint-23 default, byte-identical) vs a recorded WHOLE-SERIES choice —
so the do-nothing band can be priced from the recorded worst-case spread where the org records it,
still recorded-data only, no invented number.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7J.5 (attention), §7K.1
  (Policy, Trade-off, Organizational Learning, Forecast, Decision→Expected→Variance→WHY→change-future-policy),
  §7L (the ten morning questions), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — esp. `_forecast_closure`'s Sprint-23 band
    block (`rv = _num(fc.get("recorded_variance"))`; `sigma = abs(rv)`; `low`/`high`; `crosses`; the
    additive `band`/`recorded_variance`/`expected_last` keys; the summary + attention-`why` band
    phrases), `forecast_metric` (which returns `recorded_variance` = the last point's `variance` and
    the whole `points` list on the object), `_recorded_metric_with_series`, `render_cockpit_s7l` (the
    additive Q8 band suffix), and the frozen functions (`reconcile`, `run_scenario`, `_derive`,
    `SPEC_VOCAB`, `_aggregate`, `rank`, `machine_eligible_best`, `render_tradeoff`, `cockpit_q7q8`).
  - `run_forecast_variance_demo.py` (Sprint 23 runner — the ≥4 orgs, the superset byte-identity
    assertions), `run_forecast_direction_demo.py` (additive-aware, Sprint 22), `run_forecast_action_demo.py`
    (Sprint 21), `adjudication_configs.py` (DELI/COVE + variants).
  - `sprints/sprint-23/{summary.md,notes/findings.md}` + `sprints/sprint-22/{summary.md,notes/findings.md}`
    + `docs/ENGINE-FORECAST-VARIANCE.md` + `docs/ENGINE-FORECAST-DIRECTION.md` (+ its Sprint-23 note).
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16);
  additive only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get
  one-arg, `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2
  RFC3339 temporal-suffix keys — never name an additive field ending in
  `at|time|deadline|expires|expiry|effective|due|since` (so `band_variance` is fine, `variance_at`
  is not); strict C5 tables, `eng.reconcile(sub, cfg)` ARG ORDER, the Sprint-0 venv
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance, runner
  CWD-sensitivity, `[0]`-indexed `parents`, json round-trip restores `floor_gated` sets, float-vs-int
  rendering in summary strings (a threshold 16 renders "16.0" — keep string assertions matching the
  float rendering), and that the band is a RECORDED-DATA spread, NOT a confidence interval).

## What Sprint 24 IS and IS NOT
- **IS:** a recorded, additive **band-variance source** on the `metric://` object that lets a series
  price the do-nothing band from a recorded **whole-series** variance instead of only the last point.
  Additive field (e.g. `band_variance`) with at least: the last-point default (keep) and a recorded
  whole-series choice (e.g. `"all"` = the largest recorded |variance| across the recorded points, or
  `"minmax"`). When `band_variance` records a whole-series choice, the band's `sigma` is that recorded
  whole-series magnitude (still from recorded point `variance` values ONLY), the band is re-derived
  (low/high/crosses from the new sigma, where worst + recorded threshold are unchanged), and the
  summary/attention-why name the source honestly. The default (last point) is **byte-identical to
  Sprint 23**. No invented number — every possible sigma is a recorded point variance magnitude.
- **IS NOT:** a new service, a new URI noun, a schema/`$defs` edit, a Trust change (S5), a change that
  lets the machine overrule the §6 human; NOT a probabilistic/stochastic forecast or any variance not
  present as a recorded point value; NOT a re-implementation of `run_scenario`/`reconcile`/
  `cockpit_q7q8`; NOT any wall-clock; NOT a change to the no-variance/no-data fallback (still
  byte-identical single-point / unchanged). No frontier spend.

## The target (what "done" looks like)
1. A recorded, additive `band_variance` parameter on the `metric://` object that selects the band's
   variance source: absent / `"last"` → the last recorded point's `variance` (Sprint-23 default,
   byte-identical); `"all"` → the LARGEST |recorded variance| across the recorded points;
   `"minmax"` → the recorded min–max spread (`max(|v|)`, or a defined recorded whole-series rule).
   `band = {worst, sigma, low, high, crosses, source}` where `source` names the recorded source
   (`"last-point"` vs the whole-series choice), `sigma` = the selected recorded magnitude, low/high =
   worst ± sigma, crosses as in Sprint 23 (worst side vs threshold in the metric's direction). All
   additive; the default path emits NO `source` change / byte-identical to Sprint 23 (verify against
   the Sprint-23 runner with the additive key ignored).
2. **Sprint-23 behavior byte-identical by default**: the two variance-carrying orgs
   (`deli-forecast`, `deli-cost`) do NOT record `band_variance` → they keep the exact Sprint-23
   last-point band + summary + attention-why; only a NEW whole-series org (that records
   `band_variance: "all"` on a series whose |variance| INCREASED over time) prices a WIDER band from
   the largest recorded |variance|; the variance-less control + no-data org stay byte-identical.
3. A runner (`run_forecast_variance_all_demo.py`, exit 0 = ALL PASS) that drives ≥4 fresh orgs: the
   Sprint-23 `deli-forecast` (no `band_variance` → byte-identical to Sprint 23, asserted against
   `run_forecast_variance_demo.py`'s dicts with the additive `source` key ignored), a NEW **widening
   whole-series org** (`deli-varmax`, records `band_variance: "all"`, last-|variance| small but an
   EARLIER recorded |variance| larger → band HIGH > the Sprint-23 last-point high, sigma = the largest
   recorded |variance|, cross can flip when that wider band crosses the threshold), the Sprint-22
   `deli-cost` (no `band_variance` → byte-identical to Sprint 23), and the no-data `deli`. Asserts:
   full Q1–Q10 on each; the source selection is recorded-data-only (sigma is exactly one of the
   recorded point variances — a pure function of the `points` list, never invented); the default orgs
   are byte-identical to Sprint 23 (every pre-existing field/string preserved; only the additive
   `source` key added); the whole-series org's sigma == the recorded max |variance| and its band
   low/high/crosses are exact recorded-data arithmetic; determinism; agreement with `forecast_metric`
   (its `recorded_variance` == last point) and the hand-computed whole-series max; no §6 overrule (Q8
   recommendation unchanged); no wall-clock. Emit fixtures + a report.
4. **Honest docs** — an additive note in `docs/ENGINE-FORECAST-VARIANCE.md` (and the direction note if
   useful): the recorded `band_variance` choices, which recorded value selects each sigma, when the
   band WIDENS (a recorded earlier spread larger than the last point) and why that is still a
   recorded-data spread not a confidence interval, the byte-identical default, and the honest
   no-variance/no-data fallback. Extend the §16 verdict: does the band now price the recorded
   worst-case whole-series spread where the org records it?
5. **Real output:** new runner ALL PASS; full non-regression green; no new noun, 49 `$defs`, SPEC v0.22.

## Mandatory rules
- **Write-first:** `sprints/sprint-24/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is
  `instances/contested_reality/adjudication_engine.py` (extend `_forecast_closure`'s band block to
  read the recorded `band_variance` source + select sigma + emit the additive `source`; keep the
  frozen functions untouched). Keep 49 `$defs` + URI cap + SPEC v0.22. Re-verify `ros/`, the schema
  hash (`7fc38c8c…`), and the sector instances untouched; the default orgs' output must be a strict
  SUPERSET of Sprint 23 preserving every pre-existing byte.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-23 state): `run_forecast_variance_demo.py` (Sprint 23) +
  `run_forecast_direction_demo.py` + `run_forecast_action_demo.py` + `run_forecast_capacity_demo.py` +
  the 12 curated C-R runners + `run_cockpit_s7l_demo.py`, `conformance_adjudication.py` (16 labels),
  the 4 prior CR conformances, `build_all.py` + `conformance_all.py`, S5 reference + conformance,
  `agent_demo`.
- New assertions ALL PASS (above). Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema
  clean; template hash `7fc38c8c…`.
- **Superset byte-identity:** the Sprint-23 variance-carrying orgs (deli-forecast, deli-cost) and the
  variance-less control + no-data org unchanged (only the additive `source` key added to the band on
  the whole-series orgs; the default no-`band_variance` orgs' band has no `source` — decide whether to
  emit `source` always or only on whole-series, and keep the DEFAULT byte-identical by emitting
  `source` only when the recorded whole-series choice is active). Every projection/band value derived
  from recorded series values + a recorded variance only.

## Documentation (roll-forward)
- Additive note in `docs/ENGINE-FORECAST-VARIANCE.md`; append a Sprint-24 entry to `instances/README.md`;
  append an "Update after Sprint 24" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`;
  reference the new build in `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-24/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize, per org, the recorded band-variance source and why (which
recorded value became `sigma`, how `low`/`high`/`crosses`/`source` are derived, when the band WIDENS
vs the Sprint-23 last-point default, when it is byte-identical), that this is generic + additive
(recorded `metric://` series + recorded point-`variance` values + the recorded `band_variance` source,
no new noun, frozen 49 `$defs`), the ≥4-org proof (default byte-identity vs a widening whole-series
org vs variance-less control vs no-data), the honest §16 verdict on whether the do-nothing band now
prices the recorded worst-case whole-series spread as data where it exists — and what is still not
derivable — and the verified build + conformance commands. Write the **next** sprint's self-contained
prompt at `sprints/sprint-25/PROMPT.md`.