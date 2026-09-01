# 2.2-PLAN — Trust update + write

## Goal
Compute and persist scoped Trust from verified evidence, per §5, replacing the
static seeded T1 from Sprint 1 with an evidence-driven value.

## Design
Trust is keyed `(subject, target, claim, context)` per §3.14 (NOT a global score).
Cold-start T1 = the three `trust://` objects seeded in Sprint 1
(subject `org://quoteko`, context `relationship://qk/cust-cxn`):
- `org://qk/norcrete` 0.92 (claim "roofing & repair reliability")
- `org://qk/solarworks` 0.61 (same claim)
- `org://qk/generalco` 0.42 (claim "roofing reliability" — a DIFFERENT claim → must
  stay untouched, proving scope).

Equation (§5): `T_{k+1} = clamp(T_k + alpha*(outcome_k − expectation_k)*evidence_k*recency, 0, 1)`.
`alpha`=learning rate (the `weight` param), `evidence_k`=verify degree (verity
confidence), `recency`=recency multiplier, `outcome_k`∈{0,1} from 2.1, `expectation_k`=0.8.

Expected (alpha=0.5, evidence=0.98, recency=1.0, expectation=0.8):
- norcrete (outcome 0.0): 0.92 − 0.5·0.8·0.98 = **0.528**
- solarworks (outcome 1.0): 0.61 + 0.5·0.2·0.98 = **0.708**
- generalco: **unchanged 0.42** (different claim → not keyed)

## Steps
1. `update_trust(sub, subject, target, claim, context, evidence_obj, outcome,
   expectation, alpha, recency) -> trust://` — find the existing `trust://` by
   (subject,target,claim,context); compute the clamped equation; WRITE the updated
   `trust://` to the Graph + emit a signed STATE_CHANGE ledger event. Additive
   envelope fields (expected/outcome/evidence/alpha/recency_used) make each update
   auditable (schema `additionalProperties:true`).
2. Assert result is in [0,1], keyed, and persisted (graph object + signed ledger event).

## Done
- Trust value changes BECAUSE of verified evidence (not arbitrarily), stays in [0,1],
  is relationship/context-scoped, and persists to Graph + signed Ledger.