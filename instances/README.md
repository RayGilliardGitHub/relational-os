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

## Contested-reality / conflicting-interest extension (Sprints 9–10)

Beyond the happy-path sectors, `instances/contested_reality/` is the contested-human-reality
engine — the check on whether the word *relational* is earned off the happy path.

- **Sprint 9 — disputed fact:** `run_dispute_demo.py` + `conformance_dispute.py` carry two
  conflicting claims × evidence through conflict detection → disputed state → adjudication →
  determination, and — **inviolably — may conclude UNRESOLVED / insufficient-evidence**,
  staying Trust-safe (only an adequately-evidenced determination advances Trust). Fact /
  Claim / Determination are distinct objects. Docs: `contested_reality/docs/CONTESTED-REALITY-EXPERIMENT.md`.
- **Sprint 10 — conflicting interest (remote-work, Scenario B):** `run_interest_conflict_demo.py`
  + `conformance_interest.py` model two parties with **legitimate, conflicting interests under a
  shared constraint** — employee wants full remote + use unused leave; manager needs on-site
  coverage to meet a 30-minute customer-response SLA with a 3-agent staffing floor; company policy
  permits remote under conditions. It demonstrates: two interest objects with explicit stakes,
  the shared SLA/staffing/policy constraint binding both, deterministic conflict detection under
  the constraint, an OPEN `case://` with the conflict + recorded uncertainty, a **defensible
  determination** that is a conditional middle option (`remote-with-coverage-plan`) while keeping
  **UNRESOLVED** reachable (insufficient admissible basis), and a **first-class, signed appeal**
  (native `right://` type=APPEAL) re-adjudicated by a higher authority — not a silent redo.
  Everything is additive on existing primitives (`case://`, `relationship://`, `decision://`,
  `expectation://`, `policy://`, `right://`, `authority://`); NO new noun, NO schema edit,
  49 `$defs` intact, SPEC stays v0.22.
- **Sprint 11 — the optimizer / business-model (what "better" means):**
  `instances/contested_reality/tradeoff_model.py` + `run_tradeoff_demo.py` +
  `conformance_tradeoff.py` compute a **defensible ranking of the adjudication options**
  (side-employee / side-manager / remote-with-coverage-plan / do-nothing/UNRESOLVED) from the
  org's OWN recorded constraints (SLA target, staffing floor, leave balance, policy satisfaction,
  costs, evidence confidence) — the §7K.1 "trade-off / decision analysis" and the closing of
  Scenario-B gap#3. A documented weighted utility model ranks the options; **do-nothing/UNRESOLVED
  is always an explicit baseline** (it is never worse than breaching the customer SLA); the human
  adjudicator determines WITH the computed ranking in view. An unknown-cost coverage variant shows
  the **§6 human floor** gating every staff-changing option → human authorizes **UNRESOLVED**
  (Trust untouched). An optional **real local model advisory** (Sprint-8 `agent_adapter`) is proven
  contained — it cannot set the determination or Trust. The trade-off rides the case as an
  **additive object in the frozen `Recommendation` $def shape** (incl. a machine-readable `json`
  ranking); NO new noun / `recommendation://` scheme, 49 `$defs` intact, SPEC v0.22.
  Docs: `contested_reality/docs/TRADE-OFF-IMPLEMENTATION.md`.
- **Sprint 12 — the consolidated contested-reality lifecycle (the "does it understand disagreement?"
  proof):** `instances/contested_reality/run_full_dispute.py` + `conformance_lifecycle.py` walk ONE
  financial/customer dispute ($18,000, delivery) through the ENTIRE lifecycle over real signed ledger
  events: claims → conflicting evidence (GPS/contract/receipt/supplier) → conflict detection →
  uncertainty → epistemic status → interests/obligations/constraints → options (incl. do-nothing +
  settlement) → constrained trade-off → contained real-AI advisory → authorized human determination →
  verified outcome → learning → appeal → reopen on new evidence → reassessment → NEW determination
  (history preserved, ledger never rewritten) → error-vs-deception Trust → UNRESOLVED (valid +
  Trust-safe). Closes the review's decisive question with a runnable proof, not a document. Additive
  only; 49 `$defs` + URI cap intact; SPEC v0.22. Docs:
  `contested_reality/docs/DISPUTE-RESOLUTION-SPECIFICATION.md` (16 sections + sufficiency table +
  the honest final assessment).
