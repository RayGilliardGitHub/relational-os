# SPRINT 7 — SUMMARY — Company-branding component

**What was built:** every RelationalOS sector instance now carries a **company-branding
component** (the About-section / marketing / FAQ / design-language field set of real company
home pages) and renders it into generated reports, plus a per-instance `branding.md`
marketing artifact. No new subsystem, no new scheme, no schema change.

## How it's wired (data + a render, not a subsystem)
- **Data:** an additive **`brand` object on the company `org://` actor** — exactly the
  additive-envelope mechanism the frozen ontology already uses (Exception/Priority/
  Recommendation/capacity). The `Actor` `$def` is an `envelope`,
  `additionalProperties: true`, so brand validates under C2 and round-trips under C4 with
  **zero schema edits** and **no `brand://` noun**.
- **Config:** per-sector `brand` blocks in `instances/configs.py` (`BRANDS`, keyed by label),
  all 12 sector families incl. a uniform Financial (`finb`). Sector-appropriate prose,
  palettes, typography, logo, imagery, tone (Aero/Defense ≠ Media ≠ Pharma, etc.).
- **Builder (`instances/sector_scene.py`):** writes `cfg['brand']` onto the company org actor
  at provisioning; renders brand into the cockpit report (lead header **`Company — tagline`**
  + a **`## Brand` appendix**; `cockpit.json` now carries `brand`); emits `branding.md`.
- **Legacy Finance v1 (`instances/financial/`):** extended **self-contained** (own `BRAND`,
  header/appendix/`branding.md`, BI label line) so no report is left unbranded. The uniform
  Financial (`finb`) is the label-clean 12th builder config.
- **BI:** cockpit/BI identifies **who the report is for**; `financial/bi_snapshot.py` prints
  the label line.

## Verified commands — REAL output (all green)
```
cd /home/rlg/relational-os/instances
python3 build_all.py
  RESULT: ALL SECTORS PASS                                (12 uniform, exit 0)

(venv) conformance_all.py
  SECTOR CONFORMANCE: ALL SECTORS PASS                    (12 uniform, C1–C5, exit 0)

cd /home/rlg/relational-os/sprints/sprint-5/artifacts
python3 run_s5_demo.py               ->  RESULT: ALL PASS  (reference, exit 0)
(venv) run_s5_conformance.py         ->  RESULT: ALL PASS  (all-six, exit 0)

cd /home/rlg/relational-os/instances/financial
python3 run_fin.py                   ->  RESULT: ALL PASS  (v1, exit 0)
(venv) run_fin_conformance.py        ->  NORTHGLEN CONFORMANCE: ALL PASS (exit 0)
python3 bi_snapshot.py               ->  prints "^# Northglen Bank — Funding that lands on the date."
```
New `run_checks` gates (build_all): org actor carries additive brand · brand rendered in
cockpit (## Brand + header) · branding.md written — **all PASS** for all 12.

## Render (real, `instances/finb` financial cockpit + branding.md excerpt)
Cockpit lead header + Brand appendix (from `file:///home/rlg/relational-os/instances/finb/artifacts/reports/cockpit.md`):
```
# Northglen Bank — Funding that lands on the date.
generated 2026-09-01T00:28:36Z  |  ledger events 54  graph objects 80
...
## Brand (company identity carried on the org actor; additive field, §7J.11)
**Funding that lands on the date.**
**Mission**  Commit and settle funding tranches reliably and on time...
**Vision**   A commercial lending market where a committed tranche settling on time...
**Values**   - **Commitment is covenant** — A committed funding tranche is a promise to a date. ...
```
Other sector headers now read e.g. `# Valiant Aero — Subsystems on the line, on the date.`
Per-instance `artifacts/reports/branding.md` (About, Mission/Vision/Values, FAQ, Contact,
Design language) is written for all 13 instances (12 uniform + v1). `cockpit.json` carries
`brand` (tagline … design, incl. palette/typography/logo/imagery/tone).

## Design decisions
1. **brand:// stays OUT of the URI catalog** — documented explicitly (notes/findings.md).
   Brand is identity content, not an operating noun; it rode the additive field, holding the
   frozen ontology (§7J.11/§C16). No new scheme, no version bump.
2. **Financial via the uniform route** — added a Financial config (`finb`) so all 12 are built
   by the shared builder; the legacy v1 was ALSO branded self-contained (both carry Northglen).
3. **C2 RFC3339 probe avoided** — brand keys never end in the temporal-suffix probe
   (`at|time|deadline|expires|expiry|effective|due|since`); scripted check: NONE.

## Files changed
- `instances/configs.py` — `BRANDS` (12 sectors) + `finb` Financial config.
- `instances/sector_scene.py` — org-actor brand write, `write_branding`, cockpit header +
  `## Brand` appendix, brand in `cockpit.json`, brand checks.
- `instances/build_all.py` — calls `write_branding`.
- `instances/financial/fin_demo.py` + `bi_snapshot.py` — v1 brand (self-contained).
- Docs: `instances/README.md`, `sprints/sprint-6/artifacts/docs/00-README.md`,
  `01-system-manual.md` (new §5.1), `05-bi-reports.md`, `06-user-manual.md`, project `README.md`.
- This sprint: `plan.md`, `work/1-plan.md`, `notes/findings.md`, `summary.md`.

## Open issues
- None blocking. Fictional brand content (certifications, percentages, testimonials) is
  fiction-by-design and clearly labelled; mechanics/conformance are real and verified.

## Spec status
**SPEC.md stays v0.22.** Content/data/docs-only change; no normative spec edit, no bump.

## Hand-off
This was the branding **close-out**. No next-sprint prompt is required. The authoritative
index for the instances + brand component is `instances/README.md`; the build prompt is
`sprints/sprint-7/PROMPT.md`.