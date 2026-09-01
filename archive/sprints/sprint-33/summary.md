# SPRINT 33 — SUMMARY: consolidate the now-TWO-path decision surface (reason-not-choice ADVISORY + POLICY-authorized capacity-constrained RE-RANK) as ONE coherent, provably-composable recorded-data framework

## Goal
Sprint 31 positively inventoried the WHOLE recorded-data §7L decision surface as reason-not-choice across
11 orgs (the marker is a REASON, never a CHOICE — the Q8 recommendation provably stays the frozen `rank`
output; the §6 human always rules). Sprint 32, by explicit prompt authorization, added the ONE named
out-of-scope step as an additive PURE module `capacity_rerank.py`: when an org's machine-eligible best is
`capacity_infeasible` from RECORDED per-option `capacity_requirements`, BY POLICY the machine picks the
highest-utility option (frozen `rank`) that is neither floor-gated nor `capacity_infeasible`, reported as an
additive `capacity_rerank` block that NEVER overwrites the engine's advisory Q8. **Sprint 33 consolidates the
now-two-path decision surface** as ONE coherent framework and PROVES the two paths never silently interfere.
It is a positive consolidation: a survey/audit runner + recorded data ONLY — **`adjudication_engine.py`
(sha256 `a60f8f7…`) AND `capacity_rerank.py` (sha256 `f7c6a185…`) are BYTE-IDENTICAL**; no new capability, no
schema/norm change, no new noun, frozen 49 `$defs`, SPEC v0.22.

## The build: `run_two_path_demo.py` (new runner, exit 0 = ALL PASS)
Reuses Sprint 32's 13-org set (`r32.build()` = the eleven Sprint-31 orgs byte-identical + `cove-recommend-infcap`
+ `deli-all-infeasible`), and for each org emits a structured **`two_path_surface`** {advisory={q7_machine_eligible_best,
q8_recommendation, floor_gated, capacity_constraint(options_flagged)}, rerank={needed, prior_machine_best,
replacement, replacement_is_baseline}} + an EXHAUSTIVE-DISJOINT **PATH class**:
- **ADVISORY-no-capacity** (5): `deli`, `deli-forecast`, `deli-varmax`, `deli-flat2`, `inspect-nodata` — no
  recorded authority capacity → nothing to constrain/re-rank; the advisory IS the single answer.
- **ADVISORY-best-runnable** (4): `cove-recorded`, `deli-infcap`, `deli-deficit-inf`, `deli-varmax-cap` —
  capacity recorded, machine best NOT `capacity_infeasible` → `needed=False`, replacement == advisory Q8.
- **RE-RANK** (4): `deli-recommend-infcap`, `inspect-recorded`, `cove-recommend-infcap`, `deli-all-infeasible` —
  best `capacity_infeasible` → by POLICY a replacement is chosen (a different option).

## What is proven (all real exit-0 output)
- **(a) composition / non-interference**: advisory Q8 == `cockpit_q7q8` for ALL 13 orgs (the re-rank NEVER
  shadows the advisory); where `needed=True` the replacement is a DIFFERENT option from the advisory Q8 AND
  ≠ the machine_eligible_best (provably distinct paths — 4/4); where `needed=False` the replacement == the
  advisory Q8 (they agree — one path, unchanged, 9/9).
- **(b) floor integrity**: no advisory or re-rank selection is ever a floor-gated option (asserted against the
  frozen `rank`), 13/13.
- **(c) exhaustive-disjoint taxonomy**: every org is exactly one PATH class; no org is two; the RE-RANK orgs
  are exactly the `needed=True` orgs; no-capacity orgs carry no capacity_constraint block.
- **(d) determinism vs history**: re-running gives an identical `two_path_surface` (13/13), AND the Sprint-31
  reason-not-choice tally (11/11 q7/q8 == `cockpit_q7q8`) + the Sprint-32 re-rank results (4 firings with a
  provably-different replacement, 9 unchanged) are BOTH reproduced from the SAME recorded data in this run —
  the consolidation is a VIEW over one dataset, not a rewrite.

## Verification (all exit 0, plain python3 + Sprint-0 venv for conformance)
- NEW runner: `python3 run_two_path_demo.py` → **RESULT: ALL PASS**.
- Green baseline FIRST (Sprint-32 state): all 16 plain-python3 CR demo runners + all 5 CR conformances
  (Sprint-0 venv) + `build_all` + `conformance_all` (12 sectors) + S5 reference demo + conformance + agent
  demo + conformance → ALL PASS.
- Full non-regression AFTER the new runner (17 CR demos incl. the new one) + the same conformances + S5 + agent → ALL PASS.
- Invariants: engine raw sha256 `a60f8f7…` UNCHANGED; `capacity_rerank.py` raw sha256 `f7c6a185…` UNCHANGED;
  schema `34264934…`; **49 `$defs`**; SPEC v0.22; `ros/` + schema + sector `configs.py` untouched; no new
  fixture dirs from the new runner; no new noun.

## Documents rolled forward
`docs/ENGINE-FORECAST-CAPACITY.md` §17 · `docs/ENGINE-S7L-COCKPIT.md` §15 · `instances/README.md` Sprint-33
entry · `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after Sprint 33" · the
consolidated engine-native report `artifacts/adjudication/reports/two-path.md` · the `relational-os` skill note ·
`sprints/sprint-33/notes/findings.md` · `sprints/sprint-34/PROMPT.md`. No SPEC bump (v0.22).

## Honest §16 verdict
**The two paths are now a SINGLE coherent recorded-data decision framework — they compose without one silently
overriding the other.** For all 13 orgs the reason-not-choice ADVISORY reproduces the Sprint-31 inventory
(marker never re-ranks) AND the POLICY-authorized RE-RANK reproduces the Sprint-32 results, from the SAME
recorded data (a view, not a rewrite), classified into an exhaustive-disjoint PATH taxonomy; neither path ever
picks a floor-gated option; the re-rank never shadows the advisory. The deterministic advisory label-vs-choice
boundary (a REASON, never a CHOICE on the default path) still holds. **Still not derivable (the honest residual,
unchanged by consolidation):** a probabilistic/stochastic forecast (the recorded band is a spread, never a CI —
nothing invents a distribution); a per-option requirement NOT unit-coupled to the recorded capacity value (no
available figure → no infeasibility label → nothing to re-rank); an option with no recorded requirement carries
no infeasibility label (the machine never invents one); and any choice the §6 human must make that recorded data
cannot machine-decide (the re-rank is POLICY-authorized, not a claim of objective best). No SPEC bump (v0.22).