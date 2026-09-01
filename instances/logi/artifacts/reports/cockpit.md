# Hawkline Logistics — Freight that moves on the minute.
generated 2026-09-01T05:56:01Z  |  ledger events 54  graph objects 80

## Business health (ledger-projected metrics)
| metric | unit | target | actual | variance | status |
|---|---|---|---|---|---|
| Committed-freight-dispatch settlement on-time rate (`metric://logi/m-on-time`) | fraction | 0.95 | 0.5 | -0.45 | CRITICAL |
| Partner scoped-trust score (`metric://logi/m-trust`) | score | 0.9 | 0.79 | -0.11 | CRITICAL |
| Settled committed value (`metric://logi/m-settled-value`) | USD | 7600000.0 | 7600000.0 | 0.0 | OK |

## Prioritized attention — 2 things requiring attention today
- **0.69** re-balance committed work (`task://logi/t-rebalance`)
- **0.58** rallied follow-on (good partner) (`task://logi/t-followup`)

## Exception (heartbeat, §7J.2)
- expected 0.95  actual 0.333  variance -0.617  significance CRITICAL  (1/3 ledger committed deliveries on time)
- case `case://logi/c-on-time`  status **CLOSED**

## AI recommendation (#8) with the authority it requires (§7J.9)
- recommended work: `task://logi/t-rebalance`
- authority required: `authority://logi/for-ops`  confidence 0.85
- options: ['re-balance freight to the verified on-time carrier', 'gate the laggard (barnacle-freight)', 'do nothing']  (do-nothing included: True)
- trade-off: Routing via keystone-lines restores on-time dispatch (higher short-term concentration risk) but protects shipper Trust; doing nothing keeps below target.
- expected impact: forward on-time returns to 1.0

## Verified outcome (#10) + Learning
- rallied good-partner committed work settled event://logi/s4-exchange-keystone-linesR, outcome event://logi/s4-outcome-keystone-linesR (met); evidence evidence://logi/routed-keystone-linesR; forward on-time 1.0; org://logi/keystone-lines Trust -> 0.79
- Learning entry: `decision://logi/learning`

## §7L — the ten morning questions, answered with evidence
1. WHAT HAPPENED?  Committed work on time 2/4 (0.5); good partner on time (ev evidence://logi/routed-keystone-linesR), lag partner late; committed value 7600000.0.  [ledger evidence]
2. WHAT CHANGED?  Re-allocation recommended; rallied good-partner work verified on time; forward on-time = 1.0.  [delta -> significance]
3. WHAT MATTERS?  Priority-ordered attention: re-balance committed work, rallied follow-on (good partner).  [§7J.5]
4. WHAT'S GOING WRONG?  Committed on-time 0.5 below target 0.95 (CRITICAL).  [§7J.2]
5. WHY?  carrier failure — org://logi/barnacle-freight missed its committed freight dispatch by 2 days; scoped Trust fell 0.90->0.51 (root SUPPORTED).  [§7K.2 epistemic status]
6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.5 < target; laggard keeps missing; scoped Trust erodes.  [§7K.1 forecast]
7. WHAT ARE OUR OPTIONS?  re-balance to good partner; gate laggard; do-nothing (all costed; trade-off in the recommendation).  [§7K.1]
8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://logi/t-rebalance under authority://logi/for-ops.  [recommendation]
9. WHO DOES IT, AND AUTHORITY/CAPACITY?  agent://logi/fleet-ops via delegation://logi/ops (delegation-bounded authority, capacity 1.0), owner person://logi/cco.  [ownership + authority/capacity]
10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed work verified on time (forward on-time 1.0); Learning entry decision://logi/learning; policy v3 updated.  [verified outcome + organisational learning]

## Brand (company identity carried on the org actor; additive field, §7J.11)
**Freight that moves on the minute.**
**Mission**
Settle committed freight dispatches reliably and on time so shippers run their operations to a schedule they can bank on, lane by lane.
**Vision**
A logistics network where 'dispatched on time' is so reliable it fades into the background of our shippers' day.
**About**
Hawkline Logistics is a freight and transport operator. We take committed freight dispatches and settle them on time, lane by lane, backing every movement with ledger-verified evidence. For shippers whose entire customer promise depends on a load leaving on schedule, our on-time record is the quiet foundation they plan around.
**Values**
- **The deadline is the deal** — A freight commitment is a promise to a schedule.
- **Proof of movement** — We verify every dispatch against the ledger; 'in transit' is a measured fact.
- **Shipper trust** — Shippers plan capacity and customer delivery around our lanes.
- **Efficiency** — Every mile earned is a price we can keep fair.
- **Transparency** — If a dispatch slips, shippers hear it from us first.
**Products & Services**
- Freight dispatch and settlement
- Dedicated and shared-lane transport
- Shipment tracking and proof-of-movement reporting
**Trust signals**
- 98.5% committed freight dispatch on-time rate (2025) (Hawkline dispatch ledger)
- FMCSA-compliant safety programme (audited annually)
**Customer stories**
- “Hawkline's dispatch clock is the one I can set my whole week by.” — Shipper operations manager
**History**
- **1994** — Founded with a single truck lane.
- **2006** — Expanded into a national freight-settlement network.
- **2019** — Digitised every dispatch to ledger-verified on-time evidence.
**Leadership**
- **Dana Ferrell**, Chief Executive — Ran two carriers before founding Hawkline on schedule trust.
- **Melvin Ashe**, Chief Commercial Officer — Owns lanes, carrier network, and dispatch reliability.
**Fast facts**
- Founded 1994, freight & transport
- Lane network across 3 continents
- Freight-dispatch settlement operation
**Locations**
Nashville, TN (HQ) · dispatch hubs across the lane network
**FAQ**
- **Q:** What makes your on-time claim auditable?\n  **A:** Every dispatch settles to a signed ledger event with a verified timestamp — shippers can see the proof, not just hear the claim.
- **Q:** Do you run dedicated lanes?\n  **A:** Yes, both dedicated and shared lanes, each with a committed dispatch schedule we verify.
**Contact**
dispatch@hawkline.example · +1-615-555-0135
**Careers**
Move freight on the minute: dispatch, fleet ops, lane management, carrier relations.
**Investors**
Privately held. Lane reliability data shared with qualified shippers.
**Press**
media@hawkline.example — network and reliability stories.
**Sustainability / ESG**
Fuel-efficiency routing, backhaul reduction to cut empty miles, driver wellbeing programs.
**Site navigation**
About, Lanes, Services, Careers, Investors, Press, Contact
**Legal footer**
Privacy, Terms, California Rights, Do Not Sell or Share
**Cookie consent**
Accept All · Reject All · Preferences (link to Privacy)
**Design language**
- Palette: Roadway Black #1D1F22, Highway Amber #F0A81E, Freight Orange #E3621A, Signal Grey #C7CBCF
- Typography: heading Clear transport sans (e.g. Archivo) · body Open neutral sans (e.g. Roboto)
- Logo: HAWKLINE in sharp caps (a hawk/freight-chevron mark); usage — clear space wide; amber+orange accents on dark
- Imagery: Traffic-lane motion, trucks under speed, dispatch boards — momentum and control
- Tone of voice: Direct, efficient, factual; the clock matters more than the adjectives.