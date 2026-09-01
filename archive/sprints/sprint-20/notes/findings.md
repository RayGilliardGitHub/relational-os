# Sprint 20 — findings

Date: 2026-09-01. Sprint: make the §7L Q6 forecast and Q9 capacity answered AS DATA for a generically-driven
org that records the missing data additively on its own graph/ledger.

## What was already true (baseline, prior Sprints)
- Sprint 19 rendered the full §7L Q1–Q10 morning cockpit for ANY configured org inside the generic engine
  (`adjudication_engine.cockpit_s7l`/`render_cockpit_s7l`, data-only), but its own findings ("Residual
  seams") were explicit that **Q6 cannot forecast** on the adjudication orgs (none records a
  realized-vs-expected series) and **Q9 "capability"** is the holder-of-authority assignment, not a capacity
  number.
- The reference sector BI *does* record the forecast pattern (`ros/bol.py` `metric_loop` + `metric://`
  objects with `target`/`actual`/`variance`/`forecast`); the reference cockpit answers Q6 with a BI
  projection. That RECORDED pattern is what Sprint 20 reuses at the adjudication-engine layer.

## Decisions taken
- **Q6 / Q9 become recorded-data reads, with an honest no-data fallback.** `cockpit_s7l.q6` now locates a
  recorded `metric://` realized-vs-expected series (`_recorded_metric_with_series`) and, when one exists,
  projects deterministically via a new `forecast_metric(cfg, sub, metric_uri, *, horizon)` from ONLY the
  recorded values (last recorded `actual` + mean of recorded consecutive deltas, forward periods, labelled a
  projection). `.q9` reads an additive `capacity` field (`{value, unit, load, status}`) on the `authority://`
  object the question reads; when absent, the existing no-capability fallback is unchanged.
- **Replayable recorders.** `record_metric_series` and `record_capacity` append the missing data to the
  org's own immutable ledger as ONE signed event each (merge-not-replace, §2 preserve-unknown) — the same
  additivity discipline as `reconcile_learning.record_realized_outcome`. No new noun, no schema edit.
- **New-org proof.** The runner clones `deli` onto a clean `deli-forecast` namespace (deep copy via json +
  `://deli/`→`://deli-forecast/` relabel, so it owns its own `authority://deli-forecast/adjudicate`), runs the
  generic lifecycle, then RECORDS the metric series + capacity on THAT org's ledger. `deli` (no data) is the
  honest-fallback control. Both still render the full §7L Q1–Q10.

## The deterministic projection rule (state it plainly)
From a recorded `metric://` `points` list: `last_actual` = last point's `actual`; `mean_delta` = mean of
consecutive actual deltas (0 when one point); `projected(f)` = `round(last_actual + mean_delta * f, 4)` for
`f in 1..horizon`; the last recorded `variance` is shown alongside; the result is a projection, never an
outcome. No wall-clock anywhere. The runner proves the projection equals the hand-computed values
(`[0.84, 0.82, 0.8]` from last 0.86 / mean −0.02 / horizon 3) and that `forecast_metric` is pure on re-call.

## Assumptions that mattered
- **Q6 "over the period"** means the recorded series as found on the graph — the engine does not manage
  series append, it reads what the org recorded. This is the same "reports the recorded state" stance as
  Sprint 19.
- **Capacity is an additive field on the `authority://` object** the Q9 question reads (not an `authority`-owned
  sub-noun, not a `capacity://` scheme). It is data; the engine reads it. The reference sector's
  `assigned_capacity`/`capacity 1.0` is a sector-side additive field on `task://`; the adjudication row places
  the capacity on the authority so `q9` (which reads the authority holder) can report it.
- The new org is a config clone (pure data), mirroring the existing `org_under_library_rule`/`inspect_batch`
  reuse idiom — `floor_gated` must be restored to a `set` after the json round-trip (the engine's `in` check
  expects a set).

## Corrections / guardrails
- **`floor_gated` is a `set`** and `json.dumps` rejects sets — the relabel helper serializes sets as sorted
  lists and restores the set after the round-trip (found in the first run).
- **Sprint-0 conformance cannot be imported inside a plain-`python3` runner** (it needs the venv's
  `jsonschema`/`referencing`/`yaml`). The runner therefore asserts the recorded data landed on the org's own
  fixtures (metric series on the ledger + capacity on the `authority://` component) and the C1–C5 proof is a
  separate Sprint-0-venv command over `fixtures/deli-forecast` (ALL PASS, 49 `$defs`).
- **`emit_fixtures` has no `metric://` group**, so the adjudication fixtures carry the metric series only in
  `ledger/ledger.json` (validated by C3), not a separate `metrics.json` (the reference sector writes
  `s5/metrics.json`; the adjudication emitter does not). The capacity field is on `actors_offers.json`
  (C2-validated). Both are within the design; no emit path was rewritten.
- **C2 temporal-suffix trap respected**: metric `points` keys (`period`/`target`/`expected`/`actual`/
  `variance`) and the capacity keys (`value`/`unit`/`load`/`status`) never end in `at|time|deadline|expires|…`,
  so the capability fixture passes C2 (proved: 26 instances validated).
- The only engine change is the append (`forecast_metric`, `_recorded_metric_with_series`,
  `record_metric_series`, `record_capacity`) + the in-place `.q6`/`.q9` + render-line extensions; frozen
  functions untouched. `deli`/`cove` byte-identical up to the clock (engine demo run twice, timestamp keys
  stripped → identical).

## What the sprint gained
- `forecast_metric` + `_recorded_metric_with_series` + `record_metric_series` + `record_capacity` (append);
  `cockpit_s7l.q6`/`.q9` + `render_cockpit_s7l` now answer Q6/Q9 from recorded data where it exists.
- `run_forecast_capacity_demo.py` (exit 0) drives ≥2 orgs, asserts full §7L, deterministic forecast, capacity
  read-back, agreement with the recorded graph, no wall-clock, and the honest fallback; the new-org fixtures
  pass Sprint-0 C1–C5.
- Docs: `docs/ENGINE-FORECAST-CAPACITY.md` (new), Sprint-20 note in `docs/ENGINE-S7L-COCKPIT.md`,
  `instances/README.md` Sprint-20 entry, STRESS-TEST "Update after Sprint 20".

## Residual seams (honest)
- **Data-grounding is conditional on the org recording the data**: a no-data org still cannot be forced to
  forecast or measured for capacity — the cockpit reports the recorded reality, it does not manufacture one.
  That is the correct behavior.
- **The projection holds the recorded trend; it is not an adaptive forecast model.** `forecast_metric` is a
  deterministic, transparency-first projection (last actual + mean delta), not a fitted/stochastic model. A
  future sprint could add a richer recorded-data model, but that would trade determinism/auditability for
  complexity and is out of scope of the "honest, deterministic, ~$0" stance.
- Capacity is a single recorded scalar (+ load), not a dynamic capacity/queuing model; the engine reports the
  recorded number, it does not compute availability dynamically.
- Q7/Q8 stay the Sprint-18 line (delegated by construction); #8 remains machine-eligible-best, §6-floor-gated.

## No spec change
- No normative gap surfaced; SPEC stays v0.22, 49 `$defs`, schema hash `7fc38c8c…`, `ros/` untouched,
  only catalog URI schemes (incl. the first-class `metric://`; no `capacity://`).