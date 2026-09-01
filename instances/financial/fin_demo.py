"""Northglen Bank — a RelationalOS instance for the financial sector (dogfood trial).

Builds a full S1->S5 chain + the Business Operating Layer for a fictional commercial
bank, then produces its cockpit + the §7L ten answers for THAT company, emits its own
fixtures, and passes the Sprint-0 conformance validator (C1-C5) over those fixtures.

Domain mapped onto the reference build's operating layer:
  Company (owner)  : org://fin/northglen  — regional commercial bank (FOR_PROFIT)
  Client           : org://fin/zephyr     — small manufacturer taking a working-capital facility
  Counterparties   : org://fin/adamvale (reliable, settles on time)
                      org://fin/kaplen   (laggard, missed its committed settlement deadline)
  Human approver   : person://fin/treasurer
  Outcome class    : "committed funding tranche settled by its committed deadline"

Every object is carried by a signed Ledger event's state_update (full coverage, §3.16),
so the whole Graph rebuilds from the whole Ledger. URI cap / frozen ontology honoured:
only the existing case:// goal:// metric:// task:// dependency:// nouns are used; derived
values (Exception/Priority/Recommendation/capacity) are additive envelope fields; Learning
is a decision:// + a policy:// change. The reference S4/S5 services emit 'qk' in some URI
labels (a build artifact, harmless: conformance governs by scheme) — disclosed in README.

This module reuses the UNMODIFIED canonical ros package (now at the repo ROOT, promoted by the
reorg from its origin sprints/sprint-5/artifacts/ros) via sys.path.
"""
from __future__ import annotations
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
ROS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROS))

from ros.substrate import Substrate, now_iso            # noqa: E402
from ros.bol import BolService, project_on_time, project_settled_value, project_trust  # noqa: E402
from ros.s2 import S2Service                             # noqa: E402
from ros.s4 import S4Service                             # noqa: E402
from ros.s5 import S5Service, config_defaults            # noqa: E402
from ros.s1 import S1Service, Permission, Denial         # noqa: E402

ART = HERE / "artifacts"
FIXTURES = ART / "fixtures"
LEDGER_DIR = FIXTURES / "ledger"
SM_DIR = FIXTURES / "statemachines"
GRAPH_DIR = ART / "graph"
REPORTS = ART / "reports"

# ---- actors / identifiers (fictional) --------------------------------------
BANK = "org://fin/northglen"
CLIENT = "org://fin/zephyr"
ADAMVALE = "org://fin/adamvale"
KAPLEN = "org://fin/kaplen"
TREASURER = "person://fin/treasurer"
OPS = "agent://fin/treasury-ops"
LOAN_REL = "relationship://fin/loan-ops"
FUND_REL = "relationship://fin/funding-net"
CLAIM = "timely committed settlement"
OPS_AUTH = "authority://fin/for-treasury"
ON_TM = "metric://fin/m-on-time-settlement"
GOAL = "goal://fin/g-stable-client-funding"
CASE = "case://fin/c-on-time-funding"
TASK_R = "task://fin/t-treasury-rebalance"
TASK_F = "task://fin/t-followup-routed"
POLICY = "policy://fin/funding-allocation"
LEARN = "decision://fin/s5-learning-funding"
CTX = FUND_REL

# ---- company-branding component (Sprint 7, self-contained in the v1) -------
# Additive `brand` field on the company org://fin/northglen actor (field, not a
# noun: URI cap / frozen ontology held). Rendered into the cockpit + branding.md.
BRAND = {
    "tagline": "Funding that lands on the date.",
    "mission": "Commit and settle funding tranches reliably and on time so corporate clients can "
               "run their working-capital plans to a schedule they can trust.",
    "vision": "A commercial lending market where a committed tranche settling on time is a durable "
              "promise, backed by ledger-verified evidence.",
    "values": [
        ("Commitment is covenant", "A committed funding tranche is a promise to a date."),
        ("Evidence-first", "We verify every settlement against the ledger; on time is a fact, not a target."),
        ("Client partnership", "Corporate clients plan working capital around our settlements."),
        ("Prudence", "On time never trades away sound credit judgement."),
        ("Transparency", "If a settlement will slip, clients hear it from us first."),
    ],
    "about": "Northglen Bank is a regional commercial bank. We commit and settle funding tranches "
             "for corporate clients, and we run that commitment to the ledger-verified on-time "
             "standard of the platform. For a treasurer planning working capital around a committed "
             "settlement date, our on-time record is the reliable foundation of the relationship.",
    "fast_facts": [
        "Founded 1987, regional commercial banking",
        "Corporate lending across the region",
        "Ledger-verified settlement operation",
    ],
    "history": [
        ("1987", "Chartered as a regional commercial bank."),
        ("2005", "Expanded into syndicated committed funding."),
        ("2023", "Placed every committed settlement under ledger-verified on-time evidence."),
    ],
    "leadership": [
        ("Ruth Calloway", "Chief Executive", "Two decades in commercial lending; built Northglen on settlement integrity."),
        ("Victor Hughes", "Chief Treasury Officer", "Owns the funding and correspondent network."),
    ],
    "products_services": [
        "Committed working-capital funding tranches",
        "Syndicated committed funding",
        "Treasury and settlement operations",
    ],
    "testimonials": [
        ("Northglen's committed settlements are the ones our treasury calendar is built around.", "Corporate treasurer"),
    ],
    "trust": [
        ("98.6% committed settlement on-time rate (2025)", "Northglen settlement ledger"),
        ("Chartered bank; prudential oversight", "state regulator"),
    ],
    "locations": "Regional HQ + branches across the state",
    "faq": [
        ("How do you prove a settlement was on time?", "Every committed tranche settles to a signed "
         "ledger event with a verified timestamp — auditable, not asserted."),
        ("Do you commit syndicated funding?", "Yes, both bilateral and syndicated committed tranches "
         "run under the same evidence standard."),
    ],
    "contact": "treasury@northglen.example · +1-505-555-0199",
    "careers": "Back corporate plans with reliable funding: treasury, credit, settlement operations.",
    "investors": "Public charter with regulated reporting; settlement reliability shared with regulators.",
    "press": "media@northglen.example — lending, treasury, and community programs.",
    "esg": "Responsible lending, financial-inclusion programs, branch-efficiency investments.",
    "legal": ["Privacy", "Terms", "Financial Privacy Notice", "State Rights"],
    "nav": ["About", "Lending", "Treasury", "Careers", "Investors", "Press", "Community", "Contact"],
    "cookie_consent": "Accept All · Reject All · Preferences (link to Privacy)",
    "design": {
        "palette": [("Ledger Navy", "#14314E"), ("Settlement Blue", "#1B6CA8"), ("Vault Grey", "#8A929B"), ("Trust White", "#FAFBFC")],
        "typography": {"heading": "Trusted serif (e.g. Source Serif 4)", "body": "Open sans (e.g. Inter)"},
        "logo": {"wordmark": "NORTHGLEN", "character": "a chevron/vault-mark", "usage": "clear space generous; navy+white primary, blue accent"},
        "imagery": "Calm and solid: banking halls, treasury operations, measured growth — trustworthy",
        "tone": "Steady, precise, reassuring; speaks in commitments and verified settlements.",
    },
}


