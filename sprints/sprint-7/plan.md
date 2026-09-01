# SPRINT 7 — PLAN — Company-branding component for the sector instances

**Objective:** give every RelationalOS sector instance a **company-branding component**
(About / marketing / FAQ / design language — the field set of real company home pages),
carried as **additive `brand` fields on the company `org://` actor**, and make every
generated **cockpit/BI report carry the brand** plus a per-instance **`branding.md`**
marketing artifact. The URI cap and frozen ontology hold: brand is a field, not a noun.

**Contract read (in full, real files):** `SPEC.md` v0.22 (normalize changes only — no bump),
`PROTOCOL.md`, `instances/README.md`, `instances/sector_scene.py`, `instances/configs.py`,
`instances/build_all.py`, `instances/conformance_all.py`, the Sprint-6 docs package
(`00-README`, `01-system-manual`, `05-bi-reports`, `06-user-manual`), `instances/financial/*`.
BASELINE VERIFIED green: `build_all.py` → ALL SECTORS PASS (11), exit 0.

**Key structural facts confirmed:**
- The schema's `Actor` `$def` is `allOf [envelope]` with `additionalProperties: true`
  (JSON + YAML) → an additive `brand` object validates (C2) and round-trips (C4). No
  schema change needed.
- The company org actor is provisioned in `sector_scene.build_scene` (`{"uri": BANK, "type":
  "ORG", "identity": {...}}`) and in `financial/fin_demo.py` (`BANK` actor). Adding a
  `brand` key there is purely additive.
- C2's RFC3339 probe recurses over dict keys *ending in* `at|time|deadline|expires|expiry|
  effective|due|since`. **Brand keys must not end in those suffixes** (I use `founded`,
  `established`, `founded_year`, etc. — verified safe).
- `conformance_all.py` iterates `configs.SECTORS`; `build_all.py` writes to `HERE/<label>`.
  The legacy `instances/financial/` dir is NOT a `SECTORS` entry and must stay untouched.

## Decisions
1. **Financial — uniform-12 route** (prompt's stated preference): add a Financial config to
   `configs.py` under a **distinct label `finb`** (so `build_all` writes `instances/finb/`,
   never overwriting the legacy `instances/financial/` v1). All 12 uniform through
   `configs.py` + `sector_scene.py`.
2. **Legacy v1 financial stays ALL PASS and gets branded too:** extend `financial/fin_demo.py`
   with a self-contained brand block (org actor, `branding.md`, cockpit Brand appendix, BI
   label line) and re-verify `run_fin.py` + `run_fin_conformance.py` ALL PASS so *no* report
   is left unbranded.
3. **Brand block** (JSON-safe, additive on `org://` company actor): `tagline, mission,
   vision, values[], about, fast_facts[], history[], leadership[], products_services[],
   testimonials[], trust[], locations, faq[], contact, careers, investors, press, esg, legal,
   nav[], cookie_consent, design{palette[], typography{heading,body}, logo{}, imagery,
   tone}`. `brand://` stays OUT of the URI catalog (documented in findings).
4. **Cockpit render:** lead header becomes `# Company — tagline …` and a `## Brand` appendix
   renders where brand present; cockpit.json carries `brand`.
5. **Per-instance `branding.md`** marketing artifact written by the builder.
6. **SPEC stays v0.22** (content/data/docs change only). Docs rolled forward (instances
   README, docs 00/01/05/06, project README) as pure additions.

## Numbered sub-sprints
1. **Write-first planning** — `plan.md` + a `work/1-plan.md` before code (this file + next).
2. **Brand data** — add brand blocks for all 12 sector families to `configs.py`
   (incl. Financial, label `finb`); sector-appropriate prose, palettes, typography, logo/tone.
3. **Builder** — extend `sector_scene.py`: write `brand` onto the company `org://` actor,
   write per-instance `branding.md`, render brand into `write_cockpit` (header + `## Brand`
   appendix) + cockpit.json.
4. **Build + conformance** — `build_all.py` → ALL 12 PASS; `conformance_all.py` → ALL PASS
   (C1–C5). `build_all.py` exit 0, conformance exit 0.
5. **Brand the legacy v1** — `financial/fin_demo.py` + `financial/bi_snapshot.py`: brand
   block, branding.md, cockpit appendix, BI label; `run_fin.py` ALL PASS + conformance ALL PASS.
6. **Reference must not regress** — `run_s5_demo.py` ALL PASS; `run_s5_conformance.py` ALL PASS.
7. **Docs roll-forward** — instances/README, docs 00/01/05/06, project README.
8. **Capture findings + summary + hand-off** — `notes/findings.md`, `summary.md`,
   `sprints/README` update; SPEC stays v0.22.

## Definition of Done (exit criteria)
- `configs.py` carries a `brand` for all 12 sector families incl. Financial (uniform via
  `finb`); Financial v1 also branded self-contained.
- `sector_scene.py` writes additive `brand` onto the `org://` actor, emits per-instance
  `branding.md`, renders brand into cockpit header + `## Brand` appendix + cockpit.json.
- `build_all.py` → ALL SECTORS PASS (exit 0); `conformance_all.py` → ALL SECTORS PASS (exit 0).
- Reference (`run_s5_demo.py` + `run_s5_conformance.py`) still ALL PASS; Financial v1
  (`run_fin.py` + `run_fin_conformance.py`) still ALL PASS.
- Docs rolled forward; `notes/findings.md`, `summary.md` written; SPEC stays v0.22.
- Final message embeds a rendered cockpit brand header + `## Brand` appendix + `branding.md`
  excerpt + the verified command outputs (all real).

## Exit criteria
As above — every command's real output captured and embedded; no fabricated content.
Fictional brand prose is the deliverable; mechanics/conformance/commands are verified.