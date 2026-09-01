"""Build the Sprint-5 Business Operating Layer demo on the Sprint-4 (S1->S5) state.

  5.1  Case-led loop + exception heartbeat + Learning (§7J.2/§7J.3/§7K.1): open the
       case://qk/c-on-time-delivery on a ledger-projected exception (on-time delivery
       0.80 < 0.95 target), drive it OPEN->TRIAGE->ASSIGNED->IN_PROGRESS->BLOCKED->
       RESOLVED->CLOSED with signed evidence per transition, close an
       Exception->Case->Task->verified-outcome cycle, and record a Learning entry
       (decision:// with Expected->Actual->Variance->WHY->change-future-policy) plus a
       future-policy change on policy://qk/provider-allocation.

  5.2  Goals / Metrics / Priority / Dependency (§7J.1/§7J.5/§7J.6): Goal->Metric->Actual
       ->Variance->Decision->Action->Outcome; Priority = f(impact, urgency, confidence,
       irreversibility, relationship-importance, cost-of-delay); dependencies with a
       transitive impact analysis on the exception->case->task chain; business-health
       panel derived from ledger projections.

  5.3  The Cockpit (§7J.9) + the §7L ten questions answered with evidence; #8 becomes the
       assigned, authorized task that closes in a verified, learned outcome (#10).

Every object is carried by a signed Ledger event's state_update (full-coverage rule,
§3.16 / sprint notes). URI cap honoured — no new schemes, no new nouns.
"""
from __future__ import annotations

import json
from pathlib import Path

from ros.substrate import Substrate, now_iso
from ros.s3 import S3Service, Task
from ros.s2 import S2Service
from ros.s4 import S4Service
from ros.s5 import S5Service, config_defaults
from ros.bol import (BolService, project_on_time, project_settled_value,
                     project_trust)
import s3_demo
import s5_demo
import s4_demo

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
LEDGER_DIR = FIXTURES / "ledger"
SM_DIR = FIXTURES / "statemachines"
GRAPH_DIR = HERE / "graph"
REPORTS = HERE.parent / "reports"   # repo-root reports/ (ros/checks.cockpit_check reads it there)

SUBJ = "org://quoteko"
APPROVER = "person://qk/approver"
CTX = "relationship://qk/cust-cxn"
PERSON = "person://qk/customer"
CLAIM = "roofing & repair reliability"
OPS_AUTH = "authority://qk/for-operations"
WORKER = "agent://w-ops"
ON_TIME_METRIC = "metric://qk/m-on-time"
GOAL = "goal://qk/g-customer-trust"
CASE_URI = "case://qk/c-on-time-delivery"
TASK_R = "task://qk/t-provider-rebalance"
TASK_F = "task://qk/t-followup-routed"
POLICY = "policy://qk/provider-allocation"


def _trust_map(sub) -> dict:
    return {o["target"]: float(o.get("score", 0.0))
            for o in sub.graph.objects.values()
            if o.get("uri", "").startswith("trust://")}


def _offs(sub) -> list[dict]:
    return [o for o in sub.graph.objects.values() if o.get("uri", "").startswith("offer://")]


def _expect_obj(slug: str, buyer: str, subject: str, price: float,
                due: str) -> dict:
    return {"uri": f"expectation://qk/e-s5-{slug}", "actor": buyer, "subject": subject,
            "condition": "full and on-time settlement of the agreed value",
            "metric": "settled_value", "threshold": price, "deadline": due,
            "evidence_required": "CLEAR"}


