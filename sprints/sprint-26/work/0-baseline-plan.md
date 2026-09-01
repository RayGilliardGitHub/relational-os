# WORK 0 — capture green baseline (Sprint-25/24/23/22 state) BEFORE any edit

Run from `instances/contested_reality/` (the runners are cwd-sensitive). Record real exit codes.

1. run_forecast_horizon_demo.py            # Sprint 25 (the direct predecessor)
2. run_forecast_variance_all_demo.py       # Sprint 24
3. run_forecast_variance_demo.py           # Sprint 23
4. run_forecast_direction_demo.py          # Sprint 22
5. run_forecast_action_demo.py             # Sprint 21
6. run_forecast_capacity_demo.py           # Sprint 20
7. run_cockpit_s7l_demo.py                 # Sprint 19 (engine-native §7L)
8. the 12 curated C-R demos + conformance_adjudication (16 labels)
9. build_all.py + conformance_all.py (sectors), S5 reference + conformance, agent_demo

Implemented as a shell loop that prints each runner's own RESULT line and the exit code;
stops/fails loudly on the first non-zero.