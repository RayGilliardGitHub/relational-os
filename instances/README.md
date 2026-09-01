# RelationalOS — Sector Instances (multi-sector dogfood)

Working, **conformance-validated** instances of the platform for a company in every
sector family of SPEC Appendix B. Each one runs the full S1→S5 chain + Business Operating
Layer (exception → case → task → verified outcome → learning), produces its own cockpit
with the §7L ten answers answered with evidence, emits its fixtures/ledger/graph, and
passes the Sprint-0 conformance audits (C1–C5, exit 0).

The operating loop is identical across sectors; **only the domain vocabulary differs**
(company, counterparties, outcome class, trust claim, URIs, prose). That is the platform
generalizing: the on-time-exception loop is the product, and any sector is a config.

## The instances

| Sector family (Appendix B) | Label | Company (fictional) | Outcome class | Status |
|---|---|---|---|---|
| **Financials** (v1) | `financial` | Northglen Bank | committed funding tranche | ✅ (see `financial/`) |
| **Financials** (uniform, Sprint 7) | `finb` | Northglen Bank | committed funding tranche | ✅ (built via `configs.py`) |
| Technology | `tech` | VantageCloud | platform-upgrade deployment | ✅ |
| Healthcare / Pharma | `hlth` | Lumen Health | pharmaceutical delivery | ✅ |
| Food / Bev / Consumer | `food` | Maplehurst Foods | retail restock shipment | ✅ |
| Retail | `retail` | HardVale Stores | store replenishment delivery | ✅ |
| Energy / Chemicals | `enrg` | Basinline Energy | refined-products tanker delivery | ✅ |
| Aerospace / Defense / Aviation | `aero` | Valiant Aero | airframe-subsystem delivery | ✅ |
| Telecom | `telco` | NimbusCom | cell-site buildout | ✅ |
| Automotive | `auto` | Forge Auto | OEM part-lot delivery | ✅ |
| Media | `media` | Hollow Media | content-delivery campaign | ✅ |
| Logistics / Transport | `logi` | Hawkline Logistics | freight-dispatch settlement | ✅ |
| Industrial | `indu` | FerrousWorks | machinery parts delivery | ✅ |

Each non-financial instance lives at `instances/<label>/` with `artifacts/`
(`fixtures/ledger/ledger.json`, `graph/current-state.json`, `reports/cockpit.md|.json`,
per-kind fixture groups) plus the files that generated it.

## How the instances were provisioned (following the documentation)

Followed the Sprint-6 manuals (`sprints/sprint-6/artifacts/docs/`): the demos/cockpit run
with plain `python3`; every **conformance** run uses the Sprint-0 venv interpreter; the
audit (04-audit) is conformance C1–C5 + `Ledger.verify()` + the full-state round-trip; the
BI (05-bi) is the ledger projections. One reusable builder (`sector_scene.py`) drives all
sectors from a config (`configs.py`), rather than a bespoke scene per sector.

    cd /home/rlg/relational-os/instances
    python3 build_all.py                                   # build + verify every sector; exit 0 = ALL
    /home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python conformance_all.py   # C1-C5 per sector; exit 0
    # per-sector BI:  python3 bi_snapshot.py  (in that sector's dir, over its emitted ledger)

## Verified results (exit 0, all sectors)

- **Build + checks:** `build_all.py` → **ALL SECTORS PASS**. Each: ledger hash-chain OK,
  full-state round-trip (Graph rebuilds from Ledger), Trust flywheel (good counterparty >
  laggard), §6 floor order in the ledger (escalate < human < release), case lifecycle
  OPEN→…→CLOSED, learning + policy v3, cockpit written. (54 ledger events / 80 graph
  objects per sector.)
- **Conformance:** `conformance_all.py` → **ALL SECTORS PASS**, exit 0; C1 (49 `$defs`),
  C2 (67 instances/schemes/RFC3339 each), C3 (ledger content-addressed + signed), C4
  (round-trip preserve-unknown), C5 (state machines).
- **BI (per sector):** on-time 2/4 = 0.500, settled value USD 7,600,000, good-partner
  Trust → 0.79, laggard Trust → 0.14.

## What multi-sector provisioning found and fixed (code + spec)

