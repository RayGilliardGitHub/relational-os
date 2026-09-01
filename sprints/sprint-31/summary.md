# SPRINT 31 — SUMMARY: the WHOLE recorded-data §7L decision surface, inventoried as reason-not-choice, with the ONE remaining out-of-scope seam named exactly

## Goal
Positive consolidation, NOT a new capability. After six sprints (20–26 forecast series/variance/band,
27 emergency capacity_constraint, 28 horizon limit, 29 per-option infeasibility, 30 the RECOMMENDED-
option boundary) the whole §7L decision surface is recorded-data + reason. Sprint 31 makes the
label-vs-choice boundary the ORGANIZING truth of a full INVENTORY of that surface, proven in ONE
comprehensive, auditable run. **NO engine change** — `adjudication_engine.py` is byte-identical
(sha256 `a60f8f7…` confirmed before and after); the deliverable is a survey runner + recorded data,
exactly the Sprint-30 proof shape. No new noun; frozen 49 `$defs`; SPEC v0.22; `ros/` + schema +
sector `configs.py` untouched; ~$0.

## The build: `run_recorded_surface_demo.py` (new, exit 0 = ALL PASS)
Drives ELEVEN orgs — the eight Sprint-30 orgs byte-identical PLUS three NEW orgs (new labels, no
fixture overwrite) chosen to bound the surface beyond DELI-relabels:

| org | recorded descriptors | derived reasons |
|---|---|---|
| `deli-forecast` / `deli-varmax` / `deli-flat2` / `deli` | (reused Sprint-30 byte-identical) | metric-based reasons as their series allow; no capacity |
| `deli-varmax-cap` | (reused headroom capacity) | + Q7Q8/Q9 capacity (headroom) |
| `deli-infcap` / `deli-deficit-inf` | (reused per-option) | at-capacity / deficit + per-option flags |
| `deli-recommend-infcap` | (reused RECOMMENDED-option-infeasible) | at-capacity, recommended option `capacity_infeasible` |
| **`inspect-recorded`** (NEW) | QC on-time series (band_variance all) + capacity 500.0/load 1.3 + per-option reqs | all 5 reasons: Q3/Q6/Q7Q8(at-capacity)/Q9/Q8-donothing; 3 infeasible + 3 risk |
| **`cove-recorded`** (NEW) | lower-is-better answer-latency series (CO_POINTS, band all) + deficit capacity 30.0/load 0.9 + per-option reqs | all 5 reasons: deficit, 2 infeasible + 5 risk |
| **`inspect-nodata`** (NEW) | NO series / capacity / requirements (no-data control) | **NOTHING derived** (derivable_universe = []) |

Per org the runner emits a structured **`recorded_surface`** =
{present_recorded, derived_reasons, derivable_universe, not_derivable} where present_recorded tells
which recorded descriptor is present ({metric_series, point_variance, band_variance, capacity,
capacity_requirements, floor_gated, weights, reconcile_rule}), derived_reasons gives the actual derived
reason per question (Q3_forecast / Q6_projection / Q7Q8_capacity_constraint / Q9_capacity /
Q8_do_nothing_impact, or None), and not_derivable lists the named optimization seam + any descriptor
not recorded.

## What is proven (all real exit-0 output)
- **(a) Every derived label traces to a RECORDED descriptor.** For every org, Q3/Q6/Q8-forecast →
  `metric_series` and Q7Q8/Q9-capacity → `capacity` (missing-trace=[] on all 11). The no-data org
  derives NOTHING — the engine never invents a reason the org did not record. Capacity orgs derive the
  capacity reasons iff a capacity is recorded (all 11 True).
- **(b) The reason-not-choice proof, TOTALLED.** For ALL 11 orgs, Q7 `options` + `machine_eligible_best`
  + Q8 `recommendation` + `floor_gated` EXACTLY equal `cockpit_q7q8`. Tally: **"11/11 orgs the marker
  never re-ranks; INCLUDES the Sprint-30 org `deli-recommend-infcap` where the RECOMMENDED option is
  `capacity_infeasible`"** — the sharpest boundary is still a label, never a choice. No recorded data
  ever re-ranks the Q8 recommendation (it stays the frozen `rank` output on every org).
