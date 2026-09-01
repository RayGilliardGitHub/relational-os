#!/usr/bin/env python3
"""Northglen BI snapshot — recompute the projections from the emitted finance fixtures.

Mirrors 05-bi-reports.md's documented BI read (projection functions over the ledger),
applied to the Northglen Bank instance instead of Quoteko. Pure read of the produced
fixtures; no ros import needed.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = HERE / "artifacts"
ledger = json.loads((ART / "fixtures/ledger/ledger-northglen.json").read_text())
graph = json.loads((ART / "graph/current-state.json").read_text())
entries = ledger["entries"]
objects = graph["objects"]

rows = [e for e in entries if e.get("type") == "OUTCOME" and "on_time" in e]
on = sum(1 for e in rows if bool(e.get("on_time")))
tagline = "Funding that lands on the date."
print(f"# Northglen Bank — {tagline}   (BI snapshot; company-branding component, Sprint 7)")
print(f"project_on_time      -> {on}/{len(rows)} committed settlements on time = {on/len(rows):.3f}")

settled = round(sum(float(e.get("price", 0.0))
                    for e in entries if e.get("type") == "EXCHANGE"), 2)
print(f"project_settled_value -> USD {settled}")

def proj_trust(target, context):
    best = None
    for o in objects:
        if o.get("uri", "").startswith("trust://") and o.get("target") == target \
                and o.get("context") == context:
            best = float(o.get("score", 0.0)) if best is None else max(best, float(o.get("score", 0.0)))
    return best
print(f"project_trust(adamvale, funding-net) -> {proj_trust('org://fin/adamvale', 'relationship://fin/funding-net')}")
print(f"project_trust(kaplen,   funding-net) -> {proj_trust('org://fin/kaplen',   'relationship://fin/funding-net')}")

ok = all(e.get("hash") and e.get("signature") for e in entries)
print(f"ledger entries = {len(entries)} | all content-addressed+signed = {ok}")
print(f"graph objects  = {len(objects)}")