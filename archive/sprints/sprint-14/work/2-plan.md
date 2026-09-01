# work/2 — the verdict-change proof: same engine, only config differs

**Objective.** Add one goods-inspection org (`inspect`) whose outcome materially changes — 
a determined option vs UNRESOLVED — **solely** by choosing a different configured reconciliation
rule, with ZERO engine-side code change between rules. Drive 3 rule variants of the SAME evidence
episode through the SAME `run_scenario` and assert the rule layer is real (per-claim dispute maps
differ; A resolves at `rework-partial-credit`, B and C resolve UNRESOLVED).

## Config (`adjudication_configs.py`, additive — NOT added to `SCENARIOS`)
One shared `INSPECT` org dict (label `inspect`, options/weights/factor_scores/authority/floor
fixed). Evidence deliberately mixed so the rule choice is decisive:
- `passed` claim ← `proof-system` ANCHORED 0.84 (recent) + `proof-audit` RECORD 0.97 (**old** 52d)
- `failed` claim ← `fail-inspector` TESTIMONY 0.90 (recent) — NO anchored evidence
Rule variants differ ONLY in `reconcile` (and the label suffix for fixture separation):
- **A** `best-reliability-threshold` (0.92/0.55): passed support 0.97 → DETERMINED; failed 0.90 → DISPUTED
  → conflict, not uncertain → resolves to `rework-partial-credit` (top non-gated, §6-gated extremes).
- **B** `strict-anchor-only` (kinds:[ANCHORED], 0.92/0.55): passed support 0.84 (recent anchored),
  failed 0.0 (testimony inadmissible) → determined empty → UNRESOLVED.
- **C** `recency-weighted-threshold` (as_of=2026-08-31, half_life 21d, 0.92/0.55): passed
  max(0.84·0.936, 0.97·0.18)=0.786, failed 0.90·0.968=0.871 → both DISPUTED, none DETERMINED → UNRESOLVED.
So a claim DISPUTED under A becomes not-DISPUTED under B (failed) and the dispute flips
DETERMINED(A) → UNRESOLVED(B, C) purely by rule selection — no engine change.

## Runner (`run_rule_comparison_demo.py`)
- Build 3 cfg copies differing only in `label` + `reconcile`; run each through `eng.run_scenario`.
- Asserts (gate exit): each main episode PASS; A determination == `rework-partial-credit`;
  B & C determination == UNRESOLVED; A.certain vs B/C.UNCERTAIN; per-claim maps differ (A: passed
  determined + failed disputed; B: only passed disputed; C: both disputed); Trust untouched; authority
  preserved; rankings deterministic.
- Emit fixtures under `artifacts/adjudication/fixtures/inspect-{best,anchor,rec}/`.
- Render additive `artifacts/adjudication/reports/rule-comparison.{md,json}` + a rule-named
  cockpit-Q7 line (optional item) naming the active rule + its verdict.

## DoD
- `python3 run_rule_comparison_demo.py` → RESULT: ALL PASS (exit 0).
- The three fixtures pass C1–C5 (work/3).
- deli/cove path unaffected (they stay off this runner).