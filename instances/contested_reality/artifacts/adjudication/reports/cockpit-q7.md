# Meridian Health Plan — §7L cockpit question 7 (configured adjudication episode)
generated 2026-09-01T05:56:02Z  |  ledger events 23  graph objects 29  |  label `cove`

## 7. WHAT ARE OUR OPTIONS?  (options incl. do-nothing + trade-off — §7K.1)
- dispute: `dispute://cove/coverage`  status **RESOLVED**  lifecycle **CLOSED**  epistemic **RESOLVED_DETERMINED**
- business model (weights, Σ=1.0): {'medical_necessity': 0.4, 'safety': 0.25, 'policy': 0.2, 'cost': 0.15}

| utility | option | §6 gate |
|---|---|---|
| 0.777 | step-therapy-first |  |
| 0.740 | authorize-generic |  |
| 0.605 | escalate-to-medical-director |  |
| 0.560 | external-peer-review |  |
| 0.540 | request-more-evidence |  |
| 0.500 | unresolved |  |
| 0.480 | authorize-off-formulary | FLOOR-GATED |
| 0.280 | deny-off-formulary | FLOOR-GATED |

- machine-eligible best (non-gated, §6): **step-therapy-first** @ 0.777
- §6 floor-gated (excluded from machine auto-pick): ['authorize-off-formulary', 'deny-off-formulary']
- do-nothing / UNRESOLVED baseline present: True (never forced winner)
- recommendation (#8) with the authority it requires (§7J.9): adopt `step-therapy-first` under `authority://cove/adjudicate` (confidence 0.7)
- human determination: **step-therapy-first** (the §6 adjudicator's authoritative call; the machine can only recommend)
- trade-off: trade-off[coverage; business-model {'medical_necessity': 0.4, 'safety': 0.25, 'policy': 0.2, 'cost': 0.15}]
  0.777  step-therapy-first
  0.740  authorize-generic
  0.605  escalate-to-medical-director
  0.560  external-peer-review
  0.540  request-more-evidence
  0.500  unresolved
  0.480  authorize-off-formulary FLOOR-GATED
  0.280  deny-off-formulary FLOOR-GATED
  => machine-eligible best (non-gated): step-therapy-first (gated: ['authorize-off-formulary', 'deny-off-formulary'])

_Rendered additively from the configurable adjudication engine (SPEC v0.22, frozen ontology, §7L — options incl. do-nothing + trade-off). Same engine, any configured org._