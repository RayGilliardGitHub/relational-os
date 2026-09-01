# SPRINT 28 — PLAN

## Goal
Prove the Sprint-27 Q7/Q8 `capacity_constraint` marker at its LIMIT on a real §7L Q1–Q10 cockpit:
drive the **non-headroom** branches of the shared `_capacity_reason` rule (at-capacity, deficit) on
real recorded-data orgs, and assert the marker is a LABEL — Q7 options + machine-eligible best + Q8
recommendation EXACTLY equal to `cockpit_q7q8` at every reason.

## What already exists (Sprint 27 state, verified by reading)
- `adjudication_engine.py` `_capacity_reason(capacity_obj, band_horizon, direction)` -> (label, flag):
  - `deficit` (priority) when the horizon band's worst-side magnitude (`high` for lower-is-better,
    `low` for higher-is-better) >= the recorded capacity VALUE.
  - `at-capacity` when recorded load >= 1.0.
  - `headroom` otherwise.
  This is the SHARED rule — the Q9 `capacity_planning_attention` label AND the Q7/Q8
  `capacity_constraint.reason` are BOTH derived from it, so they agree BY CONSTRUCTION.
- `cockpit_s7l` emits the `capacity_constraint` block on BOTH Q7 and Q8 (identical values) whenever
  the org records a numeric capacity AND a band (`band_horizon`) AND a numeric threshold. In the
  non-headroom case, `options_flagged` marks EVERY capacity-consuming NON-baseline option
  `capacity_risk` (never `capacity_infeasible`, never the baseline do-nothing/UNRESOLVED). The frozen
  `rank`/`machine_eligible_best`/`cockpit_q7q8` are untouched — the block is a label added additively.
- Sprint-27 ran ONLY the headroom branch on a real org (`deli-varmax-cap`: reason `headroom`,
  `options_flagged:{}`); the at-capacity / deficit branches were only exercised at the HELPER level.
- This means NO engine change is required. This sprint is recorded data + a new runner only.

## Approach — additive, recorded-data only
Drive ≥7 fresh orgs on real Substrates; reuse the five Sprint-26/27 orgs byte-identical, add two NEW
orgs that RECORD the non-headroom situation:
- `deli-forecast` (no capacity, no band_variance)      -> no `capacity_constraint` (byte-identical)
- `deli-varmax`  (band, no capacity)                    -> no `capacity_constraint`
- `deli-varmax-cap` (band + capacity 500, load 0.72)    -> `capacity_constraint` reason **headroom** (Sprint-27 default)
- `deli-flat2`   (recorded series, no variance/band)    -> no `capacity_constraint` (no-band control)
- `deli`         (no recorded series data)              -> no `capacity_constraint` (no-data org)
- **`deli-atcap`**  (NEW)  recorded capacity 500.0 resolutions/day, **load 1.25** (>= 1.0), same
  whole-series band as deli-varmax (band_variance "all", horizon 0.62…1.02)
  -> `_capacity_reason` = **at-capacity**, flag True
- **`deli-deficit`** (NEW)  lower-is-better cost/latency metric (band_variance "all", horizon
  12.0…32.0), recorded capacity **value 30.0** resolutions/day (load 0.9)
  -> horizon worst-side high 32.0 >= capacity value 30.0 -> **deficit**, flag True

### The two new orgs' exact recorded numbers (reproducible)
- `deli-atcap`: relabel DELI to `deli-atcap`; record series `metric://deli-atcap/m-on-time` with
  the SAME 4 points as deli-varmax (actuals 0.92, 0.90, 0.87, 0.86; variances -0.18,-0.09,-0.06,-0.03;
  band_variance:"all") -> projected [0.84, 0.82, 0.80], sigma 0.18, horizon {low:0.62, high:1.02}.
  `record_capacity(... value=500.0, unit="resolutions/day", load=1.25)`.
  _capacity_reason(low-side 0.62 vs cap 500 -> not deficit; load 1.25 >= 1.0) -> **at-capacity**.
