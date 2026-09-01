# SPRINT 29 — NOTES / FINDINGS

## Assumptions that mattered
- **The engine DID need a change this sprint (unlike Sprint 28):** `capacity_infeasible` is genuinely
  new capability, not a proof-of-existing-branch. So the change is additive and confined to
  `adjudication_engine.py`: a NEW REPLAYABLE recorder `record_capacity_requirements` (next to
  `record_capacity`), a NEW pure helper `_per_option_capacity_flags`, and the additive extension of the
  existing Q7/Q8 `capacity_constraint` block in `cockpit_s7l` (swap the today loop for the per-option
  helper ONLY when a recorded `capacity_requirements` dict is present). Frozen functions untouched.
- **The cleanest home for the per-option requirement is an additive map on the SAME authority:// object
  that already carries the additive `capacity`** — not on `cfg`. Reason: it is RECORDED (in the signed
  ledger/graph, exactly like `record_capacity`), it is unit-coupled BY CONSTRUCTION (`available =
  capacity.value − capacity.load`, same recorded unit), and it rides the object the Q9/Q7/Q8 already
  read — so the engine reads it back from `auth_obj.get("capacity_requirements")` with no new lookup.
- **AVAILABLE = recorded capacity VALUE − recorded load.** The recorded `load` for these orgs is a
  ratio (e.g. 1.3), but the rule treats it as the units consumed so far, subtracted from the recorded
  VALUE → the remaining units the option can consume. It is a label from recorded numbers; not a
  directive. The prompt's wording ("recorded capacity VALUE − recorded load") is implemented verbatim.
- **The baseline is recorded with NO requirement and is NEVER flagged** — the engine skips it in the
  per-option helper AND (as today) the baseline carries no capacity-consumption.
