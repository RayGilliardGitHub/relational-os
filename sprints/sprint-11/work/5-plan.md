# Sub-sprint 5 — Non-regression + documentation (roll-forward)

## Objective
Re-verify the entire system is unaffected by Sprint 11, then document the trade-off engine and
write the hand-off artifacts. The schema, `ros/`, SPEC, and the 12 sector instances must be
untouched (the additive recommendation/trade-off leaks nothing).

## Steps
1. **Non-regression (real output):** re-run Sprint-8 agent demo, Sprint-9 + Sprint-10 demos +
   conformance, `build_all.py` + `conformance_all.py`, and the S5 reference demo — all must ALL PASS.
2. **Integrity:** `git status` — confirm only new contested_reality files added; `ros/`, schema,
   SPEC.md, and the 12 sector fixtures unchanged (schema still 49 `$defs`).
3. **Docs:** write `docs/TRADE-OFF-IMPLEMENTATION.md` (real output embedded: rankings, the §6 gate,
   the model advisory line); add a Trade-off section to `instances/README.md`; append an
   "Update after Sprint 11" note to STRESS-TEST-SCENARIOS.md (Scenario B gap #3 now closed).
4. **Hand-off:** `sprints/sprint-11/summary.md` + `notes/findings.md`; write the next sprint's
   self-contained prompt at `sprints/sprint-12/PROMPT.md`.

## Exit criteria
Every non-regression run exit 0 = ALL PASS; git shows no core-file modification; all docs written;
Sprint-12 PROMPT self-contained (absolute paths + SPEC v0.22 only).