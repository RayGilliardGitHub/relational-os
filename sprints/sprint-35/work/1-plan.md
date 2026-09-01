# work/1-plan — GREEN BASELINE FIRST (Sprint-34 committed state)

Run the whole build as one command-set, every step exit 0, plain `python3` for demos and the
Sprint-0 venv `<VENV>/python` for conformance. All commands run from their own dir (CWD-sensitive).

## CR demo runners (18, the boundary-doc set) — from `instances/contested_reality`
run_two_path_demo, run_two_path_catalog_demo, run_capacity_rerank_demo, run_recorded_surface_demo,
run_forecast_{action,capacity,direction,horizon,horizon2,horizon3,horizon4,label_vs_choice,
per_option_capacity,variance,variance_all}_demo, run_cockpit_{q7q8,s7l}_demo,
run_adjudication_engine_demo.

## CR conformances (5) — Sprint-0 venv, from `instances/contested_reality`
conformance_{adjudication,dispute,interest,lifecycle,tradeoff}.py

## Sectors + reference + agent
- `instances/`: python3 build_all.py ; <venv> conformance_all.py
- `sprints/sprint-5/artifacts/`: python3 run_s5_demo.py ; <venv> run_s5_conformance.py
- `instances/agent_demo/`: python3 run_agent_demo.py ; <venv> conformance_agent.py

## Method
Run each via a simple sequential bash loop appending exit code + first RESULT/ALL-PASS/FAIL line to a
log file; then summarize. Every exit must be 0. No inline substitution in loop heads (parser-safe).