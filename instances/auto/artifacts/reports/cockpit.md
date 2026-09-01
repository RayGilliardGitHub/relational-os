# Forge Auto — Parts on the line, on the build.
generated 2026-09-01T00:29:53Z  |  ledger events 54  graph objects 80

## Business health (ledger-projected metrics)
| metric | unit | target | actual | variance | status |
|---|---|---|---|---|---|
| Committed-oem part-lot delivery on-time rate (`metric://auto/m-on-time`) | fraction | 0.95 | 0.5 | -0.45 | CRITICAL |
| Partner scoped-trust score (`metric://auto/m-trust`) | score | 0.9 | 0.79 | -0.11 | CRITICAL |
| Settled committed value (`metric://auto/m-settled-value`) | USD | 7600000.0 | 7600000.0 | 0.0 | OK |

## Prioritized attention — 2 things requiring attention today
- **0.69** re-balance committed work (`task://auto/t-rebalance`)
- **0.58** rallied follow-on (good partner) (`task://auto/t-followup`)

## Exception (heartbeat, §7J.2)
- expected 0.95  actual 0.333  variance -0.617  significance CRITICAL  (1/3 ledger committed deliveries on time)
- case `case://auto/c-on-time`  status **CLOSED**

## AI recommendation (#8) with the authority it requires (§7J.9)
- recommended work: `task://auto/t-rebalance`
- authority required: `authority://auto/for-ops`  confidence 0.85
- options: ['re-balance OEM part lots to the verified on-time vendor', 'gate the laggard (corvair-parts)', 'do nothing']  (do-nothing included: True)
- trade-off: Routing via stellar-auto restores on-time supply (higher short-term concentration risk) but protects line Trust; doing nothing keeps below target.
- expected impact: forward on-time returns to 1.0

## Verified outcome (#10) + Learning
- rallied good-partner committed work settled event://auto/s4-exchange-stellar-autoR, outcome event://auto/s4-outcome-stellar-autoR (met); evidence evidence://auto/routed-stellar-autoR; forward on-time 1.0; org://auto/stellar-auto Trust -> 0.79
- Learning entry: `decision://auto/learning`

## §7L — the ten morning questions, answered with evidence
1. WHAT HAPPENED?  Committed work on time 2/4 (0.5); good partner on time (ev evidence://auto/routed-stellar-autoR), lag partner late; committed value 7600000.0.  [ledger evidence]
2. WHAT CHANGED?  Re-allocation recommended; rallied good-partner work verified on time; forward on-time = 1.0.  [delta -> significance]
3. WHAT MATTERS?  Priority-ordered attention: re-balance committed work, rallied follow-on (good partner).  [§7J.5]
4. WHAT'S GOING WRONG?  Committed on-time 0.5 below target 0.95 (CRITICAL).  [§7J.2]
5. WHY?  tier failure — org://auto/corvair-parts missed its committed part-lot delivery by 2 days; scoped Trust fell 0.90->0.51 (root SUPPORTED).  [§7K.2 epistemic status]
6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.5 < target; laggard keeps missing; scoped Trust erodes.  [§7K.1 forecast]
7. WHAT ARE OUR OPTIONS?  re-balance to good partner; gate laggard; do-nothing (all costed; trade-off in the recommendation).  [§7K.1]
8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://auto/t-rebalance under authority://auto/for-ops.  [recommendation]
9. WHO DOES IT, AND AUTHORITY/CAPACITY?  agent://auto/supply-ops via delegation://auto/ops (delegation-bounded authority, capacity 1.0), owner person://auto/vpo.  [ownership + authority/capacity]
10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed work verified on time (forward on-time 1.0); Learning entry decision://auto/learning; policy v3 updated.  [verified outcome + organisational learning]

## Brand (company identity carried on the org actor; additive field, §7J.11)
**Parts on the line, on the build.**
**Mission**
Deliver committed OEM part lots reliably and on time so assembly lines stay scheduled, stays running, and no plant shuts down waiting on a supplier.
**Vision**
An automotive supply chain where line-side parts are a given, and our on-time record keeps assembly floors from ever going dark.
**About**
Forge Auto is an automotive OEM supplier. We take committed part-lot deliveries and land them line-side on the scheduled date — verified, traceable, right-first-time. When a whole assembly line depends on a supplier keeping the date, our on-time evidence is not a nicety; it is what keeps the plant scheduled and the warranty quiet.
**Values**
- **Line integrity** — A missed part lot can stop a whole line; we treat the date accordingly.
- **Quality at the core** — On time is never at the expense of a defective part.
- **Traceability** — We prove every part lot against the ledger, from source to line-side.
- **Assembly partnership** — OEMs plan around us; we make that planning safe.
- **Continuous improvement** — Every miss is a system fix, not a blame.
**Products & Services**
- OEM part-lot design and delivery
- Line-side supply scheduling
- Supplier quality assurance
**Trust signals**
- 98.9% committed part-lot on-time rate (2025) (Forge Auto delivery ledger)
- IATF 16949 automotive quality certification (third-party audit)
**Customer stories**
- “Forge Auto is the one supplier our line can run without watching the clock for.” — OEM plant director
**History**
- **1989** — Founded as a forge supplying drivetrain parts.
- **2005** — Scaled to full line-side OEM part-lot delivery.
- **2018** — Digitised every lot to ledger-verified on-time evidence.
**Leadership**
- **Grant Kowalski**, Chief Executive — Cast and forged parts his whole career before leading Forge Auto.
- **Nadia Foster**, Chief Operations Officer — Owns the supply network and the on-time gate across plants.
**Fast facts**
- Founded 1989, automotive OEM parts
- 1,200+ part variants delivered
- Line-side programs with 40+ assembly plants
**Locations**
Toledo, OH (HQ) · plants and line-side hubs serving 40+ OEM assembly sites
**FAQ**
- **Q:** What proves your on-time claim?\n  **A:** Each committed part lot anchors to a signed ledger event with a verified delivery time — auditable from order to line-side.
- **Q:** Do you support just-in-time delivery?\n  **A:** Yes, JIT line-side scheduling is core, and the on-time gate applies to every committed lot.
**Contact**
supply@forgeauto.example · +1-419-555-0127
**Careers**
Keep the line scheduled: supply chain, quality, logistics, manufacturing engineering.
**Investors**
Privately held. Plant reliability data shared with OEM customers.
**Press**
media@forgeauto.example — plant and quality announcements.
**Sustainability / ESG**
Low-emissions forging, part-traceability for circularity, apprenticeship programs.
**Site navigation**
About, Capabilities, Plants, Quality, Careers, Investors, Press, Contact
**Legal footer**
Privacy, Terms, California Rights, Do Not Sell or Share
**Cookie consent**
Accept All · Reject All · Preferences (link to Privacy)
**Design language**
- Palette: Anvil Grey #3A3D42, Machining Silver #C7CCD1, Redline Red #C4262E, Deep Forge #15171A
- Typography: heading Solid industrial sans (e.g. Oswald) · body Workhorse sans (e.g. Source Sans 3)
- Logo: FORGE AUTO in heavy caps (an ingot/anvil mark); usage — clear space heavy; red as accent, grey+silver standard
- Imagery: Assembly lines, forged parts, machining in motion — heavy, capable, precise
- Tone of voice: Built, dependable, plain; about keeping the line running.