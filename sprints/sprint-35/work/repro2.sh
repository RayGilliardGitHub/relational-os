#!/usr/bin/env bash
cd /home/rlg/relational-os/instances/contested_reality
python3 run_reproducibility_demo.py > /tmp/s35-repro2.log 2>&1
echo "EXIT=$?"
echo "FAILs=$(grep -c '\[FAIL\]' /tmp/s35-repro2.log)  PASSes=$(grep -c '\[PASS\]' /tmp/s35-repro2.log)"
grep -E "RESULT|taxonomy" artifacts/adjudication/reports/reproducibility.md