- **Sprint 13 — the configurable adjudication engine (the adjudication semantics become GENERAL):**
  `instances/contested_reality/adjudication_engine.py` is a generic, rule-driven driver that runs
  the contested-reality lifecycle for ANY org configured for it — business-model weights, resolution
  options, per-option factor scores, the evidence-reconciliation rule's parameters, the §6
  floor-gated set + penalty, authority, and determination policy are all **data** in
  `adjudication_configs.py` (no per-scenario code). The SAME engine drives BOTH `deli` (freight
  $18k delivery → *partial-settlement*) and `cove` (clinical coverage → *step-therapy-first*) with
  no code change, plus each org's thin-evidence sub-dispute → **UNRESOLVED**. Optional additions in
  the same build: a **§7L cockpit Q7** render (`artifacts/adjudication/reports/cockpit-q7*.md`) and
  **Decision-Learning / realized-cost weights** (`decision_learning.py`: expected-vs-actual variance
  drives a clamp-bounded, additive re-weighting of the business model + a recorded
  `realized_cost_usd` on the `decision://`). Commands (from `contested_reality/`):
  `python3 run_adjudication_engine_demo.py` → ALL PASS; the Sprint-0 venv
  `conformance_adjudication.py` → C1–C5 ALL PASS (frozen 49 `$defs`). Labels `deli`/`cove` are NOT
  in `configs.SECTORS`, so the sector build is untouched. Docs:
  `contested_reality/docs/GENERALIZED-ADJUDICATION.md` (§16 verdict: B → B+, materially toward A).
- **Sprint 14 — the config-authorable RULE layer (the reconciliation rule becomes user-selected):**
  `instances/contested_reality/run_rule_comparison_demo.py` drives ONE dispute (`inspect`, a $54k
  goods-QC acceptance) through the SAME generic engine under THREE different CONFIGURED rules —
  `best-reliability-threshold` (default), `strict-anchor-only`, and `recency-weighted-threshold` —
  selected purely via `cfg["reconcile"]["rule"]` from the engine's deterministic registry
  (`eng.RULES`, in `adjudication_engine.py`). A rule choice CHANGES the outcome: best-rel DETERMINES
  *rework-partial-credit* (CLOSED) while strict-anchor and recency correctly end **UNRESOLVED** (OPEN),
  and a claim DISPUTED under best-rel (0.90) is UNDETERMINED under strict-anchor (0.0, testimony
  inadmissible) — with zero engine change between runs (only `reconcile` data differs). The existing
  `deli`/`cove` outputs reproduce byte-for-byte under their original rule. Commands (from
  `contested_reality/`): `python3 run_rule_comparison_demo.py` → ALL PASS; the Sprint-0 venv
  `conformance_adjudication.py` → C1–C5 ALL PASS over 5 labels (deli, cove, inspect-best/anchor/rec).
  Frozen 49 `$defs`, SPEC v0.22, `ros/` untouched. Docs:
  `contested_reality/docs/USER-AUTHORABLE-RULE-LAYER.md` (honest §16: rule *selection* & *parameters*
  are config; the rule *mapping* body is still a registry Python function — "A — Yes" is argued for
  config-selected registry-backed rule authoring, not yet a textual micro-DSL).

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
---

## Sprint 15 — user-authorable RULE-authoring DSL (contested_reality)

