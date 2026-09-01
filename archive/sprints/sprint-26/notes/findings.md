# SPRINT 26 — NOTES / FINDINGS

## Assumptions that mattered
- **Q3 must agree with Q6/Q8/do-nothing VERBATIM, not just numerically.** Earlier sprints rendered the
  band on Q8/do-nothing and the projection on Q6, but the Q3 attention `why` only named the single
  worst point. The clean fix is a single shared module constant (`_HORIZON_BAND_PHRASE`) that both the
  Q3 attention suffix AND the do-nothing summary format — so they cannot drift apart by construction.
  This is the Sprint-23 "strict prefix" rule applied one layer up: the new suffix goes AFTER the
  Sprint-23/24 single-worst phrase (+ any Sprint-24 band_variance source phrase), so every pre-existing
  byte survives.
- **Capacity planning is a derived REASON from recorded numbers, not a comparison engine and not a
  directive.** The units of a recorded `capacity` (resolutions/day), a recorded `load` (a fraction), a
  `band_horizon` (the projected on-time-rate spread), and a `threshold` (a rate) do not share a common
  dimension — so the honest rule is to state the recorded numbers and derive a *label*. ONE
  deterministic rule was chosen and documented: at-capacity when `load >= 1.0`; deficit when the horizon
  band's worst-side magnitude reaches/exceeds the recorded capacity value; else headroom. `deli-varmax-cap`
  (capacity 500.0/day, load 0.72, band 0.62…1.02) is headroom: 500 ≫ the band and load < 1.0.
- **Absence is the byte-identity contract.** A no-variance series (`deli-flat2`) and a no-data org
  (`deli`) get no Q3 suffix and no capacity key; an org that records a band but NO capacity
  (`deli-forecast`, `deli-varmax`) gets the Q3 suffix but NO `capacity_planning_attention` key. Only
  `deli-varmax-cap` carries the capacity key.
- **One engine file, two additive blocks.** Only `_forecast_closure`'s Q3 attention-why block and
  `cockpit_s7l`'s Q9 block were extended; frozen functions untouched; `render_cockpit_s7l` needed no
  change (its Q3/Q8/Q9 lines are generic and the new key is dict-only).

## Verified (real tool output, all exit 0)
- **Green baseline captured FIRST** (Sprint-25 state, before any edit): all 5 forecast runners +
  `run_cockpit_s7l` + `run_cockpit_q7q8` + `run_adjudication_engine_demo` + the 5 conformances
  (venv) + `build_all`/`conformance_all` + S5 reference + agent demo + conformance. Schema hash
  `7fc38c8c…`, 49 `$defs`, SPEC v0.22.
- **After the additive change:** new `run_forecast_horizon2_demo.py` -> **ALL PASS** (63 checks), and
  EVERY runner/conformance in the baseline re-run -> ALL PASS.
- **Q3 strict-prefix byte-identity:** `deli-forecast`'s Q3 `why` == the exact pre-Sprint-26 string
  (`rfv.FC_SINGLE_WHY` + the Sprint-23 band phrase) + the shared horizon suffix, asserted character-for-
  character; `deli-varmax`/`deli-varmax-cap` `why` startswith the Sprint-23 string and endswith the
  suffix (their band_source phrase is preserved in between). The Sprint-23/24/25 runners' own assertions
  (`startswith` + substring) still pass — proof the old string is a strict prefix, not a rewrite.
- **Capacity-planning byte-identity:** `capacity_planning_attention` present ONLY on `deli-varmax-cap`
  (`{flag: False, why: "… derived headroom …"}`); absent (key not present) on `deli-forecast`,
  `deli-varmax`, `deli-flat2`, and `deli`. `band_capacity_attention` untouched.
- **New org fixtures pass the Sprint-0 C1–C5 conformance** (26 instances, 49 `$defs`), driven directly
  for all four (`deli-forecast`, `deli-varmax`, `deli-varmax-cap`, `deli-flat2`). The C2 RFC3339
  temporal-suffix probe stays green (`capacity_planning_attention`/`flag`/`why` carry no
  `at|time|deadline|expires|expiry|effective|due|since` suffix).
- Schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` + schema + sector `configs.py` untouched.
  `git status` (source only) shows `adjudication_engine.py` + the new `run_forecast_horizon2_demo.py`
  + the docs; the rest is regenerated-artifact churn from running the runners.

## Pitfalls encountered
- **A dict-returning helper's fields are KEYS, not attributes.** `run_one()` returns a dict; an
  f-string using `{fc.label}` silently built the label as a replacement field and failed at runtime
  (attribute error) — fixed to `fc["label"]`. Also an f-string with a literal `{flag,why}` in prose
  was parsed as a format field (undefined names); escaped as `{{flag,why}}`. This is the same class of
  string-literal trap as prior sprints — re-`ast.parse` + runtime after every runner edit.
- **Pyright noise on guaranteed-non-None locals is a false positive.** `len(band_periods)` /
  `band_horizon["low"]` / `band_horizon["high"]` inside the `if band is not None: ...` branch of
  `_forecast_closure` are always non-None (band_periods/band_horizon are set whenever `band` is), and
  inside the Q9 `if capacity_recorded and ...` block `bh` is non-None; `ast.parse` + runtime ALL PASS
  confirm correctness. Do not "fix" them.

## Open issues / next work (the honest frontier for Sprint 27)
- **Q6 renders the projection, but the capacity-planning reason is not connected to the Q8 trade-off
  OPTIONS** — the org may RECORD a deficit/at-capacity reason yet the machine-eligible options are
  unchanged. A bounded later sprint could add a data-only capacity-constraint ADVISORY to Q7/Q8
  (which options the recorded capacity makes infeasible), still never overruling the §6 floor.
- **The capacity-planning rule compares the horizon band (a rate/magnitude) to a recorded capacity
  (a volume)** where their units differ; the current defense is "state the recorded numbers and label
  the reason." If a future sprint wants a unit-coupled comparison it must be a recorded descriptor,
  not an invented one (Sprint-16 vocabulary discipline).
- **`band_variance: "minmax"` remains the same recorded value as `"all"`** (Sprint-24 finding stands).
- **The horizon-wide band is still a RECORDED spread, not a stochastic forecast** — a probabilistic /
  adaptive model stays explicitly out of scope of the deterministic ~$0 stance.

No normative gap surfaced -> SPEC stays v0.22.