# ---- deterministic S5 update config (same as reference build) --------------
cfg = config_defaults()
EXPECTED = 0.95                      # on-time settlement target (a stated threshold)


def _trust_map(sub) -> dict:
    return {o["target"]: float(o.get("score", 0.0))
            for o in sub.graph.objects.values()
            if o.get("uri", "").startswith("trust://")}


def _offs(sub) -> list[dict]:
    return [o for o in sub.graph.objects.values() if o.get("uri", "").startswith("offer://")]


def _expect(slug: str, buyer: str, subject: str, price: float, due: str) -> dict:
    return {"uri": f"expectation://fin/e-{slug}", "actor": TREASURER, "subject": subject,
            "condition": "fully settle the committed funding tranche by its committed deadline",
            "metric": "settled_value", "threshold": price, "deadline": due,
            "evidence_required": "CLEAR"}


def _fx(slug: str, provider: str, price: float, due: str, settled_at: str) -> dict:
    return {"slug": slug, "buyer": BANK, "provider": provider, "price": price,
            "currency": "USD", "value": price, "cost": price,
            "due": due, "settled_at": settled_at, "of": f"commitment://fin/c-{slug}"}


# ===========================================================================
def provision(sub: Substrate, bol: BolService) -> None:
    """Seed the financial-instance base: actors, relationship(s), authority,
    ops worker (delegated), matching delegation, expectations, policy v1, process."""
    bol.prov(2, "agent://fin/s5",
             "provision financial base (actors, relationships, authority + ops worker + policy + expectation)",
             [
                 # --- actors ---
                 {"uri": BANK, "type": "ORG", "identity": {"attestations": ["chartered-bank-license"]},
                  "brand": BRAND},
                 {"uri": CLIENT, "type": "ORG"},
                 {"uri": ADAMVALE, "type": "ORG"},
                 {"uri": KAPLEN, "type": "ORG"},
                 {"uri": TREASURER, "type": "PERSON"},
                 {"uri": OPS, "type": "AGENT"},
                 # --- relationships (role is an attribute, §C2) ---
                 {"uri": LOAN_REL, "participants": [BANK, CLIENT], "status": "ACTIVE",
                  "roles": {BANK: ["bank"], CLIENT: ["borrower"]},
                  "authority": [OPS_AUTH], "purpose": "commercial working-capital lending"},
                 {"uri": FUND_REL, "participants": [BANK, ADAMVALE, KAPLEN], "status": "ACTIVE",
                  "roles": {BANK: ["treasury"], ADAMVALE: ["correspondent"], KAPLEN: ["correspondent"]},
                  "authority": [OPS_AUTH], "purpose": "syndicated committed funding"},
                 # --- authority / capability (capability-based §7B) ---
                 {"uri": OPS_AUTH, "holder": BANK,
                  "grants": ["triage_case", "assign_case", "close_case", "approve_learning",
                             "rebalance_funding_allocation", "gate_funder_performance",
                             "release_funding_tranche"],
                  "roles": ["treasury"]},
                 # --- rules + delegations (scope = rule:// refs, §3.4/§7B) ---
                 {"uri": "rule://fin/treasury-ops-run", "kind": "POLICY",
                  "text": "treasury ops worker may re-balance funding allocation and gate funder performance",
                  "grants": ["rebalance_funding_allocation", "gate_funder_performance"]},
                 {"uri": "rule://fin/match-run", "kind": "POLICY",
                  "text": "S2 may run Trust-weighted funding matching for the client",
                  "grants": ["run_funding_match"]},
                 {"uri": "delegation://fin/treasury-ops", "grantor": BANK, "grantee": OPS,
                  "scope": ["rule://fin/treasury-ops-run"], "status": "ACTIVE"},
                 {"uri": "delegation://fin/s2-match", "grantor": BANK, "grantee": "agent://s2",
                  "scope": ["rule://fin/match-run"], "status": "ACTIVE"},
                 # --- expectation (§3.11) + policy v1 (§7K.1 Policy execution) ---
                 {"uri": "expectation://fin/e-on-time-funding", "actor": TREASURER,
                  "subject": "committed funding settlement",
                  "condition": "settle each committed funding tranche by its committed deadline",
                  "metric": "on_time", "threshold": EXPECTED,
                  "deadline": "2026-12-31T00:00:00Z", "evidence_required": "CLEAR"},
                 {"uri": POLICY, "name": "funding allocation",
                  "condition": "a new committed funding tranche is to be allocated",
                  "decision": "select the counterparty with the highest fit x scoped settlement Trust",
                  "action": "allocate to the top-ranked fitted counterparty",
                  "scope": ["expectation://fin/e-on-time-funding"], "version": 1},
                 {"uri": "process://fin/pr-funding",
                  "definition": "exception -> open case -> assign -> execute -> verify -> learn -> close",
                  "steps": ["triage", "assign", "execute", "verify_outcome", "learning"]},
                 {"uri": "process_instance://fin/pi-funding",
                  "process": "process://fin/pr-funding", "status": "RUNNING",
                  "started_at": now_iso()},
             ])


