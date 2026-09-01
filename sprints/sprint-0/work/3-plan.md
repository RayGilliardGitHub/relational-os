# SUB-SPRINT 0.3 — PLAN — The four committed surveys

**Mandate:** SPEC §7D-E and §8 make these four surveys **gating** Sprint-0 deliverables —
written reports with real citations and explicit Definitions of Done. This is real
research: use `web_search`/`web_extract`, cite sources, never invent. Batch searches to
respect the ~$10/mo cap.

| # | Survey | Section | DoD | File |
|---|--------|---------|-----|------|
| 1 | Data-source & licensing | §7I | ranked source matrix: cost / ToS / rate-limit per source + default ingestion set | `surveys/01-data-licensing.md` |
| 2 | Jurisdiction & tax-filing | §7H | verified filing-calendar seed per target jurisdiction + vendor list | `surveys/02-jurisdiction-tax.md` |
| 3 | BI report-catalog validation | §7G | validated, versioned report catalog vs authoritative references | `surveys/03-bi-report-catalog.md` |
| 4 | Employee/customer data boundary | §7I/§7B | intake allow-list + privacy-policy skeleton under Consent/Disclosure | `surveys/04-data-boundary-privacy.md` |

**Target jurisdiction for survey 2 seed:** US federal (IRS) + New Mexico (state) + ABQ
(city/local), representative of Raymond's home jurisdiction; noted as a seed, extensible.

## Method
- Each survey: web_search for authoritative sources → web_extract the key pages → distill
  into a cited table/report. Batch multiple searches per call.
- Mark the provenance of each figure (source + date + caution where volatile).
- Every claim either cites the survey reference list or is labeled reasoning (LEVEL B).

## Definition of Done
- Four `.md` reports exist under `artifacts/surveys/`, each with a references list and
  an explicit DoD-satisfying finding (matrix / calendar / catalog / allow-list+skeleton).