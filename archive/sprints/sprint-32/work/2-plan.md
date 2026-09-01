# SPRINT 32 — work/2-plan (build step 2: the re-rank demo runner)

## What
A NEW runner `instances/contested_reality/run_capacity_rerank_demo.py` that drives a chosen org set
through `capacity_rerank.capacity_rerank(...)`, asserts the PROMPT's Definition of Done, emits
fixtures for the two NEW orgs + a report, and prints RESULT: ALL PASS (exit 0 under plain python3).

## Org set
RE-RANK (machine best is `capacity_infeasible` -> a replacement IS chosen):
- `deli-recommend-infcap`  prior `partial-settlement` -> `conditional-resolution`
- `inspect-recorded`       prior `rework-partial-credit` -> `conditional-accept-with-guarantee`
- `cove-recommend-infcap`(NEW) prior `step-therapy-first` -> `authorize-generic`
- `deli-all-infeasible`(NEW)   prior `partial-settlement` -> `unresolved` (baseline fallback,
  `replacement_is_baseline` True, `all_capacity_consuming_infeasible` True)

UNCHANGED (best NOT infeasible -> byte-identical to `cockpit_q7q8`): the nine others
(`cove-recorded`, `deli-infcap`, `deli-deficit-inf`, `deli-varmax-cap`, `deli`, `deli-forecast`,
`deli-varmax`, `deli-flat2`, `inspect-nodata`).

## Assertions (all exit-0 gating)
1. Determinism: `capacity_rerank` twice -> identical block (dict equality).
2. NEEDED re-rank orgs: block.needed True; block.replacement == the recomputed
   highest-non-infeasible-non-gated (from the frozen `rank`); block.replacement != prior;
   block.prior_best_capacity_flag == "capacity_infeasible"; floor_respected True AND replacement
   not in cfg.floor_gated (verified against rank()); replacement chosen per family.
3. UNCHANGED orgs: block.needed False; block.replacement == `cockpit_q7q8`.q8.recommendation ==
   s7l.q8.recommendation (byte-identical — the advisory path never re-ranks).
4. Advisory-vs-re-rank distinct: even where re-rank fires, engine s7l.q8.recommendation STILL ==
   `cockpit_q7q8` (the reason-not-choice inventory of the advisory path is intact; the re-rank is
   an explicit separate POLICY step, reported as DATA in the block).
5. New orgs emit fixtures; new-org graph round-trips.
6. Emit artifacts/adjudication/reports/capacity-rerank.md.

## Exit criteria
`python3 run_capacity_rerank_demo.py` -> RESULT: ALL PASS, exit 0; engine untouched.