# ===========================================================================
def build_chain(sub: Substrate, bol: BolService) -> None:
    """Seed a small S1->S5 history for finance: a Trust-weighted match, then two
    committed funding settlements (one late, one on time) that set up the exception."""
    s1 = S1Service(sub); s2 = S2Service(sub)
    s4 = S4Service(sub); s5 = S5Service(sub)
    i = 100

    # --- initial scoped Trust (seeds for a new (subj,tgt,claim,ctx) key, §3.14) ---
    for tgt, score in ((ADAMVALE, 0.60), (KAPLEN, 0.90)):
        t = {"uri": f"trust://fin/t-{tgt.split('/')[-1]}", "subject": BANK, "target": tgt,
             "claim": CLAIM, "context": CTX, "score": score}
        bol.prov(i, "agent://fin/s5", f"seed scoped Trust {tgt} = {score}", [t]); i += 1

    # --- S2 Trust-weighted match for the client's funding need (zephyr) ---
    # funding offers (equal fit) so the rank is decided by scoped Trust (the flywheel)
    for pfx, prov in (("adamvale", ADAMVALE), ("kaplen", KAPLEN)):
        bol.prov(i, "agent://fin/s2",
                 f"register committed-funding offer from {prov}",
                 [{"uri": f"offer://fin/o-{pfx}", "provider": prov,
                   "price": 1500000, "currency": "USD",
                   "capability_keys": ["syndication", "funding"],
                   "fit_note": "correspondent syndicated funding line"}])
        i += 1
    intent = {"subject": CLIENT, "need": "committed working-capital funding",
              "capability_keys": ["syndication", "funding"], "urgency": "normal"}
    trusts0 = [{"target": k, "score": v} for k, v in _trust_map(sub).items()]
    m0 = s2.match_offers(intent, _offs(sub), trusts0, trust_floor=0.4)
    bol.prov(i, "agent://fin/s2",
             f"initial funding match ranked {m0[0].offer_uri} (score {m0[0].score:.3f}) "
             f"— base ranking before outcomes",
             [{"uri": "decision://fin/s2-match-baseline", "by": "agent://s2",
               "authority": "delegation://fin/s2-match",
               "alternatives": [m.offer_uri for m in m0] + ["no facility"],
               "confidence": 0.9, "expected_outcome": "kaplen ranked #1 on existing Trust",
               "actual_outcome": m0[0].offer_uri,
               "detail": [m.to_dict() for m in m0], "made_at": now_iso()}])
    i += 1

    # --- prior-period committed settlements (S4 + S5) -> seed the on-time exception ---
    # f1: kaplen LATE (missed committed deadline) ; f2: adamvale ON TIME ; f3: kaplen LATE
    fx1 = _fx("kaplen-q3", KAPLEN, 1500000, "2026-08-31T00:00:00Z", "2026-09-02T00:00:00Z")
    fx2 = _fx("adamvale-q3", ADAMVALE, 1500000, "2026-08-31T00:00:00Z", "2026-08-30T00:00:00Z")
    fx3 = _fx("kaplen-q4", KAPLEN, 1200000, "2026-09-15T00:00:00Z", "2026-09-17T00:00:00Z")
    exp1, exp2 = _expect("kaplen-q3", BANK, "syndicated committed funding", 1500000, fx1["due"]), \
                 _expect("adamvale-q3", BANK, "syndicated committed funding", 1500000, fx2["due"])
    exp3 = _expect("kaplen-q4", BANK, "syndicated committed funding", 1200000, fx3["due"])
    bol.prov(i, "agent://fin/s5", "register funding expectations", [exp1, exp2, exp3]); i += 1

    prior = [(fx1, exp1), (fx2, exp2), (fx3, exp3)]
    for fx, exp in prior:
        ch = s4.settle(fx, i=i); i += 1                 # signed EXCHANGE + assets/obligation/receipt/recon
        co = s4.evaluate(fx, exp, i=i); i += 1          # signed OUTCOME (met/partial/failed)
        job = f"funding-{fx['slug']}"
        out = {"uri": f"event://fin/outcome-{job}", "job": job, "provider": fx["provider"],
               "committed_deadline": fx["due"], "actual_completed_at": fx["settled_at"],
               "note": f"committed funding settlement for {fx['slug']}"}
        ev, on_time = s5.capture(out, s5_provenance(), signer="org://fin/s5", i=i); i += 1
        vr = s5.verify(ev, f"{fx['provider']} settled the committed funding tranche "
                       f"{'on time' if on_time else 'LATE'}", out, i=i); i += 1
        s5.update_trust(subject=BANK, target=fx["provider"], claim=CLAIM, context=CTX,
                        verify=vr, evidence_score=vr.degree, i=i, alpha=cfg["alpha"],
                        expectation=cfg["expectation"], recency=cfg["recency"])
        i += 1


def s5_provenance() -> dict:
    return {"source": "signed committed-funding settlement record + treasury anchor",
            "procedure": "settlement-anchor-conformance", "confidence": 0.95}


