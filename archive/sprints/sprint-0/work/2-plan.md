# SUB-SPRINT 0.2 — PLAN — Conformance validator + executable fixtures

**Read first (done):** SPEC §2 norms, §3.16/§7F audit classes, §5 loop, §7J.3/7J.4
state machines, Appendix E (the 20 interactions), Appendix F, Appendix G (tooling per
G.1/G.9; Python chosen G.1), and the 0.1 schema under `artifacts/schema/`.

## Objective
Prove the 0.1 schema by RUNNING a conformance validator over real executable fixtures:
(1) the 20 Appendix E interactions, (2) the §7L ten-question operating loop for one
fictional company, (3) the Case lifecycle OPEN→…→CLOSED with REOPEN. All must pass.

## Deliverables (under `sprints/sprint-0/artifacts/`)
- `conformance.py` — validator. Checks:
  - **C1** schema structurally valid.
  - **C2** per-instance: classify by URI scheme (x-uri-catalog), validate against the
    mapped `$def` via jsonschema; enforce RFC3339 on temporal fields (F1); enforce
    Appendix C scheme membership (three kinds) + additive-only.
  - **C3** ledger: content-addressed hash-chaining (SHA-256) + signature presence on
    signed events.
  - **C4** round-trip preserve-unknown probe (unknown fields must not be rejected).
  - **C5** state machines: Relationship (PROPOSED→ACTIVE→SUSPENDED→…→TERMINATED→
    ARCHIVED) and Case (OPEN→TRIAGE→ASSIGNED→IN_PROGRESS→BLOCKED→RESOLVED→CLOSED,
    +REOPEN).
- `run_conformance.py` — CLI runner over all fixtures; exit 0 iff all pass.
- `fixtures/appendix-e/20.json` — the 20 interactions (Appendix E), each a valid
  Relationship/Interaction/Event/Claim/Evidence instance (18 native, 2 derived flagged).
- `fixtures/7l-loop/*.json` — one fictional company ("Meridian Machine Works") answering
  the ten §7L questions with evidence objects (Metrics, Cases, Exceptions, Tasks,
  Decisions, Recommendation, verified Outcome).
- `fixtures/case-lifecycle/sequence.json` — a Case walking OPEN→TRIAGE→ASSIGNED→
  IN_PROGRESS→BLOCKED→IN_PROGRESS→RESOLVED→CLOSED→REOPEN→RESOLVED→CLOSED.

## Definition of Done
- `./.venv/bin/python run_conformance.py` exits 0, prints a per-check PASS and a summary.
- Every fixture validates, every state-machine sequence is legal, ledger chain verifies.