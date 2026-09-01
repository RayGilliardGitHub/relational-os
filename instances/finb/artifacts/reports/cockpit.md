# Northglen Bank — Funding that lands on the date.
generated 2026-09-01T05:39:56Z  |  ledger events 54  graph objects 80

## Business health (ledger-projected metrics)
| metric | unit | target | actual | variance | status |
|---|---|---|---|---|---|
| Committed-committed funding tranche on-time rate (`metric://finb/m-on-time`) | fraction | 0.95 | 0.5 | -0.45 | CRITICAL |
| Partner scoped-trust score (`metric://finb/m-trust`) | score | 0.9 | 0.79 | -0.11 | CRITICAL |
| Settled committed value (`metric://finb/m-settled-value`) | USD | 7600000.0 | 7600000.0 | 0.0 | OK |

## Prioritized attention — 2 things requiring attention today
- **0.69** re-balance committed work (`task://finb/t-rebalance`)
- **0.58** rallied follow-on (good partner) (`task://finb/t-followup`)

## Exception (heartbeat, §7J.2)
- expected 0.95  actual 0.333  variance -0.617  significance CRITICAL  (1/3 ledger committed deliveries on time)
- case `case://finb/c-on-time`  status **CLOSED**

## AI recommendation (#8) with the authority it requires (§7J.9)
- recommended work: `task://finb/t-rebalance`
- authority required: `authority://finb/for-ops`  confidence 0.85
- options: ['re-balance committed funding to the verified on-time correspondent', 'gate the laggard (kaplen)', 'do nothing']  (do-nothing included: True)
- trade-off: Re-balancing concentrates funding with adamvale (higher short-term concentration risk) but restores on-time settlement and protects client Trust; doing nothing keeps funding below target.
- expected impact: forward on-time returns to 1.0

## Verified outcome (#10) + Learning
- rallied good-partner committed work settled event://finb/s4-exchange-adamvaleR, outcome event://finb/s4-outcome-adamvaleR (met); evidence evidence://finb/routed-adamvaleR; forward on-time 1.0; org://finb/adamvale Trust -> 0.79
- Learning entry: `decision://finb/learning`

## §7L — the ten morning questions, answered with evidence
1. WHAT HAPPENED?  Committed work on time 2/4 (0.5); good partner on time (ev evidence://finb/routed-adamvaleR), lag partner late; committed value 7600000.0.  [ledger evidence]
2. WHAT CHANGED?  Re-allocation recommended; rallied good-partner work verified on time; forward on-time = 1.0.  [delta -> significance]
3. WHAT MATTERS?  Priority-ordered attention: re-balance committed work, rallied follow-on (good partner).  [§7J.5]
4. WHAT'S GOING WRONG?  Committed on-time 0.5 below target 0.95 (CRITICAL).  [§7J.2]
5. WHY?  funding failure — org://finb/kaplen missed its committed settlement tranche by 2 days; scoped Trust fell 0.90->0.51 (root SUPPORTED).  [§7K.2 epistemic status]
6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.5 < target; laggard keeps missing; scoped Trust erodes.  [§7K.1 forecast]
7. WHAT ARE OUR OPTIONS?  re-balance to good partner; gate laggard; do-nothing (all costed; trade-off in the recommendation).  [§7K.1]
8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://finb/t-rebalance under authority://finb/for-ops.  [recommendation]
9. WHO DOES IT, AND AUTHORITY/CAPACITY?  agent://finb/treasury-ops via delegation://finb/ops (delegation-bounded authority, capacity 1.0), owner person://finb/treasurer.  [ownership + authority/capacity]
10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed work verified on time (forward on-time 1.0); Learning entry decision://finb/learning; policy v3 updated.  [verified outcome + organisational learning]

## Brand (company identity carried on the org actor; additive field, §7J.11)
**Funding that lands on the date.**
**Mission**
Commit and settle funding tranches reliably and on time so corporate clients can run their own working-capital plans to a schedule they can trust.
**Vision**
A commercial lending market where a committed tranche settling on time is a durable promise, backed by ledger-verified evidence.
**About**
Northglen Bank is a regional commercial bank. We commit and settle funding tranches for corporate clients, and we run that commitment to the ledger-verified on-time standard of the platform. For a treasurer planning working capital around a committed settlement date, our on-time record is the reliable foundation of the relationship.
**Values**
- **Commitment is covenant** — A committed funding tranche is a promise to a date.
- **Evidence-first** — We verify every settlement against the ledger; on time is a fact, not a target.
- **Client partnership** — Corporate clients plan working capital around our settlements.
- **Prudence** — On time never trades away sound credit judgement.
- **Transparency** — If a settlement will slip, clients hear it from us first.
**Products & Services**
- Committed working-capital funding tranches
- Syndicated committed funding
- Treasury and settlement operations
**Trust signals**
- 98.6% committed settlement on-time rate (2025) (Northglen settlement ledger)
- Chartered bank; prudential oversight (state regulator)
**Customer stories**
- “Northglen's committed settlements are the ones our treasury calendar is built around.” — Corporate treasurer
**History**
- **1987** — Chartered as a regional commercial bank.
- **2005** — Expanded into syndicated committed funding.
- **2023** — Placed every committed settlement under ledger-verified on-time evidence.
**Leadership**
- **Ruth Calloway**, Chief Executive — Two decades in commercial lending; built Northglen on settlement integrity.
- **Victor Hughes**, Chief Treasury Officer — Owns the funding and correspondent network.
**Fast facts**
- Founded 1987, regional commercial banking
- Corporate lending across the region
- Ledger-verified settlement operation
**Locations**
Regional HQ + branches across the state
**FAQ**
- **Q:** How do you prove a settlement was on time?\n  **A:** Every committed tranche settles to a signed ledger event with a verified timestamp — auditable, not asserted.
- **Q:** Do you commit syndicated funding?\n  **A:** Yes, both bilateral and syndicated committed tranches run under the same evidence standard.
**Contact**
treasury@northglen.example · +1-505-555-0199
**Careers**
Back corporate plans with reliable funding: treasury, credit, settlement operations.
**Investors**
Public charter with regulated reporting; settlement reliability shared with regulators.
**Press**
media@northglen.example — lending, treasury, and community programs.
**Sustainability / ESG**
Responsible lending, financial-inclusion programs, branch-efficiency investments.
**Site navigation**
About, Lending, Treasury, Careers, Investors, Press, Community, Contact
**Legal footer**
Privacy, Terms, California Rights, Do Not Sell or Share, Deposit & Lending Disclosures
**Cookie consent**
Accept All · Reject All · Preferences (link to Privacy)
**Design language**
- Palette: Ledger Navy #14314E, Settlement Blue #1B6CA8, Vault Grey #8A929B, Trust White #FAFBFC
- Typography: heading Trusted serif (e.g. Source Serif 4) · body Open sans (e.g. Inter)
- Logo: NORTHGLEN in confident caps (a chevron/vault-mark); usage — clear space generous; navy+white primary, blue accent
- Imagery: Calm and solid: banking halls, treasury operations, measured growth — trustworthy
- Tone of voice: Steady, precise, reassuring; speaks in commitments and verified settlements.