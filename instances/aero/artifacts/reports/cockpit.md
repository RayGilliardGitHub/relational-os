# Valiant Aero — Subsystems on the line, on the date.
generated 2026-09-01T06:27:55Z  |  ledger events 54  graph objects 80

## Business health (ledger-projected metrics)
| metric | unit | target | actual | variance | status |
|---|---|---|---|---|---|
| Committed-airframe-subsystem delivery on-time rate (`metric://aero/m-on-time`) | fraction | 0.95 | 0.5 | -0.45 | CRITICAL |
| Partner scoped-trust score (`metric://aero/m-trust`) | score | 0.9 | 0.79 | -0.11 | CRITICAL |
| Settled committed value (`metric://aero/m-settled-value`) | USD | 7600000.0 | 7600000.0 | 0.0 | OK |

## Prioritized attention — 2 things requiring attention today
- **0.69** re-balance committed work (`task://aero/t-rebalance`)
- **0.58** rallied follow-on (good partner) (`task://aero/t-followup`)

## Exception (heartbeat, §7J.2)
- expected 0.95  actual 0.333  variance -0.617  significance CRITICAL  (1/3 ledger committed deliveries on time)
- case `case://aero/c-on-time`  status **CLOSED**

## AI recommendation (#8) with the authority it requires (§7J.9)
- recommended work: `task://aero/t-rebalance`
- authority required: `authority://aero/for-ops`  confidence 0.85
- options: ['re-balance airframe subsystems to the verified on-time integrator', 'gate the laggard (vireo-airframe)', 'do nothing']  (do-nothing included: True)
- trade-off: Routing via apex-aeronautics restores on-time (higher short-term concentration risk) but protects program Trust; doing nothing keeps below target.
- expected impact: forward on-time returns to 1.0

## Verified outcome (#10) + Learning
- rallied good-partner committed work settled event://aero/s4-exchange-apex-aeronauticsR, outcome event://aero/s4-outcome-apex-aeronauticsR (met); evidence evidence://aero/routed-apex-aeronauticsR; forward on-time 1.0; org://aero/apex-aeronautics Trust -> 0.79
- Learning entry: `decision://aero/learning`

## §7L — the ten morning questions, answered with evidence
1. WHAT HAPPENED?  Committed work on time 2/4 (0.5); good partner on time (ev evidence://aero/routed-apex-aeronauticsR), lag partner late; committed value 7600000.0.  [ledger evidence]
2. WHAT CHANGED?  Re-allocation recommended; rallied good-partner work verified on time; forward on-time = 1.0.  [delta -> significance]
3. WHAT MATTERS?  Priority-ordered attention: re-balance committed work, rallied follow-on (good partner).  [§7J.5]
4. WHAT'S GOING WRONG?  Committed on-time 0.5 below target 0.95 (CRITICAL).  [§7J.2]
5. WHY?  supplier failure — org://aero/vireo-airframe missed its committed airframe subsystem delivery by 2 days; scoped Trust fell 0.90->0.51 (root SUPPORTED).  [§7K.2 epistemic status]
6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.5 < target; laggard keeps missing; scoped Trust erodes.  [§7K.1 forecast]
7. WHAT ARE OUR OPTIONS?  re-balance to good partner; gate laggard; do-nothing (all costed; trade-off in the recommendation).  [§7K.1]
8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://aero/t-rebalance under authority://aero/for-ops.  [recommendation]
9. WHO DOES IT, AND AUTHORITY/CAPACITY?  agent://aero/prog-ops via delegation://aero/ops (delegation-bounded authority, capacity 1.0), owner person://aero/pgm.  [ownership + authority/capacity]
10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed work verified on time (forward on-time 1.0); Learning entry decision://aero/learning; policy v3 updated.  [verified outcome + organisational learning]

## Brand (company identity carried on the org actor; additive field, §7J.11)
**Subsystems on the line, on the date.**
**Mission**
Deliver committed airframe subsystems and flight-critical components reliably and on time so aviation customers can keep their programmes on schedule and their fleets flying.
**Vision**
Aerospace programmes where subsystem delivery is the dependable core, not the critical-path risk.
**About**
Valiant Aero is an aerospace, defense, and aviation subsystem operator. We take committed airframe-subsystem deliveries and bring them in on the building date — integrated, verified, and traceable to the part. For programmes where a missed subsystem is a schedule domino, we make delivery reliability the least anxious part of the build.
**Values**
- **Zero compromises** — Flight-critical means the evidence bar is non-negotiable.
- **Schedule integrity** — A late subsystem can ground a programme; we protect the date.
- **Verification culture** — We prove readiness with data before anything is in the build.
- **Partnership** — Fleet customers plan years ahead; we keep those plans honest.
- **Stewardship** — We build responsibly — safety, export control, and ISO-grade process.
**Products & Services**
- Airframe-subsystem design and delivery
- Flight-critical component integration
- Aerospace programme schedule assurance
**Trust signals**
- 98.9% committed airframe-subsystem on-time rate (2025) (Valiant delivery ledger)
- AS9100 aerospace quality certification (third-party audit)
**Customer stories**
- “Valiant Aero is the subsystem partner we can build our master schedule around.” — Fleet programme lead
**History**
- **2001** — Founded near Dayton for precision aerospace work.
- **2013** — Won our first major airframe-subsystem programme.
- **2021** — Placed every committed subsystem delivery under ledger-verified evidence.
**Leadership**
- **Colonel (ret.) Marta Reyes**, Chief Executive — Former programme manager who runs Valiant Aero on delivery integrity.
- **Erik Lindqvist**, Chief Program Officer — Owns subsystem integration across all active programmes.
**Fast facts**
- Founded 2001, aerospace subsystems
- Component-level to subsystem integration scope
- Fleet and programme customers on 3 continents
**Locations**
Near Dayton, OH (HQ) · integration hangars and partner facilities on 3 continents
**FAQ**
- **Q:** How does on-time delivery work with flight certification?\n  **A:** Verification and certification gates are built into the schedule; our on-time evidence covers the committed delivery on the agreed date.
- **Q:** Do you handle classified work?\n  **A:** Yes, we hold appropriate clearances and follow export-control process at every stage.
**Contact**
programs@valiantaero.example · +1-937-555-0104
**Careers**
Keep programmes on schedule and fleets flying: engineering, program mgmt, quality, integration.
**Investors**
Privately held. Programme-and-reliability reporting shared with defence customers under NDA.
**Press**
media@valiantaero.example — schedule, quality, and programme announcements.
**Sustainability / ESG**
ISO-grade process, responsible export control, engineering education partnerships.
**Site navigation**
About, Capabilities, Programmes, Quality, Careers, Investors, Press, Contact
**Legal footer**
Privacy, Terms, Export-Control Notice, California Rights, Do Not Sell or Share
**Cookie consent**
Accept All · Reject All · Security Preferences (links)
**Design language**
- Palette: Flightline Grey #39434E, Signal Orange #F26522, Runway White #F4F6F8, Missile Teal #0F6E6E
- Typography: heading Sharp technical sans (e.g. Chivo) · body Technical sans (e.g. Roboto Mono for data, Source Sans for prose)
- Logo: VALIANT AERO in angular caps (a chevron/wing mark); usage — clear space wide; orange as a discipline accent only
- Imagery: Precision and scale: airframes, integration bays, flightline — engineered and controlled
- Tone of voice: Precise, disciplined, confident; about programme integrity and schedule.