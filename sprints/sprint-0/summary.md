# SPRINT 0 — SUMMARY

**Project:** RelationalOS | **Spec:** v0.16 → **v0.17** | **Date:** 2026-09-01
**Result:** Sprint 0 complete — implementation contract delivered and **verified**.

## What was built
Three sub-sprints, all done single-threaded with real tool output (no subagents):

**0.1 — Formal schema** (`artifacts/schema/`)
- `relational-os.schema.yaml` — JSON Schema (draft 2020-12), YAML w/ anchors, covering all
  §3 primitives (Actor, Purpose, Context, Relationship, Interaction, Event, Expectation,
  Claim, Evidence, Decision, Delegation, Consent, Dispute, Rights/Obligation/Commitment,
  Rule, Trust, Reputation, Resource/Asset/Knowledge, Entity, Revision), the §7J operating
  objects (Case/Goal/Metric/Task/Dependency), and §7K structural semantics (Process,
  ProcessInstance, Policy, Risk, Capacity, Escalation, SLA, plus derived Exception/
  Priority/Recommendation). Appendix C URI catalog encoded as `x-uri-catalog` with
  three-kind discipline; §2 RFC3339 + UTF-8 + signed-ledger norms; round-trip
  preserve-unknown (additionalProperties).
- `relational-os.schema.json` (built via `build_schema.py`, one source → no drift, per
  G.11). Schema is structurally valid (draft 2020-12) and a sample instance validates.

**0.2 — Validator + fixtures** (`artifacts/conformance.py`, `run_conformance.py`,
`fixtures/`)
- 5 checks, **all PASS, exit 0**: C1 schema valid (49 `$defs`); C2 all **156 fixture
  instances** validate against their scheme-mapped `$def` + Appendix C membership +
  RFC3339; C3 ledger SHA-256 hash-chain + signed; C4 round-trip preserve-unknown; C5
  Relationship + Case state machines.
- Fixtures: **20 Appendix E interactions** (`fixtures/appendix-e/`), the **§7L ten-question
  loop** for one fictional company Meridian Machine Works (`fixtures/7l-loop/`), the **Case
  lifecycle OPEN→…→CLOSED incl. REOPEN** (`fixtures/case-lifecycle/`, `statemachines/`),
  and a content-addressed ledger (`fixtures/ledger/`). Regenerated reproducibly via
  `make_fixtures.py`.
- Reused the venv: `./.venv/bin/python run_conformance.py` → exit 0.

**0.3 — Four committed surveys** (`artifacts/surveys/`), real citations, all DoDs met:
1. `01-data-licensing.md` — ranked source matrix (GDELT/EDGAR/RSS = base; Reuters/X/
   LinkedIn/TikTok/Reddit/Glassdoor = Phase-B, mostly no free commercial API) + default
   ingest set.
2. `02-jurisdiction-tax.md` — federal + New Mexico + ABQ filing-calendar seed + vendor
   comparison (Avalara/Vertex/Sovos/TaxJar, payroll e-file).
3. `03-bi-report-catalog.md` — §7G catalog **validated** against GAAP (ASC 205/210/220/230)
   + Reg S-X Art 3 + management-pack practice, versioned `report://catalog/v1.0`.
4. `04-data-boundary-privacy.md` — intake allow-list per population + privacy-policy
   skeleton under Consent/Disclosure (GDPR/CPRA/EEOC).

## Spec update (v0.16 → v0.17)
Genuine findings only; URI cap and frozen ontology untouched (no new nouns). See
`notes/findings.md` (F1–F9) and Version/Review Log entry:
- **F1/G.9** — jsonschema ships no RFC3339 checker → validator enforces §2 timestamps.
- **F2** — added §7I.6 data boundary (aggregates-only default; GDPR Art9/EEOC
  protected-class ban; CPRA employee exemptions expired; DPIA+Consent to couple).
- **F6/G.17** — default resilient ingest set = GDELT + SEC EDGAR + regulatory RSS;
  licensed news/social deferred to Phase-B (Survey 1).
- **F7/H.6** — seeded filing calendar (federal + NM + ABQ) ships from Survey 2.
- **F8/G.8** — BI statutory core reference-grounded (ASC/Reg S-X), catalog versioned.
- Appendix F now points to the normative schema as superseding the starter seed.

## Verified output (ran this sprint)
- `./.venv/bin/python schema/build_schema.py` → WROTE schema JSON, 49 $defs.
- `./.venv/bin/python make_fixtures.py` → 20 interactions + 7l-loop + case-lifecycle (156
  objects) + statemachines + ledger.
- `./.venv/bin/python run_conformance.py` → **exit 0, ALL PASS** (C1–C5).
- SPEC.md re-verified: all 35 section headings intact after patching.

## Open issues / notes
- **Mirror not synced:** the `~/Documents/ai-relational-os-spec.md/.pdf` release mirror was
  left unchanged (optional step; the canonical spec is the project `SPEC.md`). Sync it if a
  release copy is wanted.
- Survey pricing is volatile as of 2026-09-01 (esp. X's Feb-2026 model change); re-verify at
  procurement time — noted in survey 1.
- The `.venv` (~20 MB) is local tooling for the validator; re-run via `artifacts/.venv/bin/
  python run_conformance.py`.
- `delegate_task`/subagents were NOT used (mandatory single-threaded rule honored).

## Hand-off
`/home/rlg/relational-os/sprints/sprint-1/PROMPT.md` written (S1 substrate + S2
Intent/Matching minimum) and echoed as this sprint's final message. Ready for a fresh
`/new` session to run Sprint 1 against the now-0.17 spec.