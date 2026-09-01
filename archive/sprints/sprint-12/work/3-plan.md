# Sub-sprint 4 — Non-regression + documentation + hand-off

## Objective
Re-verify the whole system is unaffected, then document the consolidated lifecycle + write the
hand-off. Schema, `ros/`, SPEC, and the 12 sector instances must be untouched.

## Steps
1. Non-regression (real): run_full_dispute (this sprint) + Sprint-11/10/9 demos + all conformance +
   build_all + conformance_all + S5 reference + Sprint-8 agent demo — all ALL PASS.
2. Integrity: `git status` — only new contested_reality + sprint-12/13 files; core untouched.
3. Docs: `instances/README.md` Sprint-12 bullet; STRESS-TEST-SCENARIOS.md "Update after Sprint 12"
   (consolidated lifecycle closes the "relational, not mechanism" question with a runnable proof).
4. Hand-off: reconciling the earlier queue — rewrite `sprints/sprint-12/PROMPT.md` to describe THIS
   (the lifecycle spec + proof) so a fresh session reads it accurately, and write
   `sprints/sprint-13/PROMPT.md` as the next self-contained prompt (generalize the adjudication
   semantics to a configurable engine + wire the trade-off/lifecycle onto the §7L cockpit Q7, per the
   finding). Write `sprints/sprint-12/summary.md` + `notes/findings.md`.

## Exit criteria
Every non-regression run exit 0; git shows no core-file modification; README/STRESS-TEST/summary/
findings + sprint-12 PROMPT (accurate) + sprint-13 PROMPT (next) all written.