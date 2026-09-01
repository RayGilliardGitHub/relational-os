# work/1-plan.md — Green baseline FIRST (before the new runner)

Run the whole CR corpus green baseline, each command exit 0. Two interpreters:
- demos / build_all / S5 demo / agent demo: plain `python3`
- conformances: Sprint-0 venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python`

18 canonical CR demo runners (per DECISION-FRAMEWORK-BOUNDARY.md §1) + the Sprint-35 runner = 19 CR demos.

## Commands (from instances/contested_reality)
```
python3 run_adjudication_engine_demo.py
python3 run_cockpit_s7l_demo.py
python3 run_cockpit_q7q8_demo.py
python3 run_forecast_action_demo.py
python3 run_forecast_capacity_demo.py
python3 run_forecast_direction_demo.py
python3 run_forecast_horizon_demo.py
python3 run_forecast_horizon2_demo.py
python3 run_forecast_horizon3_demo.py
python3 run_forecast_horizon4_demo.py
python3 run_forecast_label_vs_choice_demo.py
python3 run_forecast_per_option_capacity_demo.py
python3 run_forecast_variance_demo.py
python3 run_forecast_variance_all_demo.py
python3 run_capacity_rerank_demo.py
python3 run_recorded_surface_demo.py
python3 run_two_path_demo.py
python3 run_two_path_catalog_demo.py
python3 run_reproducibility_demo.py
```
5 CR conformances (Sprint-0 venv): conformance_adjudication / dispute / interest / lifecycle / tradeoff.
Sectors + reference: instances `build_all.py` + venv `conformance_all.py`; `sprints/sprint-5/artifacts`
`run_s5_demo.py` + venv `run_s5_conformance.py`; `instances/agent_demo` `run_agent_demo.py` + venv
`conformance_agent.py`.

## Verify
Every command reports ALL PASS / exit 0. Record hashes after too (must equal baseline).

## Artifact
notes/findings.md under sprint-36 with the real tail of each green command.