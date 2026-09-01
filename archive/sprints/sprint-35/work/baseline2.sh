#!/usr/bin/env bash
# Green baseline part 2: 5 CR conformances + sectors + S5 + agent. Exit 0 = all green.
V=/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python
LOG=/home/rlg/relational-os/sprints/sprint-35/work/1-baseline2.log
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
for r in conformance_adjudication conformance_dispute conformance_interest conformance_lifecycle conformance_tradeoff; do
  run "$CR" "$r" "$V" || { echo "FAIL $r"; exit 1; }
done
run /home/rlg/relational-os/instances build_all python3 || exit 1
run /home/rlg/relational-os/instances conformance_all "$V" || exit 1
run /home/rlg/relational-os/sprints/sprint-5/artifacts run_s5_demo python3 || exit 1
run /home/rlg/relational-os/sprints/sprint-5/artifacts run_s5_conformance "$V" || exit 1
run /home/rlg/relational-os/instances/agent_demo run_agent_demo python3 || exit 1
run /home/rlg/relational-os/instances/agent_demo conformance_agent "$V" || exit 1
echo "ALL BASELINE-2 GREEN"