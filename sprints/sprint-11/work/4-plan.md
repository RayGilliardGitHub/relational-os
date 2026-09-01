# Sub-sprint 4 — Conformance gate over the trade-off fixtures

## Objective
Prove the Sprint-11 additive fields — the shared `constraint`/`interest` objects on relationships,
the `conflict` object on the case, the additive `recommendation` envelope (frozen `Recommendation`
$def shape incl. `tradeoff` + machine-readable `json` ranking), the `decision://` records with
authority, and the `UNRESOLVED`/`epistemic_state` additive fields — stay schema-valid with the
frozen 49 `$defs` and the frozen URI cap under C1–C5.

## Steps
1. Write `conformance_tradeoff.py` mirroring `conformance_interest.py`, pointing
   `conformance.FIXTURES` at `artifacts/tradeoff/fixtures`.
2. Run from instances/contested_reality with the Sprint-0 venv.

## Exit criteria
`conformance_tradeoff.py` → ALL PASS (C1–C5). This proves the additive recommendation/trade-off
does not need a schema edit and does not leak a `recommendation://` noun.