#!/usr/bin/env bash
# Sprint 35 full non-regression AFTER the new runner: 19 CR demos + 5 conformances + sectors + S5 + agent.
V=/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python
LOG=/home/rlg/relational-os/sprints/sprint-35/work/4-nonreg.log
: > "$LOG"
run() {
  local dir=$1 name=$2 interp=$3
  out=$(cd "$dir" && "$interp" "$name.py" 2>&1)
  local code=$?
  local res=$(printf '%s' "$out" | grep -E "ALL PASS|RESULT|PASS|FAIL|ERROR" | tail -1)
  printf '%s\t%s\texit=%s\t%s\n' "$dir" "$name" "$code" "$res" >> "$LOG"
  return $code
}
CR=/home/rlg/relational-os/instances/contested_reality
for r in run_two_path_demo run_two_path_catalog_demo run_capacity_rerank_demo run_recorded_surface_demo \
  run_forecast_action_demo run_forecast_capacity_demo run_forecast_direction_demo run_forecast_horizon_demo \
  run_forecast_horizon2_demo run_forecast_horizon3_demo run_forecast_horizon4_demo run_forecast_label_vs_choice_demo \
  run_forecast_per_option_capacity_demo run_forecast_variance_demo run_forecast_variance_all_demo \
  run_cockpit_q7q8_demo run_cockpit_s7l_demo run_adjudication_engine_demo run_reproducibility_demo; do
  run "$CR" "$r" python3 || { echo "FAIL $r"; exit 1; }
done
for r in conformance_adjudication conformance_dispute conformance_interest conformance_lifecycle conformance_tradeoff; do
  run "$CR" "$r" "$V" || { echo "FAIL $r"; exit 1; }
done
run /home/rlg/relational-os/instances build_all python3 || exit 1
run /home/rlg/relational-os/instances conformance_all "$V" || exit 1
run /home/rlg/relational-os/sprints/sprint-5/artifacts run_s5_demo python3 || exit 1
run /home/rlg/relational-os/sprints/sprint-5/artifacts run_s5_conformance "$V" || exit 1
run /home/rlg/relational-os/instances/agent_demo run_agent_demo python3 || exit 1
run /home/rlg/relational-os/instances/agent_demo conformance_agent "$V" || exit 1
echo "ALL NON-REGRESSION GREEN"
echo "--- engine hash ---"; sha256sum /home/rlg/relational-os/instances/contested_reality/adjudication_engine.py | cut -c1-8
echo "--- capacity_rerank hash ---"; sha256sum /home/rlg/relational-os/instances/contested_reality/capacity_rerank.py | cut -c1-8