# Sub-sprint 3 — Build `run_tradeoff_demo.py` (the informed-determination demo)

## Objective
A runnable demo (exit 0 = ALL PASS) that closes the §7K.1 gap: from the conflicting-interest
case's recorded constraints, the trade-off engine computes a defensible ranking, the human
adjudicator selects WITH that ranking in view, the §6 floor binds on unknown-cost options, and a
real local model's advisory (Sprint-8 pattern) is proven contained — it cannot set the
determination or Trust. All additive on existing primitives; no new noun/scheme.

## Structure
- Scenario 1 (coverage KNOWN): provision scene (Sprint-10 numbers) → case OPEN → trade-off rank →
  human (Manager) selects the top non-gated option `remote-with-coverage-plan` with the ranking in
  view, records `decision://` with authority; the case carries the additive `Recommendation`-shape
  `recommendation` object (incl. `tradeoff` + machine-readable `json` ranking).
- Scenario 2 (coverage UNKNOWN, §6): every staff-changing option is floor-gated → the machine's
  eligible direction is do-nothing/UNRESOLVED; the human authorizes `UNRESOLVED` /
  `INSUFFICIENT_EVIDENCE`; case stays OPEN; Trust untouched.
- Model overlay (Sprint-8 `agent_adapter`, real local model): advisory pick recorded as an
  effect-free `decision://`; if it chooses a floor-gated option it is contained (flagged, not
  actioned); the determination stays the human's; no trust:// write by the model.
- Emit fixtures under `artifacts/tradeoff/` (+ legal statemachine files) for C1–C5.

## Verification (Definition of Done assertions — all ALL PASS)
1. Ranking includes do-nothing/UNRESOLVED baseline.
2. Determined option's utility is computed and consistent (determination == top non-gated).
3. §6 floor triggers on irreversible/unknown-cost (all change-paths gated; human → UNRESOLVED;
   Trust untouched).
4. Advisory model cannot set the determination or Trust.
5. Authority/signature preserved (§7J.9).

## Exit criteria
`python3 run_tradeoff_demo.py` → RESULT: ALL PASS. Then sub-sprint 4 (conformance gate).