# SPRINT 28 — NOTES / FINDINGS

## Assumptions that mattered
- **The engine needed NO change — this sprint is recorded data + a runner proof.** Reading
  `adjudication_engine.py` confirmed `_capacity_reason` (deficit > at-capacity [load>=1.0] > headroom)
  and the Q7/Q8 `capacity_constraint` block already implement all three branches; Sprint-27 simply
  never drove a non-headroom org. So the sprint is purely additive: two NEW orgs that RECORD the
  non-headroom situation + a new runner. No engine file was modified this sprint (verified: `git diff`
  of the engine shows only the pre-existing Sprint-26/27 capacity additions; its mtime predates this
  session).
- **The recorded capacity VALUE is compared to the horizon band's worst-side magnitude even across
  different units** (a rate/volume capacity vs a latency magnitude). This is the Sprint-27 documented
  defense: "state the recorded numbers and label the reason." For `deli-deficit` we deliberately chose
  a capacity VALUE (30.0) below the horizon worst-side high (32.0) so the deficit reason is derivable
  from recorded numbers — reproducible, never invented.
- **`deficit` takes precedence over `at-capacity`** in `_capacity_reason` (deficit checked first). For
  `deli-atcap` we kept the recorded load (1.25) high enough to trigger at-capacity while the horizon
  worst-side low (0.62) stayed below the 500.0 capacity so it is NOT deficit — clean, single-reason.
- **The baseline (`unresolved` / do-nothing) consumes no capacity and is NEVER flagged.** The engine
  flags every non-baseline option `capacity_risk` when not headroom. Asserted on the deli set: 7
  `capacity_risk`, baseline excluded.
- **Reusing `r26.build_orgs()` (Sprint 26/27 builder) guarantees the five reused orgs' recorded data
  is byte-identical** — the ONLY added bytes are the two new orgs, matching the superset contract.

## Verified (real tool output, all exit 0)
- **Green baseline captured FIRST** (Sprint-27 state): all 11 CR demo runners + 5 CR conformances
  (venv) + `build_all`/`conformance_all` (12 sectors) + S5 reference demo/conformance + agent
  demo/conformance → all exit 0; schema JSON hash `7fc38c8c0a6e5b76cd55393f2c732417675b224812970951778853a6677642c4`,
  49 `$defs`, SPEC v0.22.
- **After the additive runner:** new `run_forecast_horizon4_demo.py` → **ALL PASS (94 PASS lines incl.
  the run_scenario rehearse)**. Key outputs:
  - `deli-atcap` Q7+Q8 `capacity_constraint` = `{recorded_capacity: "500.0 resolutions/day (load
    1.25)", horizon_band: {low: 0.62, high: 1.02}, reason: "at-capacity", flag: true, options_flagged:
    {7 capacity_risk}}`.
  - `deli-deficit` Q7+Q8 `capacity_constraint` = `{recorded_capacity: "30.0 resolutions/day (load
    0.9)", horizon_band: {low: 12.0, high: 32.0}, reason: "deficit", flag: true, options_flagged: {7
    capacity_risk}}`.
  - On both, the reason equals the org's Q9 `capacity_planning_attention` label BY CONSTRUCTION; the
    baseline `unresolved` is never flagged; and for EVERY org (incl. the two non-headroom) the Q7
    `options` (count+uris) + `machine_eligible_best` + Q8 `recommendation`/`floor_gated` EXACTLY equal
    `cockpit_q7q8`, Q8 recommendation `partial-settlement` unchanged.
- **Sprint-27 byte-identity after the runner:** `run_forecast_horizon3_demo.py` (and horizon2/horizon/
  variance_*/direction/action/capacity + cockpit_s7l + cockpit_q7q8 + engine demo) all ALL PASS — the
  five reused orgs unchanged.
- **New-org fixtures pass Sprint-0 C1–C5** (`deli-atcap`, `deli-deficit`; 26 instances each, 49 `$defs`).
- **Full non-regression** (final consolidated run): every demo + conformance exit 0 (FAIL=0). Schema
  hash unchanged; `ros/` + schema + sector `configs.py` untouched; no new noun.

## Pitfalls encountered
- **Pyright flags `ros.substrate` as unresolved on fresh edit** — expected: `ROS` is injected via
  `sys.path.insert` at runtime, identical to every other CR runner. Not a defect.
- **Cross-unit capacity-vs-band comparison needs a defensible recorded number.** I verified the two
  non-headroom orgs analytically (projection/band/capacity arithmetic) BEFORE writing the runner, so
  the recorded capacity values (500 / 30) provably produce the intended reasons.
- **Reading/writing a partially-paged doc**: `ENGINE-S7L-COCKPIT.md`, `instances/README.md`, and
  `STRESS-TEST-SCENARIOS.md` were edited by appending after a paged partial read; the `patch` tool
  warned accordingly but the append landed on the correct unique anchor each time (verified by diff).

## Open issues / next work (the honest frontier after Sprint 28)
- **The marker still never CHOOSES a different option for the machine — the §6 human always does.** A
  genuinely capacity-constrained OPTIMIZATION that RE-RANKS the recommendation stays explicitly out of
  scope of the deterministic advisory stance. This is a positive boundary (the marker is a reason, not
  a choice), but it is the frontier the next sprint would face if we wanted the recorded capacity to
  move the recommendation — which the prompt forbids.
- **`capacity_infeasible` remains structurally unreachable** without a RECORDED per-option capacity
  requirement (the engine never invents one). A future sprint could add such a recorded descriptor
  (Sprint-16 vocabulary discipline: unit-coupled, additive, never invented) to enable real
  infeasibility labeling — but that would be a NEW capability, not a proof-of-existing-branch.
- **Units differ in the capacity-vs-band comparison** (rate/volume vs latency magnitude); the defense
  remains "state the recorded numbers and label the reason." A unit-coupled capacity-consumption
  comparison must be a recorded descriptor.
- **`band_variance: "minmax"` still equals `"all"`** (Sprint-24 finding stands).
- **The horizon-wide band remains a recorded spread, not a stochastic forecast** — probabilistic /
  adaptive stays out.

No normative gap surfaced -> SPEC stays v0.22.