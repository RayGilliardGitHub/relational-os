# SPRINT 7 — PROMPT  (Company branding component: About · marketing · FAQ · design language)

You are Hermes Agent in a **fresh session** with **NO memory** of prior conversation. Rely
ONLY on the files named here. Read before acting; do not guess or invent. **Every command
you document MUST be run and its real output captured** — never fabricate. This sprint adds
a **company-branding component** to the RelationalOS sector instances (the multi-family
provisioned under `instances/`), so that a generated **cockpit/report carries brand
information** — the kind of content on a company's website About section and marketing
surface.

## Context — read first, in full
- Canonical spec (the contract): `/home/rlg/relational-os/SPEC.md` (v0.22)
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md`
- Project README/layout: `/home/rlg/relational-os/README.md`
- Documentation package (Sprints 6: the manuals): `/home/rlg/relational-os/sprints/sprint-6/artifacts/docs/`
  (read `00-README.md` for reading order; `02-setup`, `03-run`, `04-audit`, `05-bi-reports`, `06-user-manual`)
- **The instances to brand (the working system you extend):** `/home/rlg/relational-os/instances/`
  - `instances/README.md` — the 12 sector instances (Financial v1 + 11 label-clean sectors),
    the reusable builder `instances/sector_scene.py`, and configs `instances/configs.py`.
  - `instances/build_all.py` (build+verify every sector, plain python3),
    `instances/conformance_all.py` (C1–C5 per sector, Sprint-0 venv interpreter).
- Closing hand-off: `/home/rlg/relational-os/sprints/COMPLETE.md`

## What Sprint 7 IS and is NOT
- **IS:** a **branding/content component** that gives every sector instance a company
  identity for a website About section + marketing materials + FAQ + **design language**
  (colors, typography, logo/brand character, tone, imagery), and makes **generated
  reports bring that brand with them** (cockpit header + brand appendix; the BI snapshot
  label line). It is grounded in the **common features of real company home pages** the
  prior session observed (findings below). It works by extending the existing CONFIG
  (`configs.py`) and the BUILDER (`sector_scene.py`) so the brand is data + a render,
  not a new subsystem.
- **IS NOT:** a new service, new schema, new URI noun, or a re-implementation of the
  S1→S5/BOL logic. **Do NOT change the frozen ontology or URI cap** (§7J.11/§C16). **Do
  NOT modify the platform `git`-free reference** when avoidable — the brand must ride, NOT
  disturb, the verified chain.
- Honour the URI cap: brand identity is an **additive field** on the company `org://` actor
  (the Actor `$def` is an `envelope` / `additionalProperties`), exactly like Exception/
  Priority/Recommendation/capacity — **not** a new `brand://` scheme. If you believe a
  `brand://` noun is genuinely warranted, make it an explicit, additive, documented
  decision in `notes/findings.md` — do NOT add it silently.

## Research the prior session did (source of "the most common features")
The prior session opened **real company home/About pages across sector families** with a
browser and extracted the shared elements: **Salesforce** (Technology), **JPMorganChase**
(Financial), **UnitedHealth Group** (Healthcare), **Target** (Retail). The recurring,
cross-sector set is:

1. **Logo + wordmark (+ optional brand character/mascot)** — e.g. Target's "Bullseye"; a
   min-space / usage rule.
2. **Primary navigation** — `About · News/Newsroom · Careers · Investors · Press ·
   Sustainability & Governance · Contact` (+ Search).
