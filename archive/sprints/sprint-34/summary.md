# SPRINT 34 — SUMMARY: CONSOLIDATION-AUDIT of the two-path §7L decision surface over the ENTIRE ORG CATALOG, as ONE coherent recorded-data framework (no engine change)

## Goal
Sprint 31 inventoried the whole recorded-data §7L decision surface as reason-not-choice across 11 orgs.
Sprint 32 added the capacity-constrained RE-RANK (new pure module `capacity_rerank.py`) and proved it over
13 orgs. Sprint 33 consolidated the now-TWO-path decision surface (advisory reason-not-choice + POLICY-
authorized re-rank) as ONE framework over those 13 orgs. **Sprint 34 is a CONSOLIDATION-AUDIT**: it verifies
the reference build stays green as ONE coherent whole and extends the one-framework answer from the 13-org
set to the **ENTIRE ORG CATALOG** — the union of every org the existing CR demo runners construct. Survey/Audit
runner + recorded data ONLY: **`adjudication_engine.py` (sha256 `a60f8f7…`) AND `capacity_rerank.py` (sha256
`f7c6a185…`) are BYTE-IDENTICAL** (hashes recorded before and after); no new capability, no schema/norm
change, no new noun, frozen 49 `$defs`, schema `34264934…`, SPEC v0.22.

## The build: `run_two_path_catalog_demo.py` (new survey/audit runner, exit 0 = ALL PASS)
Builds the **22-org ORG CATALOG** fresh in memory — every org the `run_forecast_*`/`run_cockpit_*`/
`run_adjudication_engine_demo`/`r32` CR demo runners already construct, enumerated from those files (NOT
invented): the 13-org `r32.build()` set + `deli-forecast-flat`, `deli-cost`, `deli-cost-flat` (forecast/
direction family) + `deli-atcap`, `deli-deficit` (`run_forecast_horizon4_demo.build_orgs`) + `cove` (base
COVE, SCENARIOS) + `inspect-corroboration`, `inspect-learn-b`, `deli-learn` (the cockpit learned-rule orgs,
replicated faithfully so learned-this-run reads True on inspect-learn-b's own ledger). Each org is classified
via the Sprint-33 `_surface`/`_classify`/`_gated_set`, emitting a `two_path_surface` + an EXHAUSTIVE-DISJOINT
PATH class.

## Whole-catalog taxonomy (asserted, not assumed): 12 ADVISORY-no-capacity / 6 ADVISORY-best-runnable / 4 RE-RANK = 22
- **ADVISORY-no-capacity (12)**: deli-forecast, deli-flat2, deli-varmax, deli, inspect-nodata, deli-forecast-
  flat, deli-cost, deli-cost-flat, cove, inspect-corroboration, inspect-learn-b, deli-learn — no recorded
  authority capacity → nothing to constrain/re-rank; the advisory is the single answer.
- **ADVISORY-best-runnable (6)**: deli-varmax-cap, deli-infcap, deli-deficit-inf, cove-recorded, deli-atcap,
  deli-deficit — capacity recorded, machine best NOT `capacity_infeasible` → `needed=False`,
  replacement == advisory Q8. (`deli-atcap`/`deli-deficit` are the clean new data point: recorded capacity
  but NO per-option requirements → best is `capacity_risk`, never `capacity_infeasible` → nothing to re-rank.)
- **RE-RANK (4)**: deli-recommend-infcap, inspect-recorded, cove-recommend-infcap, deli-all-infeasible — best
  `capacity_infeasible` from RECORDED per-option requirements → by POLICY a replacement is chosen.
- Sprint-33's 13-org {5,4,4} is the strict subset; the 9 added split 7 no-capacity + 2 best-runnable.

## What is proven (all real exit-0 output)
- **(a) advisory never shadowed**: advisory Q8 == `cockpit_q7q8` for ALL 22 orgs (the re-rank NEVER shadows
  the advisory); where `needed=True` (4/4) the replacement is a DIFFERENT option from the advisory Q8 AND ≠
  the machine_eligible_best; where `needed=False` (18/18) the replacement == the advisory Q8 (one path,
  unchanged).
- **(b) exhaustive-disjoint**: every org is exactly one PATH class; no org is two; `needed` == (path ==
  RE-RANK) for all 22; no-capacity orgs carry no capacity_constraint block; best-runnable orgs do.
- **(c) floor integrity**: no advisory or re-rank selection is ever a floor-gated option (asserted against
  the frozen `rank`), 22/22.
- **(d) determinism vs history**: `two_path_surface` deterministic on re-run (22/22); AND the Sprint-31
  reason-not-choice tally (11/11) + the Sprint-32 re-rank results (4 firings) + the Sprint-33 13-org taxonomy
  ({5,4,4}) ALL reproduce from the SAME recorded data in this run — the audit is a VIEW over one dataset,
  not a rewrite.

## Verification (all exit 0, real output)
- NEW runner: `python3 run_two_path_catalog_demo.py` → **RESULT: ALL PASS** over the whole 22-org catalog.
- Green baseline FIRST (Sprint-33 state): all 17 CR demo runners + all 5 CR conformances (Sprint-0 venv) +
  `build_all` + `conformance_all` (12 sectors) + S5 reference demo + conformance + agent demo + conformance →
  ALL PASS.
- Full non-regression AFTER the new runner (18 CR demos incl. the new one) + the same conformances + S5 +
  agent → ALL PASS.
- Invariants: engine raw sha256 `a60f8f7…` UNCHANGED; `capacity_rerank.py` raw sha256 `f7c6a185…` UNCHANGED;
  schema `34264934…`; **49 `$defs`**; SPEC v0.22; `ros/` + schema + sector `configs.py` untouched; no new
  fixture dirs from the runner (0 `emit_fixtures` calls); no new noun.

## Documents rolled forward
`contested_reality/docs/DECISION-FRAMEWORK-BOUNDARY.md` (consolidated boundary cheat-sheet) ·
`contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` §18 · `instances/README.md` Sprint-34 entry ·
`/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after Sprint 34" · the consolidated
whole-catalog report `artifacts/adjudication/reports/two-path-catalog.md` · the `relational-os` skill note ·
`notes/findings.md` · `sprints/sprint-35/PROMPT.md`. No SPEC bump (v0.22).

## Honest §16 verdict
**The two-path decision surface is ONE coherent recorded-data framework across the ENTIRE ORG CATALOG, not
just the 13-org Sprint-33 set.** For all 22 orgs the reason-not-choice ADVISORY (marker never re-ranks;
advisory Q8 == `cockpit_q7q8`) AND the POLICY-authorized RE-RANK (4 firings with a provably-distinct
replacement, 18 unchanged where the advisory already holds) compose from the SAME recorded data — a VIEW, not
a rewrite — classified into an exhaustive-disjoint PATH taxonomy; neither path ever picks a floor-gated
option; the re-rank never shadows the advisory. The deterministic advisory label-vs-choice boundary (a
REASON, never a CHOICE on the default path) still holds. **Still not derivable (the honest residual, unchanged
by audit):** a probabilistic/stochastic forecast (the recorded band is a spread, never a CI — nothing invents
a distribution); a per-option requirement NOT unit-coupled to the recorded capacity value (no available figure
→ no infeasibility label → nothing to re-rank); an option with no recorded requirement carries no
infeasibility label (the machine never invents one — `deli-atcap`/`deli-deficit` prove recorded capacity alone
never reaches RE-RANK); and any choice the §6 human must make that recorded data cannot machine-decide (the
re-rank is POLICY-authorized, not a claim of objective best). No SPEC bump (v0.22).