# ===========================================================================
# 5.1 — Case-led loop + exception heartbeat + Learning
# ===========================================================================
def build_s51(sub: Substrate) -> dict:
    s2 = S2Service(sub); s3 = S3Service(sub); s4 = S4Service(sub)
    s5 = S5Service(sub); bol = BolService(sub)
    cfg = config_defaults()
    i = 7000

    # --- operating-layer base: authority, ops worker (delegated), expectations ---
    bol.prov(i, "agent://s5",
             f"provision operating-layer base (authority + ops worker + policy + expectation)",
             [
                 {"uri": OPS_AUTH, "holder": SUBJ,
                  "grants": ["triage_case", "assign_case", "close_case", "approve_learning",
                             "rebalance_provider_allocation", "gate_provider_performance"],
                  "roles": ["operations"]},
                 {"uri": WORKER, "type": "AGENT"},
                 {"uri": "rule://qk/w-ops-run", "kind": "POLICY",
                  "text": "ops worker may re-balance provider allocation and gate performance",
                  "grants": ["rebalance_provider_allocation", "gate_provider_performance"]},
                 {"uri": "delegation://qk/w-ops", "grantor": SUBJ, "grantee": WORKER,
                  "scope": ["rule://qk/w-ops-run"], "status": "ACTIVE"},
                 {"uri": "expectation://qk/e-on-time-delivery",
                  "actor": APPROVER, "subject": "contracted-work completion",
                  "condition": "complete the contracted job by its committed deadline",
                  "metric": "on_time", "threshold": 0.95,
                  "deadline": "2026-09-30T00:00:00Z", "evidence_required": "CLEAR"},
                 {"uri": POLICY, "name": "provider allocation",
                  "condition": "a new contracted job is to be allocated",
                  "decision": "select the provider with the highest fit x scoped delivery Trust",
                  "action": "allocate to the top-ranked fitted provider",
                  "scope": ["expectation://qk/e-on-time-delivery"], "version": 1},
                 {"uri": "process://qk/pr-delivery",
                  "definition": "exception -> open case -> assign -> execute -> verify -> learn -> close",
                  "steps": ["triage", "assign", "execute", "verify_outcome", "learning"]},
                 {"uri": "process_instance://qk/pi-on-time",
                  "process": "process://qk/pr-delivery", "status": "RUNNING",
                  "started_at": (now_iso())},
             ])
    i += 1

    # --- ledger-projected exception (the �matter): on-time delivery < target ---
    on, total = project_on_time(sub)
    actual = on / total if total else 1.0
    expected = 0.95
    cpu = project_trust(sub, "org://qk/solarworks", CTX) or 0.0

    case = bol.open_case(
        CASE_URI, "quarterly on-time fulfilment below target", APPROVER,
        [SUBJ, APPROVER, WORKER], [CTX],
        i, "agent://s5",
        suggestion="ledger-projected on-time rate below target",
    )
    i += 1

    # exception heartbeat (§7J.2) as additive fields on the case
    case = bol.exception_heartbeat(
        case, expected, round(actual, 3), "CRITICAL",
        f"On-time delivery {actual:.2f} below target {expected:.2f} "
        f"(ledger: {on}/{total} contracted completions on time)",
        "provider scheduling failure — org://qk/norcrete missed its committed deadline "
        "by 2 days; scoped Trust fell 0.92->0.528",
        "SUPPORTED",                                  # §7K.2 epistemic status
        "Re-allocate contracted work to the verified on-time provider "
        "(org://qk/solarworks) and gate the laggard (org://qk/norcrete) with a "
        "performance checkpoint before any new commitment",
        ON_TIME_METRIC,
    )
    bol.prov(i, "agent://s5", "record exception heartbeat on the case", [case])
    i += 1

    # --- TRIAGE ---
    bol.prov(i, "agent://s5", "case triage: exception assessed, root nominated",
             [{"uri": "decision://qk/s5-triage", "by": "agent://s4",
               "authority": OPS_AUTH, "alternatives": ["accept", "dismiss as anomaly"],
               "confidence": 0.85,
               "expected_outcome": "accept as a real on-time risk",
               "actual_outcome": "accepted; root (norcrete scheduling) nominated",
               "made_at": now_iso()}])
    case = bol.transition_case(case, "TRIAGE", i, "agent://s5",
                               "case triaged: the on-time variance is significant",
                               "event://qk/s5-case-triage")
    i += 1

    # --- ASSIGNED + the §7L#8 task becomes assigned, authorized work ---
    pri = bol.priority(impact=0.85, urgency=0.90, confidence=0.70,
                       irreversible=False, relationship_importance=0.80,
                       cost_of_delay=0.75)
    task = {
        "uri": TASK_R, "assigned_to": WORKER, "created_by": "agent://s5",
        "objective": "re-balance provider allocation to the verified on-time provider "
                     "(solarworks) and gate the laggard (norcrete)",
        "dependencies": [], "authority": OPS_AUTH,
        "deadline": "2026-10-01T00:00:00Z", "priority": pri["score"],
        "status": "ASSIGNED",
        "expected_outcome": "next contracted job routed to a verified on-time provider; policy updated",
        "why_here": "derived from the on-time delivery exception (case OPEN)",
        "importance": "restores on-time fulfilment, protecting customer scoped Trust",
        "evidence": ["evidence://qk/job-norcrete", "evidence://qk/job-solarworks"],
        "decision_required": "approve the provider re-allocation",
        "priority_factors": pri["factors"], "assigned_capacity": 1.0,
    }
    bol.prov(i, "agent://s5",
             "case assigned; task t-provider-rebalance becomes assigned authorized work (#8)",
             [task, {"uri": "decision://qk/s5-assign", "by": APPROVER,
                     "authority": OPS_AUTH, "alternatives": ["assign", "defer"],
                     "confidence": 0.95, "expected_outcome": "task in progress",
                     "detail": {"task": TASK_R, "assigned_to": WORKER,
                                "authority": OPS_AUTH,
                                "priority": pri["score"],
                                "capacity": task["assigned_capacity"]},
                     "made_at": now_iso()}])
    case = bol.transition_case(case, "ASSIGNED", i, "agent://s5",
                               "case assigned; owner approver + ops worker",
                               "event://qk/s5-case-assigned")
    i += 1

    # --- IN_PROGRESS: execute the task (worker ACTION + policy change + re-rank) ---
    case = bol.transition_case(case, "IN_PROGRESS", i, "agent://s5",
                               "task execution began; provider mix being re-balanced",
                               "event://qk/s5-case-inprogress")
    i += 1
    # the ops worker performs the bounded action via its delegation (capability-gated)
    worker_task = Task("t-rebalance", "rebalance_provider_allocation", WORKER, "local",
                       reversible=True, cost_knowable=True, delegation="delegation://qk/w-ops")
    s3.route_seam(worker_task, _trust_map(sub).get(SUBJ, 0.5))
    worker_task.escalate_plan()
    action_event = s3.execute_task(worker_task, {"relationship": CTX}, i)
    i += 1
    # effect 1: policy updated to encode the new allocation (future policy)
    bol.prov(i, "agent://s5", "policy updated: allocate by fit AND scoped delivery Trust",
             [{"uri": POLICY, "name": "provider allocation",
               "condition": "a new contracted job is to be allocated",
               "decision": "select by fit x scoped delivery Trust; laggard (< threshold) needs a performance gate before a new commitment",
               "action": "allocate to the top-ranked fitted provider; gate laggard (norcrete)",
               "scope": ["expectation://qk/e-on-time-delivery"], "version": 2,
               "policy_status": "REVISED"}])
    i += 1
    # effect 2: the next S2 match re-ranks (solarworks #1 under the updated policy+Trust)
    intent_roof = {"subject": PERSON, "need": "roofing & repair",
                   "capability_keys": ["roofing", "repair"], "urgency": "normal"}
    roof_offers = [o for o in _offs(sub) if o["uri"] in
                   ("offer://qk/o-solarworks", "offer://qk/o-norcrete")]
    matches = s2.match_offers(intent_roof, roof_offers,
                              [{"target": k, "score": v} for k, v in _trust_map(sub).items()],
                              trust_floor=0.5)
    bol.prov(i, "agent://s5",
             f"task effect: next roofing job ranked {matches[0].offer_uri} "
             f"(score {matches[0].score:.3f}) — re-allocation to the on-time provider",
             [{"uri": "decision://qk/s5-match-recorded", "by": "agent://s2",
               "authority": "delegation://qk/s2-match",
               "alternatives": [m.offer_uri for m in matches] + ["do nothing"],
               "confidence": 0.92, "expected_outcome": "solarworks ranked #1",
               "actual_outcome": matches[0].offer_uri,
               "detail": [m.to_dict() for m in matches], "made_at": now_iso()}])
    i += 1

    # --- BLOCKED: awaiting the rallied follow-on delivery's verified completion ---
    bol.prov(i, "agent://s5",
             "case blocked pending verified completion of the rallied follow-on delivery",
             [{"uri": "escalation://qk/s5-block-followup", "trigger":
               "follow-on job awaiting supplier completion + verification",
               "severity": "WARN", "recipient": APPROVER,
               "deadline": "2026-10-31T00:00:00Z", "fallback": "agent://s4",
               "authority": OPS_AUTH, "acknowledgement": "hold then verify"}])
    case = bol.transition_case(case, "BLOCKED", i, "agent://s5",
                               "case blocked: waiting on the rallied job's verified completion",
                               "event://qk/s5-case-blocked")
    i += 1

    # --- the rallied follow-on job: route to solarworks, settle on time, verify (#10) ---
    bol.prov(i, "agent://s5", "rallied follow-on job allocated to solarworks (the fix)",
             [{"uri": "commitment://qk/c-solarworks-followup", "by": "agent://s5",
               "to": "org://qk/solarworks", "obligation": "offer://qk/o-solarworks",
               "expectation": "expectation://qk/e-s5-routed-solarworks",
               "status": "AGREED", "terms": {"kind": "roofing follow-up", "signed": True},
               "agreed_at": now_iso()}])
    i += 1
    fx = {"slug": "routed-solarworks", "buyer": SUBJ, "provider": "org://qk/solarworks",
          "price": 2750, "currency": "USD", "value": 2750, "cost": 2750,
          "due": "2026-10-31T00:00:00Z", "settled_at": "2026-10-28T00:00:00Z",
          "of": "commitment://qk/c-solarworks-followup"}
    fexp = _expect_obj("routed-solarworks", SUBJ, "routed roofing follow-up", 2750,
                       "2026-10-31T00:00:00Z")
    bol.prov(i, "agent://s5", "register follow-on expectation", [fexp])
    i += 1
    chol = s4.settle(fx, i=i); i += 1
    fout = s4.evaluate(fx, fexp, i=i); i += 1
    ffor_s5 = {"uri": "event://qk/s5-verify-routed-solarworks", "job": "job-routed-solarworks",
               "provider": "org://qk/solarworks",
               "committed_deadline": fx["due"], "actual_completed_at": fx["settled_at"],
               "note": f"rallied delivery settled per {fout['uri']} ({fout['evaluation']})"}
    fev, fon = s5.capture(ffor_s5, s5_demo.PROVENANCE, signer="org://qk/solarworks", i=i); i += 1
    fvr = s5.verify(fev, "org://qk/solarworks delivered the rallied job on time", ffor_s5,
                    i=i); i += 1
    ftrust = s5.update_trust(subject=SUBJ, target="org://qk/solarworks", claim=CLAIM,
                             context=CTX, verify=fvr, evidence_score=fvr.degree, i=i,
                             alpha=cfg["alpha"], expectation=cfg["expectation"],
                             recency=cfg["recency"]); i += 1

    # RESOLVED: verified outcome
    on2, tot2 = project_on_time(sub)
    forward_rate = 1.0                                  # the rallied (post-change) period
    case = bol.transition_case(
        case, "RESOLVED", i, "agent://s5",
        f"exception resolved: rallied delivery verified on time; forward-period on-time = 1.0; "
        f"cumulative {on2}/{tot2}",
        "event://qk/s5-case-resolved",
        verified_outcome=f"forward-period on-time delivery restored to 1.0; "
                         f"org://qk/solarworks delivered the rallied job on time "
                         f"({fev['uri']}); solarworks Trust {ftrust['score']}")
    i += 1

    # --- Learning (§7K.1) + future-policy change, then CLOSE ---
    learning = bol.learning_entry(
        "decision://qk/s5-learning-on-time", "on-time delivery management", "agent://s5",
        i, "agent://s5",
        expected=expected, actual=forward_rate,
        why="Concentrating contracted work with a provider that has verified on-time "
            "delivery (solarworks), while gating the laggard (norcrete) with a performance "
            "checkpoint, restored on-time fulfilment. Verified good outcomes compound "
            "scoped delivery Trust and re-price routing.",
        change_future_policy="ALLOCATE by fit AND scoped delivery Trust (not fit alone); "
                             "providers below the Trust floor require a performance gate "
                             "before a new commitment.")
    i += 1
    bol.prov(i, "agent://s5", "close case; learning recorded; future policy updated",
             [{"uri": POLICY, "name": "provider allocation",
               "condition": "a new contracted job is to be allocated",
               "decision": "select by fit x scoped delivery Trust; laggard needs a performance gate BEFORE a new commitment (learned 2026-09-01)",
               "action": "allocate to the top-ranked fitted provider; gate laggard (norcrete); notify approver on divergence",
               "scope": ["expectation://qk/e-on-time-delivery"], "version": 3,
               "policy_status": "EFFECTIVE",
               "learning": "decision://qk/s5-learning-on-time"}])
    case = bol.transition_case(case, "CLOSED", i, "agent://s5",
                               "case closed with a verified, learned outcome",
                               "event://qk/s5-case-closed")
    i += 1

    summary = {
        "case": CASE_URI, "final_status": case["status"],
        "exception": {"expected": expected, "actual": round(actual, 3),
                      "variance": round(actual - expected, 3),
                      "significance": "CRITICAL", "on": on, "total": total},
        "task": TASK_R, "assigned_to": WORKER, "authority": OPS_AUTH,
        "priority": pri,
        "policy_final_version": 3,
        "follow_on": {"exchange": chol["uri"], "outcome": fout["uri"],
                      "evaluation": fout["evaluation"], "evidence": fev["uri"],
                      "after_trust": ftrust["score"],
                      "forward_on_time": forward_rate,
                      "cumulative_after": round(on2 / tot2, 3)},
        "learning": learning["uri"],
        "impact_placeholder": True,
    }
    sub._meta["s51"] = summary
    return summary


