"""Build the Sprint-4 Settlement (S4) + multi-role / multi-org demo on the Sprint-3 state.

Extends the Sprint-3 loop end-state (solarworks job committed + executed + Trust 0.806):

  4.1  S4 settle + evaluate on ONE relationship (relationship://qk/cust-cxn): settle the
       committed solarworks job -> signed EXCHANGE event:// + asset:// (title/custody, §4b)
       + obligation:// (payment) + receipt:// + reconciliation decision://; evaluate() against
       the §3.11 Expectation -> signed OUTCOME event:// (met); the settled outcome feeds S5
       capture/verify -> update_trust (solarworks up) -> S2 re-ranks. Loop closes WITH
       settlement in the middle.

  4.2  TWO roles on ONE relationship: the same actor is customer AND employee of Quoteko on
       relationship://qk/cust-cxn (§3.2/§C2 — role is an attribute). Role-scoped identity,
       role-scoped authority (authorize_for_role), role-scoped Trust keyed with
       context "relationship://qk/cust-cxn?role=employee" (§3.14). Full S1->S5 loop for the
       employee role (payroll), with a distinct scoped Trust value from the customer role.

  4.3  TWO org types on ONE relationship: private for-profit org://quoteko (donor) engages a
       charitable nonprofit org://qk/sunsetshelter (beneficiary) across the §3.1 org-kind
       attribute (Purpose FOR_PROFIT vs NONPROFIT_CHARITABLE). Purpose-constrained offer,
       jurisdiction-appropriate consent/authority. Full S1->S5 loop; the IRREVERSIBLE
       charitable-grant settlement escalates to person://qk/approver before execution (§6
       floor) — proven from Ledger ORDER alone.

Every new object is carried by a signed Ledger event's `state_update` so the Graph round-trip
reconstructs it (§3.16). No new URI schemes, no new nouns (URI cap, §7J.11/§C16).
"""
from __future__ import annotations

import json
from pathlib import Path

from ros.substrate import Substrate, now_iso
from ros.s1 import S1Service, Permission, Denial
from ros.s2 import S2Service
from ros.s3 import S3Service, Task
from ros.s4 import S4Service
from ros.s5 import S5Service, config_defaults
import s3_demo
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
EMP_CTX = "relationship://qk/cust-cxn?role=employee"      # role-qualified context (§3.2)
CHARITY_CTX = "relationship://qk/charity-cxn"
PERSON = "person://qk/customer"


# ---------------------------------------------------------------------------
# shared provisioning helper: record a bundle of seed objects as one signed event
# ---------------------------------------------------------------------------
def _provision(sub, s4: S4Service, uri: str, i: int, detail: str, objs: list,
               signer: str = "agent://s4") -> None:
    sub.record(s4._ev("STATE_CHANGE", uri, signer, i, detail, objs), signer)


def _trust_map(sub) -> dict:
    return {o["target"]: float(o.get("score", 0.0))
            for o in sub.graph.objects.values()
            if o.get("uri", "").startswith("trust://")}


def _offs(sub) -> list[dict]:
    return [o for o in sub.graph.objects.values() if o.get("uri", "").startswith("offer://")]


def _expectation_obj(slug: str, buyer: str, subject: str, price: float,
                     due: str) -> dict:
    return {
        "uri": f"expectation://qk/e-settle-{slug}",
        "actor": buyer, "subject": subject,
        "condition": "full and on-time settlement of the agreed value",
        "metric": "settled_value", "threshold": price, "deadline": due,
        "evidence_required": "CLEAR",
    }


