#!/usr/bin/env bash
R=/home/rlg/relational-os
echo "=== Sprint 35 files ==="
ls -1 "$R/sprints/sprint-35/"
echo
echo "=== docs/reports emitted ==="
ls -1 "$R/instances/contested_reality/artifacts/adjudication/reports/reproducibility.md"
ls -1 "$R/sprints/sprint-35/reproducibility.md"
ls -1 "$R/sprints/sprint-36/PROMPT.md"
echo
echo "=== invariants (must be unchanged) ==="
echo "engine:       $(sha256sum "$R/instances/contested_reality/adjudication_engine.py" | cut -c1-8)  (expect a60f8f7)"
echo "capacity_rr: $(sha256sum "$R/instances/contested_reality/capacity_rerank.py" | cut -c1-8)  (expect f7c6a185)"
echo "schema.yaml: $(sha256sum "$R/sprints/sprint-0/artifacts/schema/relational-os.schema.yaml" | cut -c1-8)  (expect 34264934)"
echo "$defs: $(python3 -c "import json;print(len(json.load(open('$R/sprints/sprint-0/artifacts/schema/relational-os.schema.json'))['\$defs']))")"
echo "spec: $(grep -m1 'Version:' "$R/SPEC.md")"
echo
echo "=== new runner once more (final ALL PASS check) ==="
cd "$R/instances/contested_reality" && python3 run_reproducibility_demo.py > /tmp/s35-final.log 2>&1
echo "EXIT=$?  FAILs=$(grep -c '\[FAIL\]' /tmp/s35-final.log)  PASSes=$(grep -c '\[PASS\]' /tmp/s35-final.log)"
grep "RESULT" /tmp/s35-final.log