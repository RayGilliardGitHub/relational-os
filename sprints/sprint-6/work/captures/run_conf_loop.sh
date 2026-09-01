#!/usr/bin/env bash
ROOT=/home/rlg/relational-os
VENV=$ROOT/sprints/sprint-0/artifacts/.venv/bin/python
W=$ROOT/sprints/sprint-6/work/captures
for s in 1 2 3 4 5; do
  dir="sprints/sprint-$s/artifacts"
  rn="run_s${s}_conformance.py"
  if [ -f "$ROOT/$dir/$rn" ]; then
    ( cd "$ROOT/$dir" && "$VENV" "$rn" > "$W/conf-s$s.txt" 2>&1 )
    ec=$?
    echo "s$s $rn exit=$ec"
  else
    echo "s$s MISSING $ROOT/$dir/$rn"
  fi
done