# SPRINT 24 — PLAN

**Goal:** Sprint 23 (recorded last-point variance -> do-nothing projected BAND) disclosed in its own
findings the next honest frontier: **the band uses only the LAST recorded point's `variance`**, so a
series whose RECORDED `variance` changed across its points (widened or narrowed spread) is collapsed
to the final variance in the band. **Sprint 24 closes that bounded slice** by making the band's
variance source a **recorded, additive `band_variance` parameter on the `metric://` object**: the
last point's variance (Sprint-23 default, byte-identical) vs a recorded **whole-series** choice
(`"all"` = largest recorded |variance| across the recorded points; `"minmax"` a defined recorded
whole-series rule). The band can then be priced from the recorded worst-case spread where the org
records it, still recorded-data only, no invented number.

**Scope (additive only):** modify `instances/contested_reality/adjudication_engine.py` — extend
`_forecast_closure`'s Sprint-23 band block to read the recorded `band_variance` source, select the
sigma, and emit the additive `source` key. `render_cockpit_s7l` unchanged (it already renders the
band generically). Frozen functions untouched. 49 `$defs`, URI cap, SPEC v0.22, `ros/` + schema
untouched.

## Baseline (verified, all exit 0 — captured FIRST before any edit)
Sprint-23 `run_forecast_variance_demo.py`, Sprint-22 `run_forecast_direction_demo.py`, Sprint-21
`run_forecast_action_demo.py`, Sprint-20 `run_forecast_capacity_demo.py`, `run_cockpit_s7l_demo.py`,
the 11 curated C-R demos (incl. `run_full_dispute.py`), `conformance_adjudication.py` (16 labels) +
`conformance_{dispute,interest,lifecycle,tradeoff}.py`, `instances/build_all.py` +
`conformance_all.py`, Sprint-5 `run_s5_demo.py` + `run_s5_conformance.py`, `agent_demo/run_agent_demo.py`.
Schema JSON hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22.

## Design
- Read `band_variance` from the recorded metric object: absent / `"last"` / unknown ->
  `source="last-point"`, `sigma = abs(last recorded point's variance)` (EXACTLY Sprint 23, byte-identical).
- `"all"` -> `sigma = max(abs(variance))` over the recorded points (the largest recorded magnitude);
  `"minmax"` -> same max-|variance| (a recorded whole-series rule; "minmax" = the recorded spread
  extremes, taken as the max |variance| magnitude). Both select a recorded point magnitude ONLY.
- `source` = `"last-point"` | `"all"` | `"minmax"` (the recorded band-variance source). Emitted ONLY
  when the band exists AND the source is a whole-series choice (so the default orgs' band stays
  byte-identical — no `source` key when no `band_variance` was recorded, preserving Sprint-23 bytes).
- low/high = worst ± sigma; `crosses` unchanged (worst side vs threshold in the direction).
- No `band_variance` recorded -> default orgs keep Sprint-23 byte-identical output (band present but
  NO `source` key). No numeric last variance -> no band (unchanged). No data -> unchanged.
- Summary + attention-why name the source honestly when a whole-series source is active.

## Steps
1. plan.md (this) + work/1-plan.md before the engine edit.
2. Patch `_forecast_closure` band block (band_variance source selection + additive `source` key).
3. New runner `run_forecast_variance_all_demo.py` (>=4 orgs):
   - `deli-forecast` (no `band_variance`) — byte-identical to Sprint 23 (source key absent).
   - `deli-varmax` (NEW: records `band_variance:"all"`, last |variance| small, EARLIER |variance|
     larger -> sigma = recorded max, band HIGH > Sprint-23 last-point high).
   - `deli-cost` (no `band_variance`) — byte-identical to Sprint 23.
   - `deli` (no-data) — unchanged.
   Full Q1–Q10; recorded-data-only sigma; superset byte-identity (Sprint-23 fields preserved, only
   the additive `source` key added on the whole-series org); determinism; agreement with
   `forecast_metric` + hand-computed whole-series max; no §6 overrule; no wall-clock. Emits fixtures +
   report.
4. Non-regression: re-run the whole baseline + new runner; verify schema hash, ros/, SPEC, sectors.
5. Docs: additive `band_variance` note in `docs/ENGINE-FORECAST-VARIANCE.md` (and `-DIRECTION.md` if
   useful), `instances/README.md` entry, `STRESS-TEST-SCENARIOS.md` note; `references/` note if useful.
6. `sprints/sprint-24/summary.md` + `notes/findings.md`; write `sprints/sprint-25/PROMPT.md`.

## DoD
New runner ALL PASS (exit 0); default orgs byte-identical to Sprint 23 (only the additive `source`
key added to the whole-series band; default orgs' band has no `source`); whole-series org's
sigma == recorded max |variance| and low/high/crosses exact recorded-data arithmetic; full
non-regression green; SPEC v0.22; 49 `$defs`; schema hash `7fc38c8c…`; no new noun.