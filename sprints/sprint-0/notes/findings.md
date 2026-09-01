# Sprint 0 — Findings Log

Appended as discoveries surface during the build. Each entry: date, finding, and the
spec-update decision (patch / note-only / no-change). Findings drive SPEC.md updates in
step 5 of the protocol — the spec is changed ONLY where a genuine build finding requires it.

## 2026-09-01 — F1: RFC3339 is NOT enforced by `jsonschema`
During 0.1 schema self-test, a string `"not-a-time"` passed `format: date-time` even with
`FormatChecker` enabled: the jsonschema library intentionally ships NO `date-time` checker
(same for `uri`). Since §2 makes RFC3339 normative, conformance cannot rely on the library.
**Decision:** the schema keeps `format: date-time` as documentation; the conformance
validator (`conformance.py`) enforces RFC3339 with its own regex + range check across all
temporal fields. **Spec action:** none needed in §2 (already normative); note in Appendix G.9
that the validator is responsible for RFC3339 conformance, not the schema library.

## 2026-09-01 — F2: Appendix C2 record schemes were missing from the fixture-run catalog
The C2 `patient_record://`/`student_record://`/`supplier_profile://`/`credit_profile://`
schemes (records are domain objects, distinct from the person) were named in prose but
absent from the schema's machine catalog, so a valid `student_record://e10/rec` fixture
failed membership. **Decision:** added the four record schemes to the schema's
`x-uri-catalog`. Additive-only, per Appendix C. **Spec action:** none — the catalog now
matches Appendix C prose.

## 2026-09-01 — F3: `delegation://` scope must be rule URIs, not free text
Appendix F types `Delegation.scope` as `rule://*`. The validator's URI pattern correctly
rejected a plain-text scope string. **Decision:** fixtures now pass `rule://` references;
a scope is a pointer to the bounding rule(s), the rule object carries the text. Faithful
to §3.4 (delegation is bounded authority). **Spec action:** none — Appendix F already
types it `rule://*`; this is the validator enforcing an existing contract.

## 2026-09-01 — F4: `policy://` collision confirmed in classification
The Appendix C collision rule (first path segment disambiguates same-scheme classes) is
exercised by `policy://ins/…` (insurance policy — domain object) vs `policy://`
(executable compliance Policy). The first fixture run wrongly classified `policy://ins/`
as an executable Policy. **Decision:** `conformance.py` now checks the `policy://ins/`
prefix before the generic scheme map. **Spec action:** none — the rule was already
documented; this is its first machine enforcement.

## 2026-09-01 — F5: Case REOPEN must re-enter the workflow, not jump to RESOLVED
An OPEN→RESOLVED transition on reopen is not legal under §7J.3 (a reopened case
re-enters triage/assignment). The fixture was corrected to `CLOSED→OPEN→TRIAGE→ASSIGNED
→IN_PROGRESS→RESOLVED→CLOSED`. **Spec action:** none — §7J.3 already implies re-workflow;
the state machine simply does not allow the skip.

## 2026-09-01 — F6…F9: survey findings applied to SPEC (genuine, grounded)
- **F6 — Survey 1 (§7I data/licensing):** of §7I.1's named sources only GDELT + SEC EDGAR
  + regulatory RSS + the business's own OAuth channels are commercially ingestible at the
  ~$10/mo cap; X (pay-per-use, no new free tier), LinkedIn (scraping banned), TikTok
  Research (academic-only), Reddit (enterprise/opaque), review platforms (paid aggregator/
  license) are NOT free-commercial. **Applied → Appendix G.17:** default resilient ingest
  set = GDELT + EDGAR + RSS; licensed news/social deferred to Phase-B.
- **F7 — Survey 2 (§7H jurisdiction):** seed calendar verified — federal (941/940/720/
  1120-S/1065/1040/1099/W-2/ACA 1095-C/1094-C, e-file mandates), NM (CIT-1 due 15th of
  3rd month after close; $50 franchise; GRT), ABQ (local-option GRT, no city income tax);
  Sec. of State annual report ≈ anniversary+30 days. **Applied → §7H.6:** seeded calendar
  ships from survey 2; other jurisdictions Phase-B.
- **F8 — Survey 3 (§7G BI):** §7G's three core statements map exactly to GAAP (ASC
  205/210/220/230) + Reg S-X Art 3 — validated, no missing/spurious statutory report.
  **Applied → §7G.8:** statutory core reference-grounded; catalog versioned `report://
  catalog/vN`; recognition subtlety needs an accountant (architecture ≠ substitute).
- **F9 — Survey 4 (§7I/§7B data boundary):** CPRA employee exemptions expired 2023-01-01;
  GDPR Art 9 bans sensitive-sentiment categories for this purpose; EEOC adds
  protected-class discrimination risk. **Applied → §7I.6 and Appendix G.17:** aggregates/
  de-identified counts by default; Glassdoor = sensitive employee data; never infer a
  protected class; coupling requires purpose-limited DPIA + Consent.