# ===========================================================================
# 4.1 — S4 settle + evaluate on the Sprint-3 loop end-state
# ===========================================================================
def build_s41(sub: Substrate) -> dict:
    s1 = S1Service(sub); s2 = S2Service(sub); s4 = S4Service(sub); s5 = S5Service(sub)
    cfg = config_defaults()

    # settlement authority + shared expectation for the exchange to settle
    authz = [{"uri": "authority://qk/for-settlement", "holder": SUBJ,
              "grants": ["settle", "release_settlement"], "roles": ["settlement_service"]}]
    expectation = _expectation_obj("solarworks", SUBJ, "solarworks roofing job",
                                   18900, "2026-10-01T00:00:00Z")
    _provision(sub, s4, "event://qk/s4-provision", 4000,
               "provision S4 settlement authority + expectation", authz + [expectation])

    # the committed/executed/trusted solarworks job settles
    exchange = {
        "slug": "solarworks", "buyer": SUBJ, "provider": "org://qk/solarworks",
        "price": 18900, "currency": "USD",
        "value": 18900, "cost": 18900,          # §3.9 Value/Cost/Price captured
        "due": "2026-10-01T00:00:00Z",          # commitment deadline
        "settled_at": "2026-09-30T00:00:00Z",   # on time
        "of": "commitment://qk/c-solarworks",
    }
    exch_event = s4.settle(exchange, i=4010)
    outcome = s4.evaluate(exchange, expectation, i=4020)          # met

    # the settled OUTCOME feeds S5 capture/verify -> Trust -> S2 re-rank (loop closed
    # WITH settlement in the middle)
    outcome_for_s5 = {
        "uri": "event://qk/s4-verify-solarworks", "job": "job-solarworks-s4",
        "provider": "org://qk/solarworks",
        "committed_deadline": exchange["due"],
        "actual_completed_at": exchange["settled_at"],
        "note": f"settled per {outcome['uri']} ({outcome['evaluation']})",
    }
    evidence, on_time = s5.capture(outcome_for_s5, s5_demo.PROVENANCE,
                                   signer="org://qk/solarworks", i=4030)
    vr = s5.verify(evidence,
                   f"org://qk/solarworks settled the exchange met per {outcome['uri']}",
                   outcome_for_s5, i=4031)
    trust = s5.update_trust(subject=SUBJ, target="org://qk/solarworks", claim=CLAIM,
                            context=CTX, verify=vr, evidence_score=vr.degree, i=4032,
                            alpha=cfg["alpha"], expectation=cfg["expectation"],
                            recency=cfg["recency"])
    next_rank = s2.match_offers(
        {"subject": PERSON, "need": "roofing", "capability_keys": ["roofing", "repair"]},
        _offs(sub),
        [{"target": k, "score": v} for k, v in _trust_map(sub).items()],
        trust_floor=0.5)

    summary = {
        "exchange": exch_event["uri"], "asset": "asset://money/qk-escrow-solarworks",
        "obligation": "obligation://qk/s4-pay-solarworks",
        "receipt": "receipt://qk/s4-receipt-solarworks",
        "reconciliation": "decision://qk/s4-recon-solarworks",
        "outcome": outcome["uri"], "evaluation": outcome["evaluation"],
        "evidence": evidence["uri"], "trust_before": 0.806, "trust_after": trust["score"],
        "next_rank": [m.to_dict() for m in next_rank],
    }
    sub._meta["s41"] = summary
    return summary


