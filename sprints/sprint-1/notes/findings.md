# SPRINT 1 — FINDINGS (feeds the ver0.18 spec update)

Collected 2026-09-01 during S1 substrate + S2 Intent/Matching build (Quoteko quoting
domain). All executed with real tool output (no subagents).

## F1 — S1 substrate is thin, role is a relationship attribute (confirms spec, no change)
`resolve_identity / authenticate / authorize / resolve_role` run against the shared
Graph + Ledger using only schema-conformant objects. Role resolution is per-relationship
(§C2: roles are attributes of `relationship://`, never a separate identity) — a customer
role resolved in the customer relationship, absent in an unrelated relationship. No spec
change; behavior matches §3.19 / §4 S1.

## F2 — Capability-based authz + delegation revocation work (confirms §7B, no change)
`authorize()` returns a bounded, expiry-bound capability. An ACTIVE `delegation://`
(scope → `rule://` carrying `grants`) grants the agent's action; setting that delegation
to REVOKED turns the same call into a DENIAL immediately — §3.4/§7B "delegation
revocation voids the capability" is demonstrated, not assumed.

## F3 — Trust-weighted matching re-ranks (confirms §5, no change)
`match_offers` scores each candidate as `fit(intent∩capability) × scoped Trust(subject→
provider, claim, context)` (§3.14), clamped [0,1], and rejects offers below a trust
floor. Two equal-fit offers ranked by their scoped Trust (0.92 vs 0.61) — the exact §5
flywheel mechanism that S2 must carry into Sprint 2.

## F4 — Human-escalation floor engaged (confirms §6/§7B, no change)
Hiring a contractor is irreversible/unknowable-cost, so the top matched offer is only
committed after a **human** (the customer) records a signed verification/acceptance
event. Never auto-committed by the S2 agent.

## F5 — Ledger=history / Graph=state wiring validates (§3.16/§7C, no change)
Events are content-addressed (SHA-256 over prev-hash + payload), signed by the
responsible service, RFC3339. Current state lives in a separate Graph projection. A
round-trip check rebuilds every Graph object from the Ledger events that produced it
and asserts history/state are not conflated — the wiring contract holds with no
conflation.

## F6 — **Schema-fidelity clarification (genuine finding; drives a spec note, not a schema change)**
`delegation.scope`, `consent.scope`, and `Context.purpose` in the Sprint-0 schema are
URI-typed (`$def::uri`, pattern `^[a-z]…://…`), NOT free-string names. The first Sprint-1
attempt used `scope:["run_matching"]` and `context.purpose:"property-services quoting"`
and FAILED conformance (C2). Corrected model: a `delegation://`/`consent://` `scope` is a
list of `rule://`/`permission://` references, and `Context.purpose` references a
`purpose://` URI; action grants live on the referenced `rule://` object (a `grants`
list). This is fully consistent with the existing schema and Appendix F (which already
shows `Delegation.scope: rule://*`); it is a clarification for implementers, so the ONLY
spec action is a short normative note in §3.4 — no schema/ontology/URI change. Schema
stays v0.17 artifacts, unchanged.

## Net spec impact (v0.17 → v0.18)
- URI cap and frozen ontology: **unchanged, respected** — no new nouns or URI schemes;
  reused `purpose:// permission:// rule:// authority:// delegation:// consent://
  trust:// offer:// service:// event:// decision:// entity:// evidence://
  relationship:// person:// org:// agent:// db://ledger`.
- Schema (`sprints/sprint-0/artifacts/schema/`): **not extended**; validator unchanged.
- One additive normative clarification added to §3.4 (delegation scope = URI refs;
  revocation verified). Version bump to **0.18**; Version/Review Log entry appended.