- `deli-deficit`: relabel DELI to `deli-deficit`; record series `metric://deli-deficit/m-latency`
  lower-is-better (actuals 12,14,16,18; variances 2,4,6,8; target 16; band_variance:"all") ->
  projected [20,22,24], sigma 8, horizon {low:12.0, high:32.0}.
  `record_capacity(... value=30.0, unit="resolutions/day", load=0.9)`.
  _capacity_reason(high-side 32.0 >= cap 30.0) -> **deficit**.

## Assertions in the new runner (`run_forecast_horizon4_demo.py`)
(a) FULL §7L Q1–Q10 cockpit + data evidence on all 7 orgs.
(b) Byte-identity/Sprint-27 regression on the 5 reused orgs: Q3 horizon suffix string, Q9
    `capacity_planning_attention` (flag False headroom), NO `capacity_constraint` on the 4
    non-capacity orgs, `deli-varmax-cap` still `reason:"headroom", options_flagged:{}`.
(c) Non-headroom block FULLY exercised:
    - `deli-atcap`: q7+q8 `capacity_constraint.reason=="at-capacity"`, flag True,
      `options_flagged` marks EVERY non-baseline option `capacity_risk`, baseline never flagged;
      agrees with its Q9 `capacity_planning_attention` (flag True, same reason).
    - `deli-deficit`: reason=="deficit", flag True, same options_flagged coverage + baseline never
      flagged; agrees with Q9 label.
(d) Marker is a LABEL at its limit (the honest core): for EVERY org, q7.options (same count/uris) +
    q7.machine_eligible_best + q8.recommendation + q8.floor_gated EXACTLY equal to `cockpit_q7q8` —
    no §6 overrule, no re-rank, no option-removal, even at at-capacity/deficit.
(e) Superset byte-identity: the capacity orgs' Q7/Q8 pre-existing keys intact; only the additive
    capacity_constraint block added. Every `capacity_constraint` value traces to a recorded field
    (recorded capacity/load, band_horizon, recorded threshold).
(f) Determinism on re-run (dict + render) for all 7 orgs.
(g) Emit fixtures for the recorded orgs (incl. the two new ones) + the engine-native report
    `cockpit-forecast-horizon4.md`.

## Verification (all exit 0; plain python3)
- Green baseline FIRST (Sprint-27 state): the full DoD list from PROMPT.md — run_forecast_horizon3_demo
  + horizon2 + horizon + variance_all + variance + direction + action + capacity + cockpit_s7l +
  cockpit_q7q8 + adjudication_engine demos; conformances (incl. conformance_adjudication + 4 prior CR
  conformances, build_all, conformance_all, S5 reference + conformance). All MUST pass unchanged
  (this sprint touches no engine file, so they stay green).
- New runner: `python3 run_forecast_horizon4_demo.py` -> ALL PASS, exit 0.
- Schema hash 7fc38c8c… + 49 $defs + ros/ untouched (verify unchanged).

## Docs (roll-forward)
- `docs/ENGINE-FORECAST-CAPACITY.md`: add a §12 "proven at its limit (at-capacity / deficit)" note.
- `docs/ENGINE-S7L-COCKPIT.md`: extend the §9 trade-off/cockpit note (marker = recorded-data reason,
  never removal/overrule; Q8 provably unchanged at at-capacity/deficit).
- `instances/README.md`: Sprint-28 entry. `sprints/sprint-28/summary.md` + `notes/findings.md`.
- `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`: "Update after Sprint 28" note.
- Write `sprints/sprint-29/PROMPT.md` (next self-contained sprint prompt).

## Honest §16 verdict
The marker is now demonstrated across ALL THREE derived reasons on real orgs (headroom default +
at-capacity + deficit) WHILE the Q8 recommendation provably stays unchanged even at at-capacity /
deficit. Still not derivable: a capacity-constrained OPTIMIZATION that re-ranks the recommendation
(out of scope — the §6 human always rules; the marker never CHOOSES), and `capacity_infeasible`
(unreachable until a RECORDED per-option capacity requirement exists).

## Protocol
Single-threaded (no subagents), plan-before-build (work/<n>-plan.md before each build step),
real tool output only (~$0, plain python3). Additive only: NO engine file change expected.