# ===========================================================================
def build_case(sub: Substrate, bol: BolService) -> dict:
    """5.1 Case-led loop + exception heartbeat + §6 human floor + Learning."""
    s1 = S1Service(sub); s2 = S2Service(sub)
    s4 = S4Service(sub); s5 = S5Service(sub)
    i = 7000

    on, total = project_on_time(sub)
    actual = on / total if total else 1.0

    case = bol.open_case(CASE, "committed funding settlement below target on time", TREASURER,
                         [BANK, TREASURER, OPS], [LOAN_REL], i, "agent://fin/s5",
                         suggestion="ledger-projected funding on-time rate below target")
    i += 1
    case = bol.exception_heartbeat(
        case, EXPECTED, round(actual, 3), "CRITICAL",
        f"Committed funding on-time {actual:.2f} below target {EXPECTED:.2f} "
        f"(ledger: {on}/{total} committed settlements on time)",
        "funding-ops failure — org://fin/kaplen missed its committed settlement deadline "
        "by 2 days; scoped settlement Trust fell 0.90->0.508",
        "SUPPORTED",                                    # §7K.2 epistemic status
        "Re-allocate committed funding to the verified on-time counterparty "
        "(org://fin/adamvale) and gate the laggard (org://fin/kaplen) with a performance "
        "checkpoint before any new commitment",
        ON_TM,
    )
    bol.prov(i, "agent://fin/s5", "record exception heartbeat on the case", [case]); i += 1

    # --- TRIAGE ---
    bol.prov(i, "agent://fin/s5", "case triage: exception assessed, root nominated",
             [{"uri": "decision://fin/s5-triage", "by": "agent://fin/s5", "authority": OPS_AUTH,
               "alternatives": ["accept", "dismiss as anomaly"], "confidence": 0.85,
               "expected_outcome": "accept as a real funding-risk",
               "actual_outcome": "accepted; root (kaplen settlement failure) nominated",
               "made_at": now_iso()}])
    case = bol.transition_case(case, "TRIAGE", i, "agent://fin/s5",
                               "case triaged: the funding on-time variance is significant",
                               "event://fin/s5-case-triage"); i += 1

    # --- ASSIGNED + #8 becomes assigned, authorized work ---
    pri = bol.priority(impact=0.85, urgency=0.90, confidence=0.70, irreversible=False,
                       relationship_importance=0.80, cost_of_delay=0.75)
    task = {
        "uri": TASK_R, "assigned_to": OPS, "created_by": "agent://fin/s5",
        "objective": "re-balance funding allocation to the verified on-time counterparty "
                     "(adamvale) and gate the laggard (kaplen)",
        "dependencies": [], "authority": OPS_AUTH,
        "deadline": "2026-10-15T00:00:00Z", "priority": pri["score"], "status": "ASSIGNED",
        "expected_outcome": "next committed funding tranche routed to a verified on-time "
                            "counterparty; policy updated",
        "why_here": "derived from the funding on-time exception (case OPEN)",
        "importance": "restores committed funding on-time, protecting the client's scoped Trust",
        "evidence": [f"evidence://qk/funding-kaplen-q3", f"evidence://qk/funding-adamvale-q3"],
        "decision_required": "approve the funding re-allocation",
        "priority_factors": pri["factors"], "assigned_capacity": 1.0,
    }
    bol.prov(i, "agent://fin/s5",
             "case assigned; task t-treasury-rebalance becomes assigned authorized work (#8)",
             [task, {"uri": "decision://fin/s5-assign", "by": TREASURER, "authority": OPS_AUTH,
                     "alternatives": ["assign", "defer"], "confidence": 0.95,
                     "expected_outcome": "task in progress",
                     "detail": {"task": TASK_R, "assigned_to": OPS, "authority": OPS_AUTH,
                                "priority": pri["score"], "capacity": task["assigned_capacity"]},
                     "made_at": now_iso()}])
    case = bol.transition_case(case, "ASSIGNED", i, "agent://fin/s5",
                               "case assigned; owner treasurer + treasury-ops worker",
                               "event://fin/s5-case-assigned"); i += 1

    # --- IN_PROGRESS: worker re-balances (policy v2 + re-ranked match) ---
    case = bol.transition_case(case, "IN_PROGRESS", i, "agent://fin/s5",
                               "task execution began; counterparty mix being re-balanced",
                               "event://fin/s5-case-inprogress"); i += 1
    # §7B capability check: the ops worker's delegation grants the action; an outside
    # action / revoked delegation would be denied (asserted in run_fin checks).
    bol.prov(i, "agent://fin/s5",
             "policy updated: allocate by fit AND scoped settlement Trust",
             [{"uri": POLICY, "name": "funding allocation",
               "condition": "a new committed funding tranche is to be allocated",
               "decision": "select by fit x scoped settlement Trust; laggard (< floor) needs a "
                           "performance gate before a new commitment",
               "action": "allocate to the top-ranked fitted counterparty; gate laggard (kaplen)",
               "scope": ["expectation://fin/e-on-time-funding"], "version": 2,
               "policy_status": "REVISED"}])
    i += 1
    # effect: the next S2 match re-ranks under the updated Trust (flywheel)
    fidx = _offs(sub)
    matches = s2.match_offers(intent_for(sub), fidx,
                              [{"target": k, "score": v} for k, v in _trust_map(sub).items()],
                              trust_floor=0.4)
    bol.prov(i, "agent://fin/s2",
             f"task effect: next funding tranche ranked {matches[0].offer_uri} "
             f"(score {matches[0].score:.3f}) — re-allocation to the on-time counterparty",
             [{"uri": "decision://fin/s5-match-recorded", "by": "agent://s2",
               "authority": "delegation://fin/s2-match",
               "alternatives": [m.offer_uri for m in matches] + ["no facility"],
               "confidence": 0.92, "expected_outcome": "adamvale ranked #1",
               "actual_outcome": matches[0].offer_uri,
               "detail": [m.to_dict() for m in matches], "made_at": now_iso()}])
    i += 1

    # --- §6 human floor: releasing the re-allocated tranche is IRREVERSIBLE ---
    bol.prov(i, "agent://fin/s5",
             "escalation raised: releasing the re-allocated committed tranche is irreversible "
             "and cost-unknowable once released (§6 floor)",
             [{"uri": "escalation://fin/escalate-tranche-release", "trigger":
               "committed external funding disbursement — irreversible and cost-unknowable "
               "once released",
               "severity": "WARN", "recipient": TREASURER,
               "deadline": "2026-11-15T00:00:00Z", "fallback": "agent://fin/s5",
               "authority": OPS_AUTH, "acknowledgement": "approve then execute"}],
             uri="event://fin/s5-escalate")
    i += 1
    # the human's signed DECISION enumerates alternatives BEFORE the action may run
    sub.record(
        {"uri": "event://fin/treasurer-human", "type": "DECISION",
         "event_id": f"ev-fin-{i}", "correlation_id": "corr-fin-bol-1",
         "causation_id": f"ev-fin-{max(0, i-1)}", "idempotency_key": f"idem-fin-{i}",
         "signature": f"signed-by-{TREASURER}", "occurred_at": now_iso(),
         "actor": TREASURER,
         "detail": "treasurer signed approval to release the re-allocated tranche (§6 floor)",
         "state_update": [{"uri": "decision://fin/treasurer-human", "by": TREASURER,
                          "authority": OPS_AUTH,
                          "alternatives": ["release_in_full", "hold_pending_portfolio_review",
                                           "release_partial_and_hold_if_shortfall", "open_dispute"],
                          "confidence": 1.0,
                          "expected_outcome": "release the committed tranche to adamvale",
                          "actual_outcome": "release_in_full (human approved)",
                          "detail": {"task": TASK_R, "action": "release_funding_tranche",
                                     "irreversible_failure": True,
                                     "cost_failure_unknowable": True},
                          "made_at": now_iso()}]},
        TREASURER)
    i += 1
    # the ACTION executes but ONLY now, after the signed human decision
    sub.record(
        {"uri": "event://fin/action-tranche-release", "type": "ACTION",
         "event_id": f"ev-fin-{i}", "correlation_id": "corr-fin-bol-1",
         "causation_id": f"ev-fin-{max(0, i-1)}", "idempotency_key": f"idem-fin-{i}",
         "signature": f"signed-by-{TREASURER}", "occurred_at": now_iso(),
         "actor": OPS, "detail": "rebalance_funding_allocation executed after human approval",
         "worker": OPS, "action": "rebalance_funding_allocation", "task_id": "t-treasury-rebalance",
         "tier": "human", "outcome": "done",
         "state_update": []},
        TREASURER)
    i += 1
    # --- BLOCKED: awaiting the rallied tranche's verified settlement ---
    case = bol.transition_case(case, "BLOCKED", i, "agent://fin/s5",
                               "case blocked pending verified settlement of the rallied "
                               "committed funding tranche",
                               "event://fin/s5-case-blocked")
    i += 1

    # --- the rallied follow-on tranche: allocate to adamvale, settle on time, verify (#10) ---
    bol.prov(i, "agent://fin/s5", "rallied follow-on tranche allocated to adamvale (the fix)",
             [{"uri": "commitment://fin/c-adamvale-followup", "by": "agent://fin/s5",
               "to": ADAMVALE, "obligation": "offer://fin/o-adamvale",
               "expectation": "expectation://fin/e-routed-adamvale",
               "status": "AGREED", "terms": {"kind": "committed funding follow-up", "signed": True},
               "agreed_at": now_iso()}])
    i += 1
    fx = _fx("routed-adamvale", ADAMVALE, 1500000, "2026-11-15T00:00:00Z", "2026-11-12T00:00:00Z")
    fexp = _expect("routed-adamvale", BANK, "committed funding follow-up", 1500000, fx["due"])
    bol.prov(i, "agent://fin/s5", "register follow-on expectation", [fexp]); i += 1
    chol = s4.settle(fx, i=i); i += 1
    fout = s4.evaluate(fx, fexp, i=i); i += 1
    out = {"uri": "event://fin/outcome-funding-routed-adamvale", "job": "funding-routed-adamvale",
           "provider": ADAMVALE, "committed_deadline": fx["due"],
           "actual_completed_at": fx["settled_at"],
           "note": f"rallied committed funding settled per {fout['uri']} ({fout['evaluation']})"}
    fev, f_on = s5.capture(out, s5_provenance(), signer="org://fin/s5", i=i); i += 1
    fvr = s5.verify(fev, "adamvale settled the rallied committed funding tranche on time",
                    out, i=i); i += 1
    ftrust = s5.update_trust(subject=BANK, target=ADAMVALE, claim=CLAIM, context=CTX,
                             verify=fvr, evidence_score=fvr.degree, i=i, alpha=cfg["alpha"],
                             expectation=cfg["expectation"], recency=cfg["recency"])
    i += 1

    # --- RESOLVED: verified outcome ---
    on2, tot2 = project_on_time(sub)
    forward_rate = 1.0            # the rallied (post-change) period
    case = bol.transition_case(
        case, "RESOLVED", i, "agent://fin/s5",
        f"exception resolved: rallied committed funding verified on time; forward-period "
        f"on-time = 1.0; cumulative {on2}/{tot2}",
        "event://fin/s5-case-resolved",
        verified_outcome=f"forward-period committed-funding on-time restored to 1.0; "
                         f"org://fin/adamvale settled the rallied tranche on time "
                         f"({fev['uri']}); adamvale settlement Trust {ftrust['score']}")
    i += 1

    # --- Learning (§7K.1) + future-policy change, then CLOSE ---
    learning = bol.learning_entry(
        LEARN, "committed funding on-time management", "agent://fin/s5",
        i, "agent://fin/s5",
        expected=EXPECTED, actual=forward_rate,
        why="Concentrating committed funding with a counterparty that has verified "
            "on-time settlement (adamvale), while gating the laggard (kaplen) with a "
            "performance checkpoint, restored committed-funding on-time. Verified good "
            "settlements compound scoped settlement Trust and re-price routing.",
        change_future_policy="ALLOCATE by fit AND scoped settlement Trust (not fit alone); "
                             "counterparties below the Trust floor require a performance gate "
                             "before a new commitment.")
    i += 1
    bol.prov(i, "agent://fin/s5", "close case; learning recorded; future policy updated",
             [{"uri": POLICY, "name": "funding allocation",
               "condition": "a new committed funding tranche is to be allocated",
               "decision": "select by fit x scoped settlement Trust; laggard needs a "
                           "performance gate BEFORE a new commitment (learned 2026-09-01)",
               "action": "allocate to the top-ranked fitted counterparty; gate laggard "
                         "(kaplen); notify treasurer on divergence",
               "scope": ["expectation://fin/e-on-time-funding"], "version": 3,
               "policy_status": "EFFECTIVE", "learning": LEARN}])
    case = bol.transition_case(case, "CLOSED", i, "agent://fin/s5",
                               "case closed with a verified, learned outcome",
                               "event://fin/s5-case-closed"); i += 1

    return {"case": CASE, "final_status": case["status"],
            "exception": {"expected": EXPECTED, "actual": round(actual, 3),
                          "variance": round(actual - EXPECTED, 3),
                          "significance": "CRITICAL", "on": on, "total": total},
            "task": TASK_R, "assigned_to": OPS, "authority": OPS_AUTH, "priority": pri,
            "policy_final_version": 3,
            "follow_on": {"exchange": chol["uri"], "outcome": fout["uri"],
                          "evaluation": fout["evaluation"], "evidence": fev["uri"],
                          "after_trust": ftrust["score"], "forward_on_time": forward_rate,
                          "cumulative_after": round(on2 / tot2, 3)},
            "learning": learning["uri"]}


