# Constellar Freight — §7L cockpit question 7 (configured adjudication episode)
generated 2026-09-01T05:08:28Z  |  ledger events 24  graph objects 32  |  label `deli`

## 7. WHAT ARE OUR OPTIONS?  (options incl. do-nothing + trade-off — §7K.1)
- dispute: `dispute://deli/delivery`  status **RESOLVED**  lifecycle **CLOSED**  epistemic **RESOLVED_DETERMINED**
- business model (weights, Σ=1.0): {'evidence': 0.35, 'contractual': 0.3, 'relationship': 0.2, 'cost': 0.15}

| utility | option | §6 gate |
|---|---|---|
| 0.728 | partial-settlement |  |
| 0.665 | conditional-resolution |  |
| 0.620 | accept-company-full-payment |  |
| 0.435 | request-more-evidence |  |
| 0.400 | unresolved |  |
| 0.385 | external-adjudication |  |
| 0.380 | escalate |  |
| 0.285 | accept-customer-refund | FLOOR-GATED |

- machine-eligible best (non-gated, §6): **partial-settlement** @ 0.728
- §6 floor-gated (excluded from machine auto-pick): ['accept-customer-refund']
- do-nothing / UNRESOLVED baseline present: True (never forced winner)
- recommendation (#8) with the authority it requires (§7J.9): adopt `partial-settlement` under `authority://deli/adjudicate` (confidence 0.7)
- human determination: **partial-settlement** (the §6 adjudicator's authoritative call; the machine can only recommend)
- trade-off: trade-off[delivery; business-model {'evidence': 0.35, 'contractual': 0.3, 'relationship': 0.2, 'cost': 0.15}]
  0.728  partial-settlement
  0.665  conditional-resolution
  0.620  accept-company-full-payment
  0.435  request-more-evidence
  0.400  unresolved
  0.385  external-adjudication
  0.380  escalate
  0.285  accept-customer-refund FLOOR-GATED
  => machine-eligible best (non-gated): partial-settlement (gated: ['accept-customer-refund'])

_Rendered additively from the configurable adjudication engine (SPEC v0.22, frozen ontology, §7L — options incl. do-nothing + trade-off). Same engine, any configured org._