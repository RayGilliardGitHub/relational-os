# SPRINT 2 — FINDINGS (feeds the v0.19 spec update)

Collected 2026-09-01 during the S5 Trust-engine-minimum build (Quoteko quoting
domain; one crisp outcome class: "roofing job completed by its committed deadline").
All executed with real tool output (no subagents).

## F1 — The Trust engine builds entirely on existing Sprint-0 contracts (confirms spec, no schema change)
`capture(as outcome+provenance → evidence://)`, `verify(evidence, statement →
{claim, degree, procedure})`, `make_expectation → expectation://`, and
`update(Trust, evidence, weight, recency) → trust://` all run using ONLY the
Sprint-0 `$defs` (Trust, Evidence, Claim, Expectation, Event) and existing URI
schemes (`evidence:// claim:// expectation:// trust:// event:// relationship://
interaction:// decision://`). **No schema or ontology/URI extension was needed** —
the frozen ontology and §7J.11/§C16 URI cap held. The S5 state delta (evidence,
claim, updated trust) embeds in each signed ledger event so Graph→Ledger
reconstruction stays exact (reused Sprint-1 1.3 round-trip, still 3/3 PASS).

## F2 — §5 equation + scoped keying behave exactly as specified (confirms §5/§3.14, no change)
- Trust is keyed `(subject, target, claim, context)` — NOT a global score. A verified
  **good** outcome moved `org://qk/solarworks` 0.61 → **0.708**; a verified **bad**
  outcome moved `org://qk/norcrete` 0.92 → **0.528**; `org://qk/generalco`
  (different claim, "roofing reliability") stayed **0.42 untouched** — proof of scope.
- Clamp holds: all values in [0,1]. Updates are driven by seeded/verified evidence
  (alpha=0.5, same for both; expectation=0.8, evidence confidence=0.98, recency=1.0),
  no hardcoded speculative weighting (§G.11).
- Flywheel demonstrated: equal-fit offers (both fit=1.0) re-rank purely by Trust —
  solarworks #2→#1, norcrete #1→#2; score = fit×trust matches the equation output.

## F3 — Persisted trust:// must carry its update inputs to be auditable (genuine clarification; additive, no schema change)
The schema's `Trust` $def has `score` / `evidence` / `updated_at` but the §5 equation
references `expectation/outcome/evidence/alpha/recency`. Without carrying those the
new score can't be reproduced or audited from the object alone. **Addressed by storing
them as additive envelope fields** on each `trust://` (`expected`, `outcome`,
`evidence`, `alpha`, `recency`) — the schema's `additionalProperties:true`
round-trip rule accepts them, so **no schema change**. Two build-real notes added to
`SPEC.md §5` (normative): the persisted trust object carries these inputs; and
`Trust.evidence` is an **array** of `evidence://` refs (`evidence_ref`) — a single
evidence URI must be wrapped in a list (build initially set a bare string and failed
C2; fixed).

## Net spec impact (v0.18 → v0.19)
- URI cap and frozen ontology: **unchanged, respected** — no new nouns or URI schemes.
- Schema (`sprints/sprint-0/artifacts/schema/`): **NOT extended**; validator unchanged
  (still v0.17 artifacts).
- One additive normative clarification added to **§5** (persisted trust carries its
  update inputs; `Trust.evidence` is an array). Version bump to **0.19**; Version/
  Review Log entry appended.
- Conformance: Sprint-0 (156), Sprint-1 (28), Sprint-2 (35) — **ALL PASS, exit 0**,
  one shared validator (no regression).