# SPRINT 34 — PLAN: a pure, engine-free CONSOLIDATION-AUDIT of the two-path decision surface over the WHOLE ORG CATALOG

## Goal
Verify the reference build stays green as ONE coherent whole, and extend the Sprint-33 question — "is
the now-two-path decision surface a single framework?" — from the 13-org Sprint-32/33 set to the ENTIRE
ORG CATALOG every CR demo runner already exercises. Write a consolidated boundary doc + update the rolls.
**NO new capability; `adjudication_engine.py` (hash `a60f8f7…`) AND `capacity_rerank.py` (hash
`f7c6a185…`) stay BYTE-IDENTICAL** (hashes recorded before and after). Consolidation at SPEC v0.22;
schema `34264934…` (sha256 of the `.yaml`), 49 `$defs`, frozen ontology.

This is an AUDIT of existing state: every org is already constructed by an existing runner; the new runner
surveys them (builds each fresh in memory) and classifies using the Sprint-33 `_surface`/`_classify` logic.

## ORG CATALOG (the union of every org the existing CR demo runners construct — enumerated from those files, NOT invented)
**13-org set** (`r32.build()` = `run_capacity_rerank_demo.build`): deli-forecast, deli-varmax,
deli-varmax-cap, deli-flat2, deli, deli-infcap, deli-deficit-inf, deli-recommend-infcap, inspect-recorded,
cove-recorded, inspect-nodata, cove-recommend-infcap, deli-all-infeasible.

**from `run_forecast_action_demo` / `run_forecast_direction_demo`**: deli-forecast-flat, deli-cost,
deli-cost-flat (+ deli, deli-forecast already in the 13).

**from `run_forecast_horizon4_demo.build_orgs`**: deli-atcap, deli-deficit.

**from `run_cockpit_s7l_demo` / `run_cockpit_q7q8_demo`** (the learned rule orgs): inspect-corroboration,
inspect-learn-b, deli-learn (+ deli already).

**from `run_adjudication_engine_demo`** (SCENARIOS = DELI, COVE): cove (the base COVE, label "cove").

→ **22 distinct orgs** (dedup by label; deli/deli-forecast appear in multiple runners but are ONE org).

### Expected whole-catalog PATH distribution (derived from the recorded data, asserted not assumed)
- **ADVISORY-no-capacity** (no recorded authority capacity — nothing to constrain/re-rank): deli-forecast,
  deli-flat2, deli-varmax, deli, inspect-nodata, deli-forecast-flat, deli-cost, deli-cost-flat, cove,
  inspect-corroboration, inspect-learn-b, deli-learn → **12**
- **ADVISORY-best-runnable** (capacity recorded, machine best NOT infeasible → needed=False): deli-varmax-cap,
  deli-infcap, deli-deficit-inf, cove-recorded, deli-atcap, deli-deficit → **6**
- **RE-RANK** (best capacity_infeasible from recorded per-option requirements → needed=True): deli-recommend-infcap,
  inspect-recorded, cove-recommend-infcap, deli-all-infeasible → **4**
- Total **22**. (Sprint-33's 13-org taxonomy {5,4,4} is the strict subset; 9 added: 7 no-capacity + 2 best-runnable.)

## What "done" looks like (from PROMPT.md)
1. **New runner** `run_two_path_catalog_demo.py` that (a) builds the 22-org catalog fresh in memory,
   (b) emits a `two_path_surface` + PATH class per org (reusing Sprint-33 `_surface`/`_classify`), and
   (c) asserts over the WHOLE catalog:
   - **advisory never shadowed**: every org with a capacity-recorded best and `needed=False` keeps advisory
     Q8 == `cockpit_q7q8`; every `needed=True` org has replacement ≠ advisory Q8 ≠ machine_eligible_best.
   - **exhaustive-disjoint**: every org exactly one class; needed=True set == RE-RANK set.
   - **floor integrity**: no advisory or re-rank selection floor-gated vs `rank`.
   - **determinism-vs-history**: Sprint-31 tally (11/11) + Sprint-32 re-rank (4) + Sprint-33 13-org taxonomy
     ALL reproduce from the SAME data in this run.
   Exit 0 = ALL PASS. Emits `artifacts/adjudication/reports/two-path-catalog.md`.
2. **No engine / no `capacity_rerank.py` change**: hashes `a60f8f7…` + `f7c6a185…` unchanged after; no new
   noun; frozen 49 `$defs`; schema `34264934…`; SPEC v0.22; non-regression green; reused orgs' default bytes intact.
3. **Honest consolidated boundary doc**: `docs/DECISION-FRAMEWORK-BOUNDARY.md` (try-it commands, the two-path
   framework, the whole-catalog taxonomy distribution, the honest §16 verdict).
4. **Real output**: new runner ALL PASS + full non-regression green.

## Sub-sprints
- **work/1-plan.md** — baseline already read (SPEC v0.22, PROTOCOL, S31/32/33 summaries+findings, the corpus
  of CR runners + engine + configs). Verify the reference build's green baseline FIRST.
- **work/2-plan.md** — enumerate the catalog (DONE above), write + run the new `run_two_path_catalog_demo.py`,
  assert the four properties over all 22; emit the report + boundary doc + roll-forward docs.
- **work/3-plan.md** — full non-regression green AFTER the new runner; re-verify hashes/schema/defs/SPEC;
  verify reused orgs' default bytes intact; write summary.md + findings.md + `sprints/sprint-35/PROMPT.md`.

## Definition of Done (all exit 0, real output)
- Green baseline FIRST: all CR demo runners + all 5 CR conformances (Sprint-0 venv) + `build_all` +
  `conformance_all` + S5 reference demo + conformance + agent demo + conformance.
- New `run_two_path_catalog_demo.py` ALL PASS over the whole 22-org catalog.
- Full non-regression green AFTER; engine `a60f8f7…` + `capacity_rerank.py` `f7c6a185…` byte-identical
  (record both before and after); schema `34264934…`; 49 `$defs`; SPEC v0.22; `ros/` + schema + sector
  `configs.py` untouched; no new noun; no new fixture dirs.

## Exit criteria for the honest §16 verdict
The two-path decision surface is ONE coherent recorded-data framework across the WHOLE catalog (advisory Q8
== `cockpit_q7q8` for every org; the re-rank never shadows; floors respected; exhaustive-disjoint classes),
WHILE the deterministic advisory label-vs-choice boundary still holds. Still not derivable (unchanged):
probabilistic/stochastic forecast; a per-option requirement NOT unit-coupled to the recorded capacity; an
option with no recorded requirement (the machine never invents one); any §6-human choice recorded data
cannot machine-decide (the re-rank is POLICY-authorized, not objective best). No SPEC bump (v0.22).