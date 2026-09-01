# NimbusCom — Coverage where you need it, on schedule.
generated 2026-09-01T00:29:53Z  |  ledger events 54  graph objects 80

## Business health (ledger-projected metrics)
| metric | unit | target | actual | variance | status |
|---|---|---|---|---|---|
| Committed-cell-site buildout on-time rate (`metric://telco/m-on-time`) | fraction | 0.95 | 0.5 | -0.45 | CRITICAL |
| Partner scoped-trust score (`metric://telco/m-trust`) | score | 0.9 | 0.79 | -0.11 | CRITICAL |
| Settled committed value (`metric://telco/m-settled-value`) | USD | 7600000.0 | 7600000.0 | 0.0 | OK |

## Prioritized attention — 2 things requiring attention today
- **0.69** re-balance committed work (`task://telco/t-rebalance`)
- **0.58** rallied follow-on (good partner) (`task://telco/t-followup`)

## Exception (heartbeat, §7J.2)
- expected 0.95  actual 0.333  variance -0.617  significance CRITICAL  (1/3 ledger committed deliveries on time)
- case `case://telco/c-on-time`  status **CLOSED**

## AI recommendation (#8) with the authority it requires (§7J.9)
- recommended work: `task://telco/t-rebalance`
- authority required: `authority://telco/for-ops`  confidence 0.85
- options: ['re-balance cell-site buildout to the verified on-time contractor', 'gate the laggard (nimbus-networks)', 'do nothing']  (do-nothing included: True)
- trade-off: Routing via meridian-tower restores on-time buildout (higher short-term concentration risk) but protects coverage Trust; doing nothing keeps below target.
- expected impact: forward on-time returns to 1.0

## Verified outcome (#10) + Learning
- rallied good-partner committed work settled event://telco/s4-exchange-meridian-towerR, outcome event://telco/s4-outcome-meridian-towerR (met); evidence evidence://telco/routed-meridian-towerR; forward on-time 1.0; org://telco/meridian-tower Trust -> 0.79
- Learning entry: `decision://telco/learning`

## §7L — the ten morning questions, answered with evidence
1. WHAT HAPPENED?  Committed work on time 2/4 (0.5); good partner on time (ev evidence://telco/routed-meridian-towerR), lag partner late; committed value 7600000.0.  [ledger evidence]
2. WHAT CHANGED?  Re-allocation recommended; rallied good-partner work verified on time; forward on-time = 1.0.  [delta -> significance]
3. WHAT MATTERS?  Priority-ordered attention: re-balance committed work, rallied follow-on (good partner).  [§7J.5]
4. WHAT'S GOING WRONG?  Committed on-time 0.5 below target 0.95 (CRITICAL).  [§7J.2]
5. WHY?  construction failure — org://telco/nimbus-networks missed its committed cell-site buildout by 2 days; scoped Trust fell 0.90->0.51 (root SUPPORTED).  [§7K.2 epistemic status]
6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.5 < target; laggard keeps missing; scoped Trust erodes.  [§7K.1 forecast]
7. WHAT ARE OUR OPTIONS?  re-balance to good partner; gate laggard; do-nothing (all costed; trade-off in the recommendation).  [§7K.1]
8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://telco/t-rebalance under authority://telco/for-ops.  [recommendation]
9. WHO DOES IT, AND AUTHORITY/CAPACITY?  agent://telco/build-ops via delegation://telco/ops (delegation-bounded authority, capacity 1.0), owner person://telco/cno.  [ownership + authority/capacity]
10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed work verified on time (forward on-time 1.0); Learning entry decision://telco/learning; policy v3 updated.  [verified outcome + organisational learning]

## Brand (company identity carried on the org actor; additive field, §7J.11)
**Coverage where you need it, on schedule.**
**Mission**
Deliver committed cell-site buildouts reliably and on time so metropolitan communities and subscribers get the coverage they were promised, when they were promised it.
**Vision**
A connected city where 'we're building coverage' means the tower is coming up on the scheduled date.
**About**
NimbusCom is a telecom operator that builds and lights up cellular coverage. We take committed cell-site buildouts and energize them on schedule — verified, code-compliant, ready to carry traffic. Between the promise on a coverage map and the bars on a subscriber's phone, there is a site that has to come up on the date; that handover is the work we are built for.
**Values**
- **Coverage is a promise** — A site on time means a neighbourhood connected on time.
- **Build it right** — Speed never trades away a safe, code-compliant handover.
- **Evidence in hand** — We verify every energized site against the ledger.
- **Subscriber trust** — People count on us to make the signal real; we protect that.
- **Metro partnership** — We build with the community, not around it.
**Products & Services**
- Mobile network operation
- Cell-site buildout and erection
- Coverage expansion and modernization
**Trust signals**
- 98.8% committed cell-site on-time rate (2025) (NimbusCom buildout ledger)
- FCC-compliant, code-certified site handovers (independent inspection)
**Customer stories**
- “NimbusCom lit the site on the exact date they committed. Our coverage story changed that day.” — Metro community liaison
**History**
- **2003** — Founded rolling out metro coverage.
- **2011** — Accelerated the cell-site buildout business.
- **2022** — Verifying every energized handover against the ledger.
**Leadership**
- **CEO — Lena Park**, Chief Executive — Ran network engineering for years before leading NimbusCom.
- **Tanaji Rao**, Chief Network Officer — Owns buildout schedule and handover integrity.
**Fast facts**
- Founded 2003, mobile network operator
- 2,100+ cell sites lit
- Metropolitan coverage across 3 metro regions
**Locations**
Metro HQ across 3 regions; build teams dispatched per site programme
**FAQ**
- **Q:** What counts as 'on time' for a site?\n  **A:** The committed energization date, verified by a signed ledger event at handover — measured, not promised.
- **Q:** Do you handle permits and community outreach?\n  **A:** Yes, buildout includes permitting, outreach, and code handover, all on a schedule.
**Contact**
coverage@nimbuscom.example · +1-512-555-0110
**Careers**
Light up whole neighbourhoods: site engineering, buildout ops, network, field coordination.
**Investors**
Privately held. Coverage and buildout reliability shared on request.
**Press**
news@nimbuscom.example — new sites and coverage announcements.
**Sustainability / ESG**
Carbon-aware build scheduling, site-power efficiency, community digital-inclusion grants.
**Site navigation**
About, Coverage, Buildout, Community, Careers, Investors, Press, Contact
**Legal footer**
Privacy, Terms, California Rights, Do Not Sell or Share, Health & Safety
**Cookie consent**
Accept All · Reject All · Preferences (link to Privacy)
**Design language**
- Palette: Signal Purple #5A2F8A, Lumen Blue #1E7BD8, Dark Sky #101A2E, Zing Yellow #F5B700
- Typography: heading Modern geometric sans (e.g. Nunito Sans) · body Open sans (e.g. Roboto)
- Logo: nimbuscom (a tower/signal-wave mark); usage — clear space fixed; purple+blue standard, yellow for energy accents
- Imagery: City skylines, towers on the skyline, energized coverage maps — bright and forward
- Tone of voice: Energised, clear, reassuring; speaks in coverage and connection.