# ===========================================================================
# 5.2 — Goals / Metrics / Priority / Dependency + impact analysis
# ===========================================================================
def build_s52(sub: Substrate) -> dict:
    bol = BolService(sub)
    i = 8000
    cpu = project_trust(sub, "org://qk/solarworks", CTX) or 0.0
    settled = project_settled_value(sub)

    on, total = project_on_time(sub)
    on_rate = on / total if total else 1.0

    goal = {"uri": GOAL, "for": SUBJ,
            "statement": "Consistently deliver contracted work on time so customers "
                         "trust Quoteko enough to return.",
            "horizon": "quarter", "owner": APPROVER,
            "metrics": [ON_TIME_METRIC, "metric://qk/m-customer-trust",
                        "metric://qk/m-settled-value"]}
    m_on = {"uri": ON_TIME_METRIC, "name": "On-time delivery rate",
            "definition": "share of contracted completions verified on time",
            "unit": "fraction", "formula": "on_time / (on_time + late) from ledger",
            "dimensions": ["provider"], "target": 0.95, "threshold": 0.8,
            "period": "quarter", "source": "ledger completion records",
            "owner": APPROVER, "actual": round(on_rate, 3),
            "forecast": 0.83, "variance": round(on_rate - 0.95, 3),
            "root_cause": "provider scheduling failure (norcrete missed deadline)",
            "root_cause_status": "SUPPORTED"}
    m_trust = {"uri": "metric://qk/m-customer-trust", "name": "Customer-trust score",
               "definition": "best scoped delivery Trust on the customer relationship",
               "unit": "score", "formula": "T(subject->target, claim, context) per §5",
               "dimensions": ["provider"], "target": 0.9, "threshold": 0.6,
               "period": "rolling", "source": "S5 scoped Trust graph",
               "owner": APPROVER, "actual": round(cpu, 3), "forecast": 0.92,
               "variance": round(cpu - 0.9, 3),
               "root_cause_status": "UNKNOWN"}
    m_val = {"uri": "metric://qk/m-settled-value", "name": "Settled value",
             "definition": "value of EXCHANGE events settled this period",
             "unit": "USD", "formula": "sum(EXCHANGE.price) from ledger",
             "dimensions": ["provider"], "target": 25000.0, "threshold": 15000.0,
             "period": "quarter", "source": "ledger EXCHANGE events",
             "owner": APPROVER, "actual": settled, "forecast": 30000.0,
             "variance": round(settled - 25000.0, 2),
             "root_cause_status": "UNKNOWN"}
    bol.prov(i, "agent://s5",
             "register goal + ledger-projected metrics (health source)",
             [goal, m_on, m_trust, m_val])
    i += 1

    # --- Goal->Metric->Actual->Variance->Decision->Action->Outcome loop (§7J.1) ---
    bol.metric_loop(goal, m_on, "decision://qk/s5-metric-loop-on-time",
                    TASK_R,
                    "event://qk/s5-verify-routed-solarworks", i, "agent://s5")
    i += 1

    # --- Priority-ordered attention (derive, don't overload) ---
    att_tasks = [
        (TASK_R, 0.85, 0.90, 0.70, False, 0.80, 0.75, "re-balance provider allocation"),
        (TASK_F, 0.70, 0.75, 0.60, False, 0.70, 0.60, "rallied follow-on delivery (solarworks)"),
    ]
    attention = []
    for uri, imp, urg, conf, irr, rel, cod, label in att_tasks:
        p = bol.priority(imp, urg, conf, irr, rel, cod)
        attention.append({"uri": uri, "label": label, "priority": p["score"],
                          "factors": p["factors"]})
    attention.sort(key=lambda x: x["priority"], reverse=True)
    bol.prov(i, "agent://s5", "priority-ordered attention list (§7J.5)",
             [{"uri": "decision://qk/s5-attention-ordered", "by": "agent://s5",
               "authority": OPS_AUTH, "confidence": 0.9,
               "expected_outcome": "top-of-attention items ranked",
               "actual_outcome": "attention prioritized by derived score",
               "detail": {"attention": attention}, "made_at": now_iso()}])
    i += 1

    # --- Dependencies (§7J.6) + impact analysis ---
    bol.make_dependency("dependency://qk/d-rebalance-enables-followup",
                        TASK_R, TASK_F, "ENABLES", i, "agent://s5"); i += 1
    bol.make_dependency("dependency://qk/d-followup-requires-allocation",
                        TASK_F, POLICY, "REQUIRES", i, "agent://s5"); i += 1
    bol.make_dependency("dependency://qk/d-followup-blocks-case",
                        TASK_F, CASE_URI, "BLOCKS", i, "agent://s5"); i += 1
    bol.make_dependency("dependency://qk/d-case-derived-from-metric",
                        CASE_URI, ON_TIME_METRIC, "DERIVED_FROM", i, "agent://s5"); i += 1
    bol.make_dependency("dependency://qk/d-metric-impacts-goal",
                        ON_TIME_METRIC, GOAL, "IMPACTS", i, "agent://s5"); i += 1
    bol.make_dependency("dependency://qk/d-rebalance-blocks-case",
                        TASK_R, CASE_URI, "BLOCKS", i, "agent://s5"); i += 1

    impact_r = bol.impact_analysis(TASK_R)
    impact_f = bol.impact_analysis(TASK_F)

    # --- business-health panel (from ledger projections) ---
    health = []
    for m in (m_on, m_trust, m_val):
        var = m.get("variance", 0.0)
        tgt = m.get("target") or 1.0
        rel = var / abs(tgt)                     # compare on a common (relative) scale
        status = "OK" if rel >= 0 else ("WARN" if rel >= -0.05 else "CRITICAL")
        health.append({"metric": m["uri"], "name": m["name"], "unit": m["unit"],
                       "target": m.get("target"), "actual": m.get("actual"),
                       "variance": var, "status": status,
                       "forecast": m.get("forecast")})
    summary = {
        "goal": goal["uri"], "metrics": [m["uri"] for m in (m_on, m_trust, m_val)],
        "attention": attention, "health": health, "impact": impact_f,
        "impact_from_task_rebalance": impact_r,
        "dependencies": 6,
    }
    sub._meta["s52"] = summary
    return summary