def intent_for(sub) -> dict:
    return {"subject": CLIENT, "need": "committed working-capital funding",
            "capability_keys": ["syndication", "funding"], "urgency": "normal"}


# ===========================================================================
def build_metrics(sub: Substrate, bol: BolService) -> dict:
    """5.2 Goals / Metrics / Priority / Dependency + impact analysis."""
    i = 8000
    cpu = project_trust(sub, ADAMVALE, CTX) or 0.0
    settled = project_settled_value(sub)
    on, total = project_on_time(sub)
    on_rate = on / total if total else 1.0

    goal = {"uri": GOAL, "for": BANK,
            "statement": "Consistently settle committed funding tranches on time so the "
                         "client trusts Northglen enough to deepen the relationship.",
            "horizon": "quarter", "owner": TREASURER,
            "metrics": [ON_TM, "metric://fin/m-funder-trust", "metric://fin/m-settled-value"]}
    m_on = {"uri": ON_TM, "name": "Funding on-time settlement rate",
            "definition": "share of committed funding tranches verified settled on time",
            "unit": "fraction", "formula": "on_time / (on_time + late) from ledger",
            "dimensions": ["counterparty"], "target": EXPECTED, "threshold": 0.8,
            "period": "quarter", "source": "ledger committed-settlement records",
            "owner": TREASURER, "actual": round(on_rate, 3), "forecast": 0.5,
            "variance": round(on_rate - EXPECTED, 3),
            "root_cause": "funding-ops failure (kaplen missed committed deadline)",
            "root_cause_status": "SUPPORTED"}
    m_trust = {"uri": "metric://fin/m-funder-trust", "name": "Counterparty settlement-trust score",
               "definition": "best scoped settlement Trust on the funding relationship",
               "unit": "score", "formula": "T(subject->target, claim, context) per §5",
               "dimensions": ["counterparty"], "target": 0.9, "threshold": 0.6,
               "period": "rolling", "source": "S5 scoped Trust graph",
               "owner": TREASURER, "actual": round(cpu, 3), "forecast": 0.92,
               "variance": round(cpu - 0.9, 3), "root_cause_status": "UNKNOWN"}
    m_val = {"uri": "metric://fin/m-settled-value", "name": "Settled committed value",
             "definition": "value of EXCHANGE events settled this period",
             "unit": "USD", "formula": "sum(EXCHANGE.price) from ledger",
             "dimensions": ["counterparty"], "target": 6000000.0, "threshold": 3500000.0,
             "period": "quarter", "source": "ledger EXCHANGE events",
             "owner": TREASURER, "actual": settled, "forecast": 7000000.0,
             "variance": round(settled - 6000000.0, 2), "root_cause_status": "UNKNOWN"}
    bol.prov(i, "agent://fin/s5", "register goal + ledger-projected metrics (health source)",
             [goal, m_on, m_trust, m_val]); i += 1

    bol.metric_loop(goal, m_on, "decision://fin/s5-metric-loop-on-time", TASK_R,
                    "event://fin/outcome-funding-routed-adamvale", i, "agent://fin/s5"); i += 1

    # --- priority-ordered attention (derive, don't overload) ---
    att = [
        {"uri": TASK_R, "label": "re-balance funding allocation",
         "priority": bol.priority(0.85, 0.90, 0.70, False, 0.80, 0.75)["score"]},
        {"uri": TASK_F, "label": "rallied follow-on committed funding (adamvale)",
         "priority": bol.priority(0.70, 0.75, 0.60, False, 0.70, 0.60)["score"]},
    ]
    att.sort(key=lambda x: x["priority"], reverse=True)
    bol.prov(i, "agent://fin/s5", "priority-ordered attention list (§7J.5)",
             [{"uri": "decision://fin/s5-attention-ordered", "by": "agent://fin/s5",
               "authority": OPS_AUTH, "confidence": 0.9,
               "expected_outcome": "top-of-attention items ranked",
               "actual_outcome": "attention prioritized by derived score",
               "detail": {"attention": att}, "made_at": now_iso()}]); i += 1

    # --- dependencies (§7J.6) + impact analysis ---
    for uri, fr, to, kind in (
            ("dependency://fin/d-rebalance-enables-followup", TASK_R, TASK_F, "ENABLES"),
            ("dependency://fin/d-followup-requires-allocation", TASK_F, POLICY, "REQUIRES"),
            ("dependency://fin/d-followup-blocks-case", TASK_F, CASE, "BLOCKS"),
            ("dependency://fin/d-case-derived-from-metric", CASE, ON_TM, "DERIVED_FROM"),
            ("dependency://fin/d-metric-impacts-goal", ON_TM, GOAL, "IMPACTS"),
            ("dependency://fin/d-rebalance-blocks-case", TASK_R, CASE, "BLOCKS")):
        bol.make_dependency(uri, fr, to, kind, i, "agent://fin/s5"); i += 1
    impact_r = bol.impact_analysis(TASK_R)
    impact_f = bol.impact_analysis(TASK_F)

    # --- business-health panel (from ledger projections) ---
    health = []
    for m in (m_on, m_trust, m_val):
        var = m.get("variance", 0.0); tgt = m.get("target") or 1.0
        rel = var / abs(tgt)
        status = "OK" if rel >= 0 else ("WARN" if rel >= -0.05 else "CRITICAL")
        health.append({"metric": m["uri"], "name": m["name"], "unit": m["unit"],
                       "target": m.get("target"), "actual": m.get("actual"),
                       "variance": var, "status": status, "forecast": m.get("forecast")})
    return {"goal": goal["uri"], "metrics": [m["uri"] for m in (m_on, m_trust, m_val)],
            "attention": att, "health": health, "impact": impact_f,
            "impact_from_task_rebalance": impact_r, "dependencies": 6}


