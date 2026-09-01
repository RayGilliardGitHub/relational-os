#!/usr/bin/env bash
# RelationalOS reference-build green/red gate (in-tree copy of the runbook's verify.sh).
# Runs the daily cockpit (whole build) + conformance-all-six and reports result.
# Usage: bash scripts/verify.sh [repo-root]   (default = the repo root containing this script)
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${1:-$SCRIPT_DIR/..}"
REF=$ROOT/reference
SCHEMA=$ROOT/schema
VENV=$ROOT/.venv/bin/python
FLAGS=0

if [ ! -d "$REF" ]; then echo "ERR: no reference build dir at $REF"; exit 2; fi

step() { echo; echo "== $1 =="; }

step "1) daily cockpit (S1-S5 + BOL, writes graph/ledger/cockpit)"
( cd "$REF" && python3 run_s5_demo.py > /tmp/relos-demo.txt 2>&1 )
ec=$?; echo "exit=$ec last=$(tail -1 /tmp/relos-demo.txt)"; [ $ec -ne 0 ] && FLAGS=$((FLAGS+1))

if [ -x "$VENV" ]; then
  step "2) conformance all-six generations"
  ( cd "$SCHEMA" && "$VENV" run_conformance_all.py > /tmp/relos-conf.txt 2>&1 )
  ec=$?; echo "exit=$ec last=$(tail -1 /tmp/relos-conf.txt)"; [ $ec -ne 0 ] && FLAGS=$((FLAGS+1))
  echo "C2 instance counts:"
  grep -E 'C2 all fixture' /tmp/relos-conf.txt | sed 's/  \[PASS\] C2 all fixture instances validate \+ schemes \+ RFC3339  — /   /'
else
  echo "WARN: venv missing at $VENV — rebuild per docs/02-setup (python3 -m venv + pip install jsonschema referencing pyyaml)"
  FLAGS=$((FLAGS+1))
fi

echo
echo "SUMMARY: $([ $FLAGS -eq 0 ] && echo 'ALL GREEN (exit 0)' || echo "$FLAGS FAILURES") "
exit $FLAGS