# ===========================================================================
# 5.3 — The Cockpit (§7J.9) — assembled, rendered in run_s5_demo
# ===========================================================================
def build_s53(sub: Substrate) -> dict:
    s51 = sub._meta["s51"]; s52 = sub._meta["s52"]
    pdf = project_on_time(sub)
    cpu = project_trust(sub, "org://qk/solarworks", CTX)
    settled = project_settled_value(sub)
    cockpit = {
        "company": "Quoteko (fictional)", "generated": now_iso(),
        "health": s52["health"],
        "attention_line": f"{len(s52['attention'])} things requiring attention today",
        "attention": s52["attention"],
        "exception": s51["exception"],
        "case": s51["case"], "case_status": s51["final_status"],
        "recommendation": {
            "summary": s51["task"],
            "authority_required": OPS_AUTH,
            "options": ["re-balance to verified on-time provider",
                        "gate the laggard (norcrete)",
                        "do nothing"],
            "includes_do_nothing": True,
            "tradeoff": "Re-balancing concentrates work with solarworks (higher short-term "
                        "concentration risk) but restores on-time fulfilment and protects "
                        "scoped customer Trust; doing nothing keeps on-time below target.",
            "confidence": 0.85,
            "expected_impact": "forward-period on-time delivery returns to 1.0 "
                               "(verified, rallied solarworks delivery on time).",
            "decision": "decision://qk/s5-assign",
        },
        "verified_outcome": s51["follow_on"],
        "learning": s51["learning"],
        "ledger": len(sub.ledger.entries), "graph": len(sub.graph.objects),
    }
    sub._meta["s53"] = cockpit
    return cockpit


