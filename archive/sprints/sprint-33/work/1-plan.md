# work/1-plan — build `run_two_path_demo.py` (Sprint 33 consolidation audit runner)

## Goal
One NEW runner, engine + `capacity_rerank.py` byte-identical, that drives the same 13-org recorded data
as Sprint 32 (`r32.build()`) and emits, per org, a structured `two_path_surface` +
`path` classification ∈ {ADVISORY-no-capacity, ADVISORY-best-runnable, RE-RANK}, then asserts the four
groups: (a) composition/non-interference, (b) floor integrity, (c) exhaustive-disjoint taxonomy,
(d) determinism-vs-history. Emits `artifacts/adjudication/reports/two-path.md`. Exit 0 = ALL PASS.

## Data sources (reused, unchanged)
- `eng.cockpit_s7l(cfg, sub, library)` -> q7 {baseline, machine_eligible_best, options} + q8
  {recommendation, floor_gated(list), capacity_constraint?{options_flagged, available_capacity,
  per_option_requirements}}.
- `eng.cockpit_q7q8(cfg, sub, library)` -> the advisory q7/q8 WITHOUT the capacity block (the
  reason-not-choice / "marker never re-ranks" reference).
- `eng.rank(cfg)` -> [{option, floor_gated, ...}] (the frozen utility ordering + §6 floor).
- `cr.capacity_rerank(cfg, sub, library)` -> {needed, prior_machine_best, replacement,
  replacement_is_baseline, ...}.

## Classification (disjoint + exhaustive by construction)
- cc = q8.capacity_constraint; if not a dict                -> ADVISORY-no-capacity
- elif options_flagged[machine_eligible_best]=='capacity_infeasible' -> RE-RANK
- else                                                     -> ADVISORY-best-runnable
Assert `needed == (path == RE-RANK)` for every org (the authz re-rank fires iff the best is infeasible).

## Assertions (ALL PASS)
a) composition/non-interference:
   - advisory Q8 rec == cockpit_q7q8 rec for EVERY org (reason-not-choice inventory intact; the re-rank
     never shadows the advisory).
   - where needed=True: replacement != advisory Q8 rec AND replacement != machine_eligible_best.
   - where needed=False: replacement == advisory Q8 rec (one path, unchanged).
b) floor integrity: advisory Q8 rec and replacement each NOT in the rank-derived floor-gated set
   (for every org).
c) exhaustive-disjoint: every org yields exactly one class; classes are pairwise-disjoint strings;
   the RE-RANK orgs == the needed=True orgs; no-capacity orgs have no capacity_constraint.
d) determinism-vs-history:
   - determinism: two cockpit/rerank evaluations on the same org give an identical two_path_surface.
   - history: the Sprint-31 reason-not-choice tally (11/11 orgs q7/q8 == cockpit_q7q8) AND the
     Sprint-32 re-rank results (4 replacements: deli-recommend-infcap->conditional-resolution,
     inspect-recorded->conditional-accept-with-guarantee, cove-recommend-infcap->authorize-generic,
     deli-all-infeasible->unresolved[baseline fallback]; 9 unchanged replacement==advisory) both
     reproduce from the SAME recorded data in this run.

## Deliverable
`run_two_path_demo.py` (plain python3; `--help` no; exits 0 on ALL PASS). Suppress the engine demo
build noise with contextlib.redirect_stdout around `r32.build()`. Report md written last.