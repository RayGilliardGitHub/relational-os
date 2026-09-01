"""Build the Sprint-3 orchestration + human floor on the Sprint-2 S5 state.

Chains the full §5 loop on ONE relationship (relationship://qk/cust-cxn):
  S1 identity/role/authz -> S2 intent/match (initial) -> first S5 trust cycle (Sprint-2)
  -> S3 commit + execute across the fleet over the routing seam (REVERSIBLE tasks auto-run,
     IRREVERSIBLE final-payment escalates to person://qk/approver, human approves, then run)
  -> 2nd S5 capture/update on the S3-executed outcome -> S2 re-ranks the NEXT cycle (flywheel).

Reuses the Sprint-1 substrate (make_fixtures) and Sprint-2 S5 engine (s5_demo.build_s2).
Emits Sprint-3 fixtures (commitment/trust/evidence/claim/decisions/events/relationship/
actors_offers + ledger + graph + statemachines), validated by the reused Sprint-0 validator.
"""
from __future__ import annotations

import json
from pathlib import Path

from ros.substrate import Substrate
from ros.s1 import S1Service
from ros.s2 import S2Service
from ros.s3 import S3Service
from ros.s5 import S5Service, config_defaults
from ros.substrate import now_iso
import s5_demo

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
LEDGER_DIR = FIXTURES / "ledger"
SM_DIR = FIXTURES / "statemachines"
GRAPH_DIR = HERE / "graph"

CTX = "relationship://qk/cust-cxn"
SUBJ = "org://quoteko"
CLAIM = "roofing & repair reliability"
APPROVER = "person://qk/approver"


def _trust_map(sub) -> dict:
    """target -> scoped score (the §3.14 keyed trust for the relationship)."""
    return {o["target"]: float(o.get("score", 0.0))
            for o in sub.graph.objects.values()
            if o.get("uri", "").startswith("trust://")}


def _offs(sub) -> list[dict]:
    return [o for o in sub.graph.objects.values() if o.get("uri", "").startswith("offer://")]


def _seed_s3_fleet(sub, i: int) -> None:
    """Provision the S3 orchestrator + worker fleet with bounded delegations (§3.4/§7B)."""
    s3 = S3Service(sub)
    fleet = [
        {"uri": "agent://s3", "type": "AGENT"},
        {"uri": "agent://w-local", "type": "AGENT"},
        {"uri": "agent://w-cloud", "type": "AGENT"},
        {"uri": "agent://w-frontier", "type": "AGENT"},
    ]
    relations = [
        {"uri": "delegation://qk/s3-execute", "grantor": "org://quoteko",
         "grantee": "agent://s3", "scope": ["rule://qk/s3-run"], "status": "ACTIVE"},
        {"uri": "delegation://qk/w-local", "grantor": "org://quoteko",
         "grantee": "agent://w-local", "scope": ["rule://qk/w-local-run"], "status": "ACTIVE"},
        {"uri": "delegation://qk/w-cloud", "grantor": "org://quoteko",
         "grantee": "agent://w-cloud", "scope": ["rule://qk/w-cloud-run"], "status": "ACTIVE"},
        {"uri": "delegation://qk/w-frontier", "grantor": "org://quoteko",
         "grantee": "agent://w-frontier", "scope": ["rule://qk/w-frontier-run"],
         "status": "ACTIVE"},
        {"uri": "authority://qk/for-exec", "grants": ["release_final_payment",
                                                      "approve_final_payment"],
         "holder": "org://quoteko"},
        {"uri": "rule://qk/s3-run", "kind": "POLICY",
         "text": "S3 orchestrator may split + commit a matched job under Quoteko",
         "grants": ["orchestrate", "split_work", "commit_job"]},
        {"uri": "rule://qk/w-local-run", "kind": "POLICY",
         "text": "local worker prepares work order + schedule (reversible)",
         "grants": ["prepare_work_order_and_schedule"]},
        {"uri": "rule://qk/w-cloud-run", "kind": "POLICY",
         "text": "cloud worker dispatches + verifies materials (reversible)",
         "grants": ["dispatch_dispatcher_and_verify_materials"]},
        {"uri": "rule://qk/w-frontier-run", "kind": "POLICY",
         "text": "frontier worker may release final payment ONLY after human acknowledgement",
         "grants": ["release_final_payment"]},
    ]
    sub.record(s3._ev("STATE_CHANGE", "event://qk/s3-provision", "agent://s1", i,
                      "provision S3 orchestrator + worker fleet with bounded delegations",
                      fleet + relations),
               signer="agent://s1")


