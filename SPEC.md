# Project RelationalOS
## A Chain of Integrated Services Delivering AI at Maximum ROI

**Version:** 0.22
**Date:** 2026-09-01
**Status:** Working draft — specification v0.22

---

# PROJECT SPECIFICATION
# RelationalOS — A Chain of Integrated Services Delivering AI at Maximum ROI

---

## 1. Abstract

**Core principle statement.** RelationalOS models relationships among
**Actors** — Person, Organization, Agent, System. Each relationship is carried
across a lifecycle that divides cleanly into Relationship · Interaction · Event ·
State, over a backbone of Evidence and Trust. AI concentrates where it pays most, and
each cycle compounds verified evidence no single service can copy. Four layers — the
ontology, the substrate, the operating system (Goals, Metrics, Processes, Cases,
Exceptions, Tasks), and Business Intelligence (Forecast, Optimization, Learning) —
carry the product: an organizational operating system that answers "what happened,
what matters, what should we do, what happens if we don't." The moat is not the data;
it is the verified history of decisions and outcomes attached to relationships,
compounded by Learning.

The fundamental primitive is **Actor ↔ Actor**. Person↔Organization is the primary
*initial* use case, not the universal relationship type (Boeing↔supplier, employee↔
AI agent, government↔corporation are all first-class Actor↔Actor relationships). A
**Relationship** (which may last years) contains many **Interactions** (requests,
offers, decisions, actions, exchanges); each interaction is a series of **Events**;
and the current truth of it all is **State** (Ledger = history; Graph = current
state).

Five services implement the ontology. All read and write one shared Relationship
Graph (state) and one append-only Transaction Ledger (history), and draw on a shared
Knowledge Fabric and Resource Ledger. AI does the highest-ROI work — not the biggest
model, but the stages where work is expensive, error-prone, and under-automated
today. The chain is the moat: each service alone is mediocre; integrated they form a
flywheel where verified evidence (Trust) re-prices and re-routes every subsequent
interaction.

The build is ROI-sequenced to fund itself: (A) revenue from Intent/Matching first,
(B) the Trust moat second, (C) Orchestration and Settlement third to widen and
monetize the integrated chain.

---

## 1a. Status and Epistemological Framing

This is a **product and architecture specification** — its claims are about system
design and market ROI, not empirical science. Three levels of discourse are used;
each claim is flagged by level:

- **[LEVEL A — Architecture]** Formal model, service contracts, data flow. These are
  design decisions, checkable against the specification itself.
- **[LEVEL B — Strategy/ROI]** Where AI creates greatest value and build ordering.
  These are reasoned estimates, flagged as such, not forecast guarantees.
- **[LEVEL C — Ontology]** The lifecycle primitives, inherited from the
  person↔organization interaction model on which the project is grounded. These are
  assumed true for the purposes of this project.

ROI figures in **Section 7** are LEVEL B estimates. Treat them as ordering arguments,
not financial guarantees.

---

## 2. Scope

RelationalOS models relationships among **Actors**: Person, Organization, Agent,
System. The fundamental relationship primitive is **Actor ↔ Actor**. Person↔
Organization is the primary initial use case, not the universal type; Actor↔Actor
covers business-to-business, human-to-agent, agent-to-system, and inter-organization
relationships. It is organized as a chain of five services implementing the ontology.

**In scope:**
- The relationship primitives and the Actor↔Actor / Relationship / Interaction /
  Event / State distinction.
- The shared Relationship Graph (state) and append-only Transaction Ledger (history)
  that integrate the chain.
- The cross-cutting ontology substrate (Purpose, Governance, Rules, Rights, Consent,
  Authority, Expectation, Value) — owned by no single service.
- The AI routing seam (local / private cloud / frontier) and the human-escalation floor.
- The Trust and Accountability engine that closes the loop (the moat).
- Normative requirements, non-goals, ROI model, risk register, and build roadmap.

**Normative requirements:**
- **Character encoding:** all strings UTF-8.
- **Timestamps:** RFC 3339 (`2026-08-31T14:00:00Z`) for all date-time fields.
- **Identity:** every participant and organization has a stable typed URI
  (`person://`, `org://`); role is an attribute, not a separate identity.
- **Ledger:** append-only, content-addressed, signed by the responsible service.
- **Round-tripping:** unknown fields MUST be preserved when a service re-writes a
  record it read.
- **Trust input:** no service may ignore Trust output from the Trust engine (S5).
  Trust is a first-class routing and pricing input, not advisory.
- **Escalation:** any action whose failure is irreversible or unknowable-cost MUST
  escalate to a human before execution (see Section 7A).

---

## 3. The Fundamental Ontology (LEVEL C — inherited foundation)

The ontology comes first; the services (Section 4) implement it. What follows is a
general relational operating model of organizations — private, public, and
charitable — not merely a business-transaction model. `Relationship` is the
fundamental object; value exchange is one type of relationship, not the whole of it.

### 3.0 Cast of actors

Every entity that acts in the system is an **Actor**:
```
ACTOR
├── Person        (natural person; canonical identity person://)
├── Organization  (private | public | charitable)
├── Agent         (AI agent — an actor, not merely a capability)
└── System        (non-AI systems, appliances, infrastructure)
```
An AI agent is a first-class actor: it has identity, capability, **authority**, role,
and performs actions. It is not reducible to a capability. Because an agent can hold
delegated authority, who permitted it to act (Delegation) is mandatory to record.

### 3.1 Purpose (precedes identity)

An organization does not just exist; it exists **for something**. Purpose is the
primitive before Identity:
```
ORGANIZATION → PURPOSE → CAPABILITIES → OFFERS/OBLIGATIONS → RELATIONSHIPS
```
Purpose distinguishes organization kinds and constrains everything below. **Private ≠
for-profit** — private spans nonprofits, religious, educational, philanthropic,
cooperative, mutual, and foundation forms, and public bodies can generate revenue.
Organization kind is therefore an **attribute** (purpose / legal structure), not a
member of three mutually exclusive buckets:
- **Private for-profit** — create value and generate a financial return.
- **Public / Government** — exercise authority and provide public services (coercive,
  not wholly voluntary).
- **Nonprofit / Charitable** — pursue a mission / social benefit.
- **Cooperative / Mutual / Other** — member-owned or hybrid missions.

Organization model: **Identity, Legal Entity, Purpose, Ownership, Governance,
Jurisdiction, Authority, Capabilities, Resources, Obligations, Policies** (see §3.19
for the substrate that owns these).

### 3.2 Context (role is only meaningful in context)

The same person is `employee`, `customer`, `citizen`, `donor` in different
relationships. The **context** determines what a role means:
```
CONTEXT
├── organization
├── relationship
├── role
├── jurisdiction
├── time
├── purpose
└── applicable rules
```
Principle: **Identity is universal; context is relationship-specific.** A person's
cross-organization history is NOT exposed automatically to every organization —
what travels on request is identity; what stays scoped is context.
**Normative (Sprint-4 verified):** role-scoping a context is carried as a query-qualified URI
on the SAME relationship scheme (e.g. `relationship://…?role=employee`) — it is NOT a new
identity and NOT a new URI scheme. Two roles (e.g. customer AND employee) may therefore span
ONE relationship with role-scoped authority (a role→`authority://` map on the relationship)
and role-scoped Trust (§3.14), with no second `person://`.

### 3.3 Relationship lifecycle primitives

The eleven concepts are **relationship primitives**, not eleven fixed stages — some
(e.g. Capability, Trust) exist before, during, and after any given interaction. The
process view, with Expectation elevated and Decision/Dispute/Evidence made explicit:
```
IDENTITY
  → ROLE (in CONTEXT)
  → PURPOSE / INTENT
  → CAPABILITY / NEED
  → OFFER / REQUEST
  → AUTHORITY / CONSENT
  → COMMITMENT / OBLIGATION
  → DECISION
  → PLAN → ACTION
  → EXCHANGE
  → OUTCOME
  → EVIDENCE
  → EVALUATION (against EXPECTATION)
  → ACCOUNTABILITY / DISPUTE
  → TRUST / REPUTATION
  → NEXT RELATIONSHIP CYCLE
```
Running **beside** the entire cycle (orthogonal layers): Rules, Rights, Resources,
Knowledge, Time, Governance, Context.

### 3.4 Authority, Governance and Delegation

Accountability is not governance. Governance answers: who has authority; who decides;
who delegates; who approves; who overrides an agent; who is accountable; what rules
constrain decisions; how conflicts of authority resolve. First-class chain:
```
AUTHORITY → PERMISSION → DELEGATION → DECISION → ACCOUNTABILITY
```
Authority is a general primitive, not a government-only object. **Delegation** records
precisely who empowered which actor to do what (e.g. a manager delegates an AI agent
to approve invoices under $5,000), bounding the agent's authority and keeping
accountability legible. **Normative (Sprint-1 verified):** delegation/consent `scope`
is expressed as URI references to `rule://`/`permission://` objects (which carry the
`grants` for each permitted action), never as bare action-name strings; a
`Delegation` whose `status` is `REVOKED` or `EXPIRED` immediately voids the derived
capability for `authorize()` (see §7B) — both demonstrated running in Sprint 1.

### 3.5 Rights and Obligations (both sides of every relationship)

- **Rights** possessed by participants: to access, appeal, privacy, refuse, receive
  payment, terminate, inspect, representation. A government interaction is
  Rights-and-Obligations both ways, not just Authority→Public Service.
- **Obligation** may exist without voluntary Commitment: pay taxes, comply with
  regulation, honor a court order, provide required benefits.
- **Commitment** = an actor's *voluntarily undertaken* undertaking to satisfy an
  obligation or agreed condition. **Obligation/Duty** is broader: it may be *imposed*
  (tax, regulation, court order, statutory benefit) with no voluntary commitment.
  ```
  DUTY / OBLIGATION
  ├── imposed
  └── voluntarily undertaken  →  COMMITMENT
  ```
  Commitments are a subset of obligations an actor has actively accepted; obligation
  does not reduce to commitment. Corrects an earlier `Obligation ⊆ Commitment` error.

### 3.6 Rules (distinct from Commitment)

A commitment is not a rule. Distinguish:
```
RULE
├── law
├── regulation
├── policy
├── procedure
├── constraint
└── contract term
```
This matters for AI: an agent must know not only what it can do, but what it is
**allowed** to do.

### 3.7 Consent / Authorization (distinct from Commitment)

A person can consent to something (data processing, marketing, care, employment,
financial authorization, delegation, biometric identification, AI processing) without
committing to perform an action. Consent is its own primitive, recording scope,
duration, revocability, and the evidence of grant.

### 3.8 Resource (a supercategory above Asset and Knowledge)

A relationship consumes **resources** to produce outcomes. Resources include items
that are not assets:
```
RESOURCE
├── Money  ├── Material  ├── Asset         ├── Information
├── Knowledge         ├── Labor  ├── Capability
├── Time  ├── Authority  ├── Attention  ├── Trust
```
Time and Attention are resources of a kind; labor and knowledge are resources that no
Asset Ledger alone captures.

### 3.9 Value, Cost, Price (distinct, fundamental)

`PRICE ≠ COST ≠ VALUE`. A customer may pay $100 for something perceived as $500 of
value; an employee accepts $80k for a broader relationship they value; a charity
spends $1M to create social benefit not sold at market price; government provides
public goods. Fundamental economic relation:
```
Value created  −  Resources consumed  =  Economic result
Expected value −  Actual cost         =  ROI
```

### 3.10 Time (explicit)

Time distinguishes what was / is / should be / will be / was promised / was scheduled /
actually happened. Every primitive carries temporal fields (effective_from, due_by,
expires, completed_at). `Expectation vs Actuality` is one of the most important
relationships in the system.

### 3.11 Expectation (elevated, central)

Trust rests on `what was expected` vs `what actually happened` (`outcome − expectation`
in the trust function). Expectation object:
```
Expectation { actor, subject, condition, metric, threshold, deadline, evidence_required }
```
Clean chain: **Commitment** = agreed to do → **Expectation** = what success means →
**Outcome** = what happened → **Accountability** = responsible for the difference →
**Trust** = history of those differences.

### 3.12 Decision

Between Commitment and Action lies Decision. Record: decision maker, authority,
alternatives considered, evidence used, rules applied, confidence, expected outcome,
actual outcome. This is what makes AI accountability and audit possible.

### 3.13 Dispute

Disagreement is fundamental, not an edge case. When an outcome is contested:
```
OUTCOME → accepted | disputed → EVIDENCE → ADJUDICATION → RESOLUTION
```
The Trust thesis depends on establishing whether an outcome is actually true; Dispute
is a first-class lifecycle entity, and the evidence it surfaces is the same evidence
the Trust engine verifies.

### 3.14 Trust and Reputation (separate, re-contextualized)

Trust is not one-dimensional `Trust(person, org)`. Multi-dimensional:
```
Trust(subject, target, claim/capability, context)
```
I trust Amazon to deliver but not to advise medically; a colleague's technical
judgment, but not their custody of payroll. **Trust** = what a relationship believes;
**Reputation** = what the broader system believes about an actor. **Do not transfer
Trust across organizations — transfer evidence about behavior**, and let each
relationship compute its own Trust. This preserves privacy and prevents a universal
social-credit score.
**Normative (Sprint-4 verified):** distinct role-scoped Trust values coexist on the SAME
relationship — e.g. customer-role Trust (providers, roofing claim, context `relationship://…`)
and employee-role Trust (the employer, payroll claim, context
`relationship://…?role=employee`) — updating independently per `(subject, target, claim,
context)`, never a single score for the pair of parties.

### 3.15 Orthogonal layers summary

Running beside the lifecycle and cross-cutting every primitive:
```
RULES · RIGHTS · RESOURCES · KNOWLEDGE · TIME · GOVERNANCE · CONTEXT
```
These are addressed by Appendix C (e.g. `rule://`, `right://`, `authority://`,
`delegation://`, `consent://`, `expectation://`, `decision://`, `dispute://`,
`evidence://`, `resource://`), and Knowledge (Section 4a) and Assets (Section 4b) are
two reified slices of Resources.

### 3.16 Structural backbone: Relationship ≠ Interaction ≠ Event ≠ State

The cleanest conceptual spine underlying everything:

```
ACTOR → RELATIONSHIP → INTERACTION → EVENT → STATE
                                 ↘ EVIDENCE → TRUST
```

- **Relationship** — a durable bond, potentially spanning years, that may hold many
  transactions or none (employment, citizenship, a customer who has never purchased, a
  marriage). Not a transaction.
- **Interaction** — a discrete episode within a relationship (an offer, a request, a
  decision, an action, an exchange, an outcome).
- **Event** — the atomic record; not everything is an actor-performed action:
  ```
  EVENT
  ├── Action       (actor-performed)
  ├── Decision     (per §3.12)
  ├── Exchange     (per §4b/3.9)
  ├── Outcome
  ├── StateChange  (status, authority, rule change)
  └── ExternalEvent(weather, market move, regulation, mishap — no actor intent)
  ```
- **State** — current relational truth. **Normative:** the **Ledger = history**
  (append-only events); the **Graph = current relational state** (what is true now,
  e.g. employee active / contract balance / customer trust). The two are not the same
  thing and must not be conflated.
  **Normative (Sprint-5 built):** every state delta embedded in a signed Ledger event is an
  **immutable snapshot** of the objects it carries (deep-copied at signing). A later
  in-place edit to a live operating object (e.g. a Case's `history`, an updated Policy, a
  re-scored Metric) MUST NOT retroactively alter an earlier signed entry — the content-
  addressed hash-chain breaks if a shared mutable object in an embedded `state_update` is
  changed after signing. Applies to the generalised closure-copy convention (Sprint-1/4):
  an object being mutated after first signing is re-recorded as a fresh deep copy in the
  new event, never edited in place in an old one.

**Relationship model (formal):**
```
Relationship {
  uri  participants[]  roles[]  context  purpose
  rights[]  obligations[]  authority[]  consent[]  rules[]
  expectations[]  commitments[]  status  created_at  effective_from  expires_at
}
```
**Relationship state machine:** `PROPOSED → ACTIVE → SUSPENDED → ACTIVE → TERMINATED → ARCHIVED`
(with `renew`, `transform` transitions). Employing, subscribing, contracts, insurance,
government benefits, and memberships all depend on this machine.

### 3.17 Claim and the epistemology of verification

The Trust engine is, at bottom, a **claim-verification** system. Insert Claim between
Outcome and Trust:
```
CLAIM → EVIDENCE → VERIFICATION → EVALUATION → OUTCOME → TRUST
```
Example: "the shipment was delivered" is a **Claim**; the GPS record, signed receipt,
and warehouse scan are **Evidence**; conceding it is **Evaluation**. The spec must not
conflate categories. Verification does not establish capital-T Truth — it establishes
`evidence supports claim X to degree Y under procedure Z`. Separate the epistemic
levels so the engine claims no powers it lacks:
```
OBSERVATION → EVIDENCE → CLAIM → VERIFICATION → INFERENCE → JUDGMENT
```

### 3.18 Actor psychology and conflict (compact)

- **Incentive** — what behavior the actor is driven toward by reward, penalty,
  preference, constraint, objective. Often explains behavior better than stated
  Intent, and is central to Trust: trustworthy actors are those with weak incentives
  to behave badly.
- **Interest** — what outcome benefits the actor, distinct from **Intent** (what they
  want to do), **Capability** (what they can do), **Authority** (what they may do).
- **Conflict** — incompatible interests need not be a disagreement (employee wants
  leave; employer needs staff on-site — nobody is confused). Distinguish:
  `DISAGREEMENT→DISPUTE` from `CONFLICTING INTERESTS→NEGOTIATION/TRADEOFF/DECISION`.
- **Negotiation** — the process between Request and Commitment:
  `Request → Offer → Counteroffer → Negotiation → Agreement → Commitment`. Represented
  as an interaction type, needed because AI contract-negotiation is a canonical test.

