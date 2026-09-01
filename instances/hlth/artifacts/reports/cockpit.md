# Lumen Health — Supply that heals, on schedule.
generated 2026-09-01T05:56:01Z  |  ledger events 54  graph objects 80

## Business health (ledger-projected metrics)
| metric | unit | target | actual | variance | status |
|---|---|---|---|---|---|
| Committed-pharmaceutical delivery on-time rate (`metric://hlth/m-on-time`) | fraction | 0.95 | 0.5 | -0.45 | CRITICAL |
| Partner scoped-trust score (`metric://hlth/m-trust`) | score | 0.9 | 0.79 | -0.11 | CRITICAL |
| Settled committed value (`metric://hlth/m-settled-value`) | USD | 7600000.0 | 7600000.0 | 0.0 | OK |

## Prioritized attention — 2 things requiring attention today
- **0.69** re-balance committed work (`task://hlth/t-rebalance`)
- **0.58** rallied follow-on (good partner) (`task://hlth/t-followup`)

## Exception (heartbeat, §7J.2)
- expected 0.95  actual 0.333  variance -0.617  significance CRITICAL  (1/3 ledger committed deliveries on time)
- case `case://hlth/c-on-time`  status **CLOSED**

## AI recommendation (#8) with the authority it requires (§7J.9)
- recommended work: `task://hlth/t-rebalance`
- authority required: `authority://hlth/for-ops`  confidence 0.85
- options: ['re-balance pharmaceutical supply to the verified on-time distributor', 'gate the laggard (meridian-med)', 'do nothing']  (do-nothing included: True)
- trade-off: Concentrating supply with cortica-supply restores on-time delivery (higher short-term concentration risk) but protects facility-trust; doing nothing keeps below target.
- expected impact: forward on-time returns to 1.0

## Verified outcome (#10) + Learning
- rallied good-partner committed work settled event://hlth/s4-exchange-cortica-supplyR, outcome event://hlth/s4-outcome-cortica-supplyR (met); evidence evidence://hlth/routed-cortica-supplyR; forward on-time 1.0; org://hlth/cortica-supply Trust -> 0.79
- Learning entry: `decision://hlth/learning`

## §7L — the ten morning questions, answered with evidence
1. WHAT HAPPENED?  Committed work on time 2/4 (0.5); good partner on time (ev evidence://hlth/routed-cortica-supplyR), lag partner late; committed value 7600000.0.  [ledger evidence]
2. WHAT CHANGED?  Re-allocation recommended; rallied good-partner work verified on time; forward on-time = 1.0.  [delta -> significance]
3. WHAT MATTERS?  Priority-ordered attention: re-balance committed work, rallied follow-on (good partner).  [§7J.5]
4. WHAT'S GOING WRONG?  Committed on-time 0.5 below target 0.95 (CRITICAL).  [§7J.2]
5. WHY?  supply failure — org://hlth/meridian-med missed its committed pharmaceutical delivery by 2 days; scoped Trust fell 0.90->0.51 (root SUPPORTED).  [§7K.2 epistemic status]
6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.5 < target; laggard keeps missing; scoped Trust erodes.  [§7K.1 forecast]
7. WHAT ARE OUR OPTIONS?  re-balance to good partner; gate laggard; do-nothing (all costed; trade-off in the recommendation).  [§7K.1]
8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://hlth/t-rebalance under authority://hlth/for-ops.  [recommendation]
9. WHO DOES IT, AND AUTHORITY/CAPACITY?  agent://hlth/supply-ops via delegation://hlth/ops (delegation-bounded authority, capacity 1.0), owner person://hlth/oph.  [ownership + authority/capacity]
10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed work verified on time (forward on-time 1.0); Learning entry decision://hlth/learning; policy v3 updated.  [verified outcome + organisational learning]

## Brand (company identity carried on the org actor; additive field, §7J.11)
**Supply that heals, on schedule.**
**Mission**
Move committed pharmaceutical supply reliably and on time so care facilities always have the medicine they ordered, exactly when they ordered it.
**Vision**
A healthcare supply chain so dependable that a pharmacy's worry is one less thing in the operating room.
**About**
Lumen Health is a healthcare and pharmaceutical supply operator. We run committed pharmaceutical distribution for care facilities — and we treat an on-time release the same way clinicians treat a vital sign: it is either within range, or it gets immediate, documented attention. By anchoring each committed delivery to ledger evidence, we give pharmacies and their patients the rarest thing in the supply chain — certainty.
**Values**
- **Patients first** — Every shipment carries a patient at the other end.
- **On-time is safety** — A delayed essential medicine is a clinical risk, not an inventory hiccup.
- **Evidence-based** — We verify every delivery against the ledger; nothing ships on trust alone.
- **Compassion** — We treat supply failures as care failures, and fix the system, not the blame.
- **Accountability** — If a delivery misses, we say so, we learn, and the policy changes.
**Products & Services**
- Committed pharmaceutical supply and distribution
- Cold-chain logistics
- Supply-reliability assurance for care facilities
**Trust signals**
- 99.4% committed pharmacy-delivery on-time rate (2025) (Lumen delivery ledger)
- GDP (Good Distribution Practice) aligned cold-chain (third-party audit)
**Customer stories**
- “Since Lumen, 'reorder' is boring again. That is exactly what I want it to be.” — Facility pharmacy director
**History**
- **2009** — Founded in Minneapolis to fix fragile pharma distribution.
- **2015** — Launched the committed pharmaceutical-delivery line.
- **2022** — Placed every committed delivery under ledger-verified on-time evidence.
**Leadership**
- **Dana Okafor**, Chief Operating Officer — Former hospital pharmacy director who joined Lumen to put reliability at the centre of supply.
- **Marco Beltran**, VP, Distribution — Owns the distributor network and the on-time bar.
**Fast facts**
- Founded 2009, pharmaceutical distribution
- 3,200+ care facilities served
- Cold-chain and schedule-critical delivery practice
**Locations**
Minneapolis, MN (HQ) · regional depots across the Midwest
**FAQ**
- **Q:** How do you prove a delivery was on time?\n  **A:** Each committed delivery anchors to a signed ledger event with a verified completion time — auditable end to end.
- **Q:** Do you handle temperature-sensitive product?\n  **A:** Yes, cold-chain is a first-class service with its own verification and reporting.
**Contact**
supply@lumenhealth.example · +1-612-555-0177
**Careers**
Help us make healthcare supply boring again: distribution leads, cold-chain specialists, supply ops.
**Investors**
Privately held. On-time and reliability reporting available on request.
**Press**
media@lumenhealth.example — spokespeople and reliability data.
**Sustainability / ESG**
Cold-chain energy efficiency, temperature-monitoring transparency, community medication-access grants.
**Site navigation**
About, What We Do, Facilities, Careers, Investors, Press, Sustainability, Contact
**Legal footer**
Privacy, Terms, Health Privacy Notice, State Rights
**Cookie consent**
Accept All · Reject All · Health-Privacy Preferences (links)
**Design language**
- Palette: Healing Teal #0E8575, Clinical White #FDFDFD, Patient Warmth #F2C14E, Trust Navy #14324A
- Typography: heading Clean serif (e.g. Lora) · body Open sans-serif (e.g. Source Sans 3)
- Logo: Lumen Health in rounded friendly caps (a pulse-line leaf mark); usage — clear space around the leaf; calm tones only
- Imagery: Human and calm: clinicians, care settings, organized supply — never sterile or alarming
- Tone of voice: Calm, caring, and rigorous; speaks in outcomes for patients.