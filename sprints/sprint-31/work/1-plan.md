# work/1 — GREEN BASELINE (Sprint-30 state)

## Goal
Capture the exact Sprint-30 green state BEFORE adding any Sprint-31 source, so the new runner can be
proved non-regressive. Every command must run with real output; every exit code recorded.

## Steps
From `/home/rlg/relational-os/instances/contested_reality` (the CR cwd — wanted for runner CWD-sensitivity):
1. Plain python3 (demos), in order:
   run_forecast_label_vs_choice_demo.py  (Sprint 30)
   run_forecast_per_option_capacity_demo.py  (Sprint 29)
   run_forecast_horizon4_demo.py  (Sprint 28)
   run_forecast_horizon3_demo.py  (Sprint 27)
   run_forecast_horizon2_demo.py  (Sprint 26)
   run_forecast_horizon_demo.py  (Sprint 25)
   run_forecast_variance_all_demo.py
   run_forecast_variance_demo.py
   run_forecast_direction_demo.py
   run_forecast_action_demo.py
   run_forecast_capacity_demo.py
   run_cockpit_s7l_demo.py
   run_cockpit_q7q8_demo.py
   run_adjudication_engine_demo.py
   Each must print `RESULT: ALL PASS` / exit 0.
2. The 5 CR conformances with the Sprint-0 venv (absolute path
   `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python`):
   conformance_adjudication.py, conformance_dispute.py, conformance_interest.py,
   conformance_lifecycle.py, conformance_tradeoff.py  (exit 0 = ALL PASS).
3. Sectors: `python3 build_all.py` + `python3 conformance_all.py` (12 sectors), from `instances/`.
4. S5 reference: `sprints/sprint-5/artifacts/run_s5_demo.py` + `run_s5_conformance.py`.
5. Agent: `instances/agent_demo/run_agent_demo.py` + `conformance_agent.py`.
6. Capture invariants: `sha256sum adjudication_engine.py` (expect a60f8f7…), schema sha 7fc38c8c…,
   49 `$defs`, SPEC v0.22.

## Exit criteria (real output)
Every command returns exit 0; every demo prints ALL PASS; hashes unchanged. Record all in findings.