- **(c) Byte-identity / no regression.** The eight reused Sprint-30 orgs keep every byte (the runner's
  capacity blocks / `cockpit_q7q8` equalities are a strict superset); the three new orgs are NEW labels
  only. Determinism (dict + render) on re-run for all 11. New-org fixtures pass Sprint-0 C1-C5 (the
  no-data org correctly emits no fixtures — the honest empty surface).
- **(d) The frontier, named exactly.** The ONE remaining out-of-scope step is a capacity-constrained
  OPTIMIZATION that RE-RANKS the Q8 recommendation for the machine — a deliberate "re-rank for the
  machine" POLICY / user decision, NOT a label, deliberately NOT built. The seam is spelled: recorded
  per-option `capacity_requirements` already exist, so a deterministic next-best-non-infeasible rule by
  the frozen `rank` utility would be the only missing piece; it CHANGES the Q8 recommendation. Plus a
  per-option requirement NOT unit-coupled to the recorded capacity / an option with no recorded
  requirement remains non-derivable (the engine never invents one).
- **(e) Real output + conformance.** New runner ALL PASS; full non-regression green; `adjudication_engine.py`
  hash `a60f8f7…` unchanged; schema hash `7fc38c8c…`; 49 `$defs`; SPEC v0.22; `ros/` + schema + sector
  configs untouched; no `://qk/` in the config-driven new fixtures; no new noun.

## Verification (all exit 0, plain python3 + Sprint-0 venv for conformance)
- NEW runner: `python3 run_recorded_surface_demo.py` → **RESULT: ALL PASS**.
- Full non-regression (captured twice — green Sprint-30 baseline first, again after the new runner):
  all 14 CR demo runners + all 5 CR conformances + `build_all`/`conformance_all` (12 sectors) + S5
  reference demo + conformance + agent demo + conformance → ALL PASS. (Conformance + S5 + agent
  conformances use the Sprint-0 venv for jsonschema.)
- Invariants: engine raw sha256 `a60f8f7…` unchanged; schema `7fc38c8c…`; **49 `$defs`**; SPEC v0.22;
  `ros/` + schema + sector `configs.py` untouched; no `://qk/` in the config-driven new fixtures
  (only the legacy hand-written `instances/financial/` v1, which is not a `configs.py` entry).

## Documents rolled forward
`docs/ENGINE-FORECAST-CAPACITY.md` §15 · `docs/ENGINE-S7L-COCKPIT.md` §13 · `instances/README.md`
Sprint-31 entry · `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after
Sprint 31" · the `relational-os` skill note (below). No SPEC bump (v0.22).

## Honest §16 verdict
**Sprint 30's frontier is now the ORGANIZING truth of an inventory: the whole recorded-data §7L
decision surface is provably recorded-data + a REASON, inventoried in one auditable run, while the Q8
recommendation provably stays the frozen `rank` output for every org (no recorded data ever re-ranks).**
An 11-org runner (the eight Sprint-30 orgs byte-identical + INSPECT + COVE + a no-data control) emits a
per-org `recorded_surface` inventory and asserts every derived label traces to a recorded descriptor
and the marker is a REASON, never a CHOICE — Q7 options + machine_eligible_best + Q8 recommendation +
floor_gated EXACTLY == `cockpit_q7q8` for all 11, including `deli-recommend-infcap` where the RECOMMENDED
option is `capacity_infeasible`. This is generic + additive: recorded `metric://` series + recorded
point-`variance` + the recorded `band_variance` source + a recorded authority `capacity` + a recorded
per-option `capacity_required` descriptor; no new noun, frozen 49 `$defs`, and the engine is provably
UNCHANGED (hash `a60f8f7…`). **Still not derivable (the honest frontier):** the ONE remaining
out-of-scope step — a capacity-constrained OPTIMIZATION that RE-RANKS the Q8 recommendation for the
machine (a "re-rank for the machine" POLICY / user decision, NOT a label, deliberately NOT built; seam =
recorded per-option `capacity_requirements` already present + a deterministic next-best-non-infeasible
rule by the frozen `rank` utility being the only missing piece); plus a per-option requirement that is
NOT unit-coupled to the recorded capacity / an option with no recorded requirement remains non-derivable
(the engine never invents one). The deterministic advisory stance can label — even the RECOMMENDED option
`capacity_infeasible` from recorded data, and it can inventory the entire recorded surface as
reason-not-choice — but it cannot and must not choose the replacement for the §6 human. No SPEC bump
(v0.22), no new noun.