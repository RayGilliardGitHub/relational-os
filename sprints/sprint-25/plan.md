# SPRINT 25 — PLAN: horizon-wide do-nothing band + Q9 capacity-attention

## Objective
Close Sprint 24's disclosed frontier (sprints/sprint-24/notes/findings.md, "Open issues / next
work"): the do-nothing projected BAND is still computed around the SINGLE worst projected point; it
does not carry the recorded band across ALL projection periods (the whole-horizon worst case), and it
does not feed §7L Q9 capacity attention. Sprint 25 makes the do-nothing price + a Q9 capacity-attention
signal carry the **horizon-wide recorded worst-case** — the recorded band (same recorded sigma) applied
to every projection period — additively, recorded-data only, no invented number.

## Accepted scope (normalized from the prompt)
- **IS:** additive `band_periods` (per-period low/high from the same recorded sigma on every projected
  value) + `band_horizon` (record-wide min-low / max-high) on the closure, `q8["forecast"]`,
  `do_nothing_expected_impact`; an additive do-nothing summary phrase naming the horizon-wide range
  (old single-worst band string stays a strict prefix); an additive `band_capacity_attention`
  flagged/reasoned Q9 signal derived from the horizon range + recorded threshold (referencing any
  RECORDED capacity without inventing it). `sigma` is STILL exactly a recorded point |variance|
  magnitude.
- **IS NOT:** new service/noun/schema/$defs; S5/Trust change; §6 overrule; stochastic/probabilistic
  forecast; re-implementation of frozen functions; a change to the no-variance/no-data fallback
  (still byte-identical single-point/unchanged); a fabricated Q9 capacity number.

## Frozen functions (must NOT touch)
`reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`, `rank`, `machine_eligible_best`,
`render_tradeoff`, `cockpit_q7q8`, `cockpit_s7l`, `render_cockpit_s7l`, `forecast_metric`,
`record_metric_series`, `record_capacity`, `emit_fixtures`. ONLY `_forecast_closure`'s band block and
`cockpit_s7l`'s Q9 block in `instances/contested_reality/adjudication_engine.py` are extended.

## Numbered sub-sprints
1. **Build (engine).** In `_forecast_closure`, inside the existing `if src_variance is not None:` band
   block, compute `band_periods = [{period, low, high}]` over every `fc["projections"]` period
   (`low = projected − sigma`, `high = projected + sigma`, 4dp) and
   `band_horizon = {low: min(period lows), high: max(period highs)}`. Ride them additively on `res`,
   `res["forecast"]`, `do_nothing` (only when `band is not None`, so no-variance/no-data orgs stay
   byte-identical). Append an additive horizon-wide phrase to the do-nothing summary (prefix property).
   Then in `cockpit_s7l`'s Q9 block, when a band exists AND the recorded threshold is numeric, add
   `q9["band_capacity_attention"] = {flag, why, low, high, crosses}` derived only from the horizon
   range + recorded threshold (+ an optional reference to the recorded capacity, never invented).
   No-band/no-data orgs carry NO key.
2. **Build (runner).** New `instances/contested_reality/run_forecast_horizon_demo.py`, exit 0 = ALL
   PASS, drives ≥4 fresh orgs: `deli-forecast` (Sprint-23 default last-point band — byte-identical
   superset, now with band_periods/band_horizon/band_capacity_attention), `deli-varmax`
   (whole-series `band_variance:"all"`, band 0.62…0.98 — asserted to carry band_periods/band_horizon
   with horizon-wide high 1.02 > single-worst high 0.98), a 5th fresh org `deli-varmax-cap` (same
   whole-series band + a recorded capacity, to prove the why references capacity without inventing it),
   `deli-flat2` (no-band control — NO new keys, byte-identical single-point), `deli` (no-data —
   unchanged). Asserts: full Q1–Q10; band_periods EXACT arithmetic; band_horizon = min/max of periods;
   sigma is a recorded point |variance|; default orgs byte-identical superset (only additive keys);
   determinism; no §6 overrule (Q8 recommendation unchanged); no wall-clock. Emits fixtures + a report.
3. **Verify (green).** New runner ALL PASS; full non-regression: all forecast/adj runners, the 4 prior
   CR conformances + `conformance_adjudication` (16 labels), `build_all` + `conformance_all`, S5
   reference + conformance, agent demo; SPEC v0.22, 49 `$defs`, schema hash `7fc38c8c…`, `ros/` +
   sector instances untouched.
4. **Docs roll-forward.** Additive §8 addendum in `docs/ENGINE-FORECAST-VARIANCE.md` (+ the capacity doc
   if useful); `instances/README.md` Sprint-25 entry; STRESS-TEST-SCENARIOS "Update after Sprint 25"
   note; `sprints/sprint-25/summary.md` + `notes/findings.md`.
5. **Hand-off.** Write `sprints/sprint-26/PROMPT.md`.

## Definition of Done
- `run_forecast_horizon_demo.py` -> **ALL PASS**, exit 0.
- Superset byte-identity: the Sprint-23/24 variance-carrying orgs (`deli-forecast`, `deli-varmax`,
  `deli-cost`) and variance-less control + no-data org unchanged EXCEPT for the additive
  `band_periods`/`band_horizon` (when a band exists) and `band_capacity_attention` (when a band +
  threshold exist). Every new value derived from recorded series values + recorded variance only.
- Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema clean; template hash `7fc38c8c…`.
- Honest §16 verdict documented.

## Exit criteria
- No new noun; URI cap respected; frozen functions byte-identical; C2 temporal-suffix probe unharmed
  (new keys: `band_periods`, `band_horizon`, `band_capacity_attention` — none carry
  `at|time|deadline|expires|expiry|effective|due|since`).
- Raymond: clean English, `file://` paths, status at each long step.