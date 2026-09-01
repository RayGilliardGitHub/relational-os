# RelationalOS — Sector Instances (multi-sector dogfood)

Working, **conformance-validated** instances of the platform for a company in every
sector family of SPEC Appendix B. Each one runs the full S1→S5 chain + Business Operating
Layer (exception → case → task → verified outcome → learning), produces its own cockpit
with the §7L ten answers answered with evidence, emits its fixtures/ledger/graph, and
passes the Sprint-0 conformance audits (C1–C5, exit 0).

The operating loop is identical across sectors; **only the domain vocabulary differs**
(company, counterparties, outcome class, trust claim, URIs, prose). That is the platform
generalizing: the on-time-exception loop is the product, and any sector is a config.

## Project layout (post-reorg standard roots)
- **Canonical `ros/` package** lives at the repo ROOT (`/home/rlg/relational-os/ros/`), flat
  byte-identical to `sprints/sprint-5/artifacts/ros/` (the sprint-5 copy remains the narrative
  snapshot of where it was promoted from; sprints 1–4 hold earlier partial snapshots).
- **Docs** (the verified manuals) are at the repo ROOT `docs/` (also still under
  `sprints/sprint-6/artifacts/docs/` as narrative).
- **Gate** `scripts/verify.sh` + **test suite** `tests/run_checks.py` live at the repo root and
  run from ANY cwd (the conformance scripts were re-anchored to `Path(__file__)` so they are no
  longer CWD-bound). Python layout: `pyproject.toml` declares the `ros` package.
- Everything in this `instances/` dir is unchanged + `__file__`-anchored and runs from repo root.

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

### Sprint 17 — decision learning at the reconciliation layer (honest + additive)
- **Reconcile-rule learning** (`contested_reality/reconcile_learning.py`, additive): the
  `threshold` is recalibrated deterministically from a RECORDED, realized outcome —
  `learn_threshold(prior, realized, lr, [lo,hi])`, clamp-bounded, evidence-gated (`eps`), never the
  wall-clock. It learns the RULE's parameter, not the answer to any case (§7K.1 Decision→Expected→
  Actual→Variance→WHY→change-future-policy at the reconcile boundary).
- **Learning feeds the RULE LIBRARY:** a NEW named spec (`calibrated-threshold-091`) is added to
  `ac.RULE_LIBRARY` and recorded as an append-only signed `rule://` (kind=PROCEDURE) +
  `decision://` (with `rules_applied`) — history not rewritten.
- **Cross-dispute flip + cross-org reuse:** `inspect-learn-a`'s realized outcome (0.90 < 0.95)
  recalibrates the threshold to 0.91; `inspect-learn-b` (a DISTINCT predicate set) is driven once
  under the learned rule and DETERMINES a 0.93-support claim the old 0.95 would wrongly leave
  UNRESOLVED; `deli-learn` (freight) reuses the SAME learned dict by `is`-identity → a library, not a
  one-case patch.
- **§7L Q7/Q8 cockpit line:** `cockpit-q7-q8-reconcile-learning.md` names each org's ACTIVE rule,
  its source (registry / rule-library / learned-this-run), and whether learning changed it + why.
