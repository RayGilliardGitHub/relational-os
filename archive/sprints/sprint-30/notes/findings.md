# SPRINT 30 — NOTES / FINDINGS

## Assumptions that mattered
- **NO engine change was required (unlike Sprint 29).** Sprint 29's `_per_option_capacity_flags` already
  labels ANY option — including the recommended one — `capacity_infeasible` when its recorded requirement
  > available. So the "recommended option is infeasible" story is pure recorded data + a new runner. I
  verified `adjudication_engine.py` sha256 = `a60f8f7…` BEFORE the new runner and AFTER — identical. This
  is the cleanest kind of additive proof: the whole certification point is the org story + the assertion,
  not a capability change.
- **The machine-eligible best / Q8 recommendation for DELI is `partial-settlement`** (utility 0.7275,
  non-gated; `accept-customer-refund` is the only floor-gated option). Verified pre-plan by running
  `eng.rank(ac.DELI)` + `machine_eligible_best`. So making `partial-settlement` `capacity_infeasible`
  exercises the boundary AT the recommendation, not beside it.
- **AVAILABLE = recorded capacity VALUE − recorded load = 500.0 − 1.3 = 498.7.** Same unit-coupled
  arithmetic as Sprint 29 (authority holds both the `capacity` and `capacity_requirements`). I kept the
  horizon worst-side low (0.62) well below the 500.0 capacity so `_capacity_reason` returns a clean
  single `at-capacity` (not deficit) — same defense as `deli-infcap`.
- **The per-option requirement map records 499.0 for `partial-settlement` and ≤ available for the other
  6 non-baseline options**, so EXACTLY ONE option (the recommended one) is `capacity_infeasible` and the
  other 6 are `capacity_risk` — the sharpest possible statement: "the only option the machine would
  recommend is the only one the recorded capacity says can't run."
- **Baseline `unresolved` records NO requirement and is NEVER flagged** (the engine skips it in the
  per-option helper AND it consumes no capacity).

## Verified (real tool output, all exit 0)
- **Green baseline captured FIRST** (Sprint-29 state): all 12 prior CR demo runners + the 5 CR
  conformances (Sprint-0 venv) + `build_all`/`conformance_all` (12 sectors) + S5 reference
  demo/conformance + agent demo/conformance → all exit 0. Schema raw sha256 `7fc38c8c…`, 49 `$defs`,
  SPEC v0.22. The S5 + agent scripts live OUTSIDE `instances/contested_reality`: S5 reference in
  `sprints/sprint-5/artifacts/` (`run_s5_demo.py` + `run_s5_conformance.py`), agent in
  `instances/agent_demo/` (`run_agent_demo.py` + `conformance_agent.py`).
- **New runner** `run_forecast_label_vs_choice_demo.py` → **ALL PASS**. Key outputs:
  - `deli-recommend-infcap` Q7+Q8 `capacity_constraint` = `{recorded_capacity:"500.0 resolutions/day
    (load 1.3)", horizon_band:{low:0.62,high:1.02}, reason:"at-capacity", flag:true,
    options_flagged:{partial-settlement:"capacity_infeasible", 6×capacity_risk},
    per_option_requirements:{partial-settlement:499.0, ...200.0/100.0/50.0/80.0}, available_capacity:498.7}`.
  - The Q8 recommendation + machine-eligible best are STILL `partial-settlement`, and `q7.options` (8) +
    `machine_eligible_best` + `q8.recommendation` + `floor_gated` EXACTLY equal `cockpit_q7q8` — the
    marker is a REASON, never a CHOICE (the note names the UNCHANGED Q8 + the §6 human).
  - `reason` == the org's Q9 `capacity_planning_attention` label BY CONSTRUCTION (shared
    `_capacity_reason`).
