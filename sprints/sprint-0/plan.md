# SPRINT 0 — PLAN

**Project:** RelationalOS (chain of integrated services delivering AI at maximum ROI)
**Spec:** v0.16 (`/home/rlg/relational-os/SPEC.md`)
**Date:** 2026-09-01
**Sprint objective:** Deliver the *implementation contract* — a machine-validatable
schema, a conformance validator, executable fixtures, and the four committed surveys —
so independent implementers and Sprints 1–5 can build against real, checked contracts.

## Objectives
1. Turn the Appendix F starter schema and every §3 primitive + §7J/§7K operating
   object into one **machine-validatable schema**.
2. Prove the schema by **running** a conformance validator over executable fixtures:
   the 20 Appendix E interactions, the §7L ten-question loop, and the Case lifecycle.
3. Deliver the **four committed surveys** (§7D-E, §8) with real citations and DoDs.
4. Update `SPEC.md` to 0.17 only where the build surfaces genuine findings.

## Definition of Done
- `sprints/sprint-0/plan.md` written first; each sub-sprint has `work/<n>-plan.md`
  written before that sub-sprint executes. ✓ (this file)
- **0.1** — validatable schema (JSON Schema authored in YAML w/ anchors) under
  `artifacts/`; passes a syntactic/structural validation.
- **0.2** — Python conformance validator + fixtures (20 interactions, §7L loop, Case
  lifecycle) under `artifacts/`; `run_conformance.py` exits 0 with all checks passing.
- **0.3** — four survey reports with real citations under `artifacts/surveys/`, each
  meeting its stated DoD.
- `SPEC.md` updated to **v0.17** from genuine findings; Version/Review Log appended.
- `sprints/sprint-0/summary.md` written.
- `sprints/sprint-1/PROMPT.md` written AND echoed verbatim as the final message.

## Sub-sprint breakdown (executed sequentially, single-threaded)
1. **0.1 — Formal schema.** Build a JSON Schema (draft 2020-12) covering: §3 Actor,
   Purpose, Context, Relationship (state machine), Interaction, Event (6 types +
   §7K idempotency/causation/correlation fields), Expectation, Claim, Evidence,
   Decision, Delegation, Consent, Dispute, Rights/Obligation/Commitment, Rule, Trust/
   Reputation, Resource/Asset/Knowledge; §7J Case/Goal/Metric/Task/Dependency +
   Exception/Priority (derived, no URI) + §7K structural semantics (ProcessInstance,
   Policy, Risk, Escalation, SLA-as-assembly, Entity). Enforce Appendix C conventions:
   typed URIs, three-kind separation, collision rule, additive-only, round-trip
   preserve-unknown. Validate with the venv's `jsonschema` against a sample instance.
2. **0.2 — Validator + fixtures.** Python `conformance.py` (URI catalog check,
   RFC3339/enum conformance via jsonschema against the 0.1 schema, ledger chaining,
   round-trip preserve-unknown probe, Relationship & Case state-machine legality).
   Fixtures: `fixtures/appendix-e/*.json` (20 interactions), `fixtures/7l-loop/*.json`
   (one fictional company), `fixtures/case-lifecycle/*.json` (OPEN→CLOSED w/ REOPEN).
   Runner `run_conformance.py` must pass.
3. **0.3 — Surveys.** Four written reports (cited) under `artifacts/surveys/`:

   | # | Survey | DoD |
   |---|--------|-----|
   | 1 | §7I data-source & licensing | ranked source matrix: cost / ToS / rate limit per source + default ingest set |
   | 2 | §7H jurisdiction & tax-filing | verified filing-calendar seed per target jurisdiction + vendor comparison |
   | 3 | §7G BI report-catalog | validated, versioned report catalog vs authoritative references |
   | 4 | §7I data boundary | intake allow-list + privacy-policy skeleton under Consent/Disclosure |

## Exit criteria
- Every artifact RAN (real tool output recorded in this sprint); no fabricated results
  or citations.
- URI cap (§7J.11) and frozen ontology (§3) respected — no new nouns/schemes.
- $ budget respected: local compute for build; batched web calls for surveys.

## Hand-off
Final message == saved `sprints/sprint-1/PROMPT.md` (self-contained, absolute paths,
current SPEC v0.17).