1. **Code defect (fixed):** the reference `ros/bol.py`, `ros/s4.py`, `ros/s5.py` services
   **hardcoded a construction org/path segment (`qk`)** in the URIs they build, which
   leaked into any non-construction instance (visible in the Finance v1 instance). Fixed
   by parameterizing a `label` segment (default `'qk'`), preserving the reference build
   byte-for-byte (Sprint-0..5 demo + all-six conformance re-verify ALL PASS). New sector
   instances emit clean per-sector URIs — verified: **no `qk` URIs in any sector fixture**.
2. **Scene-level S1/S2/S3 note:** the reference S1 role/authz and S2 matching are generic
   (reused directly); the reference **S3 orchestration is a construction-scene service**
   (hardcoded roofing actions/fleet), so sector instances drive the §6 human floor at the
   BOL surface (signed escalation + owner decision + ACTION) — the documented operating
   layer — rather than S3's construction scene. `ros/checks.py` stays the Quoteko reference
   test suite.
3. **Spec Version/Review Log:** a dated v0.22 entry records the code hardening and the
   12-family validation; the **URI cap and frozen ontology are unchanged** (no new nouns).

## Files
- `sector_scene.py` — reusable config-driven instance builder (S1→S5 + BOL + cockpit + emit).
- `configs.py` — one config per sector family (domain vocabulary).
- `build_all.py` — build + verify every sector (plain python3).
- `conformance_all.py` — C1–C5 over every sector's fixtures (Sprint-0 venv).
- `financial/` — the Finance v1 instance (built before the label fix; its README notes the
  `qk`-label artifact). All other sectors are label-clean.
- `<label>/artifacts/…` — each sector's fixtures, graph, ledger, and cockpit report.

Cross-references: manuals `sprints/sprint-6/artifacts/docs/`; spec `SPEC.md` (v0.22);
platform hand-off `sprints/COMPLETE.md`.

## Branding component (Sprint 7)

Each instance now carries a **company-branding component** — the About/marketing/FAQ/design
language set common to real company home pages (tagline, mission/vision/values, about,
history, leadership, products, testimonials, trust signals, fast facts, locations, FAQ,
contact, careers, investors, press, ESG/philanthropy, legal footer, nav, cookie consent,
and a `design{palette, typography, logo, imagery, tone}` block).

- **Where it lives:** an **additive `brand` field on the company `org://` actor** — exactly
  like Exception/Priority/Recommendation/capacity. The **URI cap and frozen ontology hold**;
  there is **no new `brand://` noun/scheme.** It is schema-safe by construction (`Actor` is an
  `envelope`, `additionalProperties: true`), so C1–C5 conformance is unchanged.
- **Data:** a `brand` block per sector family in `instances/configs.py` (`BRANDS`, keyed by
  label) — sector-appropriate prose, palettes, typography, logo, imagery, tone (e.g. the
  Aero/Defense brand differs from the Media brand). Both the uniform Financial (`finb`) and
  the legacy v1 Financial (`financial/`) carry a Northglen brand.
- **Builder:** `sector_scene.py` writes `cfg['brand']` onto the company org actor at
  provisioning, renders it into the **cockpit report** (lead header `Company — tagline` plus
  a `## Brand` appendix; `cockpit.json` carries `brand`), and writes a per-instance
  **`branding.md`** marketing artifact (About, Mission/Vision/Values, FAQ, Contact, Design
  language) under `<label>/artifacts/reports/`.
- **BI:** the cockpit/BI report header identifies **who the report is for** (the branded
  company), and the Financial v1 `bi_snapshot.py` prints the brand label line
  (`Northglen Bank — Funding that lands on the date.`).
- **Implementation notes (v1 self-contained):** the legacy `financial/fin_demo.py` carries its
  own `BRAND` and renders the same header/appendix/branding.md, keeping the v1 self-contained
  (no dependency on `configs.py`/`sector_scene.py`).

**Verified (exit 0):** `build_all.py` → ALL SECTORS PASS (now 13 builds: 11 + `finb` + the
v1 under `financial/`); `conformance_all.py` → ALL SECTORS PASS (C1–C5 per sector);
`financial/run_fin.py` + `run_fin_conformance.py` → ALL PASS; `financial/bi_snapshot.py`
prints the brand label line. Sector cockpit headers now read e.g.
`# Valiant Aero — Subsystems on the line, on the date.` and each cockpit + branding.md
carries the brand. Self-contained build prompt: `sprints/sprint-7/PROMPT.md`.