# ===========================================================================
# Fixture emission + cockpit report writer
# ===========================================================================
def _dump_group(by_uri, dirname, filename, prefixes):
    p = FIXTURES / dirname / f"{filename}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    items = [o for u, o in by_uri.items()
             if u.startswith(tuple(f"{pfx}://" for pfx in prefixes))]
    p.write_text(json.dumps(items, indent=2))
    return p


def emit_s5_fixtures(sub: Substrate) -> dict[str, Path]:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    by_uri = {}
    for e in sub.ledger.entries:
        for obj in e.get("state_update") or []:
            by_uri[obj["uri"]] = obj
    files = [
        _dump_group(by_uri, "s5", "cases", ["case"]),
        _dump_group(by_uri, "s5", "goals", ["goal"]),
        _dump_group(by_uri, "s5", "metrics", ["metric"]),
        _dump_group(by_uri, "s5", "tasks", ["task"]),
        _dump_group(by_uri, "s5", "dependencies", ["dependency"]),
        _dump_group(by_uri, "s5", "policies", ["policy"]),
        _dump_group(by_uri, "s5", "processes", ["process", "process_instance",
                                                "risk", "escalation"]),
        _dump_group(by_uri, "s5", "decisions", ["decision"]),
        _dump_group(by_uri, "s5", "expectations", ["expectation"]),
        _dump_group(by_uri, "s5", "evidence", ["evidence"]),
        _dump_group(by_uri, "s5", "trust", ["trust"]),
        _dump_group(by_uri, "s5", "claims", ["claim"]),
        _dump_group(by_uri, "s5", "actors_offers",
                    ["person", "org", "agent", "entity", "rule", "offer",
                     "authority", "delegation", "consent"]),
        _dump_group(by_uri, "s5", "relationships", ["relationship", "interaction"]),
        _dump_group(by_uri, "s5", "events", ["event"]),
    ]
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    lf = LEDGER_DIR / "ledger-quoteko.json"
    lf.write_text(json.dumps(sub.ledger.to_dict(), indent=2))
    files.append(lf)
    SM_DIR.mkdir(parents=True, exist_ok=True)
    rf = SM_DIR / "relationship.json"
    rf.write_text(json.dumps({"uri": CTX, "states": ["PROPOSED", "ACTIVE"]}))
    files.append(rf)
    cf = SM_DIR / "case.json"
    cf.write_text(json.dumps({"uri": CASE_URI,
                              "states": ["OPEN", "TRIAGE", "ASSIGNED", "IN_PROGRESS",
                                         "BLOCKED", "RESOLVED", "CLOSED"]}))
    files.append(cf)
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    gf = GRAPH_DIR / "current-state.json"
    gf.write_text(json.dumps(sub.graph.to_dict(), indent=2))
    files.append(gf)
    return {f.name: f for f in files}


