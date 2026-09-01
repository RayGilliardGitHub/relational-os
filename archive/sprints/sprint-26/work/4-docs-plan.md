# WORK 4 — documentation + roll-forward files

1. docs/ENGINE-FORECAST-ACTION.md — append Sprint-26 addendum: the Q3 forecast-driven attention
   `why` now appends the horizon-wide `band_horizon` range (shared `_HORIZON_BAND_PHRASE` constant,
   strict-prefix, verbatim with Q8/do-nothing), byte-identical default, honest no-data fallback.
2. docs/ENGINE-FORECAST-CAPACITY.md — append Sprint-26 addendum: the Q9 `capacity_planning_attention`
   {flag,why} derived from a recorded numeric capacity + recorded load + the horizon band (+
   threshold), ONE deterministic headroom/at-capacity/deficit rule, NEVER an invented number or a
   directive; absent when no capacity recorded (byte-identical superset).
3. instances/README.md — Sprint-26 entry.
4. /home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md — "Update after Sprint 26" note.
5. sprints/sprint-26/summary.md + notes/findings.md.
6. sprints/sprint-27/PROMPT.md — self-contained next-sprint prompt.
SPEC stays v0.22 (no normative gap surfaced).