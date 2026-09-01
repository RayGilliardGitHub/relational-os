# Sprint 14 — summary

**Goal.** Make the evidence-reconciliation RULE layer itself config-authorable — the last code hinge
Sprint 13 left (only the parameters of one rule were config; a new rule needed a new engine function)
— then re-test the §16 verdict. Done: the rule layer is now a config-selected, registry-backed
capability; the choice of rule CHANGES a dispute's outcome; additive, frozen ontology, SPEC v0.22, ~$0.

## What was built (instances/contested_reality/)
- **Config-authorable reconciliation rule layer** in `adjudication_engine.py`: `eng.RULES` is a
  deterministic registry (name → pure function); `reconcile` dispatches on `cfg["reconcile"]["rule"]`.
  `cfg["reconcile"]` accepts `{rule, params}` (and the legacy flat shape, so deli/cove configs are
  byte-untouched). New rule = a registry entry + a pure function, reusable by config across orgs.
  Ships THREE working rules: `best-reliability-threshold` (verbatim Sprint-13 → deli/cove reproduce),
  `strict-anchor-only` (only ANCHORED evidence admissible), `recency-weighted-threshold`
  (reliability × deterministic time-decay against an explicit `as_of`).
- `adjudication_configs.py`: an `inspect` org (Vigilant QA, $54k goods-QC acceptance) + `RULE_VARIANTS`
  (best/anchor/rec) — only `reconcile` (and the label suffix) differ.
- `run_rule_comparison_demo.py`: drives the SAME dispute through the SAME engine under all three
  rules and asserts the rule layer is real — the rule choice flips the outcome.
- `conformance_adjudication.py`: now validates 5 labels (deli, cove, inspect-best/anchor/rec).
- `docs/USER-AUTHORABLE-RULE-LAYER.md` + an additive update to `docs/GENERALIZED-ADJUDICATION.md`.

## Verified output (all exit 0, ALL PASS)
- **Rule layer proof:** `python3 run_rule_comparison_demo.py` →
  `best-reliability-threshold` DETERMINES *rework-partial-credit* (epistemic RESOLVED_DETERMINED,
  lifecycle CLOSED); **`strict-anchor-only` and `recency-weighted-threshold` both resolve UNRESOLVED**
  (epistemic INSUFFICIENT_EVIDENCE, OPEN). A claim DISPUTED under best-rel (support 0.90) is
  UNDETERMINED under strict-anchor (0.0, testimony inadmissible); `passed` flips DETERMINED(0.97) →
  DISPUTED-only(0.84 / 0.786). Trust untouched (0.80) under every rule; authority preserved; all
  rankings deterministic; three per-claim support maps pairwise distinct; every variant ends in a
  lawful terminal state. **Same engine, only `reconcile` data changed.**
- **Sprint-13 reproduction:** `python3 run_adjudication_engine_demo.py` (deli/cove) → RESULT: ALL
  PASS; two-consecutive-run diff (timestamp-normalized) = 0 non-timestamp differences → byte-identical
  up to the clock.
- **Conformance:** Sprint-0 venv `conformance_adjudication.py` → C1–C5 ALL PASS over 5 labels
  (49 `$defs`, 23–24 instances each).
- **Full non-regression (all exit 0):** the four prior contested-reality demos + conformances
  (dispute, interest, tradeoff, lifecycle); sectors `build_all.py` + `conformance_all.py`; S5
  reference demo + all-six conformance; agent demo + conformance.
- **Frozen invariants:** SPEC.md hash unchanged (v0.22); schema hash unchanged, 49 `$defs`; `ros/`
  git-clean (untouched); new fixtures mint no URI scheme outside the established §3/C16 base + cap.

## §16 verdict
Moves from **B+ — materially toward A** to **argued "A — Yes" for config-selected, registry-backed
rule authoring** — but honestly still not an unconditional text-DSL "A". The rule *selection* and
*every parameter* are now user-authorable config, and a rule choice demonstrably moves a
determination-vs-UNRESOLVED outcome with zero engine change. What remains authored is the pure
support-*mapping body* (a Python function in the registry), not a config-textural micro-DSL the
operator writes entirely in data. That boundary (the rule BODY vs rule SELECTION) is the precise seam
for a clean A and is specified — not faked — as the natural Sprint 15 step.

## Open issues / next work
- A user-authored textual rule DSL (a declarative config-rule spec compiled to the support function)
  would let the §16 claim be made unconditionally. Directly specified in `sprints/sprint-15/PROMPT.md`.

## Docs touched (no SPEC bump)
- `contested_reality/docs/USER-AUTHORABLE-RULE-LAYER.md` (new), `GENERALIZED-ADJUDICATION.md` (update)
- `instances/README.md` (Sprint-14 entry)
- `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` ("Update after Sprint 14")
- `sprints/sprint-14/plan.md`, `work/1–4-plan.md`, `notes/findings.md`, `summary.md`
- `sprints/sprint-15/PROMPT.md` (next prompt)
- `instances/contested_reality/`: `adjudication_engine.py`, `adjudication_configs.py`,
  `run_rule_comparison_demo.py`, `conformance_adjudication.py`