The evidence-reconciliation RULE **body** is now authorable as **config text**, not engine Python.
`cfg["reconcile"]["rule_spec"]` is a small declarative spec (admissible evidence kinds × value_field
× optional recency decay × one fixed aggregation op) that the engine **compiles** into the same pure
support map the registry rules run — `adjudication_engine.py` gains `SPEC_VOCAB`,
`compile_rule_spec`, `_spec_support`; the three registry rules and the shared `_derive` are untouched.

- **Parity (same engine, not a different one):** `strict-anchor-only` and `recency-weighted-threshold`
  re-expressed as specs reproduce their registry verdicts **exactly** on the `inspect` dispute
  (`passed 0.84 / failed 0.0` and `passed 0.7863 / failed 0.9`).
- **A genuinely NEW spec-only rule:** `majority-of-sources` (`aggregate:"majority"`,
  `source_threshold:0.92`) was never a registry function; it is authored wholly as a config dict,
  drives a real lifecycle, and *changes the verdict* — `inspect` flips from best-rel's DETERMINED
  `rework-partial-credit` (CLOSED) to **UNRESOLVED** (OPEN), support `0.5/0.0`, distinct from all
  three registry rules. Zero engine Python for the new rule.
- **Runner / conformance:** `run_rule_authoring_demo.py` → ALL PASS; `conformance_adjudication.py`
  now covers **8 labels** (deli, cove, inspect-best/anchor/rec + inspect-anchor-spec/rec-spec/majority)
  C1–C5 ALL PASS, 49 `$defs`; EOF full non-regression green; SPEC v0.22 + `ros/` untouched.

Format + expressiveness frontier (what a spec covers; what still needs a builtin e.g. a Bayesian
posterior) stated plainly in `contested_reality/docs/USER-AUTHORABLE-RULE-DSL.md`.

## Sprint 16 — the named cross-org RULE LIBRARY + a new `bayesian-combine` primitive (contested_reality)

Sprint 16 closes (part of) Sprint 15's disclosed seam and turns spec-authored rules into a real,
reusable, cross-org library.

- **A genuinely NEW inference primitive, `bayesian-combine`** (a reliability-likelihood posterior /
  independent-corroboration aggregate) is added to `eng.SPEC_VOCAB`, authored ONCE as a general,
  deterministic + strict operator (an explicit author `prior`, loud rejection of a bad `prior`), and
  then authorable as data by ANY org. It expresses what `max`/`mean`/... **cannot**: many
  weak-but-independent sources can raise a claim's support ABOVE every single source (posterior
  0.9674 > max 0.7 on identical inputs).
- **A named, reusable cross-org RULE LIBRARY** (`ac.RULE_LIBRARY`): named specs defined once and
  reused by reference (proven by `is`-identity) across ≥2 genuinely different orgs — `majority-of-sources`
  on `inspect` **and** `deli` (goods-QC + freight); the new `independent-corroboration` on `inspect`
  **and** `cove` (goods-QC + clinical).
- **A real verdict flip the new primitive produces:** on the `inspect` dispute at reconcile threshold
  0.98, single-source `max` (0.97) clears nothing → **UNRESOLVED**, while `bayesian-combine` of the
  0.84+0.97 independent witnesses → posterior **0.9961** → **DETERMINED `rework-partial-credit`
  (CLOSED)**. Same org, same threshold, only the `reconcile` rule differs.
- **§7L cockpit Q7 surface:** the report names the ACTIVE rule + spec-authored-vs-registry source
  per org (`cockpit-q7-rule-library.md`).
- **Runner / conformance:** `run_rule_library_demo.py` → ALL PASS; `conformance_adjudication.py`
  now validates **13 labels** C1–C5 ALL PASS, 49 `$defs`; full non-regression green; SPEC v0.22 +
  `ros/` untouched; only catalog URI schemes in the new fixtures.

Full write-up: `contested_reality/docs/USER-AUTHORABLE-RULE-LIBRARY.md` (updated frontier + §16
verdict: A — Yes for the shipped vocabulary *including* the Bayesian-likelihood family; the precise
remaining dependence is an op the vocabulary still cannot name, added once as interpreter code).
