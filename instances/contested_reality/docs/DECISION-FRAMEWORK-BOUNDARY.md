# DECISION-FRAMEWORK-BOUNDARY — the §7L two-path decision surface as ONE coherent recorded-data framework, over the WHOLE org catalog (CONSOLIDATION-AUDIT, Sprint 34)

Consolidated boundary cheat-sheet. **Sprint 34 is a pure, engine-free AUDIT**: it verifies the reference
build is green as one whole and proves the Sprint-33 two-path answer holds across the **entire ORG CATALOG**
— the union of every org the `run_forecast_*`/`run_cockpit_*`/`run_adjudication_engine_demo`/`r32` CR demo
runners already construct — not just the 13-org Sprint-32/33 set. `adjudication_engine.py` (sha256
`a60f8f7…`) AND `capacity_rerank.py` (sha256 `f7c6a185…`) are **byte-identical**; no new capability, no new
noun, frozen 49 `$defs`, schema `34264934…`, SPEC v0.22.

---

## 1. Try it (all plain `python3` unless noted)

- **Reference green baseline FIRST** (the whole build as one command-set):
  - CR demo runners: `cd instances/contested_reality && python3 run_two_path_demo.py && python3
    run_two_path_catalog_demo.py && python3 run_capacity_rerank_demo.py && python3 run_recorded_surface_demo.py
    && python3 run_forecast_{action,capacity,direction,horizon,horizon2,horizon3,horizon4,label_vs_choice,
    per_option_capacity,variance,variance_all}_demo.py && python3 run_cockpit_{q7q8,s7l}_demo.py && python3
    run_adjudication_engine_demo.py` (all 18 exit 0 = ALL PASS).
  - All 5 CR conformances: `python3 conformance_{adjudication,dispute,interest,lifecycle,tradeoff}.py` with
    the Sprint-0 venv `/home/rlg/relational-os/archive/sprints/sprint-0/artifacts/.venv/bin/python`.
  - Sectors + reference: `cd instances && python3 build_all.py && <venv> conformance_all.py`;
    `cd archive/sprints/sprint-5/artifacts && python3 run_s5_demo.py && <venv> run_s5_conformance.py`;
    `cd instances/agent_demo && python3 run_agent_demo.py && <venv> conformance_agent.py`.
- **The two-path demo** (13-org set, Sprint 33): `cd instances/contested_reality && python3 run_two_path_demo.py`.
- **The whole-catalog audit** (22 orgs, Sprint 34): `cd instances/contested_reality && python3
  run_two_path_catalog_demo.py` → `RESULT: ALL PASS`; report at
  `artifacts/adjudication/reports/two-path-catalog.md`.

Run from each dir (runners are CWD-sensitive).

## 2. The two-path framework (ONE coherent recorded-data decision surface)

Every org's §7L Q8 decision surface is a pure function of RECORDED data + the frozen `rank` utility, on two
explicitly-distinct, provably-composable paths:

- **ADVISORY (reason-not-choice, Sprint 31).** The Q7/Q8 `capacity_constraint` block + per-option
  `capacity_infeasible`/`capacity_risk` flags are a **REASON, never a CHOICE**: the Q8 recommendation provably
  stays the frozen `rank` output (`== cockpit_q7q8`), the §6 floor is respected, and even the RECOMMENDED
  option can be labelled `capacity_infeasible` from a recorded per-option requirement — the engine never
  picks a replacement.
- **RE-RANK (POLICY-authorized, Sprint 32).** When the machine-eligible best is `capacity_infeasible` from
  RECORDED per-option `capacity_requirements`, BY POLICY the machine picks the highest-utility option (frozen
  `rank`) that is neither floor-gated nor `capacity_infeasible` — reported as an ADDITIVE `capacity_rerank`
  block that NEVER overwrites the engine's advisory Q8. `capacity_rerank.py` is a pure module, untouched.
- **Composition.** The re-rank never shadows the advisory: advisory Q8 == `cockpit_q7q8` for EVERY org; where
  the re-rank fires its replacement is provably distinct (≠ advisory Q8 ≠ machine_eligible_best); where not
  they agree (replacement == advisory Q8). Floors are respected on both paths. `capacity_rerank.py` f7c6a185….

## 3. Whole-catalog taxonomy (Sprint 34 distribution, 22 orgs — exhaustive-disjoint)

| PATH class | count | orgs |
|---|---|---|
| **ADVISORY-no-capacity** (no recorded authority capacity → the advisory is the single answer) | **12** | deli-forecast, deli-flat2, deli-varmax, deli, inspect-nodata, deli-forecast-flat, deli-cost, deli-cost-flat, cove, inspect-corroboration, inspect-learn-b, deli-learn |
| **ADVISORY-best-runnable** (capacity recorded, machine best NOT `capacity_infeasible` → `needed=False`, replacement == advisory Q8) | **6** | deli-varmax-cap, deli-infcap, deli-deficit-inf, cove-recorded, deli-atcap, deli-deficit |
| **RE-RANK** (best `capacity_infeasible` from recorded per-option requirements → `needed=True`, distinct replacement) | **4** | deli-recommend-infcap, inspect-recorded, cove-recommend-infcap, deli-all-infeasible |