- **Byte-identity regression:** the seven reused orgs carried the exact Sprint-29 output (verified by
  the runner's own PASS lines: `deli-infcap`/`deli-deficit-inf` identical `{reason, flag, options_flagged,
  per_option_requirements, available_capacity}`; `deli-varmax-cap` `{reason:"headroom", flag:False,
  options_flagged:{}}` no per-option keys; the 4 no-capacity orgs no `capacity_constraint`).
- **New-org fixtures pass Sprint-0 C1–C5** (26 instances, 49 `$defs`, ALL PASS) — ran the validator
  directly against `fixtures/deli-recommend-infcap/` by pointing `conformance.FIXTURES` at it.
- **Full non-regression** (final consolidated re-run): every CR demo + every conformance + sectors + S5 +
  agent → ALL PASS. Engine hash `a60f8f7…` unchanged; schema `7fc38c8c…`; 49 `$defs`; SPEC v0.22;
  `ros/` + schema + sector `configs.py` untouched; the ONLY new source is the runner.

## Pitfalls encountered
- **The S5 + agent scripts are NOT in `instances/contested_reality`** — I initially ran them from the
  wrong cwd and got "can't open file". The proof's verification list hides that they live in
  `sprints/sprint-5/artifacts/` (S5) and `instances/agent_demo/` (agent). Notably Sprint-0's schema dir
  is `artifacts/schema/` and there is NO `validate_fixtures.py` in it — the C1–C5 validator is
  `artifacts/conformance.py` and I ran it on a new org's fixtures by monkeypatching `conformance.FIXTURES`.
- **A literal `{{the marker is a REASON, never a CHOICE}}` placeholder** slipped into the README
  Sprint-30 heading (the Sprint-29 half-f-string lesson) — I caught and removed it (`grep -c '{{'` = 0
  confirmed across all four doc files). Re-read after each paged-doc patch.
- **Pyright noise** on the runner (unresolved `ros.substrate`, optional-dict `not in` / `-` on `None`) is
  the known, expected artifact of the runtime `sys.path` injection + optional dict access — identical to
  every CR runner; not a defect.

## Open issues / next work (the honest frontier after Sprint 30)
- **The deterministic advisory stance can label an option — even the RECOMMENDED one — as
  `capacity_infeasible` from recorded data, but it CANNOT and MUST NOT choose the replacement for the §6
  human.** This is a positive boundary (the marker is a reason, not a choice), now demonstrated at its
  sharpest AS DATA. A genuinely capacity-constrained OPTIMIZATION that MOVES the recommendation is a
  POLICY / user request, not a label, and stays firmly out of scope unless the prompt author explicitly
  asks to build it (a deliberate "re-rank for the machine" capability change).
- **The optimization SEAM, spelled out (what it WOULD need if ever wanted):** recorded per-option
  requirements already exist (`authority.capacity_requirements`, `available = capacity.value − load`),
  so the ONLY missing piece for a deterministic next-best-non-infeasible is a RE-RANK RULE: e.g. from the
  frozen `rank` utility ordering, pick the highest-utility option not labeled `capacity_infeasible`;
  unreachable if all changing options are infeasible (then the machine would fall back to the
  do-nothing/UNRESOLVED baseline — itself a policy question). That would CHANGE the Q8 recommendation
  and does NOT fit a label.
- **A per-option requirement NOT unit-coupled to the capacity remains non-derivable.** Infeasibility is
  labeled only where a recorded authority `capacity` {value, load} AND a recorded per-option requirement
  both exist in the same unit. An org with no capacity value/load, or an option with no recorded
  requirement, carries no infeasibility label — correct (the engine never invents a requirement), but it
  means a requirement in a different unit (no capacity VALUE to subtract) can't be compared.
- **`band_variance: "minmax"` still equals `"all"`** (Sprint-24 finding stands).
- **The horizon-wide band remains a recorded spread, not a stochastic forecast** — probabilistic /
  adaptive stays out.

No normative gap surfaced -> SPEC stays v0.22.