# ===========================================================================
# 4.2 — TWO roles on ONE relationship (customer + employee)
# ===========================================================================
def build_s42(sub: Substrate) -> dict:
    s1 = S1Service(sub); s2 = S2Service(sub); s3 = S3Service(sub)
    s4 = S4Service(sub); s5 = S5Service(sub)
    cfg = config_defaults()

    # --- role is an attribute: the SAME relationship now carries BOTH roles ---
    rel = dict(sub.graph.get(CTX))
    rel["roles"] = {PERSON: ["customer", "employee"],
                    SUBJ: ["service_provider", "employer"]}
    rel["authority_by_role"] = {"customer": "authority://qk/for-matching",
                                "employee": "authority://qk/for-employment"}
    rel["consent"] = ["consent://qk/match-data", "consent://qk/employee-consent"]

    emp_objs = [
        rel,
        {"uri": "authority://qk/for-employment", "holder": SUBJ,
         "grants": ["submit_timesheet", "enroll_benefits", "receive_payroll"],
         "roles": ["employee"]},
        {"uri": "rule://qk/emp-actions", "kind": "POLICY",
         "text": "employee-role actions within Quoteko",
         "grants": ["submit_timesheet", "enroll_benefits", "receive_payroll"]},
        {"uri": "consent://qk/employee-consent", "granted_by": PERSON,
         "granted_for": "employment & payroll rights with Quoteko as employer",
         "scope": ["rule://qk/emp-actions"],
         "duration": {"effective": "2026-09-01T00:00:00Z",
                      "expires": "2027-09-01T00:00:00Z"},
         "revocable": True, "status": "GRANTED"},
        # employee-role Trust is a DISTINCT scoped value (subject=person, target=org)
        {"uri": "trust://qk/t-emp-quoteko", "subject": PERSON, "target": SUBJ,
         "claim": "payroll & benefits reliability",
         "context": EMP_CTX, "score": 0.5, "updated_at": now_iso()},
        # internal (employer) offers for the employee domain
        {"uri": "offer://qk/o-payroll", "provider": SUBJ,
         "service": "payroll & benefits services to employees",
         "capability_keys": ["payroll"], "price": 0, "currency": "USD",
         "terms": "employment service", "status": "AVAILABLE"},
        {"uri": "offer://qk/o-benefits", "provider": SUBJ,
         "service": "benefits administration", "capability_keys": ["benefits"],
         "price": 0, "currency": "USD", "terms": "employment service",
         "status": "AVAILABLE"},
        # payroll worker delegation (capability-gated, §3.4/§7B)
        {"uri": "agent://w-payroll", "type": "AGENT"},
        {"uri": "rule://qk/w-payroll-run", "kind": "POLICY",
         "text": "payroll worker may issue paystub & disburse (reversible)",
         "grants": ["issue_paystub_and_disburse"]},
        {"uri": "delegation://qk/w-payroll", "grantor": SUBJ, "grantee": "agent://w-payroll",
         "scope": ["rule://qk/w-payroll-run"], "status": "ACTIVE"},
    ]
    _provision(sub, s4, "event://qk/s42-provision", 5000,
               "extend relationship to two roles (customer+employee) with scoped authz+trust",
               emp_objs)

    # ---- S1 role-scoped identity + role-scoped authority ------------------
    is_emp = s4.resolve_role_named(CTX, PERSON, "employee")
    is_cust = s4.resolve_role_named(CTX, PERSON, "customer")
    p_emp = s4.authorize_for_role(PERSON, "submit_timesheet", CTX, "employee")
    p_emp_pay = s4.authorize_for_role(PERSON, "receive_payroll", CTX, "employee")
    den_emp_quote = s4.authorize_for_role(PERSON, "request_quote", CTX, "employee")
    p_cust_quote = s4.authorize_for_role(PERSON, "request_quote", CTX, "customer")
    den_cust_pay = s4.authorize_for_role(PERSON, "receive_payroll", CTX, "customer")
    authrz = {
        "employee": {"submit_timesheet": isinstance(p_emp, Permission),
                     "receive_payroll": isinstance(p_emp_pay, Permission),
                     "request_quote_denied": isinstance(den_emp_quote, Denial)},
        "customer": {"request_quote": isinstance(p_cust_quote, Permission),
                     "receive_payroll_denied": isinstance(den_cust_pay, Denial)},
    }
    _provision(sub, s4, "event://qk/s42-authz", 5010,
               "role-scoped authorization proven both ways (same relationship, both roles)",
               [{"uri": "decision://qk/s42-role-authz", "by": "agent://s4",
                 "authority": "authority://qk/for-employment",
                 "confidence": 1.0, "actual_outcome": "scoped per role", "detail": authrz,
                 "made_at": now_iso()}])

    # ---- S2 intent/match for the employee role (payroll) ------------------
    intent_emp = {"subject": PERSON, "need": "payroll disbursement",
                  "capability_keys": ["payroll"], "urgency": "normal", "budget": None}
    emp_offers = [o for o in _offs(sub) if o["uri"] in ("offer://qk/o-payroll",
                                                        "offer://qk/o-benefits")]
    emp_matches = s2.match_offers(intent_emp, emp_offers,
                                  [{"target": k, "score": v} for k, v in _trust_map(sub).items()],
                                  trust_floor=0.4)
    top_emp = emp_matches[0]
    _provision(sub, s4, "event://qk/s42-match", 5020,
               f"employee-role match: {top_emp.offer_uri} (score {top_emp.score:.3f})",
               [{"uri": "decision://qk/s42-match", "by": "agent://s2",
                 "authority": "delegation://qk/s2-match", "alternatives": ["defer"],
                 "confidence": 0.9, "expected_outcome": top_emp.offer_uri,
                 "detail": top_emp.to_dict(), "made_at": now_iso()}])

    # ---- S3 commit + execute a reversible payroll micro-task ---------------
    payroll_offer = [o for o in emp_offers if o["uri"] == top_emp.offer_uri][0]
    commitment = s3.commit(payroll_offer, {"currency": "USD", "kind": "payroll",
                                           "signed": True},
                           by="agent://s3", i=5030,
                           expectation="expectation://qk/e-settle-emp-payroll",
                           signer="agent://s3")
    task = Task("t-payroll", "issue_paystub_and_disburse", "agent://w-payroll",
                "local", reversible=True, cost_knowable=True,
                delegation="delegation://qk/w-payroll")
    s3.route_seam(task, _trust_map(sub).get(SUBJ, 0.5))
    task.escalate_plan()
    pay_action = s3.execute_task(task, {"relationship": CTX, "role": "employee"}, i=5040)
    s3_step = pay_action["uri"] if pay_action else None

    # ---- S4 settle the payroll exchange -----------------------------------
    emp_exchange = {
        "slug": "emp-payroll", "buyer": SUBJ, "provider": PERSON,   # Quoteko pays the employee
        "price": 3200, "currency": "USD", "value": 3200, "cost": 3200,
        "due": "2026-10-31T00:00:00Z", "settled_at": "2026-09-30T00:00:00Z",
        "of": commitment["uri"],
    }
    emp_exp = _expectation_obj("emp-payroll", SUBJ, "employee payroll", 3200,
                               "2026-10-31T00:00:00Z")
    _provision(sub, s4, "event://qk/s42-emp-exp", 5050, "register payroll expectation",
               [emp_exp])
    emp_exch_event = s4.settle(emp_exchange, i=5060)
    emp_outcome = s4.evaluate(emp_exchange, emp_exp, i=5070)          # met

    # ---- S5 capture/verify -> employee-role Trust update ------------------
    emp_for_s5 = {
        "uri": "event://qk/s42-verify-payroll", "job": "job-emp-payroll-s4",
        "provider": SUBJ, "committed_deadline": emp_exchange["due"],
        "actual_completed_at": emp_exchange["settled_at"],
        "note": f"payroll settled per {emp_outcome['uri']} ({emp_outcome['evaluation']})",
    }
    ev_emp, _on = s5.capture(emp_for_s5, s5_demo.PROVENANCE, signer=SUBJ, i=5080)
    vr_emp = s5.verify(ev_emp, f"Quoteko payroll service met per {emp_outcome['uri']}",
                       emp_for_s5, i=5081)
    emp_trust = s5.update_trust(subject=PERSON, target=SUBJ,
                                claim="payroll & benefits reliability",
                                context=EMP_CTX, verify=vr_emp, evidence_score=vr_emp.degree,
                                i=5082, alpha=cfg["alpha"], expectation=cfg["expectation"],
                                recency=cfg["recency"])
    emp_next = s2.match_offers(intent_emp, emp_offers,
                               [{"target": k, "score": v} for k, v in _trust_map(sub).items()],
                               trust_floor=0.4)

    summary = {
        "role_employee": is_emp, "role_customer": is_cust, "authz": authrz,
        "emp_match": [m.to_dict() for m in emp_matches],
        "commitment": commitment["uri"], "pay_action": s3_step,
        "settle": emp_exch_event["uri"], "outcome": emp_outcome["uri"],
        "outcome_eval": emp_outcome["evaluation"],
        "emp_trust_before": 0.5, "emp_trust_after": emp_trust["score"],
        "emp_next": [m.to_dict() for m in emp_next],
        "customer_trust_untouched": sub.graph.get(f"trust://qk/t-solarworks")["score"],
    }
    sub._meta["s42"] = summary
    return summary


