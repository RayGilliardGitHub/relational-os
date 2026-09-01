# FerrousWorks — Parts that keep the line turning.
generated 2026-09-01T05:31:12Z  |  ledger events 54  graph objects 80

## Business health (ledger-projected metrics)
| metric | unit | target | actual | variance | status |
|---|---|---|---|---|---|
| Committed-machinery parts delivery on-time rate (`metric://indu/m-on-time`) | fraction | 0.95 | 0.5 | -0.45 | CRITICAL |
| Partner scoped-trust score (`metric://indu/m-trust`) | score | 0.9 | 0.79 | -0.11 | CRITICAL |
| Settled committed value (`metric://indu/m-settled-value`) | USD | 7600000.0 | 7600000.0 | 0.0 | OK |

## Prioritized attention — 2 things requiring attention today
- **0.69** re-balance committed work (`task://indu/t-rebalance`)
- **0.58** rallied follow-on (good partner) (`task://indu/t-followup`)

## Exception (heartbeat, §7J.2)
- expected 0.95  actual 0.333  variance -0.617  significance CRITICAL  (1/3 ledger committed deliveries on time)
- case `case://indu/c-on-time`  status **CLOSED**

## AI recommendation (#8) with the authority it requires (§7J.9)
- recommended work: `task://indu/t-rebalance`
- authority required: `authority://indu/for-ops`  confidence 0.85
- options: ['re-balance machinery parts to the verified on-time supplier', 'gate the laggard (cadence-tools)', 'do nothing']  (do-nothing included: True)
- trade-off: Routing via quadrant-works restores on-time (higher short-term concentration risk) but protects plant Trust; doing nothing keeps below target.
- expected impact: forward on-time returns to 1.0

## Verified outcome (#10) + Learning
- rallied good-partner committed work settled event://indu/s4-exchange-quadrant-worksR, outcome event://indu/s4-outcome-quadrant-worksR (met); evidence evidence://indu/routed-quadrant-worksR; forward on-time 1.0; org://indu/quadrant-works Trust -> 0.79
- Learning entry: `decision://indu/learning`

## §7L — the ten morning questions, answered with evidence
1. WHAT HAPPENED?  Committed work on time 2/4 (0.5); good partner on time (ev evidence://indu/routed-quadrant-worksR), lag partner late; committed value 7600000.0.  [ledger evidence]
2. WHAT CHANGED?  Re-allocation recommended; rallied good-partner work verified on time; forward on-time = 1.0.  [delta -> significance]
3. WHAT MATTERS?  Priority-ordered attention: re-balance committed work, rallied follow-on (good partner).  [§7J.5]
4. WHAT'S GOING WRONG?  Committed on-time 0.5 below target 0.95 (CRITICAL).  [§7J.2]
5. WHY?  supplier failure — org://indu/cadence-tools missed its committed machinery parts delivery by 2 days; scoped Trust fell 0.90->0.51 (root SUPPORTED).  [§7K.2 epistemic status]
6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.5 < target; laggard keeps missing; scoped Trust erodes.  [§7K.1 forecast]
7. WHAT ARE OUR OPTIONS?  re-balance to good partner; gate laggard; do-nothing (all costed; trade-off in the recommendation).  [§7K.1]
8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://indu/t-rebalance under authority://indu/for-ops.  [recommendation]
9. WHO DOES IT, AND AUTHORITY/CAPACITY?  agent://indu/line-ops via delegation://indu/ops (delegation-bounded authority, capacity 1.0), owner person://indu/plant-mgr.  [ownership + authority/capacity]
10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed work verified on time (forward on-time 1.0); Learning entry decision://indu/learning; policy v3 updated.  [verified outcome + organisational learning]

## Brand (company identity carried on the org actor; additive field, §7J.11)
**Parts that keep the line turning.**
**Mission**
Deliver committed machinery parts reliably and on time so plants and workshops trust FerrousWorks enough to keep production lines scheduled without a backstop.
**Vision**
Industrial machinery where the part you ordered arrives exactly when the maintenance plan said — so uptime is planned, not hoped for.
**About**
FerrousWorks is an industrial machinery-parts supplier. We take committed machinery parts deliveries and land them on the date the production plan needs them — machined, verified, traceable. In a plant where a missed part means a quiet line and idle labour, our on-time evidence is what lets planners schedule with confidence instead of contingency.
**Values**
- **Uptime is the deliverable** — A late part is a stopped line; we protect the schedule.
- **Machined right** — On time never trades off tolerances or metallurgy.
- **Traceability** — Every part lot is ledger-verified from material to machine.
- **Plant partnership** — Planners lean on us to keep lines running.
- **Built to last** — We make parts that outlast the maintenance cycle.
**Products & Services**
- Machinery parts design and delivery
- Precision machining and fabrication
- Part-traceability and reliability reporting
**Trust signals**
- 99.0% committed machinery-parts on-time rate (2025) (FerrousWorks delivery ledger)
- ISO 9001 quality management certification (third-party audit)
**Customer stories**
- “FerrousWorks is the one supplier our maintenance schedule doesn't hedge against.” — Plant maintenance engineer
**History**
- **1983** — Founded as a machine shop in the industrial Midwest.
- **1999** — Scaled to committed machinery-parts supply.
- **2017** — Digitised every lot to ledger-verified on-time evidence.
**Leadership**
- **Ingrid Halvorsen**, Chief Executive — Metallurgist and shop floor leader before taking the helm of FerrousWorks.
- **Carl Betancourt**, Chief Operating Officer — Owns machining capacity and the on-time gate.
**Fast facts**
- Founded 1983, industrial machinery parts
- 5,000+ parts delivered annually
- Serving plants, OEMs, and job shops
**Locations**
Cleveland, OH (HQ) · machining plants serving the industrial Midwest and beyond
**FAQ**
- **Q:** How is your on-time claim verified?\n  **A:** Each committed part lot anchors to a signed ledger event with a verified delivery time — traceable from material order to the plant.
- **Q:** Do you support emergency and planned maintenance parts?\n  **A:** Yes, both; every committed delivery, planned or rush, runs under the same on-time gate.
**Contact**
orders@ferrousworks.example · +1-216-555-0156
**Careers**
Keep the line turning: machining, metallurgy, supply, quality, planning.
**Investors**
Privately held. Plant reliability data shared on request.
**Press**
media@ferrousworks.example — capability and quality announcements.
**Sustainability / ESG**
Low-waste machining, material traceability for circularity, apprentice and upskilling programs.
**Site navigation**
About, Capabilities, Plants & Facilites, Quality, Careers, Investors, Press, Contact
**Legal footer**
Privacy, Terms, California Rights, Do Not Sell or Share
**Cookie consent**
Accept All · Reject All · Preferences (link to Privacy)
**Design language**
- Palette: Foundry Charcoal #24262B, Forge Orange #D85C27, Steel Grey #9AA0A6, Mill White #F2F1EE
- Typography: heading Sturdy industrial sans (e.g. Chivo) · body Workhorse sans (e.g. Source Sans 3)
- Logo: FERROUSWORKS in hard caps (a gear/ingot mark); usage — clear space sturdy; forge orange as accent on charcoal
- Imagery: Machining centre work, forged parts, shop floors at scale — heavy and precise
- Tone of voice: Built, straightforward, exact; about uptime and tolerances.