### 3.19 Substrate, versioning, identity, disclosure

- **Cross-cutting substrate (normative):** Purpose, Governance, Rules, Rights,
  Consent, Authority, Expectation, Value, and Reputation are **ontology-level objects
  implemented through shared infrastructure, owned by NO individual service**. No
  service "owns" `delegation://`, `consent://`, or `dispute://`; they are typed
  objects on the graph/ledger that every service consumes. Section 4's S1–S5 own the
  *lifecycle*; the substrate cuts across them.
- **Versioning:** rules, contracts, org structure, roles, authority, prices, and Trust
  change over time. Append-only history handles this, but identity across versions is
  explicit: `contract://123` is one identity with revisions; each Revision names its
  effective range. A URI identifies an object, not a snapshot.
- **Identity ≠ Authentication ≠ Authorization:** S1 currently folds these. Separately:
  `IDENTITY (who) → AUTHENTICATION (prove it) → AUTHORIZATION (may you) → ACTION`.
- **Disclosure (privacy):** "identity is universal; context is relationship-specific"
  begs the harder question — **who may know that two contexts belong to the same
  person?** Formalize **Disclosure** and **purpose limitation**: the system must NOT
  infer that knowing self = knowing all four contexts. Linkage across contexts is a
  gated, consented act, not a default inference.

---

## 4. The Service Chain

Five services implement the ontology: they own the lifecycle primitives. Each service exposes a function signature,
consumes prior-state from the shared graph, writes its stage and any evidence to the
shared ledger, and hands a complete relationship forward.

### S1 — Identity, Authentication, Authorization  *owns: Identity base*
**Function:**
```
resolve_identity(subject, evidence)   -> person://|org://|agent://  (who)
authenticate(identity, credentials)   -> verif_score                 (prove it)
authorize(identity, action, context)  -> permission | denial         (may you)
resolve_role(relationship, context)   -> role (customer|employee|citizen|...)
```
**AI role [LEVEL A]:** classify role from context; extract and verify identity evidence
from noisy, multi-source input; scoring of confidence; evaluating delegated authority
(§3.4) to authorize an action.
**Identity ≠ Authentication ≠ Authorization (per §3.19): these are three functions,
not one.**
**Differentiator [LEVEL B]:** low — identity is crowded (IdP, KYC vendors). Utility is
parity; we build it thin as the substrate all other services need, reusing external
identity where possible.
**Build priority:** first as substrate only. Not a revenue service.

### S2 — Intent & Matching  *owns: Intent, Capability, Offer*
**Function:**
```
infer_intent(subject, evidence)             -> intent graph
match_offers(intent, offers, trust_scores)  -> ranked matches (Trust-weighted)
```
**AI role [LEVEL A]:** LLM+retrieval to infer what the person actually wants from
ambiguous input; capability-model matching; personalized ranking.
**Differentiator [LEVEL B]:** medium — commoditizing fast. This is the front-of-revenue
service: qualify + route + match before a human touches it.
**Build priority:** FIRST revenue service. Fastest payback, easiest adoption.

### S3 — Orchestration & Execution  *owns: Commitment, Action*
**Function:**
```
agree(offer, terms)                                -> commitment
execute(commitment, fleet)                         -> action set
orchestrate(plan, capabilities)                    -> routed agent/human work
```
**AI role [LEVEL A]:** turn agreement into a plan; route sub-tasks to the best
capability (agent fleet or human) across the routing seam (local/private-cloud/
frontier); decompose and parallelize.
**Differentiator [LEVEL B]:** medium — crowded (agents everywhere). High value from
labor substitution, but capital-heavy and reliability-capped in the near term.
**Build priority:** scale phase. Only adds value once S2 is generating commitments.

### S4 — Exchange & Settlement  *owns: Exchange, Outcome*
**Function:**
```
settle(ledger, exchange)  -> payment obligation, receipt, reconciliation
evaluate(exchange, expectation) -> outcome (met|partial|failed)
```
**Normative (Sprint-4 verified):** the exchange is recorded per §4b as an `event://` of type
EXCHANGE carrying the Asset-Ledger title/custody delta (`asset://`) in its embedded
`state_update`; the payment obligation (`obligation://`), receipt (`receipt://`), and
reconciliation (`decision://`) ride that SAME signed EXCHANGE event's state, so every
settlement artifact is covered by the one signed ledger event and the Graph round-trip
reconstructs all of them from history (§3.16, §5 state-delta convention). `evaluate()` emits
an `event://` OUTCOME (met | partial | failed) that S5 captures to update scoped Trust.
**AI role [LEVEL A]:** reconcile, detect fraud/discrepancy, close the record against
expectation.
**Differentiator [LEVEL B]:** low standalone (payment rails, accounting tools) — the
value materializes only when integrated end-to-end with S2 and S3.
**Build priority:** late, as the hook that closes value capture and monetizes the chain.

### S5 — Accountability & Trust Engine  *owns: Accountability, Trust*
**Function:**
```
capture(outcome, provenance)     -> signed evidence (confidential compute)
verify(evidence, axioms)         -> verified result
update(Trust, evidence, weight, recency) -> Trust  # scoped per §3.14
```
**AI role [LEVEL A]:** verification, audit-trail generation, discrepancy detection
and dispute triage, trust scoring. Evidence is hardware-anchored and unalterable
(confidential compute at the edge).
**Differentiator [LEVEL B]: HIGH — nearly unclaimed.** No existing system closes the
loop from "what actually happened" to "verified and the relationship should
continue." This is the moat and the unlock for every other service.
**Build priority:** phase B — the differentiator, funded by S2's revenue.

---

## 4a. The Knowledge Fabric — Where Knowledge Lives (Level A)

Knowledge is not owned by any individual service — it is an orthogonal substrate that
every service draws on (Intent inference, Capability matching, Offer generation,
Execution, and Trust verification all need facts). It resolves the question of where
knowledge lives.

**Principle 1 — The residences are not the knowledge.** Documents, emails, databases,
and correspondence are the *physical residences* of knowledge, but knowledge itself
lives in a unified semantic layer that indexes and links all of them. There is no
single winner among "Documents / Emails / Correspondents / Databases" because the
fabric spans all of them.

**Principle 2 — Sources stay in place.** The fabric does not relocate or copy
content (moving an email into a database destroys custody and provenance). The
original source remains authoritative; the fabric adds a unified index, resolver, and
semantic address, not a duplicate store.

**Principle 3 — Knowledge is addressed by what it is about, not where it sits.**
Every knowledge object carries a typed semantic URI anchored to the identity scheme:
```
doc://contract/2026-0714      mail://alice/grievance-3     db://ledger/final-2026
corr://agency/inquiry-2       ticket://support/4181       chat://session/992
voice://call/2026-0714        log://fulfillment/node-7
```
A resolver maps these to concrete backends at access time, exactly as the earlier
`character://`/`asset://` discipline — references, not literals.

**Principle 4 — Knowledge is relationship-anchored.** Each object links to the
person/org/role/relationship it concerns. A person's context graph therefore includes
not just their recorded attributes but their documents, mail, correspondence, tickets,
and history — the unified-person model from the ontology, extended to knowledge.

**Principle 5 — Knowledge participates in Trust.** Every object carries provenance
(author/origin, custody chain) and a trust score from the S5 loop. Untrusted, stale,
or unverified knowledge is downweighted (or flagged) before it shapes a matching,
offer, or execution decision. Knowledge and action share the same trust currency.

**Knowledge object model (Level A):**
```
Knowledge {
  uri            : typed semantic URI
  kind           : doc | mail | db | corr | ticket | chat | voice | log | other
  source         : original residency reference (authoritative)
  entities       : [person://, org://, subject//…]          # what it is about
  relationships  : [Relationship refs]                      # which interfaces it serves
  provenance     : author, origin, custodianship chain
  trust          : score from S5 loop; recency; evidence
  access         : scope/permission  (reuses the instance/role gate of S1)
  content        : reference to source content                # not a copy
}
```

**Router implicit:** the same routing seam that sends a *task* to a model also routes
a *query* to the knowledge the task needs — pulling from whichever backend the object
lives in, trust-weighted. Knowledge retrieval is not a separate system;
it is the fabric under the chain.

**Why the fabric matters to ROI (Level B):** most ground truth for the high-value
stages (Intent, Matching, Executing, Settlement, Trust) already exists, scattered in
orgs' documents, mail, databases, and correspondence. The fabric captures that value
without requiring data migration, and it is what lets the Trust engine verify a claim
against the original source rather than a copy. It converts existing organizational
knowledge into the trusted substrate the entire chain runs on.

---

## 4b. The Asset Ledger — Where Assets Live (Level A)

Assets are not knowledge. **Information** is recorded representation (a document can
contain a false claim; an email an opinion; a database corrupted data). **Knowledge** is
information interpreted as a proposition/claim with provenance. **Truth** is an
epistemic status, not a storage category. An asset, by contrast, is what is *held,
owned, and exchanged* — its unit is **title and custody**, not truth. This
distinction changes where and how assets live.

**Principle 1 — Assets have title and custody; knowledge has provenance.** The
differentiator is legal/economic: an asset is a thing that can be owned, transferred,
and settled. A mere fact cannot. Digital assets complicate this (they are
information-like), which is precisely why they need a ledger: a *copy* of a digital
asset is a different asset with its own title — copying is not transfer. The ledger
resolves this ambiguity; the Knowledge Fabric alone cannot.

**Principle 2 — Assets live in a custody-and-title ledger over real residences that
stay in place.** The ledger of record holds entitlement, status, and value. The asset
itself is not relocated: a transfer can settle title without moving a barrel, a file,
or a balance. The ledger references custody; it does not duplicate the asset.

**Principle 3 — Residence is by asset kind.** Each kind has its own physical/legal
home, unified under the ledger:
```
money     → financial accounts / payment rails         (balances, settlement)
goods     → inventory / warehouses / supply-chain       (physical custody)
rights    → registries / licenses / title records       (entitlement)
digital   → object / file stores                         (deliverables, IP, code, media)
capacity  → the capability graph                         (agents'/humans' availability)
```

**Principle 4 — Assets participate in S4 and S5.** Exchange/Settlement (S4) transacts
title; the ledger records every custody/transfer event as signed evidence consumed by
the Trust engine (S5). S5 verification of an asset = verifying it actually exists and
the transfer is valid: clean title, no double-sell, valid custody chain. This is the
substrate that makes S4's fraud/discrepancy detection real.

**Asset object model (Level A):**
```
Asset {
  uri        : asset:// (money | good | right | digital | capacity | other)
  title      : current owner/entitlement  (person://, org://, relationship ref)
  custody    : current residence (account, warehouse, registry, store, capability)
  value      : ledger value + valuation basis
  status     : held | committed | in-transit | delivered | retired
  provenance : custody chain, origin
  trust      : S5 evidence (clean title? condition? verified transfer?)
  content    : reference to residence (not a copy)
}
```

**Why the ledger matters to ROI (Level B):** the value that changes hands in an
exchange is not in every case an asset — it may be service, labor, attention, access,
information, experience, obligation, forgiveness, reputation, or a right. The correct
universal statement is: **an exchange transfers, consumes, creates, destroys, or
modifies resources, rights, obligations, or value** (the Resource abstraction, §3.8).
The Asset Ledger is the slice that carries the title-and-custody parcels among those
resources; it is not a claim about all exchanged value.

---

## 5. The Integration — What Makes It a Chain

The chain is not five products. It is one loop. Each service reads the shared
**Relationship Graph** (person, org, role, stage, trust) and appends to the shared
**Transaction Ledger** (content-addressed, signed evidence of every action). The
loop is the source of compounding ROI.

**Formal state machine:**
```
state:  Relationship(person, org, role, stage, trust, ledger_ref)
loop:
  i     = resolve_identity(subject, evidence)          # S1
  role  = resolve_role(person, org, context)           # S1
  intent    = infer_intent(subject, evidence)          # S2
  offers    = match_offers(intent, capability_models,
                           trust_scores)               # S2, Trust-weighted
  offer     = propose(offers, subject)
  commitment= agree(offer, terms)                      # S3
  actions   = execute(commitment, fleet)               # S3
  exchange  = settle(actions, ledger)                  # S4
  outcome   = evaluate(exchange, expectation)          # S4
  evidence  = capture(outcome, provenance)             # S5, anchored
  trust     = update(Trust, evidence,
                     weight, recency)                  # S5, scoped (§3.14)
  # trust re-ranks S2 next cycle  →  flywheel
```

**Trust function (Level A interface / Level B algorithm), scoped and bounded.** Trust is keyed on
`(subject, target, claim/capability, context)` per §3.14 — not a single global score:
```
T_1(c)   = initial credibility of claim c in this relationship
T_{k+1}(c) = clamp( T_k(c) + alpha*(outcome_k - expectation_k)*evidence_k, 0, 1 )
          # evidence_k ∈ [0,1]; alpha = learning rate; recency-weighted; clamped to [0,1]
```
**Normative (Sprint-2 verified): persistence carries the update's inputs.** The
persisted `trust://` object must carry, as additive envelope fields (schema
`additionalProperties: true`), the exact inputs of its last update — `expected`
(expectation_k), `outcome` (outcome_k), `evidence` (the `evidence://` ref list),
`alpha` (learning rate) and `recency` — so every new score is auditable and
reproducible from the object alone. `Trust.evidence` is an **array** of `evidence://`
refs (`evidence_ref`); a single evidence URI must be wrapped in a list. Updates key on
`(subject, target, claim, context)` independently; an unrelated claim/context stays
untouched — demonstrated running in Sprint 2 (good outcome raised one provider, bad
lowered another, a third with a different claim was unchanged).
**Reputation is separate from Trust.** Reputation aggregates verified *evidence* about
an actor across relationships; each relationship then derives its own scoped Trust from
that evidence. Evidence travels; Trust does not. This preserves privacy and prevents
a single cross-organization social-credit score.
Trust is consumed by S2 (re-rank matching, price risk) and by S4 (settlement terms):
an actor that accumulates verified good outcomes in a given context is routed more
work and billed on better terms. The compounding moat is verified evidence — which can
only be accumulated through the whole chain, so it cannot be replicated by a single
service.

---

## 6. AI Deployment — Where AI Works (LEVEL B)

Consistent with the ROI heuristic — value is highest where a stage is expensive,
error-prone at scale, and under-automated today:

| Stage | AI strength | Existing automation | AI ROI |
|---|---|---|---|
| Identity/Role | High (verify, classify) | High (KYC/IdP) | Medium, commoditized |
| Intent/Matching | High (infer, rank) | Medium (CRM, marketing) | **Highest near-term** |
| Orchestration/Execution | High (plan, route, agents) | Medium (workflow, RPA) | High, capital-heavy |
| Exchange/Settlement | Medium (reconcile, detect) | High (payments, ERP) | Medium, integration-gated |
| Accountability/Trust | High (verify, audit, risk) | **Very low** | **Highest strategic (moat)** |

Concentration: AI is concentrated at the two ends of the chain — the front
(Intent/Matching) for fast revenue and the settlement (Accountability/Trust) for the
moat. The mid-chain (Execution, Settlement) is automated heavily by everyone and is
where value compresses.

**Routing seam [LEVEL A]:** a model router sends each task to local (cheap, private,
own), private cloud (scalable own), or frontier (best capability) — Trust-weighted and
latency/loss-of-capability-priced. This is the same own-vs-rent ladder adapted to
per-task routing.

**Human-escalation floor [LEVEL A — normative]:** any action with
`irreversible(failure) == true` OR `cost(failure) == unknowable` MUST escalate to a
human before execution. Full autonomy is permitted only where failure is cheap and
reversible. This is the guardrail that makes the Trust engine trustworthy.
**Sprint-3 clarified (normative, additive):** the floor OVERRIDES the routing seam's tier —
the closed task is still routed by capability to its best tier (the `seam_tier`, kept for
audit) while its governing executable `tier` is forced to a human until a signed acceptance
is recorded. Escalation compliance is itself auditable purely from the signed, append-only
Ledger ORDER: the irreversible ACTION `event://` must appear strictly AFTER the approver's
signed human DECISION `event://`, which must in turn follow an escalation DECISION — a
checkable property of the history, not a separate flag.

---

## 7. ROI Model and Build Order (LEVEL B — estimates, ordering arguments)

**ROI = (value − cost) − weighted by {feasibility, differentiation}; and estates (near-term
revenue, strategic moat).**

| # | Service | Value | Cost | Differentiation | Near-term ROI | Strategic ROI |
|---|---|---|---|---|---|---|
| S2 | Intent & Matching | High | Med | Med | **Highest** | Medium |
| S5 | Accountab. & Trust | High | High | **Very high** | Medium | **Highest** |
| S3 | Orchestration | High | High | Med | High | High |
| S4 | Settlement | Medium | High | Low | Medium | Medium (integrated) |
| S1 | Identity/Role | Medium | Med | Low | Medium | Medium (substrate) |

**Build order (self-funding):**
- **Phase A — revenue:** S1 substrate (thin) + S2 Intent/Matching. Fast payback, proves
  ROI, funds the rest.
- **Phase B — moat:** S5 Accountability & Trust. The differentiator; cannot be copied
  without the chain; raises the whole system's defensibility.
- **Phase C — scale & monetize:** S3 Orchestration + S4 Settlement, chained onto S2/S5.
  Captures labor substitution and recurring settlement margin.

**Why the chain beats any single service [LEVEL B]:** each service alone competes
against an existing, crowded incumbent (Salesforce, ServiceNow, Splunk, payment
rails). Integrated, they form a flywheel — S2 generates the deal, S3 executes, S4
settles, S5 verifies and builds Trust that re-prices and re-routes the next S2 cycle.
The compounding artifact (Trust on verified behavior) is the durable advantage, and
it is only expressible through the whole chain.