# ===========================================================================
def build_cockpit(sub: Substrate, s51: dict, s52: dict) -> dict:
    on, total = project_on_time(sub)
    cpu = project_trust(sub, ADAMVALE, CTX)
    settled = project_settled_value(sub)
    return {
        "company": "Northglen Bank (fictional, financial sector)", "generated": now_iso(),
        "health": s52["health"],
        "attention_line": f"{len(s52['attention'])} things requiring attention today",
        "attention": s52["attention"],
        "exception": s51["exception"], "case": s51["case"], "case_status": s51["final_status"],
        "recommendation": {
            "summary": s51["task"], "authority_required": OPS_AUTH,
            "options": ["re-balance committed funding to verified on-time counterparty",
                        "gate the laggard (kaplen)", "do nothing"],
            "includes_do_nothing": True,
            "tradeoff": "Re-balancing concentrates committed funding with adamvale (higher "
                        "short-term concentration risk) but restores funding on-time and "
                        "protects the client's scoped Trust; doing nothing keeps on-time below target.",
            "confidence": 0.85,
            "expected_impact": "forward-period committed-funding on-time returns to 1.0 "
                               "(verified, rallied adamvale settlement on time).",
            "decision": "decision://fin/s5-assign",
        },
        "verified_outcome": s51["follow_on"], "learning": s51["learning"],
        "ledger": len(sub.ledger.entries), "graph": len(sub.graph.objects),
    }


