# work/4 — documentation + hand-off

**Objective.** Record the config-authorable rule layer honestly, update the standing docs, and hand
off to Sprint 15.

## Artifacts
- `instances/contested_reality/docs/USER-AUTHORABLE-RULE-LAYER.md` (new): what became
  config-authorable (rule SELECTION + every parameter via `cfg["reconcile"]`), the registry + the 3
  shipped rules, the verdict-change proof (same engine, only config differs), what is STILL authored
  (the pure rule *mapping* body in the registry = Python; the *selection* is config — say so plainly),
  and the honest §16 verdict: is it now **A — Yes**, and on exactly what it still hinges.
- `instances/README.md`: append a Sprint-14 entry.
- `instances/contested_reality/docs/GENERALIZED-ADJUDICATION.md`: append a short additive note that
  Sprint 14 generalized the reconciliation rule layer (the §16 residual hinge #3 is closed).
- `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`: append an "Update after Sprint
  14" note.
- `sprints/sprint-14/summary.md` + `notes/findings.md`.
- `sprints/sprint-15/PROMPT.md` (next sprint, self-contained, absolute paths only).

## DoD
- All docs reflect real exit-0 output; the §16 verdict argues **A — Yes** only if a new rule is
  entirely config-selected (it is: the rule *name + params* are config; the mapping body is a
  registry Python function — state the boundary exactly).