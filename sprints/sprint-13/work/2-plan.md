# work/2-plan.md — §7L cockpit Q7 render + Decision-Learning (optional, additive)

**Objective (optional Sprint-13 items, kept additive + in-build):** surface the generalized
adjudication on the §7L cockpit question 7, and make the business-model objective itself learned.

## §7L cockpit Q7 render
- Reuse the existing cockpit/report render path (no new renderer universe; `sector_scene.py`
  untouched). `render_q7()` in `run_adjudication_engine_demo.py` writes an additive
  `artifacts/adjudication/reports/cockpit-q7.md` + `.json` (plus per-label `cockpit-q7-{label}`.
  copies) for the configured episode: business-model weights, ranked options with utilities, §6
  floor-gated set, machine-eligible best, do-nothing/UNRESOLVED baseline, recommendation with the
  required authority, the human determination, and the trade-off. Proven: rendered for BOTH `deli`
  and `cove`.

## Decision-Learning / realized-cost weights (tested, exit 0)
- `decision_learning.py`: `update_weights` computes, deterministically + clamp-bounded, a new
  weight vector from the variance between the computed expected utility of the chosen option and
  a recorded realized `outcome_value`; `record_learning` appends a signed learning event carrying
  `realized_cost_usd`, `outcome_value`, `expected_utility`, `variance`, and `learned_weights`
  additively on the chosen `decision://` and the dispute (merge-not-replace).
- Success: both scenarios report variance + realized cost + learned weights; new weights remain in
  [lo,hi] and renormalise to Σ=1.0; never rewrites history; never touches Trust.

## Conflicts / corrections surfaced
- Exact-vs-substring membership bug in the engine's UNRESOLVED-availability check (fixed to `any`).
- Decision `determination` lives under its `detail`, not top-level (assertion reads the dispute).