def write_cockpit_report(cockpit: dict, sub: Substrate) -> tuple[Path, Path]:
    REPORTS.mkdir(parents=True, exist_ok=True)
    L = []
    A = L.append
    headline = "# Northglen Bank — Business Operating Layer cockpit (financial-sector instance)"
    if isinstance(BRAND.get("tagline"), str):
        headline = f"# Northglen Bank — {BRAND['tagline']}"
    A(headline)
    A(f"generated {cockpit['generated']}  |  ledger events {len(sub.ledger.entries)}  graph objects {len(sub.graph.objects)}")
    A("")
    A("## Business health (ledger-projected metrics)")
    A("| metric | unit | target | actual | variance | status |")
    A("|---|---|---|---|---|---|")
    for h in cockpit["health"]:
        A(f"| {h['name']} (`{h['metric']}`) | {h['unit']} | {h['target']} | {h['actual']} | {h['variance']} | {h['status']} |")
    A("")
    A(f"## Prioritized attention — {cockpit['attention_line']}")
    for a in cockpit["attention"]:
        A(f"- **{a['priority']:.2f}** {a['label']} (`{a['uri']}`)")
    A("")
    A("## Exception (heartbeat, §7J.2)")
    ex = cockpit["exception"]
    A(f"- expected {ex['expected']}  actual {ex['actual']}  variance {ex['variance']}  "
      f"significance {ex['significance']}  ({ex['on']}/{ex['total']} ledger committed settlements on time)")
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
    A(f"- rallied adamvale committed funding settled {fo['exchange']}, outcome {fo['outcome']} "
      f"({fo['evaluation']}); evidence {fo['evidence']}; forward-period on-time {fo['forward_on_time']}; "
      f"adamvale settlement Trust -> {fo['after_trust']}")
    A(f"- Learning entry: `{cockpit['learning']}`")
    A("")
    A("## §7L — the ten morning questions, answered with evidence")
    on, total = project_on_time(sub)
    settled = project_settled_value(sub)
    rate = round(on / total, 3) if total else 1.0
    att_labels = ", ".join(a["label"] for a in cockpit["attention"])
    A(f"1. WHAT HAPPENED?  Committed funding settled on time {on}/{total} ({rate}); "
      f"adamvale settled on time (ev {fo['evidence']}), kaplen late; committed value "
      f"{settled}.  [ledger evidence]")
    A(f"2. WHAT CHANGED?  Counterparty re-allocation recommended; rallied adamvale committed "
      f"funding verified on time; cumulative forward on-time {fo['cumulative_after']}; "
      f"forward-period on-time = {fo['forward_on_time']}.  [delta -> significance]")
    A(f"3. WHAT MATTERS?  Priority-ordered attention: {att_labels}.  [§7J.5]")
    A(f"4. WHAT'S GOING WRONG?  Committed funding on-time {rate} below target {EXPECTED} (CRITICAL).  [§7J.2]")
    A("5. WHY?  Funding-ops failure — kaplen missed its committed settlement deadline (root "
      "SUPPORTED: scoped settlement Trust 0.90->0.508).  [§7K.2 epistemic status]")
    A("6. WHAT IF WE DO NOTHING?  Forecast funding on-time ~0.5 < 0.95; laggard keeps missing "
      "committed deadlines; client-scoped Trust erodes.  [§7K.1 forecast]")
    A("7. WHAT ARE OUR OPTIONS?  re-balance to adamvale; gate kaplen; do-nothing (all costed; "
      "trade-off in the recommendation).  [§7K.1 options incl. do-nothing]")
    A(f"8. WHAT SHOULD WE DO?  -> assigned, authorized Task {cockpit['recommendation']['summary']} "
      f"under {cockpit['recommendation']['authority_required']}.  [recommendation]")
    A(f"9. WHO DOES IT, AND AUTHORITY/CAPACITY?  {OPS} via delegation://fin/treasury-ops "
      f"(delegation-bounded authority, capacity 1.0), owner {TREASURER}.  [ownership + authority/capacity]")
    A(f"10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed funding verified on time "
      f"(forward on-time {fo['forward_on_time']}); Learning entry {cockpit['learning']}; "
      f"funding-allocation policy v3 updated (change-future-policy).  [verified outcome + organisational learning]")
    A("")
    A("## Brand (company identity carried on the org actor; additive field, §7J.11)")
    A(_brand_block(BRAND))
    md = REPORTS / "cockpit.md"; md.write_text("\n".join(L))
    j = REPORTS / "cockpit.json"; j.write_text(json.dumps({"cockpit": cockpit, "brand": BRAND}, indent=2))
    write_branding()
    return md, j


def _brand_block(brand: dict) -> str:
    """Render the Northglen brand as a markdown block (cockpit appendix / branding.md)."""
    out = [f"**{brand['tagline']}**"]
    for title, lines in _brand_sections(brand):
        out.append(f"**{title}**")
        out.extend(lines)
    d = brand.get("design") or {}
    if d:
        out.append("**Design language**")
        out.append("- Palette: " + ", ".join(f"{n} {h}" for n, h in d.get("palette", [])))
        if d.get("typography"):
            out.append(f"- Typography: heading {d['typography'].get('heading')} · body {d['typography'].get('body')}")
        if d.get("logo"):
            out.append(f"- Logo: {d['logo'].get('wordmark')} ({d['logo'].get('character')}); usage — {d['logo'].get('usage')}")
        if d.get("imagery"):
            out.append(f"- Imagery: {d['imagery']}")
        if d.get("tone"):
            out.append(f"- Tone of voice: {d['tone']}")
    return "\n".join(out)