---

## 7A. Failure Modes

1. **Trust-engine false positives/negatives** — an incorrect verification destroys the
   system's credibility. Mitigation: confidence thresholds, human escalation on low
   confidence, conservative defaults, reversible-by-default.
2. **Central single point of failure** — if orchestration mirrors the droid-army
   topology (one control point killed → whole fleet dies), reliability collapses.
   Mitigation: distributed, no central brain; fleet survives node loss (Geth-style
   consensus over control-ship collapse).
3. **Regulatory/legal exposure** — compliance, liability, right-to-audit, PII/privacy.
   Mitigation: confidential compute, PII-minimal design, per-jurisdiction config,
   human floor on irreversible actions.
4. **Model unreliability across the fleet** — a mis-routed or drifting model degrades
   output. Mitigation: route to best tier, guardrails, fallback-to-human, audit
   evidence on every action.
5. **Adoption reluctance** — enterprises won't trust agents or pay for unproven ROI.
   Mitigation: enter on S2 (fast, obvious revenue), make Trust features opt-in and
   demonstrable, price on outcomes not tokens.

---

## 8. Development Roadmap (LEVEL A planning — build to fund itself)

**Two build tracks (per external review, v0.16):** the *platform* build order (substrate
first) and the *customer-value* build order (the product first). They are not the same.
The platform is built S0→S5 as below; the **customer-facing MVP** is built first around
the §7J/§7K case-led loop, so the thing an owner opens is demonstrable before the full
substrate exists:

```
MVP (customer value first):  Relationship → Cases → Tasks → Exceptions → Attention
                             → AI recommendation → Human decision → Verified outcome
```
This is the first killer workflow and the target of the §7L test — not a late feature.

**Sprint 0 — Specification.** This document, the ontology as a schema, the Relationship
Graph + Ledger contracts, a conformance validator, and 5+ canonical lifecycle
examples. The spec precedes software: others can build against the contracts while
the platform is developed.

**Sprint 0 — Surveys & external data sourcing (explicit sprint-0 research), each with
a written deliverable and a Definition of Done:**
1. **§7I data-source & licensing survey** — reality check on news and social-media
   access: which providers (Reuters, AP, wires, X/LinkedIn/Reddit/etc.), which are
   licensed and cost-effective, API rate limits and terms-of-service constraints,
   and a resilient fallback (e.g. GDELT/aggregators). DoD: a ranked source matrix with
   cost/T.o.S/limit per source and a default ingestion set chosen.
2. **§7H jurisdiction & tax-filing survey** — confirms the federal/state/local filing
   set (§7H.3), e-file mandates, filing calendars, and provider (Avalara/Vertex/Sovos,
   payroll, treasury) scope and cost. DoD: a verified filing-calendar seed per target
   jurisdiction and a vendor comparison.
3. **§7G BI report-catalog validation** — checks the standard business report set
   (three statements + management package) against authoritative references for the
   target sectors. DoD: a validated, versioned report catalog with defining metrics.
4. **§7I employee/customer data boundary** — confirms what employee and customer
   sentiment data may legally and ethically be ingested under Consent/Disclosure, per
   jurisdiction (§§3.19, 7B). DoD: an intake allow-list and a privacy-policy skeleton.

These surveys are gating: they de-risk the source/format/jurisdiction assumptions that
Sprints 1–5 depend on. Treat "survey done" as a completed checklist item with a written
report, not a conversation.

**MVP — Case-led operating loop (customer value FIRST; parallel to platform Sprints).**
Build just enough substrate to close the loop once: Relationship → Case → Exception →
Task → Attention/Acknowledgement → AI recommendation → human Decision/Approval →
execution → verified Outcome → a Learning entry. DoD: §7L questions 1–8 answered with
evidence for one fictional company, #8 becomes assigned, authorized work, and #10
records a learned outcome. This is the product demonstrable on day one — not deferred
to Sprint 5, per review #23.

**Sprint 1 — S1 substrate + S2 minimum.** Identity/role resolution thin integration +
an Intent/Matching service for one role (customer) on one domain (e.g. a quoting or
triage flow). Definition of Done: a cycle from identity → matched offer, human-verified,
on the shared ledger.

**Sprint 2 — Trust engine minimum.** Capture + verify one outcome class; compute and
write Trust; Trust visibly re-ranks S2 results. DoD: Trust demonstrably changes
routing/pricing in a test harness.

**Sprint 3 — Orchestration (S3) + human floor.** Commit→execute with an agent fleet
across the routing seam; irreversible actions escalate to a human. DoD: a full
S1→S5 cycle on one relationship, end-to-end, with signed evidence at each step.

**Sprint 4 — Settlement (S4) and multi-role/multi-org extension.** Settlement
integration (payment rails/ERP), then extend from customer to employee/citizen/donor
roles and private/public/charitable orgs. DoD: one relationship across two roles and
two org types chained through the full loop.

**Sprint 5 — Business Operating Layer (the product).** Case, Goal/Metric, Task/Work
Queue, Exception management, Priority/Attention, Dependency — built on the §7J red
core and the Appendix F additions. DoD: the cockpit (§7J.9) shows business health,
prioritized attention (exceptions→cases→tasks), and an AI recommendation with the
authority it requires; one end-to-end exception→case→task→verified-outcome cycle.
The ranked beyond-backlog (§7J.10: process mining, change detection, scenario,
decision learning, organizational memory, universal query, benchmarking) is Phase B,
added only after this proves out.

> **Status (v0.22):** Sprint 5 — Business Operating Layer is **COMPLETE** and the S1→S5
> platform chain is fully built and verified (Sprints 0–5). The §7L Business Indispensability
> Test is answered with evidence for one fictional company (Quoteko): health + prioritized
> attention in the cockpit, #8 becomes assigned authorized Task work, and #9/#10 are satisfied
> in a verified, learned outcome. See `archive/sprints/sprint-5/` and `archive/sprints/COMPLETE.md`.

**Honest constraints:** near-term fully-autonomous white-collar work is mostly
augmentation + redeploy-to-oversight, not wholesale replacement. The design embraces
that: the human-escalation floor is the feature, not a limitation, and it is what
makes the Trust engine sellable.

**Top risks (likelihood × impact):** (1) Trust accuracy — HIGH×HIGH; (2) regulatory —
MED×HIGH; (3) model reliability — MED×HIGH; (4) adoption — MED×MED; (5) SPOF — LOW×HIGH.
Order of attack: (1) first via evidence + escalation; (2) via architecture; (3) via
routing seam; (4) via S2 revenue entry; (5) via distributed topology.

---

## 7B. Security, Privacy & Compliance (normative)

Enterprises will not adopt a relationship/Trust platform without these being
first-class. Requirements:

- **Threat model** MUST be explicit before Sprint 1: high-value targets are the Trust
  engine (tampering corrupts reputation), agents holding delegated authority (abuse,
  hijack), cross-org evidence sharing, and the Knowledge Fabric (sensitive records).
- **Authorization is capability-based.** `authorize()` (S1) returns a bounded
  capability (scoped, revocable, expiry-bound), not blanket privilege. **Delegation
  revocation** (§3.4) is first-class: removing `delegation://` must immediately void
  the associated capability.
- **Disclosure gate + audit** operationalize §3.19: any linkage across relationship
  contexts (inferring same-person) is a logged, consented, auditable act — never a
  default inference. Purpose limitation is enforced per context.
- **Regulated data** (PHI, financial, biometric, court/government records) is
  tagged per jurisdiction; jurisdiction-specific rules gate access and processing.
- **Confidential compute** assumptions are named: hardware root of trust, attestation,
  key management, and evidence anchoring. These are dependencies to be specified in
  Sprint 0, not assumed available.
- **Knowledge Fabric** supports right-to-forget and data-minimization patterns
  consistent with per-source provenance (Section 4a), without breaking round-tripping.

## 7C. Shared Graph + Ledger — Implementation Model

The single integration point; underspecifying it invites the droid-army failure the
same document criticizes. Requirements and deferred decisions:

- **Model:** property-graph vs RDF vs hybrid is OPEN — decided in Sprint 0; the
  ontology must survive the choice regardless.
- **Ledger semantics:** the append-only Ledger MUST be content-addressed and signed
  (per §2). Whether it carries cryptographic/non-repudiation properties across
  adversarial parties (vs application-level integrity only) is an explicit Sprint-0
  decision, driven by Section 10, Q4 (multi-org sharing).
- **Consistency & partitioning:** cross-org sharing, multi-tenancy, and partition
  strategy decided in Sprint 0.
- **Interaction under load:** how Trust updates, evidence anchoring (confidential
  compute), and label resolver reads compose with the store (Section 5 / 4a).
- **Recovery:** failure and recovery of the substrate itself, beyond the high-level
  SPOF note — no control-ship collapse (§7A-2).

## 7D. Sprint 0 Scope — Implementation Contracts & Research Workstreams

Turns Grok's gaps and Section 10's open questions into **committed scope with owners**,
so nothing is deferred silently:

**A. Contracts (the gate for independent implementers):**
1. YAML schema + formal field definitions for `Relationship`, `Interaction`, `Event`,
   `Expectation`, `Claim`, `Evidence`, `Decision`, `Consent`, `Delegation`, Trust, and
   every Appendix C URI scheme.
2. Relationship Graph + Ledger API surface, event schemas, serialization, content
   addressing, and signature/verification model.
3. Conformance validator; the 20 interactions of Appendix E become **executable
   fixtures**, not prose.
4. EBNF grammar for the lifecycle. **Shipped:** `schema/relational-os-lifecycle.ebnf`
   (relationship/interaction/event/state spine, Relationship + Case state machines,
   the five §7J nouns, derived-exception/priority chains, RFC-3339 temporal, typed-URI
   grammar). The JSON Schema remains the normative type contract; the EBNF is its
   lifecycle-grammar companion (gap-closure noted in the Version Log, v0.22).

**B. Trust closure (owners: S5 + gate):**
- Cold-start T₁ (§10.Q1) — Phase B research item.
- Transferability of Trust (§10.Q2) — confirm relationship-scoped assumption.
- Verification axioms for subjective outcomes (§10.Q3) — bound engine to provable
  claims; epistemic boundary per §3.17.
- Reputation aggregation WITHOUT a de-facto social-credit score (§3.14) — Phase B.
- Dispute→adjudication workflow + authority to resolve contested Trust — Phase B.
- Evidence-submission incentives / anti-gaming (§3.18 Incentive) — Phase B.

**C. Operations & product (Phase B, not Sprint 0):** human-loop UI/SLA/queue/override
and audit; observability/metrics/logging/tracing/evaluation harness; error handling,
retries, compensation, partial failure; routing-seam cost/latency/quality/fallback
policy; agent-fleet capability discovery/sandboxing; monetization pricing; deployment
models (SaaS/hybrid/on-prem/air-gapped) and data residency. Market positioning vs
specific incumbents is tracked here (Phase B), not Sprint 0.

**D. Non-goals (explicitly out of scope):** NOT a model lab, NOT a payment processor,
NOT an identity vendor, NOT a CRM/ERP/ServiceNow replacement — operates beneath and
integrates via the contracts. These repeat §2 scope but are stated here so Sprint 0
scope stays bounded.

**E. Surveys & external-data research (Sprint-0 committed):** the data-source and
licensing survey (§7I), the jurisdiction and tax-filing survey (§7H), BI report-catalog
validation (§7G), and the employee/customer data boundary review (§7I). Each has a
written deliverable and a Definition of Done; all four are gating for Sprints 1–5
(details and DoDs in §8 Sprint 0).

**F. Business Operating Layer (Sprint 0 / Sprint 5):** Case, Goal/Metric, Task, and
Dependency enter the Appendix F schema and contract list (§7D-A); the §7J.10 beyond-
backlog (process mining, change detection, scenario, decision learning, organizational
memory, universal query, benchmarking) is registered as Phase-B research, not Sprint 0.

---

## 7E. Architecture — Backend/​Frontend split, customer interfaces, and IoT

The system is explicitly split into a **back end** and a **front end**:

```
                    BACK END (the platform)
   services S1–S5 · substrate (rules/rights/consent/authority) · graph + ledger
   Trust engine · routing seam · hub / cloud tiers          ← source of truth
        ▲                    ▲                      ▲
        │                    │                      │
  ┌─────┴──────┐     ┌───────┴────────┐     ┌──────┴────────┐
  │  FRONTEND  │     │ CUSTOMER CHANNEL│    │   IoT CHANNEL │
  │  (admins / │     │ PC · tablet ·   │    │  headless      │
  │  operators)│     │ phone · web/PWA │    │  devices       │
  └────────────┘     └────────────────┘    └───────────────┘
```
The back end carries the ontology and the chain (§3–§5). The front end is a thin
presentation/action layer for humans; IoT devices are a separate headless channel
that produces Evidence/Events and receives actuation. Neither hosts the substrate.

### 7E.1 Back end
Everything specified as "the platform" — S1–S5, the cross-cutting substrate, the
Relationship Graph (state) and append-only Ledger (history), the Trust engine, and the
routing seam. Deployed on the hub or cloud tier (§G.7). This is unchanged by form
factor.

### 7E.2 Customer interfaces — PC, Tablet, Phone (+ Web/PWA)
**Choice: Flutter (primary) for native apps + Web/PWA for zero-install.** One codebase
compiles to all six targets, so customer interfaces ship to every OS with no rewrites:

| Form factor | OS | Support |
|---|---|---|
| Phone | Android, iOS | native from one codebase |
| Tablet | Android, iOS | native from one codebase |
| PC | Windows, macOS, Linux | native desktop from one codebase |
| Any, no install | **Web / PWA** | same codebase in the browser (zero-install) |

The customer interface is a **thin client**: it authenticates (OIDC, §G.5), renders the
Relationship Graph, and lets the customer act — request, offer, consent, dispute,
decide — by posting Events to the back end. The back end is the source of truth; the
front end is a cached view with offline grace.

**Honest constraints:** iOS restricts long-running background agents and some PWA
features; heavy/continuous agent work is delegated to the hub/cloud. UI is responsive
(PC = dashboard, tablet = split-view, phone = stacked drawer) via adaptive layout.

### 7E.3 Customer client responsibilities
- **Identity & consent:** OIDC + a local capability wallet presenting
  consent/authority/delegation scopes (§3.4/§3.7); disclosure gate on cross-context
  linkage (§3.19).
- **Offline-first:** capture Events locally (embed store), idempotent replay to the
  ledger on reconnect (§3.16); client is disposable and re-provisionable.
- **Inference:** optional local (cheap/private) tier of the routing seam; offload to
  hub/cloud otherwise (§6).
- **Evidence capture:** sensors/camera/mic/input as human-facing Evidence within §7B.

### 7E.4 IoT channel — headless devices (a distinct class, not a UI)
IoT devices (`device://`, `sensor://`, `meter://`, `machine://`, etc.) are **not
interactive customers**. They are programmatic actors that produce Evidence/Events
and execute actuation:
- **Produce:** telemetry, sensor reads, meter reads, machine state — posted as Events
  (especially `EXTERNAL` / `STATE_CHANGE`) to the back end.
- **Actuate:** receive commands bound by Authority and Delegation (§3.4).
- **Channel:** lightweight pub/sub — **MQTT** (or CoAP for constrained devices) through
  a gateway that signs and verifies into the ledger (Kafka). At-least-once delivery +
  idempotent event ID protects against loss/duplication.
- **Security:** per-device identity + attestation/trust level (§7B); credential is
  a short-lived device token, not a shared secret; a compromised device gets a bounded
  capability and is revocable.
- **Fleet:** device management + firmware OTA; devices versioned like software (§3.19).

### 7E.5 Security & trust (extends §7B)
- Frontend: OS keychain/keystore/TPM, local data-at-rest encryption, cert pinning.
- IoT: per-device token + attestation; MQTT over TLS; gateway is the tamper point and
  the ledger ingress.
- Device-attestation/trust level factors into authorization for BOTH channels —
  a low-trust device gets a bounded capability (§7B).

### 7E.6 Update & deployment
- Frontend: OTA via app stores + PWA refresh; client schema-versioned per §3.19
  (stale client = upgrade, never corrupt).
- IoT: gateway-managed firmware OTA with staged rollout; devices must not be
  bricked by an interrupted update.

### 7E.7 Non-goals for the device/front-end layer
- NOT a peer host of the substrate (no Neo4j/Kafka/Postgres on a phone or device).
- NOT the Trust/compute authority — the hub/cloud is; devices/frontends are clients
  with offline grace and local inference only.
- IoT devices are NOT general-purpose customer interfaces; they are event producers
  and actuators under delegation.

---

## 7F. Audit Layer — continuous integrity review of all entities

A cross-cutting service (an **auditor** actor) that continuously and on-demand reviews
every entity — Actors, Relationships, Events, Ledger, Graph, and the substrate objects
(Consent, Authority, Delegation, Expectation, Evidence, Claim, Dispute, Trust, Rules)
— for integrity. Its purpose is early detection of data corruption, process gaps, and
security drift; it is part of the "ease of support" and redundancy story (§7D-C, G.6).

### 7F.1 Check classes (what the layer looks for)
- **Referential integrity** — dangling URIs: every `relationship://`, `event://`,
  `claim://`, `evidence://` points at existing actors/objects; no orphans.
- **Ledger ↔ Graph agreement** (§3.16) — the append-only history and the current-state
  graph are consistent; no event that should have changed state is missing from it.
- **Schema conformance** — entities validate against the Appendix F schema and URI
  catalog (identity / relationship / domain-object separation, §C1/C2).
- **Missing records** — expected-but-absent: an ACTIVE relationship without required
  Consent; a Commitment without an Expectation; an Exchange without a settled Outcome;
  a signed event missing its source Evidence.
