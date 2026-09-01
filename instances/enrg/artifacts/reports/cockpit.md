# Basinline Energy — Energy that arrives when it's supposed to.
generated 2026-09-01T00:57:37Z  |  ledger events 54  graph objects 80

## Business health (ledger-projected metrics)
| metric | unit | target | actual | variance | status |
|---|---|---|---|---|---|
| Committed-refined-products tanker delivery on-time rate (`metric://enrg/m-on-time`) | fraction | 0.95 | 0.5 | -0.45 | CRITICAL |
| Partner scoped-trust score (`metric://enrg/m-trust`) | score | 0.9 | 0.79 | -0.11 | CRITICAL |
| Settled committed value (`metric://enrg/m-settled-value`) | USD | 7600000.0 | 7600000.0 | 0.0 | OK |

## Prioritized attention — 2 things requiring attention today
- **0.69** re-balance committed work (`task://enrg/t-rebalance`)
- **0.58** rallied follow-on (good partner) (`task://enrg/t-followup`)

## Exception (heartbeat, §7J.2)
- expected 0.95  actual 0.333  variance -0.617  significance CRITICAL  (1/3 ledger committed deliveries on time)
- case `case://enrg/c-on-time`  status **CLOSED**

## AI recommendation (#8) with the authority it requires (§7J.9)
- recommended work: `task://enrg/t-rebalance`
- authority required: `authority://enrg/for-ops`  confidence 0.85
- options: ['re-balance tanker volume to the verified on-time carrier', 'gate the laggard (peridot-shipping)', 'do nothing']  (do-nothing included: True)
- trade-off: Routing via gyre-marine restores on-time discharge (higher short-term concentration risk) but protects term-customer Trust; doing nothing keeps below target.
- expected impact: forward on-time returns to 1.0

## Verified outcome (#10) + Learning
- rallied good-partner committed work settled event://enrg/s4-exchange-gyre-marineR, outcome event://enrg/s4-outcome-gyre-marineR (met); evidence evidence://enrg/routed-gyre-marineR; forward on-time 1.0; org://enrg/gyre-marine Trust -> 0.79
- Learning entry: `decision://enrg/learning`

## §7L — the ten morning questions, answered with evidence
1. WHAT HAPPENED?  Committed work on time 2/4 (0.5); good partner on time (ev evidence://enrg/routed-gyre-marineR), lag partner late; committed value 7600000.0.  [ledger evidence]
2. WHAT CHANGED?  Re-allocation recommended; rallied good-partner work verified on time; forward on-time = 1.0.  [delta -> significance]
3. WHAT MATTERS?  Priority-ordered attention: re-balance committed work, rallied follow-on (good partner).  [§7J.5]
4. WHAT'S GOING WRONG?  Committed on-time 0.5 below target 0.95 (CRITICAL).  [§7J.2]
5. WHY?  shipping failure — org://enrg/peridot-shipping missed its committed tanker delivery by 2 days; scoped Trust fell 0.90->0.51 (root SUPPORTED).  [§7K.2 epistemic status]
6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.5 < target; laggard keeps missing; scoped Trust erodes.  [§7K.1 forecast]
7. WHAT ARE OUR OPTIONS?  re-balance to good partner; gate laggard; do-nothing (all costed; trade-off in the recommendation).  [§7K.1]
8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://enrg/t-rebalance under authority://enrg/for-ops.  [recommendation]
9. WHO DOES IT, AND AUTHORITY/CAPACITY?  agent://enrg/logistics-ops via delegation://enrg/ops (delegation-bounded authority, capacity 1.0), owner person://enrg/supt.  [ownership + authority/capacity]
10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed work verified on time (forward on-time 1.0); Learning entry decision://enrg/learning; policy v3 updated.  [verified outcome + organisational learning]

## Brand (company identity carried on the org actor; additive field, §7J.11)
**Energy that arrives when it's supposed to.**
**Mission**
Deliver committed refined-products tanker and chemical cargoes reliably and on time so term customers can run their operations without a barrel of uncertainty.
**Vision**
An energy market where 'it's on the water' means it will be there — measured, verified, and on the agreed date.
**About**
Basinline Energy is a refined-products and chemicals logistics operator. We take committed tanker deliveries and make discharge dates as firm as a bank statement, backing every arrival with ledger-verified evidence. For term customers whose whole plant schedule hinges on a cargo, our on-time record is not a marketing line — it is the working relationship.
**Values**
- **Dependability** — A charter is a commitment; delivering late is a failure, not a forecast.
- **Safety first** — On time never means cutting corners on the creole, the tank, or the port.
- **Evidence over rumor** — We prove when cargoes arrive with ledger-verified records.
- **Stewardship** — We move energy responsibly and report the footprint.
- **Partnership** — Term customers plan around us; we honour that trust.
**Products & Services**
- Refined-products tanker delivery
- Chemical cargo logistics
- Terminal discharge coordination
**Trust signals**
- 98.7% committed tanker discharge on-time rate (2025) (Basinline discharge ledger)
- OCIMF/ISGOTT-aligned tanker safety programme (audited annually)
**Customer stories**
- “Basinline's discharge dates are the only ones in the market I'd build a schedule around.” — Term customer, refining
**History**
- **1998** — Founded in Houston as a fuel-hauling operation.
- **2010** — Entered refined-products tanker chartering.
- **2023** — Verifying every cargo discharge against the ledger for on-time proof.
**Leadership**
- **Wade Okonkwo**, Chief Executive — 25 years in energy shipping; built Basinline on discharge reliability.
- **Lena Alvarado**, Chief Supply Officer — Runs the tanker network and terminal relationships.
**Fast facts**
- Founded 1998, energy & chemicals logistics
- Fleet of 40+ contracted tankers
- Terminal and refining connections across the Gulf
**Locations**
Houston, TX (HQ) · Gulf terminals; global charter coverage to order
**FAQ**
- **Q:** Why is your on-time claim credible?\n  **A:** Every cargo discharge is anchored to a signed ledger event with a verified completion time — auditable, not asserted.
- **Q:** Do you coordinate the terminal side too?\n  **A:** Yes, we manage both vessel and terminal, so the commitment covers the full landing.
**Contact**
charter@basinline.example · +1-713-555-0149
**Careers**
Keep the barrels moving on schedule: marine ops, chartering, terminal logistics, safety.
**Investors**
Privately held. Fleet and reliability data shared on request.
**Press**
media@basinline.example — safety and reliability reporting.
**Sustainability / ESG**
Emissions-tracking per voyage, ballast and spill stewardship, port-community partnerships.
**Site navigation**
About, What We Move, Terminals, Safety, Careers, Investors, Press, Contact
**Legal footer**
Privacy, Terms, Caifornia Rights, Do Not Sell or Share
**Cookie consent**
Accept All · Reject All · Preferences (link to Privacy)
**Design language**
- Palette: Pipeline Black #1B1E24, Refinery Amber #F2A124, Marine Steel #5B6470, Terminal Teal #0E7C86
- Typography: heading Strong industrial sans (e.g. Archivo) · body Neutral sans (e.g. Roboto)
- Logo: BASINLINE in strong caps (a tanker/pipeline chevron mark); usage — clear space wide; dark-on-light, amber as accent only
- Imagery: Open-water tankers, terminals, pipelines at scale — powerful and engineered
- Tone of voice: Solid, understated, exact; heavy on measured facts over adjectives.