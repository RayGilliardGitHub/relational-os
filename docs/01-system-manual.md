# 01 — SYSTEM MANUAL

**Audience:** engineer / architect. **Scope:** what the completed system is, how it is
put together, the data model and ontology, the URI cap and frozen ontology, the schema +
conformance + EBNF, the technology truth, and a file→artifact map.
**Grounding:** SPEC v0.22 (`/home/rlg/relational-os/SPEC.md`) and the verified Sprints 0–5
build under `/home/rlg/relational-os/archive/sprints/`. Section references are to `SPEC.md §X`.

---

## 1. Architecture in one diagram

RelationalOS is not a monolith; it is a **chain of five services** over one shared
substrate, capped by a **Business Operating Layer (BOL)** and an **AI-supervisor →
human-decision-maker** surface (SPEC §7J reframe).

```
                 RELATIONALOS
        ┌─────────────┴─────────────┐
    SUBSTRATE                   SERVICES
 (graph · ledger · knowledge   (S1–S5 lifecycle)
  · rules · rights · authority
  · consent · resources · evidence · trust)
        │
        ▼
   BUSINESS OPERATING LAYER        ← the product an owner uses every morning
 (goals · metrics · cases · exceptions ·
  tasks/work · priority · dependency · risk)
        │
        ▼
   AI SUPERVISOR  →  HUMAN DECISION MAKER
```

**The integration point** is the shared substrate: one **Relationship Graph (state)** and
one **append-only, content-addressed, signed Ledger (history)**. SPEC §3.16 is normative:
*Ledger = history, Graph = current state — never conflated.* Every service consumes
prior-state from the graph, writes its stage (+ evidence) as a signed event to the ledger,
and hands a complete relationship forward (SPEC §4).

## 2. The services (S1–S5)

| # | Service | Owns (SPEC §4) | Function |
|---|---|---|---|
| S1 | Identity, Authentication, Authorization | Identity base | `resolve_identity` → `authenticate` → `authorize` → `resolve_role`. **Identity ≠ Authentication ≠ Authorization** are three functions, not one (§3.19). Authorization is **capability-based** and **relationship-scoped** (§7B, §3.4). |
| S2 | Intent & Matching | Intent, Capability, Offer | `infer_intent` → `match_offers` (Trust-weighted ranking). First revenue service. |
| S3 | Orchestration & Execution | Commitment, Action | `agree` → `execute` with an agent fleet across a routing seam (local / private-cloud / frontier); **irreversible or unknowable-cost actions escalate to a human** (§6 floor). |
| S4 | Exchange & Settlement | Exchange, Outcome | `settle` (payment obligation + receipt + reconciliation as **signed ledger events**) and `evaluate` (outcome `met|partial|failed`). Asset title/custody moves on `asset://` (§4b). |
| S5 | Trust engine | Evidence, Trust | `capture` (signed, grounded evidence) → `verify` → `update_trust`. Trust is **scoped** keyed `(subject, target, claim, context)`, never a global score (§3.14). |

The **trust flywheel** (the moat): a verified good/bad outcome → captured as signed
evidence → scoped Trust updated → S2 re-ranks the next match. Verified repeatedly across
Sprints 1–5 (e.g. `checks.flywheel_check`, `checks.loop_check`).

## 3. The substrate: Graph = state, Ledger = history (§3.16)

- **Ledger (history):** append-only, **content-addressed** (each entry's `hash` =
  `SHA-256(prev_hash ‖ canonical(payload))`), and **signed** by the responsible service
  (`signature: sig:<service>:<sha256>`). Verified by `substrate.ledger.verify()` and by
  conformance **C3**. (Code: `ros/substrate.py` `Ledger`.)
- **Graph (state):** current relational truth keyed by URI; `put`/`get`/`resolve`.
  (Code: `ros/substrate.py` `Graph`.)
- **Full-coverage rule:** every object the operating layer creates is carried by a signed
  ledger event's `state_update`, so the **whole Graph rebuilds from the whole Ledger**
  (round-trip). Verified each sprint; end-state = **160 graph objects rebuilt
  from 97 ledger events**.