- **Trust setup** — every relationship has a seeded, bounded Trust for each claim
  (cold-start T₁ present, §10.Q1); no missing/NaN/never-updated Trust on active
  relationships; Trust within [0,1]; recency within policy.
- **Authority/Delegation completeness** — every Action that performed has a matching
  Authorization/Delegation on record; no action with missing authority; expired or
  revoked delegations honored (§3.4, §7B).
- **Evidence completeness & health** — every Outcome succeeds or fails through a Claim
  with Evidence; no open Dispute stalled without adjudication (§3.17/§3.13).
- **Versioning integrity** — revision chains are gapless (§3.19); no contract/rules
  revision skips an effective range.
- **Security/compliance** — disclosure-linkage (same-person across contexts) is never
  unlogged (§3.19); revocations enforced; no expired consent/authority still granting;
  no regulated data escaping its jurisdiction (§7B).
- **Timing anomaly** — event clock-order violations (an event dated before its parent),
  duplicate event IDs, ledger hash-chain discontinuities (§G.3).

### 7F.2 Behavior
- **Cadence:** continuous scans + scheduled sweeps + on-demand runs.
- **Output:** findings are themselves **first-class signed Events** in the ledger
  (each an `audit_finding`, with severity: info / warn / critical), feeding a
  remediation queue. Nothing the audit finds is outside the ledger — audit is
  evidence-producing like any other actor.
- **Authority:** the auditor is a read-scoped actor with attestation; it cannot mutate,
  only report. Findings route to §7D human-loop for action.

---

## 7G. BI Layer — standard reports for running a business

A reporting service that turns the Relationship Graph + Ledger into standard business
intelligence. **The ledger is the audit-grade source of truth; BI reads queryable
projections (analytics warehouse), never the live graph under load** (separation per
§7C). Catalog grounded by a survey of standard BI/management reporting (2026) plus the
canonical accounting report set.

### 7G.1 Core financial statements (produced from GL/ledger events)
| Report | Source objects |
|---|---|
| **P&L / Income statement** | revenue & expense GL events |
| **Balance sheet** | asset/liability/equity ledger positions |
| **Cash-flow statement** | money inflows/outflows over period |
| Budget vs actual (variance) | budget// + settled/txn events |
| Segmented profitability | income by product/segment/org unit |
| Cash-flow forecast / working capital | outstanding orders, AP/AR aging |
| AR aging and AP aging | invoice/receipt/payment events |

### 7G.2 Customer & demand
| Report | Measures |
|---|---|
| Revenue by product / segment / region / channel | sum over settled Outcomes |
| Customer acquisition cost & lifetime value | investment events vs retained value |
| Churn / retention / repeat purchase | relationship state (Terminated vs Active) |
| Open orders & pipeline | order/offer states |

### 7G.3 Operations & fulfilment
| Report | Measures |
|---|---|
| Orders delivered on-time / complete | shipment vs expectation (delivery) |
| Backlog & capacity | open commitments vs capability |
| Inventory / stockout (if applicable) | asset://good positions |
| Service level & dispute rate | resolved disputes / outcomes |

### 7G.4 Workforce (employee channel)
| Report | Measures |
|---|---|
| Headcount, hire/termination, turnover | employee relationships + state machine |
| Utilization & cost per job | labor/workorder events |
| Payroll summaries | compensation events |

### 7G.5 Supplier & procurement
| Report | Measures |
|---|---|
| Spend by supplier & category | PO/invoice events |
| On-time / in-full delivery rate | supplier shipment vs Expectation |
| **Supplier trust / risk** | S5 Trust per supplier relationship |

### 7G.6 RelationalOS-native (the differentiator)
| Report | Measures |
|---|---|
| **Trust distribution** | Trust over relationships by actor/context (§3.14) |
| **Evidence & reputation health** | aggregate verified evidence; reputation (not Trust) score |
| **Dispute pipeline** | open → adjudicated → resolved; resolution cycle time |
| **Audit health** | §7F findings by class/severity over time |
| **Consent/authority hygiene** | expiring, expired, revoked grants (§3.7/§3.4) |

### 7G.7 Compliance / regulatory
| Report | Measures |
|---|---|
| Filing & licensing status | filing/return/license objects vs jurisdiction |
| Regulated-data exposure | §7B-tagged records, cross-context access log |

### 7G.8 BI mechanics
- Analytical **warehouse + SQL transforms** (dbt) over ledger projections; a BI tool
  (**Metabase / Apache Superset** self-serve; Looker/Power BI/Tableau for enterprise)
  renders the catalog (§G.15). Reports are versioned (§3.19) and themselves addressable
  (`report://`).
- **Statutory core is reference-grounded (Sprint-0 survey 3):** income / balance sheet /
  cash flow map to U.S. GAAP (FASB ASC 205/210/220/230) + SEC Regulation S-X Article 3;
  the catalog is versioned at `report://catalog/vN`. Revenue recognition (ASC 606), lease
  (ASC 842), and segment nuances still require an accountant's judgment — the ledger-based
  mapping is architecture, not a substitute for it.
- Trust-weighted: any report touching reputation reads scoped Trust / evidence, never a
  single global score (§3.14).

---

## 7H. External Interfaces & Regulatory / Payroll / Tax Reporting

A **gateway layer** that connects the platform to external systems (financial rails,
payroll providers, tax authorities, regulators, and government). Principle: every
external exchange is normalized into the ontology — the outgoing original and any
receipt/confirmation are stored as **Evidence** in the ledger (`filing://`,
`submission://`, `payment://`), so "we filed X on date Y with authority Z" is provable
and auditable (§7F). Providers and formats are connectors, not owned machinery.

### 7H.1 Financial & treasury interfaces
| Rail / system | Class | Notes |
|---|---|---|
| **SWIFT** (MT/ISO 20022) | cross-border, correspondent banking | wire + message standard |
| **Fedwire**, **CHIPS**, T2/CHAPS | large-value RTGS | finality for big moves |
| **ACH** (NACHA) | batch payments | payroll, vendor, debits |
| **SEPA** Credit/Debit | EU batch | region-specific |
| **FedNow**, **RTP**, SEPA Instant, Faster Payments | real-time | instant credit |
| Card networks (Visa/MC/Amex) | merchant settlement | if the org is a merchant |
| Bank APIs / host-to-host (camt.053, MT940/942, PSD2/open-banking) | treasury & statements | reconciliation → GL |

### 7H.2 Payroll & HR interfaces
- **Providers (connectors):** **ADP** (Run/etc.), Paychex, Gusto, UKG/Kronos, or in-house
  — the platform integrates, it does not re-implement payroll.
- **Forms & filings:** W-2/W-3, W-4 (withholding), **1099-NEC** (contractors), state
  **new-hire reporting**, **SUTA**/unemployment, workers-comp premium reporting, **ACA**
  (1095-B/C and 1094-C transmittal), **EEO-1** and OFCCP/VETS-1002 (when applicable),
  benefits (COBRA, FSA/HSA, retirement deferrals).

### 7H.3 Tax reporting — three tiers (survey-grounded)
**Federal (IRS):**
- Income: 1120 (C-corp), 1120-S (S-corp), 1065 (partnership), 990 (nonprofit), 1040 (sole prop) — by entity form.
- Payroll/employment: **941** (quarterly), **944** (annual), **940** (FUTA).
- Excise: **720**.
- Information returns: W-2/W-3, **1099 series** (NEC, MISC, INT, DIV, R, K), **1095-B/C + 1094**
  (ACA), 5498/5498-SA (retirement).
- Reporting: **FBAR** (FinCEN), **FATCA**; e-file mandates.

**State:**
- Income / franchise / **PTET** (pass-through entity tax), **sales & use** (economic-nexus
  registration), payroll/UI (**SUTA**) and withholding, property, gross-receipts/
  occupancy (where applicable), business registrations.

**Local (city/county):**
- Sales/use tax, **business license / B&O**, occupancy/tourism, property, local
  payroll-withholding where a city imposes it (e.g., Seattle, New York).

**Tax automation (connectors):** Avalara, Vertex, Sovos, TaxJar for calculation and
e-file; provider choice is Phase-B procurement, not Sprint 0.

### 7H.4 Regulatory & securities interfaces
- **Securities (public):** **SEC EDGAR** — 10-K, 10-Q, 8-K, proxy (DEF 14A), insider
  Form 3/4/5, Section 16; **FINRA** (brokers/dealers).
- **Insurance:** **NAIC** / **SERFF** state filings.
- **Banking:** state/federal Call Report, money-transmitter licensing, **BSA/AML**,
  SAR/CTR.
- **Healthcare:** **HIPAA X12** (837 claims, 835 remits), CMS, NPPES enrollment.
- **Energy/utilities:** **FERC**, state PUC rate/reliability filings.
- **Labor/environment:** **OSHA** (300A log), DOL, **EPA/EHS** emissions & TRI.
- **Transport/telecom:** DOT/FMCSA (fleet), FAA (aviation), IATA; FCC licensing, E-rate;
  state PUC (telecom/utility).

### 7H.5 Government & public-org interfaces (ties §C14)
Licenses, permits, and registrations per jurisdiction; `filing://`/`return://`
submission; **grant reporting** and awarded-contract compliance (public/charitable);
FOIA/transparency disclosure. Government remains the coercive/authority interface
(§3.1), handled as imposed Obligations, not voluntary exchanges.

### 7H.6 Integration mechanics
- **One gateway:** connectors normalize external systems to ontology contracts; every
  exchange is a signed Event with the original payload preserved as Evidence.
- **Filing/compliance calendar:** a scheduler of jurisdiction × form × deadline with
  automated reminders that escalate to the human-loop (§7D-C). Missed-filing risk is an
  audit finding (§7F). A Sprint-0 **seed calendar** (US federal + New Mexico, incl.
  Albuquerque local-option GRT) ships from survey 2; calibrating other jurisdictions is
  a Phase-B provider task (§7H.7).
- **Format adapters:** ISO 20022 / SWIFT MT, NACHA, X12 EDI, XML/JSON API, and PDF/paper
  fallback for authorities without e-file.
- **Receipts as evidence:** e-filing acceptance/trace numbers stored as Evidence, feeding
  §7F (filed-on-time proof) and §7G compliance reports.
- **Idempotency/retry + dead-letter** for carrier and authority failures; jurisdiction-
  aware routing honors §7B data-residency.

### 7H.7 Non-goals
- NOT an in-house tax engine, payroll provider, or bank — connectors only.
- NOT a registry of every jurisdiction's law (§7B/§7D-B handles jurisdiction handling);
  provider and jurisdiction calibration is Phase B.

---

## 7I. Market & Social Intelligence (media, sentiment, trend)

Ingests **external signals** — news services (e.g. Reuters, wire/regulatory newswires)
and **social media** — and turns them into **recommended business actions**. The
load-bearing boundary: external feeds are ingested as **Claims with provenance**, not
as truth, and they *inform* decisions but never execute them unilaterally. Any derived
action routes through Authority/Delegation (§3.4) and the human-escalation floor (§3.19,
§7B). This is the guardrail that keeps a market/sentiment watcher from becoming a
rogue auto-actor.

### 7I.1 Intake sources
- **News / authoritative:** Reuters (and AP, wire/regulatory newswires, BusinessWire,
  GlobeNewswire, company/industry vertical feeds) via official APIs/RSS.
- **Social media:** X/Twitter, LinkedIn, Reddit, Facebook, Instagram, TikTok — per
  platform, using licensed/official APIs and within terms of service.
- **Reputation / review platforms:** Trustpilot, Yelp, Google Reviews, app-store
  reviews, and **Glassdoor/employee feedback** (the employee-reputation population).

### 7I.2 Processing (into the ontology)
- Every signal is normalized as an **EXTERNAL Event** (§3.16) → stored as a **Claim
  with provenance** in the Knowledge Fabric (§4a), carrying source credibility and a
  trust weight (§3.17).
- **Entity extraction:** the affected actors — the business, competitors, products,
  employees, regulators — linked to `person://`/`org://`/`relationship://`.
- **Signal typing:** what kind of change — market (price, supply, FX, competitor,
  merger), regulatory/legal, reputational, or employee-community.
- **Sentiment & trend:** aggregate sentiment per entity; detect spikes/anomalies vs a
  rolling baseline; trend over time. Sentiment is an **inference with a stated
  confidence**, not a fact.

### 7I.3 Business-action derivation
A Decision layer (§3.12) converts signal + context → **recommended actions** targeted
at the three affected populations:
- **Market change** → recommend: hedge, supplier diversification, price/inventory
  response, sourcing shift, FX/trade adjustment.
- **Reputational (customer)** → recommend: customer communications, service recovery,
  dispute intake, escalation root-cause.
- **Reputational (employee)** → recommend: retention outreach, HR/benefit action,
  internal comms — within §3.19 (no unconsented exposure of employee data).
- **Regulatory/legal** → recommend: compliance action, jurisdiction assessment, filing
  review (§7H).

Derived actions are **recommendations, recorded as Decisions** with source evidence,
alternatives considered, and confidence (§3.12) — fully auditable (§7F). **No
recommendation auto-executes** an irreversible or unknowable-cost action; those reach a
human (§3.19).

### 7I.4 Trust & verification discipline
- External data is a **Claim with provenance**, not capital-T truth (§3.17): source
  credibility weighting; **cross-verification** (Reuters plus a second source) raises
  confidence; unverified, high-impact claims escalate to human, never to auto-action.
- Baseline monitors prevent false-positive storms; anomaly thresholds are calibrated,
  not permanent.
- All ingestion, assessment, and action-recommendation Events are signed and in the
  ledger — the watcher is evidence-producing like any actor (§7F).

### 7I.5 Monitoring framework & integration
- Continuous ingestion via the §7H.6 scheduler (media calendars, not just filing
  calendars); watches keyed to business, competitors, customers, and employees.
- Feeds **§7F** (a reputational spike is an observable) and **§7G** (adds a
  sentiment/trend report class: market-signal, reputation, and employee-sentiment
  reports alongside the existing catalog).

### 7I.6 Non-goals & limits
- NOT an auto-trader and **never auto-executes** market actions.
- Respects platform **terms of service and privacy**; no unmoderated access to
  employee personal data beyond what Consent/Disclosure permits (§3.19, §7B).
- **Data boundary (Sprint-0 survey 4):** ingest **aggregates and de-identified counts**
  by default; treat employee-platform data (e.g. Glassdoor) as sensitive employee data;
  NEVER infer a protected class (health, union membership, politics, biometric) — banned
  under GDPR Art 9 for this purpose and a discrimination risk under EEOC/Title VII. Couple
  review scores to an identifiable person only under a logged, purpose-limited DPIA +
  Consent (CPRA's employee exemptions expired 2023-01-01, so employees hold consumer
  rights). Any derived sentiment→action enters as a Decision (§3.12) with alternatives +
  confidence, escalating to a human where irreversible (§3.19, §7B).
- NOT a replacement for a dedicated social-suite — it captures the signals that matter
  to the three populations and closes the action loop; full social-campaign tooling is
  out of scope.

---

## 7J. Business Operating Layer — Cases, Metrics, Exceptions, Work

**Architectural reframe (external review, v0.15):** the platform is no longer well
described as "a chain of five services." It is now:

```
                 RELATIONALOS
        ┌─────────────┴─────────────┐
        │                           │
    SUBSTRATE                   SERVICES
 (graph · ledger · knowledge   (S1–S5 lifecycle)
  · rules · rights · authority
  · consent · resources · evidence · trust)
        │
        ▼
   BUSINESS OPERATING LAYER
 (goals · metrics · cases · exceptions ·
  tasks/work · priority · dependency · risk)
        │
        ▼
   AI SUPERVISOR  →  HUMAN DECISION MAKER
```
The Business Operating Layer is what a CEO, manager, employee, customer-service agent,
and AI agent actually *do with the system every morning*. This section is deliberately
prioritized (red items spec'd in full; orange/yellow registered as a ranked backlog,
NOT expanded) per external review: the ontology is strong enough — stop adding nouns,
make it indispensable.

### 7J.1 Goals, Metrics, Targets  (Priority 1 — what we optimize toward)
Strategic chain, distinct concepts:
```
PURPOSE → MISSION → GOALS → OBJECTIVES → STRATEGY → PLANS → COMMITMENTS → ACTIONS → OUTCOMES → MEASUREMENT → ADJUSTMENT
```
**Goal** = desired future state; **Mission** = what it exists to accomplish; **Objective**
= measurable result; **Strategy** = how; **Plan** = sequence. A **Metric** is the number
that says whether we're winning:
```
Metric { name, definition, unit, formula, dimensions, target, threshold, period, source, owner }
```
The core AI loop: `Goal → Metric → Actual → Variance → Decision → Action → Outcome`.
Example: target $10M, actual $8.7M, variance −13% → cause candidates → recommended
actions → expected impact → owner → deadline → result. This is business intelligence that
becomes business action (extends §7G beyond reporting).

### 7J.2 Exception Management  (Priority 2 — the heartbeat)
Businesses need *"here are the five things to deal with today,"* not dashboards and
alerts:
```
EXPECTED → ACTUAL → VARIANCE → SIGNIFICANCE → EXCEPTION → ROOT → RECOMMENDED ACTION → DECISION → EXECUTION → VERIFIED OUTCOME
```
The daily heartbeat: an executive opens the system to **seven things requiring
attention** — not 47 dashboards, not 3,000 alerts. Feeds the cockpit (§7J.9) and
inherits Root-causing from §7I evidence + §7J.6 dependencies.