- **`deficit` still takes precedence over `at-capacity`** in `_capacity_reason`; for `deli-infcap` we
  kept the horizon worst-side low (0.62) well below the 500.0 capacity so it is NOT deficit → clean
  single at-capacity reason (same defense as Sprint 28's `deli-atcap`).
- **A no-requirements org is byte-identical to Sprint 28** (strict superset): the `capacity_constraint`
  dict has NO `per_option_requirements` / `available_capacity` keys unless requirements are recorded.
  Verified: the five reused orgs keep every pre-existing byte (headroom org still
  `{reason:"headroom", flag:False, options_flagged:{}}`).

## Verified (real tool output, all exit 0)
- **Green baseline captured FIRST** (Sprint-28 state): all 12 CR demo runners + 5 CR conformances
  (venv) + `build_all`/`conformance_all` (12 sectors) + S5 reference demo/conformance + agent
  demo/conformance → all exit 0; schema raw sha256 `7fc38c8c0a6e5b76cd55393f2c732417675b224812970951778853a6677642c4`,
  49 `$defs`, SPEC v0.22.
- **Engine change + re-baseline:** after the additive engine change, `run_forecast_horizon4`/`horizon3`/
  `horizon2` still ALL PASS (the 5 reused orgs stay byte-identical — the per-option helper fires only
  when `capacity_requirements` is recorded). New functions present + unit sanity checked:
  `_per_option_capacity_flags({"value":500.0,"load":1.3}, {a:499.0,b:200.0}, [a,b,unresolved],
  "unresolved", non_headroom=True) == {a:"capacity_infeasible", b:"capacity_risk"}`; with
  `non_headroom=False` (headroom) == `{}` (only infeasible under headroom).
- **New runner** `run_forecast_per_option_capacity_demo.py` → **ALL PASS (88 PASS lines)**. Key
  outputs:
  - `deli-infcap` Q7+Q8 `capacity_constraint` = `{recorded_capacity:"500.0 resolutions/day (load 1.3)",
    horizon_band:{low:0.62,high:1.02}, reason:"at-capacity", flag:true, options_flagged:{3
    capacity_infeasible, 4 capacity_risk}, per_option_requirements:{...499.0/200.0/50.0/100.0},
    available_capacity:498.7}`.
  - `deli-deficit-inf` Q7+Q8 `capacity_constraint` = `{... reason:"deficit", flag:true,
    options_flagged:{3 capacity_infeasible, 4 capacity_risk}, per_option_requirements:{...30.0/20.0/
    10.0/15.0}, available_capacity:29.1}`.
  - On both, the per-option formula is reproduced from the RECORDED requirements vs available; the
    reason equals each org's Q9 `capacity_planning_attention` label BY CONSTRUCTION; the baseline is
    never flagged; and for EVERY org (incl. the two infeasible ones) `q7.options` (count 8) +
    `machine_eligible_best` + `q8.recommendation` + `floor_gated` EXACTLY equal `cockpit_q7q8`, Q8
    recommendation `partial-settlement` unchanged.
- **New-org fixtures pass Sprint-0 C1–C5** (ran the validator directly on `deli-infcap` and
  `deli-deficit-inf`: 26 instances each, 49 `$defs`, all 5 checks PASS).
- **Full non-regression** (final consolidated run): every CR demo + every conformance +
  `build_all`/`conformance_all` + S5 + agent → ALL PASS (FAIL=0). Schema raw hash `7fc38c8c…`
  unchanged; 49 `$defs`; SPEC v0.22; `ros/` + schema + sector `configs.py` untouched; the ONLY source
  change is `adjudication_engine.py` (+ the new runner).

## Pitfalls encountered
- **Pyright flags `ros.substrate` as unresolved on fresh edit** — expected: `ROS` is injected via
  `sys.path.insert` at runtime, identical to every other CR runner. Not a defect.
- **The `_num` helper returns `float | None`**, so `_num(a) - _num(b)` trips Pyright's
  `reportOptionalOperand` in the RUNNER — but in the ENGINE the recorded value/load are always present
  for a requirement-bearing org. In the runner assert I compared `cc["available_capacity"] == available`
  (the runner's own constant) to avoid that noise; the recorded-data provenance (available == recorded
  value − load) is asserted via the equality of the surfaced `available_capacity` with the constant
  that is itself `round(cap_value - cap_load, 4)`.
- **A half-f-string blob in the report** left literal `{INFCAP_AVAILABLE}`/`{{DEFINF_AVAILABLE}}` in the
  generated .md — fixed by making every interpolating segment an f-string and re-running; re-verified
  no placeholder survives in the report.
- **`patch` on a paged doc can corrupt an anchor line** — when appending §29 to STRESS-TEST-SCENARIOS.md
  the fuzzy matcher duplicated "out of" ("out of out of scope"); I re-read and corrected the anchor. As
  with prior sprints: re-read after a paged-doc patch.

## Open issues / next work (the honest frontier after Sprint 29)
- **The marker still never CHOOSES a different option for the machine — the §6 human always does.** A
  genuinely capacity-constrained OPTIMIZATION that RE-RANKS the recommendation stays explicitly out of
  scope of the deterministic advisory stance. This is a positive boundary (the marker is a reason, not
  a choice) but it is the frontier the next sprint would face if we wanted the recorded capacity +
  requirements to MOVE the recommendation — which the prompt forbids.
- **A per-option requirement that is NOT unit-coupled to the capacity remains non-derivable.** The
  engine labels infeasibility only where a recorded authority `capacity` {value, load} AND a recorded
  per-option requirement both exist. An org with no capacity value/load, or an option with no recorded
  requirement, carries no infeasibility label. This is correct (the engine never invents a requirement),
  but it means a per-option requirement in a DIFFERENT unit (no capacity VALUE to subtract) can't be
  compared — a unit-coupled comparison requires the recorded descriptor.
- **`band_variance: "minmax"` still equals `"all"`** (Sprint-24 finding stands).
- **The horizon-wide band remains a recorded spread, not a stochastic forecast** — probabilistic /
  adaptive stays out.

No normative gap surfaced -> SPEC stays v0.22.