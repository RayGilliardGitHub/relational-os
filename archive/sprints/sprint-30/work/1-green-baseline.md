# work/1-green-baseline.md — capture the Sprint-29 green state BEFORE any Sprint-30 work

Goal: prove the tree is green at the Sprint-29 state so any regression I add later is attributable to
Sprint 30. Then confirm `adjudication_engine.py` hash so I can assert it is untouched at the end.

Run (plain python3, from instances/contested_reality unless noted), capture each real exit code:
1. run_forecast_per_option_capacity_demo.py      (Sprint 29 new runner)
2. run_forecast_horizon4_demo.py                 (Sprint 28)
3. run_forecast_horizon3_demo.py                 (Sprint 27)
4. run_forecast_horizon2_demo.py                 (Sprint 26)
5. run_forecast_horizon_demo.py                  (Sprint 25)
6. run_forecast_variance_all_demo.py             (Sprint 25)
7. run_forecast_variance_demo.py                 (Sprint 23)
8. run_forecast_direction_demo.py                (Sprint 22)
9. run_forecast_action_demo.py                   (Sprint 21)
10. run_forecast_capacity_demo.py                (Sprint 20)
11. run_cockpit_s7l_demo.py                      (Sprint 19)
12. run_cockpit_q7q8_demo.py                     (Sprint 18)
13. run_adjudication_engine_demo.py              (Sprint 13)
Then Sprint-0 venv for conformances: conformance_adjudication, conformance_dispute, conformance_interest,
conformance_lifecycle, conformance_tradeoff (5).
Then instances/: build_all.py + conformance_all.py (12 sectors), S5 reference run_s5_demo.py +
run_s5_conformance.py, agent run_agent_demo.py + conformance_agent.py.
Then schema raw sha256 + 49-$defs count + `grep -rl '://qk/'` (no qk segment) to assert invariants.