#!/usr/bin/env bash
# Sprint-6 capture: per-sprint conformance runners (run from each artifacts dir).
set -u
ROOT=/home/rlg/relational-os
VENV=$ROOT/sprints/sprint-0/artifacts/.venv/bin/python
W=$ROOT/sprints/sprint-6/work/captures
cd $ROOT/sprints/sprint-0/artifacts
"$VENV" "$ROOT/sprints/sprint-0/artifacts/run_conformance.py" > "$W/conf-s0.txt" 2>&1
echo "s0 run_conformance.py exit=$? last=$(tail -1 "$W/conf-s0.txt")"
cd $ROOT
for s in 1 2 3 4 5; do
  r=sprint-$s/artifacts/run_s${s}_conformance.py
  [ "$s" = "1" ] && r=sprint-1/artifacts/run_s1_conformance.py
  if [ -f "$r" ]; then
    (cd "$ROOT/$(dirname "$r")" && "$VENV" run_s${s}_conformance.py > "$W/conf-s$s.txt" 2>&1)
    ec=$?
    echo "s$s $(basename "$r") exit=$ec last=$(tail -1 "$W/conf-s$s.txt")"
  fi
done