# ===========================================================================
# 4.3 — TWO org types on ONE relationship (private + charitable) + §6 floor
# ===========================================================================
def build_s43(sub: Substrate) -> dict:
    s1 = S1Service(sub); s2 = S2Service(sub); s3 = S3Service(sub)
    s4 = S4Service(sub); s5 = S5Service(sub)
    cfg = config_defaults()

    shelter = "org://qk/sunsetshelter"
    charity_objs = [
        {"uri": shelter, "type": "ORG"},
        {"uri": "purpose://qk/pv-quoteko", "for": SUBJ, "kind": "FOR_PROFIT",
         "statement": "Quoteko creates value and generates a financial return (§3.1 private)"},
        {"uri": "purpose://qk/pv-shelter", "for": shelter,
         "kind": "NONPROFIT_CHARITABLE",
         "statement": "Sunsetshelter pursues a charitable solar/mission benefit (§3.1)"},
        {"uri": CHARITY_CTX, "participants": [SUBJ, shelter],
         "roles": {SUBJ: ["donor"], shelter: ["beneficiary"]},
         "context": {"organization": shelter, "relationship": CHARITY_CTX,
                     "role": "donor", "jurisdiction": "US-NM",
                     "purpose": "purpose://qk/pv-shelter", "time": now_iso()},
         "purpose": "charitable solar installation at the shelter",
         "authority": ["authority://qk/for-charity"],
         "consent": ["consent://qk/charity-use"],
         "authority_by_role": {"donor": "authority://qk/for-charity",
                               "beneficiary": "authority://qk/for-charity"},
         "status": "ACTIVE", "created_at": now_iso(), "effective_from": now_iso()},
        {"uri": "authority://qk/for-charity", "holder": SUBJ,
         "grants": ["donate_install", "release_charitable_grant"],
         "roles": ["donor", "beneficiary"]},
        {"uri": "consent://qk/charity-use", "granted_by": shelter,
         "granted_for": "receive the charitable solar installation and grant",
         "scope": [], "duration": {"effective": "2026-09-01T00:00:00Z",
                                   "expires": "2027-09-01T00:00:00Z"},
         "revocable": True, "status": "GRANTED"},
        # charity-context scoped Trust (subject=donor, target=shelter)
        {"uri": "trust://qk/t-shelter", "subject": SUBJ, "target": shelter,
         "claim": "charitable installation reliability",
         "context": CHARITY_CTX, "score": 0.5, "updated_at": now_iso()},
        # purpose-constrained charitable offer (pro bono, §3.9 price=0)
        {"uri": "offer://qk/o-shelter-solar", "provider": shelter,
         "service": "charitable solar installation at the shelter",
         "capability_keys": ["solar", "install"], "price": 0, "currency": "USD",
         "terms": "pro bono; purpose-constrained to the shelter mission",
         "status": "AVAILABLE"},
        # worker fleet + bounded delegations (capability-gated, §3.4/§7B)
        {"uri": "agent://w-charity-install", "type": "AGENT"},
        {"uri": "agent://w-charity-dispatch", "type": "AGENT"},
        {"uri": "agent://w-charity-grant", "type": "AGENT"},
        {"uri": "rule://qk/w-charity-install-run", "kind": "POLICY",
         "text": "charity worker may prepare installation (reversible)",
         "grants": ["prepare_installation"]},
        {"uri": "rule://qk/w-charity-dispatch-run", "kind": "POLICY",
         "text": "charity worker may dispatch the solar crew (reversible)",
         "grants": ["dispatch_solar_crew"]},
        {"uri": "rule://qk/w-charity-grant-run", "kind": "POLICY",
         "text": "grant worker may release the charitable grant ONLY after human acknowledgement",
         "grants": ["release_charitable_grant"]},
        {"uri": "delegation://qk/w-charity-install", "grantor": SUBJ,
         "grantee": "agent://w-charity-install", "scope": ["rule://qk/w-charity-install-run"],
         "status": "ACTIVE"},
        {"uri": "delegation://qk/w-charity-dispatch", "grantor": SUBJ,
         "grantee": "agent://w-charity-dispatch", "scope": ["rule://qk/w-charity-dispatch-run"],
         "status": "ACTIVE"},
        {"uri": "delegation://qk/w-charity-grant", "grantor": SUBJ,
         "grantee": "agent://w-charity-grant", "scope": ["rule://qk/w-charity-grant-run"],
         "status": "ACTIVE"},
    ]
    _provision(sub, s4, "event://qk/s43-provision", 6000,
               "provision cross-org (private<->charitable) relationship + fleet", charity_objs)

    # ---- S1 roles + authorize in the charity context ----------------------
    donor_role = s4.resolve_role_named(CHARITY_CTX, SUBJ, "donor")
    bene_role = s4.resolve_role_named(CHARITY_CTX, shelter, "beneficiary")
    p_donate = s4.authorize_for_role(SUBJ, "donate_install", CHARITY_CTX, "donor")
    _provision(sub, s4, "event://qk/s43-authz", 6010,
               "cross-org role resolution + authorize (donor can donate_install)",
               [{"uri": "decision://qk/s43-authz", "by": "agent://s4",
                 "authority": "authority://qk/for-charity", "confidence": 1.0,
                 "actual_outcome": "donor authorized",
                 "detail": {"donor": donor_role, "beneficiary": bene_role,
                            "donate_install": isinstance(p_donate, Permission)},
                 "made_at": now_iso()}])

    # ---- S2 intent/match for the charitable install -----------------------
    intent_c = {"subject": SUBJ, "need": "charitable solar install at the shelter",
                "capability_keys": ["solar", "install"], "urgency": "normal"}
    c_matches = s2.match_offers(
        intent_c, [o for o in _offs(sub) if o["uri"] == "offer://qk/o-shelter-solar"],
        [{"target": k, "score": v} for k, v in _trust_map(sub).items()],
        trust_floor=0.4)
    top_c = c_matches[0]
    _provision(sub, s4, "event://qk/s43-match", 6020,
               f"charity-context match: {top_c.offer_uri} (score {top_c.score:.3f})",
               [{"uri": "decision://qk/s43-match", "by": "agent://s2",
                 "authority": "delegation://qk/s2-match", "alternatives": ["do nothing"],
                 "confidence": 0.9, "expected_outcome": top_c.offer_uri,
                 "detail": top_c.to_dict(), "made_at": now_iso()}])

    # ---- S3 commit + orchestrate the charitable install -------------------
    shelter_offer = [o for o in _offs(sub) if o["uri"] == top_c.offer_uri][0]
    commitment = s3.commit(shelter_offer, {"currency": "USD", "kind": "charitable-grant",
                                           "purpose": "shelter solar", "signed": True},
                           by="agent://s3", i=6030, signer="agent://s3")
    # signed split decision for the charity job
    _provision(sub, s4, "event://qk/s4-split-charity", 6035,
               "orchestrate shelter job: 2 reversible fleet steps + 1 irreversible grant",
               [{"uri": "decision://qk/s4-split-charity", "by": "agent://s3",
                 "authority": "authority://qk/for-charity",
                 "alternatives": ["defer"], "confidence": 0.9,
                 "expected_outcome": "install; grant time-locked to human",
                 "actual_outcome": "plan sealed", "made_at": now_iso()}])

    ctx_c = {"relationship": CHARITY_CTX, "role": "donor"}
    exec_ctx = dict(ctx_c)
    reversible_events = []
    locate = {"t-charity-prep": ("prepare_installation", "agent://w-charity-install",
                                 "local", "delegation://qk/w-charity-install", True, True),
              "t-charity-dispatch": ("dispatch_solar_crew", "agent://w-charity-dispatch",
                                     "private-cloud", "delegation://qk/w-charity-dispatch",
                                     True, True),
              "t-charity-grant": ("release_charitable_grant", "agent://w-charity-grant",
                                  "frontier", "delegation://qk/w-charity-grant", False, False)}
    tasks = {}
    for tid, (action, worker, seam, deleg, rev, ck) in locate.items():
        t = Task(tid, action, worker, seam, rev, ck, deleg)
        s3.route_seam(t, _trust_map(sub).get(shelter, 0.5))
        t.escalate_plan()
        tasks[tid] = t
    # reversible install steps auto-execute (full autonomy where failure is cheap)
    for tid in ("t-charity-prep", "t-charity-dispatch"):
        e = s3.execute_task(tasks[tid], exec_ctx, i=6040 + {"t-charity-prep": 0,
                                                            "t-charity-dispatch": 1}[tid])
        if e:
            reversible_events.append(e["uri"])
    # IRREVERSIBLE charitable grant MUST escalate to a human before execution (§6)
    esc = s3.escalate_to_human(tasks["t-charity-grant"], APPROVER, commitment, i=6050)
    hum = s3.human_acknowledge(tasks["t-charity-grant"], APPROVER,
                               "authority://qk/for-charity", commitment, i=6060)
    # ONLY NOW, after the signed human acknowledgement, may the grant be released.
    grant_event = s3.execute_task(tasks["t-charity-grant"], exec_ctx, i=6070)

    # ---- S4 settle the charitable exchange --------------------------------
    charity_exchange = {
        "slug": "shelter-solar", "buyer": SUBJ, "provider": shelter,
        "price": 0, "currency": "USD",                            # pro bono (§3.9)
        "value": 0, "cost": 18000,                                # cost borne by donor
        "due": "2026-12-31T00:00:00Z", "settled_at": "2026-11-20T00:00:00Z",
        "of": commitment["uri"],
    }
    c_exp = _expectation_obj("shelter-solar", SUBJ, "charitable solar install", 0,
                             "2026-12-31T00:00:00Z")
    _provision(sub, s4, "event://qk/s43-exp", 6080, "register charitable expectation",
               [c_exp])
    c_exch_event = s4.settle(charity_exchange, i=6090)
    c_outcome = s4.evaluate(charity_exchange, c_exp, i=6100)          # met

    # ---- S5 capture/verify -> charity-context Trust update ----------------
    c_for_s5 = {
        "uri": "event://qk/s43-verify-shelter", "job": "job-shelter-solar-s4",
        "provider": shelter, "committed_deadline": charity_exchange["due"],
        "actual_completed_at": charity_exchange["settled_at"],
        "note": f"charitable install settled per {c_outcome['uri']} ({c_outcome['evaluation']})",
    }
    ev_c, _on = s5.capture(c_for_s5, s5_demo.PROVENANCE, signer=shelter, i=6110)
    vr_c = s5.verify(ev_c, f"{shelter} charitable install met per {c_outcome['uri']}",
                     c_for_s5, i=6111)
    c_trust = s5.update_trust(subject=SUBJ, target=shelter,
                              claim="charitable installation reliability",
                              context=CHARITY_CTX, verify=vr_c,
                              evidence_score=vr_c.degree, i=6112,
                              alpha=cfg["alpha"], expectation=cfg["expectation"],
                              recency=cfg["recency"])
    c_next = s2.match_offers(
        intent_c, [o for o in _offs(sub) if o["uri"] == "offer://qk/o-shelter-solar"],
        [{"target": k, "score": v} for k, v in _trust_map(sub).items()],
        trust_floor=0.4)

    summary = {
        "donor_role": donor_role, "beneficiary_role": bene_role,
        "org_kind": {"quoteko": "FOR_PROFIT", "sunsetshelter": "NONPROFIT_CHARITABLE"},
        "charity_match": [m.to_dict() for m in c_matches],
        "commitment": commitment["uri"],
        "reversible_steps": reversible_events,
        "escalation": esc["uri"], "human": hum["uri"],
        "grant_executed": grant_event["uri"] if grant_event else None,
        "settle": c_exch_event["uri"], "outcome": c_outcome["uri"],
        "outcome_eval": c_outcome["evaluation"],
        "charity_trust_before": 0.5, "charity_trust_after": c_trust["score"],
        "charity_next": [m.to_dict() for m in c_next],
    }
    sub._meta["s43"] = summary
    return summary


