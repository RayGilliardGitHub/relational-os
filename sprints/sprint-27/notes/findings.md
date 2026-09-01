# SPRINT 27 — NOTES / FINDINGS

## Assumptions that mattered
- **The marker's home is a PARALLEL block, not per-option mutation.** The frozen `rank` owns `cfg`
  `options` + the ranked list; `cockpit_q7q8`/`render_tradeoff` build the `q7.options`/`q7.tradeoff`
  bytes. To keep those byte-identical, the capacity constraint rides as an additive
  `capacity_constraint` block on BOTH `q7` and `q8`, with the per-option flags INSIDE it
  (`options_flagged`) rather than on the option dicts. This is the prompt's preferred decision and it
  passes the "Q7 option set unchanged" assertion trivially-by-construction (the `options` list is
  never touched).
- **A per-option capacity requirement is never recorded, so `capacity_infeasible` is never derivable**
  — the honest ceiling is `capacity_risk`. The ONLY recorded capacity-consumption datum is the
  org-level `load`; nothing on the trade-off options carries a per-option capacity figure. So the rule
  marks non-baseline options `capacity_risk` only at at-capacity/deficit, and the baseline
  (do-nothing/UNRESOLVED — consumes no capacity) is never flagged. This keeps every value recorded-data
  only and never invents a requirement.
- **Q8 must agree with Q9 BY CONSTRUCTION, not just numerically.** The cleanest fix was to EXTRACT the
  Sprint-26 Q9 `capacity_planning_attention` rule into a shared `_capacity_reason(capacity_obj,
  band_horizon, direction)` helper and have BOTH blocks call it. The Q9 block's output is provably
  byte-identical (the Sprint-26 regressor `run_forecast_horizon2_demo.py` still ALL PASS), and the Q8
  `reason`/`flag` equal the Q9 label/flag by construction — one rule, no drift.
- **Absence is the byte-identity contract.** Only `deli-varmax-cap` (recorded capacity + band +
  threshold) carries `capacity_constraint`; `deli-forecast`/`deli-varmax` (band but NO capacity),
  `deli-flat2` (no band), and no-data `deli` carry it on neither q7 nor q8.
- **The capacity-constraint marker is a dict-level cockpit field, not a graph object** — so the
  fixtures' instance count stays 26 (Sprint-26 parity); it is C2-safe (no
  `at|time|deadline|expires|expiry|effective|due|since` suffix on `capacity_constraint`/
  `recorded_capacity`/`horizon_band`/`reason`/`options_flagged`/`note`/`flag`).

## Verified (real tool output, all exit 0)
- **Green baseline captured FIRST** (Sprint-26 state): all 11 CR runners + 5 conformances (venv) +
  `build_all`/`conformance_all` (12 sectors) + S5 reference demo/conformance + agent demo/conformance
  → all exit 0; schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22.
- **After the additive change:** new `run_forecast_horizon3_demo.py` → **ALL PASS (all curated checks;
  64 PASS lines incl. the runner's own run_scenario rehearse)**; and EVERY runner/conformance in the
  baseline re-run → ALL PASS (full non-regression FAIL=0). Schema hash unchanged `7fc38c8c…`.
- **Sprint-26 byte-identity after the Q9 refactor:** `run_forecast_horizon2_demo.py` still ALL PASS
  (Q3 strict-prefix suffix + Q9 `capacity_planning_attention` `{flag: False, why: "… derived
  headroom …"}` byte-identical). `run_forecast_horizon_demo.py` (Sprint 25) + `run_forecast_variance_*`
  also ALL PASS.
- **New marker proof:** `deli-varmax-cap` Q7 AND Q8 carry `capacity_constraint`
  `{recorded_capacity: "500.0 resolutions/day (load 0.72)", horizon_band: {low: 0.62, high: 1.02},
  reason: "headroom", flag: false, options_flagged: {}}` — headroom (load 0.72 < 1.0; horizon worst-side
  0.62 < capacity 500.0) → **NO option flagged**. `deli-forecast`/`deli-varmax`/`deli-flat2`/`deli`:
  NO `capacity_constraint` key. For every org Q7 `options` + Q8 `recommendation`/`machine_eligible_best`
  EQUAL `cockpit_q7q8` (no §6 overrule, no re-rank). Q8 `reason` == Q9 label by construction.
- **New-org fixtures pass Sprint-0 C1–C5** (all four recorded orgs, 26 instances each, 49 `$defs`).
- Schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` + schema + sector `configs.py` untouched,
  no new noun. `git status` (source) shows only `adjudication_engine.py` + the new
  `run_forecast_horizon3_demo.py` + the docs; the rest is regenerated-artifact churn.

## Pitfalls encountered
- **A bogus placeholder in an assertion silently forces a FAIL.** I first wrote
  `isinstance(vcc8, dict) and "never an invention" in " "  # placeholder no-op` — `"never an
  invention" in " "` is `False`, so that assertion would have ALWAYS failed. Caught before running:
  removed the placeholder. Lesson: never leave a throwaway predicate in a `_report` condition —
  re-`ast.parse` + RUN every new runner, and skim the FAIL lines, not just the RESULT line.
- **`vcc8["flag"] == cpa["flag"] is False` parses as chained comparison**, not as intent — `(a == b)
  and (b is False)`. It happened to be True here, but it is clearer and safer to write
  `cpa is not None and cpa["flag"] is False and vcc8["flag"] is False`. Avoid `== x is False` chain.
- **Runner import needs the right `parents[N]` index for the `ros` path** (a known footgun): in an
  ad-hoc check I used `HERE.parents[0]` (= `instances/`) which made `ros` unresolvable; the runners
  anchor `ROS = INSTANCES.parents[0] / "sprints/sprint-5/artifacts"` where `INSTANCES = HERE.parent`,
  i.e. the repo root — so it is `HERE.parents[1]` from `contested_reality`. Same off-by-one class as
  prior sprints.
- **Reusing `r26.build_orgs()` (Sprint 26) for the Sprint-27 runner guarantees the source recorded
  data is byte-identical** (same orgs, same series/variance/capacity) — the marker is the ONLY added
  bytes, which is exactly the superset contract.

## Open issues / next work (the honest frontier for Sprint 28)
- **The marker is a reason, not a choice.** It never CHOOSES a different option for the machine — the
  §6 human always does — so an org at-capacity/deficit still sees the same machine-eligible set, now
  with `capacity_risk` flags on the capacity-consuming options. A genuinely capacity-constrained
  optimization that RE-RANKS the recommendation for the machine stays out of scope of the
  deterministic advisory stance.
- **`capacity_infeasible` is structurally unreachable** without a RECORDED per-option capacity
  requirement (the engine never invents one). A future sprint could add such a recorded descriptor
  (Sprint-16 vocabulary discipline) to enable real infeasibility labeling — unit-coupled and additive,
  never invented.
- **The rule compares the horizon band (a rate/magnitude) to the recorded capacity VALUE (a volume)
  where units differ**; the defense remains "state the recorded numbers and label the reason." A
  unit-coupled capacity-consumption comparison must be a recorded descriptor, not an invented one.
- **`band_variance: "minmax"` still equals `"all"`** (Sprint-24 finding stands).
- **The horizon-wide band remains a recorded spread, not a stochastic forecast** — probabilistic /
  adaptive stays out.

No normative gap surfaced -> SPEC stays v0.22.