Sprint-33's 13-org {5,4,4} is the strict subset. The 9 added are 7 no-capacity (these carry no
`capacity_constraint` block) + 2 best-runnable (`deli-atcap`, `deli-deficit` — recorded capacity but NO
per-option requirements, so the machine best is `capacity_risk`, never `capacity_infeasible` → nothing to
re-rank).

## 4. Whole-catalog proof (all asserted in `run_two_path_catalog_demo.py`, exit 0 = ALL PASS)

- **(a) advisory never shadowed**: 22/22 advisory Q8 == `cockpit_q7q8`; 4/4 re-rank orgs pick a distinct
  replacement; 18/18 non-firing orgs agree.
- **(b) exhaustive-disjoint**: every org is exactly one PATH class; `needed` == (path == RE-RANK); no-capacity
  orgs carry no `capacity_constraint` block; best-runnable orgs do.
- **(c) floor integrity**: 22/22 — no advisory Q8 nor re-rank replacement is ever floor-gated vs `rank`.
- **(d) determinism-vs-history**: `two_path_surface` deterministic on re-run (22/22); the Sprint-31
  reason-not-choice tally **11/11**, the Sprint-32 re-rank results **4 firings**, and the Sprint-33 13-org
  taxonomy **{5,4,4}** ALL reproduce from the SAME recorded data in this run.

## 5. Honest §16 verdict (the boundary)

**The two-path decision surface is ONE coherent recorded-data framework across the WHOLE catalog.** For all
22 orgs the reason-not-choice ADVISORY (marker never re-ranks; advisory Q8 == `cockpit_q7q8`) and the
POLICY-authorized RE-RANK (4 firings, distinct replacement; 18 unchanged where the advisory already holds)
compose from the SAME recorded data — a VIEW, not a rewrite — with exhaustively-disjoint classification and
floor integrity everywhere. The deterministic advisory label-vs-choice boundary still holds on the default
path.

**Still not derivable (the honest residual, unchanged by audit):** a probabilistic/stochastic forecast (the
recorded band is a spread, never a CI — nothing invents a distribution); a per-option requirement NOT
unit-coupled to the recorded capacity value (no available figure → no infeasibility label → nothing to
re-rank); an option with no recorded requirement carries no infeasibility label (the machine never invents
one); and any choice the §6 human must make that recorded data cannot machine-decide (the re-rank is
POLICY-authorized, not a claim of objective best).

No SPEC bump (v0.22); no new capability; engine `a60f8f7…` + `capacity_rerank.py` `f7c6a185…` byte-identical;
no new noun; frozen 49 `$defs`; schema `34264934…`; `ros/` + schema + sector `configs.py` untouched.

## Update after Sprint 36 — CORPUS-CONSISTENCY note (the Sprint-35 reproducibility figure re-run + the two boundary docs cross-checked; engine AND `capacity_rerank.py` untouched)

Sprint 36 is a pure, engine-free CORPUS-CONSISTENCY note: no new capability. `run_corpus_consistency_demo.py`
(exit 0 = ALL PASS; **engine `a60f8f7…` AND `capacity_rerank.py` `f7c6a185…` BYTE-IDENTICAL**, recorded before
and after; schema `34264934…`, SPEC v0.22, 49 `$defs`, no new noun, 0 `emit_fixtures` calls):
- **(a)** re-runs the Sprint-35 reproducibility FIGURE in a FRESH run over the current corpus (reusing
  `run_reproducibility_demo`) and asserts it reproduces byte-identical — whole 22-org two-path survey,
  taxonomy **{12,6,4}**, the 4 re-rank replacements, **22/22** advisory Q8 == `cockpit_q7q8`, floor integrity
  22/22, determinism on re-run, and the Sprint-31 (11/11) + Sprint-32 (4/4) + Sprint-33 ({5,4,4}) histories.
- **(b)** cross-checks THIS cheat-sheet's §3 taxonomy rows (12/6/4 + per-class org list) AND the
  `ENGINE-FORECAST-CAPACITY.md` §18/§17 figures against EACH OTHER and the LIVE corpus — every counted org
  matches the live per-class set, the cited hashes (`a60f8f7…`/`f7c6a185…`/`34264934…`/49 `$defs`/SPEC v0.22)
  match live, and the "9 added = 7 no-capacity + 2 best-runnable (deli-atcap/deli-deficit)" story holds. No
  drifted number, no stale org list — **no doc fix needed**. Report:
  `contested_reality/artifacts/adjudication/reports/corpus-consistency.md`.