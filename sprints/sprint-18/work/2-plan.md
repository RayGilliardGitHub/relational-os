# Sprint 18 / work — 2-plan: run_cockpit_q7q8_demo.py (the ≥3-org proof)

**Purpose:** prove the engine-native `cockpit_q7q8`/`render_cockpit_q7q8` are generic (data-only, no
per-org Python) and CORRECT for ≥2 orgs whose ACTIVE reconcile rule has DIFFERENT sources, then prove
agreement with the Sprint-16/17 runner-report lines. Exit 0 = ALL PASS.

**Orgs driven (4, spanning 3+ source classes):**
- `deli` (ac.DELI) — **registry** rule `best-reliability-threshold`. Expect source=registry,
  learned_this_run=False, why="unchanged".
- `inspect-corroboration` (ac.INSPECT_CORROBORATION) — **rule-library** spec
  `independent-corroboration` (is-identical to `ac.RULE_LIBRARY[...]`). Expect source=rule-library,
  learned_this_run=False.
- `inspect-learn-b` — a **learned** RULE_LIBRARY entry **added this run**: recompute
  `learn_threshold(0.95, 0.90, 0.8, [0.55,0.95]) -> 0.91` (LEARN_HYPER, assert deterministic +
  clamp-bounded + changed), build `calibrated-threshold-091`, drive INSPECT_BATCH_B under it, and
  `record_learned_rule` the reconcile-learning decision ON THIS ORG'S OWN ledger. Expect
  source=learned, learned_this_run=True, why = that decision's evidence-gated `detail.why`.
- `deli-learn` (ac.org_under_library_rule(DELI,"deli-learn","calibrated-threshold-091",...)) — reuses
  the SAME learned spec but records no learning decision on its own ledger. Expect source=learned,
  learned_this_run=False (the "reused a learned rule, no learning step on this org" case).

The learned spec is added to `ac.RULE_LIBRARY[lib_name]` at runtime (the established Sprint-17 pattern)
so `org_under_library_rule` can reuse it by name AND `cockpit_q7q8(library=ac.RULE_LIBRARY)` classifies
both library + learned orgs.

**Assertions (each `[PASS]`, exit 0 = ALL PASS):**
- For every org: `cockpit_q7q8` active_rule == the reconcile's rule name/spec name; source class is the
  expected one; learned_this_run is the expected bool; why is "unchanged" OR a real evidence-gated
  recalibration string (asserts `"recalibrated"` in the why for the learned-this-run org).
- Q7 + Q8 both present: q7.options non-empty with a do-nothing/UNRESOLVED baseline; q8 has
  recommendation + authority + determination.
- Deterministic: re-call equals first call (per org).
- Agreement with runner reports: re-run Sprint-16 `run_rule_library_demo` + Sprint-17
  `run_reconcile_learning_demo` first (fresh reports), then assert engine active_rule + determination
  for `inspect-corroboration` match `cockpit-q7-rule-library.md`, and engine source/learned flags for
  `inspect-learn-b`/`deli-learn` match `cockpit-q7-q8-reconcile-learning.md` semantics. (Learned-this-run
  TRUE requires the reconcile-learning decision on that org's ledger — my runner records it there, which
  is exactly what the Sprint-17 report line asserts for inspect-learn-b.)
- No per-org Python: every org is pure config data + one generic engine call `cockpit_q7q8(cfg, sub)`.
- Containment / engineering: each driven org ends in a lawful terminal state; engine change is additive.

**Button > doc > build:** this plan precedes the build. Emits engine-native renders to
`artifacts/adjudication/reports/cockpit-q7q8-engine.{md,json}` and fixtures for the driven orgs.