def build_s3(sub: Substrate) -> dict:
    """Extend `sub` (Sprint-2 state) through the S3 cycle + 2nd S5 update + next S2 rank.

    Returns a summary dict for the demo printer.
    """
    s1 = S1Service(sub)
    s2 = S2Service(sub)
    s3 = S3Service(sub)
    s5 = S5Service(sub)
    cfg = config_defaults()

    _seed_s3_fleet(sub, 2000)
    identity = sub._meta["identity"] if hasattr(sub, "_meta") else "person://qk/customer"

    rs = {}
    # ---- S2 (2nd engagement, same relationship) ----------------------------
    intent2 = s2.infer_intent(identity, {
        "request": "Skylight and gutter leaking around the roof seam — urgent, quote ASAP.",
        "budget": 18000})
    offers = _offs(sub)
    trusts = _trust_map(sub)
    match2 = s2.match_offers(intent2, offers,
                             [{"target": k, "score": v} for k, v in trusts.items()],
                             trust_floor=0.5)
    top = match2[0]
    provider = top.provider

    # human verification floor (engaging a provider is itself irreversible, §7B)
    sub.record(s3._ev("DECISION", "event://qk/s3-human-accept", identity, 2010,
                      f"customer verified & accepted {top.offer_uri} (2nd engagement) -> engage",
                      [{"uri": "decision://qk/s3-human-accept", "by": identity,
                        "authority": "authority://qk/for-exec",
                        "alternatives": [m.offer_uri for m in match2[1:]],
                        "confidence": 1.0, "expected_outcome": f"engage {provider}",
                        "actual_outcome": "accepted", "made_at": now_iso()}]),
               signer=identity)

    # ---- S3 commit (§5: commitment = agree(offer, terms)) -------------------
    offer = [o for o in offers if o["uri"] == top.offer_uri][0]
    commitment = s3.commit(offer, {"price": offer["price"], "currency": offer["currency"],
                                   "warranty": "5yr", "signed": True},
                           by="agent://s3", i=2020, signer="agent://s3")

    # ---- S3 orchestrate + execute across the fleet ---------------------------
    workers = {"w-local": "agent://w-local", "w-cloud": "agent://w-cloud",
               "w-frontier": "agent://w-frontier"}
    tasks = s3.orchestrate(commitment, workers, trusts, i=2030)
    ctx = {"relationship": CTX}
    executed = []
    escalated = None
    for t in tasks:
        if t.tier == "human":                      # irreversible -> no auto-execution
            escalated = t
            continue
        ev = s3.execute_task(t, ctx, i=2040 + int(t.task_id[-1]))
        if ev:
            executed.append(ev)

    # ---- 3.2 human floor: escalate the irreversible action ------------------
    esc_decision = s3.escalate_to_human(escalated, APPROVER, commitment, i=2050)
    human_decision = s3.human_acknowledge(escalated, APPROVER,
                                          "authority://qk/for-exec", commitment, i=2060)
    # ONLY NOW, after the signed human acknowledgement, may the irreversible act run.
    final_event = s3.execute_task(escalated, ctx, i=2070)

    # ---- 2nd S5 cycle: capture the S3-executed outcome -> trust update -------
    job = {"uri": "event://qk/outcome-solarworks-s3", "job": "job-solarworks-s3",
           "provider": provider, "committed_deadline": "2026-10-01T00:00:00Z",
           "actual_completed_at": "2026-09-29T00:00:00Z"}  # ON TIME -> good outcome
    evidence2, on_time = s5.capture(job, s5_demo.PROVENANCE, signer=provider, i=3000)
    vr = s5.verify(evidence2, f"{provider} completed {job['job']} by its committed deadline",
                   job, i=3001)
    trust2 = s5.update_trust(subject=SUBJ, target=provider, claim=CLAIM, context=CTX,
                             verify=vr, evidence_score=vr.degree, i=3002,
                             alpha=cfg["alpha"], expectation=cfg["expectation"],
                             recency=cfg["recency"])

    # ---- S2 re-ranks the NEXT cycle under the updated Trust (flywheel, closed)
    trusts3 = _trust_map(sub)
    next_rank = s2.match_offers(intent2, offers,
                                [{"target": k, "score": v} for k, v in trusts3.items()],
                                trust_floor=0.5)

    summary = {
        "identity": identity, "intent2": intent2, "match2": [m.to_dict() for m in match2],
        "commitment": commitment, "tasks": [t.to_dict() for t in tasks],
        "executed": [e["uri"] for e in executed],
        "escalated": escalated.to_dict() if escalated else None,
        "escalation_decision": esc_decision["uri"],
        "human_decision": human_decision["uri"],
        "final_event": final_event["uri"] if final_event else None,
        "evidence2": evidence2, "trust2": trust2, "next_rank": [m.to_dict() for m in next_rank],
    }
    sub._meta.update({f"s3_{k}": v for k, v in summary.items()})
    return summary


def emit_s3_fixtures(sub: Substrate) -> dict[str, Path]:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    by_uri = {}
    for e in sub.ledger.entries:
        for obj in e.get("state_update") or []:
            by_uri[obj["uri"]] = obj

    def dump_grp(name, prefixes):
        items = [o for u, o in by_uri.items()
                 if u.startswith(tuple(f"{p}://" for p in prefixes))]
        p = FIXTURES / "s3" / f"{name}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(items, indent=2))
        return p

    files = [
        dump_grp("commitment", ["commitment"]),
        dump_grp("trust", ["trust"]),
        dump_grp("evidence", ["evidence"]),
        dump_grp("claim", ["claim"]),
        dump_grp("decisions", ["decision"]),
        dump_grp("events", ["event"]),
        dump_grp("relationship", ["relationship", "interaction", "consent",
                                  "delegation", "authority"]),
        dump_grp("actors_offers", ["person", "org", "agent", "entity", "rule", "offer"]),
    ]
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    lf = LEDGER_DIR / "ledger-quoteko.json"
    lf.write_text(json.dumps(sub.ledger.to_dict(), indent=2))
    files.append(lf)

    SM_DIR.mkdir(parents=True, exist_ok=True)
    rf = SM_DIR / "relationship.json"
    rf.write_text(json.dumps({"uri": "relationship://qk/cust-cxn",
                              "states": ["PROPOSED", "ACTIVE"]}))
    files.append(rf)

    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    gf = GRAPH_DIR / "current-state.json"
    gf.write_text(json.dumps(sub.graph.to_dict(), indent=2))
    files.append(gf)
    return {f.name: f for f in files}


if __name__ == "__main__":
    sub = s5_demo.build_s2()
    summary = build_s3(sub)
    print("S3 cycle summary:", json.dumps(summary, indent=2, default=str))
    emitted = emit_s3_fixtures(sub)
    for name, path in emitted.items():
        print(f"  wrote {name} -> file://{path}")