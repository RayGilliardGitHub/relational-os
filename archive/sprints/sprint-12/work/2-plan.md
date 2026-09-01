# Sub-sprint 2 — Conformance gate over the lifecycle fixtures
## Objective
C1–C5 over `artifacts/lifecycle/fixtures`: prove every Sprint-12 additive field (epistemic_status on
claims, reliability/supports/provenance on evidence, interests/obligations/constraints/available_
resolutions, lifecycle_state/epistemic_state/determination/resolution_type/reopened, appeal/reopen
chains, trust error-vs-deception, UNRESOLVED) is schema-valid with the frozen 49 $defs + URI cap.
## Steps
Write `conformance_lifecycle.py` (mirror of `conformance_interest.py`, FIXTURES → lifecycle), run
with Sprint-0 venv. Pass + exit 0; no schema edit.
## Exit criteria
`conformance_lifecycle.py` → ALL PASS (C1–C5).