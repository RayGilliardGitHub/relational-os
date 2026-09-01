# SPRINT 1 — PLAN

**Project:** RelationalOS | **Spec:** v0.17 → target **v0.18**
**Date:** 2026-09-01 | **Status:** Planning-first per PROTOCOL.

## Objectives
Build the S1 substrate (thin) + the S2 Intent/Matching minimum for **one role
(customer)** on **one domain (a quoting/triage flow)** for one fictional company.
Prove the §5 loop end-to-end on the shared Ledger + Graph, with every artifact
schema-conformant against the Sprint-0 (v0.17) contracts and validated by the
re-used conformance validator.

## Fictional scene (chosen to match DoD)
- **Quoteko** (`org://quoteko`) — a property-services **quoting/triage marketplace**:
  it resolves/enrolls a customer, infers intent, and matches the intent to vetted
  contractor **offers** (`offer://`), ranked by fit and Trust. S2 revenue service.
- Customer `person://qk/customer` joins as **role=customer** (relationship://).
- Contractors `org://qk/norcrete` and `org://qk/solarworks` hold `offer://` quotes
  with capabilities + price, each carrying a scoped `trust://` (S5-seeded T1 in this
  context) used to re-rank.
- S1 and S2 are **Agent actors** (`agent://s1`, `agent://s2`) acting under a
  `delegation://` from Quoteko — so authorization-by-relationship and delegation
  honoring are exercised for real.

## Sub-sprints
- **1.1 S1 substrate (thin).** A runnable Python service that reads/writes the shared
  Relationship Graph + append-only Ledger exactly per Sprint-0 schema: implements
  `resolve_identity`, `authenticate`, `authorize` (capability-based per §7B),
  `resolve_role`. DoD: identity→role resolution against the ledger; a **new S1 check
  of my own** (authorize used per relationship; delegation honored, incl. a revoked
  delegation denial).
- **1.2 S2 Intent/Matching (min).** `infer_intent` + `match_offers` (Trust-weighted
  per §5) for the Quoteko quoting domain. Ranked matches become **signed Events** on
  the ledger; a **human verifies** (acknowledgment) before the match is committed as
  current state. DoD: runnable cycle `identity → intent → matched offer →
  human-verified → on the ledger` in a test that RUNS.
- **1.3 Ledger/graph wiring.** Show the full S1→S2 slice writing: each match = a
  content-addressed, **signed** Ledger event; current state (the match, its status)
  lands on the Graph. Ledger=history / Graph=state kept distinct (§3.16). DoD:
  a round-trip check proves Graph state reconstructs to its Ledger events.

## Definition of Done (all must hold)
1. `plan.md` written first; each sub-sprint has `work/<n>-plan.md` written before it executes.
2. S1 + S2 run and produce real, verified output under `sprints/sprint-1/artifacts/`.
3. **Sprint-0 conformance still exits 0** (no schema/ontology regression).
4. The full slice, emitted as fixtures, validates under the **same Sprint-0 validator**
   pointed at the Sprint-1 fixtures → exit 0.
5. A new self-authored S1 check passes (authz per relationship + delegation honored +
   revocation denial).
6. Graph→Ledger round-trip check passes.
7. `SPEC.md` updated to **v0.18** for genuine findings only (targeted patches; URI cap
   and frozen ontology respected — no new nouns/schemes unless a real build finding
   forces an additive one, which is then justified in findings).
8. `summary.md` written.
9. Next-sprint prompt written at `sprints/sprint-2/PROMPT.md` and echoed as final message.

## Exit criteria / guardrails
- Real tool output only. No fabrication.
- Single-threaded (no subagents) per PROTOCOL.
- Reuse Sprint-0 schema + conformance.py — do not re-derive. Extend schema only if a
  genuine finding requires it (additive-only); if so, rebuild `.json` via
  `build_schema.py`.
- Budget ~$0 (local computation only; no web/API spend).
- Touch nothing outside `/home/rlg/relational-os/` (except reading the `~/Documents`
  mirror, which I will not modify).
- Clean English; `file://` absolute paths when reporting files.