- **Containment proven (real assertions):** Trust stays 0.80 (S5 only), `determination_policy` never
  edited (the §6 human's call), ledger append-only (prior events byte-identical), rebound from
  explicit `[0.55,0.95]`.
- **Runner / conformance:** `run_reconcile_learning_demo.py` → ALL PASS;
  `conformance_adjudication.py` now validates **16 labels** C1–C5 ALL PASS, 49 `$defs`; full
  non-regression green; SPEC v0.22 + `ros/` untouched; only catalog URI schemes (incl. the frozen
  `rule://` Rule $def), no new noun.
- **Honest §16 verdict: calibrated re-authoring, not autonomous learning.**

Full write-up: `contested_reality/docs/RECONCILE-LEARNING.md`.

### Sprint 18 — the §7L Q7/Q8 cockpit line, first-class in the ENGINE (data-only)
- **Engine-native Q7/Q8 render** (`contested_reality/adjudication_engine.py`, additive):
  `cockpit_q7q8(cfg, sub, *, library=None)` returns the ORG's ACTIVE reconcile rule + its SOURCE class
  (registry / rule-library / learned / rule-spec-authored) + learned-or-not-this-run + the
  evidence-gated WHY; `render_cockpit_q7q8(...)` renders that as a plain-text §7L Q7/Q8 line (Q7 =
  options incl. do-nothing baseline + machine-eligible best; Q8 = recommendation with authority +
  authorized determination). Reads the org's OWN config + ledger — data-only, no per-org engine Python.
- **Any org renders it:** a registry rule (`deli`→best-reliability-threshold), a hand-authored
  `RULE_LIBRARY` spec (`inspect-corroboration`→independent-corroboration), and a LEARNED library entry
  added this run (`inspect-learn-b`→calibrated-threshold-091, learned-this-run=True when that org's
  ledger carries its reconcile-learning decision) plus the cross-org reuse case (`deli-learn`→learned,
  learned-this-run=False).
- **Proven generic + correct:** `run_cockpit_q7q8_demo.py` drives 4 orgs across 3 source classes,
  asserts source classification + determinism + both Q7 and Q8 present, and AGREES with the Sprint-16
  (`cockpit-q7-rule-library.md`) and Sprint-17 (`cockpit-q7-q8-reconcile-learning.md`) lines.
- **Runner / conformance:** `run_cockpit_q7q8_demo.py` → ALL PASS; conformance_adjudication
  (16 labels) C1–C5 ALL PASS; full non-regression green; deli/cove byte-identical up to the clock;
  SPEC v0.22, 49 `$defs`, `ros/` untouched, no new noun.
- **Honest §16 verdict: FIRST-CLASS engine render, not a runner-side artifact** — the Q7/Q8 line now
  lives in the generic engine itself and every org renders it identically; the Sprint-16/17 cockpit
  report files are a view over that engine render, not the only place the line exists.

Full write-up: `contested_reality/docs/ENGINE-Q7Q8-COCKPIT.md`.

### Sprint 19 — the FULL §7L Q1–Q10 morning cockpit, first-class in the ENGINE (data-only)
- **Engine-native full §7L render** (`contested_reality/adjudication_engine.py`, additive):
  `cockpit_s7l(cfg, sub, *, library=None)` answers **all ten** §7L morning questions for ANY
  configured org, data-only — Q1 state/events, Q2 change, Q3 attention, Q4 exceptions, Q5 root-cause
  WITH epistemic status, Q6 forecast-if-nothing-changes, Q7 options+trade-off, Q8 recommendation with
  authority, Q9 ownership/capability/authority, Q10 verified outcome + learning. All read off the
  org's OWN graph/ledger/config; `render_cockpit_s7l(...)` renders it as plain text.
- **Strict superset of Sprint-18:** Q7/Q8 delegate to `cockpit_q7q8` by construction (same dict
  blocks), and the Q7/Q8 + active-rule/source/learned/why line is equal on every org.
- **Honest Q6:** a forecast is only produced when a recorded realized-vs-expected series exists;
  otherwise it plainly says "cannot forecast from recorded data". Q5 epistemic status and Q10
  verified/learning are read from the org's real graph/ledger (no authored literals).
- **Proven generic + correct:** `run_cockpit_s7l_demo.py` drives 4 orgs / 3 rule sources and asserts
  all ten Q present (with evidence), Q7/Q8 == Sprint-18 line, determinism, agreement with the
  Sprint-16/17/18 runner lines, real-graph Q5/Q10, and no-fabrication Q6.
- **Runner / conformance:** exit 0 = ALL PASS; conformance_adjudication (16 labels) C1–C5 green; full
  non-regression green; deli/cove byte-identical up to the clock; SPEC v0.22, 49 `$defs`, `ros/`
  untouched, no new noun.
- **Honest §16 verdict: the §7L gate is met at the engine-render level** — #8 (Q8) is the
  machine-eligible best (§6-floor-gated, with the authority it requires) and the determination is the
  §6 human's call that closes in a verified, learned outcome (Q10); the engine reports the recorded
  state and never overrules the human; Q6 honestly cannot forecast where no series is recorded.

Full write-up: `contested_reality/docs/ENGINE-S7L-COCKPIT.md` (+ Sprint-19 appendix in
`docs/ENGINE-Q7Q8-COCKPIT.md`).

### Sprint 20 — recorded-data Q6 forecast + Q9 capacity for the §7L morning cockpit
- **Closes the two honest seams Sprint 19 disclosed** (`notes/findings.md`, "Residual seams"): an org
  that RECORDS the missing data on its own graph/ledger now answers **Q6 ("what if we do nothing?")**
  with a deterministic forecast and **Q9 ("who does it, authority/capacity?")** with a capacity
  number, AS DATA where the data exists — with the honest no-data fallback unchanged.
- **Additive, generic engine additions** (`contested_reality/adjudication_engine.py`, only):
  `forecast_metric(cfg, sub, metric_uri, *, horizon)` computes a **deterministic projection** purely
  from a recorded `metric://` realized-vs-expected series (last recorded `actual` + mean of recorded
  consecutive deltas, forward periods, labelled a projection; never the wall-clock); `record_metric_series`
  + `record_capacity` are REPLAYABLE recorders that append the data to the org's own immutable ledger
  (one signed event, merge-not-replace); `cockpit_s7l`'s `.q6`/`.q9` + `render_cockpit_s7l` consume the
  recorded data when present. 49 `$defs`/URI cap/SPEC v0.22 intact; `metric://` is a first-class catalog
  noun and `capacity` an additive envelope field (**no `capacity://` noun**); `ros/` untouched.
- **Proven on ≥2 orgs:** `run_forecast_capacity_demo.py` (exit 0 = ALL PASS) drives a NEW org
  `deli-forecast` (records a `metric://deli-forecast/m-on-time` series + a `capacity` field on its
  `authority://`) and the existing `deli` (no data). The recorded org forecasts Q6 (`[0.84, 0.82, 0.8]`
  from last 0.86, mean delta −0.02) + reports capacity `1.0 obligations`; `deli` keeps the honest
  fallback. Asserts full §7L on both, determinism, agreement with the recorded graph, no wall-clock,
  and that the deli-forecast fixtures pass the Sprint-0 C1–C5 conformance.
- **§16 verdict:** Q6/Q9 are now data-grounded wherever an org records the data; a no-data org honestly
  says it cannot forecast / reports no capacity rather than inventing one. Q7/Q8 stay the Sprint-18 line
  (delegated); #8 remains §6-floor-gated; the determination is the §6 human's call; S5 alone moves Trust.
- **Non-regression:** all curated runners (incl. the new one) + conformance_adjudication (16 labels)
  C1–C5 ALL PASS; sector `build_all` + `conformance_all`, S5 reference + conformance, agent demo +
  conformance ALL PASS; deli/cove byte-identical up to the clock; schema hash `7fc38c8c…`, 49 `$defs`,
  SPEC v0.22, `ros/` untouched, no new noun.

Full write-up: `contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` (+ additive Sprint-20 note in
`docs/ENGINE-S7L-COCKPIT.md`).

### Sprint 21 — the RECORDED forecast now DRIVES Q3 attention + the Q8 do-nothing expected-impact
- **Closes the honest frontier Sprint 20 disclosed (`notes/findings.md`, "Residual seams"):** the Q6
  projection was computed + rendered but not CONNECTED to the org's decision surface. Sprint 21 makes
  the recorded forecast drive **§7L Q3** and **Q8** — `Q6 → Q3 → Q8` now close as DATA where the data
  exists, with the honest no-data fallback unchanged.
- **Threshold rule (deterministic, recorded-data only):** from a recorded `metric://`
  realized-vs-expected series + `forecast_metric`, the threshold is the recorded `forecast_threshold`
  additive field → else the metric's own `target` → else the last recorded `actual`. When
  `min(projection) < threshold` (the higher-is-better "do nothing and it gets worse" condition),
  `cockpit_s7l.q3` gains a **forecast-driven attention item** `{"tag": "forecast", …}`; `q8` + the
  trade-off carry a **projected-cost do-nothing expected-impact** (`do_nothing_expected_impact` with
  `on_target` bool) from that same projection. The **Q8 recommendation is UNCHANGED** — the forecast
  prices attention + do-nothing, never overrules the §6-floor-gated machine-eligible best.
- **Additive, generic engine additions** (`contested_reality/adjudication_engine.py`, only): a `_num`
  helper + `_forecast_closure(cfg, sub)` (append), `.q3` forecast-attention append, `.q6` now reuses
  the closure (Q3/Q6/Q8 agree by construction), additive `q7`/`q8` enrichment + `render_cockpit_s7l`
  Q3-tag + Q8 do-nothing lines. Frozen functions (`reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/
  `_aggregate`/`rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`) untouched;
  `forecast_threshold` an additive field (**no new noun**); 49 `$defs`/URI cap/SPEC v0.22 intact.
- **Proven on ≥3 orgs:** `run_forecast_action_demo.py` (exit 0 = ALL PASS) drives a **deteriorating**
  `deli-forecast` (projection [0.84,0.82,0.8] crosses target 0.95 → Q3 forecast item + forecast-driven
  do-nothing cost on_target=False), an **on-target** `deli-forecast-flat` (flat [0.96,0.96,0.96] →
  NO forecast attention, do-nothing priced on_target=True), and the **no-data** `deli` (unchanged
  fallback). Asserts full §7L on each, determinism, agreement of Q8 with `forecast_metric` + a
  hand-computed projection, no §6 overrule (Q8 recommendation unchanged), no wall-clock.
- **§16 verdict:** for an org that records a series, the loop **Q6→Q3→Q8 is now closed as data** — the
  projection itself becomes prioritized attention and the do-nothing baseline is priced; a no-data org
  keeps today's cockpit exactly. What is still not derivable: an org that has not recorded a series
  cannot be forced to forecast/price do-nothing (correct), and a richer adaptive forecast model remains
  out of scope of the deterministic, ~$0 stance.
- **Non-regression:** all C-R runners (incl. the new one) + `run_cockpit_s7l_demo` +
  `run_forecast_capacity_demo` ALL PASS; conformance_adjudication (16 labels) C1–C5 ALL PASS; new
  recorded-org fixtures (`deli-forecast`, `deli-forecast-flat`) pass the Sprint-0 C1–C5 (26 instances
  each); sector `build_all` + `conformance_all`, S5 reference + conformance, agent demo +
  conformance ALL PASS; deli/cove fixtures carry **no** closure keys (byte-identical up to the clock);
  schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` untouched, no new noun.

Full write-up: `contested_reality/docs/ENGINE-FORECAST-ACTION.md` (+ additive Sprint-21 note in
`docs/ENGINE-FORECAST-CAPACITY.md`).

### Sprint 22 — the forecast→attention crossing now honors a recorded `direction` (BOTH orientations as data)
- **Closes the honest frontier Sprint 21 disclosed (`notes/findings.md`, "Assumptions that mattered"):**
  the crossing test was hardcoded to the **higher-is-better / rate** case (`min(projection) <
  threshold`). Sprint 22 makes the crossing **direction a recorded, additive parameter** on the
  `metric://` object, so the same data-only closure flags forecast-driven Q3 attention + prices the
  Q8/trade-off do-nothing baseline for **both** orientations.
- **Direction rule:** the `direction` field defaults to `"higher-is-better"` (rate/quality: `min <
  threshold`, falling below a target is bad) — the Sprint-21 test, **byte-identical by default**; an
  org records `"lower-is-better"` for a cost/latency/defect/risk metric (`max > threshold`, rising above
  a recorded ceiling is bad). Threshold resolution unchanged (`forecast_threshold` → `target` → last
  `actual`); the do-nothing summary is worded per direction ("below recorded … by" vs "above recorded …
  by").
- **Additive, generic engine additions** (`contested_reality/adjudication_engine.py`, only): extend
  `_forecast_closure`'s worst/crossing/summary block to branch on the recorded `direction` (+ additive
  `direction` key on the closure / `q6` / `q8["forecast"]` / `do_nothing`). Frozen functions untouched;
  `direction` an additive field (**no new noun**); 49 `$defs`/URI cap/SPEC v0.22 intact.
- **Proven on ≥4/5 orgs:** `run_forecast_direction_demo.py` (exit 0 = ALL PASS) drives the two Sprint-21
  higher-is-better orgs `deli-forecast` / `deli-forecast-flat` (asserted **byte-identical to Sprint 21**,
  recorded without a `direction` field → default), the new **rising-cost** `deli-cost` (lower-is-better,
  projection [20,22,24] above ceiling 16 → Q3 `[forecast]` item + a do-nothing cost priced in the RISING
  orientation, on_target=False), its **below-ceiling** control `deli-cost-flat` (no forecast attention,
  on-target), and the no-data `deli` (unchanged fallback). Asserts full §7L on each, determinism,
  agreement of Q8 with `forecast_metric` + a hand-computed projection, no §6 overrule, no wall-clock.
- **§16 verdict:** the forecast→attention→expected-impact closure now serves **BOTH directions as data** —
  a rate/quality metric projected to fall below target and a cost/latency metric projected to rise above
  ceiling each become prioritized attention with the do-nothing baseline priced in the correct orientation;
  the Q8 recommendation is unchanged (no §6 overrule) and the no-data fallback is intact.
- **Non-regression:** all C-R runners (incl. +Sprint-21 +new) + `run_cockpit_s7l_demo` +
  `run_forecast_capacity_demo` ALL PASS; conformance_adjudication (16 labels) C1–C5 ALL PASS; the new
  lower-is-better fixtures (`deli-cost`, `deli-cost-flat`) pass the Sprint-0 C1–C5 (26 instances each —
  the additive `direction` field survives the C2 temporal-suffix probe); sector `build_all` +
  `conformance_all`, S5 reference + conformance, agent demo + conformance ALL PASS; deli/cove fixtures
  carry **no** closure keys and the two Sprint-21 recorded orgs' Q3/Q8 unchanged (direction default);
  schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` untouched, no new noun.

Full write-up: `contested_reality/docs/ENGINE-FORECAST-DIRECTION.md` (+ additive Sprint-22 note in
`docs/ENGINE-FORECAST-ACTION.md`).

### Sprint 23 — the do-nothing expected-impact is priced as a recorded-variance band (worst ± σ, NOT a single point)
- **Closes the honest frontier Sprint 22 disclosed (`notes/findings.md`, "Open issues / next work"):**
  the Q8/trade-off do-nothing expected-impact was a **single point** (worst vs the recorded threshold),
  IGNORING the RECORDED variance the engine already computes/renders on Q6. Sprint 23 makes the
  **recorded variance a recorded, additive input** to the do-nothing pricing: when the recorded
  `metric://` series' last point carries a numeric `variance`, the closure reports a projected **BAND**
  `{worst, sigma, low, high, crosses}` where `sigma` = the recorded variance (magnitude),
  `low = worst − sigma`, `high = worst + sigma` (exact recorded-data arithmetic), and `crosses` =
  whether the WORST side crosses the threshold in the metric's direction (higher-is-better:
  `low < threshold`; lower-is-better: `high > threshold`).
- **Additive (only `adjudication_engine.py`'s `_forecast_closure` + `render_cockpit_s7l` extended):**
  the `band` + `recorded_variance`/`variance` + `expected_last` (anchor) keys ride on the closure,
  `q8["forecast"]`, and `do_nothing_expected_impact`; the do-nothing summary + Q3 attention `why`
  append an additive phrase naming the band. All frozen functions untouched; no new noun, 49 `$defs`,
  SPEC v0.22, `ros/` + sector instances untouched.
- **Byte-identity is preserved:** a series with **no** recorded variance on its last point (or no
  numeric one) keeps the Sprint-22 single-point output **byte-identical** (no new keys, summary
  unchanged); a no-data org keeps the fallback. The variance-carrying orgs GAIN only the additive
  band/keys/phrase — every pre-existing single-point field/string verified identical
  (`run_forecast_direction_demo.py` now asserts superset byte-identity; the Sprint-21/20 runners
  unchanged and green).
- **Proven on ≥4 orgs (`run_forecast_variance_demo.py`, exit 0 = ALL PASS):** variance-carriers
  `deli-forecast` (higher-is-better, band 0.71…0.89 σ0.09, crosses True) and `deli-cost`
  (lower-is-better, band 16.0…32.0 σ8, high 32.0 above ceiling 16 → a **worse** do-nothing than the
  single point 24.0), a **variance-less control** `deli-flat2` (exactly single-point, no band), and
  the no-data `deli` (unchanged). Asserts: full Q1–Q10; band from recorded values only; summary
  surfaces the variance with superset byte-identity; control exactly single-point; determinism;
  agreement with `forecast_metric` (incl. `recorded_variance`); no §6 overrule; no wall-clock.
- **Honest definition:** this is a **recorded-data spread** (the deterministic worst bounded by the
  last recorded variance) — **NOT a probability/confidence interval**; no stochastic model. What is
  still not derivable: a series that does not record a variance cannot be made to produce a band.
- **§16 verdict:** the do-nothing expected-impact now prices the **recorded spread as data where it
  exists**; the Q8 recommendation is unchanged (the band prices, it never overrules the
  §6-floor-gated pick). New runner ALL PASS; all Sprint-22/21/20 runners + the 12 curated C-R demos +
  `conformance_adjudication` (16 labels) + the 4 prior CR conformances + sector `build_all`/
  `conformance_all` + S5 reference + conformance + agent demo ALL PASS; new orgs' fixtures pass
  Sprint-0 C1–C5; schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` untouched, no new noun.

Full write-up: `contested_reality/docs/ENGINE-FORECAST-VARIANCE.md` (+ additive Sprint-23 notes in
`docs/ENGINE-FORECAST-DIRECTION.md` and `docs/ENGINE-FORECAST-ACTION.md`).

### Sprint 24 — the band's variance SOURCE is a recorded whole-series parameter (`band_variance`)
- **Closes the honest frontier Sprint 23 disclosed (`notes/findings.md`, "Open issues / next work"):**
  the Sprint-23 band used **only the LAST recorded point's `variance`**, so a series whose RECORDED
  `variance` changed across its points (widened or narrowed spread) was collapsed to the final
  variance. Sprint 24 makes the band's variance source a **recorded, additive `band_variance`
  parameter on the `metric://` object** — absent/`"last"` → the last point's variance (**Sprint-23
  byte-identical**, no `source` key); `"all"`/`"minmax"` → the recorded **whole-series** choice
  (`max(|variance|)` over the recorded points) — so an org can price the do-nothing band from the
  recorded **worst-case** spread where it records it.
- **Additive (only `adjudication_engine.py`'s `_forecast_closure` extended):** when a whole-series
  choice is active the band gains `source: "all"`/`"minmax"`, the closure / `q8["forecast"]` /
  `do_nothing_expected_impact` each gain an additive `band_variance` key, and the do-nothing summary +
  Q3 attention `why` append an honest phrase naming the recorded source (`— band σ from the recorded
  whole-series max |variance| (band_variance all)`). Frozen functions untouched; no new noun, 49
  `$defs`, SPEC v0.22, `ros/` + sector instances untouched.
- **Default byte-identity preserved:** the variance-carrying orgs that do NOT record `band_variance`
  (`deli-forecast`, `deli-cost`) keep the EXACT Sprint-23 last-point band + summary + attention-why
  (no `source` key); the no-variance control + no-data org unchanged.
- **Proven on ≥4 orgs (`run_forecast_variance_all_demo.py`, exit 0 = ALL PASS):** default orgs
  `deli-forecast` + `deli-cost` byte-identical to the Sprint-23 runner's constants (only the additive
  `source` added to the whole-series band), the NEW **widening** whole-series org **`deli-varmax`**
  (records `band_variance:"all"`, last |variance| 0.03 small but an earlier recorded |variance| 0.18
  larger → sigma = recorded max 0.18 → band **0.62…0.98 WIDENS** vs the Sprint-23 last-point
  0.77…0.83, `source:"all"`), and the no-data `deli`. Asserts: full Q1–Q10; sigma is a recorded point
  magnitude (never invented); default orgs superset byte-identical; whole-series sigma == recorded
  max |variance| + exact low/high/crosses arithmetic; determinism; agreement with `forecast_metric`
  (its `recorded_variance` == last point) + hand-computed whole-series max; no §6 overrule; no
  wall-clock.
- **Honest definition:** still a **recorded-data spread**, never a probability/confidence interval;
  every possible sigma is a recorded point `variance` magnitude (a pure function of the recorded
  `points` list).
- **§16 verdict:** the do-nothing band now prices the recorded **worst-case whole-series spread as
  data where the org records it**; the default is byte-identical to Sprint 23; the Q8 recommendation
  is unchanged (no §6 overrule). New runner ALL PASS (56 assertions); full non-regression green
  (all forecast runners, the 16 curated C-R demos, all conformances, sectors `build_all`/
  `conformance_all`, S5 reference + conformance, agent demo); `deli-varmax` fixtures pass Sprint-0
  C1–C5 (26 instances, 49 `$defs`); schema hash `7fc38c8c…`, SPEC v0.22, `ros/` untouched, no new noun.

Full write-up: `contested_reality/docs/ENGINE-FORECAST-VARIANCE.md` (Sprint-24 addendum, §7).
### Sprint 25 — the do-nothing band carries the WHOLE-HORIZON worst case + Q9 capacity-attention
- **Closes the honest frontier Sprint 24 disclosed (`notes/findings.md`, "Open issues / next work"):**
  the projected band was still computed around the **single worst projected point**; it did not
  aggregate a band across ALL projection periods (the whole horizon's worst-case spread) and did not
  feed §7L Q9 capacity attention. Sprint 25 closes that bounded slice additively.
- **Horizon-wide band (`_forecast_closure`):** the **SAME recorded sigma** is applied to EVERY
  projection period -> the closure, `q8["forecast"]`, and `do_nothing_expected_impact` additionally
  carry **`band_periods`** (`[{period, low, high}]`, each `projected ± sigma`) + **`band_horizon`**
  (`{low: min period low, high: max period high}` — the record-wide whole-horizon worst case), and the
  do-nothing summary appends an additive horizon-wide phrase (appended AFTER the Sprint-23/24
  single-worst phrase, keeping it a strict prefix). `band_horizon` can **WIDEN beyond the single-worst
  point's band** when an earlier period at +σ exceeds the worst point's high — still the same recorded
  sigma over recorded values, never a new/interpolated sigma.
- **Q9 capacity-attention (`cockpit_s7l`):** when a band exists AND the threshold is numeric, `q9`
  gains an additive **`band_capacity_attention`** `{flag, why, low, high, crosses}` — a data-only flag
  of whether the record-wide horizon range signals the recorded threshold, whose `why` references any
  RECORDED capacity WITHOUT inventing or mutating a number; no-band / no-data orgs carry no key.
- **Default byte-identity preserved:** the variance-carrying orgs (`deli-forecast`, `deli-varmax`,
  `deli-cost`) are unchanged except the additive `band_periods`/`band_horizon` (when a band exists) +
  `band_capacity_attention` (when a band + threshold exist); the no-variance control + no-data org are
  byte-identical.
- **Proven on ≥5 orgs (`run_forecast_horizon_demo.py`, exit 0 = ALL PASS):** `deli-forecast`
  (last-point band byte-identical superset, horizon 0.71…0.93), **`deli-varmax`** (whole-series
  `"all"`, horizon 0.62…1.02 — horizon-wide high 1.02 > single-worst high 0.98), **`deli-varmax-cap`**
  (same band + a recorded capacity -> the Q9 `why` references it, capacity intact), `deli-flat2`
  (no-band control, NO new keys, summary byte-identical), and the no-data `deli`. Asserts: full
  Q1–Q10; `band_periods` = per-period projected ± sigma EXACT; `band_horizon` = min/max of those
  periods; sigma still exactly a recorded point |variance| magnitude; default orgs byte-identical
  superset; determinism; no §6 overrule; no wall-clock.
- **§16 verdict:** the do-nothing price + Q9 capacity-attention now carry the **recorded whole-horizon
  worst case as data where it exists**; the default is byte-identical to Sprint 23/24; the Q8
  recommendation is unchanged. New runner ALL PASS; full non-regression green; new org fixtures pass
  Sprint-0 C1–C5; schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` untouched, no new noun.

Full write-up: `contested_reality/docs/ENGINE-FORECAST-VARIANCE.md` (Sprint-25 addendum, §8) +
`contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` (§9).
### Sprint 26 — the Q3 attention `why` names the horizon-wide range + Q9 capacity-planning REASON
- **Closes the honest frontier Sprint 25 disclosed (`notes/findings.md`, "Open issues / next work"):**
  `band_horizon`/`band_periods` were surfaced on Q6/Q8/do-nothing, but the **Q3** forecast-driven
  attention `why` still named only the single worst point + single-worst band, and the Q9
  `band_capacity_attention` was a FLAG that did not drive any recorded capacity-planning reasoning.
  Sprint 26 closes that bounded slice additively.
- **Q3 horizon-wide suffix (`_forecast_closure`):** when a recorded-variance band exists AND the
  forecast-driven attention item was created, the attention `why` **appends the same record-wide
  `band_horizon` range** (` — horizon-wide recorded band {lo}…{hi} across {n} projection periods
  (band_periods/band_horizon, same recorded σ)`) — appended AFTER the Sprint-23/24 single-worst band
  phrase (+ any Sprint-24 `band_variance` source phrase), so the old `why` stays a **strict prefix**.
  The suffix is the SHARED `_HORIZON_BAND_PHRASE` constant the do-nothing summary also uses, so
  Q3/Q6/Q8/do-nothing name the record-wide worst case **verbatim by construction**. No-band / no-data
  orgs get no suffix (unchanged).
- **Q9 capacity-planning REASON (`cockpit_s7l`):** ONLY where the org records a numeric `capacity` on
  its authority object AND a band + numeric threshold exist, `q9` gains an additive
  **`capacity_planning_attention`** = `{flag, why}` — ONE deterministic rule from recorded numbers only
  (at-capacity when recorded `load >= 1.0`; deficit when the horizon band's worst-side magnitude
  reaches/exceeds the recorded capacity VALUE; otherwise headroom). `why` states the recorded capacity
  value/unit/load + the horizon band and labels headroom/at-capacity/deficit as a derived REASON —
  NEVER an invented capacity figure, NEVER a directive. Orgs that record no capacity carry NO key.
  The Sprint-25 `band_capacity_attention` flag is untouched (additive superset).
- **Proven on ≥5 orgs (`run_forecast_horizon2_demo.py`, exit 0 = ALL PASS):** the same
  `deli-forecast` / `deli-varmax` / `deli-varmax-cap` (recorded capacity 500.0 resolutions/day, load
  0.72 -> `{flag: False, why: "… derived headroom …"}`) / `deli-flat2` (no-band) / `deli` (no-data).
  Asserts: full Q1–Q10; `deli-forecast`'s Q3 `why` == the exact pre-Sprint-26 string + the shared
  suffix (strict-prefix byte-identity); varmax/varmax-cap `why` endswith the suffix; capacity-
  planning present ONLY on `deli-varmax-cap`; `band_periods`/`band_horizon`/`band_capacity_attention`
  unchanged; determinism; no §6 overrule; no wall-clock / no invented number.
- **§16 verdict:** Q3 and Q9 capacity attention now carry the **recorded whole-horizon worst case as
  data where it exists**, and capacity planning is a **data-only REASON** (headroom/at-capacity/
  deficit from recorded numbers only), never a fabricated figure or a directive. New runner ALL PASS;
  full non-regression green; new org fixtures pass Sprint-0 C1–C5; schema hash `7fc38c8c…`, 49 `$defs`,
  SPEC v0.22, `ros/` untouched, no new noun.

Full write-up: the Sprint-26 addendum in `contested_reality/docs/ENGINE-FORECAST-ACTION.md` +
`contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` (§10).

### Sprint 27 — the recorded capacity reaches the Q7/Q8 trade-off as a data-only REASON
- **Build** (`run_forecast_horizon3_demo.py`, exit 0 = ALL PASS): where the org records a numeric
  `capacity` AND a band + numeric threshold exist, `cockpit_s7l` adds an additive
  **`capacity_constraint`** block on BOTH **`q7`** (the trade-off) and **`q8`** (next to
  `do_nothing_expected_impact`) as a PARALLEL block — the frozen `rank`-owned `options`/`tradeoff` and
  the `cockpit_q7q8` bytes are untouched. It names the recorded capacity value/unit/load + the
  horizon-wide recorded band, derives ONE deterministic reason (headroom / at-capacity when recorded
  load >= 1.0 / deficit when the horizon band's worst-side magnitude reaches/exceeds the capacity
  value) via the SHARED `_capacity_reason` helper — so **Q8's `reason` always equals the Q9
  `capacity_planning_attention` label BY CONSTRUCTION** — and marks capacity-consuming (non-baseline)
  options `capacity_risk` in `options_flagged` when not headroom (NEVER `capacity_infeasible`: no
  per-option requirement is ever recorded; the baseline consumes no capacity).
- **Proof on ≥5 orgs:** `deli-varmax-cap` (recorded capacity 500.0 resolutions/day, load 0.72, horizon
  band 0.62…1.02) carries `capacity_constraint` on Q7/Q8 with `{reason: "headroom", flag: false,
  options_flagged: {}}` — **NO option marked infeasible** (headroom) — while `deli-forecast`,
  `deli-varmax`, `deli-flat2`, no-data `deli` carry NO `capacity_constraint` key (byte-identical
  superset). For every org Q7 `options` + Q8 `recommendation`/`machine_eligible_best` are asserted
  EQUAL to `cockpit_q7q8` (no §6 overrule, no re-rank); determinism; no wall-clock / no invented number.
- **§16 verdict:** the recorded capacity now reaches the Q7/Q8 trade-off as a data-only REASON (a
  label, never a removal, never an overrule) while the Q8 recommendation provably stays UNCHANGED.
  **Still not derivable:** the marker does not CHOOSE a different option for the machine (the §6 human
  always does), and a genuinely capacity-constrained optimization that RE-RANKS the recommendation
  stays out of the deterministic advisory scope. New runner ALL PASS; full non-regression green; new
  org fixtures pass Sprint-0 C1–C5; schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` untouched,
  no new noun.

Full write-up: the Sprint-27 section in `contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` (§11) +
`contested_reality/docs/ENGINE-S7L-COCKPIT.md` (§9).

### Sprint 28 — the capacity marker is PROVEN AT ITS LIMIT (at-capacity / deficit) on real orgs
- **Build** (`run_forecast_horizon4_demo.py`, exit 0 = ALL PASS, **recorded data + a runner ONLY — no
  engine change**). Sprint 27 proved the Q7/Q8 `capacity_constraint` marker only in its **headroom**
  branch on a real org (helper-level beyond that). Sprint 28 drives the non-headroom branches AS DATA
  on a full §7L Q1–Q10 cockpit by adding two NEW orgs that RECORD the situation from recorded numbers
  only:
  - **`deli-atcap`** — recorded capacity 500.0 resolutions/day with recorded **load 1.25 (>= 1.0)**,
    same whole-series band as `deli-varmax` (horizon `{0.62, 1.02}`) → `_capacity_reason`
    **`at-capacity`**, `flag: True`.
  - **`deli-deficit`** — **lower-is-better** latency series (horizon `{12.0, 32.0}`, sigma 8) with
    recorded capacity VALUE **30.0** (load 0.9) → horizon worst-side high **32.0 >= capacity 30.0** →
    **`deficit`**, `flag: True`.
- **Proof:** on both non-headroom orgs, `options_flagged` marks EVERY capacity-consuming non-baseline
  option `capacity_risk` (7 options) and NEVER the baseline `unresolved`; the `reason` equals each
  org's Q9 `capacity_planning_attention` **BY CONSTRUCTION** (shared `_capacity_reason`). **The marker
  is a LABEL at its limit:** for EVERY org the Q7 `options` (same count + uris) +
  `machine_eligible_best` + Q8 `recommendation`/`floor_gated` EXACTLY equal `cockpit_q7q8` (no §6
  overrule, no re-rank, no option-removal) — the Q8 `partial-settlement` recommendation provably
  unchanged even at at-capacity/deficit. The five reused Sprint-26/27 orgs (fc, vm, vmc-headroom, fl2,
  deli) are byte-identical.
- **§16 verdict:** the marker is now demonstrated across ALL THREE of its derived reasons (headroom /
  at-capacity / deficit) on real orgs WHILE the Q8 recommendation provably stays unchanged. **Still not
  derivable:** a capacity-constrained OPTIMIZATION that re-ranks the recommendation (out of scope — the
  §6 human always rules), and `capacity_infeasible` (unreachable until a RECORDED per-option capacity
  requirement exists). New runner ALL PASS; full non-regression green; the two new orgs' fixtures pass
  Sprint-0 C1–C5; schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` + schema untouched, no new
  noun.

Full write-up: the Sprint-28 section in `contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` (§12) +
`contested_reality/docs/ENGINE-S7L-COCKPIT.md` (§10).

### Sprint 29 — the capacity marker labels a SPECIFIC option `capacity_infeasible` (from a RECORDED per-option requirement)
- **Build** (`run_forecast_per_option_capacity_demo.py`, exit 0 = 88 PASS, additive — the ONLY engine
  file touched is `adjudication_engine.py`). Sprint 28 proved the marker at-headroom/at-capacity/
  deficit but its own finding disclosed that `capacity_infeasible` was **structurally unreachable**
  (no per-option requirement was ever recorded). Sprint 29 makes the recorded capacity PER-OPTION:
  - a new REPLAYABLE recorder `record_capacity_requirements(sub, authority_uri, requirements, signer)`
    appends an additive `capacity_requirements` map ({option: nonneg amount}) **on the SAME
    `authority://` object that carries the additive `capacity`** → unit-coupled by construction
    (`available = capacity.value − capacity.load`, same recorded unit);
  - the Q7/Q8 `capacity_constraint` block (via the additive `_per_option_capacity_flags` rule) labels
    a SPECIFIC option `capacity_infeasible` iff its RECORDED requirement > available; otherwise
    `capacity_risk`; the baseline (do-nothing/UNRESOLVED) is NEVER flagged, `reason`/`flag` still come
    from the frozen org-level `_capacity_reason`, and the block also surfaces `per_option_requirements`
    + `available_capacity`. A no-requirements org keeps the Sprint-28 block byte-identical.
- **Proof** (two NEW orgs that RECORD per-option requirements):
  - **`deli-infcap`** (at-capacity, cap 500.0 res/day load 1.3 → available **498.7**): heavy options
    record 499.0 (> 498.7) → `capacity_infeasible`; lighter ≤ available → `capacity_risk`.
  - **`deli-deficit-inf`** (deficit, lower-is-better latency cap 30.0 load 0.9 → available **29.1**):
    heavy options record 30.0 (> 29.1) → `capacity_infeasible`; lighter → `capacity_risk`.
  On both, `options_flagged` = 3 `capacity_infeasible` + 4 `capacity_risk` (baseline never flagged),
  every label traces to a recorded requirement vs available, and for EVERY org the Q7 `options` +
  `machine_eligible_best` + Q8 `recommendation`/`floor_gated` EXACTLY equal `cockpit_q7q8` — the Q8
  `partial-settlement` recommendation is provably unchanged even when SOME option is infeasible. The
  five Sprint-28 orgs (fc, vm, vmc-headroom, fl2, deli) are byte-identical.
- **§16 verdict:** the marker now reaches `capacity_infeasible` for a SPECIFIC option from a RECORDED
  per-option requirement + recorded available number, while it is still a LABEL — never a removal,
  never a re-rank, never an overrule of the §6 human — and the Q8 recommendation provably stays
  unchanged. **Still not derivable:** a genuinely capacity-constrained OPTIMIZATION that RE-RANKS the
  recommendation for the machine (out of scope of the deterministic advisory stance — the marker never
  CHOOSES), and a per-option requirement that is NOT unit-coupled to the capacity (an org with no
  recorded capacity value/load, or an option with no recorded requirement, carries no infeasibility
  label — the engine never invents one). New runner ALL PASS; full non-regression green; both new orgs'
  fixtures pass Sprint-0 C1–C5 (26 instances); schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/`
  + schema + sector configs untouched, no new noun.

Full write-up: the Sprint-29 section in `contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` (§13) +
`contested_reality/docs/ENGINE-S7L-COCKPIT.md` (§11).

### Sprint 30 — the label-vs-choice boundary at its sharpest: the RECOMMENDED option made `capacity_infeasible` (the marker is a REASON, never a CHOICE)
- **Build** (`run_forecast_label_vs_choice_demo.py`, exit 0 = ALL PASS, **NO engine change** — pure
  recorded data + a runner; `adjudication_engine.py` hash `a60f8f7…` unchanged). Sprint 29's own finding
  disclosed that the per-option marker NAMES a specific infeasible option but **never CHOOSES a different
  one for the machine — the §6 human always does**. Sprint 30 closes that boundary proof AS DATA on a
  NEW org `deli-recommend-infcap` that RECORDS a per-option requirement making the machine-eligible
  best / Q8 recommendation ITSELF (`partial-settlement`) `capacity_infeasible`.
- **Proof** (the seven Sprint-29 orgs byte-identical + one NEW org): `deli-recommend-infcap` (at-capacity,
  cap 500.0 res/day load 1.3 → available **498.7**) records `partial-settlement` REQUIREMENT **499.0**
  (> 498.7) → **`capacity_infeasible` ON THE RECOMMENDED OPTION**; the other 6 non-baseline options ≤
  available → `capacity_risk`; the `unresolved` baseline (no recorded requirement) → never flagged.
  Asserted: the Q8 recommendation + machine-eligible best **provably STAY `partial-settlement`** — Q7
  `options` (count 8 + uris) + `machine_eligible_best` + Q8 `recommendation` + `floor_gated` EXACTLY
  equal `cockpit_q7q8` (no re-rank, no removal, no §6 overrule); the `capacity_constraint.note` names the
  UNCHANGED Q8 + the §6 human; `reason` still `at-capacity` (== the Q9 label BY CONSTRUCTION). The marker
  says "the recorded capacity says the recommended option can't run"; it does NOT pick a replacement.
- **§16 verdict:** the marker now reaches the recorded per-option limit at its sharpest — the recommended
  option itself is `capacity_infeasible` and the cockpit provably STILL recommends it. **Still not
  derivable:** a capacity-constrained OPTIMIZATION that RE-RANKS the recommendation for the machine (out
  of scope of the deterministic advisory stance — that is a policy / user decision, not a label), and a
  per-option requirement NOT unit-coupled to the capacity (an option with no recorded requirement stays
  non-derivable). New runner ALL PASS; full non-regression green; new org's fixtures pass Sprint-0 C1–C5
  (26 instances, 49 `$defs`); schema hash `7fc38c8c…`, SPEC v0.22, `ros/` + schema + sector configs + the
  engine untouched, no new noun.

Full write-up: the Sprint-30 section in `contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` (§14) +
`contested_reality/docs/ENGINE-S7L-COCKPIT.md` (§12).

### Sprint 31 — the WHOLE recorded-data §7L decision surface inventoried as reason-not-choice (positive consolidation, NO engine change)
- **Build** (`run_recorded_surface_demo.py`, exit 0 = ALL PASS, **NO engine change** — `adjudication
  _engine.py` hash `a60f8f7…` unchanged; a survey runner + recorded data only, as Sprint 30). After six
  sprints (20-30) the whole §7L decision surface is recorded-data + reason; Sprint 31 makes that the
  ORGANIZING truth of a full INVENTORY of the recorded-data decision surface, proven in ONE auditable run.
- **What it does:** drives 11 orgs (the eight Sprint-30 orgs byte-identical + INSPECT + COVE + one no-data
  org, all NEW labels — `inspect-recorded`, `cove-recorded`, `inspect-nodata`; no fixture overwrite) and
  emits a structured `recorded_surface` per org = {present_recorded={metric_series, point_variance,
  band_variance, capacity, capacity_requirements, floor_gated, weights, reconcile_rule},
  derived_reasons={Q3_forecast, Q6_projection, Q7Q8_capacity_constraint, Q9_capacity,
  Q8_do_nothing_impact}, derivable_universe, not_derivable}. It asserts per org that EVERY derived label
  traces to a recorded descriptor (Q3/Q6/Q8-forecast → metric_series; Q7Q8/Q9-capacity → capacity; the
  no-data org derives NOTHING — the engine never invents a reason the org did not record).
- **Reason-not-choice proof, TOTALLED:** for ALL 11 orgs, Q7 `options` + `machine_eligible_best` + Q8
  `recommendation` + `floor_gated` EXACTLY equal `cockpit_q7q8` — the tally prints "11/11 orgs the marker
  never re-ranks; INCLUDES the Sprint-30 org `deli-recommend-infcap` where the RECOMMENDED option is
  `capacity_infeasible`". No recorded data ever re-ranks the Q8 recommendation (it stays the frozen
  `rank` output on every org). Determinism (dict + render) on re-run for all 11.
- **§16 verdict:** the whole recorded-data decision surface is now positively inventoried as recorded-data
  + a REASON while the Q8 recommendation provably stays the frozen `rank` output. **Still not derivable:**
  the ONE remaining out-of-scope step — a capacity-constrained OPTIMIZATION that RE-RANKS the Q8
  recommendation for the machine (a "re-rank for the machine" POLICY / user decision, deliberately NOT
  built; seam = recorded per-option `capacity_requirements` + a deterministic next-best-non-infeasible
  rule by the frozen `rank` utility), plus a per-option requirement NOT unit-coupled / an option with no
  recorded requirement. New runner ALL PASS; new orgs' fixtures pass Sprint-0 C1-C5 (inspect-nodata
  emits no fixtures, correct for a no-data org); full non-regression green; schema hash `7fc38c8c…`,
  SPEC v0.22, `ros/` + schema + sector configs + the engine untouched, 49 `$defs`, no new noun.

Full write-up: the Sprint-31 section in `contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` (§15) +
`contested_reality/docs/ENGINE-S7L-COCKPIT.md` (§13).

### Sprint 32 — the capacity-constrained RE-RANK of the §7L Q8 recommendation for the machine (an EXPLICIT authorized POLICY step, distinct from the reason-not-choice advisory; engine untouched)
- **Build** (`capacity_rerank.py`, NEW module + `run_capacity_rerank_demo.py`, NEW runner, exit 0 = ALL PASS;
  **NO engine change** — `adjudication_engine.py` hash `a60f8f7…` byte-identical). Sprint 30/31 named the ONE
  remaining out-of-scope step — a capacity-constrained OPTIMIZATION that RE-RANKS the Q8 recommendation for
  the machine ("re-rank for the machine" POLICY / user decision). Sprint 32's prompt **explicitly asked for
  it**, so it is built additively: a pure `capacity_rerank(cfg, sub, *)` that reads the engine's recorded
  `capacity_constraint` block + the frozen `rank` utility.
- **What it does:** when an org's machine-eligible best is `capacity_infeasible` (RECORDED per-option
  requirement > available = recorded capacity.value − recorded load), it picks the highest-utility option
  that is neither floor-gated nor `capacity_infeasible` — a deterministic next-best-non-infeasible rule by
  the frozen `rank` — and reports it as an additive `capacity_rerank` block (`prior_machine_best`,
  `prior_best_capacity_flag`, `recorded_descriptors`, `available_capacity`, `per_option_requirements`,
  `replacement`, `replacement_is_baseline`, `all_capacity_consuming_infeasible`, `floor_respected`,
  `policy`, `why`). It respects the §6 floor; never invents a requirement; falls back to the
  do-nothing/UNRESOLVED baseline (and says so) when every capacity-consuming option is infeasible; NEVER
  overwrites the engine's advisory Q8 recommendation.
- **Proven (13 orgs — the eleven Sprint-31 orgs byte-identical + NEW `cove-recommend-infcap` +
  `deli-all-infeasible`):** RE-RANK fires on `deli-recommend-infcap` (partial-settlement →
  conditional-resolution), `inspect-recorded` (rework-partial-credit → conditional-accept-with-guarantee),
  `cove-recommend-infcap` (step-therapy-first → authorize-generic), `deli-all-infeasible` (every
  capacity-consuming option infeasible → unresolved baseline, `replacement_is_baseline` True) — each
  re-ranked Q8 == the recomputed highest non-infeasible non-gated utility option. UNCHANGED (best NOT
  infeasible → byte-identical `cockpit_q7q8`): the nine other orgs incl. `cove-recorded` and no-data
  `inspect-nodata`. **The advisory path NEVER re-ranks** — even where re-rank fires the engine's Q8 still
  == `cockpit_q7q8`, so the Sprint-31 reason-not-choice inventory stands untouched.
- **Honest §16 verdict:** the ONE remaining frontier (a capacity-constrained, re-ranked Q8 under recorded
  capacity) is now derivable AS AN EXPLICIT POLICY step; the deterministic advisory label-vs-choice boundary
  still holds (marks a REASON, never a CHOICE on the default path). **Still not derivable:** a
  probabilistic/stochastic forecast; a per-option requirement NOT unit-coupled to the recorded capacity / an
  option with no recorded requirement (never invented); and any choice the §6 human must make that recorded
  data cannot machine-decide. Determinism; new fixtures pass Sprint-0 C1-C5; full non-regression green;
  schema `7fc38c8c…`, SPEC v0.22, `ros/` + schema + sector `configs.py` untouched, 49 `$defs`, no new noun.

Full write-up: the Sprint-32 section in `contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` (§16) +
`contested_reality/docs/ENGINE-S7L-COCKPIT.md` (§14) + the engine-native report
`contested_reality/artifacts/adjudication/reports/capacity-rerank.md` + `sprints/sprint-32/summary.md`.

### Sprint 33 — the now-TWO-path decision surface consolidated as ONE coherent recorded-data framework (reason-not-choice ADVISORY + POLICY-authorized capacity-constrained RE-RANK, proven to compose; engine AND `capacity_rerank.py` both untouched)
- **Build** (`run_two_path_demo.py`, NEW survey/audit runner, exit 0 = ALL PASS; **`adjudication_engine.py`
  sha256 `a60f8f7…` AND `capacity_rerank.py` sha256 `f7c6a185…` BYTE-IDENTICAL**; recorded data only — a
  consolidation, not a capability). Drives the SAME 13 orgs as Sprint 32 and emits, per org, a
  `two_path_surface` {advisory, rerank} + an EXHAUSTIVE-DISJOINT PATH class.
- **The taxonomy (every org is exactly one):** **ADVISORY-no-capacity** (5: `deli`, `deli-forecast`,
  `deli-varmax`, `deli-flat2`, `inspect-nodata` — no recorded capacity → the advisory is the single answer);
  **ADVISORY-best-runnable** (4: `cove-recorded`, `deli-infcap`, `deli-deficit-inf`, `deli-varmax-cap` —
  capacity recorded, best runnable → `needed=False`, replacement == advisory Q8); **RE-RANK** (4:
  `deli-recommend-infcap`, `inspect-recorded`, `cove-recommend-infcap`, `deli-all-infeasible` — best
  `capacity_infeasible` → by POLICY a replacement is chosen).
- **Proven (ALL PASS):** **(a) composition / non-interference** — advisory Q8 == `cockpit_q7q8` for all 13
  (the re-rank NEVER shadows it); where it fires the replacement is a DIFFERENT option from the advisory Q8
  AND ≠ machine_eligible_best; where `needed=False` they agree; **(b) floor integrity** — no advisory or
  re-rank selection is ever floor-gated (asserted against `rank`, 13/13); **(c) exhaustive-disjoint
  taxonomy**; **(d) determinism vs history** — identical `two_path_surface` on re-run, and the Sprint-31
  reason-not-choice tally (11/11) + the Sprint-32 re-rank results BOTH reproduced from the SAME recorded data
  in this run.
- **Honest §17 verdict / §15:** the two paths are ONE coherent recorded-data decision framework — the
  deterministic advisory label-vs-choice boundary still holds on the default path (a REASON, never a CHOICE)
  and the re-rank is the distinct, POLICY-authorized capability. **Still not derivable:** a
  probabilistic/stochastic forecast; a per-option requirement NOT unit-coupled to the recorded capacity / an
  option with no recorded requirement (never invented); and any §6-human choice recorded data cannot
  machine-decide (the re-rank is POLICY-authorized, not objective best). Full non-regression green; schema
  `7fc38c8c…`, SPEC v0.22, `ros/` + schema + sector `configs.py` untouched, 49 `$defs`, no new noun; no new
  fixture dirs.
- Write-up: `contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` (§17) +
  `contested_reality/docs/ENGINE-S7L-COCKPIT.md` (§15) + the consolidated report
  `contested_reality/artifacts/adjudication/reports/two-path.md` + `sprints/sprint-33/summary.md`.

### Sprint 34 — CONSOLIDATION-AUDIT of the two-path decision surface over the ENTIRE ORG CATALOG (a pure, engine-free audit; `adjudication_engine.py` AND `capacity_rerank.py` BYTE-IDENTICAL)
- **Build** (`run_two_path_catalog_demo.py`, NEW survey/audit runner, exit 0 = ALL PASS; **engine `a60f8f7…`
  AND `capacity_rerank.py` `f7c6a185…` BYTE-IDENTICAL**; schema `34264934…`, SPEC v0.22, 49 `$defs`, no new
  noun, no fixture writes from this runner). Builds the **22-org ORG CATALOG** fresh in memory — the union of
  every org the `run_forecast_*`/`run_cockpit_*`/`run_adjudication_engine_demo`/`r32` CR demo runners already
  construct, enumerated from those files, NOT invented — and classifies each via the Sprint-33
  `_surface`/`_classify`/`_gated_set`.
- **Whole-catalog taxonomy (exhaustive-disjoint): 12 ADVISORY-no-capacity / 6 ADVISORY-best-runnable / 4
  RE-RANK = 22.** Sprint-33 13-org {5,4,4} is the strict subset; the 9 added are 7 no-capacity (deli-forecast-
  flat, deli-cost, deli-cost-flat, cove, inspect-corroboration, inspect-learn-b, deli-learn — no capacity
  block) + 2 best-runnable (deli-atcap, deli-deficit — recorded capacity but NO per-option requirements, so
  best is `capacity_risk`, never `capacity_infeasible`).
- **Proven over the WHOLE catalog (ALL PASS):** **(a) advisory never shadowed** — 22/22 advisory Q8 ==
  `cockpit_q7q8`; 4/4 re-rank orgs pick a provably-distinct replacement (≠ advisory Q8 ≠ machine_eligible_
  best); 18/18 non-firing orgs agree (replacement == advisory Q8); **(b) exhaustive-disjoint** — every org
  exactly one PATH class; `needed` == (path == RE-RANK); **(c) floor integrity** 22/22 (no advisory or re-rank
  selection ever floor-gated vs `rank`); **(d) determinism-vs-history** — `two_path_surface` deterministic on
  re-run (22/22) AND the Sprint-31 tally (11/11) + Sprint-32 re-rank (4) + Sprint-33 13-org taxonomy {5,4,4}
  ALL reproduce from the SAME recorded data.
- **Honest §18 verdict / §16:** the two-path decision surface is ONE coherent recorded-data framework across
  the WHOLE catalog; the deterministic advisory label-vs-choice boundary still holds; the re-rank is the
  POLICY-authorized, distinct capability. **Still not derivable (unchanged):** probabilistic/stochastic
  forecast; a per-option requirement NOT unit-coupled to the recorded capacity / an option with no recorded
  requirement (never invented); and any §6-human choice recorded data cannot machine-decide (the re-rank is
  POLICY-authorized, not objective best). Full non-regression green (18 CR demos incl. the new one + 5
  conformances + build_all + conformance_all + S5 ref + agent); no new fixture dirs.
- Write-up: `contested_reality/docs/DECISION-FRAMEWORK-BOUNDARY.md` (cheat-sheet) + ENGINE-FORECAST-CAPACITY.md
  (§18) + the report `contested_reality/artifacts/adjudication/reports/two-path-catalog.md` +
  `sprints/sprint-34/summary.md`.

### Sprint 35 — REPRODUCIBILITY-AUDIT: the "deterministic local Python, ~$0, real tool output" claim, VERIFIED on this host across the WHOLE corpus (a pure, engine-free audit; `adjudication_engine.py` AND `capacity_rerank.py` BYTE-IDENTICAL)
- **Build** (`run_reproducibility_demo.py`, NEW survey/audit runner, exit 0 = ALL PASS; **engine `a60f8f7…` AND
  `capacity_rerank.py` `f7c6a185…` BYTE-IDENTICAL**, recorded before AND after; schema `34264934…`, SPEC v0.22,
  49 `$defs`, no new noun, 0 `emit_fixtures` calls). Emits
  `contested_reality/artifacts/adjudication/reports/reproducibility.md`.
- **(a) host/platform facts captured LIVE** (emitted to the report + shown): uname `Linux 7.0.0-30-generic
  x86_64` (node `dad`), Python `CPython 3.12.3`, CPU `20`.
- **(b) whole-catalog determinism re-verified on THIS host:** re-runs the Sprint-34 two-path survey over the
  whole 22-org catalog (reusing the Sprint-34 builder + Sprint-33 `_surface`) and asserts EVERY org's
  `two_path_surface` + PATH class EQUALS the Sprint-34 recorded result — taxonomy **{12,6,4}**, the 4 re-rank
  replacements (`deli-recommend-infcap`→conditional-resolution, `inspect-recorded`→conditional-accept-with-
  guarantee, `cove-recommend-infcap`→authorize-generic, `deli-all-infeasible`→unresolved), **22/22** advisory
  Q8 == `cockpit_q7q8` (never shadowed), 18/18 non-firing orgs agree, floor integrity 22/22, two_path_surface
  identical on re-run, and the Sprint-31 tally (11/11) + Sprint-32 re-rank (4/4) + Sprint-33 13-org taxonomy
  {5,4,4} ALL reproduced from the SAME recorded data.
- **(c) the Sprint-34 consolidated boundary doc (`DECISION-FRAMEWORK-BOUNDARY.md`) verified ACCURATE against
  live code** — engine sha256 `a60f8f71`, `capacity_rerank.py` `f7c6a185`, schema `.yaml` `34264934`
  (`.json` `7fc38c8c` — the documented hash is the `.yaml`), 49 `$defs`, SPEC v0.22, and the taxonomy numbers;
  every concrete claim PASSED, so NO doc fix was needed (this is a doc audit, not a code change).
- **Honest §16:** deterministic local reproducibility of the one-framework two-path decision surface across the
  whole catalog is VERIFIED on this host (~$0, real output only); the still-not-derivable residual is
  unchanged (probabilistic/stochastic forecast; a per-option requirement NOT unit-coupled to recorded capacity
  / an option with no recorded requirement — never invented; any §6-human choice recorded data cannot machine-
  decide). Full non-regression green (19 CR demos incl. the new one + 5 conformances + build_all +
  conformance_all + S5 ref + agent), engine + `capacity_rerank.py` raw sha256 unchanged AFTER.
- Write-up: `sprints/sprint-35/reproducibility.md` (host + determinism + build results) + `sprints/sprint-35/
  summary.md` + `notes/findings.md` + the report `contested_reality/artifacts/adjudication/reports/
  reproducibility.md`.

### Sprint 36 — CORPUS-CONSISTENCY note: the Sprint-35 reproducibility FIGURE re-run from the current corpus + the two boundary docs cross-checked against each other and the live corpus (a pure, engine-free audit; `adjudication_engine.py` AND `capacity_rerank.py` BYTE-IDENTICAL)
- **Build** (`run_corpus_consistency_demo.py`, NEW survey/audit runner, exit 0 = ALL PASS; **engine
  `a60f8f7…` AND `capacity_rerank.py` `f7c6a185…` BYTE-IDENTICAL**, recorded before AND after; schema
  `34264934…`, SPEC v0.22, 49 `$defs`, no new noun, 0 `emit_fixtures` calls, pure in-memory + read-only).
  Emits `contested_reality/artifacts/adjudication/reports/corpus-consistency.md`.
- **(a) Sprint-35 reproducibility figure re-run from the CURRENT corpus:** `run_corpus_consistency_demo.py`
  reuses `run_reproducibility_demo` wholesale in a fresh run and asserts the recorded figure reproduces
  byte-identical — whole 22-org two-path survey, taxonomy **{12,6,4}**, the 4 re-rank replacements
  (conditional-resolution / conditional-accept-with-guarantee / authorize-generic / unresolved), **22/22**
  advisory Q8 == `cockpit_q7q8`, floor integrity 22/22, determinism on re-run, and the Sprint-31 (11/11) +
  Sprint-32 (4/4) + Sprint-33 ({5,4,4}) histories.
- **(b) boundary docs mutually consistent + consistent with the live corpus:** parses each class org list
  out of `DECISION-FRAMEWORK-BOUNDARY.md` §3 and verifies it EQUALS the live per-class set; verifies
  `ENGINE-FORECAST-CAPACITY.md` §18/§17 states the same {12,6,4}=22 taxonomy, the 9-added split (7 no-capacity
  + 2 best-runnable deli-atcap/deli-deficit), and the same hashes/invariants; the two docs agree with each
  other and the live corpus — no drifted number, no stale org list, **no doc fix needed**.
- **Honest §16:** deterministic local reproducibility of the one-framework two-path decision surface across
  the whole catalog is RE-VERIFIED on this host from the current corpus; the still-not-derivable residual is
  unchanged (probabilistic/stochastic forecast; a per-option requirement NOT unit-coupled to recorded capacity
  / an option with no recorded requirement — never invented; any §6-human choice recorded data cannot
  machine-decide). Full non-regression green (20 CR demos incl. the new one + 5 conformances + build_all +
  conformance_all + S5 ref + agent), engine + `capacity_rerank.py` raw sha256 unchanged AFTER.
- Write-up: `sprints/sprint-36/summary.md` + `notes/findings.md` + the report
  `contested_reality/artifacts/adjudication/reports/corpus-consistency.md`.
