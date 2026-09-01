# work/3 — plan: conformance over the new fixtures + full non-regression

Do FIRST: work/2 done, `run_rule_library_demo.py` ALL PASS (real output above) driving
`inspect-majority-lib`, `deli-majority`, `inspect-corroboration`, `cove-corroboration`,
`inspect-max098` with fixtures emitted and the Q7 report + rule-library report written.

## Step 1 — conformance over the 5 new labels
`conformance_adjudication.py` labels extended (done) with the 5 Sprint-16 library labels →
**13 labels total**. Run with the Sprint-0 venv → expect C1–C5 ALL PASS for all 13.

## Step 2 — full non-regression (all exit 0)
Re-run every prior suite fresh so nothing regressed by the primitive/library additions:
- `run_rule_authoring_demo.py`, `run_rule_comparison_demo.py`, `run_adjudication_engine_demo.py`
  → ALL PASS; deli/cove byte-identical up to the clock (their registry best-rel reconstitute is
  byte-identical to before — asserted by the unchanged engine + the prior runners).
- `run_rule_library_demo.py` → ALL PASS.
- `conformance_adjudication.py` (13 labels) → ALL PASS.
- the 4 prior contested-reality demos + conformances (dispute / interest / tradeoff / lifecycle).
- sectors `build_all.py` + `conformance_all.py` → ALL SECTORS PASS.
- S5 reference `run_s5_demo.py` + `run_s5_conformance.py` → ALL PASS.
- agent `run_agent_demo.py` + `conformance_agent.py` → ALL PASS.

## Step 3 — invariants re-verified
SPEC.md hash `d10f0010…` (v0.22), schema hash `7fc38c8c…`, **49 `$defs`**, `ros/` source
untracked-modified 0, no new URI scheme (`grep` the new fixtures for any non-catalog noun),
no `qk` leak. deli/cove original configs unchanged.

DoD: every command above exit 0; invariants hold; the new fixtures C1–C5 green.