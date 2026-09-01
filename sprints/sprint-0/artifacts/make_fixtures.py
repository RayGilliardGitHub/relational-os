#!/usr/bin/env python3
"""Generate all RelationalOS Sprint-0 fixtures (reproducible).

Sources of truth: SPEC Appendix E (the 20 interactions), §7L (ten-question loop,
one fictional company), §7J.3 Case lifecycle, §2/§3.16 (ledger), §3.16 relationships.
Writes JSON under fixtures/. Each top-level object is a valid instance per the 0.17
schema (URI-mined nouns only; derived items — exception/priority/recommendation/
SLA/capacity — are EMBEDDED assemblies, not URI nouns, per §7J.11/§7K).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"

TS = "2026-09-01T09:00:00Z"
TS2 = "2026-09-01T10:30:00Z"


def actor(uri, typ, **kw):
    d = {"uri": uri, "type": typ}
    d.update(kw)
    return d


def relationship(uri, participants, status="ACTIVE", **kw):
    d = {"uri": uri, "participants": participants, "status": status}
    d.update(kw)
    return d


def interaction(uri, of, kind, **kw):
    d = {"uri": uri, "of": of, "kind": kind}
    d.update(kw)
    return d


def event(uri, typ, actor=None, **kw):
    d = {
        "uri": uri, "type": typ,
        "event_id": uri.replace("://", "-"),
        "correlation_id": uri.replace("://", "-c"),
        "causation_id": uri.replace("://", "-ca"),
        "idempotency_key": uri.replace("://", "-i"),
        "signature": "signed-by-s1",
        "occurred_at": TS,
    }
    if actor:
        d["actor"] = actor
    d.update(kw)
    return d


def claim(uri, proposer, statement, **kw):
    d = {"uri": uri, "proposer": proposer, "statement": statement}
    d.update(kw)
    return d


def evidence(uri, kind, source, **kw):
    d = {"uri": uri, "kind": kind, "source": source}
    d.update(kw)
    return d


def decision(uri, by, authority, **kw):
    d = {"uri": uri, "by": by, "authority": authority}
    d.update(kw)
    return d


def obligation(uri, subject, source, **kw):
    d = {"uri": uri, "subject": subject, "source": source}
    d.update(kw)
    return d


def right(uri, holder, typ, **kw):
    return {"uri": uri, "holder": holder, "type": typ, **kw}


def consent(uri, granted_by, granted_for, **kw):
    return {"uri": uri, "granted_by": granted_by, "granted_for": granted_for, **kw}


def commitment(uri, by, to, **kw):
    return {"uri": uri, "by": by, "to": to, **kw}


def delegation(uri, grantor, grantee, scope, **kw):
    return {"uri": uri, "grantor": grantor, "grantee": grantee, "scope": [scope], **kw}


def dispute(uri, about, parties, status, **kw):
    return {"uri": uri, "about": about, "parties": parties, "status": status, **kw}


def expectation(uri, actor, subject, condition, **kw):
    return {"uri": uri, "actor": actor, "subject": subject, "condition": condition, **kw}


# ---------------------------------------------------------------------------
# Appendix E — the 20 interactions (18 native, 2 derived)
# ---------------------------------------------------------------------------
E = {}

E["01-hamburger"] = [
    actor("person://e01/customer", "PERSON"),
    actor("org://e01/diner", "ORG"),
    relationship("relationship://e01/r1", ["person://e01/customer", "org://e01/diner"],
                 roles={"person://e01/customer": ["customer"], "org://e01/diner": ["merchant"]}),
    interaction("interaction://e01/offer", "relationship://e01/r1", "OFFER"),
    interaction("interaction://e01/exchange", "relationship://e01/r1", "EXCHANGE"),
    event("event://e01/action", "ACTION", "person://e01/customer"),
    event("event://e01/exchange", "EXCHANGE", "person://e01/customer"),
]

E["02-car"] = [   # DERIVED: composes multiple relationships (buyer↔dealer, borrower↔lender, owner↔registrar)
    actor("person://e02/buyer", "PERSON"),
    actor("org://e02/dealer", "ORG"),
    actor("org://e02/bank", "ORG"),
    actor("org://e02/dmv", "ORG"),
    relationship("relationship://e02/sale", ["person://e02/buyer", "org://e02/dealer"]),
    relationship("relationship://e02/loan", ["person://e02/buyer", "org://e02/bank"]),
    relationship("relationship://e02/reg", ["person://e02/buyer", "org://e02/dmv"]),
    interaction("interaction://e02/negotiation", "relationship://e02/sale", "NEGOTIATION"),
    interaction("interaction://e02/exchange", "relationship://e02/sale", "EXCHANGE"),
    event("event://e02/decision", "DECISION", "person://e02/buyer"),
]

E["03-work-walmart"] = [
    actor("person://e03/emp", "PERSON"),
    actor("org://e03/walmart", "ORG"),
    relationship("relationship://e03/employ", ["person://e03/emp", "org://e03/walmart"],
                 roles={"person://e03/emp": ["employee"]}, status="ACTIVE",
                 effective_from="2024-03-01T00:00:00Z"),
    commitment("commitment://e03/c1", "person://e03/emp", "perform duties per role"),
    obligation("obligation://e03/o1", "org://e03/walmart", "IMPOSED", content="pay wages"),
    interaction("interaction://e03/payroll", "relationship://e03/employ", "EXCHANGE"),
    event("event://e03/exchange", "EXCHANGE", "org://e03/walmart"),
]

E["04-taxes"] = [
    actor("person://e04/filer", "PERSON"),
    actor("org://e04/irs", "ORG"),
    relationship("relationship://e04/tax", ["person://e04/filer", "org://e04/irs"]),
    obligation("obligation://e04/taxob", "person://e04/filer", "IMPOSED", content="file federal return"),
    interaction("interaction://e04/file", "relationship://e04/tax", "OUTCOME"),
    {"uri": "return://e04/1040-2025", "kind": "tax-return", "subject_to": "person://e04/filer"},
    event("event://e04/outcome", "OUTCOME", "person://e04/filer"),
]

E["05-drivers-license"] = [
    actor("person://e05/d", "PERSON"),
    actor("org://e05/state", "ORG"),
    relationship("relationship://e05/lic", ["person://e05/d", "org://e05/state"]),
    {"uri": "license://e05/dl-123456", "type": "drivers", "holder": "person://e05/d"},
    interaction("interaction://e05/grant", "relationship://e05/lic", "DECISION"),
    event("event://e05/decision", "DECISION", "org://e05/state"),
]

E["06-unemployment"] = [
    actor("person://e06/u", "PERSON"),
    actor("org://e06/ui", "ORG"),
    relationship("relationship://e06/benefit", ["person://e06/u", "org://e06/ui"]),
    right("right://e06/claimbenefit", "person://e06/u", "RECEIVE_PAYMENT"),
    obligation("obligation://e06/seekwork", "person://e06/u", "IMPOSED", content="actively seek work"),
    interaction("interaction://e06/order", "relationship://e06/benefit", "EXCHANGE"),
    event("event://e06/exchange", "EXCHANGE", "org://e06/ui"),
]

E["07-donate-foodbank"] = [
    actor("person://e07/donor", "PERSON"),
    actor("org://e07/foodbank", "ORG"),
    relationship("relationship://e07/donation", ["person://e07/donor", "org://e07/foodbank"],
                 roles={"org://e07/foodbank": ["charity"]}),
    {"uri": "resource://e07/food", "kind": "MATERIAL", "donated_by": "person://e07/donor"},
    interaction("interaction://e07/exchange", "relationship://e07/donation", "EXCHANGE"),
    event("event://e07/exchange", "EXCHANGE", "person://e07/donor"),
]

E["08-volunteer"] = [
    actor("person://e08/v", "PERSON"),
    actor("org://e08/charity", "ORG"),
    relationship("relationship://e08/vol", ["person://e08/v", "org://e08/charity"],
                 roles={"person://e08/v": ["volunteer"]}),
    {"uri": "resource://e08/labor", "kind": "LABOR", "provided_by": "person://e08/v"},
    {"uri": "resource://e08/time", "kind": "TIME", "provided_by": "person://e08/v"},
    interaction("interaction://e08/action", "relationship://e08/vol", "ACTION"),
    event("event://e08/action", "ACTION", "person://e08/v"),
]

E["09-hospital"] = [
    actor("person://e09/pat", "PERSON"),
    actor("org://e09/hospital", "ORG"),
    relationship("relationship://e09/care", ["person://e09/pat", "org://e09/hospital"],
                 roles={"person://e09/pat": ["patient"]}),
    consent("consent://e09/c1", "person://e09/pat", "treatment + PHI processing"),
    claim("claim://e09/dx", "org://e09/hospital", "diagnosis of per the record"),
    evidence("evidence://e09/record", "RECORD", "org://e09/hospital/emr#visit"),
    interaction("interaction://e09/care", "relationship://e09/care", "ACTION"),
]

E["10-college"] = [
    actor("person://e10/std", "PERSON"),
    actor("org://e10/uni", "ORG"),
    relationship("relationship://e10/enroll", ["person://e10/std", "org://e10/uni"],
                 roles={"person://e10/std": ["student"]}),
    {"uri": "student_record://e10/rec", "type": "enrollment", "person": "person://e10/std"},
    interaction("interaction://e10/exchange", "relationship://e10/enroll", "EXCHANGE"),
    event("event://e10/exchange", "EXCHANGE", "person://e10/std"),
]

E["11-buy-insurance"] = [
    actor("person://e11/insd", "PERSON"),
    actor("org://e11/insurer", "ORG"),
    relationship("relationship://e11/policy", ["person://e11/insd", "org://e11/insurer"]),
    {"uri": "policy://ins/e11-h22", "type": "auto", "holder": "person://e11/insd"},
    right("right://e11/coverage", "person://e11/insd", "RECEIVE_PAYMENT"),
    interaction("interaction://e11/exchange", "relationship://e11/policy", "EXCHANGE"),
    event("event://e11/exchange", "EXCHANGE", "person://e11/insd"),
]

E["12-insurance-claim"] = [
    actor("person://e12/insd", "PERSON"),
    actor("org://e12/insurer", "ORG"),
    relationship("relationship://e12/claimrel", ["person://e12/insd", "org://e12/insurer"]),
    claim("claim://e12/c1", "person://e12/insd", "collision damage covered by policy"),
    evidence("evidence://e12/photo", "OBSERVATION", "adjuster report"),
    dispute("dispute://e12/d1", "claim://e12/c1", ["person://e12/insd", "org://e12/insurer"], "OPEN"),
    interaction("interaction://e12/claim", "relationship://e12/claimrel", "DISPUTE"),
]

E["13-hire-contractor"] = [
    actor("person://e13/homeowner", "PERSON"),
    actor("person://e13/contractor", "PERSON"),
    relationship("relationship://e13/hire", ["person://e13/homeowner", "person://e13/contractor"]),
    {"uri": "contract://e13/c1", "parties": ["person://e13/homeowner", "person://e13/contractor"]},
    interaction("interaction://e13/offer", "relationship://e13/hire", "OFFER"),
    event("event://e13/decision", "DECISION", "person://e13/homeowner"),
]

E["14-supply-boeing"] = [
    actor("org://e14/boeing", "ORG"),
    actor("org://e14/supplier", "ORG"),
    relationship("relationship://e14/supply", ["org://e14/supplier", "org://e14/boeing"],
                 roles={"org://e14/supplier": ["supplier"], "org://e14/boeing": ["customer"]}),
    expectation("expectation://e14/ontime", "org://e14/boeing", "deliver on schedule", "delivery within 7 days"),
    commitment("commitment://e14/c1", "org://e14/supplier", "deliver parts per contract"),
    interaction("interaction://e14/fulfil", "relationship://e14/supply", "ACTION"),
]

E["15-arrest"] = [
    actor("person://e15/accused", "PERSON"),
    actor("org://e15/state", "ORG"),
    relationship("relationship://e15/custody", ["person://e15/accused", "org://e15/state"]),
    obligation("obligation://e15/o1", "person://e15/accused", "IMPOSED", content="submit to lawful arrest"),
    right("right://e15/legalrep", "person://e15/accused", "REPRESENTATION"),
    interaction("interaction://e15/custody", "relationship://e15/custody", "ACTION"),
    event("event://e15/action", "ACTION", "org://e15/state"),
]

E["16-appeal-gov"] = [
    actor("person://e16/appellant", "PERSON"),
    actor("org://e16/agency", "ORG"),
    relationship("relationship://e16/appeal", ["person://e16/appellant", "org://e16/agency"]),
    dispute("dispute://e16/d1", "decision://e16/denied", ["person://e16/appellant", "org://e16/agency"], "OPEN"),
    evidence("evidence://e16/e1", "RECORD", "agency decision letter"),
    decision("decision://e16/denied", "org://e16/agency", "authority://e16/adjudication",
             confidence=0.9),
    interaction("interaction://e16/appeal", "relationship://e16/appeal", "DISPUTE"),
]

E["17-voting"] = [   # DERIVED: secret ballot = strict non-disclosure on the Action (§3.19)
    actor("person://e17/voter", "PERSON"),
    actor("org://e17/state", "ORG"),
    relationship("relationship://e17/vote", ["person://e17/voter", "org://e17/state"],
                 roles={"person://e17/voter": ["citizen"]}),
    {  # non-disclosure constraint carried on the Action — no evidence, private
        "uri": "event://e17/private", "type": "ACTION", "actor": "person://e17/voter",
        "event_id": "event-e17-private", "correlation_id": "event-e17-private-c",
        "causation_id": "event-e17-private-ca", "idempotency_key": "event-e17-private-i",
        "signature": "zero-knowledge-proof", "occurred_at": TS,
        "disclosure": "NON_DISCLOSURE",
    },
]

E["18-bank-account"] = [
    actor("person://e18/accountholder", "PERSON"),
    actor("org://e18/bank", "ORG"),
    relationship("relationship://e18/acct", ["person://e18/accountholder", "org://e18/bank"]),
    consent("consent://e18/c1", "person://e18/accountholder", "KYC + account terms"),
    {"uri": "acct://e18/checking", "kind": "customer-account", "holder": "person://e18/accountholder"},
    interaction("interaction://e18/open", "relationship://e18/acct", "OFFER"),
    event("event://e18/decision", "DECISION", "org://e18/bank"),
]

E["19-ai-invoice-approve"] = [
    actor("agent://e19/agent", "AGENT"),
    actor("org://e19/company", "ORG"),
    relationship("relationship://e19/r1", ["agent://e19/agent", "org://e19/company"]),
    delegation("delegation://e19/d1", "org://e19/company", "agent://e19/agent", "rule://e19/approve-invoices-under-5k"),
    decision("decision://e19/d1", "agent://e19/agent", "delegation://e19/d1",
             alternatives=["approve", "escalate"], confidence=0.95),
    event("event://e19/decision", "DECISION", "agent://e19/agent"),
    interaction("interaction://e19/approve", "relationship://e19/r1", "DECISION"),
]

E["20-ai-negotiate"] = [
    actor("agent://e20/a1", "AGENT"),
    actor("org://e20/company", "ORG"),
    relationship("relationship://e20/r1", ["agent://e20/a1", "org://e20/company"]),
    delegation("delegation://e20/d1", "org://e20/company", "agent://e20/a1", "rule://e20/negotiation-terms"),
    interaction("interaction://e20/neg", "relationship://e20/r1", "NEGOTIATION"),
    commitment("commitment://e20/c1", "agent://e20/a1", "agreed contract terms"),
    event("event://e20/outcome", "OUTCOME", "agent://e20/a1"),
]


# ---------------------------------------------------------------------------
# §7L — Meridian Machine Works (fictional), the ten morning questions w/ evidence
# ---------------------------------------------------------------------------
MERIDIAN = [
    actor("org://meridian", "ORG", identity={"attestations": ["registered"]}),
    actor("person://meridian/cfo", "PERSON"),
    actor("person://meridian/buyer", "PERSON"),
    actor("org://meridian/supplier", "ORG"),
    relationship("relationship://meridian/prod", ["org://meridian", "org://meridian/supplier"],
                 roles={"org://meridian/supplier": ["supplier"]}, status="ACTIVE"),
    # Q1 What happened: a supplier shipment event
    event("event://meridian/e-ship", "EXCHANGE", "org://meridian/supplier",
          of_interaction="interaction://meridian/i-supply"),
    # Q2 What changed: OTD metric moved
    {"uri": "metric://meridian/otd", "name": "OnTimeDelivery", "formula": "on_time/total",
     "target": 0.95, "threshold": 0.90, "actual": 0.82, "period": "2026-W35",
     "owner": "person://meridian/cfo", "unit": "ratio", "source": "supplier_shipments",
     "definition": "share of purchase orders received on time", "variance": -0.08,
     "forecast": 0.80},
    # Q4 What's going wrong: exception (embedded, derived — NOT a URI noun)
    {"uri": "case://meridian/otd-shortfall", "subject": "OnTimeDelivery below threshold",
     "status": "OPEN", "owner": "person://meridian/buyer",
     "relationships": ["relationship://meridian/prod"], "created_at": "2026-09-01T06:00:00Z",
     "exception": {"significance": "CRITICAL", "exception": "OTD 0.82 vs threshold 0.90",
                   "expected": 0.95, "actual": 0.82, "variance": -0.13}},
    # Q5 Why: root cause with epistemic status (SUPPORTED)
    {"uri": "metric://meridian/otd", "name": "OnTimeDelivery", "formula": "on_time/total",
     "target": 0.95, "threshold": 0.90, "actual": 0.82, "period": "2026-W35",
     "owner": "person://meridian/cfo", "unit": "ratio", "source": "supplier_shipments",
     "definition": "share of PO received on time", "variance": -0.08, "forecast": 0.80,
     "root_cause": "supplier capacity constraint (strike + no second source)",
     "root_cause_status": "SUPPORTED",
     "evidence": ["evidence://meridian/e-strike"]},
    evidence("evidence://meridian/e-strike", "RECORD", "regulatory notice + supplier comms",
             confidence=0.8, procedure="cross-source verify"),
    # Q6 What if we do nothing: forecast states worse
    {"uri": "metric://meridian/otd", "name": "OnTimeDelivery", "formula": "on_time/total",
     "target": 0.95, "threshold": 0.90, "actual": 0.82, "period": "2026-W35",
     "owner": "person://meridian/cfo", "unit": "ratio", "source": "supplier_shipments",
     "definition": "OTD", "variance": -0.08, "forecast": 0.70,
     "if_nothing_changes": "OTD trending to 0.70 by W37; production disruption"},
    # Q7 Options incl. do-nothing + trade-off (embedded recommendation — derived)
    {"uri": "decision://meridian/options", "by": "org://meridian", "authority": "authority://meridian/cfo",
     "confidence": 0.8,
     "recommendation": {
         "options": ["expedite existing order", "dual-source with second supplier", "do nothing"],
         "includes_do_nothing": True,
         "tradeoff": "expedite is fastest but costly; dual-source adds lead time but derisks",
     }},
    # Q8 What should we do: recommendation with authority required → assignment
    {"uri": "decision://meridian/decision", "by": "org://meridian", "authority": "authority://meridian/cfo",
     "confidence": 0.82,
     "recommendation": {"options": ["dual-source"], "includes_do_nothing": False,
                        "authority_required": "authority://meridian/cfo",
                        "expected_impact": "OTD back to 0.95 within 3 weeks"},
     "expected_outcome": "restore OTD",
     "actual_outcome": "pending"},
    # Q9 Who does it + authority/capacity
    {"uri": "task://meridian/t1", "assigned_to": "person://meridian/buyer",
     "created_by": "org://meridian", "objective": "onboard second supplier for part P-773",
     "authority": "delegation://meridian/dual-source", "status": "ASSIGNED",
     "priority": 0.9, "deadline": "2026-09-08T17:00:00Z", "expected_outcome": "contract signed"},
    delegation("delegation://meridian/dual-source", "org://meridian", "person://meridian/buyer",
               "rule://meridian/sign-supplier-agreements"),
    # Q2 alternate: capacity
    {"uri": "resource://meridian/buyer-cap", "kind": "CAPABILITY", "value": "value://meridian/alloc"},
    # Q10 Did it work, and what did we learn: verified outcome + learning
    {"uri": "event://meridian/e-verified", "type": "OUTCOME", "actor": "org://meridian",
     "event_id": "event-meridian-e-verified", "correlation_id": "event-meridian-e-verified-c",
     "causation_id": "event-meridian-e-verified-ca", "idempotency_key": "event-meridian-e-verified-i",
     "signature": "signed-by-s5", "occurred_at": "2026-09-29T09:00:00Z",
     "verified": True},
    {"uri": "task://meridian/t1", "assigned_to": "person://meridian/buyer",
     "created_by": "org://meridian", "objective": "onboard second supplier P-773",
     "authority": "delegation://meridian/dual-source", "status": "COMPLETED",
     "priority": 0.9, "expected_outcome": "contract signed", "actual_outcome": "2nd supplier live; OTD 0.96"},
    decision("decision://meridian/learned", "org://meridian", "authority://meridian/cfo",
             confidence=0.85,
             learning="dual-sourcing became standard policy after supplier strike",
             expected_outcome="derisk", actual_outcome="derisk completed, OTD restored"),
]

# ---------------------------------------------------------------------------
# Case lifecycle — OPEN→TRIAGE→ASSIGNED→IN_PROGRESS→BLOCKED→IN_PROGRESS→
# RESOLVED→CLOSED→REOPEN→RESOLVED→CLOSED  (final resolved object + machine doc)
# ---------------------------------------------------------------------------
CASE_LIFECYCLE = [
    {"uri": "case://cl/prize", "subject": "customer warranty claim",
     "status": "CLOSED", "owner": "person://cl/agent",
     "created_at": "2026-08-01T09:00:00Z", "closed_at": "2026-08-20T17:00:00Z",
     "resolution": "replacement shipped; dispute resolved",
     "reopened": True},
    actor("person://cl/agent", "PERSON"),
]
CASE_STATES = ["OPEN", "TRIAGE", "ASSIGNED", "IN_PROGRESS", "BLOCKED", "IN_PROGRESS",
               "RESOLVED", "CLOSED", "OPEN", "TRIAGE", "ASSIGNED", "IN_PROGRESS",
               "RESOLVED", "CLOSED"]   # REOPEN through the full workflow
REL_STATES = ["PROPOSED", "ACTIVE", "SUSPENDED", "ACTIVE", "TERMINATED", "ARCHIVED"]

# ---------------------------------------------------------------------------
# Ledger — content-addressed & signed
# ---------------------------------------------------------------------------
def _mk_ledger():
    entries = [
        {"event_id": "lg-1", "actor": "person://meridian/cfo",
         "event_type": "DECISION", "action": "approve dual-source", "signature": "sig:a"},
        {"event_id": "lg-2", "actor": "person://meridian/buyer",
         "event_type": "ACTION", "action": "sign supplier agreement", "signature": "sig:b"},
        {"event_id": "lg-3", "actor": "org://meridian/supplier",
         "event_type": "EXCHANGE", "action": "shipment dispatched", "signature": "sig:c"},
    ]
    prev = ""
    for e in entries:
        content = json.dumps({k: v for k, v in e.items() if k != "hash"},
                             sort_keys=True, separators=(",", ":"))
        e["hash"] = hashlib.sha256((prev + content).encode()).hexdigest()
        prev = e["hash"]
    return {"uri": "db://ledger/meridian-2026", "head_hash": prev, "entries": entries}


def main():
    for slug, objs in E.items():
        (FIX / "appendix-e").mkdir(parents=True, exist_ok=True)
        (FIX / "appendix-e" / f"{slug}.json").write_text(json.dumps(objs, indent=2))

    (FIX / "7l-loop").mkdir(parents=True, exist_ok=True)
    (FIX / "7l-loop" / "company.json").write_text(json.dumps(MERIDIAN, indent=2))

    (FIX / "case-lifecycle").mkdir(parents=True, exist_ok=True)
    (FIX / "case-lifecycle" / "sequence.json").write_text(json.dumps(CASE_LIFECYCLE, indent=2))

    (FIX / "statemachines").mkdir(parents=True, exist_ok=True)
    (FIX / "statemachines" / "relationship.json").write_text(json.dumps({"states": REL_STATES}, indent=2))
    (FIX / "statemachines" / "case.json").write_text(json.dumps({"states": CASE_STATES}, indent=2))

    (FIX / "ledger").mkdir(parents=True, exist_ok=True)
    (FIX / "ledger" / "ledger-1.json").write_text(json.dumps(_mk_ledger(), indent=2))

    n = sum(len(v) for v in E.values()) + len(MERIDIAN) + len(CASE_LIFECYCLE)
    print(f"WROTE fixtures: {len(E)} appendix-e interactions, 7l-loop, case-lifecycle "
          f"({n} instance objects) + statemachines + ledger")


if __name__ == "__main__":
    main()