def build_s4() -> Substrate:
    """Run the whole Sprint-4 chain: S1->S5 (Sprint 3) + S4 settlement + multi-role + multi-org."""
    sub, _b, _a = s5_demo.build_s2()          # Sprint-1/2 substrate + S5 loop
    s3_demo.build_s3(sub)                      # Sprint-3 orchestration + human floor
    build_s41(sub)                             # 4.1 settle + evaluate (closes loop with settlement)
    build_s42(sub)                             # 4.2 two roles, one relationship
    build_s43(sub)                             # 4.3 two org types + §6 floor
    return sub


def emit_s4_fixtures(sub: Substrate) -> dict[str, Path]:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    by_uri = {}
    for e in sub.ledger.entries:
        for obj in e.get("state_update") or []:
            by_uri[obj["uri"]] = obj

    def dump_grp(dir_name, name, prefixes):
        p = FIXTURES / dir_name / f"{name}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        items = [o for u, o in by_uri.items()
                 if u.startswith(tuple(f"{pfix}://" for pfix in prefixes))]
        p.write_text(json.dumps(items, indent=2))
        return p

    files = []
    # 4.1 settlement artifacts
    s41 = ["exchange", "event", "outcome"]            # event-exchanges + outcomes
    files.append(dump_grp("s4", "exchanges",
                          ["event"]))                # full event set incl. exchanges/outcomes
    files.append(dump_grp("s4", "obligations", ["obligation"]))
    files.append(dump_grp("s4", "receipts", ["receipt"]))
    files.append(dump_grp("s4", "assets", ["asset"]))
    files.append(dump_grp("s4", "reconciliation", ["decision"]))
    files.append(dump_grp("s4", "trust", ["trust"]))
    files.append(dump_grp("s4", "evidence", ["evidence"]))
    files.append(dump_grp("s4", "claim", ["claim"]))
    files.append(dump_grp("s4", "expectation", ["expectation"]))
    files.append(dump_grp("s4", "actors_offers", ["person", "org", "agent", "rule",
                                                  "purpose", "offer", "entity"]))
    files.append(dump_grp("s4", "relationships", ["relationship", "consent", "delegation",
                                                  "authority", "interaction"]))
    # ledger + statemachine + graph shared across the sprint-4 generation
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    lf = LEDGER_DIR / "ledger-quoteko.json"
    lf.write_text(json.dumps(sub.ledger.to_dict(), indent=2))
    files.append(lf)

    SM_DIR.mkdir(parents=True, exist_ok=True)
    rf = SM_DIR / "relationship.json"
    rf.write_text(json.dumps({"uri": CTX, "states": ["PROPOSED", "ACTIVE"]}))
    files.append(rf)

    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    gf = GRAPH_DIR / "current-state.json"
    gf.write_text(json.dumps(sub.graph.to_dict(), indent=2))
    files.append(gf)
    return {f.name: f for f in files}


if __name__ == "__main__":
    import run_s4_demo  # noqa: F401  (run end-to-end with checks)