# SPRINT 6 — WORK (pre-drafting notes)

Real commands to run (each will be executed and its output embedded). Conformance uses the
Sprint-0 venv interpreter; demos use plain `python3`.

## Setup / verify
- `python3 --version`            (plain interpreter for demos)
- `sprints/sprint-0/artifacts/.venv/bin/python --version`   (venv interpreter for conformance)
- `sprints/sprint-0/artifacts/.venv/bin/python -m pip list` (show jsonschema/referencing/pyyaml deps) — for 02
- layout listing (dir tree of artifacts) — for 02/01

## Conformance (all six generations, ONE validator)  — for 03 + 04
- `sprints/sprint-0/artifacts/.venv/bin/python sprints/sprint-5/artifacts/run_s5_conformance.py`
  → covers sprint-0(156)/1(28)/2(35)/3(55)/4(174)/5(316) fixtures, exit 0.
- Per-generation runners for completeness (03 table): each run_*_conformance.py.

## Demos — for 03 + cockpit
- Daily cockpit: `cd sprints/sprint-5/artifacts && python3 run_s5_demo.py` → exit 0; writes
  `graph/current-state.json`, `fixtures/ledger/ledger-quoteko.json`, `reports/cockpit.md|.json`.
- Per-sprint demos (03 table): sprint-4 `run_s4_demo.py`, sprint-3 `run_s3_demo.py`,
  sprint-2 `run_s2_demo.py`, sprint-1 `run_demo.py` (note: name differs in sprint-1).

## Audit (04) — real checks
- `Ledger.verify()` hash-chain + signatures: executed inside run_s5_demo.py output
  ("ledger hash-chain + signatures: OK … entries N").
- Full-state round-trip: Graph rebuilds from Ledger ("N graph objects rebuilt from M events").
- Conformance C1–C5 = the audit's schema/instance/chain/roundtrip/statemachine coverage.
- §7F.1 mapping table: each check class → covering check today.

## BI (05) — real projections
- Read the emitted fixture and recompute projections on demand (executed snippet):
  from `sprints/sprint-5/artifacts` -> `project_on_time`, `project_settled_value`,
  `project_trust` over `fixtures/ledger/ledger-quoteko.json`.
- Business-health panel + prioritized attention + §7L answers: real content of
  `reports/cockpit.md` (embedded).
- §7G.1–.6 mapping: cockpit health/attention today vs production warehouse (P&L/BS/cash-flow) future.

## Outputs to save for embedding (under work/)
Save each command's stdout to `work/<name>.txt` so the docs embed verbatim real output:
- `conformance-all.txt`, `cockpit-run.txt`, `cockpit-final.md`, `bireport-snapshot.txt`,
  `venv-deps.txt`, `versions.txt`.

## Known naming nuance
- Sprint-1's demo runner is `run_demo.py`, not `run_s1_demo.py` (Sprints 2–5 use `run_sN_demo.py`).
- Sprint-3/4 artifact dirs also carry copies of earlier runners (they accumulate); the s5 runner
  is the canonical entry point that re-runs the whole S1→S5 chain + the operating layer.