def write_cockpit_report(cockpit: dict, sub: Substrate) -> tuple[Path, Path]:
    """Render the cockpit screen + the §7L ten answers with evidence to report files."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    A = lines.append
    A(f"# Quoteko — Business Operating Layer cockpit")
    A(f"generated {cockpit['generated']}  |  ledger events {len(sub.ledger.entries)}  graph objects {len(sub.graph.objects)}")
    A("")
    A("## Business health (ledger-projected metrics)")
    A(f"| metric | unit | target | actual | variance | status |")
    A(f"|---|---|---|---|---|---|")
    for h in cockpit["health"]:
        A(f"| {h['name']} (`{h['metric']}`) | {h['unit']} | {h['target']} | "
          f"{h['actual']} | {h['variance']} | {h['status']} |")
    A("")
    A(f"## Prioritized attention — {cockpit['attention_line']}")
    for a in cockpit["attention"]:
        A(f"- **{a['priority']:.2f}** {a['label']} (`{a['uri']}`)")
    A("")
    A("## Exception (heartbeat, §7J.2)")
    ex = cockpit["exception"]
    A(f"- expected {ex['expected']}  actual {ex['actual']}  variance {ex['variance']}  "
      f"significance {ex['significance']}  ({ex['on']}/{ex['total']} ledger completions on time)")
    A(f"- case `{cockpit['case']}`  status **{cockpit['case_status']}**")
    A("")
    A("## AI recommendation (#8) with the authority it requires (§7J.9)")
    rec = cockpit["recommendation"]
    A(f"- recommended work: `{rec['summary']}`")
    A(f"- authority required: `{rec['authority_required']}`  confidence {rec['confidence']}")
    A(f"- options: {rec['options']}  (do-nothing included: {rec['includes_do_nothing']})")
    A(f"- trade-off: {rec['tradeoff']}")
    A(f"- expected impact: {rec['expected_impact']}")
    A("")
    A("## Verified outcome (#10) + Learning")
    fo = cockpit["verified_outcome"]
    A(f"- rallied solarworks delivery settled {fo['exchange']}, outcome {fo['outcome']} "
      f"({fo['evaluation']}); evidence {fo['evidence']}; forward-period on-time {fo['forward_on_time']}; "
      f"solarworks Trust -> {fo['after_trust']}")
    A(f"- Learning entry: `{cockpit['learning']}`")
    A("")
    A("## §7L — the ten morning questions, answered with evidence")
    on, total = project_on_time(sub)
    rate = round(on / total, 3) if total else 1.0
    settled = project_settled_value(sub)
    att_labels = ", ".join(a["label"] for a in cockpit["attention"])
    vo = cockpit["verified_outcome"]
    A(f"1. WHAT HAPPENED?  On-time contracted completions {on}/{total} ({rate}); "
      f"solarworks settled on time (ev {vo['evidence']}), norcrete late; settled value "
      f"{settled}.  [ledger evidence]")
    A(f"2. WHAT CHANGED?  Provider re-allocation recommended; rallied solarworks delivery "
      f"verified on time; cumulative forward on-time {vo['cumulative_after']}; forward-period "
      f"on-time = {vo['forward_on_time']}.  [delta -> significance]")
    A(f"3. WHAT MATTERS?  Priority-ordered attention: {att_labels}.  [§7J.5]")
    A(f"4. WHAT'S GOING WRONG?  On-time delivery {rate} below target 0.95 (CRITICAL).  [§7J.2]")
    A("5. WHY?  Provider scheduling failure — norcrete missed its deadline (root SUPPORTED: "
      "scoped Trust 0.92->0.528).  [§7K.2 epistemic status]")
    A("6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.83 < 0.95; laggard keeps missing "
      "deadlines; scoped customer Trust erodes.  [§7K.1 forecast]")
    A("7. WHAT ARE OUR OPTIONS?  re-balance to solarworks; gate norcrete; do-nothing "
      "(all costed; trade-off in the recommendation).  [§7K.1 options incl. do-nothing]")
    A(f"8. WHAT SHOULD WE DO?  -> assigned, authorized Task "
      f"{cockpit['recommendation']['summary']} under "
      f"{cockpit['recommendation']['authority_required']}.  [recommendation]")
    A(f"9. WHO DOES IT, AND AUTHORITY/CAPACITY?  {WORKER} via delegation://qk/w-ops "
      f"(delegation-bounded authority, capacity 1.0), owner {APPROVER}."
      f"  [ownership + authority/capacity]")
    A(f"10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied delivery verified on time "
       f"(forward on-time {vo['forward_on_time']}); Learning entry "
       f"{cockpit['learning']}; provider-allocation policy v3 updated "
       f"(change-future-policy).  [verified outcome + organisational learning]")
    md = REPORTS / "cockpit.md"
    md.write_text("\n".join(lines))
    j = REPORTS / "cockpit.json"
    j.write_text(json.dumps({"cockpit": cockpit,
                             "seven": cockpit["attention"],
                             "health": cockpit["health"]}, indent=2))
    return md, j


def build_s5() -> Substrate:
    """Run the whole Sprint-5 chain on the Sprint-4 S1->S5 end-state."""
    sub, _b, _a = s5_demo.build_s2()
    s3_demo.build_s3(sub)
    s4_demo.build_s41(sub); s4_demo.build_s42(sub); s4_demo.build_s43(sub)
    build_s51(sub)
    build_s52(sub)
    cockpit = build_s53(sub)
    write_cockpit_report(cockpit, sub)
    return sub


if __name__ == "__main__":
    import run_s5_demo  # noqa: F401