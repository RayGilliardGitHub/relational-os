#!/usr/bin/env python3
"""Sprint-6 BI snapshot — recompute the dashboard's ledger projections from the
emitted fixtures (the real data run_s5_demo.py wrote). Mirrors ros/bol.py's
project_on_time / project_settled_value / project_trust.

Usage:  python3 bi_snapshot.py [sprint-5-artifacts-dir]
Default: /home/rlg/relational-os/sprints/sprint-5/artifacts
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/home/rlg/relational-os/sprints/sprint-5/artifacts")

ledger = json.loads((ROOT / "fixtures/ledger/ledger-quoteko.json").read_text())
graph = json.loads((ROOT / "graph/current-state.json").read_text())

entries = ledger["entries"]
objects = graph["objects"]

# project_on_time: share of OUTCOME events carrying an on_time flag that are on time
rows = [e for e in entries if e.get("type") == "OUTCOME" and "on_time" in e]
on = sum(1 for e in rows if bool(e.get("on_time")))
print(f"project_on_time      -> {on}/{len(rows)} completions on time = "
      f"{on/len(rows):.3f}" if rows else "project_on_time      -> 0/0")

# project_settled_value: sum of settled EXCHANGE prices
settled = round(sum(float(e.get("price", 0.0))
                    for e in entries if e.get("type") == "EXCHANGE"), 2)
print(f"project_settled_value -> USD {settled}")

# project_trust: best scoped Trust for (target=solarworks, context=cust-cxn)
def proj_trust(target, context):
    best = None
    for o in objects:
        if o.get("uri", "").startswith("trust://") and o.get("target") == target \
                and o.get("context") == context:
            best = float(o.get("score", 0.0)) if best is None else max(best, float(o.get("score", 0.0)))
    return best
print(f"project_trust(solarworks, cust-cxn) -> {proj_trust('org://qk/solarworks', 'relationship://qk/cust-cxn')}")

# ledger integrity + counts (the audit trio)
ledger_ok = all(e.get("hash") and e.get("signature") for e in entries)
print(f"ledger entries = {len(entries)} | all content-addressed+signed = {ledger_ok}")
print(f"graph objects  = {len(objects)}")

# full-state round-trip: every graph object covered by a signed ledger state_update
covered = {o["uri"] for e in entries for o in (e.get("state_update") or [])}
missing = [o["uri"] for o in objects if o["uri"] not in covered]
print(f"round-trip: {len(objects)} graph objects covered by state_update "
      f"({'OK, none missing' if not missing else 'MISSING '+str(missing)})")