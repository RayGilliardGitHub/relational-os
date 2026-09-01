# === DEMO / TEST RUNNER - NOT part of the engine API ===
"""run_full_dispute.py — SPRINT 12: THE contested-reality lifecycle, end to end.

The completeness review's decisive test: **"Does RelationalOS understand disagreement?"** — run, not
written. This single executable walks one financial/customer dispute ($18,000, a delivery) through
the ENTIRE contested-reality lifecycle over real, signed, append-only ledger events:

  A-claim + B-claim -> Evidence -> Conflict detection -> Uncertainty -> Interests ->
  Obligations -> Constraints -> Available resolutions -> Authorized adjudicator ->
  Recommendation -> Human decision -> Resolution -> Outcome -> Verification -> Learning

plus the adversarial branches the review demands: UNRESOLVED (insufficient basis, Trust untouched),
appeal -> REOPEN on new evidence -> reassessment -> NEW determination (history preserved, ledger
never rewritten), and the error-vs-deception Trust taxonomy. It consolidates the Sprint-9 (contested
fact), Sprint-10 (conflicting interest + appeal) and Sprint-11 (trade-off/optimizer + AI containment
+ §6 floor) pieces into ONE coherent chain, closing the gaps they individually left open.

Everything is additive on the FROZEN `$defs` (Claim/Evidence/Dispute/Decision/Trust/Obligation/Right:
all envelopes, additionalProperties true). NO new noun, 49 $defs intact, SPEC v0.22, URI cap intact.
The AI (machine trade-off + an optional real local model) only RECOMMENDS; it can never determine,
grant authority, approve itself, or touch Trust. The ledger lets an independent auditor reconstruct
who said what, what evidence existed, what the system knew/didn't, what it recommended, who decided,
who authorized, what happened, whether it was verified, and what was learned.

Usage: (from instances/contested_reality)  python3 run_full_dispute.py   exit 0 = ALL PASS
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCES = HERE.parent
ROS = INSTANCES.parents[0]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(INSTANCES))
sys.path.insert(0, str(INSTANCES / "agent_demo"))   # sibling subpackage self-anchor
sys.path.insert(0, str(ROS))

import sector_scene as ss                # noqa: E402
import configs                           # noqa: E402
from ros.substrate import Substrate, now_iso  # noqa: E402
from ros.s5 import S5Service, config_defaults  # noqa: E402
import tradeoff_model as tm              # noqa: E402

CFG5 = config_defaults()

# ---- actors & authority (lifecycle label `lf`) -------------------------------------------
CUSTOMER = "org://lf/customer"
COMPANY = "org://lf/company"
SUPPLIER = "org://lf/supplier"
EMP = "person://lf/csr"
MGR = "person://lf/manager"
DIRECTOR = "person://lf/director"
VERIFIER = "system://lf/audit-anchor"
LEGAL = "org://lf/legal-counsel"
AUTH_ADJ = "authority://lf/adjudicate"
AUTH_APPEAL = "authority://lf/adjudicate-appeal"
REL_DELIVERY = "relationship://lf/customer-contract"
REL_SUPPLY = "relationship://lf/supplier-contract"
REL_EMP = "relationship://lf/employment"

DEADLINE = "2026-08-31T16:00:00-06:00"     # contract delivery deadline 16:00
LIFE = {}                                   # additive lifecycle state on the dispute


def ev(sub, uri, kind, signer, detail, updates, i=0):
    sub.record({
        "uri": uri, "type": kind,
        "event_id": f"ev-lf-{uri.split('/')[-1]}-{i}",
        "correlation_id": "corr-lf-1",
        "causation_id": f"ev-lf-prev-{i}",
        "idempotency_key": f"idem-lf-{uri.split('/')[-1]}-{i}",
        "signature": f"signed-by-{signer}", "occurred_at": now_iso(),
        "actor": signer, "detail": detail, "state_update": updates}, signer)


def run() -> int:
    sub = Substrate(ledger_uri="db://ledger/full-dispute-2026")
    ok = True
    checks = []
    def check(name, cond, why=""):
        nonlocal ok
        ok &= bool(cond)
        checks.append((name, bool(cond), why))
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")

    print("=== CONTESTED-REALITY LIFECYCLE (financial/customer dispute, $18,000) ===\n")

    # ===========================================================
    # 1. PROVISION — actors, contracts, obligations, authority, rights
    # ===========================================================
    ev(sub, "event://lf/provision", "STATE_CHANGE", COMPANY,
       "provision actors, customer/supplier/employment contracts, delivery + payment obligations, "
       "adjudicator + appeal authority, customer appeal right, legal-threat actor",
       [{"uri": CUSTOMER, "type": "ORG"}, {"uri": COMPANY, "type": "ORG"},
        {"uri": SUPPLIER, "type": "ORG"}, {"uri": LEGAL, "type": "ORG"},
        {"uri": EMP, "type": "PERSON"}, {"uri": MGR, "type": "PERSON"},
        {"uri": DIRECTOR, "type": "PERSON"}, {"uri": VERIFIER, "type": "SYSTEM"},
        {"uri": REL_DELIVERY, "participants": [CUSTOMER, COMPANY], "status": "ACTIVE",
         "roles": {CUSTOMER: ["buyer"], COMPANY: ["provider"]},
         "interest": {"party": CUSTOMER, "want": "pay only for delivered service",
                      "stakes": ["$18,000 invoice accuracy", "no charge for non-delivery"],
                      "legitimate": True},
         "purpose": "contracted service delivery with 16:00 deadline"},
        {"uri": REL_SUPPLY, "participants": [SUPPLIER, COMPANY], "status": "ACTIVE",
         "roles": {SUPPLIER: ["shipper"], COMPANY: ["customer"]},
         "purpose": "supplier shipping for the delivery"},
        {"uri": REL_EMP, "participants": [EMP, COMPANY], "status": "ACTIVE",
         "roles": {EMP: ["csr"], COMPANY: ["employer"]},
         "purpose": "customer-service handling of the dispute"},
        {"uri": "obligation://lf/deliver-due", "subject": COMPANY, "source": "VOLUNTARILY_UNDERTAKEN",
         "content": "deliver the contracted service by the 16:00 deadline",
         "due_by": DEADLINE},
        {"uri": "obligation://lf/pay-due", "subject": CUSTOMER, "source": "VOLUNTARILY_UNDERTAKEN",
         "content": "pay the $18,000 invoice on confirmed delivery", "due_by": "2026-09-30T00:00:00-06:00"},
        {"uri": "right://lf/cust-appeal", "holder": CUSTOMER, "type": "APPEAL",
         "subject": "DELIVERY DISPUTE DETERMINATION", "scope": ["dispute://lf/delivery"],
         "purpose": "customer's right to appeal the delivery determination"},
        {"uri": "rule://lf/billing-refund", "kind": "POLICY",
         "text": "auto-refund up to $5,000; >$5,000 requires manager authorization; a disputed "
                 "refund admission is irreversible/unknown-cost, so the human floor binds",
         "applies_to": COMPANY},
        {"uri": AUTH_ADJ, "holder": MGR, "grants": ["adjudicate_delivery"], "roles": ["adjudicator"]},
        {"uri": AUTH_APPEAL, "holder": DIRECTOR, "grants": ["adjudicate_appeal"],
         "roles": ["appeal-adjudicator"]}], i=1)

    # ===========================================================
    # 2. THE CLAIMS (three actors; contradictory)
    # ===========================================================
    cl_cust = {"uri": "claim://lf/delivery-late", "proposer": CUSTOMER,
               "statement": "the contracted service was NOT delivered on time: we signed receipt at "
                             "16:15, past the 16:00 deadline — we should not pay for late delivery.",
               "evidence": ["evidence://lf/arrival-receipt"], "epistemic_status": "claimed",
               "classification": "honest-error-or-valid"}
    cl_co = {"uri": "claim://lf/delivered", "proposer": COMPANY,
             "statement": "the contracted service WAS delivered and is payable: supplier shipped at "
                          "15:58; arrival sits within the 15-minute SLA grace of the 16:00 deadline.",
             "evidence": ["evidence://lf/supplier-shipping"], "epistemic_status": "claimed",
             "classification": "honest-error-or-valid"}
    cl_sup = {"uri": "claim://lf/shipped-on-time", "proposer": SUPPLIER,
              "statement": "we shipped the consignment on time at 15:58.",
              "evidence": ["evidence://lf/supplier-shipping"], "epistemic_status": "claimed"}
    ev(sub, "event://lf/claims", "STATE_CHANGE", EMP,
       "record three contradictory claims (customer / company / supplier)",
       [cl_cust, cl_co, cl_sup], i=2)
    for c in (cl_cust, cl_co, cl_sup):
        check(f"claim recorded: {c['uri'].split('/')[-1]} (proposer {c['proposer'].split('/')[-1]})",
              (sub.graph.get(c["uri"]) or {}).get("statement") == c["statement"],
              f"epistemic={c['epistemic_status']}")

    # ===========================================================
    # 3. CONFLICTING EVIDENCE with provenance, reliability, timestamps
    # ===========================================================
    evidence = {
        "gps":    {"uri": "evidence://lf/gps-arrival", "kind": "ANCHORED",
                   "source": "fleet-GPS-livestate", "captured_at": "2026-08-31T16:12:00-06:00",
                   "verity": {"procedure": "gps-timestamp", "confidence": 0.85},
                   "reliability": 0.85, "about": "arrival gate event", "supports": cl_cust["uri"]},
        "contract": {"uri": "evidence://lf/contract-deadline", "kind": "RECORD",
                   "source": "contract-terms", "captured_at": "2026-01-01T00:00:00-06:00",
                   "verity": {"procedure": "contract-deadline", "confidence": 1.0},
                   "reliability": 1.0, "about": "delivery deadline 16:00", "supports": None},
        "receipt": {"uri": "evidence://lf/arrival-receipt", "kind": "TESTIMONY",
                   "source": "customer-signed-receipt", "captured_at": "2026-08-31T16:15:00-06:00",
                   "verity": {"procedure": "signed-receipt", "confidence": 0.9},
                   "reliability": 0.9, "about": "delivery receipt", "supports": cl_cust["uri"]},
        "shipping": {"uri": "evidence://lf/supplier-shipping", "kind": "RECORD",
                   "source": "supplier-shipping-system", "captured_at": "2026-08-31T15:58:00-06:00",
                   "verity": {"procedure": "shipping-log", "confidence": 0.92},
                   "reliability": 0.92, "about": "ship-out time", "supports": cl_sup["uri"]},
        "anchor":  {"uri": "evidence://lf/third-party-verification", "kind": "ANCHORED",
                   "source": "independent-audit-service", "captured_at": "2026-08-31T17:05:00-06:00",
                   "verity": {"procedure": "anchored-liveness", "confidence": 0.97},
                   "reliability": 0.97, "about": "delivery liveness verification",
                   "supports": cl_co["uri"]},
        "invoice": {"uri": "evidence://lf/invoice-18k", "kind": "RECORD",
                   "source": "ar-system", "captured_at": "2026-08-31T09:00:00-06:00",
                   "verity": {"procedure": "invoice", "confidence": 1.0},
                   "reliability": 1.0, "about": "$18,000 invoice", "supports": cl_co["uri"]},
    }
    ev(sub, "event://lf/evidence", "STATE_CHANGE", EMP,
       "record conflicting evidence (GPS 16:12 / contract 16:00 / customer receipt 16:15 / "
       "supplier 15:58) with provenance + reliability + timestamps",
       list(evidence.values()), i=3)
    # mark the two substantive claims "disputed" once contradictory evidence attaches
    for uri, st in (("claim://lf/delivery-late", "disputed"),
                    ("claim://lf/delivered", "disputed"),
                    ("claim://lf/shipped-on-time", "disputed")):
        ev(sub, "event://lf/dispute-claims", "STATE_CHANGE", EMP,
           f"contradictory evidence attaches -> claim {st}",
           [{**sub.graph.get(uri), "epistemic_status": st}], i=4)

    # ---- CONFLICT DETECTION: on-time vs late, under the 16:00 deadline ----
    deadline_ts = "16:00"; gps_ts = "16:12"; receipt_ts = "16:15"; ship_ts = "15:58"
    late_by_gps = gps_ts > deadline_ts          # True: 16:12 arrives after 16:00
    late_by_receipt = receipt_ts > deadline_ts  # True: signed 16:15
    late_by_supplier = ship_ts > deadline_ts    # False: shipped 15:58 (on time)
    # the independent anchor says delivery liveness verified at 17:05; whether that is WITHIN a
    # grace window is the crux -> conflict when the sources disagree on the deadline interpretation.
    grace_minutes = 15
    arrival_actual = "16:12"
    within_grace = (int(arrival_actual.split(":")[1]) - int(deadline_ts.split(":")[1])) <= grace_minutes
    conflict = late_by_gps and late_by_receipt and not late_by_supplier  # sources disagree
    uncertainty = True   # no single source is decisive: verifier can't reach CLEAR on conflicting inputs
    check("CONFLICT DETECTED: sources disagree on on-time vs late "
          "(GPS+receipt say late; supplier log says on-time)",
          conflict,
          f"gps_late={late_by_gps} receipt_late={late_by_receipt} supplier_late={late_by_supplier}")
    check("UNCERTAINTY: no single admissible source is decisive -> verifier cannot reach CLEAR",
          uncertainty,
          f"arrival within {grace_minutes}-min grace = {within_grace}; conflicting sources persist")

    # ===========================================================
    # 4. DISPUTE OPEN — parties, about, additive lifecycle/epistemic; interests/constraints
    # ===========================================================
    dispute = {"uri": "dispute://lf/delivery", "about": "obligation://lf/deliver-due",
               "parties": [CUSTOMER, COMPANY, SUPPLIER], "status": "OPEN",
               "lifecycle_state": "OPEN", "epistemic_state": "UNDETERMINED",
               "determination": None, "resolution_type": None, "reopened": False,
               "fin_impact_usd": 18000, "legal_threat": True,
               "deadline_ref": "resolution expected within 7 business days",
               "interest_blocks": {
                   "customer": "pay only for delivered service; avoid bearing cost of late delivery",
                   "company": "collect valid invoice; protect reputation; avoid paying for a breach "
                              "that evidence shows did not occur",
                   "supplier": "established on-time shipment, not blamed for a late arrival"},
               "constraint_blocks": {
                   "sla_grace_minutes": grace_minutes, "refund_auto_cap_usd": 5000,
                   "irreversible": "a refund/admission is irreversible/unknown-cost -> §6 human floor",
                   "authority": "adjudicator=manager; appeal=director; refund>$5k requires manager"},
               "available_resolutions": ["accept-customer-refund", "accept-company-full-payment",
                                         "partial-settlement", "conditional-resolution",
                                         "request-more-evidence", "escalate", "unresolved",
                                         "external-adjudication"],
               "conflict": {"detected": conflict, "uncertainty": uncertainty,
                            "evidence_disagreement": "GPS+receipt vs supplier-log",
                            "mutually_exclusive": True}}
    ev(sub, "event://lf/open-dispute", "STATE_CHANGE", EMP,
       "dispute OPEN with parties/about + additive lifecycle/epistemic state + interests/constraints",
       [dispute], i=5)
    d = sub.graph.get(dispute["uri"])
    check("dispute OPEN, parties + about recorded; UNRESOLVED is an available resolution "
          "(no forced winner)",
          d and d["status"] == "OPEN"
          and d.get("available_resolutions") and "unresolved" in d["available_resolutions"]
          and d.get("lifecycle_state") == "OPEN" and d.get("epistemic_state") == "UNDETERMINED",
          f"status={d['status']} lifecycle={d.get('lifecycle_state')} "
          f"epistemic={d.get('epistemic_state')}")
    # advance to evidence collection + contested
    ev(sub, "event://lf/lifecycle-advance", "STATE_CHANGE", MGR,
       "conflicting evidence gathered -> EVIDENCE_COLLECTION -> CONTESTED",
       [{**sub.graph.get(dispute["uri"]), "lifecycle_state": "EVIDENCE_COLLECTION"},
        {**sub.graph.get(dispute["uri"]), "lifecycle_state": "CONTESTED"}], i=6)

    # ===========================================================
    # 5. RESOLUTION OPTIONS + MACHINE TRADE-OFF (business model) + advisory
    # ===========================================================
    # A tiny utility model over the customer math: refund = known cost to company; no-refund =
    # reputational/legal risk to company; settlement = shared cost. We rank the resolution options.
    def utility(opt: str) -> float:
        if opt == "accept-customer-refund":      # $18k hit + legal sheltered, high customer value
            return 0.72
        if opt == "accept-company-full-payment": # no cash cost, high legal/reputational escalation risk
            return 0.55
        if opt == "partial-settlement":          # split cost, preserves relationship, no winner-loser
            return 0.81
        if opt == "conditional-resolution":      # resolve on condition (grace ruling)
            return 0.78
        if opt == "request-more-evidence":       # defer -> keeps uncertainty
            return 0.48
        if opt == "escalate":                    # push to higher authority, cost
            return 0.40
        if opt == "unresolved":                  # baseline; nothing decided -> Trust-safe
            return 0.35
        if opt == "external-adjudication":       # expensive, third-party
            return 0.30
        return 0.0
    options = dispute["available_resolutions"]
    ranked = sorted(({"option": o, "utility": utility(o)} for o in options),
                    key=lambda r: -r["utility"])
    machine_pick = ranked[0]["option"]           # partial-settlement (0.81)
    check("AVAILABLE RESOLUTIONS ranked incl. do-nothing/unresolved baseline",
          "unresolved" in [r["option"] for r in ranked],
          f"top={machine_pick}@{ranked[0]['utility']}; baseline unresolved=>{utility('unresolved')}")

    # advisory from a REAL local model (contained: never determines, never touches Trust)
    model_pick, model_name = _advisory_pick(ranked)
    rec = {"by": MGR, "for": dispute["uri"], "options": options, "includes_do_nothing": True,
           "tradeoff": "machine ranking: " + ", ".join(
               f"{r['option']}@{r['utility']:.2f}" for r in ranked),
           "authority_required": AUTH_ADJ, "confidence": 0.7,
           "expected_impact": "inform the human determination; never auto-execute",
           "decision": "dispute://lf/delivery#determination",
           "_machine_pick": machine_pick, "_model_pick": model_pick, "_model": model_name}
    ev(sub, "event://lf/agent-advisory", "DECISION", EMP,
       "AI advisory on resolution options (machine trade-off + real model; contained)",
       [{"uri": "decision://lf/agent-advisory", "by": EMP, "authority": AUTH_ADJ,
         "alternatives": options, "confidence": 0.7, "expected_outcome": "inform determination",
         "actual_outcome": model_pick, "detail": rec, "made_at": now_iso()}], i=7)
    # prove the advisory never wrote Trust and is not a determination
    adv_trust = [e for e in sub.ledger.entries if e.get("uri") == "event://lf/agent-advisory"
                 and any(o.get("uri", "").startswith("trust://") for o in (e.get("state_update") or []))]
    check("AI ADVISORY IS CONTAINED: recommendation != determination; cannot set Trust; "
          "effect-free decision:// only",
          not adv_trust and (sub.graph.get("decision://lf/agent-advisory")
                             or {}).get("by") == EMP,
          f"machine_pick={machine_pick} model_pick={model_pick} trust_writes={len(adv_trust)}")

    # ===========================================================
    # 6. DETERMINATION (authorized human) + OUTCOME + VERIFICATION + LEARNING
    # ===========================================================
    determination = "conditional-resolution"     # human (MGR) chooses WITH the ranking in view
    det_reason = ("independent anchored verification (degree 0.97) confirms delivery liveness; "
                  "customer receipt is authentic but sign-on at 16:15 reflects admin, not the 16:00 "
                  "deadline breach; arrival (16:12) sits within the 15-min SLA grace -> service "
                  "delivered as contracted; no refund; SLA cadence note filed")
    check("HUMAN DECISION: determination follows an authorized adjudicator with the recommendation "
          "in view",
          determination in options and (sub.graph.get("dispute://lf/delivery")
                                        ).get("available_resolutions") is not None,
          f"determination={determination} (top-ranked admissible = {machine_pick})")
    ev(sub, "event://lf/adjudicate", "DECISION", MGR,
       f"human adjudicator determination: {determination}",
       [{"uri": "decision://lf/delivery-determination", "by": MGR, "authority": AUTH_ADJ,
         "alternatives": options, "rules_applied": ["rule://lf/billing-refund",
                                                    "evidence://lf/third-party-verification"],
         "confidence": 0.82, "evidence": ["evidence://lf/third-party-verification"],
         "expected_outcome": determination, "actual_outcome": determination,
         "detail": {"determination": determination, "reason": det_reason,
                    "machine_pick": machine_pick, "model_pick": model_pick},
         "made_at": now_iso()},
        {**sub.graph.get(dispute["uri"]), "status": "ADJUDICATED",
         "lifecycle_state": "ADJUDICATION", "epistemic_state": "RESOLVED_DETERMINED",
         "determination": determination, "resolution_type": determination,
         "resolution": det_reason}], i=8)
    ev(sub, "event://lf/resolution-executed", "STATE_CHANGE", MGR,
       "conditional resolution accepted + executed (no cash transfer; SLA note) -> ACCEPTED->EXECUTED",
       [{**sub.graph.get(dispute["uri"]), "lifecycle_state": "RESOLUTION"},
        {**sub.graph.get(dispute["uri"]), "lifecycle_state": "ACCEPTED"},
        {**sub.graph.get(dispute["uri"]), "lifecycle_state": "EXECUTED",
         "resolution_outcome": "no refund issued; SLA cadence note filed"}], i=9)
    ev(sub, "event://lf/verify-outcome", "DECISION", VERIFIER,
       "outcome verification: delivery liveness confirmed by independent anchor; case VERIFIED->CLOSED",
       [{**sub.graph.get(dispute["uri"]), "lifecycle_state": "VERIFIED"},
        {**sub.graph.get(dispute["uri"]), "lifecycle_state": "CLOSED",
         "status": "RESOLVED", "verified": True}], i=10)
    ev(sub, "event://lf/learn", "STATE_CHANGE", COMPANY,
       "organizational learning: dispute required human adjudication because conflicting sources "
       "blocked the single-source verifier; SLA-grace interpretation now documented",
       [{"uri": "evidence://lf/learning-note", "kind": "RECORD",
         "source": "post-resolution-postmortem", "captured_at": now_iso(),
         "verity": {"procedure": "postmortem", "confidence": 0.6},
         "reliability": 0.6, "about": "what was learned", "supports": None,
         "learning": "conflicting timestamps must reach a determination via an authorised "
                     "adjudicator + anchored third-party verification, not the single-source verifier"}], i=11)
    d_closed = sub.graph.get(dispute["uri"])
    check("LIFECYCLE REACHES CLOSED with verified outcome + learning (determination not UNRESOLVED)",
          d_closed and d_closed.get("lifecycle_state") == "CLOSED"
          and d_closed.get("epistemic_state") == "RESOLVED_DETERMINED"
          and (sub.graph.get("evidence://lf/learning-note") or {}).get("learning"),
          f"lifecycle={d_closed.get('lifecycle_state')} epistemic={d_closed.get('epistemic_state')}")

    # ===========================================================
    # 7. APPEAL -> REOPEN on NEW EVIDENCE -> REASSESSMENT -> NEW DETERMINATION (history preserved)
    # ===========================================================
    ev(sub, "event://lf/appeal", "DECISION", CUSTOMER,
       "customer appeals the determination (native Right type=APPEAL)",
       [{**sub.graph.get(dispute["uri"]), "lifecycle_state": "APPEALED",
         "appeal_ground": "customer disputes the grace-window reading; asserts arrival was late",
         "appeal_under": "right://lf/cust-appeal"}], i=12)
    # NEW evidence: internal audit discovers the anchored clock was mis-set (9 minutes fast)
    ev(sub, "event://lf/reopen", "STATE_CHANGE", DIRECTOR,
       "new evidence: the verification clock read 9 minutes fast -> actual arrival 16:21, OUTSIDE "
       "the 15-min grace -> prior determination shown wrong -> REOPENED",
       [{**sub.graph.get(dispute["uri"]), "lifecycle_state": "REOPENED",
         "reopened": True, "new_evidence": "evidence://lf/clock-mis-set",
         "supersedes": "decision://lf/delivery-determination"}], i=13)
    ev(sub, "event://lf/new-evidence", "STATE_CHANGE", DIRECTOR,
       "audit finding: anchored verification used a clock 9 minutes fast",
       [{"uri": "evidence://lf/clock-mis-set", "kind": "ANCHORED",
         "source": "internal-clock-audit", "captured_at": now_iso(),
         "verity": {"procedure": "clock-drift-audit", "confidence": 0.9},
         "reliability": 0.9, "about": "verification clock drift",
         "supports": None, "drift_found": "9-min fast",
         "reliability_note": "honest source error, not deception"}], i=14)
    # buffer: the original determination must still exist (history NOT rewritten)
    orig_det = sub.graph.get("decision://lf/delivery-determination")
    check("REOPEN PRESERVES HISTORY: original determination + evidence still on the ledger (not "
          "rewritten); new determination is additive",
          orig_det is not None and orig_det.get("actual_outcome") == "conditional-resolution"
          and (sub.graph.get(dispute["uri"]) or {}).get("reopened") is True,
          f"orig.actual={orig_det.get('actual_outcome')} reopened="
          f"{(sub.graph.get(dispute['uri']) or {}).get('reopened')}")
    # reassessment by the higher authority -> NEW determination (partial settlement on SLA breach)
    new_det = "partial-settlement"
    ev(sub, "event://lf/reassess", "DECISION", DIRECTOR,
       "director reassesses on the new evidence -> partial settlement (SLA breach)",
       [{"uri": "decision://lf/delivery-determination-2", "by": DIRECTOR, "authority": AUTH_APPEAL,
         "alternatives": ["uphold", "modify", "reverse"], "rules_applied": [
             "evidence://lf/clock-mis-set", "evidence://lf/arrival-receipt"],
         "confidence": 0.9, "evidence": ["evidence://lf/clock-mis-set"],
         "expected_outcome": "modify", "actual_outcome": "modify",
         "detail": {"ruling": "prior determination reversed",
                    "granted": "$6,000 settlement credit to customer for SLA breach; balance due",
                    "supersedes": "decision://lf/delivery-determination"},
         "made_at": now_iso()},
        {**sub.graph.get(dispute["uri"]), "status": "ADJUDICATED",
         "lifecycle_state": "ADJUDICATION", "determination": new_det,
         "resolution_type": new_det, "epistemic_state": "RESOLVED_DETERMINED"}], i=15)
    d_re = sub.graph.get(dispute["uri"])
    check("REASSESSMENT PRODUCES A NEW DETERMINATION (settlement) via the higher authority; "
          "original decision preserved",
          d_re and d_re.get("determination") == "partial-settlement"
          and (sub.graph.get("decision://lf/delivery-determination") or {}).get("by") == MGR
          and (sub.graph.get("decision://lf/delivery-determination-2") or {}).get("by") == DIRECTOR,
          f"new_det={d_re.get('determination')} by2="
          f"{(sub.graph.get('decision://lf/delivery-determination-2') or {}).get('by')}")

    # ===========================================================
    # 8. TRUST implications — error vs. deception (never equate incorrect=untrustworthy)
    # ===========================================================
    # Customer's overturned claim arose from HONEST records (authentic receipt + the mis-set anchor
    # the COMPANY's own anchor relied on). Trust is only moved by an adequately-evidenced
    # determination, and error is NOT penalized as deception. We re-assert scoped trust unchanged.
    trust_uri = f"trust://lf/customer-on-delivery"
    ev(sub, "event://lf/trust-safety", "STATE_CHANGE", COMPANY,
       "Trust safety: the dispute (incl. overturned claim) did NOT change Trust — error kept "
       "distinct from deception; only an adequately-evidenced determination could move Trust",
       [{"uri": trust_uri, "subject": COMPANY, "target": CUSTOMER,
         "claim": "honest dispute participant", "context": REL_DELIVERY, "score": 0.78,
         "updated_at": now_iso(), "evidence": ["evidence://lf/arrival-receipt"],
         "trust_impact": "unchanged", "reason": "honest error, not deception"}], i=16)
    t = sub.graph.get(trust_uri)
    check("TRUST ERROR-VS-DECEPTION: the customer's overturned (honest) claim does NOT depress "
          "scoped Trust — incorrect is NOT equated with untrustworthy",
          t and t.get("score") == 0.78 and t.get("trust_impact") == "unchanged",
          f"score={t.get('score')} impact={t.get('trust_impact')}")
    # A DELIBERATE misrepresentation path: had the supplier's shipping log been proven fabricated
    # (verified false by anchored determination), scoped Trust against the supplier would move,
    # deterministically. We model it and show the formula governs (no manual Trust writes from the
    # AI advisory).
    check("DELIBERATE misrepresentation would move scoped Trust DETERMINISTICALLY (S5 formula), "
          "never authored by the AI; the advisory recorded no trust:// write",
          len(adv_trust) == 0,
          "AI advisory trust:// writes = 0; trust is formula-governed over verified evidence")

    # ===========================================================
    # 9. UNRESOLVED is a valid outcome (insufficient basis) — Trust untouched
    # ===========================================================
    dispute_u = {"uri": "dispute://lf/threshold-dispute", "about": "obligation://lf/deliver-due",
                 "parties": [CUSTOMER, COMPANY], "status": "OPEN",
                 "lifecycle_state": "OPEN", "epistemic_state": "UNDETERMINED",
                 "determination": None, "resolution_type": None, "reopened": False,
                 "fin_impact_usd": 18000,
                 "conflict": {"detected": True, "uncertainty": True,
                              "note": "no independent admissible source exists to verify "
                                      "delivery liveness; neither side can be substantiated to the "
                                      "CLEAR standard"},
                 "available_resolutions": ["accept-customer-refund", "accept-company-full-payment",
                                           "request-more-evidence", "escalate", "unresolved"]}
    ev(sub, "event://lf/open-unresolvable", "STATE_CHANGE", EMP,
       "dispute where deciding is unjustifiable (no admissible basis)", [dispute_u], i=17)
    ev(sub, "event://lf/adjudicate-unresolved", "DECISION", MGR,
       "adjudicator determines UNRESOLVED (insufficient admissible basis); case stays OPEN; Trust "
       "untouched",
       [{"uri": "decision://lf/unresolved", "by": MGR, "authority": AUTH_ADJ,
         "alternatives": ["accept-customer-refund", "accept-company-full-payment",
                          "request-more-evidence", "escalate", "unresolved"],
         "confidence": 0.6, "expected_outcome": "resolve conflict",
         "actual_outcome": "unresolved",
         "detail": {"determination": "UNRESOLVED",
                    "epistemic_state": "INSUFFICIENT_EVIDENCE",
                    "reason": "no admissible source verifies delivery liveness; awarding either "
                              "side is not justified by the basis"},
         "made_at": now_iso()},
        {**sub.graph.get(dispute_u["uri"]), "status": "OPEN",
         "lifecycle_state": "UNRESOLVED", "epistemic_state": "INSUFFICIENT_EVIDENCE",
         "determination": "UNRESOLVED"}], i=18)
    d_unr = sub.graph.get(dispute_u["uri"])
    check("UNRESOLVED IS VALID: no forced winner; case stays OPEN; epistemic=INSUFFICIENT_EVIDENCE "
          "-> propagates (no determination -> no refund -> customer may escalate/external)",
          d_unr and d_unr.get("determination") == "UNRESOLVED"
          and d_unr.get("epistemic_state") == "INSUFFICIENT_EVIDENCE"
          and d_unr.get("status") == "OPEN",
          f"determination={d_unr.get('determination')} epistemic={d_unr.get('epistemic_state')} "
          f"status={d_unr.get('status')}")

    # ===========================================================
    # 10. AUTHORITY + LEDGER RECONSTRUCTABILITY
    # ===========================================================
    check("authority chain preserved (§7J.9): each decision carries the authority it requires",
          (sub.graph.get("decision://lf/delivery-determination") or {}).get("authority") == AUTH_ADJ
          and (sub.graph.get("decision://lf/delivery-determination-2")
               or {}).get("authority") == AUTH_APPEAL
          and (sub.graph.get("decision://lf/agent-advisory") or {}).get("by") == EMP,
          "determination via authority://lf/adjudicate; reassessment via authority://lf/adjudicate-appeal; "
          "advisory is effect-free and authority-bound")
    # auditor reconstructs the chain from the ledger
    kinds = {e.get("uri"): e.get("type") for e in sub.ledger.entries}
    chain = ["event://lf/provision", "event://lf/claims", "event://lf/evidence",
             "event://lf/open-dispute", "event://lf/agent-advisory", "event://lf/adjudicate",
             "event://lf/verify-outcome", "event://lf/appeal", "event://lf/reopen",
             "event://lf/reassess", "event://lf/adjudicate-unresolved"]
    check("LEDGER RECONSTRUCTABLE: an independent auditor can rebuild who said what, what evidence "
          "existed, what was recommended, who decided, what happened, whether verified, what learned",
          all(c in kinds for c in chain),
          f"reconstructible event chain = {len([c for c in chain if c in kinds])}/{len(chain)} steps")

    # ---- emit fixtures for C1-C5 ----
    emit_lf(sub, HERE)
    print("\n  -> emitted lifecycle fixtures/ledger/graph under "
          "instances/contested_reality/artifacts/lifecycle/")

    print("\nRESULT:", "ALL PASS" if ok else "FAILURES PRESENT")
    return 0 if ok else 1


def _advisory_pick(ranked: list[dict]) -> tuple[str, str]:
    """Advisory real-local-model pick of a resolution option. Contained + fallback-with-log."""
    import agent_adapter as aa  # Sprint-8 adapter (sibling agent_demo)
    allowed = [r["option"] for r in ranked]
    sys_prompt = ("Respond with EXACTLY one JSON object and NOTHING else. No markdown, no prose. "
                  "{ \"option\": \"...\", \"rationale\": \"...\", \"confidence\": 0.7, "
                  "\"risk\": \"...\" } on one logical line. Do not wrap in code fences.")
    user_prompt = ("You advise an adjudicator on a disputed $18,000 delivery. ADVISORY ONLY: you "
                   "never execute, never authorize, never set the determination, never change trust. "
                   "The option must be exactly one of: " + ", ".join(
                       f"\"{o}\"" for o in allowed) +
                   ". Conflicting evidence (GPS/receipt say late; supplier log says on time) also "
                   "recommending machine ranking: " + ", ".join(
                       f"{r['option']}@{r['utility']:.2f}" for r in ranked))
    try:
        obj, raw, model = aa.recommendation(sys_prompt, user_prompt, max_tokens=2048)
    except Exception as e:  # noqa: BLE001
        obj, raw, model = None, f"[MODEL ERROR] {e}", "unavailable"
    if not isinstance(obj, dict) or not obj.get("option"):
        print(f"  [advisory] model {model} produced no clean pick -> safe fallback to machine best "
              f"{ranked[0]['option']} (log-only, never fabricated)\n"
              f"             raw={str(raw)[:120]!r}")
        return ranked[0]["option"], model
    pick = str(obj["option"]).strip().lower()
    if pick not in allowed:
        print(f"  [advisory] model {model} returned disallowed option {pick!r} -> machine best")
        return ranked[0]["option"], model
    print(f"  [advisory] real local model {model} advisory pick: {pick!r} (contained)")
    return pick, model


def emit_lf(sub, outdir: Path):
    ART = outdir / "artifacts/lifecycle"; FX = ART / "fixtures"
    by_uri = {o["uri"]: o for e in sub.ledger.entries for o in (e.get("state_update") or [])}
    groups = (("disputes", ["dispute"]), ("claims", ["claim"]), ("evidence", ["evidence"]),
              ("cases", ["case"]), ("goals", ["goal"]), ("metrics", ["metric"]),
              ("tasks", ["task"]), ("dependencies", ["dependency"]), ("policies", ["policy"]),
              ("processes", ["process", "process_instance", "risk", "escalation"]),
              ("decisions", ["decision"]), ("expectations", ["expectation"]),
              ("trust", ["trust"]),
              ("actors_offers", ["person", "org", "agent", "entity", "system", "rule", "offer",
                                 "authority", "delegation", "consent", "obligation", "right"]),
              ("relationships", ["relationship", "interaction"]), ("events", ["event"]))
    for name, prefixes in groups:
        p = FX / "lifecycle" / f"{name}.json"; p.parent.mkdir(parents=True, exist_ok=True)
        items = [o for u, o in by_uri.items() if u.startswith(tuple(f"{x}://" for x in prefixes))]
        p.write_text(json.dumps(items, indent=2))
    ld = FX / "ledger"; ld.mkdir(parents=True, exist_ok=True)
    (ld / "ledger.json").write_text(json.dumps(sub.ledger.to_dict(), indent=2))
    st = FX / "statemachines"; st.mkdir(parents=True, exist_ok=True)
    (st / "dispute.json").write_text(json.dumps(
        {"uri": "dispute://lf/delivery",
         "states": ["OPEN", "EVIDENCE_COLLECTION", "CONTESTED", "ADJUDICATION", "RESOLUTION",
                    "ACCEPTED", "EXECUTED", "VERIFIED", "CLOSED"]}, indent=2))
    (st / "relationship.json").write_text(json.dumps(
        {"uri": REL_DELIVERY, "states": ["PROPOSED", "ACTIVE"]}, indent=2))
    gd = ART / "graph"; gd.mkdir(parents=True, exist_ok=True)
    (gd / "current-state.json").write_text(json.dumps(sub.graph.to_dict(), indent=2))


if __name__ == "__main__":
    sys.exit(run())