### 7J.3 Case — the universal unit of unresolved business work  (Priority 3 — build around this)
A **Case** is *a business problem that stays open until resolved*. The bridge between
the ontology and the product:
```
CASE
 ├ Actors ├ Relationships ├ Claims ├ Evidence ├ Events ├ Tasks ├ Decisions
 ├ Commitments ├ Deadlines ├ Costs ├ Outcomes └ Resolution
```
Any of these is a Case: customer complaint, insurance claim, employee grievance,
supplier failure, security incident, legal matter, compliance violation, unpaid
invoice, product defect, government inquiry, fraud investigation — and any problem an
AI discovers (§7I/§7F) opens a Case.
**Case lifecycle:** `OPEN → TRIAGE → ASSIGNED → IN_PROGRESS → BLOCKED → RESOLVED → CLOSED` (with `REOPEN`), each with evidence.
Case is the **universal seat** beneath Salesforce cases, ServiceNow incidents/requests,
insurance claims, and government matters — one abstraction, per §7D-A as a Sprint-0 contract.

### 7J.4 Task & Work Queue  (Priority 4 — recommendations become action)
**Task** = work assigned but not necessarily done yet (Action = done, Task = to-do):
```
Task { assigned_to, created_by, objective, dependencies, authority, deadline, priority, status, expected_outcome, actual_outcome }
```
**Work queue states:** `incoming → prioritized → assigned → in_progress → blocked → awaiting_human → awaiting_external → completed → failed`.
Every queue item carries *why it is here, why it is important, the supporting evidence,
the authority required, and what the human must decide* — turning the human from AI
**babysitter** into AI **supervisor**. The Exception (7J.2) → Task → Assignment →
Execution → Evidence → Outcome chain is the operations bridge.

### 7J.5 Priority & Attention  (Priority 5 — don't overwhelm humans)
When the system watches everything, it discovers more than humans can address. It must
answer *what matters most right now*:
```
Priority = f(impact, urgency, confidence, irreversibility, relationship-importance, cost-of-delay)
```
**Notification/Attention:** notify about **decisions or actions requiring attention**,
not raw events. This is the difference between an exception *generator* and an
attention-*management* system.
**Normative (Sprint-5 verified):** Exception (§7J.2), Priority, the AI Recommendation
(§7J.9), and the §7L Q9 **capacity** are *derived* values carried as **additive envelope
fields** on the first-class objects (`case://`/`task://`/`metric://`) — there is NO
`exception:// priority:// recommendation:// capacity://` URI scheme. Capacity (how much/how
often, as opposed to capability = can-do) is expressed for an assigned task as an additive
`assigned_capacity` field (Q9 asks for it; `capacity://` exists as a `$def` but is not a
catalog scheme). Exception/Priority/Recommendation/Capacity are never new nouns (§7J.11,
§C16).

### 7J.6 Dependency & Impact  (Priority 6 — real organizational reasoning)
Business actions aren't independent: `order → inventory → supplier → production →
quality → delivery → invoice → payment`. Represent:
```
Dependency { requires, blocks, enables, derived_from, impacts }
```
Distinct from Relationship (a dependency is directional on workflow, not a bond). This
enables **impact analysis** — "if the supplier shipment fails, these six things break."

### 7J.7 Risk & Capacity (registered, Priority 7–8 — not fully spec'd)
- **Risk** elevated to a first-class business object using the platform's unique
  raw material (relationships + evidence + expectations + dependencies + external
  events + Trust): `{ threat, probability, impact, exposure, affected_relationships,
  evidence, mitigations, owner, deadline, residual_risk }`. Enables "what could go wrong" as a query.
- **Capability vs Capacity:** Capability = can do it; **Capacity** = how much/how often.
  `Demand → Capacity → Constraints → Priority → Optimization → Allocation → Execution`
  (resource allocation is potentially a highest-value AI function).

### 7J.8 SLA
An **SLA** is a specialized **Expectation + Commitment + Consequence** — modeled as
those primitives with a metric, threshold, response/resolution time, availability,
penalty, and escalation. Keeps the ontology universal (no new concept, just an assembly).

### 7J.9 The Cockpit (product embodiment)
The Monday-morning screen — *business health, attention required, strategic, AI
recommendation* — so "tell me what I need to know, what I need to do, and what happens
if I don't" is a real product surface (red items + §7C substrate). It is the customer
facing the Business Operating Layer renders on the §7E frontends.

### 7J.10 Ranked beyond-backlog (registered, NOT expanded — Phase B)
The reviewer's priority order; add these only after the core (7J.1–7J.6) proves out:
```
Process Mining   — the ledger is a process microscope (orders, approvals, handoffs)
Change Detection — state(t1)→state(t2)→delta→significance→attention
Scenario / What-if      — price +8%? supplier fails? rate rise? new location? automate?
Decision Learning       — decision→expected→actual→variance→decision-quality→learning
Organizational Memory   — knowledge ≠ memory; what we decided and why, last time
Universal Query         — natural-language across graph+ledger+knowledge+metrics+cases
Benchmarking            — cross-org normalized comparison under strict privacy
```
Registered in §7D-B as Phase-B research items; none become URI mining.

### 7J.11 URI cap (normative, per review)
Appendix C is NOT extended into new domain noun-mining. Only first-class operational
objects get schemes; everything else is derived:
`case:// goal:// metric:// task:// dependency://` (added to C16). Exception, priority,
alert, and work-queue entries are **derived** from the above — they are not new nouns.

---

## 7K. Business Operating Semantics (short — per external review, v0.16)

The architecture now divides into **four layers**:

```
1. ONTOLOGY        Actor · Relationship · Interaction · Event · State · Evidence · Trust
2. SUBSTRATE       Graph · Ledger · Knowledge · Resources · Rules · Rights · Authority · Consent
3. OPERATING SYS   Goals · Metrics · Processes · Cases · Exceptions · Tasks · Dependencies · Risk · Capacity · Allocation · Decisions
4. BUSINESS INTEL  Forecast · Optimization · Learning · Recommendation · Scenario · Strategy
                       ↓   HUMAN + AI
```

These semantics are **assemblies of existing primitives** — the URI cap (§7J.11, §C16)
STAYS. No new nouns.

### 7K.1 Essential operating semantics
- **Process / ProcessInstance** — Process = the reusable definition of how work should
  flow; ProcessInstance = one actual execution. Gives process-mining a "designed" model
  to compare against the ledger's actual (§7J.10).
- **Policy execution** — executable business logic, not documents: `Condition → Decision
  → Action` (invoice <$5k → AI approves; supplier Trust<.60 → human; contract ≤30 days →
  notify owner; VIP complaint → escalate). Extends OPA/Rego (G.14) from authority to the
  whole operating layer. Possibly the OS's most important feature.
- **Forecast** — Metric gains `Target/Actual/Forecast/Variance/Threshold`. Answers "where
  are we if nothing changes?" and "will we hit the goal?" — not just "did we?".
- **Ownership** — every operational object that can require action has an accountable
  owner (Goal/Metric/Case/Task/Risk/Process/Relationship/Asset/Policy). Structurally
  prevents "somebody else was handling it."
- **Escalation** — trigger→severity→recipient→deadline→fallback→authority→acknowledgement;
  operational, not just a human floor (CFO silent 2h → COO; 4h → contingency).
- **Approval** — `Recommendation → Decision → Approval → Authorization → Execution`.
  Approval is an Interaction/Event type, not a new noun.
- **Acknowledgement** — oversight must be *demonstrable*: Attention→Acknowledgement→
  Accept/Reject/Delegate/Snooze→Action. RelationalOS only claims "human oversight" where
  the human provably took custody of the decision.
- **Causation / Correlation / Idempotency** — every executable Event carries
  `event_id, correlation_id, causation_id, idempotency_key`. Promotes §7H/IoT idempotency
  to a universal Event property (§3.16) and lets the audit reconstruct decision chains.
- **Entity resolution (canonical)** — IBM ≡ International Business Machines ≡ Vendor
  #18392; J. Smith ≡ John A. Smith. Canonical resolution across people/orgs/products/
  suppliers/customers/locations/assets/accounts; essential for the Knowledge Fabric (§4a).
- **Business Model (the value engine)** — how THIS business makes money (merchandiser,
  SaaS, manufacturer, charity): `Purpose→Business Model→Goals→Metrics→Processes→
  Resources→Execution→Financial/mission results`. The optimizer needs to know what
  "better" means before it can optimize.
- **Trade-off / decision analysis** — real choices are "good here, bad there," not
  good-vs-bad; explicit **Options incl. do-nothing**; decision support explains the
  trade-off ("B is best *IF* retention outweighs margin"), not a bare pick.
- **Organizational Learning** (promoted above all, review #25) —
  `Decision→Expected→Actual→Variance→WHY right or wrong→Learning→change future
  decision policy`. The system gets better because the business uses it — the truest moat.

### 7K.2 Elevated (now in operating semantics; still not URI-mined)
- **Risk** and **Capacity/Allocation** (from §7J.7) join the operating layer.
- **Cost of Delay** — a computable cost-curve, not a buried priority term: "what does
  waiting a day cost?" ($12k→$47k→$190k→$630k). Feeds Priority and Allocation.
- **Uncertainty ≠ confidence** — distinguish `Probability / Confidence / Impact /
  Uncertainty` for risk, scenario, forecast, and recommendations.
- **Root-cause has epistemic status** — Observed / Correlated / Suspected / Supported /
  Verified / Unknown. Root-cause is a Claim with evidence (§3.17); prevents AI bullshitting.
- **Org structure is a graph** — who reports to whom, owns budget, approves, holds
  capacity, can delegate — critical to the AI supervisor (§7J.9).
- **Authority ≠ Responsibility** — delegation of *authority* (may act) vs *assignment of
  work* (must perform) vs *accountability* (own the outcome). (§3.4/Task.)
- **Two observability layers** — Technical (is the system working?) vs **Business** (is
  the organization working? — "onboarding takes 3.2 days not 1"). Business observability
  is what RelationalOS owns (§7G/§7J).
- **Process Mining · Decision Learning · Organizational Memory** — promoted from the
  §7J.10 backlog into this semantics set; executed (not just registered) after the core
  operating loop proves out.

### 7K.3 Accept, do not add
Per review: no new §3 primitives, no more Appendix C URIs, no "business model" as one more
ontology noun — it is an assembly. The next milestone is behavioral, not definitional (§7L).

## 7L. Business Indispensability Test — the ten morning questions

The acceptance test for the product (external review, v0.16). Take one fictional
company; RelationalOS must answer these ten questions every morning **with evidence**, and
turn #8 into real work while preserving human authority:

```
1.  What happened?              (state/events over the period)
2.  What changed?               (delta + significance — change detection)
3.  What matters?               (prioritized attention — §7J.5)
4.  What is going wrong?        (exceptions — §7J.2)
5.  Why is it going wrong?      (root-cause WITH epistemic status — §7K.2)
6.  What will happen if we do   (forecast "if nothing changes" — §7K.1)
    nothing?
7.  What are our options?       (options incl. do-nothing + trade-off — §7K.1)
8.  What should we do?          (recommendation with authority required — §7J.9)
9.  Who does it, and do they    (ownership + capability/capacity + authority — §7K.1)
    have the authority/capacity?
10. Did it work, and what did   (verified outcome + organizational learning — §7K.1)
    we learn?
```

**Grading:** v0.15/16 answers 1–4 strongly, 5–8 increasingly, 9–10 incompletely. The
test is the gate: when a fresh fictional company's ten questions are answered with
evidence and #8 becomes assigned, authorized work that closes in a verified, learned
outcome, RelationalOS is an operating system, not an architecture. This is the target
for the MVP track in §8, not a Phase-B add-on.

---

## 9. Implications

- **For incumbents:** RelationalOS competes with Salesforce/ServiceNow/Splunk not by
  doing their slice better but by owning the loop that stitches slices together and
  closes the Trust gap none of them close.
- **For AI vendors (Apple/Nvidia framing):** the platform is a consumer of the routing
  seam, not a model lab. It is agnostic to which silicon or model wins — it wins by
  owning orchestration + verification, which is exactly the "trust and integration
  moat" argument.
- **For enterprises:** the value proposition is a verifiable, integrated workforce
  (agents + humans + oversight) priced on outcomes, not a per-token firehose.

---

## 10. Open Questions

1. **Trust initial values** — how to seed T_1 for a brand-new relationship without
   verified history? Cold-start is unsolved and material.
2. **Trust transferability** — does Trust travel across roles and orgs for the same
   person, or is it relationship-scoped? (Design assumes relationship-scoped; worth
   revisiting.)
3. **Verification axioms** — what counts as "verified outcome" for fuzzy, subjective
   work (judgment, quality) rather than crisp, objective work? The engine must bound
   itself to what it can actually prove.
4. **Multi-org cooperation** — do rival organizations share a ledger, or does each run
   its own? This determines whether Trust is cross-org or siloed.

*(Left open intentionally — see skill norm: do not answer questions the owner has not
answered.)*

---

## 11. Design Rationale (why not the alternatives)

**Why a 5-service chain, not one "super-platform"?** A single monolith is undeliverable,
unfundable, and un-auditable. The chain lets work ship in ROI-sequenced slices (S2
first) while the integration contract keeps the end-state coherent.

**Why a shared graph + ledger, not per-service databases?** The compound asset is a
relationship that travels the whole lifecycle with trusted provenance. Siloed stores
cannot produce it. Per-service data is the droid-army mistake: a fragile, non-integrated
fleet.

**Why concentrate AI at both ends, not the middle?** The middle (Execution, Settlement)
is where everyone's AI already is — value compresses there. The front generates the
revenue; the settlement end builds the uncopyable Trust. Paraphrase of the ROI
heuristic from the source conversation: the crown value sits at the two ends.

**Why a human-escalation floor and not full autonomy?** Unverified autonomy is the
Rogue failure mode and is unsellable to enterprises. Oversight is the feature that
makes Trust trustworthy, and it matches the honest near-term reality of
augmentation-over-replacement.

**Why not build a model lab?** Model capability is a commodity and the routing seam
already buys the best tier. Competitive advantage is in orchestration + verification,
not in owning a model.

---

## Appendix A — Appendix (Set aside for a separate companion paper / later
development; included here for completeness.)

- **Unified Person Graph across roles** — the "same person across every interface"
  insight as its own deliverable. Full realization is Level-B strategic and the
  longest to pay off (needs the ontology + integrated data across orgs). Tracked
  as an open question (Section 10, item 4) rather than a committed module in v0.1.
- **Formal EBNF / schema for the lifecycle** — deferred until the ontology stabilizes
  (Sprint 0 will produce a YAML schema).

---

## Appendix B — Survey: Business Types in the Top ~100 US Companies

Grounding for the URI catalog in **Appendix C**. Source: the current largest-100
US companies by revenue (Wikipedia / Fortune data, parsed 2026-08-31). 119 companies
were parsed and grouped into sector families:

| Sector family | ~count in top 100 | Representative companies |
|---|---|---|
| Financials | 25 | JPMorgan, Bank of America, Citigroup, Wells Fargo, Goldman Sachs, Morgan Stanley, Visa, Mastercard, AmEx, Berkshire Hathaway, Progressive, Allstate, Travelers |
| Technology | 18 | Apple, Microsoft, Nvidia, Alphabet, Amazon, Meta, Oracle, Dell, Cisco, IBM, Intel, Broadcom |
| Healthcare / Pharma | 17 | UnitedHealth, CVS, McKesson, Cencora, Elevance, Cigna, Centene, Humana; J&J, Pfizer, Merck, AbbVie, Lilly, Amgen, Bristol-Myers |
| Food / Bev / Consumer | 13 | PepsiCo, Coca-Cola, Kraft Heinz, Mondelez, General Mills, Tyson, Archer-Daniels, ADM, Philip Morris, Altria, P&G |
| Retail | 10 | Walmart, Costco, Home Depot, Target, Kroger, Lowe's, Albertsons, Dollar General, Best Buy |
| Energy / Chemicals | 10 | ExxonMobil, Chevron, ConocoPhillips, Marathon Petroleum, Valero, Phillips 66, Dow, LyondellBasell |
| Aerospace / Defense / Aviation | 7 | Boeing, RTX, Lockheed Martin, GE Aerospace, Delta, United, American, Southwest |
| Telecom | 4 | AT&T, Verizon, T-Mobile, Comcast, Charter |
| Automotive | 3 | GM, Ford, Tesla |
| Media | 2 | Disney, Netflix |
| Logistics / Transport | 2 | UPS, FedEx |
| Industrial / Apparel / Services / Misc | ~9 | machinery, apparel, diversified services, conglomerates |

**Implication for the address space [Level B]:** the top of the US economy is
dominated by financial services, technology, healthcare/pharma, consumer/retail,
energy, and aerospace-defense. A system serving this population must address, per
company: financial ledger machinery (GL, accounts, policies, claims), devices and
endpoints (physical and digital), industrial/operations entities (units, parts, BOMs,
wells, aircraft, fleets), commercial lifecycle entities (customers, accounts, orders,
contracts, invoices), and regulated knowledge records (compliance, filings, PHI/
patient, policy). Appendix C covers all of these.

---

## Appendix C — URI Address Space (Comprehensive Catalog)

All entity types a company in the surveyed population may carry. Conventions:

- **Canonical identity:** every entity has exactly one typed URI. `person://` is the
  canonical identity for a natural person; the role it plays with an organization is
  an attribute of `relationship://`, not a separate identity.
- **Scheme + path:** `scheme://namespace/instance`. Path segments disambiguate and
  reify types (e.g. `asset://good/:id` vs `asset://money/:id`).
- **Collision rule:** when one scheme could mean two classes (e.g. `policy://` =
  insurance policy vs compliance policy), the first path segment disambiguates and
  the scheme is declared generic (`policy://ins/…`, `policy://compliance/…`).
- **Round-trip:** unknown URIs and fields MUST be preserved on rewrite.
- **Resolver:** the fabric maps every URI to its concrete backend/residence at access
  time; a URI is a reference, never a moved or duplicated object.

