# Maplehurst Foods — Fresh on the shelf, right on schedule.
generated 2026-09-01T05:39:56Z  |  ledger events 54  graph objects 80

## Business health (ledger-projected metrics)
| metric | unit | target | actual | variance | status |
|---|---|---|---|---|---|
| Committed-retail restock shipment on-time rate (`metric://food/m-on-time`) | fraction | 0.95 | 0.5 | -0.45 | CRITICAL |
| Partner scoped-trust score (`metric://food/m-trust`) | score | 0.9 | 0.79 | -0.11 | CRITICAL |
| Settled committed value (`metric://food/m-settled-value`) | USD | 7600000.0 | 7600000.0 | 0.0 | OK |

## Prioritized attention — 2 things requiring attention today
- **0.69** re-balance committed work (`task://food/t-rebalance`)
- **0.58** rallied follow-on (good partner) (`task://food/t-followup`)

## Exception (heartbeat, §7J.2)
- expected 0.95  actual 0.333  variance -0.617  significance CRITICAL  (1/3 ledger committed deliveries on time)
- case `case://food/c-on-time`  status **CLOSED**

## AI recommendation (#8) with the authority it requires (§7J.9)
- recommended work: `task://food/t-rebalance`
- authority required: `authority://food/for-ops`  confidence 0.85
- options: ['re-balance restock to the verified on-time distributor', 'gate the laggard (harlow)', 'do nothing']  (do-nothing included: True)
- trade-off: Restocking via crestline restores on-time (higher short-term concentration risk) but protects retailer Trust; doing nothing keeps shipments below target.
- expected impact: forward on-time returns to 1.0

## Verified outcome (#10) + Learning
- rallied good-partner committed work settled event://food/s4-exchange-crestlineR, outcome event://food/s4-outcome-crestlineR (met); evidence evidence://food/routed-crestlineR; forward on-time 1.0; org://food/crestline Trust -> 0.79
- Learning entry: `decision://food/learning`

## §7L — the ten morning questions, answered with evidence
1. WHAT HAPPENED?  Committed work on time 2/4 (0.5); good partner on time (ev evidence://food/routed-crestlineR), lag partner late; committed value 7600000.0.  [ledger evidence]
2. WHAT CHANGED?  Re-allocation recommended; rallied good-partner work verified on time; forward on-time = 1.0.  [delta -> significance]
3. WHAT MATTERS?  Priority-ordered attention: re-balance committed work, rallied follow-on (good partner).  [§7J.5]
4. WHAT'S GOING WRONG?  Committed on-time 0.5 below target 0.95 (CRITICAL).  [§7J.2]
5. WHY?  distribution failure — org://food/harlow missed its committed restock shipment by 2 days; scoped Trust fell 0.90->0.51 (root SUPPORTED).  [§7K.2 epistemic status]
6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.5 < target; laggard keeps missing; scoped Trust erodes.  [§7K.1 forecast]
7. WHAT ARE OUR OPTIONS?  re-balance to good partner; gate laggard; do-nothing (all costed; trade-off in the recommendation).  [§7K.1]
8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://food/t-rebalance under authority://food/for-ops.  [recommendation]
9. WHO DOES IT, AND AUTHORITY/CAPACITY?  agent://food/restock-ops via delegation://food/ops (delegation-bounded authority, capacity 1.0), owner person://food/cso.  [ownership + authority/capacity]
10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed work verified on time (forward on-time 1.0); Learning entry decision://food/learning; policy v3 updated.  [verified outcome + organisational learning]

## Brand (company identity carried on the org actor; additive field, §7J.11)
**Fresh on the shelf, right on schedule.**
**Mission**
Deliver committed restock shipments reliably and on time so retailers can promise their own customers freshness and never run dry.
**Vision**
A pantry where nothing runs out because the shipment was late — only because it sold.
**About**
Maplehurst Foods moves committed restock shipments and consumer goods so retailers keep the shelf full. Our origin story is a produce manager's complaint — that good food kept arriving a day late and getting pushed to markdown. We built a restock operation on the opposite principle: committed delivery is verified, on time, and the shelf is the report card.
**Values**
- **Freshness is a promise** — On-time restock keeps quality at the centre of the shelf.
- **Shelf truth** — We ship to the schedule, because an empty shelf costs everyone.
- **Fair to partners** — Reliable volume in, honest communication out.
- **Reduce waste** — Right amount, right time, right place — less product thrown away.
- **Taste and trust** — Consumers trust a stocked shelf; we protect that every run.
**Products & Services**
- Retail restock shipments (frozen, fresh, grocery)
- Consumer-brand staples manufactured in-house
- Shelf-on-time logistics for retailers
**Trust signals**
- 99.1% committed restock on-time rate (2025) (Maplehurst delivery ledger)
- FSSC 22000 food-safety certification (third-party audit)
**Customer stories**
- “Markdown went from a weekly guessing game to a rounding error.” — Regional grocery chain buyer
**History**
- **2004** — Founded in Cincinnati around a refrigerated truck and a promise.
- **2011** — Expanded from produce to the full food-and-bev restock line.
- **2020** — Automated restock scheduling to keep the shelf on time at scale.
**Leadership**
- **Sofia Marchetti**, Chief Executive — Third-generation food distributor who built Maplehurst around freshness.
- **Andre Whitfield**, Chief Supply Officer — Owns the distributor network running today's restock.
**Fast facts**
- Founded 2004, food & beverage distribution
- 8,500+ retail shelves served
- Own-brand consumer staples line
**Locations**
Cincinnati, OH (HQ) · distribution centres in 6 states
**FAQ**
- **Q:** What makes Maplehurst 'on time' different?\n  **A:** Every committed shipment is tracked to a verified ledger completion — 'on time' is a measured fact, not a promise.
- **Q:** Can you handle frozen and fresh in one order?\n  **A:** Yes, our restock service spans the temperature range with verification on every leg.
**Contact**
orders@maplehurst.example · +1-513-555-0163
**Careers**
Keep good food out of the markdown bin: logistics, food-safety, supply planning, route operations.
**Investors**
Privately held; family-owned. On-time reliability data on request.
**Press**
news@maplehurst.example — brand and freshness stories.
**Sustainability / ESG**
Waste-reduction routing, food-recovery donations, fuel-efficient fleet, sustainable packaging for own-brand.
**Site navigation**
About, Our Brands, For Retailers, Sustainability, Careers, Press, Contact
**Legal footer**
Privacy, Terms, California Rights, Do Not Sell or Share
**Cookie consent**
Accept All · Reject All · Preferences (link to Privacy)
**Design language**
- Palette: Orchard Green #4E7C2A, Cream Butter #F6EFD9, Berry Red #A63C3C, Midnight Cocoa #2A1F1A
- Typography: heading Warm friendly sans (e.g. Quicksand) · body Humanist sans (e.g. Lato)
- Logo: Maplehurst in rounded case (a maple-leaf/apple mark); usage — clear space generous; food photography must keep greens true
- Imagery: Bright, appetising, real food; family tables; full shelves — warmth and freshness
- Tone of voice: Warm, genuine, modest; talks about freshness and the people who depend on it.