def _brand_sections(brand: dict):
    out = []
    if brand.get("mission"): out.append(("Mission", [brand["mission"]]))
    if brand.get("vision"): out.append(("Vision", [brand["vision"]]))
    if brand.get("about"): out.append(("About", [brand["about"]]))
    if brand.get("values"): out.append(("Values", [f"- **{n}** — {d}" for n, d in brand["values"]]))
    if brand.get("products_services"): out.append(("Products & Services", [f"- {x}" for x in brand["products_services"]]))
    if brand.get("trust"): out.append(("Trust signals", [f"- {c} ({s})" for c, s in brand["trust"]]))
    if brand.get("testimonials"): out.append(("Customer stories", [f"- “{q}” — {s}" for q, s in brand["testimonials"]]))
    if brand.get("history"): out.append(("History", [f"- **{y}** — {e}" for y, e in brand["history"]]))
    if brand.get("leadership"): out.append(("Leadership", [f"- **{n}**, {t} — {b}" for n, t, b in brand["leadership"]]))
    if brand.get("fast_facts"): out.append(("Fast facts", [f"- {x}" for x in brand["fast_facts"]]))
    if brand.get("locations"): out.append(("Locations", [brand["locations"]]))
    if brand.get("faq"): out.append(("FAQ", [f"- **Q:** {q}\n  **A:** {a}" for q, a in brand["faq"]]))
    if brand.get("contact"): out.append(("Contact", [brand["contact"]]))
    if brand.get("careers"): out.append(("Careers", [brand["careers"]]))
    if brand.get("investors"): out.append(("Investors", [brand["investors"]]))
    if brand.get("press"): out.append(("Press", [brand["press"]]))
    if brand.get("esg"): out.append(("Sustainability / ESG", [brand["esg"]]))
    return out


def write_branding() -> Path:
    """Write the Northglen branding.md marketing artifact (Sprint 7)."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    L = ["# Northglen Bank — brand", "",
         "> Company-branding component (Sprint 7, v1 self-contained). Carried as additive "
         f"`brand` fields on the company `org://` actor {BANK} (URI cap held; not a new noun).",
         "", "## About the company", BRAND.get("about", ""), "",
         "### Mission / Vision / Values",
         f"**Mission.** {BRAND.get('mission','')}", f"**Vision.** {BRAND.get('vision','')}",
         "**Values.**", *([f"- **{n}** — {d}" for n, d in BRAND.get("values", [])] or ["—"]), "",
         "### Products & Services", *([f"- {x}" for x in BRAND.get("products_services", [])] or ["—"]), "",
         "### Customer stories / social proof",
         *([f"- “{q}” — {s}" for q, s in BRAND.get("testimonials", [])] or ["—"]), "",
         "### Trust signals", *([f"- {c} ({s})" for c, s in BRAND.get("trust", [])] or ["—"]), "",
         "### History & milestones", *([f"- **{y}** — {e}" for y, e in BRAND.get("history", [])] or ["—"]), "",
         "### Fast facts", *([f"- {x}" for x in BRAND.get("fast_facts", [])] or ["—"]), "",
         "### Locations", BRAND.get("locations", "—"), "",
         "### Leadership", *([f"- **{n}**, {t} — {b}" for n, t, b in BRAND.get("leadership", [])] or ["—"]), "",
         "## FAQ", *([f"- **Q:** {q}\n  **A:** {a}" for q, a in BRAND.get("faq", [])] or ["—"]), "",
         "## Contact", BRAND.get("contact", "—"), "",
         "## Careers", BRAND.get("careers", "—"), "",
         "## Investors", BRAND.get("investors", "—"), "",
         "## Press", BRAND.get("press", "—"), "",
         "## Sustainability / ESG", BRAND.get("esg", "—"), "",
         "## Design language",
         *([x for x in _brand_block(BRAND).splitlines() if x] or ["—"])]
    p = REPORTS / "branding.md"
    p.write_text("\n".join(L))
    return p


# ===========================================================================
# Fixture emission (same grouping the reference build uses)
# ===========================================================================
def _dump_group(by_uri, dirname, filename, prefixes):
    p = FIXTURES / dirname / f"{filename}.json"; p.parent.mkdir(parents=True, exist_ok=True)
    items = [o for u, o in by_uri.items() if u.startswith(tuple(f"{pfx}://" for pfx in prefixes))]
    p.write_text(json.dumps(items, indent=2)); return p


def emit(sub: Substrate) -> dict[str, Path]:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    by_uri = {o["uri"]: o for e in sub.ledger.entries for o in (e.get("state_update") or [])}
    files = []
    for name, prefixes in (
            ("cases", ["case"]), ("goals", ["goal"]), ("metrics", ["metric"]),
            ("tasks", ["task"]), ("dependencies", ["dependency"]), ("policies", ["policy"]),
            ("processes", ["process", "process_instance", "risk", "escalation"]),
            ("decisions", ["decision"]), ("expectations", ["expectation"]),
            ("evidence", ["evidence"]), ("trust", ["trust"]), ("claims", ["claim"]),
            ("actors_offers", ["person", "org", "agent", "entity", "rule", "offer",
                               "authority", "delegation", "consent"]),
            ("relationships", ["relationship", "interaction"]), ("events", ["event"])):
        files.append(_dump_group(by_uri, "s5", name, prefixes))
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    lf = LEDGER_DIR / "ledger-northglen.json"
    lf.write_text(json.dumps(sub.ledger.to_dict(), indent=2)); files.append(lf)
    SM_DIR.mkdir(parents=True, exist_ok=True)
    rf = SM_DIR / "relationship.json"
    rf.write_text(json.dumps({"uri": LOAN_REL, "states": ["PROPOSED", "ACTIVE"]})); files.append(rf)
    cf = SM_DIR / "case.json"
    cf.write_text(json.dumps({"uri": CASE,
                              "states": ["OPEN", "TRIAGE", "ASSIGNED", "IN_PROGRESS",
                                         "BLOCKED", "RESOLVED", "CLOSED"]})); files.append(cf)
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    gf = GRAPH_DIR / "current-state.json"
    gf.write_text(json.dumps(sub.graph.to_dict(), indent=2)); files.append(gf)
    return {f.name: f for f in files}


def build_northglen() -> Substrate:
    """Run the whole financial-sector instance: S1->S5 chain + BOL + cockpit."""
    sub = Substrate(ledger_uri="db://ledger/northglen-2026")
    bol = BolService(sub)
    provision(sub, bol)
    build_chain(sub, bol)
    s51 = build_case(sub, bol)
    s52 = build_metrics(sub, bol)
    cockpit = build_cockpit(sub, s51, s52)
    write_cockpit_report(cockpit, sub)
    emit(sub)
    sub._meta = {"s51": s51, "s52": s52, "s53": cockpit}
    return sub


if __name__ == "__main__":
    s = build_northglen()
    print("built Northglen Bank instance: ledger", len(s.ledger.entries),
          "entries, graph", len(s.graph.objects), "objects")