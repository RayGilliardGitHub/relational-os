# Sprint 17 — Decision Learning at the reconciliation layer (the learned rule, honest + additive)

generated 2026-09-01T05:39:57Z  |  learned rule library entry `calibrated-threshold-091`  |  SPEC v0.22, 49 $defs, URI cap

The §7K.1 loop `Decision->Expected->Actual->Variance->WHY->change-future-policy` is applied to the reconcile **threshold**. It learns the RULE's parameter from a recorded, realized outcome — it does NOT learn the answer to any case. **Contained**: Trust is never touched (S5 only), `determination_policy` (the §6 human's call) is never edited, the ledger is append-only (a NEW `rule://` + `decision://` + one signed event), and the update is rebound from an explicit `[lo, hi]` + explicit prior threshold (never the wall-clock).

## Learning episode A → the realized outcome
- **inspect-learn-a** driven under `best-reliability-threshold` @ threshold **0.95** → determination `rework-partial-credit`; realized outcome value **0.90** recorded additively (signed event). The bar demanded 0.95 but the realization held at 0.90 → the threshold was **too strong**.
- `learn_threshold(prior=0.95, realized=0.90, lr=0.8, [0.55,0.95])` → **0.91** (changed=True, evidence-gated, clamp-bounded, deterministic).

## Learning feeds the RULE LIBRARY (append-only signed record)
- NEW named library spec **`calibrated-threshold-091`** added to `adjudication_configs.RULE_LIBRARY` (aggregate `max`, additive `learned_threshold=0.91`/`calibrated_from`/`bound`/`why`).
- Signed append-only record: `rule://inspect-learn-a/reconcile-rule` (kind=PROCEDURE) + `decision://inspect-learn-a/reconcile-learning` + event — the ledger's prior entries were UNCHANGED (append-only proven).

## A SECOND, distinct dispute re-driven under the learned rule
- **inspect-learn-b** — a genuinely different predicate set (A and B claim/evidence URIs disjoint) — driven once under the LEARNED rule (`rule_spec` = RULE_LIBRARY[`calibrated-threshold-091`], threshold 0.91).
- winning claim support **0.93**: under the OLD 0.95 → uncertainty=True, `determined=[]` (would be UNRESOLVED); under the LEARNED 0.91 → **determined rework-partial-credit (RESOLVED_DETERMINED)**. Only the learned threshold differs — a real cross-dispute flip.

## Cross-org reuse (a library, not a one-case patch)
- **deli-learn** (freight — a genuinely different org) reuses the SAME `RULE_LIBRARY['calibrated-threshold-091']` dict (`is`-identity) → determination `partial-settlement`.

## §7L Q7/Q8 — ACTIVE reconcile rule, its source, and learned-or-not + WHY
- **inspect-learn-a**: ACTIVE rule = `registry (best-reliability-threshold)` → determination `rework-partial-credit`; learned-this-run = False; why: not changed this run — it IS the pre-learning baseline.
- **inspect-learn-b**: ACTIVE rule = `rule-library (learned `calibrated-threshold-091`)` → determination `rework-partial-credit`; learned-this-run = True; why: changed this run — the learning step's realized outcome (0.90 < prior 0.95) recalibrated the threshold to 0.91 so this modulo-evidenced dispute is no longer wrongly UNRESOLVED.
- **deli-learn**: ACTIVE rule = `rule-library (learned `calibrated-threshold-091`, cross-org reuse)` → determination `partial-settlement`; learned-this-run = False; why: reused an already-recorded learned rule; no learning step ran on this org this run.

## Honest §16 verdict
**Calibrated re-authoring, not autonomous learning.** The engine deterministically recalibrates one reconcile parameter (the threshold) from a realized outcome — a bounded, evidence-gated, explicitly-clamped authoring action. It proposes and records a reusable rule; it does NOT learn an open-ended answer, does not move Trust (S5 only), does not change the §6 human's `determination_policy`, and appends rather than rewrites history. That is a real and valuable capability accurately labeled as calibrated parameter re-authoring — the standard, honest name for updating a rule from outcomes without subverting authority.

_Additive report; frozen ontology, SPEC v0.22, 49 $defs. Trust only ever moved by S5._