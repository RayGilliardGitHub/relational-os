# HardVale Stores — Stock for every store, on time.
generated 2026-09-01T05:45:49Z  |  ledger events 54  graph objects 80

## Business health (ledger-projected metrics)
| metric | unit | target | actual | variance | status |
|---|---|---|---|---|---|
| Committed-store replenishment delivery on-time rate (`metric://retail/m-on-time`) | fraction | 0.95 | 0.5 | -0.45 | CRITICAL |
| Partner scoped-trust score (`metric://retail/m-trust`) | score | 0.9 | 0.79 | -0.11 | CRITICAL |
| Settled committed value (`metric://retail/m-settled-value`) | USD | 7600000.0 | 7600000.0 | 0.0 | OK |

## Prioritized attention — 2 things requiring attention today
- **0.69** re-balance committed work (`task://retail/t-rebalance`)
- **0.58** rallied follow-on (good partner) (`task://retail/t-followup`)

## Exception (heartbeat, §7J.2)
- expected 0.95  actual 0.333  variance -0.617  significance CRITICAL  (1/3 ledger committed deliveries on time)
- case `case://retail/c-on-time`  status **CLOSED**

## AI recommendation (#8) with the authority it requires (§7J.9)
- recommended work: `task://retail/t-rebalance`
- authority required: `authority://retail/for-ops`  confidence 0.85
- options: ['re-balance replenishment to the verified on-time carrier', 'gate the laggard (corvus-logistics)', 'do nothing']  (do-nothing included: True)
- trade-off: Routing via atlas-freight restores on-time (higher short-term concentration risk) but protects shopper Trust; doing nothing keeps below target.
- expected impact: forward on-time returns to 1.0

## Verified outcome (#10) + Learning
- rallied good-partner committed work settled event://retail/s4-exchange-atlas-freightR, outcome event://retail/s4-outcome-atlas-freightR (met); evidence evidence://retail/routed-atlas-freightR; forward on-time 1.0; org://retail/atlas-freight Trust -> 0.79
- Learning entry: `decision://retail/learning`

## §7L — the ten morning questions, answered with evidence
1. WHAT HAPPENED?  Committed work on time 2/4 (0.5); good partner on time (ev evidence://retail/routed-atlas-freightR), lag partner late; committed value 7600000.0.  [ledger evidence]
2. WHAT CHANGED?  Re-allocation recommended; rallied good-partner work verified on time; forward on-time = 1.0.  [delta -> significance]
3. WHAT MATTERS?  Priority-ordered attention: re-balance committed work, rallied follow-on (good partner).  [§7J.5]
4. WHAT'S GOING WRONG?  Committed on-time 0.5 below target 0.95 (CRITICAL).  [§7J.2]
5. WHY?  logistics failure — org://retail/corvus-logistics missed its committed store replenishment by 2 days; scoped Trust fell 0.90->0.51 (root SUPPORTED).  [§7K.2 epistemic status]
6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.5 < target; laggard keeps missing; scoped Trust erodes.  [§7K.1 forecast]
7. WHAT ARE OUR OPTIONS?  re-balance to good partner; gate laggard; do-nothing (all costed; trade-off in the recommendation).  [§7K.1]
8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://retail/t-rebalance under authority://retail/for-ops.  [recommendation]
9. WHO DOES IT, AND AUTHORITY/CAPACITY?  agent://retail/inbound-ops via delegation://retail/ops (delegation-bounded authority, capacity 1.0), owner person://retail/cfo.  [ownership + authority/capacity]
10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed work verified on time (forward on-time 1.0); Learning entry decision://retail/learning; policy v3 updated.  [verified outcome + organisational learning]

## Brand (company identity carried on the org actor; additive field, §7J.11)
**Stock for every store, on time.**
**Mission**
Deliver committed store replenishment reliably and on time so every HardVale customer finds what they came for, every day, at every store.
**Vision**
Shoppers who never think about whether the shelf will be there — because it always is.
**About**
HardVale Stores runs a chain of community retail stores and the replenishment operation that keeps their shelves honest. We take committed store replenishment deliveries and make them land so reliably that running out of a staple stops being a plot point in our shoppers' day. Every delivery is verified, every store is a promise, every shelf is the metric.
**Values**
- **Customer first** — Behind every pallet is a shopper who chose us.
- **Shelf faith** — We guard the simple promise that the item will be there.
- **Efficient by habit** — We move stock efficiently so prices stay fair.
- **Community store** — Our stores are neighbourhoods; we stock them like neighbours.
- **Own the outcome** — A store that runs out is our problem to solve, not an excuse to make.
**Products & Services**
- Community retail stores
- Store replenishment and distribution
- Efficient price leadership on essentials
**Trust signals**
- 99.0% committed store-replenishment on-time rate (2025) (HardVale logistics ledger)
- 5-year shopper satisfaction programme (independent survey)
**Customer stories**
- “I can count on the staples always being there. That is why I keep coming back.” — HardVale shopper
**History**
- **1996** — Opened the first HardVale store in a converted warehouse.
- **2008** — Built our own replenishment logistics to end bare shelves.
- **2019** — Digitised every restock run to ledger-verified on-time evidence.
**Leadership**
- **Elena Vasquez**, Chief Executive — Retail lifer who has run stores, buying, and now the whole chain.
- **Tyrone Grant**, Chief Merchandising Officer — Connects what shoppers want to what the shelf holds.
**Fast facts**
- Founded 1996, retail stores
- 460+ stores across the region
- Committed replenishment delivery network
**Locations**
Regional HQ + 460+ stores; distribution parks in 4 states
**FAQ**
- **Q:** How do you keep shelves full?\n  **A:** Every committed replenishment is tracked to a verified on-time ledger completion; stores below target get immediate attention, not excuses.
- **Q:** Do you deliver to stores every day?\n  **A:** Cadence varies by store and category; the committed deliveries on those cadences are the ones we verify.
**Contact**
care@hardvale.example · +1-800-STOCKED
**Careers**
Grow with a store that keeps its promise: store ops, logistics, buying, sustainability.
**Investors**
Privately held. Store-level reliability data shared with partners on request.
**Press**
press@hardvale.example — new stores, community programs, reliability stories.
**Sustainability / ESG**
Waste-less replenishment, community food programs, efficient fleet, sustainable packaging for own-brand.
**Site navigation**
About, Stores, Our Brands, Careers, Investors, Press, Sustainability, Contact
**Legal footer**
Privacy, Terms, California Rights, Do Not Sell or Share, Accessibility
**Cookie consent**
Accept All · Reject All · Preferences (link to Privacy)
**Design language**
- Palette: Bullseye Red #C8102E, Navy Briefcase #1F2A44, Shelf Grey #E6E3DC, Fresh White #FFFFFF
- Typography: heading Bold condensed sans (e.g. Barlow Condensed) · body Open sans (e.g. Work Sans)
- Logo: HARDVALE (bold) (a target/chevron mark); usage — clear space fixed; red on white or navy on white primary
- Imagery: Bright store scenes, stocked shelves, real shoppers — energy and value
- Tone of voice: Friendly, confident, plain-spoken; about the shopper's day going well.