# WORK 2 — engine edit: Q9 capacity-planning attention (additive, cockpit_s7l)

In `cockpit_s7l`'s Q9 block, after the Sprint-25 `band_capacity_attention` assignment, add an
additive `capacity_planning_attention` = {flag, why} emitted ONLY when:
  - the org RECORDS a numeric `capacity` on its authority object (`capacity_recorded` True), AND
  - a band exists (`bh is not None`) AND the recorded threshold is numeric.

ONE deterministic rule (recorded numbers only; documented):
  - `_load >= 1.0` -> at/over recorded capacity (at-capacity).
  - horizon band's worst-side magnitude reaches/exceeds the recorded capacity VALUE
    (`worst_side >= capacity_value`) -> deficit.
    - higher-is-better (rate/quality): worst side = band_horizon.low.
    - lower-is-better (cost/load):   worst side = band_horizon.high.
  - otherwise headroom.
  `flag` = bool(at-capacity OR deficit). `why` states the recorded capacity value/unit/load and the
  horizon-wide band, and labels headroom / at-capacity / deficit as a derived REASON. NEVER a
  fabricated capacity number, NEVER a directive.

Additive superset: `band_capacity_attention` (Sprint 25) unchanged. Orgs that record NO capacity
(fc/vm/fl2/deli) get NO `capacity_planning_attention` key -> byte-identical. C2-safe keys only
(`capacity_planning_attention`, `flag`, `why`).