- **Immutable snapshots (§3.16, Sprint-5 F2):** a signed `state_update` embeds **deep
  copies** of the objects it carries. A later in-place edit to a live mutating object
  (e.g. a Case's `history`) must NOT retroactively alter an earlier signed entry — doing so
  would break the content-address hash-chain. This is why the operating layer `prov()` deep-
  copies into every event.

## 4. The Business Operating Layer (the product) — `ros/bol.py`

The BOL sits on the substrate and implements SPEC §7J/§7K as **assemblies of existing
primitives** — no new nouns (URI cap, §7J.11/§C16):

- **Case** (`case://` §7J.3): universal unit of unresolved work; lifecycle
  `OPEN→TRIAGE→ASSIGNED→IN_PROGRESS→BLOCKED→RESOLVED→CLOSED` (+REOPEN), each transition
  a signed event with evidence.
- **Goal / Metric** (`goal://` / `metric://`) + the goal loop
  `Goal→Metric→Actual→Variance→Decision→Action→Outcome` (§7J.1). Metrics carry
  `target/actual/forecast/variance/threshold` (§7K.1 Forecast).
- **Exception** (§7J.2): heartbeat
  `EXPECTED→ACTUAL→VARIANCE→SIGNIFICANCE→EXCEPTION→ROOT→RECOMMENDED→DECISION→EXECUTION→VERIFIED`
  — carried as **additive fields on the `case://`** (not a `exception://` scheme).
- **Priority** (§7J.5): `Priority = f(impact, urgency, confidence, irreversibility,
  relationship-importance, cost-of-delay)`, a deterministic weighted score → priority-
  ordered attention. Additive field on `task://`/`case://`.
- **Task & Work Queue** (§7J.4): recommendations become assigned, **authorized** work
  (`task://` with `assigned_to`, `authority://`, `assigned_capacity`, `priority`).
- **Dependency** (`dependency://` §7J.6): `requires/blocks/enables/derived_from/impacts`
  with a **transitive impact analysis** (`impact_analysis()`).
- **Recommendation** (§7J.9): additive fields on the case; carries `authority_required`,
  options **incl. do-nothing**, confidence, expected impact, trade-off.
- **Learning** (§7K.1): a `decision://` entry
  `Decision→Expected→Actual→Variance→WHY→change-future-policy` + a future-policy change on
  a `policy://` — organizational learning, promoted above all.
- **Capacity (Q9):** additive `assigned_capacity` on the assigned task (no `capacity://`
  scheme; that `$def` exists but is not in the URI catalog — Sprint-5 F6).

Derived values (Exception/Priority/Recommendation/Capacity) are **never new nouns** — this
is the strongest confirmation of the URI cap: the schema stayed byte-identical (49 `$defs`)
across Sprints 1–5.

## 5. URI cap & frozen ontology (§7J.11, §C16)

Only **five** first-class operating nouns were ever added to the ontology (Sprint 0):

    case://  goal://  metric://  task://  dependency://

Everything else the operating layer needs — Exception, Priority, Recommendation, capacity —
is an **additive envelope field** on those objects. Learning is a `decision://` + a
`policy://` change. The full Appendix C catalog remains authoritative; new schemes MUST be
**additive** (added, never reclassified) so resolvers and round-tripping stay valid (§C16).

### 5.1 Company-branding component (Sprint 7)

Every **sector instance** (see `instances/README.md`) carries a company **brand** for its
website About / marketing / FAQ surface. It is a **data model addition, not a new scheme**:

- **Data model:** an additive **`brand` object on the company `org://` actor** — exactly the
  same mechanism as Exception/Priority/Recommendation/capacity on cases. `Actor` is an
  `envelope` (`additionalProperties: true`), so the brand validates under C2 and round-trips
  under C4 with **no schema or ontology change** and **no `brand://` noun** in the URI
  catalog (§7J.11/§C16 held).
- **Fields** (sector-applicable subset of the 20-feature home page set): `tagline, mission,
  vision, values[], about, fast_facts[], history[], leadership[], products_services[],
  testimonials[], trust[], locations, faq[], contact, careers, investors, press, esg, legal,
  nav[], cookie_consent, design{palette[], typography, logo{}, imagery, tone}`.
- **Where it's defined:** per-sector `brand` blocks in `instances/configs.py` (`BRANDS`,
  keyed by label). The legacy Finance v1 carries its own copy in `financial/fin_demo.py`.
