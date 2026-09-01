# SPRINT 28 — work/2-plan.md  (close-out: docs, summary, findings, sprint-29 prompt)

## Prior state
- work/1-plan executed: `run_forecast_horizon4_demo.py` builds 7 orgs (5 reused + deli-atcap +
  deli-deficit), ALL PASS exit 0; new org fixtures pass Sprint-0 C1–C5; engine NOT modified.
- Docs roll-forward done: ENGINE-FORECAST-CAPACITY §12, ENGINE-S7L-COCKPIT §10, instances/README
  Sprint-28 entry, STRESS-TEST-SCENARIOS "Update after Sprint 28".

## This step (close-out)
1. Consolidated final non-regression: re-run ALL demo runners + the new horizon4 + the 5 CR
   conformances + build_all + conformance_all + S5 reference demo/conformance + agent demo/conformance
   -> all exit 0. Confirm schema hash `7fc38c8c…` (JSON) + 49 $defs unchanged; engine/schema/ros/
   untouched.
2. `sprints/sprint-28/summary.md` — the sprint close-out (goal, orgs, exact recorded numbers for the
   two non-headroom reasons, the ≤LABEL-at-limit proof, byte-identity default, generic+additive, the
   verified build+conformance commands, the honest §16 verdict).
3. `sprints/sprint-28/notes/findings.md` — assumptions, verified real output, pitfalls, open issues /
   next-work (the honest frontier after this sprint).
4. Write `sprints/sprint-29/PROMPT.md` — the next self-contained sprint prompt (self-contained, NO
   memory).

## Honest §16 verdict (to carry into summary + findings + sprint-29)
The Sprint-27 `capacity_constraint` marker is now demonstrated across ALL THREE of its derived reasons
(headroom / at-capacity / deficit) on real orgs WHILE the Q8 recommendation provably stays unchanged
even at at-capacity/deficit. The marker never re-ranks, never removes, never overrules the §6 human.
Still not derivable: a capacity-constrained OPTIMIZATION that re-ranks the recommendation (out of
scope — §6 human always rules; the marker never CHOOSES), and `capacity_infeasible` (unreachable until
a RECORDED per-option capacity requirement exists).