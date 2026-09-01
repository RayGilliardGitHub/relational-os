# Hollow Media — Campaigns that land on the date.
generated 2026-09-01T03:13:38Z  |  ledger events 54  graph objects 80

## Business health (ledger-projected metrics)
| metric | unit | target | actual | variance | status |
|---|---|---|---|---|---|
| Committed-content-delivery campaign on-time rate (`metric://media/m-on-time`) | fraction | 0.95 | 0.5 | -0.45 | CRITICAL |
| Partner scoped-trust score (`metric://media/m-trust`) | score | 0.9 | 0.79 | -0.11 | CRITICAL |
| Settled committed value (`metric://media/m-settled-value`) | USD | 7600000.0 | 7600000.0 | 0.0 | OK |

## Prioritized attention — 2 things requiring attention today
- **0.69** re-balance committed work (`task://media/t-rebalance`)
- **0.58** rallied follow-on (good partner) (`task://media/t-followup`)

## Exception (heartbeat, §7J.2)
- expected 0.95  actual 0.333  variance -0.617  significance CRITICAL  (1/3 ledger committed deliveries on time)
- case `case://media/c-on-time`  status **CLOSED**

## AI recommendation (#8) with the authority it requires (§7J.9)
- recommended work: `task://media/t-rebalance`
- authority required: `authority://media/for-ops`  confidence 0.85
- options: ['re-balance media distribution to the verified on-time partner', 'gate the laggard (hollowpoint-digital)', 'do nothing']  (do-nothing included: True)
- trade-off: Routing via lyra-ops restores on-time campaigns (higher short-term concentration risk) but protects platform Trust; doing nothing keeps below target.
- expected impact: forward on-time returns to 1.0

## Verified outcome (#10) + Learning
- rallied good-partner committed work settled event://media/s4-exchange-lyra-opsR, outcome event://media/s4-outcome-lyra-opsR (met); evidence evidence://media/routed-lyra-opsR; forward on-time 1.0; org://media/lyra-ops Trust -> 0.79
- Learning entry: `decision://media/learning`

## §7L — the ten morning questions, answered with evidence
1. WHAT HAPPENED?  Committed work on time 2/4 (0.5); good partner on time (ev evidence://media/routed-lyra-opsR), lag partner late; committed value 7600000.0.  [ledger evidence]
2. WHAT CHANGED?  Re-allocation recommended; rallied good-partner work verified on time; forward on-time = 1.0.  [delta -> significance]
3. WHAT MATTERS?  Priority-ordered attention: re-balance committed work, rallied follow-on (good partner).  [§7J.5]
4. WHAT'S GOING WRONG?  Committed on-time 0.5 below target 0.95 (CRITICAL).  [§7J.2]
5. WHY?  distribution failure — org://media/hollowpoint-digital missed its committed content-delivery campaign by 2 days; scoped Trust fell 0.90->0.51 (root SUPPORTED).  [§7K.2 epistemic status]
6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.5 < target; laggard keeps missing; scoped Trust erodes.  [§7K.1 forecast]
7. WHAT ARE OUR OPTIONS?  re-balance to good partner; gate laggard; do-nothing (all costed; trade-off in the recommendation).  [§7K.1]
8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://media/t-rebalance under authority://media/for-ops.  [recommendation]
9. WHO DOES IT, AND AUTHORITY/CAPACITY?  agent://media/campaign-ops via delegation://media/ops (delegation-bounded authority, capacity 1.0), owner person://media/cmo.  [ownership + authority/capacity]
10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed work verified on time (forward on-time 1.0); Learning entry decision://media/learning; policy v3 updated.  [verified outcome + organisational learning]

## Brand (company identity carried on the org actor; additive field, §7J.11)
**Campaigns that land on the date.**
**Mission**
Deliver committed content-delivery campaigns reliably and on time so platforms and brands stay in the mix and audiences see the story on schedule.
**Vision**
A media marketplace where a campaign release date is a contract audiences can count on.
**About**
Hollow Media produces and delivers committed content-delivery campaigns — from concept through to an energized, measured launch on the agreed date. In a business where timing is the whole story, we back every campaign release with ledger-verified on-time evidence, so a 'drop' date is a real commitment, not a hopeful aspiration.
**Values**
- **The date is the story** — A late campaign is a missed audience moment.
- **Creative rigour** — Great work delivered on time, never rushed at the end.
- **Measured impact** — We verify every run against the ledger; reach is a fact.
- **Platform partnership** — We make our partners' schedules look good.
- **Audience respect** — We deliver content audiences actually want, when they want it.
**Products & Services**
- Content-delivery campaigns (concept to launch)
- Multi-platform distribution
- Campaign measurement and reporting
**Trust signals**
- 99.3% committed campaign on-time rate (2025) (Hollow delivery ledger)
- MARC (Media Rating Council) aligned measurement (independent audit)
**Customer stories**
- “Hollow delivered the campaign on the exact date we'd promised our brand. That never happens in media.” — Brand marketing lead
**History**
- **2007** — Founded producing branded content.
- **2014** — Launched the content-delivery campaign business.
- **2022** — Verifying every campaign release against the ledger.
**Leadership**
- **Celine Wexler**, Chief Executive — Producer-turned-executive who built Hollow on delivered dates.
- **Omar Delgado**, Chief Media Officer — Owns the distribution network and campaign timing.
**Fast facts**
- Founded 2007, media & content production
- 400+ campaigns delivered
- Multi-format distribution across platforms
**Locations**
LA (HQ) · production + distribution hubs across 3 regions
**FAQ**
- **Q:** How can you commit a creative launch date?\n  **A:** We treat the release like a delivery: planned backwards from the date, verified at launch, and measured against the ledger.
- **Q:** Do you handle distribution yourselves?\n  **A:** Yes, multi-platform distribution is core and part of the on-time commitment.
**Contact**
hello@hollowmedia.example · +1-310-555-0188
**Careers**
Drop stories on time: production, distribution, data, and campaign leads.
**Investors**
Privately held. Campaign performance data shared with brands on request.
**Press**
press@hollowmedia.example — launches, shows, and reliability stories.
**Sustainability / ESG**
Sustainable production practices, audience-inclusive content, creator equity programs.
**Site navigation**
About, Work, Distribution, Press, Careers, Contact
**Legal footer**
Privacy, Terms, California Rights, Do Not Sell or Share, Content Policy
**Cookie consent**
Accept All · Reject All · Preferences (link to Privacy)
**Design language**
- Palette: Studio Black #111214, Hollow Cerise #D41159, Screen White #F7F5F2, Signal Teal #0F7A72
- Typography: heading Contemporary display serif (e.g. Playfair Display) · body Neutral sans (e.g. Inter)
- Logo: hollow (a hollow-circle/cutout mark); usage — clear space fine; cerise-on-black primary, teal for data accents
- Imagery: Cinematic stills, editing bays, campaign storyboards — dark, bold, precise
- Tone of voice: Confident, slightly provocative, disciplined about timing; the date is the point.