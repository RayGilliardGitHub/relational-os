# Quoteko — Business Operating Layer cockpit
generated 2026-09-01T05:45:48Z  |  ledger events 97  graph objects 160

## Business health (ledger-projected metrics)
| metric | unit | target | actual | variance | status |
|---|---|---|---|---|---|
| On-time delivery rate (`metric://qk/m-on-time`) | fraction | 0.95 | 0.857 | -0.093 | CRITICAL |
| Customer-trust score (`metric://qk/m-customer-trust`) | score | 0.9 | 1.0 | 0.1 | OK |
| Settled value (`metric://qk/m-settled-value`) | USD | 25000.0 | 24850.0 | -150.0 | WARN |

## Prioritized attention — 2 things requiring attention today
- **0.69** re-balance provider allocation (`task://qk/t-provider-rebalance`)
- **0.58** rallied follow-on delivery (solarworks) (`task://qk/t-followup-routed`)

## Exception (heartbeat, §7J.2)
- expected 0.95  actual 0.833  variance -0.117  significance CRITICAL  (5/6 ledger completions on time)
- case `case://qk/c-on-time-delivery`  status **CLOSED**

## AI recommendation (#8) with the authority it requires (§7J.9)
- recommended work: `task://qk/t-provider-rebalance`
- authority required: `authority://qk/for-operations`  confidence 0.85
- options: ['re-balance to verified on-time provider', 'gate the laggard (norcrete)', 'do nothing']  (do-nothing included: True)
- trade-off: Re-balancing concentrates work with solarworks (higher short-term concentration risk) but restores on-time fulfilment and protects scoped customer Trust; doing nothing keeps on-time below target.
- expected impact: forward-period on-time delivery returns to 1.0 (verified, rallied solarworks delivery on time).

## Verified outcome (#10) + Learning
- rallied solarworks delivery settled event://qk/s4-exchange-routed-solarworks, outcome event://qk/s4-outcome-routed-solarworks (met); evidence evidence://qk/job-routed-solarworks; forward-period on-time 1.0; solarworks Trust -> 1.0
- Learning entry: `decision://qk/s5-learning-on-time`

## §7L — the ten morning questions, answered with evidence
1. WHAT HAPPENED?  On-time contracted completions 6/7 (0.857); solarworks settled on time (ev evidence://qk/job-routed-solarworks), norcrete late; settled value 24850.0.  [ledger evidence]
2. WHAT CHANGED?  Provider re-allocation recommended; rallied solarworks delivery verified on time; cumulative forward on-time 0.857; forward-period on-time = 1.0.  [delta -> significance]
3. WHAT MATTERS?  Priority-ordered attention: re-balance provider allocation, rallied follow-on delivery (solarworks).  [§7J.5]
4. WHAT'S GOING WRONG?  On-time delivery 0.857 below target 0.95 (CRITICAL).  [§7J.2]
5. WHY?  Provider scheduling failure — norcrete missed its deadline (root SUPPORTED: scoped Trust 0.92->0.528).  [§7K.2 epistemic status]
6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.83 < 0.95; laggard keeps missing deadlines; scoped customer Trust erodes.  [§7K.1 forecast]
7. WHAT ARE OUR OPTIONS?  re-balance to solarworks; gate norcrete; do-nothing (all costed; trade-off in the recommendation).  [§7K.1 options incl. do-nothing]
8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://qk/t-provider-rebalance under authority://qk/for-operations.  [recommendation]
9. WHO DOES IT, AND AUTHORITY/CAPACITY?  agent://w-ops via delegation://qk/w-ops (delegation-bounded authority, capacity 1.0), owner person://qk/approver.  [ownership + authority/capacity]
10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied delivery verified on time (forward on-time 1.0); Learning entry decision://qk/s5-learning-on-time; provider-allocation policy v3 updated (change-future-policy).  [verified outcome + organisational learning]