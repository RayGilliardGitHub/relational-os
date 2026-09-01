#!/usr/bin/env bash
# Final verification: reference + financial + sectors, all gates.
set -u
ROOT=/home/rlg/relational-os
VENV=$ROOT/sprints/sprint-0/artifacts/.venv/bin/python
echo "1) REFERENCE (Quoteko) demo:"
(cd "$ROOT/sprints/sprint-5/artifacts" && python3 run_s5_demo.py >/tmp/f1.txt 2>&1); echo "   exit=$? last=$(tail -1 /tmp/f1.txt)"
echo "2) REFERENCE conformance (all six):"
(cd "$ROOT/sprints/sprint-5/artifacts" && "$VENV" run_s5_conformance.py >/tmp/f2.txt 2>&1); echo "   exit=$? last=$(tail -1 /tmp/f2.txt)"
echo "3) FINANCIAL instance build:"
(cd "$ROOT/instances/financial" && python3 run_fin.py >/tmp/f3.txt 2>&1); echo "   exit=$? last=$(tail -1 /tmp/f3.txt)"
echo "4) FINANCIAL conformance:"
(cd "$ROOT/instances/financial" && "$VENV" run_fin_conformance.py >/tmp/f4.txt 2>&1); echo "   exit=$? last=$(tail -1 /tmp/f4.txt)"
echo "5) ALL 11 SECTORS build:"
(cd "$ROOT/instances" && python3 build_all.py >/tmp/f5.txt 2>&1); echo "   exit=$? last=$(tail -1 /tmp/f5.txt)"
echo "6) ALL 11 SECTORS conformance:"
(cd "$ROOT/instances" && "$VENV" conformance_all.py >/tmp/f6.txt 2>&1); echo "   exit=$? last=$(tail -1 /tmp/f6.txt)"
echo "7) spec version + log line:"
grep -m1 '^\*\*Version:\*\*' "$ROOT/SPEC.md"