- **Rendering:** `sector_scene.py` writes `cfg['brand']` onto the company actor at
  provisioning, renders the brand into the **cockpit report** (lead header `Company — tagline`
  plus a `## Brand` appendix; `cockpit.json` carries it), and emits a per-instance
  **`branding.md`** marketing artifact. The BI snapshot's label line identifies the company
  (`Northglen Bank — Funding that lands on the date.`). The reference build (`ros/`) is
  untouched — brand rides the sector instances, not the platform chain.

## 6. Schema + conformance validator + EBNF

- **Schema (normative type contract):** `/home/rlg/relational-os/schema/relational-os.schema.yaml`
  (draft 2020-12, **49 `$defs`**; + generated `.json`, and `build_schema.py`). One source of
  type truth; `x-uri-catalog` groups `identity / relationship / domain-object`.
- **Conformance validator:** `/home/rlg/relational-os/schema/conformance.py`.
  Checks (the audit's core, see `04-audit.md`):
  - **C1** schema structurally valid
  - **C2** per-instance schema + Appendix-C URI-kind compliance + RFC 3339 temporal (jsonschema
    ships no date-time checker, so it enforces RFC 3339 itself)
  - **C3** ledger content-addressed SHA-256 chain + signature presence (§2/§3.16)
  - **C4** round-trip preserve-unknown (§2, Appendix C) — unknown fields MUST survive rewrite
  - **C5** Relationship and Case state-machine legality (§3.16, §7J.3)
- **EBNF grammar:** `/home/rlg/relational-os/schema/relational-os-lifecycle.ebnf`
  — the lifecycle/instance grammar companion to the schema (relationship·interaction·event·state
  spine, the two state machines, the five §7J nouns, derived chains, RFC-3339 temporal, typed-URI
  grammar). The JSON Schema remains the normative type contract.

## 7. Technology truth (§G.11, ROI sequencing)

The verified build is **deterministic local Python** — no frontier-API spend (~$0/run). Per
SPEC §G.11 the priority weights, the forecast, and the root-cause nomination are **explicit,
documented local logic**, not learned or frontier-API behavior — the right call at the build
stage, and *not* the production answer (see "Future deployment" below; SPEC §8 marks this a
Phase-B item).

**Multi-sector generalization (post-close hardening, v0.22):** the reusable operating
surface is `BolService` + the generic `S4Service`/`S5Service`, which now take an org/path
`label` (default `'qk'`) so an instance builds clean URIs on its own segment instead of the
construction reference's `qk`. This was a genuine defect the multi-sector build surfaced
and fixed; the reference Quoteko build is byte-identical at the default and re-verifies
ALL PASS. `S1.authorize`/`resolve_role` and `S2.match_offers` are generic and reused
directly; the reference `S3` orchestration is a construction-scene service (hardcoded
roofing fleet/actions), so new-sector instances exercise the §6 human floor at the BOL
surface (signed escalation → owner decision → ACTION), not S3's construction scene.
Proven by provisioning conformance-clean instances for all 12 Appendix-B sector families
under `/home/rlg/relational-os/instances/` (see `instances/README.md`). The **frozen
ontology and URI cap are unchanged** — no new nouns, no new schemes.

**Branding component (Sprint 7 — planned):** each instance will carry a company **brand**
block (the website-About / marketing / FAQ / design-language set: tagline, mission, vision,
values, about, history, leadership, products, testimonials, trust, fast-facts, locations,
FAQ, contact, careers, investors, press, ESG, legal, nav, cookie consent, palette/
typography/logo/tone) as **additive `brand` fields on the company `org://` actor** — the same
additive-field convention as Exception/Priority/Recommendation (§7J.5/§C16), so the URI cap
and frozen ontology hold. Generated cockpit/BI reports will carry the brand (lead header +
`## Brand` appendix). Build hand-off: `archive/sprints/sprint-7/PROMPT.md`.

## 8. File → artifact map (what lives where)

Root: `/home/rlg/relational-os/`

| Path | What it is |
|---|---|
| `SPEC.md` | The working spec (v0.22) — **the contract**. |
| `PROTOCOL.md` | The sprint lifecycle every build session follows. |
| `README.md` | Workspace index (points at this docs package). |
| `docs/` | The verified manual package (Sprint 6) — canonical at repo root, narrative copy at `docs/`. |
| `archive/sprints/COMPLETE.md` | Project closing hand-off (Sprints 0–5). |
| `archive/sprints/` | Narrative build history (PROMPT/plan/work/notes/summary per build step) — kept for provenance; not the run surface. |
| `schema/` | Schema (`schema/`), `conformance.py`, `run_conformance.py`, `make_fixtures.py`, `fixtures/` (156 instances incl. 20-interaction Appendix-E + case-lifecycle + ledgers + statemachines), `surveys/` (4 commissioned surveys), `.venv/` (jsonschema/referencing/yaml deps). |
| `/ros/` (repo root) — canonical | `substrate.py` (Graph+Ledger+sign), `s1..s5.py` (services), `bol.py` (Business Operating Layer), `checks.py` (the PASS/FAIL assertions). Promoted from `ros/` (its byte-identical origin snapshot) by the reorg. |
| `reference/reference/run_s5_demo.py` | The **daily cockpit** producer (rebuild whole state + write fixtures + reports). |
| `schema/run_conformance_all.py` | Validator re-run over all SIX fixture generations. |
| `reference/{s3,s4,s5,bol}_demo.py` | Builders that script the scenes. |
| `reference/graph/current-state.json` | Produced Graph (state). |
| `reference/fixtures/ledger/ledger-quoteko.json` | Produced Ledger (history). |
| `reports/cockpit.md` / `.json` | The daily cockpit + §7L answers. |
| `data/fixtures/gen-0..4` + `reference/fixtures` (gen-5) | The fixture corpus the validator checks (gen-0 156 / 28 / 35 / 55 / 174 / 316 instances). |
| `~/Documents/ai-relational-os-spec.md` (+.pdf) | Release mirror (read-only reference for cross-checks). |

## 9. Future deployment (spec'd, not built in Sprints 0–5)

These are fully specified but **NOT implemented** in the verified build; the working
analogue *today* is noted. See SPEC §7E–H, §8.
- **§7F continuous audit *service*** (per-entity auditor actor, findings as
  `audit_finding://` signed events, remediation queue) → *today's analogue:* the conformance
  C1–C5 harness + `Ledger.verify()` + the full-state round-trip (detailed mapping in `04-audit.md`).
- **§7G BI *warehouse*** (SQL transforms over ledger projections, Metabase/Superset) →
  *today's analogue:* the deterministic ledger projections in `ros/bol.py` + the cockpit
  health panel (detailed in `05-bi-reports.md`).
- **§7E frontends / IoT channel** (Flutter clients, MQTT/CoAP headless devices) → not built; the cockpit is a markdown report.
- **§7H external gateway** (payments, payroll, tax, regulatory rails) → not built; S4 settlement is seam-mocked.
- **Confidential-compute anchoring, real graph/ledger store + redundancy (no SPOF), real
  S2/S4 connectors, AI routing for root-cause/forecast over real data, and the §8 Phase-B
  backlog** (process mining, change detection, scenario/what-if, decision learning,
  organizational memory, universal query, benchmarking) → future.

*See also `archive/sprints/sprint-5/summary.md` and `archive/sprints/COMPLETE.md` for the same boundary
stated at build close.*