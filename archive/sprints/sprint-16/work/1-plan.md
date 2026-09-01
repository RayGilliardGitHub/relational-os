# work/1 — plan: the NEW `bayesian-combine` primitive + the named RULE_LIBRARY

Do FIRST (no build before this is read): the baseline is already locked green (real output above:
rule_authoring / rule_comparison / adj_engine ALL PASS, 8-label conformance ALL PASS, sectors,
agent, S5 ALL PASS; SPEC/schema/49-defs/ros clean).

## Step 1 — engine: add `bayesian-combine` to `SPEC_VOCAB` (general + deterministic + strict)
In `instances/contested_reality/adjudication_engine.py`:
- `SPEC_VOCAB`: add `"bayesian-combine"` (frozenset is purely additive; the 3 registry rules, the
  shared `_derive`, and all existing ops stay byte-identical).
- `_aggregate`: `if op == "bayesian-combine"` → combine per-source values as independent likelihoods
  `v_i = P(claim | source_i)` under Bayes with explicit `spec["prior"]`:
  `posterior = O/(1+O)` where `O = odds(prior) · Π_i (v_i/(1−v_i))`; returns `round(…, 4)`.
  - `prior` required, strictly in (0,1); empty source set → posterior = `prior` (no evidence → prior).
  - a source `v == 1.0` → posterior 1.0 (a certain source pins the claim); `v == 0.0` → posterior 0.0.
  - deterministic: only explicit params, no wall-clock; ignores `verity.confidence` weight (each
    independent source = one equal likelihood — distinct from `weighted-mean`).
- `compile_rule_spec`: when `op == "bayesian-combine"`, require `spec["prior"]` present and
  `0 < prior < 1` (int/float), else `ValueError` loudly (missing/≤0/≥1/non-numeric all rejected).
  Keep all existing validations intact.

## Step 2 — configs: the named RULE_LIBRARY + library-reuse org variants
In `instances/contested_reality/adjudication_configs.py` (SCENARIOS / RULE_VARIANTS /
SPEC_AUTHORED_RULES / DELI / COVE / INSPECT all untouched — deli/cove byte-identical invariant):
- `RULE_LIBRARY: dict[str, dict]` — named rule specs defined ONCE, reused by reference by any org:
  - `"strict-anchor-only"`        (parity spec, aggregate max, kinds [ANCHORED])
  - `"recency-weighted-threshold"`(parity spec, aggregate max, decay given)
  - `"majority-of-sources"`       (aggregate majority, source_threshold 0.92)
  - `"independent-corroboration"` (aggregate bayesian-combine, value_field reliability, prior 0.6) — the NEW primitive as a library rule.
- Library-reuse org variants (the established `inspect_variant`/`inspect_spec_variant` pattern — new
  labels, same org data, only `reconcile` differs using a RULE_LIBRARY entry by name):
  - `DELI_MAJORITY`  — label `deli-majority`, DELI data, `reconcile` = RULE_LIBRARY["majority-of-sources"] + threshold 0.92 / floor 0.55.
  - `INSPECT_CORROB` — label `inspect-corroboration`, INSPECT data, `reconcile` =
      RULE_LIBRARY["independent-corroboration"] + threshold **0.98** / floor 0.55 (the flip threshold:
      best/max 0.97 clears nothing → UNRESOLVED; bayesian combine 0.84+0.97 → 0.9961 clears → CLOSED).
  - `COVE_CORROB`   — label `cove-corroboration`, COVE data, `reconcile` =
      RULE_LIBRARY["independent-corroboration"] + threshold 0.90 / floor 0.55 (the new rule usable as
      data by a genuinely different second org).
- A small helper `org_under_library_rule(cfg, label, rule_name, extra_params)` to build each variant
  referencing the shared RULE_LIBRARY dict (proving reuse of the SAME dict, not a fresh copy).

## DoD (work/1)
- `python3 run_adjudication_engine_demo.py` (deli/cove) still ALL PASS; deli/cove byte-identical
  up to the clock. `run_rule_authoring_demo.py` + `run_rule_comparison_demo.py` still ALL PASS.
- `python3 -c` import checks: `RULES` unbroken; `SPEC_VOCAB` now 7 ops incl. bayesian-combine;
  bad crib `prior` (`0`, `1`, `1.5`, missing) raises ValueError; good `prior=0.6` compiles.