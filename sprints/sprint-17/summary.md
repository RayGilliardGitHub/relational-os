# Sprint 17 — summary

**Goal.** Take on Sprint 13's explicitly-optional `decision_learning.py` (realized-cost learning that
was never wired into the reconcile RULE choice) and build an honest **decision-learning step at the
reconciliation layer**: define what "a better reconciliation rule" means from RECORDED, realized
outcomes (not hindsight on the same case), learn the rule's `threshold` as an additive,
clamp-bounded, evidence-gated update, prove it is **contained** (no Trust move — S5 only; no
human-authority lowering — `determination_policy` intact; ledger append-only — no rewrite; explicit
bound), feed the learned rule into the **RULE LIBRARY** as a new named spec, re-drive a SECOND,
distinct dispute with it, and render a §7L Q7/Q8 cockpit line. Done: deterministic,
clamp-bounded learner; learning→library→future-dispute flow across 2 distinct disputes + a
cross-org reuse; containment asserted real; honest §16 verdict = **calibrated re-authoring**.
Additive, frozen ontology, SPEC v0.22, ~$0.

## What was built (instances/contested_reality/)
- **`reconcile_learning.py`** (new, additive, pure stdlib): `learn_threshold(prior_threshold,
  realized_value, learning_rate, lo, hi, eps)` — `new = clamp(prior + lr·(realized − prior), lo, hi)`,
  `changed = |delta| >= eps`, deterministic (explicit inputs, never the wall-clock); the learning
  feed-through `build_learned_library_spec` (a NEW named `RULE_LIBRARY` rule_spec with additive
  learned fields); and `record_learned_rule` / `record_realized_outcome` (append-only signed event +
  `rule://` kind=PROCEDURE + `decision://` with `rules_applied`).
- **Config data** (`adjudication_configs.py`): `INSPECT_BATCH_A` / `INSPECT_BATCH_B` (two genuinely
  distinct goods-QC batch disputes via the data-only `inspect_batch` helper) + `LEARN_HYPER`. Engine
  and prior configs untouched.
- **`run_reconcile_learning_demo.py`** (exit 0 = ALL PASS): episode A (0.95 threshold) → realized
  outcome 0.90 → learn 0.91 → learned spec `calibrated-threshold-091` added to `RULE_LIBRARY` +
  append-only signed record → episode B (distinct dispute) driven once under the learned rule
  (0.93-support claim DETERMINES vs old 0.95 UNRESOLVED — a real cross-dispute flip) → `deli-learn`
  reuses the SAME learned dict (`is`-identity) → containment contract asserted → §7L Q7/Q8 line.
  Emits 3 new fixture families + reports.
- **`conformance_adjudication.py`** now validates **16 labels**, C1–C5 ALL PASS, 49 `$defs`.

## Verified output (all exit 0, ALL PASS)
- **Cross-dispute flip (real, only the learned threshold differs):** `inspect-learn-b`'s winning-claim
  support 0.93 — old 0.95 reconcile → `determined=[]`, uncertainty True (UNRESOLVED); learned 0.91 →
  determined → `rework-partial-credit` CLOSED. Proven as a derived reconcile of the SAME evidence.
- **Learning→library→reuse:** learned rule `calibrated-threshold-091` is a NEW `RULE_LIBRARY` entry;
  reused by `is`-identity on `inspect-learn-b` AND `deli-learn` (a genuinely different org) → a
  library, not a one-case patch.
- **Learner properties:** deterministic (recompute-identical), clamp-bounded (0.55 ≤ 0.91 ≤ 0.95),
  evidence-gated (sub-eps signal → changed=False), rebound from an explicit prior + bound.
- **Containment:** every org's `trust://` stays 0.80 (S5 only); every determination carries its
  configured `authority://`; `determination_policy` byte-identical before vs after learning; the
  ledger grew 13 → 15 events with every PRIOR event byte-identical (append-only proven element-wise);
  the learned `rule://` (PROCEDURE) + `decision://` (`rules_applied`) are new objects, none rewritten.
- **Non-regression:** rule_library / authoring / comparison / adj_engine, the 4 prior CR demos +
  conformances, sectors `build_all.py` + `conformance_all.py`, S5 reference demo + conformance, agent
  demo + conformance — all exit 0. deli/cove byte-identical. SPEC v0.22, schema hash `7fc38c8c`, 49
  `$defs`, `ros/` source git-clean; new fixtures mint only catalog schemes (incl. `rule`), no new noun.

## §16 verdict
**Calibrated re-authoring — not autonomous learning.** The engine deterministically recalibrates ONE
reconcile parameter (the threshold) from a recorded, realized outcome, within an explicit
`[lo, hi]`, gated by `eps`, and records the result as an append-only, reusable `RULE_LIBRARY` entry.
It learns the RULE's parameter, not the answer to any case; it cannot move Trust (S5 formula only),
cannot edit `determination_policy` (the §6 human's authoritative call), and cannot rewrite the ledger.
That is a real and defensible capability accurately named **calibrated re-authoring** — the standard,
honest label for updating a rule from outcomes without subverting authority. What it is NOT is the
machine silently moving its own goalposts.

## Open issues / next work
- **Q7/Q8 is currently rendered in the runner reports, not wired into the generic engine's own §7L
  cockpit render.** Sprint 16 already flagged this; Sprint 17's Q7/Q8 line is rendered per-org in the
  learning runner's `cockpit-q7-q8-reconcile-learning.md`. Making the ACTIVE rule + source +
  learned-or-not a first-class line in `adjudication_engine.py`'s own cockpit output (Q7/Q8) is the
  natural next thread.
- The (intentionally bounded) learning primitive can be extended to other reconcile parameters
  (e.g. a `support_floor`, or a `prior` for `bayesian-combine`) with the same clamp-gate discipline.
- The residual rule-authoring seam from Sprint 16 — an op the vocabulary still cannot name (e.g. a
  provenance-conditional if/then) — remains; a next primitive could close a slice of it.

## Docs touched (no SPEC bump)
- `contested_reality/docs/RECONCILE-LEARNING.md` (new)
- `contested_reality/docs/USER-AUTHORABLE-RULE-LIBRARY.md` (Sprint-17 appendix: learning → the library)
- `instances/README.md` (Sprint-17 entry)
- `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` ("Update after Sprint 17")
- `sprints/sprint-17/plan.md`, `work/{1,2,3}-plan.md`, `notes/findings.md`, `summary.md`
- `sprints/sprint-18/PROMPT.md` (next prompt)
- `instances/contested_reality/`: `reconcile_learning.py`, `run_reconcile_learning_demo.py`,
  `adjudication_configs.py`, `conformance_adjudication.py`