3. **Hero tagline + mission** — the H1 promise (Target: "We're here to help all families
   discover the joy of everyday life."; Salesforce's mission-from-1999).
4. **Purpose / History / milestones** — founders, timeline, key dates (Salesforce
   "A history of firsts"; Target "Purpose & History").
5. **Vision + Values, each with a one-liner** (Salesforce: Trust, Customer Success,
   Innovation, Equality, Sustainability).
6. **Leadership & Team** — executives with bios (Target "Leadership & Team").
7. **Products & Services / "what we do" / industries served.**
8. **Customer stories / testimonials / social proof** (Salesforce customer tabs).
9. **Trust signals** — rankings/awards/certifications with a source (Salesforce "#1",
   IDC-cited); awards & recognition.
10. **Fast facts / company-at-a-glance** — revenue, stores, employees, footprint
    (Target "Fast facts", "locations at a glance").
11. **Locations / footprint.**
12. **FAQ / Contact & Help** — "Questions? We'll put you on the right path."
13. **Careers** — value proposition ("Work somewhere you love").
14. **Investor relations / financials.**
15. **Press / Newsroom / news-alert signup.**
16. **Philanthropy / Sustainability / ESG / Foundation / community giving**
    (Target 5%-of-profits; Salesforce 1-1-1/Pledge 1%).
17. **Footer**: legal (Privacy, Terms, State/CA rights, Do-Not-Sell, Health Privacy),
    © year + trademark notices, social-media links, newsletter signup, site map.
18. **Cookie-consent / preference banner** — "Accept All / Reject All / Do Not Share or
    Sell" + link to Privacy Policy (JPMorgan, UnitedHealth).
19. **Design language** — brand color palette, typography/hierarchy, logo usage, imagery
    style/mood, tone of voice.
20. **Ambient**: search, region/language selector, site-feedback survey.

Use this set as the target field list for the brand component. You may do **additional
verified research** (browser/web) for sector-appropriate phrasing, but every feature you
ship must trace to the list above or be a clearly-labelled, common-sense extension.

## Task
Under `/home/rlg/relational-os/instances/`, extend the framework so every sector instance
carries and renders a **brand component**, then add brand content for the 12 instances.

1. **Spec the brand shape (write first, per PROTOCOL plan-then-build):**
   - `<sprint>/plan.md` FIRST, then a `<sprint>/work/` plan before drafting code/content.
   - The brand block as **additive `brand` fields on the company `org://` actor** (schema-
     safe in `$def Actor`). Define the fields (the 20-feature set above, sector-applicable),
     e.g. a `brand` object: `tagline, mission, vision, values[], about, fast_facts[],
     history[], leadership[], products_services[], testimonials[], trust[], locations,
     faq[], contact, careers, investors, press, esg, legal, nav[], cookie_consent,
     design{palette[], typography, logo{}, imagery, tone}`.
2. **Extend `instances/configs.py`:** add a `brand` section to each of the 11 configs
   (Technology, Healthcare/Pharma, Food/Bev/Consumer, Retail, Energy/Chemicals,
   Aerospace/Defense/Aviation, Telecom, Automotive, Media, Logistics/Transport, Industrial)
   with **real, sector-appropriate prose and tokens** (design palettes/fonts/logo per
   sector family — e.g. an Aero/Defense brand vs a Media brand differ). Also add a brand
   for the **Financial** instance — if you extend `instances/financial/fin_demo.py`
   (v1), keep it self-contained; otherwise add Financial to `configs.py` so all 12 are
   uniform. Prefer **uniform 12 via `configs.py` + `sector_scene.py`** unless doing so
   breaks the existing v1 Financial; the PRIORITY is that **every generated report for
   every instance carries brand**.
3. **Extend `instances/sector_scene.py`:** when provisioning, write the `brand` as an
   additive field on the company `org://` actor (and emit a per-instance **`branding.md`**
   marketing artifact: About, Mission/Vision/Values, FAQ, Contact, Design language — the
   "website About section in prose"). Render the brand into the **cockpit report**
   (`reports/cockpit.md` / `.json`): lead header = `Company — tagline` + a `## Brand`
   appendix (about, mission, values, products, FAQ, contact, design language) where present.
   Reference the brand in the **BI snapshot** label line (company + tagline), per
   `05-bi-reports.md`.
4. **Conformance/verification (mandatory, real output):** after adding the `brand`
   additive field to org actors, re-run:
   - `cd /home/rlg/relational-os/instances && python3 build_all.py` → **ALL SECTORS PASS**, exit 0.
   - `cd /home/rlg/relational-os/instances && /home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python conformance_all.py` → **ALL SECTORS PASS**, exit 0 (C1–C5; the additive `brand` must not break C2/C4).
   - The reference must not regress: `cd /home/rlg/relational-os/sprints/sprint-5/artifacts && python3 run_s5_demo.py` → ALL PASS, and `…/.venv/bin/python run_s5_conformance.py` → ALL PASS.
   - The Financial attempt must stay ALL PASS if you touched `instances/financial/`.
   - Show a **cockpit with the brand header + Brand appendix** and the **branding.md** artifact verbatim in your summary.
5. **Update the documentation (roll-forward, non-negotiable):**
   - `instances/README.md` — document the brand component (fields, where it lives, that
     reports carry it), and the per-instance `branding.md`.
   - `sprints/sprint-6/artifacts/docs/00-README.md` — add a short "Branding component
     (Sprint 7)" note.
   - `sprints/sprint-6/artifacts/docs/01-system-manual.md` — add a short subsection on the
     brand component (data model: additive `brand` on the org actor; rendering into reports).
   - `sprints/sprint-6/artifacts/docs/05-bi-reports.md` and `06-user-manual.md` — note that
     the cockpit/BI reports carry the company brand (who the report is for).
   - `/home/rlg/relational-os/README.md` — keep the Documentation section pointing at these.
   - Do NOT bump the spec version for a content/data/docs change; keep **v0.22**. Only a
     genuine normative change to `SPEC.md` would justify a minor bump (log it then).

## Mandatory rules
- **Real tool output only.** Run every command you document; embed real output. Never
  fabricate content, prose, citations, or brand claims. Brand content you invent for the
  fictional companies is the deliverable (it is fiction by design) — but the *mechanics*
  (commands, conformance results) must be real and verified.
- **URI cap / frozen ontology:** brand is an **additive field**, never a new noun/scheme.
- **Do not disturb the verified chain:** the brand must ride on the org actor and renders,
  not alter the shared schema/`ros/` logic or the S1→S5/BOL semantics. If a `ros/` change
  is genuinely required, make it a targeted, backward-compatible fix and re-verify the
  full reference conformance — else avoid it.
- **Single-threaded** per PROTOCOL: all work in ONE sequential process; NO `delegate_task`/
  subagents.
- **Budget:** ~$10/mo cap; local computation, no frontier-API spend; write sector-appropriate
  brand prose yourself (no external AI spend).
- **Raymond:** clean English, `file://` absolute paths, honest "stuck/failed" over fabricated
  success, report status at each long step.

## Definition of Done (exit criteria)
- `sprints/sprint-7/plan.md` written FIRST; a `work/` plan before drafting code/content.
- `instances/configs.py` carries a `brand` for **every sector family** (all 12, incl.
  Financial — either in `configs.py` or the Financial v1 in a uniform way).
- `instances/sector_scene.py` writes the additive `brand` onto the company `org://` actor,
  emits a per-instance **`branding.md`** marketing artifact, and renders brand into the
  **cockpit reports** (header + `## Brand` appendix) + BI snapshot label line.
- `build_all.py` → **ALL SECTORS PASS** (exit 0) and `conformance_all.py` → **ALL SECTORS
  PASS** (exit 0), real outputs captured.
- Reference (Sprint-5 demo + all-six conformance) still **ALL PASS**; Financial (if touched)
  still ALL PASS.
- Documentation rolled forward per task 5 (instances README, docs index/system-manual/
  bi-reports/user-manual, project README).
- `sprints/sprint-7/summary.md` written: what was built, the verified commands/output, a
  rendered cockpit brand header/Brand-appendix snippet and `branding.md` excerpt, and the
  design decisions (incl. whether `brand://` stays out of the URI catalog).
- SPEC stays **v0.22** unless a genuine normative correction (then bump + Version/Review Log).

## Hand-off requirement
Your **final message** must summarize the brand component (what was added, where it lives,
the verified build/conformance commands with real results, the rendered brand-in-report
output) and point to `sprints/sprint-7/summary.md` and the package index
`instances/README.md` (absolute paths). No next-sprint prompt is required — this is the
project's branding close-out.