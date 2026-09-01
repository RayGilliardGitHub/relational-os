#!/bin/bash
# work/3-nonreg-cr-demos.sh — all 20 CR demo runners (19 + run_corpus_consistency_demo); print name+exit
cd /home/rlg/relational-os/instances/contested_reality || exit 9
DEMOS=(run_adjudication_engine_demo.py run_cockpit_s7l_demo.py run_cockpit_q7q8_demo.py \
  run_forecast_action_demo.py run_forecast_capacity_demo.py run_forecast_direction_demo.py \
  run_forecast_horizon_demo.py run_forecast_horizon2_demo.py run_forecast_horizon3_demo.py \
  run_forecast_horizon4_demo.py run_forecast_label_vs_choice_demo.py run_forecast_per_option_capacity_demo.py \
  run_forecast_variance_demo.py run_forecast_variance_all_demo.py run_capacity_rerank_demo.py \
  run_recorded_surface_demo.py run_two_path_demo.py run_two_path_catalog_demo.py run_reproducibility_demo.py \
  run_corpus_consistency_demo.py)
FAIL=0
for d in "${DEMOS[@]}"; do
  python3 "$d" >/dev/null 2>&1
  rc=$?
  echo "CR-DEMO $d exit=$rc"
  if [ "$rc" -ne 0 ]; then FAIL=1; fi
done
echo "NONREG-CR-DEMOS-FAIL=$FAIL"
exit $FAIL