### C1. Actor Identity  (all sectors — only these are identities)
```text
person://            natural person — the one canonical identity
org://               organization — kind is an attribute (for-profit/public/charity/cooperative)
agent://             AI agent — a first-class actor with identity + delegated authority
system://            non-AI system / appliance / infrastructure actor
relationship://      Actor↔Actor relationship (role-scoped; carries Trust)
legal_entity://      legal entity / subsidiary / jurisdiction-entity
```
Three kinds of URI, and they must not be conflated:
- **Identity** — `person://`, `org://`, `agent://`, `system://` (who the actor is).
- **Relationship** — `relationship://` (the durable bond; roles are attributes of it).
- **Domain object** — `claim://`, `contract://`, `invoice://`, `patient_record://`,
  `student_record://`, `policy://`, etc. (the things a relationship operates on).

### C2. Roles are attributes, not URIs  (replaces the earlier "People Roles" list)
```
relationship://abc  role=customer | employee | citizen | donor | volunteer |
                    member | supplier | patient | student | contractor | ...
```
A role is an attribute of a `relationship://` (per §3.2 context), never a separate
identity. `patient://`, `supplier://`, `contractor://`, `student://` etc. are removed
as identities. Where a role context carries its own durable **record**, the record is
a domain object, distinct from the person: `patient_record://` (≠ the person),
`student_record://`, `supplier_profile://`, `credit_profile://`. This keeps identity
universal and context relationship-specific without fragmenting the person.

### C3. Organization Structure
```
department://                   internal division
cost_center://                  spend-owner unit
brand://                        consumer-facing mark/entity
franchise://                    location-level branded unit (retail, food)
store:// / site:// / plant://   physical operating unit
storehouse:// / warehouse:// / facility://   physical capacity
```

### C4. Financial Ledger & Money  (all; esp. Financials)
```
gl://                           General Ledger account
acct://                         receivable / payable / customer / vendor account
money://                        monetary asset instance / balance (alias of asset://money)
txn://                          ledger transaction (posting to GL)
invoice://                      billing document
receipt://                      payment evidence
payment://                      money transfer event
budget:// / forecast://         planning ledger
rate://                         interest / fee / tax rate, price basis
```
*Financial-services specific:*
```
policy://ins/…                  insurance policy / coverage
claim://                        insurance claim
loan:// / mortgage://           credit instruments
portfolio:// / position://      holdings and market positions
risk:// score://                exposure and credit/underwriting metrics
```

### C5. Commercial Lifecycle  (retail, consumer, most sectors)
```
product:// / service:// / sku://    sellable items
catalog:// / offer://               sellable intent and terms
price://                            sales price record
order://  (sales order)             customer order intent
po://    (purchase order)           procurement commitment
case:// / ticket://                 service/support request
agreement:// / contract://          binding terms between parties
delivery:// / shipment://           fulfillment movement
```

### C6. Assets & Property  (all; cross-ref §4b)
```
asset://good/…      physical good (inventory, product, mro)
asset://money/…     financial asset (alias money://)
asset://right/…     entitlement: license, permit, option
asset://digital/…   deliverables, code, media, ip (copy ≠ transfer)
asset://capacity/…  availability of agent/human capability
property:// / building:// / lease://real-estate    holdings and occupancy
equipment:// / tool:// / machine://                 capital & operating equipment
```

### C7. Devices & Endpoints  (Technology, industrial, energy, healthcare, telecom, auto, logistics)
```
device://                       general endpoint or IoT object
endpoint://                     network endpoint
pos://                          point-of-sale terminal   atm://  bank terminal
sim:// / handset:// / line://   telecom subscriber device
meter://                        utility / usage meter   sensor://  telemetry probe
vehicle:// / fleet:// / truck:/// drone:// / robot://   mobile physical units
monitor:// / medical_device://  healthcare monitoring equipment
server:// / node://             compute infrastructure endpoint
```

### C8. Industrial & Operations  (energy, aerospace/defense, manufacturing, auto)
```
job:// / workorder://           discrete unit of work
project:// / program://         long-lived effort
part://                         component;  bom://  bill of materials
unit:// (serial)                individually serialized physical unit (aircraft, engine, vehicle)
lot:// / batch://               traceability grouping (food, pharma, chemicals)
shift:// / schedule://          labor/equipment rostering
```

### C9. Energy & Utilities
```
well:// / platform:// / rig://  production assets
field:// / lease:// / reservoir://   subsurface rights and inventory
load://                         grid demand   consumer://  grid user
delivery:// (ESS end)           gas/terminal delivery point
```

### C10. Healthcare & Pharma  (reference C2 patient)
```
provider://                     clinician or care facility
care://                         encounter / visit
rx://                           prescription   formulary://  covered-drug list
plan://                         health plan / coverage
clinical trial:// / lot://      pharma R&D and batch traceability
```

### C11. Telecom & Media
```
sub://  subscription   plan://  service offering   bundle://
content:// / media:// / stream://   media assets and channels
franchise:// (films)   audience:// / ad_inventory://   monetization
```

### C12. Logistics & Transport
```
route:// / leg:// / stop://       planned movement
container:// / pallet:// / parcel:// / package://   handling units
dock:// / gate:// / hub://       network facilities
manifest:// / bill_of_lading://  shipment documentation
```

### C13. Knowledge & Records  (from §4a, expanded)
```
doc://  mail://  db://  corr://  chat://  voice://  log://  report://
contract://  transcript://  spec://  ticket://  training://  audit://
```
Provenance + Trust apply to every knowledge object (see Section 4a).

### C14. Rights, IP & Regulation  (the Government / Authority interface)
```
ip://                    patent | trademark | copyright   royalty://  payment streams
license://               granted permission     permit:// / registration://  operational authority
regulation://            applicable rule        filing:// / return://  submitted obligation
tax://                   tax obligation/credit   compliance://  evidence of conformity
```

### C16. Ontology Primitives (from §3 — review incorporation)
```
purpose:// / mission:// / objective://         why an org exists; what it aims at
authority:// / permission:// / delegation://   who may decide, who delegated it (§3.4)
decision://                                    a recorded decision (§3.12)
rule:// / policy:// / procedure:// / constraint://   what is allowed (§3.6)
right://  obligation://                         participant rights/burdens (§3.5)
consent://  authorization://                  granted scope (§3.7)
expectation://                                 what success means (§3.11)
dispute://  evidence:// / adjudication://       contested outcomes (§3.13) and proofs
resource://                                    supercategory above asset/knowledge (§3.8)
value://  cost://   time://                     economic and temporal primitives (§3.9/3.10)
# §7J Business Operating Layer — the ONLY new first-class operational nouns (URI cap):
case://        unresolved business work until resolved (§7J.3)
goal://  metric://                             what we optimize toward, and the number that proves it (§7J.1)
task://  dependency://                         assigned-not-yet-done work; directional workflow link (§7J.4/7J.6)
```
`relationship://` (C1) is the anchor: purpose, authority, consent, expectation, and
rules all resolve onto the relationship whose behavior they constrain.

### C15. Example URIs Across Sectors
```
person://ph-0a1f2       relationship://r-7731 (role=customer)   gl://3401-revenue
device://sensor/well-14 acct://ar-albertsons  txn://tr-8890   claim://cl-5041
unit://airframe/UA784   bom://bom-a320        rx://rx-9912     policy://ins/h-22
contract://po-20144     invoice://inv-5561    shipment://sh-9    lot://chemed/77
```

**Catalog completeness [Level B]:** this catalog is derived from the §B survey and is
expected to grow with each new sector or organization type. The extension rule is
normative but additive: **new URI schemes MUST be added rather than reclassified** so
resolvers and round-tripping stay valid. Underspecified types fall back to the closest
generic (e.g. `device://`, `asset://`, `doc://`) until a reified type is justified.

---

## Appendix D — Ontology Verification: 20 Radically Different Interactions

Adopted from external review (ChatGPT, 2026-08-31). Before adding further technology,
the §3 ontology must describe every relationship *without special pleading*. Test the
primitives against these 20 interactions; each must resolve without bending the model:

```
buying a hamburger              buying a car                working for Walmart
filing taxes                    getting a driver's license  receiving unemployment
donating to a food bank         volunteering                going to a hospital
attending college               buying insurance            filing an insurance claim
hiring a contractor             supplying Boeing            getting arrested
appealing a government decision voting                      opening a bank account
an AI agent approving an invoice                            an AI agent negotiating a contract
```

**Acceptance rule:** if any interaction requires a special case or a distortion of the
ontology, the primitive set is not yet general — revise the ontology, not the test.
**Status:** RUN in v0.6 — see **Appendix E** (result: 18 native, 2 derived, 0 special
case). The test remains the gate before Sprint 1 (Section 8).

---

## Appendix E — Ontology Test: 20 Interactions, INSTANTIATED (v0.6)

Per external review: do not merely define the test — run it. Each interaction was
walked through the §3 primitives (Actors, Relationship, Context, Purpose, Intent,
Capability, Offer/Request, Authority, Rights, Obligations, Rules, Consent, Commitment,
Decision, Action, Exchange, Outcome, Evidence, Claim, Evaluation, Accountability,
Dispute, Trust) and labeled.

| # | Interaction | Actors | Backbone | Verdict |
|---|---|---|---|---|
| 1 | Buying a hamburger | Person↔Org | offer→consent→exchange | **native** |
| 2 | Buying a car | Person↔Org(+lender+state) | multi-relationship (compose) | **derived** |
| 3 | Working for Walmart | Person↔Org | durable employment; interaction/state split | **native** |
| 4 | Filing taxes | Person↔Gov | **imposed** obligation; return→evaluation→dispute | **native** |
| 5 | Getting a driver's license | Person↔Gov | authority grant (license://) | **native** |
| 6 | Receiving unemployment | Person↔Gov | rights+obligations; benefit relation | **native** |
| 7 | Donating to a food bank | Person↔Charity | purpose-based org; resource transfer | **native** |
| 8 | Volunteering | Person↔Charity | labor/time as **Resource** (not asset) | **native** |
| 9 | Going to a hospital | Person↔Provider | **consent**, **disclosure** (PHI), claim | **native** |
| 10 | Attending college | Person↔Org | enrollment relation; tuition exchange | **native** |
| 11 | Buying insurance | Person↔Insurer | policy (right); premium exchange | **native** |
| 12 | Filing an insurance claim | Person↔Insurer | **claim→evidence→evaluation→dispute** | **native** |
| 13 | Hiring a contractor | Person↔Person(contractor) | Org↔Person contract | **native** |
| 14 | Supplying Boeing | **Org↔Org** | now first-class (Actor↔Actor) | **native** |
| 15 | Getting arrested | Person↔Gov | coercion via imposed obligation+authority+rights | **native** |
| 16 | Appealing a gov decision | Person↔Gov | **dispute→evidence→adjudication** | **native** |
| 17 | Voting | Person↔Gov(System) | identity+authn+**private action** (non-disclosure) | **derived** |
| 18 | Opening a bank account | Person↔Bank | KYC identity, consent, compliance | **native** |
| 19 | AI agent approving invoice | **Agent↔Org** | **delegation→decision→accountability** | **native** |
| 20 | AI agent negotiating contract | **Agent↔Org/Agent** | **negotiation→counteroffer→commitment** | **native** |

**Result: 18 native, 2 derived, 0 require a special case** under the v0.6 ontology.
The two derived cases delimit, not violate:
- **Buying a car** — decomposes into multiple Actor↔Actor relationships (buyer–dealer,
  borrower–lender, owner–registrar) composing one deal; a first-class multi-tier
  deal type is a future refinement, not currently a distortion.
- **Voting** — secret ballot means the Action must carry a strict *non-disclosure*
  constraint (the opposite of the usual evidence-rich action). Covered by §3.19
  Disclosure/purpose-limitation, but flagged as the handler's responsibility.

