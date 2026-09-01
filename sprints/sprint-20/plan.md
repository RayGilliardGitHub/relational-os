# Sprint 20 — plan: recorded-data Q6 forecast + Q9 capacity for the §7L morning cockpit

**Goal.** Sprint 19 made `adjudication_engine.cockpit_s7l` render the full §7L Q1–Q10 cockpit, data-only,
for any configured org — but its own findings ("Residual seams") disclosed that **Q6 cannot forecast** (no
org records a realized-vs-expected series) and **Q9 "capability" is the holder-of-authority assignment, not
a capacity number**. Sprint 20 closes a bounded slice of both by making a generically-driven org *record*
the missing data additively on its own graph/ledger (a `metric://` realized-vs-expected series + a
`capacity` additive field on the authority the Q9 question reads), so those two questions are answered
**AS DATA where the data exists**, with the honest no-data fallback unchanged.

**Constraints (from PROMPT.md, mandatory).** Additive only; the ONLY engine file I may touch is
`instances/contested_reality/adjudication_engine.py`. No new URI noun, no schema/`$defs` edit (49 `$defs`,
SPEC v0.22). No rewrite of any frozen function (`reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/
`_aggregate`/`rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`/`cockpit_s7l`/`render_cockpit_s7l`).
Never the wall-clock, never an invented number. Single-threaded, ~$0, deterministic local Python.

**Baseline (verified green this session before any edit).** `run_cockpit_s7l_demo.py` ALL PASS; 9 curated
contested-reality runners ALL PASS exit 0; `conformance_adjudication.py` 16 labels C1–C5 ALL PASS (49 $defs);
sector `build_all.py` + `conformance_all.py` ALL PASS; S5 reference demo + conformance ALL PASS; agent demo +
conformance ALL PASS. Schema hash `7fc38c8c…` = SPEC v0.22.

## Design (why this is generic + additive)

- **QP6 / Q9 become recorded-data reads.** `cockpit_s7l.q6` already introspects a recorded realized-vs-expected
  series (`_recorded_forecast_series`); Sprint 20 turns that into an *actual deterministic projection* via a new
  generic `forecast_metric(cfg, sub, metric_uri, *, horizon)` that projects purely from the recorded
  `metric://` points (last recorded `actual`, mean of recorded consecutive deltas, forward periods) and labels
  the result a projection — never an outcome. `cockpit_s7l.q9` gains a read of an additive **`capacity`** field
  (`{value, unit, load}`) recorded on the `authority://` object the Q9 question reads.
- **Replayable recorders.** Two small additive recorder helpers (`record_metric_series`, `record_capacity`)
  let any org append the missing data to its own immutable ledger (one signed event, merge-not-replace on the
  existing objects) — the same additivity discipline as `reconcile_learning.record_realized_outcome`.
- **New org proof.** The runner clones `deli` to a clean `deli-forecast` namespace (relabels every
  `://deli/` → `://deli-forecast/`, so it owns its own `authority://deli-forecast/adjudicate`), runs the
  generic lifecycle, then records a `metric://deli-forecast/m-on-time` realized-vs-expected series + the
  `capacity` field. `deli` (existing, no recorded series/capacity) is the honest-fallback control. Both must
  still pass the full §7L Q1–Q10.

## Forecast projection rule (deterministic, from recorded values only)

From a recorded `metric://` object carrying a `points` list (`{expected,target,actual,variance}` per period):
- `last_actual` = last point's `actual`
- `mean_delta` = mean of consecutive `actual` deltas (0 when <2 points)
- forward projection for period `f` in `1..horizon`: `round(last_actual + mean_delta * f, 4)`
- reported alongside the **last recorded variance** and labelled a **projection** (never expanded to an outcome).
- Absent series → honest `{"available": False, "forecast": "cannot project …"}`.

## Build steps (plan-before-build; real tool output)

1. Append to `adjudication_engine.py`: `forecast_metric`, `_recorded_metric_with_series`, `record_metric_series`,
   `record_capacity`; extend `cockpit_s7l` `.q6`/`.q9` and `render_cockpit_s7l` Q6/Q9 lines. Frozen functions
   untouched; 49 `$defs`, URI cap, SPEC v0.22 intact.
2. `run_forecast_capacity_demo.py` (exit 0 = ALL PASS): drive `deli-forecast` (recorded data) + `deli` (no data);
   assert both full §7L; recorded org forecasts Q6 + reports Q9 capacity; no-data org keeps the honest fallback;
   determinism on re-run; forecast values agree with the recorded points (hand-computed); q9.capacity equals the
   recorded field on the authority object; validate the `deli-forecast` fixtures with the Sprint-0 conformance.
3. Full non-regression: all curated runners + conformance_adjudication (16 labels) + sector + S5 + agent;
   deli/cove byte-identical up to the clock.
4. Docs: `docs/ENGINE-FORECAST-CAPACITY.md` (new), additive note in `docs/ENGINE-S7L-COCKPIT.md` (§2 Q6/Q9 +
   §6 verdict), `instances/README.md` Sprint-20 entry, STRESS-TEST "Update after Sprint 20".
5. `sprints/sprint-20/summary.md` + `notes/findings.md`; write `sprints/sprint-21/PROMPT.md`.

## Definition of done

New runner ALL PASS; full non-regression green; no new noun; 49 `$defs`; SPEC v0.22; `ros/` + schema untouched;
deli/cove byte-identical up to the clock; honest §16 verdict on whether the ten-question cockpit is now
data-grounded on every question where the data exists.