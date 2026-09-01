# work/2 — DESIGN + build `run_recorded_surface_demo.py`

## Goal
A new runner that inventories the ENTIRE recorded-data §7L decision surface as reason-not-choice,
for 11 orgs: the eight Sprint-30 orgs (byte-identical) + INSPECT + COVE + one no-data org (new
labels, no fixture overwrite). NO engine change (`adjudication_engine.py` stays byte-identical).

## Org set
- 8 reused (r30.build_orgs()): deli-forecast, deli-varmax, deli-varmax-cap, deli-flat2, deli,
  deli-infcap, deli-deficit-inf, deli-recommend-infcap.
- 3 NEW (name them; new labels):
  - `inspect-recorded` — INSPECT relabel; record a QC on-time metric series (band_variance "all"),
    authority capacity {value,load}, per-option requirements (at-capacity).
  - `cove-recorded` — COVE relabel; record a lower-is-better answer-latency series (CO_POINTS), a
    deficit capacity {value,load}, per-option requirements.
  - `inspect-nodata` — INSPECT relabel with NO recorded series/capacity/requirements (the no-data
    control org — proves the derivable-vs-not boundary: nothing derivable, everything in not_derivable).

## `recorded_surface` per org (the inventory)
- present_recorded = {metric_series, point_variance, band_variance, capacity, capacity_requirements,
  floor_gated, weights, reconcile_rule} (each a bool; read from the org's own graph/config via the
  SAME read paths the engine uses: a recorded metric:// series via `_recorded_metric_with_series`,
  authority.capacity / capacity_requirements, cfg.floor_gated / weights / reconcile).
- derived_reasons = {Q3_forecast: attention why|None, Q6_projection: projection worst|None,
  Q7Q8_capacity_constraint: reason label|None, Q9_capacity: planning label|None,
  Q8_do_nothing_impact: summary|None} (each the actual derived reason, or None).
- derivable_universe = sorted keys actually derived.
- not_derivable = the NAMED optimization seam + any recorded descriptor this org does NOT record.

## Assertions (per org)
1. Every present derived reason traces to a recorded descriptor (map: Q3_forecast/Q6_projection/
   Q8_do_nothing_impact → metric_series; Q7Q8_capacity_constraint/Q9_capacity → capacity). No reason
   without its recorded source (and inversely, the engine never derives a reason the org didn't record).
2. Reason-not-choice proof for EVERY org: q7.options + machine_eligible_best + q8.recommendation +
   floor_gated EXACTLY == cockpit_q7q8. Print tally: "N/N orgs: the marker never re-ranks; includes
   the Sprint-30 org where the RECOMMENDED option is capacity_infeasible (deli-recommend-infcap)."
3. Determinism (dict + render) on re-run for every org.
4. Byte-identity: the 8 reused orgs' capacity blocks / cockpit equalities are a strict superset.

## Report + fixtures
- New-org fixtures via eng.emit_fixtures (labels only: inspect-recorded, cove-recorded,
  inspect-nodata — DO NOT overwrite inspect/cove existing dirs).
- artifacts/adjudication/reports/cockpit-recorded-surface-inventory.md (engine-native §16, per-org
  surface + tally + the named seam).
- RESULT: ALL PASS / exit 0.