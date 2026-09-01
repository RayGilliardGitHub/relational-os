# Sprint 7 — Findings

Date: 2026-09-01. Company-branding component for the sector instances.

## Decisions taken
- **brand is an additive field on the company `org://` actor — NOT a new noun.** The
  `brand://` scheme was **deliberately kept OUT** of the URI catalog. Rationale: brand is
  identity content, not an operating noun; it behaves exactly like Exception/Priority/
  Recommendation/capacity (additive envelope field). Adding a scheme would risk the frozen
  ontology (§7J.11/§C16) for no modelling gain. This is an explicit, documented decision.
- **Financial family:** went the **uniform-12 route** the prompt preferred — added a Financial
  config to `configs.py` under a distinct label **`finb`** so `build_all` writes
  `instances/finb/` and never overwrites the legacy `instances/financial/` v1. The v1 was
  ALSO branded self-contained (`financial/fin_demo.py`), so no report is left unbranded.

## Assumptions verified (read-before-write confirmed safe)
- The schema `Actor` `$def` is `allOf [envelope]` (`additionalProperties: true`) in both the
  YAML (what conformance reads) and JSON → the additive `brand` object **validates under C2
  and round-trips under C4** with **zero schema changes**. Confirmed by green C1–C5 across
  all 12 uniform sectors + the v1.
- **C2 RFC3339 probe pitfall (avoided):** `_temporal_ok` recurses through *every* dict value
  and treats any string whose key ends in `at|time|deadline|expires|expiry|effective|due|since`
  as a timestamp. Brand keys were therefore chosen to **never end in those suffixes**
  (`founded`, `history`, `established`, `founded_year`) so the additive object is validated
  unchanged. Verified: no brand key matches the probe (scripted check).
- Brand data/section keys that end in `_since`/`_at` (e.g. `established_at`) MUST be avoided
  in this project's additive content, or the C2 RFC3339 probe will demand a timestamp.

## Build mechanics that explain the result
- `build_all.py` now writes 12 uniform instances (11 + `finb`) and `sector_scene.write_branding`
  emits `branding.md`; `run_checks` gained brand checks (org actor carries brand, cockpit
  appendix + JSON, branding.md exists) — all PASS.
- Reference `ros/` chain and schema are **untouched**; the reference demo + all-six conformance
  stay ALL PASS. Brand rides the sector instances only.
- The legacy `financial/` v1 is fully self-contained (its own `BRAND`, header/appendix/
  branding.md, BI label line) and remains ALL PASS.

## Open items / honest limits
- This is the fictional company brand deliverable itself; it carries the platform's "verified
  delivery" narrative but the companies are invented. Certifications, percentages, and
  testimonial quotes are **sector-appropriate fabricated content** (fiction by design), not
  claims about real firms.
- `brand://` is intentionally absent; revisit only if a genuine un-branded operating use
  emerges (today none exists).

## Spec impact
**None normative.** SPEC stays **v0.22**. No version bump, no ontology change, no new scheme.
Documentation rolled forward in `instances/README.md`, docs 00/01/05/06, project README.