**What the test proves:** the Actor↔Actor upgrade (#14), the enforced Obligation/
Commitment distinction (#4), Consent+Disclosure (#9), Claim/Evidence (#12, #16),
Delegation/Decision (#19), and Negotiation (#20) — all v0.6 changes — are exactly the
primitives that turn formerly-awkward cases native. The ontology now describes all 20
interactions without bending. Gate passed for this corpus; the formal schema (Sprint 0)
must restore these 20 as executable fixtures, not prose.

---

## Appendix F — Starter Schema (core ontology objects, YAML)

Answers the "no machine-checkable definitions" gap (Grok §1). Sprint 0 will expand
this into the normative schema; this is the seed others can already build against.
> **v0.17 note:** the normative schema is now shipped and supersedes this seed — every
> §3 primitive + §7J/§7K object is machine-validatable in
> `schema/relational-os.schema.yaml` (with `.json` build and a
> passing conformance validator + fixtures). This appendix remains the human-readable seed;
> the machine contract is the artifact.

```yaml
# RelationalOS starter schema — v0.7 draft (informative, non-normative until Sprint 0)
defaults:
  on_new: preserve_unknown        # round-tripping: unknown fields MUST survive rewrite
  rfcs_3339: true

Actor:
  uri: person:// | org:// | agent:// | system://     # canonical identity types
  type: enum(PERSON, ORG, AGENT, SYSTEM)
  identity: { authenticators: [], attestations: [] }

Relationship:
  uri: relationship://
  participants: [ Actor* ]                 # any actors; role-carrier per §3.2
  roles: map(actor -> [role*])
  context: { org, role, jurisdiction, time, purpose, rules[] }
  purpose: string
  rights: right://*    obligations: obligation://*   authority: authority://*
  consent: consent://* rules: rule://*
  expectations: expectation://*  commitments: commitment://*
  status: enum(PROPOSED, ACTIVE, SUSPENDED, TERMINATED, ARCHIVED)
  timestamps: { created_at, effective_from, expires_at }

Interaction:                 # a discrete episode within a relationship
  uri: interaction://
  of: relationship://
  kind: enum(OFFER, REQUEST, DECISION, ACTION, EXCHANGE, OUTCOME, NEGOTIATION)
  events: [ Event* ]

Event:                       # atomic record — the ledger entry
  uri: event://
  type: enum(ACTION, DECISION, EXCHANGE, OUTCOME, STATE_CHANGE, EXTERNAL)
  actor: Actor?              # absent for EXTERNAL
  ledger_ref: txn://
  signature: string          # signed by responsible service (§2)

Expectation:
  uri: expectation://
  actor: Actor?   subject: string   condition: string
  metric: string? threshold: number? deadline: datetime? evidence_required: enum(CLEAR, SOME, NONE)

Claim:
  uri: claim://
  proposer: Actor   statement: string    evidence: [ evidence://* ]

Evidence:
  uri: evidence://
  kind: enum(OBSERVATION, TESTIMONY, RECORD, ANCHORED)   # anchored = confidential compute
  source: provenance_ref   verity: { procedure: string, confidence: float }

Decision:
  uri: decision://
  by: Actor   authority: authority://  alternatives: [*]  rules_applied: [ rule://* ]
  confidence: float?  expected_outcome: string?  actual_outcome: string?

Delegation:
  uri: delegation://
  grantor: Actor   grantee: Actor   scope: rule://*   expiry: datetime?
  status: enum(ACTIVE, REVOKED, EXPIRED)

Consent:
  uri: consent://
  granted_by: Actor   granted_for: purpose   scope: rule://*
  duration: { effective, expires }   revocable: bool   evidence: evidence://*

Dispute:
  uri: dispute://
  about: outcome://|claim://   parties: [ Actor* ]   status: enum(OPEN, ADJUDICATED, RESOLVED)
  evidence: [ evidence://* ]

# §7J Business Operating Layer
Case:                       # universal unit of unresolved business work
  uri: case://
  subject: string           # complaint, claim, grievance, supplier failure, incident, matter…
  actors: [ Actor* ]   claims: [ claim://* ]   events: [ event://* ]   tasks: [ task://* ]
  decisions: [ decision://* ]  commitments: [ commitment://* ]  deadlines: [ deadline* ]
  status: enum(OPEN, TRIAGE, ASSIGNED, IN_PROGRESS, BLOCKED, RESOLVED, CLOSED)  # +REOPEN

Goal:
  uri: goal://
  for: org://   parent: goal://?  statement: string  horizon: string
  metrics: [ metric://* ]

Metric:
  uri: metric://
  name: string  definition: string  unit: string  formula: string
  dimensions: [*]  target: number  threshold: number  period: string
  source: string  owner: Actor   actual: number?  variance: number?

Task:
  uri: task://
  assigned_to: Actor   created_by: Actor   objective: string
  dependencies: [ dependency://* ]   authority: authority://
  deadline: datetime?   priority: number   status: enum(INCOMING, ASSIGNED, IN_PROGRESS,
      BLOCKED, AWAITING_HUMAN, AWAITING_EXTERNAL, COMPLETED, FAILED)
  expected_outcome: string?  actual_outcome: string?

Dependency:
  uri: dependency://
  from: task://|step   to: task://|step   kind: enum(REQUIRES, BLOCKS, ENABLES, DERIVED_FROM, IMPACTS)
```

**Conventions enforced here:** identity ≠ role (roles are attributes); Ledger=history,
Graph=state (§3.16); every actor-action has a signature; consent/authority are scoped,
expiry-bound, and revocable (§7B); URI schemes match Appendix C with
identity/relationship/domain-object separation (C1/C2).

---

## Appendix G — Implementation Guide: Tools, Frameworks, Libraries (informative)

Era-specific (tools will age; the §3 ontology and §7D contracts are the timeless
part). This is a recommended reference stack for scalable, redundant, supportable,
professional build-out. Mark all of it LEVEL B (engineering estimate) unless marked
normative.

### G.0 Guiding principles
1. **Boring, supportable tech over clever tech.** Every choice prefers a large hiring
   pool, strong docs, and commercial support over novelty. When in doubt, pick the
   mainstream option.
2. **Redundancy is a per-layer property, not a single bolt-on.** Chosen below per layer.
3. **Contracts first.** Service interfaces are Protobuf/gRPC with the Appendix F schema
   as the single source of truth; no ad-hoc wire format.
4. **Durability lives in the ledger, scale lives in the graph, speed lives in cache.**

### G.1 Languages & runtimes
| Layer | Primary | Notes |
|---|---|---|
| Core services (S1–S5, substrate) | **Go** | concurrency, fast, trivial ops, huge hiring pool; generates one static binary |
| Agent fleet / AI glue | **Python** | model routing, evals, LangGraph, data-heavy code |
| Performance-critical hot path | **Rust** | optional, for the Trust/evidence verifier and ledger hash-chaining |
| Schema/API surface | **Protobuf (protovalidate)** | contract boundary; codegen to Go+Python |

**Rationale:** Go for the event-sourced platform core gives easy horizontal scale,
low memory, and simple on-call debugging. Python is where the LLM ecosystem lives.
Rust only where cold, provable speed matters — not as the default.

### G.2 Service architecture & contracts
- **Transport:** gRPC + TLS for service-to-service; OpenAPI/REST (generated from the
  same Protobuf) for external-facing; optional GraphQL gateway if clients demand it.
- **Contract boundary:** Protobuf messages mirror Appendix F exactly; breaking changes
  require a new version and a migration (per §3.19 versioning).
- **Service mesh** is optional early; start lean (no mesh), adopt later for mTLS and
  canary if fleet grows.

### G.3 Data layer (+ redundancy + support)
| Duty | Primary | Alternatives | Redundancy/support note |
|---|---|---|---|
| Relationship Graph (state) | **Neo4j** | TigerGraph, Amazon Neptune | causal clustering; single multi-active graph; strong docs/community |
| Append-only Ledger (history) | **Kafka** (log) + **PostgreSQL** (queryable projection) | Redpanda; NATS JetStream; QLDB (AWS-only) | Kafka replicated log = durable, redundant event history; Postgres is the supportable query layer and audit market standard |
| Content addressing | **SHA-256 / hash-chained (Merkle-style)** over ledger entries | — | optional non-repudiation per §7C decision |
| Knowledge search | **OpenSearch** | Elasticsearch | mature, replicated shards, huge support base |
| Vector index | **pgvector** (Postgres) → **Qdrant/Milvus** at scale | | start inside Postgres (one less system), split when size demands |
| Cache/hot state | **Redis** (or Valkey) | | sentinel/cluster for redundancy |
| Object store (knowledge/asset content refs) | **MinIO** (S3 API, self-host) | cloud object store | erasure coding = redundancy without exotic hardware |
| Distributed coordination | **etcd** or Consul | | leader election, service discovery |

**Supportability driver:** Postgres + Kafka + OpenSearch + Redis + MinIO are all
boring, well-documented, widely-hired technologies that run identically on-prem
(Tailscale/Raymond-style fleet), in VMs, or on major clouds.

### G.4 AI & agent layer
- **Model router (the §6 routing seam):** **LiteLLM** — one OpenAI-compatible gateway
  over local, private-cloud, and frontier models with routing, retries, and fallback.
  Directly realizes the "own vs rent" ladder.
- **Durable agent workflows:** **Temporal** — long-running, retry, saga/compensation,
  partial-failure recovery. This is what §7D-C (error handling, retries, compensation)
  demands and the column human escalation sit on.
- **Agent reasoning:** **LangGraph** for the reasoning/state graph on top of Temporal's
  durability (Temporal is the engine; LangGraph is the reasoning model).
- **Local inference:** **Ollama** (dev/desktop) and **vLLM** (self-hosted serving);
  cloud APIs as the frontier tier. Embeddings via pgvector + a local embedding model
  or API.
- **Evaluation harness:** LangSmith (or a custom harness storing results as Evidence
  objects in the ledger) — feed outcomes back into the Trust engine. (§7D-C.)
- **Fleet management:** containerized agents; capability discovery via the graph;
  sandboxing via container isolation; skills versioned like code (mirrors §3.19).

### G.5 Identity & security (per §7B, normative intent)
- **Authentication:** **OIDC/OAuth2** — Keycloak (self-host) or a managed IdP.
- **Authorization:** **OpenFGA** (Google-Zanzibar-style, relationship-based access
  control). Strong fit: the model IS relationships, so `authz` reads relationship
  tuples directly — capability-based and consistent with §3.4/§7B.
- **Secrets:** **HashiCorp Vault** (or SOPS+age for lighter footprint).
- **Signing/keys:** Vault transit or a cloud KMS/HSM; evidence anchoring in a **TEE**
  (SGX/SEV) via an attestation service when available — flagged in §7B as a
  dependency, not a given.
- **Regulated data:** per-context jurisdiction tagging + policies enforced through
  OpenFGA; disclosure-linkage (same-person across contexts) is a logged, audited,
  consented act (§3.19/§7B).

### G.6 Observability & reliability (ease of support)
- **Stack:** OpenTelemetry (traces+metrics) → Prometheus → Grafana; **Loki** for logs.
- **Logging:** structured JSON, correlation IDs propagated across services via trace
  context; every Event carries its `event://` URI in the log for replay (§3.16).
- **SLOs/error budgets;** runbook-first; **reproducible local dev** (docker-compose
  single-node analog so the whole chain runs on a laptop for debugging).
- **Chaos/recovery drills** for the substrate (§7C; no control-ship collapse).

### G.7 Delivery & operations
- **Containers + images:** Docker; images scanned (Trivy).
- **Orchestration:** **Kubernetes** for scale; **k3s/Nomad** for small/edge/on-prem
  footprints (fits the home-fleet / air-gapped model). Accept both — the schema and
  contracts must not couple to either.
- **Provisioning/IaC:** Terraform; **Helm** (or kustomize) for K8s.
- **GitOps/CI:** Git + GitHub Actions/GitLab CI; **ArgoCD** (K8s). Branch-protected;
  the Appendix F schema change is a reviewed PR that makes breaking versions explicit.
- **Deployment models:** SaaS, hybrid, and on-prem/air-gapped all supported from one
  codebase; data-residency and multi-region via Postgres logical replication + Kafka
  mirroring + GeoDNS.

### G.8 Multi-region / data-residency
- Kafka cross-region mirroring, Postgres logical replication, OpenSearch cross-cluster.
- Jurisdiction-aware routing: regulated data stays in the region that law requires
  (per §7B), enforced by the routing seam + OpenFGA policies.
- This is the *deployment* answer to §10.Q4 (multi-org sharing) pending the Sprint-0
  ledger decision (§7C).

### G.9 Testing & quality
- **Property-based testing:** Hypothesis (Python), rapid (Go) on the ontology invariants.
- **Contract testing:** Pact across service boundaries.
- **Adversarial Trust tests:** collusion, gaming, contradictory/biased evidence (§7D-B).
- **End-to-end:** the 20 Appendix E interactions as observable fixtures in CI.
- **Conformance validator (Sprint 0):** the `jsonschema` library ships NO RFC 3339 /
  `date-time` checker, so the conformance validator itself enforces §2 timestamps (see
  Sprint-0 findings F1). The Sprint-0 validator + fixtures are the gate to re-run in CI.
- **Mutation/quality gates:** ruff (Python), go vet/staticcheck (Go).

### G.10 Licensing & what to avoid
- Prefer Apache-2.0/MIT/BSL-with-kill-switch for the core; avoid viral-copyleft in
  distributed binaries; review each dependency's license before production.
- **Avoid:** building proprietary model training (non-goal), hand-rolling a ledger
  (use Kafka+Postgres), DIY identity (use OIDC), a custom vector DB too early.

### G.11 Footguns
- **Schema drift:** the Appendix F schema, Protobuf, and OpenAPI must be generated from
  ONE source; manual duplication rots fast.
- **Graph/Ledger conflation:** §3.16 is normative — do not let services read the graph
  as history or the ledger as state.
- **The droid-army SPOF** (§7A-2): the substrate (graph/ledger/bus) must be redundant
  before any agent ships; a single shared store that dies takes the whole chain down.
- **Trust as math too early:** the §5 equation is interface/algo (§3.14) — do not hardcode
  weights before the evidence/incentive research (§7D-B).

### G.12 Client layer (PC / tablet / phone)
- **Runtime:** **Flutter** (single Dart codebase → Android, iOS, Windows, macOS, Linux,
  Web/PWA). See §7E.2 for the OS matrix.
- **Offline/sync engine:** local durable store (**Drift**/SQLite on-device) as the
  event queue; idempotent replay against the ledger (§7E.3/§3.16). Prefer
  SQLite-family so the client stays an embedded, disposable cache.
- **Auth:** OIDC client (authorization_code + PKCE) → Keycloak/managed IdP (§G.5).
- **Local inference:** onnxruntime / MLKit / Ollama for the on-device tier; connect to
  hub (LiteLLM local/private-cloud) or cloud (frontier) for offload (§6 seam).
- **Responsive UI:** Flutter adaptive layout (dashboard / split-view / stacked-drawer);
  no per-form-factor apps.
- **Security:** keychain/keystore/TPM storage, local data-at-rest encryption, cert
  pinning, device-trust-level in authz (§7E.4, §7B).
- **Update:** OTA via stores + PWA; client schema-versioned per §3.19 (stale client =
  upgrade, never corrupt).

### G.13 IoT channel tooling
- **Broker:** **EMQX** or **Mosquitto** (MQTT); CoAP gateway for constrained devices;
  MQTT-over-TLS into a gateway that signs Events into the Kafka ledger (§7E.4).
- **Device SDKs:** lightweight MQTT clients per embedded target; per-device identity
  via short-lived tokens, not shared secrets; attestation feed into OpenFGA authz (§G.5).
- **Fleet/DM:** device-management + staged firmware OTA; devices versioned like software
  (§3.19); a device is a `device://` actor, not a customer UI (§7E.4).

### G.14 Audit layer tooling
- **Integrity/data-quality:** **Great Expectations** or **dbt test** for the §7F check
  classes (referential integrity, schema conformance, missing records) over ledger/
  graph projections.
- **Policy/authority conformance:** **Open Policy Agent (OPA/Rego)** for authority,
  delegation, consent, and disclosure-gate rules (§3.4/§3.7 — complements OpenFGA in G.5).
- **Scheduling:** **Prefect** or **Airflow** for the scheduled sweeps; continuous scans
  as a streaming consumer on the event bus.
- **Output:** findings written as signed `audit_finding://` events to the ledger,
  feeding the remediation queue (§7F.2) and the §7G.6 audit-health report.

### G.15 BI layer tooling
- **Analytics store:** **ClickHouse** (or Postgres/Redshift/BigQuery) as the OLAP
  warehouse over ledger projections — separate from the live graph (separation per
  §7C/§7G.8).
- **Transforms:** **dbt** (SQL) — the three core statements and every catalog report are
  versioned dbt models, reviewable like code (§3.19).
- **Semantic layer:** dbt Semantic Layer or **Cube** so report definitions don't drift
  from the ontology.
- **BI render:** **Metabase** or **Apache Superset** (self-serve/web, fits the Flutter/
  PWA front ends) — or fall back on **Looker / Power BI / Tableau** where enterprises demand it.
- **Trust-weighted reporting:** any reputation report reads scoped Trust / evidence via
  SQL against the S5 projections — never a single global score (§3.14).

### G.16 External interfaces / gateway tooling
- **Gateway:** an API gateway (Kong/Traefik) + connector framework that normalizes each
  external exchange to ontology contracts (§7H.6); every original payload stored as
  Evidence in object store (MinIO) with a signed Event.
- **Format libs:** ISO 20022 / SWIFT (e.g., Prowide ISO in Java), NACHA (ACH),
  X12 EDI parsers, and XML/JSON/PDF adapters (§7H.6).
- **Provider/rail connectors:** bank treasury APIs & host-to-host (camt.053, MT940),
  ADP/UKG/Gusto/Paychex, Avalara/Vertex/Sovos/TaxJar, SEC EDGAR, IRS e-file vendors —
  all connectors, versioned like code (§3.19).
- **Compliance calendar:** a jurisdiction × form × deadline scheduler on Prefect/Airflow
  (extends §G.14) with human-loop escalation for missed-filing risk (§7F).
- **Secrets & keys:** provider credentials in Vault; per-provider signing/attestation
  (§G.5).

### G.17 Market & social intelligence tooling
- **Default resilient ingest set (Sprint-0 survey 1):** **GDELT 2.0** (open, free,
  hourly news+social-spike) + **SEC EDGAR** (free company/regulatory filings) +
  regulatory-wire **RSS** plus the business's own consent-gated/OAuth channels. Licensed
  news/social (Reuters/AP, X, LinkedIn, TikTok, Reddit, Glassdoor) is a **Phase-B tier**:
  most have no free commercial API (X is pay-per-use ~$0.005/read with no new free tier;
  LinkedIn prohibits scraping; TikTok Research is academic-only; Reddit is enterprise/
  opaque; review platforms via paid aggregator/licensing). Respect API limits and
  platform terms. GDELT is the cost floor and the emergency fallback provider.
- **Data-boundary default (survey 4):** ingest aggregates/de-identified counts; treat
  employee-platform data as sensitive employee data; never infer protected classes
  (GDPR Art 9 / EEOC); coupling review scores to an identifiable person requires a
  purpose-limited DPIA + Consent (CPRA employee exemptions expired 2023-01-01).
- **Extraction/analysis:** entity + topic NER (spaCy) and LLM-based extraction;
  sentiment scoring (LLM or model) with stated confidence (§7I.4); anomaly/spike detection
  vs rolling baseline (stats/ML).
- **Action derivation:** LLM + policy rules (OPA/Rego, §G.14) produce **recommended
  actions**, gated by Authority/Delegation and the §3.19 human floor — never
  auto-executed for irreversible actions.
- **Pipeline:** Prefect/Airflow (extends §G.14) for continuous ingestion + trend
  baselines; results land as Evidence/Claims in the ledger (Object store: MinIO).
- **Opt-in privacy:** employee/social data only under Consent/Disclosure (§3.19);
  regulated-data jurisdiction tags per §7B.

---

## Version / Review Log

- **v0.1** — initial specification (service chain, integration loop, ROI, roadmap).
- **v0.2** — Knowledge Fabric (§4a): where knowledge lives.
- **v0.3** — Asset Ledger (§4b): where assets live; Knowledge/Asset distinction.
- **v0.4** — Appendix B (top-100 survey) and Appendix C (URI address space).
- **v0.5** — Fundamental Ontology (§3) per external review: Purpose, Context, Authority/
  Governance/Delegation, Rights/Obligations, Rules, Consent, Resource, Value/Cost/Price,
  Time, Expectation, Decision, Dispute, scoped Trust vs Reputation; ontology-first
  service framing; C16 URI schemes; Appendix D ontology test.
- **v0.6** — Second external review (ChatGPT, 2026-08-31): Actor↔Actor as the universal
  primitive; Relationship·Interaction·Event·State backbone (§3.16) with a formal
  Relationship model and Ledger=history/Graph=state; Claim + epistemic levels (§3.17);
  Incentive/Interest/Conflict/Negotiation (§3.18); cross-cutting substrate, versioning,
  identity≠authn≠authz, and Disclosure (§3.19); Obligation/Commitment logic corrected;
  private≠for-profit; trust equation demoted to interface/algo; Knowledge=Information·
  Truth and the Asset↔Resource reframe; URI simplification (roles as attributes, not
  URIs); Appendix E = the 20-interaction test RUN (18 native / 2 derived / 0 special).
- **v0.7** — Third external review (Grok, 2026-08-31): implementation-readiness layer.
  §7B Security/Privacy/Compliance (normative: threat model, capability-based authz,
  disclosure gate, regulated data, confidential-compute dependencies); §7C Shared
  Graph+Ledger implementation model (open decisions); §7D Sprint-0 committed scope
  (contracts, Trust closure w/ §10 Q1–4 owners, operations/product as Phase B,
  explicit non-goals); Appendix F starter YAML schema.
- **v0.8** — Appendix G Implementation Guide (informative, era-specific): languages
  (Go core / Python AI / Rust hot path), Protobuf+gRPC contracts, data layer
  (Neo4j graph, Kafka+Postgres ledger, OpenSearch, pgvector, Redis, MinIO), AI layer
  (LiteLLM router, Temporal durable workflows, LangGraph, Ollama/vLLM, LangSmith),
  security (OIDC/Keycloak, OpenFGA relationship-based authz, Vault, TEE), observability
  (OTel/Prometheus/Grafana/Loki), delivery (Docker, K8s + k3s/Nomad, Terraform, Helm,
  ArgoCD, GitOps), multi-region/json-residency, testing, license policy, footguns.
- **v0.9** — §7E Device & Client Layer (PC/tablet/phone): client-not-substrate model,
  single cross-platform runtime (Flutter → Android/iOS/Windows/macOS/Linux/Web-PWA),
  offline-first sync, local compute tier + home-hub/cloud offload, device security &
  attestation, responsive UI, non-goals; Appendix G.12 client tooling.
- **v0.10** — §7E reframed per user clarity as an explicit **Backend/Frontend split**:
  back end = the platform (unchanged by form factor); front end = thin customer
  interfaces on PC/tablet/phone + Web/PWA (Flutter); distinct **IoT channel** for
  headless device producers/actuators (MQTT/CoAP gateway → ledger, per-device
  identity/attestation, firmware OTA, non-goal: IoT ≠ customer UI). Appendix G.13 IoT
  tooling.
- **v0.11** — **§7F Audit Layer**: continuous integrity review of all entities
  (referential integrity, ledger↔graph agreement, schema conformance, missing records,
  Trust setup, authority/delegation completeness, evidence health, versioning,
  security/compliance, timing anomalies); findings as first-class signed ledger Events
  (audit_finding://) feeding a remediation queue. **§7G BI Layer**: standard business
  reports catalog (three statements + budget/segment/cash, customer, operations,
  workforce, supplier, RelationalOS-native Trust/evidence/dispute/audit-health, compliance)
  over an analytics warehouse, survey-grounded (2026). Appendix G.14 audit tooling
  (Great Expectations/dbt test, OPA, Prefect/Airflow) and G.15 BI tooling
  (ClickHouse/dbt/Cube + Metabase/Superset or Looker/PowerBI/Tableau).
- **v0.12** — **§7H External Interfaces & Regulatory / Payroll / Tax Reporting**:
  gateway layer normalizing every external exchange to ontology + Evidence in ledger.
  Treasury/payment rails (SWIFT/ISO 20022, Fedwire, CHIPS, T2/CHAPS, ACH/NACHA, SEPA,
  FedNow/RTP, cards, bank APIs); payroll/HR (ADP/Paychex/Gusto/UKG, W-2/1099/ACA/EEO-1,
  SUTA); tax three tiers (federal IRS forms incl 941/944/940/720/1095, state incl
  PTET/sales-us/nexus, local business-license/B&O/occupancy), tax connectors (Avalara/
  Vertex/Sovos); regulatory (SEC EDGAR, FINRA, NAIC/SERFF, HIPAA X12, FERC/OSHA/EPA,
  DOT/FAA/FCC); government/grants. Mechanics: filing calendar, format adapters, e-file
  receipts as Evidence, idempotency/dead-letter. Appendix G.16 gateway tooling.
- **v0.13** — **§7I Market & Social Intelligence**: ingest Reuters/news + social media
  + review/employee platforms as Claims-with-provenance (EXTERNAL events in §3.16);
  entity extraction, signal typing, sentiment/trend with baseline anomaly detection;
  **recommended actions** for market / customer-reputation / employee-reputation /
  regulatory-triggers, gated by Authority and the human-escalation floor — never
  auto-executed for irreversible actions; cross-verification discipline (§3.17); feeds
  §7F audit and §7G sentiment/trend reports. Appendix G.17 tooling (news APIs, GDELT,
  NER/sentiment, OPA-gated action derivation, Prefect, opt-in privacy).
- **v0.14** — Surveys added as **explicit gating Sprint-0 deliverables** with written
  reports and Definitions of Done: (1) §7I data-source & licensing survey; (2) §7H
  jurisdiction & tax-filing survey; (3) §7G BI report-catalog validation; (4) §7I
  employee/customer data boundary review. Registered in §7D-E and §8 Sprint 0.
- **v0.15** — Fourth external review (ChatGPT, 2026-08-31): **stop expanding the
  ontology; build the Business Operating Layer.** Architecturally reframed
  Substrate + Services + Business Operating Layer (§7J). Spec'd the red-priority core
    in full: Goals/Metrics/Targets (strategic chain, Metric object, variance→action AI
    loop), Exception Management (the "seven things today" heartbeat), Case (universal
    unit of unresolved work — the product bridge), Task & Work Queue (human = supervisor),
    Priority/Attention (derive, don't overload), Dependency & Impact (impact analysis).
    Registered (not expanded): Risk, Capacity/Allocation, SLA-as-assembly, the Cockpit,
    and a ranked Phase-B beyond-backlog (process mining, change detection, scenario,
    decision learning, organizational memory, universal query, benchmarking). **URI cap
    imposed** (case/goal/metric/task/dependency only). Appendix F + Sprint 5
    (Business Operating Layer) + §7D-F added.
- **v0.16** — Fifth external review (ChatGPT): STOP adding concepts. Added a SHORT
  **§7K Business Operating Semantics** (four-layer architecture — Ontology / Substrate /
  Operating System / Business Intelligence; Process+ProcessInstance, Policy execution,
  Forecast, Ownership, Escalation, Approval, Acknowledgement, Causation/Correlation/
  Idempotency, Entity resolution, Business Model, Trade-off analysis, Organizational
  Learning; elevated Risk, Capacity/Allocation, Cost of Delay, Uncertainty, root-cause
  epistemic status, org-structure-as-graph, authority≠responsibility, two observability
  layers, process-mining/decision-learning/memory). URI cap upheld (no new nouns).
  **§7L Business Indispensability Test** — the ten morning questions. **§8 split into
  platform vs customer-value build tracks with an early Case-led MVP** (review #23).
  **Thesis strengthened** (review #24/25): the moat is the verified history of decisions
  and outcomes attached to relationships, compounded by Learning.
- **v0.17** — **Sprint 0 (implementation contract) build findings.** Shipped a normative,
  machine-validatable JSON Schema (all §3 primitives + §7J operating objects + §7K
  structural semantics + Appendix C URI-conventions) with a Python conformance validator
  and executable fixtures (20 Appendix E interactions, the §7L loop, the Case lifecycle),
  all passing. **Spec updated from genuine survey/build findings only:** §7I.6 data
  boundary sharpened (aggregates-only default; GDPR Art 9 / EEOC protected-class ban;
  CPRA employee exemptions expired; DPIA+Consent for coupling) — from survey 4; §7G.8
  statutory core reference-grounded (ASC 205/210/220/230 + Reg S-X Art 3) — from survey
  3; §7H.6 seeded filing calendar (federal + NM + ABQ) — from survey 2; Appendix G.17
  default resilient ingest set (GDELT + SEC EDGAR + RSS; licensed news/social deferred to
  Phase-B) — from survey 1. URI cap and frozen ontology unchanged (no new nouns). The
  four gating surveys (§8) are DONE with cited DoDs in `archive/sprints/sprint-0/artifacts/surveys/`.
- **v0.18** — **Sprint 1 (S1 substrate + S2 Intent/Matching) build findings.** Built and
  VERIFIED the S1→S2 loop on the shared Ledger + Graph for one role (customer) and one
  domain (Quoteko quoting/triage): a runnable Python service implementing
  `resolve_identity/authenticate/authorize/resolve_role` (S1, thin substrate) and
  `infer_intent/match_offers` (S2, Trust-weighted per §5) with a human verification
  floor (§6/§7B) engaged before an irreversible hire is committed. Each step is a
  signed, content-addressed Ledger event; current state lands on the Graph; a
  round-trip check rebuilds the Graph from the Ledger with no history/state conflation
  (§3.16). **New self-authored S1 check passes** (authz per relationship; delegation
  honored; revocation voids capability) and **Sprint-0 conformance still exits 0** over
  both the original 156 fixtures and the new 28 Sprint-1 instances. **URI cap and
  frozen ontology respected** — no new nouns or URI schemes; the schema artifacts stay
  v0.17, unchanged. Genuine finding F6 added a single normative clarification to §3.4
  (delegation/consent `scope` = URI refs to `rule://`/`permission://`, never bare
  strings; revocation voids the capability). Artifacts under
  `archive/sprints/sprint-1/artifacts/`; findings under `archive/sprints/sprint-1/notes/findings.md`.
- **v0.19** — **Sprint 2 (Trust engine minimum) build findings.** Built and VERIFIED
  the S5 loop on the Sprint-1 Quoteko scene: `capture(outcome, provenance)→evidence://`,
  `verify(evidence, statement)→{claim, degree, procedure}` per §3.17,
  `make_expectation→expectation://`, and `update(Trust, evidence, weight, recency)→
  trust://` per the §5 scoped/bounded equation, keyed `(subject, target, claim,
  context)` per §3.14. One crisp objective outcome class ("roofing job completed by
  its committed deadline", anchored completion record) exercised both signs of the
  flywheel: a verified good outcome raised one provider 0.61→0.708 and a verified bad
  outcome lowered another 0.92→0.528, while a third provider (different claim) stayed
  at 0.42 — proof of scope, not a global score. S2 `match_offers` re-ranks under the
  updated Trust (same fit → rank decided by Trust), the §5 flywheel. New self-authored
  S5 + flywheel checks pass; **Sprint-0 conformance still exits 0** over all three
  fixture generations (Sprint-0 156, Sprint-1 28, Sprint-2 35). **URI cap and frozen
  ontology respected** — no new nouns or URI schemes; schema artifacts unchanged.
  Genuine finding F3 added a single normative clarification to §5 (persisted `trust://`
  carries its update inputs as additive envelope fields for auditability;
  `Trust.evidence` is an array). Artifacts under `archive/sprints/sprint-2/artifacts/`;
  findings under `archive/sprints/sprint-2/notes/findings.md`.
- **v0.20** — **Sprint 3 (Orchestration S3 + human floor) build findings.** Built and
  VERIFIED the S3 Orchestration & Execution service on the Sprint-2 Quoteko state:
  `commit(offer, terms, authority)→commitment://` (§5 `commitment=agree(offer, terms)`),
  `orchestrate(commitment, fleet, trust_scores)→[Task]` (the split recorded as a signed
  `decision://`), the §6 `route_seam(task, trust)→{local, private-cloud, frontier}`
  (Trust-weighted, deterministic, no speculative weights per §G.11), and per-worker
  `execute_task` as a capability-gated (delegation-bounded, §3.4/§7B) signed ACTION
  `event://`. Demonstrated the **human-escalation floor** both ways on one relationship:
  a cheap reversible micro-action auto-executed by a worker (full autonomy where
  failure is cheap), and an **irreversible** `release_final_payment` (cost `unknowable`)
  that escalated to `person://qk/approver`, whose signed human DECISION enumerated four
  alternatives and committed it — the irreversible ACTION ran only after that
  acknowledgement, and the Ledger recorded the escalation. Chained the FULL §5 loop on
  one relationship: S1 identity/role → S2 intent/match → S3 commit + fleet execute →
  2nd S5 capture/update on the S3-executed OUTCOME (solarworks Trust 0.708→0.806) → S2
  re-ranks the NEXT cycle (solarworks #1) — the flywheel, closed. New self-authored S3 +
  escalate + loop checks pass; **Sprint-0 conformance still exits 0** over all FOUR
  fixture generations (Sprint-0 156, Sprint-1 28, Sprint-2 35, Sprint-3 55). **URI cap
  and frozen ontology respected** — no new nouns or URI schemes; schema artifacts
  unchanged. Two genuine, additive normative clarifications added to **§6** (F2: the
  floor overrides the seam tier, with the capability `seam_tier` and the governing
  executable `tier` kept distinct for audit; F4: escalation compliance is auditable
  from the signed append-only Ledger event ORDER — the irreversible ACTION must follow
  the approver's signed DECISION). Artifacts under `archive/sprints/sprint-3/artifacts/`;
  findings under `archive/sprints/sprint-3/notes/findings.md`.
- **v0.21** — **Sprint 4 (Exchange & Settlement S4 + multi-role / multi-org extension)
  build findings.** Built and VERIFIED Settlement on the Sprint-3 loop end-state and extended
  the chain from customer to employee roles and from private to charitable orgs. `settle()`
  records the exchange per §4b as an `event://` type EXCHANGE carrying the Asset-Ledger
  title/custody delta (`asset://`), with the payment `obligation://`, `receipt://`, and
  reconciliation `decision://` riding that SAME signed EXCHANGE event's state; `evaluate()`
  emits an `event://` OUTCOME (met|partial|failed) that S5 captures to update scoped Trust,
  re-ranks S2 — the §5 loop closes WITH settlement in the middle (solarworks Trust
  0.806→0.904). **Multi-role** on ONE relationship (§3.2/§C2): the same actor is customer AND
  employee on `relationship://qk/cust-cxn`, with role-scoped authority
  (`authority_by_role`) and role-scoped Trust keyed `context = relationship://…?role=employee`
  (a query param on the SAME scheme — not a new identity/scheme); the employee-role Trust
  rises 0.5→0.598 while the customer-role Trust stays untouched. **Multi-org** across the §3.1
  org-kind attribute: private for-profit `org://quoteko` (FOR_PROFIT) engages charitable
  `org://qk/sunsetshelter` (NONPROFIT_CHARITABLE) with a purpose-constrained pro-bono offer,
  full S1→S5 loop, and the IRREVERSIBLE charitable-grant settlement gated by the §6 human
  floor — proven from Ledger ORDER (`split@52 < esc@55 < hum@56 < release@57`). All checks
  exit 0; **Sprint-0 conformance still exits 0** over all FIVE fixture generations
  (Sprint-0 156, Sprint-1 28, Sprint-2 35, Sprint-3 55, Sprint-4 174). **URI cap and frozen
  ontology respected** — no new nouns or URI schemes; the schema artifacts stay unchanged
  (49 `$defs`, validator unmodified). Three genuine additive normative clarifications: §4 S4
  (settlement artifacts ride the signed EXCHANGE event's embedded state — F2), §3.2
  (role-qualified context is a query param on the same relationship scheme — F3), §3.14
  (distinct role-scoped Trust values coexist on the same relationship). Artifacts under
  `archive/sprints/sprint-4/artifacts/`; findings under `archive/sprints/sprint-4/notes/findings.md`.
- **v0.22** — **Sprint 5 (Business Operating Layer — the product) build findings.** Built and
  VERIFIED the operating layer on the Sprint-4 S1→S5 state for Quoteko: a Case-led loop
  (`case://` OPEN→TRIAGE→ASSIGNED→IN_PROGRESS→BLOCKED→RESOLVED→CLOSED with signed evidence per
  transition), the §7J.2 Exception heartbeat (on-time delivery 0.833 < target 0.95 → CRITICAL,
  root SUPPORTED per §7K.2), Goals/Metrics (**Goal→Metric→Actual→Variance→Decision→Action→
  Outcome**, ledger-projected actuals), Priority = f(impact, urgency, confidence,
  irreversibility, relationship-importance, cost-of-delay) with priority-ordered attention,
  Dependencies (`requires/blocks/enables/derived_from/impacts`) with a transitive impact
  analysis over the exception→case→task chain, and the **Cockpit** (§7J.9): business health,
  prioritized attention, and an AI recommendation carrying the authority it requires.
  **§7L answered with evidence:** #8 becomes assigned, authorized Task work
  (`task://` under `authority://`) that closed in a **verified outcome** (the re-allocated,
  rallied solarworks delivery settled and captured/verified on time; forward-period on-time
  1.0) and a **Learning** entry (§7K.1 Decision→Expected→Actual→Variance→WHY→change-future-
  policy) plus an updated `policy://` — #9 (owner + delegation-bounded authority + capacity)
  and #10 (verified outcome + learning) satisfied. The full S1→S5 chain stays intact: all
  re-used Sprint-1..4 checks pass unchanged on the full state (**97** ledger events → **160**
  graph objects rebuilt, full-state round-trip exit 0). **URI cap and frozen ontology held —
  the operating layer is a pure assembly:** zero schema/ontology/URI change; schema artifacts
  byte-identical (49 `$defs`); conformance still exits 0 over all SIX fixture generations
  (Sprint-0 156, Sprint-1 28, Sprint-2 35, Sprint-3 55, Sprint-4 174, Sprint-5 316). Exception/
  Priority/Recommendation and Q9 capacity are additive envelope fields (never new nouns).
  Four genuine additive normative clarifications: §3.16 (signed state deltas are immutable
  snapshots — deep-copied, so a mutating operating object can't retroactively break an earlier
  signing — F2), §7J.5/§C16 (derived values carried as additive fields; no `capacity://
  priority:// exception:// recommendation://` scheme; capacity is Q9's additive
  `assigned_capacity` — F1/F6), §8 Sprint 5 marked COMPLETE (S1→S5 chain done; §7L
  answerable for one company — F4). Artifacts under `archive/sprints/sprint-5/artifacts/`; findings
  under `archive/sprints/sprint-5/notes/findings.md`.
- **Gap-closure (post-review, v0.22):** added the §7D-A4 **EBNF lifecycle grammar**
  (`schema/relational-os-lifecycle.ebnf`) that the delivery
  audit flagged as the one outstanding literal contract item. No schema/ontology/URI
  change; the JSON Schema stays the normative type contract.
- **Post-close code hardening (v0.22, multi-sector dogfood):** provisioning instances for
  every sector family (SPEC Appendix B) surfaced a genuine build defect — the reference
  `ros/bol.py` / `ros/s4.py` / `ros/s5.py` services **hardcoded a construction org/path
  segment (`qk`)** in the URIs they build, which leaked into any non-construction instance.
  Fixed by **parameterizing a `label` segment** on `BolService` / `S4Service` /
  `S5Service` (default `'qk'` preserves the reference Quoteko build byte-for-byte — the
  Sprint-0..5 demo and all-six conformance re-verify ALL PASS). This is a **code-level
  hardening only — the frozen ontology and URI cap are unchanged** (no new nouns, no new
  schemes). The platform was then validated by provisioning **working, conformance-clean
  instances for all 12 sector families** (Financial + Technology, Healthcare/Pharma,
  Food/Bev/Consumer, Retail, Energy/Chemicals, Aerospace/Defense/Aviation, Telecom,
  Automotive, Media, Logistics/Transport, Industrial) under `instances/`, each with a
  S1→S5 chain + BOL + cockpit + §7L and passing the C1–C5 conformance gate. The on-time-
  exception operating loop is the same across sectors; only the domain vocabulary
  (URIs, outcome class, trust claim, prose) differs. Spec release mirror not re-synced.

---

> **Core principle statement.** Every requirement in this specification exists to carry
> one **Actor↔Actor relationship** across Relationship · Interaction · Event · State,
> concentrating AI where it pays most and compounding verified evidence no single
> service can copy. The ontology (Actors, Purpose, Context, Authority, Rights,
> Resources, Value) grounds everything; the services implement it.
> **The moat is not the data. The moat is the verified history of decisions and outcomes
> attached to relationships — compounded by Learning.** Anyone can collect customer data,
> transactions, documents, and telemetry. What is harder to reproduce is the verified
> chain of *situation → evidence → recommendation → human decision → action → outcome →
> verification → what we learned*, repeated across thousands of decisions. That is what
> no CRM, ERP, or LLM wrapper can copy.