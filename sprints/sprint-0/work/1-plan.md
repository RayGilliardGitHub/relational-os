# SUB-SPRINT 0.1 — PLAN — Formal machine-validatable schema

**Read first (done):** `SPEC.md` in full — §2 norms, §3 ont serang primitives (Actor,
Purpose, Context, Relationship, Interaction, Event, State, Expectation, Claim, Evidence,
Decision, Delegation, Consent, Dispute, Value/Cost/Price, Trust/Reputation, Resource/
Asset/Knowledge, Rights/Obligation/Commitment, Rule, §3.16–3.19), §7J (Case/Goal/Metric/
Task/Dependency/Exception/Priority), §7K structural semantics, Appendix C URI conventions,
Appendix F starter schema (the seed to expand).

## Objective
Expand Appendix F into ONE machine-validatable schema covering every §3 primitive and
the §7J operating objects, enforcing Appendix C conventions and §7K structural semantics.
**Choice of representation:** JSON Schema (draft 2020-12), authored in YAML with anchors
(both validatable; YAML is human-readable, json.load-able after anchor resolution). Per the
spec's own G.11 footgun rule (one source, no drift), this single schema IS the source of
truth under `artifacts/`, and the validator reads it directly.

## Deliverables (under `sprints/sprint-0/artifacts/`)
- `schema/relational-os.schema.yaml` — the schema (YAML+anchors).
- `schema/relational-os.schema.json` — the same after anchor resolution (portable).
- `schema/build_schema.py` — resolves YAML anchors → JSON (reproducible from one source).
- A self-check instance `schema/_selftest.instance.json` validating against the schema.

## Schema content map (derived strictly from SPEC, no new nouns/URIs)
- **$defs per §3 primitive** with Appendix F fields as the seed, expanded structurally.
- **Enums exactly as spec'd:** Event type (ACTION, DECISION, EXCHANGE, OUTCOME,
  STATE_CHANGE, EXTERNAL); Relationship status; Case status (+REOPEN via transition);
  Task status (work-queue states); Delegation/Consent/Dispute statuses; Evidence kind.
- **Universal Event fields** §7K.1: event_id, correlation_id, causation_id, idempotency_key.
- **Appendix C conventions:** `uri` is a typed URI string constrained to the catalog;
  three-kind separation (identity / relationship / domain-object); collision rule;
  additive-only; unknown-field round-trip preserve.
- **§7J/§7K structural:** Case, Goal, Metric (incl Forecast fields Target/Actual/
  Forecast/Variance/Threshold), Task, Dependency, Exception (derived), Priority (derived),
  SLA (assembly), ProcessInstance, Policy (Condition→Decision→Action), Risk, Escalation,
  Entity(canonical resolution).
- **§2 norms:** RFC3339 timestamps (format assertion), UTF-8 strings, signed ledger entries.

## Definition of Done
- YAML parses; anchor resolution produces valid JSON; `jsonschema` validates the schema
  structure; a sample instance validates successfully.