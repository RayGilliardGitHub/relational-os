#!/usr/bin/env bash
# Sprint-6 final DoD verification: fresh-run the canonical commands.
set -u
ROOT=/home/rlg/relational-os
VENV=$ROOT/sprints/sprint-0/artifacts/.venv/bin/python
cd "$ROOT/sprints/sprint-5/artifacts"
echo "1) daily cockpit:"
python3 run_s5_demo.py > /tmp/s6-demo.txt 2>&1; echo "   exit=$?  last=$(tail -1 /tmp/s6-demo.txt)"
echo "2) conformance all six:"
"$VENV" run_s5_conformance.py > /tmp/s6-conf.txt 2>&1; echo "   exit=$?  last=$(tail -1 /tmp/s6-conf.txt)"
echo "   c2 counts:"; grep -E 'C2 all fixture' /tmp/s6-conf.txt | sed 's/  \[PASS\] C2 all fixture instances validate \+ schemes \+ RFC3339  — /   /'
echo "3) SPEC version line:"
grep -m1 '^\*\*Version:\*\*\|Version:\*\*' "$ROOT/SPEC.md" 2>/dev/null || head -8 "$ROOT/SPEC.md"