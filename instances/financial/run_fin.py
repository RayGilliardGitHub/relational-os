#!/usr/bin/env python3
"""Northglen Bank — run the financial-sector RelationalOS instance.

Builds the full S1->S5 chain + Business Operating Layer for the fictional commercial
bank, runs real PASS/FAIL checks (S1 authz, ledger/round-trip, Trust flywheel, §6 human
floor order in the ledger, S4 settlement artifacts, BOL lifecycle, health, cockpit),
emits the instance fixtures + graph + ledger, and writes the cockpit report.

Usage:  (from instances/financial/)  python3 run_fin.py     exit 0 = ALL PASS
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import fin_demo as fd                       # noqa: E402
from ros.s1 import S1Service, Permission, Denial   # noqa: E402
from ros.bol import project_on_time, project_settled_value, project_trust   # noqa: E402


def main() -> int:
    allok = True
    print("=== Northglen Bank — financial-sector RelationalOS instance (dogfood) ===\n")

    sub = fd.build_northglen()

    # ---- S1: role + relationship-scoped + capability-based authz + delegation ----
    s1 = S1Service(sub)
    rel = fd.LOAN_REL
    print("--- [S1] identity / role / authorization ---")
    role = s1.resolve_role(rel, fd.CLIENT, {"relationship": rel})
    ok = role == "borrower"; allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] borrower role resolved on loan-ops  — got {role}")
    other = s1.resolve_role("relationship://fin/not-a-rel", fd.CLIENT, {"relationship": rel})
    print(f"  [{'PASS' if other is None else 'FAIL'}] role is relationship-scoped  — got {other}")
    allok &= other is None
    perm = s1.authorize(fd.OPS, "rebalance_funding_allocation",
                        {"relationship": fd.FUND_REL, "delegation": "delegation://fin/treasury-ops"})
    ok = isinstance(perm, Permission); allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] delegation grants scoped capability  — {perm}")
    den = s1.authorize(fd.OPS, "rebalance_funding_allocation",
                       {"relationship": "relationship://fin/not-a-rel"})
    ok = isinstance(den, Denial); allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] authz denied outside any known relationship  — {den}")
    # §7B: revoking the delegation voids the capability immediately
    from types import SimpleNamespace
    clone = sub.clone_graph()
    d = clone.resolve("delegation://fin/treasury-ops"); d["status"] = "REVOKED"; clone.put(d)
    s1b = S1Service(SimpleNamespace(graph=clone))
    den2 = s1b.authorize(fd.OPS, "rebalance_funding_allocation",
                         {"relationship": fd.FUND_REL, "delegation": "delegation://fin/treasury-ops"})
    ok = isinstance(den2, Denial); allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] revoked delegation -> denial (capability voided)  — {den2}")

    # ---- Ledger integrity + full-state round-trip ----
    print("\n--- Ledger / Graph wiring (§3.16) ---")
    ok, why = sub.ledger.verify()
    allok &= ok
    print(f"  ledger hash-chain + signatures: {'OK' if ok else why} | entries {len(sub.ledger.entries)}")
    print(f"  graph current-state objects: {len(sub.graph.objects)}")
    rebuilt = {o["uri"]: o for e in sub.ledger.entries for o in (e.get("state_update") or [])}
    orig = {o["uri"]: o for o in sub.graph.to_dict()["objects"]}
    missing = [u for u in orig if u not in rebuilt]
    ok = not missing and len(orig) == len(rebuilt); allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] round-trip: {len(orig)} graph objects rebuilt "
          f"from {len(sub.ledger.entries)} events" + (f" (missing {missing})" if missing else ""))

    # ---- Trust flywheel re-rank ----
    print("\n--- [S5] trust flywheel (re-ranked next match) ---")
    m0 = fd._offs(sub)
    intent = fd.intent_for(sub)
    from ros.s2 import S2Service
    s2 = S2Service(sub)
    matches = s2.match_offers(intent, m0,
                              [{"target": k, "score": v} for k, v in fd._trust_map(sub).items()],
                              trust_floor=0.4)
    top = matches[0].offer_uri if matches else None
    ok = top == "offer://fin/o-adamvale"; allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] trust re-ranked next funding match to adamvale  — "
          f"top={top}, rank={[(m.offer_uri, m.trust) for m in matches]}")
    kaplen = sub.graph.get("trust://fin/t-kaplen"); adamvale = sub.graph.get("trust://fin/t-adamvale")
    ok = kaplen and adamvale and kaplen["score"] < 0.6 and adamvale["score"] > kaplen["score"]; allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] scoped trust moved as predicted (kaplen {kaplen['score']}, "
          f"adamvale {adamvale['score']})")

    # ---- §6 human floor: irreversible tranche release NOT auto-executed ----
    print("\n--- [§6] human-escalation floor (Ledger ORDER, not a flag) ---")
    entries = sub.ledger.entries
    def idx(uri):
        for n, e in enumerate(entries):
            if e.get("uri") == uri:
                return n
        return -1
    i_esc = idx("event://fin/s5-escalate")
    i_hum = idx("event://fin/treasurer-human")
    i_rel = idx("event://fin/action-tranche-release")
    ok = i_esc >= 0 and i_hum >= 0 and i_rel >= 0 and i_esc < i_hum < i_rel
    allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] §6 floor order in the ledger (escalate < human < release) "
          f"[{i_esc} < {i_hum} < {i_rel}]  — irreversible action gated by a signed human")
    esc = sub.graph.get("escalation://fin/escalate-tranche-release")
    ok = esc is not None and esc.get("trigger") and esc.get("recipient") == fd.TREASURER; allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] escalation:// recorded with trigger + recipient")

    # ---- S4 settlement artifacts ride one signed EXCHANGE event ----
    print("\n--- [S4] settlement artifacts as signed Ledger events ---")
    exch = [e for e in entries if e.get("uri") == "event://qk/s4-exchange-routed-adamvale"]
    ok = bool(exch) and bool(exch[0].get("signature")) and \
        all(u in {o["uri"] for o in (exch[0].get("state_update") or [])}
            for u in ("obligation://qk/s4-pay-routed-adamvale",
                      "receipt://qk/s4-receipt-routed-adamvale",
                      "decision://qk/s4-recon-routed-adamvale"))
    allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] obligation+receipt+reconciliation embedded in the signed EXCHANGE event")

    # ---- Business Operating Layer: case lifecycle + exception + learning ----
    print("\n--- [BOL] case lifecycle + exception heartbeat + learning ---")
    case = sub.graph.get(fd.CASE)
    hist = [h["status"] for h in (case or {}).get("history", [])]
    expected = ["OPEN", "TRIAGE", "ASSIGNED", "IN_PROGRESS", "BLOCKED", "RESOLVED", "CLOSED"]
    ok = hist == expected; allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] case lifecycle OPEN->...->CLOSED  — {hist}")
    ok = case and case.get("significance") == "CRITICAL" and case.get("root_cause_status") == "SUPPORTED"
    allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] exception heartbeat + root epistemic status (SUPPORTED)")
    learn = sub.graph.get(fd.LEARN)
    ok = learn and all(k in learn for k in ("expected", "actual", "why", "change_future_policy"))
    allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] Learning entry (§7K.1) recorded")
    pol = sub.graph.get(fd.POLICY)
    ok = pol and pol.get("version") == 3 and pol.get("learning") == fd.LEARN; allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] future policy updated by Learning (version {pol.get('version') if pol else None})")

    # ---- health + cockpit ----
    h = sub._meta["s52"]["health"]
    ok = len(h) == 3 and all("status" in x for x in h); allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] business-health panel: "
          + ", ".join(f"{x['name']}={x['status']}" for x in h))
    ok = (HERE / "artifacts/reports/cockpit.md").exists() and \
         (HERE / "artifacts/reports/cockpit.json").exists(); allok &= ok
    print(f"  [{'PASS' if ok else 'FAIL'}] cockpit report written (cockpit.md + .json)")

    # ---- cockpit §7L answer line ----
    c = sub._meta["s53"]
    print("\n======== COCKPIT ========")
    print(f"attention_line: {c['attention_line']}")
    print(f"AI recommendation -> {c['recommendation']['summary']}  "
          f"(authority {c['recommendation']['authority_required']}, "
          f"confidence {c['recommendation']['confidence']})")
    print(f"verified outcome: forward on-time {c['verified_outcome']['forward_on_time']}; "
          f"adamvale Trust -> {c['verified_outcome']['after_trust']}; learning {c['learning']}")
    print(f"ledger events {len(sub.ledger.entries)} | graph objects {len(sub.graph.objects)}")

    print("\n--- emitted instance files ---")
    if "__main__" == "__main__":
        for name, path in fd.emit(sub).items():
            print(f"  wrote {name} -> file://{path}")

    print("\nRESULT:", "ALL PASS" if allok else "FAILURES PRESENT")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())