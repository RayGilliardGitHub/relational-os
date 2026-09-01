"""Reusable sector-instance builder for RelationalOS (multi-sector dogfood).

Given a per-sector config, builds a complete, validated instance — S1->S5 chain +
Business Operating Layer + cockpit + §7L answers — for a representative fictional
company in that sector family, and emits its fixtures/ledger/graph under
instances/<label>/artifacts. Reuses the UNMODIFIED-platform ros package; the only code
"fix" the multi-sector build surfaced (now in place) is that S4/S5 take an org/path
`label` (default 'qk' preserves the reference build byte-for-byte) so each sector emits
clean URIs on its own label instead of 'qk'.

The scene is the Financial dogfood's operating loop, parameterized: an on-time exception
on a resource-commitment outcome class, a Case, a #8 re-allocation task to the verified
counterparty and a gate on the laggard, a verified outcome, and Learning that updates a
future policy. The mechanics are identical across sectors; the domain vocabulary (URIs,
outcome class, trust claim, prose) is the config.

Design notes (URI cap / frozen ontology held):
  - Only the existing case:// goal:// metric:// task:// dependency:// nouns are used.
  - Exception/Priority/Recommendation/capacity are additive envelope fields.
  - Learning is a decision:// + a policy:// change.
  - Every object rides a signed Ledger event (full coverage, so Graph rebuilds from Ledger).
"""
from __future__ import annotations
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
ROS = HERE.parents[0] / "sprints/sprint-5/artifacts"     # /home/rlg/relational-os/sprints/...
sys.path.insert(0, str(ROS))

from ros.substrate import Substrate, now_iso            # noqa: E402
from ros.bol import BolService, project_on_time, project_settled_value, project_trust  # noqa: E402
from ros.s1 import S1Service, Permission, Denial        # noqa: E402
from ros.s2 import S2Service                            # noqa: E402
from ros.s4 import S4Service                            # noqa: E402
from ros.s5 import S5Service, config_defaults           # noqa: E402

cfg_s5 = config_defaults()
CFG5 = cfg_s5


def _uris(cfg: dict) -> dict:
    L = cfg["label"]
    def ur(scheme, rest): return f"{scheme}://{L}/{rest}"
    return {
        # fixed identity/relationship URIs are built by the config (mk) so they are
        # consistent across all uses; leave them verbatim.
        "bank": cfg["company"], "client": cfg["client"],
        "g": cfg["partner_good"], "l": cfg["partner_lag"],
        "owner": cfg["owner"], "ops": cfg["operator"],
        "orel": ur("relationship", config("orel", cfg, "ops-rel")),
        "prel": ur("relationship", config("prel", cfg, "partner-net")),
        "auth": ur("authority", "for-ops"),
        "dops": ur("delegation", "ops"), "ds2": ur("delegation", "s2-match"),
        "rop": ur("rule", "ops-run"), "rmt": ur("rule", "match-run"),
        "exp": ur("expectation", "e-on-time"),
        "pol": ur("policy", config("policy", cfg, "allocation")),
        "goal": ur("goal", config("goal", cfg, "g-core")),
        "m_on": ur("metric", "m-on-time"), "m_tr": ur("metric", "m-trust"), "m_val": ur("metric", "m-settled-value"),
        "case": ur("case", config("case", cfg, "c-on-time")),
        "task_r": ur("task", "t-rebalance"), "task_f": ur("task", "t-followup"),
        "proc": ur("process", "pr-core"), "pi": ur("process_instance", "pi-core"),
        "esc": ur("escalation", "escalate-release"), "learndec": ur("decision", "learning"),
    }


def config(key, cfg, default=None):
    return cfg.get(key, default)


# ===========================================================================
# Provision + chain + BOL (parameterized mirror of the Financial instance)
# ===========================================================================
def build_scene(cfg: dict, sub: Substrate) -> Substrate:
    L = cfg["label"]
    U = _uris(cfg)
    bol = BolService(sub, label=L)
    s1 = S1Service(sub); s2 = S2Service(sub)
    s4 = S4Service(sub, label=L); s5 = S5Service(sub, label=L)

    BANK, CLIENT, GOP, LAGP, OWNER, OPS = U["bank"], U["client"], U["g"], U["l"], U["owner"], U["ops"]
    CLAIM = cfg["claim"]
    TARGET = cfg.get("target", 0.95)
    TRUST_TARGET = cfg.get("trust_target", 0.9)
    VAL_TARGET = cfg.get("value_target", 6000000.0)

    # ---------------- provision base ----------------
    bol.prov(2, f"agent://{L}/s5",
             f"provision {cfg['sector']} base (actors, relationships, authority + operator + policy + expectation)",
             [
                 {"uri": BANK, "type": "ORG", "identity": {"attestations": [cfg["attestation"]]},
                  "brand": cfg.get("brand", {})},
                 {"uri": CLIENT, "type": "ORG"}, {"uri": GOP, "type": "ORG"}, {"uri": LAGP, "type": "ORG"},
                 {"uri": OWNER, "type": "PERSON"}, {"uri": OPS, "type": "AGENT"},
                 {"uri": U["orel"], "participants": [BANK, CLIENT], "status": "ACTIVE",
                  "roles": {BANK: [cfg["bank_role"]], CLIENT: [cfg["client_role"]]},
                  "authority": [U["auth"]], "purpose": cfg["purpose"]},
                 {"uri": U["prel"], "participants": [BANK, GOP, LAGP], "status": "ACTIVE",
                  "roles": {BANK: [cfg["net_owner_role"]], GOP: [cfg["partner_role"]], LAGP: [cfg["partner_role"]]},
                  "authority": [U["auth"]], "purpose": cfg["net_purpose"]},
                 {"uri": U["auth"], "holder": BANK,
                  "grants": ["triage_case", "assign_case", "close_case", "approve_learning",
                             "rebalance_commitment", "gate_partner", "release_committed_action"],
                  "roles": [cfg["net_owner_role"]]},
                 {"uri": U["rop"], "kind": "POLICY",
                  "text": f"{cfg['operator']} may re-balance resource commitment and gate partner performance",
                  "grants": ["rebalance_commitment", "gate_partner"]},
                 {"uri": U["rmt"], "kind": "POLICY",
                  "text": "S2 may run Trust-weighted matching for the client",
                  "grants": ["run_match"]},
                 {"uri": U["dops"], "grantor": BANK, "grantee": OPS,
                  "scope": [U["rop"]], "status": "ACTIVE"},
                 {"uri": U["ds2"], "grantor": BANK, "grantee": "agent://s2",
                  "scope": [U["rmt"]], "status": "ACTIVE"},
                 {"uri": U["exp"], "actor": OWNER, "subject": cfg["outcome"],
                  "condition": cfg["expect_cond"], "metric": "on_time", "threshold": TARGET,
                  "deadline": "2026-12-31T00:00:00Z", "evidence_required": "CLEAR"},
                 {"uri": U["pol"], "name": cfg["policy_name"], "condition": cfg["policy_cond"],
                  "decision": "select the partner with the highest fit x scoped Trust",
                  "action": "allocate to the top-ranked fitted partner", "scope": [U["exp"]], "version": 1},
                 {"uri": U["proc"], "definition": "exception -> open case -> assign -> execute -> verify -> learn -> close",
                  "steps": ["triage", "assign", "execute", "verify_outcome", "learning"]},
                 {"uri": U["pi"], "process": U["proc"], "status": "RUNNING", "started_at": now_iso()},
             ])

    # ---------------- seed scoped Trust + S2 match + prior settlements ----------------
    i = 100
    for tgt, score in ((GOP, cfg["good_seed"]), (LAGP, cfg["lag_seed"])):
        t = {"uri": f"trust://{L}/t-{tgt.split('/')[-1]}", "subject": BANK, "target": tgt,
             "claim": CLAIM, "context": U["prel"], "score": score}
        bol.prov(i, f"agent://{L}/s5", f"seed scoped Trust {tgt} = {score}", [t]); i += 1

    caps = cfg["caps"]
    for pfx, prov in (("g", GOP), ("l", LAGP)):
        bol.prov(i, f"agent://{L}/s2", f"register resource-commitment offer from {prov}",
                 [{"uri": f"offer://{L}/o-{pfx}", "provider": prov, "price": cfg.get("price", 0),
                   "currency": "USD", "capability_keys": caps,
                   "fit_note": cfg["offer_note"]}])
        i += 1
    intent = {"subject": CLIENT, "need": cfg["need"], "capability_keys": caps, "urgency": "normal"}
    m0 = s2.match_offers(intent, _offs(sub), [{"target": k, "score": v} for k, v in _trust_map(sub).items()],
                         trust_floor=cfg.get("floor", 0.4))
    bol.prov(i, f"agent://{L}/s2",
             f"initial match ranked {m0[0].offer_uri} (score {m0[0].score:.3f}) — base ranking",
             [{"uri": f"decision://{L}/s2-match-baseline", "by": "agent://s2",
               "authority": U["ds2"], "alternatives": [m.offer_uri for m in m0] + ["none"],
               "confidence": 0.9, "expected_outcome": "lag partner ranked #1 on existing Trust",
               "actual_outcome": m0[0].offer_uri, "detail": [m.to_dict() for m in m0],
               "made_at": now_iso()}]); i += 1

    # prior settled commitments: (is_good, slug-prefix, price, due, settled_offset_late)
    priors = cfg["priors"]           # list of (is_good, slug, price, committed_due, settled_at)
    for (is_good, slug, price, due, settled) in priors:
        prov = GOP if is_good else LAGP
        fx = _fx(L, U, slug, BANK, prov, price, due, settled)
        exp = _expect(L, slug, OWNER, cfg["outcome"], price, due)
        ch = s4.settle(fx, i=i); i += 1
        co = s4.evaluate(fx, exp, i=i); i += 1
        job = f"committed-{slug}"
        out = {"uri": f"event://{L}/outcome-{job}", "job": job, "provider": prov,
               "committed_deadline": due, "actual_completed_at": settled,
               "note": f"committed settlement for {slug}"}
        ev, on = s5.capture(out, _prov(cfg), signer=f"org://{L}/s5", i=i); i += 1
        vr = s5.verify(ev, f"{prov} delivered the committed resource "
                       f"{'on time' if on else 'LATE'}", out, i=i); i += 1
        s5.update_trust(subject=BANK, target=prov, claim=CLAIM, context=U["prel"], verify=vr,
                        evidence_score=vr.degree, i=i, alpha=CFG5["alpha"], expectation=CFG5["expectation"],
                        recency=CFG5["recency"], signer=f"agent://{L}/s5")
        i += 1

    # ---------------- BOL: exception -> case -> task -> verified outcome -> learning ----------------
    i = 7000
    on, total = project_on_time(sub)
    actual = on / total if total else 1.0
    case = bol.open_case(U["case"], cfg["case_subject"], OWNER, [BANK, OWNER, OPS], [U["orel"]],
                         i, f"agent://{L}/s5", suggestion="ledger-projected on-time below target")
    i += 1
    case = bol.exception_heartbeat(
        case, TARGET, round(actual, 3), "CRITICAL",
        f"{cfg['outcome_title']} on-time {actual:.2f} below target {TARGET:.2f} "
        f"(ledger: {on}/{total} committed deliveries on time)",
        cfg["root"], "SUPPORTED", cfg["recommended"], U["m_on"])
    bol.prov(i, f"agent://{L}/s5", "record exception heartbeat on the case", [case]); i += 1

    bol.prov(i, f"agent://{L}/s5", "case triage: exception assessed, root nominated",
             [{"uri": f"decision://{L}/s5-triage", "by": f"agent://{L}/s5", "authority": U["auth"],
               "alternatives": ["accept", "dismiss as anomaly"], "confidence": 0.85,
               "expected_outcome": "accept as a real risk", "actual_outcome": "accepted; root nominated",
               "made_at": now_iso()}]); i += 1
    case = bol.transition_case(case, "TRIAGE", i, f"agent://{L}/s5", "case triaged",
                               f"event://{L}/s5-case-triage"); i += 1

    pri = bol.priority(impact=0.85, urgency=0.90, confidence=0.70, irreversible=False,
                       relationship_importance=0.80, cost_of_delay=0.75)
    task = {"uri": U["task_r"], "assigned_to": OPS, "created_by": f"agent://{L}/s5",
            "objective": cfg["task_objective"], "dependencies": [], "authority": U["auth"],
            "deadline": "2026-10-15T00:00:00Z", "priority": pri["score"], "status": "ASSIGNED",
            "expected_outcome": "next committed work routed to the verified on-time partner; policy updated",
            "why_here": "derived from the on-time exception (case OPEN)",
            "importance": cfg["task_importance"],
            "evidence": [f"evidence://{L}/committed-{slug}" for _, slug, *_ in priors],
            "decision_required": "approve the re-allocation",
            "priority_factors": pri["factors"], "assigned_capacity": 1.0}
    bol.prov(i, f"agent://{L}/s5", "case assigned; task becomes assigned authorized work (#8)",
             [task, {"uri": f"decision://{L}/s5-assign", "by": OWNER, "authority": U["auth"],
                     "alternatives": ["assign", "defer"], "confidence": 0.95,
                     "expected_outcome": "task in progress",
                     "detail": {"task": U["task_r"], "assigned_to": OPS, "authority": U["auth"],
                                "priority": pri["score"], "capacity": task["assigned_capacity"]},
                     "made_at": now_iso()}]); i += 1
    case = bol.transition_case(case, "ASSIGNED", i, f"agent://{L}/s5", "case assigned",
                               f"event://{L}/s5-case-assigned"); i += 1

    case = bol.transition_case(case, "IN_PROGRESS", i, f"agent://{L}/s5", "task execution began",
                               f"event://{L}/s5-case-inprogress"); i += 1
    bol.prov(i, f"agent://{L}/s5", "policy updated: allocate by fit AND scoped Trust",
             [{"uri": U["pol"], "name": cfg["policy_name"], "condition": cfg["policy_cond"],
               "decision": "select by fit x scoped Trust; laggard (< floor) needs a performance gate",
               "action": "allocate to the top-ranked fitted partner; gate laggard",
               "scope": [U["exp"]], "version": 2, "policy_status": "REVISED"}]); i += 1
    matches = s2.match_offers(intent, _offs(sub),
                              [{"target": k, "score": v} for k, v in _trust_map(sub).items()],
                              trust_floor=cfg.get("floor", 0.4))
    bol.prov(i, f"agent://{L}/s2",
             f"task effect: next committed work ranked {matches[0].offer_uri} (score {matches[0].score:.3f})",
             [{"uri": f"decision://{L}/s5-match-recorded", "by": "agent://s2", "authority": U["ds2"],
               "alternatives": [m.offer_uri for m in matches] + ["none"], "confidence": 0.92,
               "expected_outcome": "good partner ranked #1", "actual_outcome": matches[0].offer_uri,
               "detail": [m.to_dict() for m in matches], "made_at": now_iso()}]); i += 1

    # §6 human floor: releasing the committed action is irreversible -> escalates to the owner
    bol.prov(i, f"agent://{L}/s5",
             "escalation: the committed action is irreversible and cost-unknowable once done (§6 floor)",
             [{"uri": U["esc"], "trigger": cfg["esc_trigger"], "severity": "WARN", "recipient": OWNER,
               "deadline": "2026-11-15T00:00:00Z", "fallback": f"agent://{L}/s4", "authority": U["auth"],
               "acknowledgement": "approve then execute"}], uri=f"event://{L}/s5-escalate")
    i += 1
    sub.record({"uri": f"event://{L}/owner-human", "type": "DECISION",
                "event_id": f"ev-{L}-{i}", "correlation_id": f"corr-{L}-bol-1",
                "causation_id": f"ev-{L}-{max(0, i-1)}", "idempotency_key": f"idem-{L}-{i}",
                "signature": f"signed-by-{OWNER}", "occurred_at": now_iso(), "actor": OWNER,
                "detail": f"{cfg['owner']} signed approval to release the committed action (§6 floor)",
                "state_update": [{"uri": f"decision://{L}/owner-human", "by": OWNER, "authority": U["auth"],
                                  "alternatives": ["release_in_full", "hold",
                                                   "release_partial_and_hold_if_shortfall", "open_dispute"],
                                  "confidence": 1.0, "expected_outcome": "release to the verified partner",
                                  "actual_outcome": "release_in_full (human approved)",
                                  "detail": {"task": U["task_r"], "action": "release_committed_action",
                                             "irreversible_failure": True, "cost_failure_unknowable": True},
                                  "made_at": now_iso()}]}, OWNER)
    i += 1
    sub.record({"uri": f"event://{L}/action-release", "type": "ACTION",
                "event_id": f"ev-{L}-{i}", "correlation_id": f"corr-{L}-bol-1",
                "causation_id": f"ev-{L}-{max(0, i-1)}", "idempotency_key": f"idem-{L}-{i}",
                "signature": f"signed-by-{OWNER}", "occurred_at": now_iso(), "actor": OPS,
                "detail": "rebalance_commitment executed after human approval",
                "worker": OPS, "action": "rebalance_commitment", "task_id": "t-rebalance",
                "tier": "human", "outcome": "done", "state_update": []}, OWNER)
    i += 1
    case = bol.transition_case(case, "BLOCKED", i, f"agent://{L}/s5",
                               "case blocked pending the rallied committed delivery's verification",
                               f"event://{L}/s5-case-blocked"); i += 1

    # rallied follow-on to the good partner -> settle on time -> verify -> trust up
    rx = cfg["rallied"]          # (slug, price, due, settled)
    rs, rpr, rdue, rsettled = rx
    bol.prov(i, f"agent://{L}/s5", f"rallied committed work allocated to {GOP} (the fix)",
             [{"uri": f"commitment://{L}/c-{GOP.split('/')[-1]}-followup", "by": f"agent://{L}/s5",
               "to": GOP, "obligation": f"offer://{L}/o-g",
               "expectation": f"expectation://{L}/e-routed-{rs}", "status": "AGREED",
               "terms": {"kind": cfg["outcome"] + " follow-up", "signed": True},
               "agreed_at": now_iso()}]); i += 1
    fx = _fx(L, U, rs, BANK, GOP, rpr, rdue, rsettled)
    fexp = _expect(L, rs, OWNER, cfg["outcome"], rpr, rdue)
    bol.prov(i, f"agent://{L}/s5", "register follow-on expectation", [fexp]); i += 1
    chol = s4.settle(fx, i=i); i += 1
    fout = s4.evaluate(fx, fexp, i=i); i += 1
    job = "routed-" + rs
    out = {"uri": f"event://{L}/outcome-{job}", "job": job, "provider": GOP,
           "committed_deadline": rdue, "actual_completed_at": rsettled,
           "note": f"rallied committed work settled per {fout['uri']} ({fout['evaluation']})"}
    fev, fon = s5.capture(out, _prov(cfg), signer=f"org://{L}/s5", i=i); i += 1
    fvr = s5.verify(fev, f"{GOP} delivered the rallied committed {cfg['outcome']} on time", out, i=i); i += 1
    ftrust = s5.update_trust(subject=BANK, target=GOP, claim=CLAIM, context=U["prel"], verify=fvr,
                             evidence_score=fvr.degree, i=i, alpha=CFG5["alpha"],
                             expectation=CFG5["expectation"], recency=CFG5["recency"],
                             signer=f"agent://{L}/s5")
    i += 1

    on2, tot2 = project_on_time(sub)
    forward_rate = 1.0
    case = bol.transition_case(case, "RESOLVED", i, f"agent://{L}/s5",
                               f"exception resolved: rallied committed work verified on time; "
                               f"forward on-time = 1.0; cumulative {on2}/{tot2}",
                               f"event://{L}/s5-case-resolved",
                               verified_outcome=f"forward on-time restored to 1.0; {GOP} delivered "
                                                f"the rallied {cfg['outcome']} on time ({fev['uri']}); "
                                                f"{GOP} Trust {ftrust['score']}")
    i += 1
    learning = bol.learning_entry(
        f"decision://{L}/learning", cfg["outcome"] + " on-time management", f"agent://{L}/s5",
        i, f"agent://{L}/s5", expected=TARGET, actual=forward_rate,
        why=cfg["learning_why"], change_future_policy=cfg["policy_change"])
    i += 1
    bol.prov(i, f"agent://{L}/s5", "close case; learning recorded; future policy updated",
             [{"uri": U["pol"], "name": cfg["policy_name"], "condition": cfg["policy_cond"],
               "decision": cfg["policy_final"], "action": "allocate to the top-ranked fitted partner; gate laggard",
               "scope": [U["exp"]], "version": 3, "policy_status": "EFFECTIVE",
               "learning": f"decision://{L}/learning"}])
    case = bol.transition_case(case, "CLOSED", i, f"agent://{L}/s5", "case closed",
                               f"event://{L}/s5-case-closed"); i += 1

    summary = {"case": U["case"], "final_status": case["status"],
               "exception": {"expected": TARGET, "actual": round(actual, 3),
                             "variance": round(actual - TARGET, 3), "significance": "CRITICAL",
                             "on": on, "total": total},
               "task": U["task_r"], "assigned_to": OPS, "authority": U["auth"], "priority": pri,
               "follow_on": {"exchange": chol["uri"], "outcome": fout["uri"],
                             "evaluation": fout["evaluation"], "evidence": fev["uri"],
                             "after_trust": ftrust["score"], "forward_on_time": forward_rate,
                             "cumulative_after": round(on2 / tot2, 3)},
               "learning": learning["uri"]}

    # ---------------- goals / metrics / health ----------------
    cpu = project_trust(sub, GOP, U["prel"]) or 0.0
    settled_v = project_settled_value(sub)
    onf, totf = project_on_time(sub)
    on_rate = onf / totf if totf else 1.0
    goal = {"uri": U["goal"], "for": BANK, "statement": cfg["goal_text"], "horizon": "quarter",
            "owner": OWNER, "metrics": [U["m_on"], U["m_tr"], U["m_val"]]}
    m_on = {"uri": U["m_on"], "name": cfg["m_on_name"], "definition": cfg["m_on_def"],
            "unit": "fraction", "formula": "on_time / (on_time + late) from ledger",
            "dimensions": ["partner"], "target": TARGET, "threshold": 0.8, "period": "quarter",
            "source": "ledger committed-delivery records", "owner": OWNER,
            "actual": round(on_rate, 3), "forecast": 0.5, "variance": round(on_rate - TARGET, 3),
            "root_cause": cfg["root"], "root_cause_status": "SUPPORTED"}
    m_tr = {"uri": U["m_tr"], "name": cfg["m_trust_name"], "definition": cfg["m_trust_def"],
            "unit": "score", "formula": "T(subject->target, claim, context) per §5",
            "dimensions": ["partner"], "target": TRUST_TARGET, "threshold": 0.6, "period": "rolling",
            "source": "S5 scoped Trust graph", "owner": OWNER, "actual": round(cpu, 3),
            "forecast": 0.92, "variance": round(cpu - TRUST_TARGET, 3), "root_cause_status": "UNKNOWN"}
    m_val = {"uri": U["m_val"], "name": cfg["m_val_name"], "definition": cfg["m_val_def"],
             "unit": "USD", "formula": "sum(EXCHANGE.price) from ledger",
             "dimensions": ["partner"], "target": VAL_TARGET, "threshold": VAL_TARGET * 0.55,
             "period": "quarter", "source": "ledger EXCHANGE events", "owner": OWNER,
             "actual": settled_v, "forecast": VAL_TARGET * 1.15, "variance": round(settled_v - VAL_TARGET, 2),
             "root_cause_status": "UNKNOWN"}
    bol.prov(i, f"agent://{L}/s5", "register goal + ledger-projected metrics",
             [goal, m_on, m_tr, m_val]); i += 1
    bol.metric_loop(goal, m_on, f"decision://{L}/s5-metric-loop", U["task_r"],
                    f"event://{L}/outcome-routed-{rs}", i, f"agent://{L}/s5"); i += 1
    att = [{"uri": U["task_r"], "label": "re-balance committed work",
            "priority": bol.priority(0.85, 0.90, 0.70, False, 0.80, 0.75)["score"]},
           {"uri": U["task_f"], "label": "rallied follow-on (good partner)",
            "priority": bol.priority(0.70, 0.75, 0.60, False, 0.70, 0.60)["score"]}]
    att.sort(key=lambda x: x["priority"], reverse=True)
    bol.prov(i, f"agent://{L}/s5", "priority-ordered attention list",
             [{"uri": f"decision://{L}/s5-attention", "by": f"agent://{L}/s5", "authority": U["auth"],
               "confidence": 0.9, "expected_outcome": "top-of-attention ranked",
               "actual_outcome": "attention prioritized by derived score",
               "detail": {"attention": att}, "made_at": now_iso()}]); i += 1
    for uri, fr, to, kind in (
            (f"dependency://{L}/d-rb-enables-fu", U["task_r"], U["task_f"], "ENABLES"),
            (f"dependency://{L}/d-fu-requires-pol", U["task_f"], U["pol"], "REQUIRES"),
            (f"dependency://{L}/d-fu-blocks-case", U["task_f"], U["case"], "BLOCKS"),
            (f"dependency://{L}/d-case-from-metric", U["case"], U["m_on"], "DERIVED_FROM"),
            (f"dependency://{L}/d-metric-impacts-goal", U["m_on"], U["goal"], "IMPACTS"),
            (f"dependency://{L}/d-rb-blocks-case", U["task_r"], U["case"], "BLOCKS")):
        bol.make_dependency(uri, fr, to, kind, i, f"agent://{L}/s5"); i += 1
    impact_r = bol.impact_analysis(U["task_r"])
    health = []
    for m in (m_on, m_tr, m_val):
        var = m.get("variance", 0.0); tgt = m.get("target") or 1.0
        rel = var / abs(tgt)
        status = "OK" if rel >= 0 else ("WARN" if rel >= -0.05 else "CRITICAL")
        health.append({"metric": m["uri"], "name": m["name"], "unit": m["unit"],
                       "target": m.get("target"), "actual": m.get("actual"),
                       "variance": var, "status": status, "forecast": m.get("forecast")})

    cockpit = {
        "company": f"{cfg['company_name']} ({cfg['sector']}, fictional)", "generated": now_iso(),
        "health": health,
        "attention_line": f"{len(att)} things requiring attention today", "attention": att,
        "exception": summary["exception"], "case": summary["case"], "case_status": summary["final_status"],
        "recommendation": {"summary": summary["task"], "authority_required": U["auth"],
                           "options": [cfg["rec_option"], cfg["gate_option"], "do nothing"],
                           "includes_do_nothing": True, "tradeoff": cfg["tradeoff"],
                           "confidence": 0.85, "expected_impact": cfg["expected_impact"],
                           "decision": f"decision://{L}/s5-assign"},
        "verified_outcome": summary["follow_on"], "learning": summary["learning"],
        "ledger": len(sub.ledger.entries), "graph": len(sub.graph.objects),
    }
    sub._meta = {"s52_health": health, "s53": cockpit,
                 "cfg": cfg, "uris": U, "s51_exception": summary["exception"],
                 "prior_good": GOP, "prior_lag": LAGP}
    return sub


def _fx(L, U, slug, buyer, prov, price, due, settled):
    return {"slug": slug, "buyer": buyer, "provider": prov, "price": price,
            "currency": "USD", "value": price, "cost": price, "due": due,
            "settled_at": settled, "of": f"commitment://{L}/c-{slug}"}


def _expect(L, slug, actor, subject, price, due):
    return {"uri": f"expectation://{L}/e-{slug}", "actor": actor, "subject": subject,
            "condition": "fully deliver the committed resource by its committed deadline",
            "metric": "settled_value", "threshold": price, "deadline": due,
            "evidence_required": "CLEAR"}


def _prov(cfg):
    return {"source": cfg["prov_source"], "procedure": cfg.get("prov_procedure", "anchor-conformance"),
            "confidence": 0.95}


def _trust_map(sub) -> dict:
    return {o["target"]: float(o.get("score", 0.0))
            for o in sub.graph.objects.values() if o.get("uri", "").startswith("trust://")}


def _offs(sub) -> list[dict]:
    return [o for o in sub.graph.objects.values() if o.get("uri", "").startswith("offer://")]


# ===========================================================================
# Fixture emission + cockpit report + generic checks
# ===========================================================================
def emit(sub, outdir: Path) -> dict[str, Path]:
    ART = outdir / "artifacts"; FX = ART / "fixtures"
    by_uri = {o["uri"]: o for e in sub.ledger.entries for o in (e.get("state_update") or [])}
    groups = (("cases", ["case"]), ("goals", ["goal"]), ("metrics", ["metric"]),
              ("tasks", ["task"]), ("dependencies", ["dependency"]), ("policies", ["policy"]),
              ("processes", ["process", "process_instance", "risk", "escalation"]),
              ("decisions", ["decision"]), ("expectations", ["expectation"]),
              ("evidence", ["evidence"]), ("trust", ["trust"]), ("claims", ["claim"]),
              ("actors_offers", ["person", "org", "agent", "entity", "rule", "offer",
                                 "authority", "delegation", "consent"]),
              ("relationships", ["relationship", "interaction"]), ("events", ["event"]))
    files = []
    for name, prefixes in groups:
        p = FX / "s5" / f"{name}.json"; p.parent.mkdir(parents=True, exist_ok=True)
        items = [o for u, o in by_uri.items() if u.startswith(tuple(f"{x}://" for x in prefixes))]
        p.write_text(json.dumps(items, indent=2)); files.append(p)
    ld = FX / "ledger"; ld.mkdir(parents=True, exist_ok=True)
    lf = ld / "ledger.json"; lf.write_text(json.dumps(sub.ledger.to_dict(), indent=2)); files.append(lf)
    st = FX / "statemachines"; st.mkdir(parents=True, exist_ok=True)
    rel = sub._meta["uris"]["orel"]
    rf = st / "relationship.json"; rf.write_text(json.dumps({"uri": rel, "states": ["PROPOSED", "ACTIVE"]}))
    ctv = sub._meta["uris"]["case"]
    cf = st / "case.json"; cf.write_text(json.dumps({"uri": ctv,
        "states": ["OPEN", "TRIAGE", "ASSIGNED", "IN_PROGRESS", "BLOCKED", "RESOLVED", "CLOSED"]}))
    gd = ART / "graph"; gd.mkdir(parents=True, exist_ok=True)
    gf = gd / "current-state.json"; gf.write_text(json.dumps(sub.graph.to_dict(), indent=2)); files.append(gf)
    return {f.name: f for f in files}


def write_cockpit(sub, outdir: Path) -> None:
    cfg = sub._meta["cfg"]; L = sub._meta["cfg"]["label"]; c = sub._meta["s53"]
    U = sub._meta["uris"]; rp = outdir / "artifacts/reports"; rp.mkdir(parents=True, exist_ok=True)
    brand = cfg.get("brand", {})
    on, total = project_on_time(sub); settled_v = project_settled_value(sub)
    rate = round(on / total, 3) if total else 1.0
    A = []
    ap = A.append
    headline = f"# {cfg['company_name']} — Business Operating Layer cockpit ({cfg['sector']} instance)"
    if brand and isinstance(brand.get("tagline"), str):
        headline = f"# {cfg['company_name']} — {brand['tagline']}"
    ap(headline)
    ap(f"generated {c['generated']}  |  ledger events {len(sub.ledger.entries)}  graph objects {len(sub.graph.objects)}")
    ap("")
    ap("## Business health (ledger-projected metrics)")
    ap("| metric | unit | target | actual | variance | status |")
    ap("|---|---|---|---|---|---|")
    for h in c["health"]:
        ap(f"| {h['name']} (`{h['metric']}`) | {h['unit']} | {h['target']} | {h['actual']} | {h['variance']} | {h['status']} |")
    ap("")
    ap(f"## Prioritized attention — {c['attention_line']}")
    for a in c["attention"]:
        ap(f"- **{a['priority']:.2f}** {a['label']} (`{a['uri']}`)")
    ap("")
    ap("## Exception (heartbeat, §7J.2)")
    ex = c["exception"]
    ap(f"- expected {ex['expected']}  actual {ex['actual']}  variance {ex['variance']}  "
      f"significance {ex['significance']}  ({ex['on']}/{ex['total']} ledger committed deliveries on time)")
    ap(f"- case `{c['case']}`  status **{c['case_status']}**")
    ap("")
    ap("## AI recommendation (#8) with the authority it requires (§7J.9)")
    rec = c["recommendation"]
    ap(f"- recommended work: `{rec['summary']}`")
    ap(f"- authority required: `{rec['authority_required']}`  confidence {rec['confidence']}")
    ap(f"- options: {rec['options']}  (do-nothing included: {rec['includes_do_nothing']})")
    ap(f"- trade-off: {rec['tradeoff']}")
    ap(f"- expected impact: {rec['expected_impact']}")
    ap("")
    ap("## Verified outcome (#10) + Learning")
    fo = c["verified_outcome"]
    ap(f"- rallied good-partner committed work settled {fo['exchange']}, outcome {fo['outcome']} "
      f"({fo['evaluation']}); evidence {fo['evidence']}; forward on-time {fo['forward_on_time']}; "
      f"{U['g']} Trust -> {fo['after_trust']}")
    ap(f"- Learning entry: `{c['learning']}`")
    ap("")
    ap("## §7L — the ten morning questions, answered with evidence")
    ap(f"1. WHAT HAPPENED?  Committed work on time {on}/{total} ({rate}); good partner on time "
      f"(ev {fo['evidence']}), lag partner late; committed value {settled_v}.  [ledger evidence]")
    ap(f"2. WHAT CHANGED?  Re-allocation recommended; rallied good-partner work verified on time; "
      f"forward on-time = {fo['forward_on_time']}.  [delta -> significance]")
    ap(f"3. WHAT MATTERS?  Priority-ordered attention: {', '.join(a['label'] for a in c['attention'])}.  [§7J.5]")
    ap(f"4. WHAT'S GOING WRONG?  Committed on-time {rate} below target {ex['expected']} (CRITICAL).  [§7J.2]")
    ap(f"5. WHY?  {cfg['root']} (root SUPPORTED).  [§7K.2 epistemic status]")
    ap("6. WHAT IF WE DO NOTHING?  Forecast on-time ~0.5 < target; laggard keeps missing; "
       "scoped Trust erodes.  [§7K.1 forecast]")
    ap("7. WHAT ARE OUR OPTIONS?  re-balance to good partner; gate laggard; do-nothing (all "
       "costed; trade-off in the recommendation).  [§7K.1]")
    ap(f"8. WHAT SHOULD WE DO?  -> assigned, authorized Task {rec['summary']} under "
      f"{rec['authority_required']}.  [recommendation]")
    ap(f"9. WHO DOES IT, AND AUTHORITY/CAPACITY?  {U['ops']} via {U['dops']} (delegation-bounded "
      f"authority, capacity 1.0), owner {U['owner']}.  [ownership + authority/capacity]")
    ap(f"10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied committed work verified on time "
      f"(forward on-time {fo['forward_on_time']}); Learning entry {c['learning']}; policy v3 updated.  "
      f"[verified outcome + organisational learning]")
    if brand:
        ap("")
        ap("## Brand (company identity carried on the org actor; additive field, §7J.11)")
        ap(_brand_block(brand))
    (rp / "cockpit.md").write_text("\n".join(A))
    (rp / "cockpit.json").write_text(json.dumps({"cockpit": c, "brand": brand}, indent=2))


def _brand_entries(brand: dict) -> list[tuple[str, list[str]]]:
    """Flatten the brand dict into [(section, [lines])] for rendering (Sprint 7)."""
    out = []
    if brand.get("mission"):
        out.append(("Mission", [brand["mission"]]))
    if brand.get("vision"):
        out.append(("Vision", [brand["vision"]]))
    if brand.get("about"):
        out.append(("About", [brand["about"]]))
    if brand.get("values"):
        out.append(("Values", [f"- **{n}** — {d}" for n, d in brand["values"]]))
    if brand.get("products_services"):
        out.append(("Products & Services", [f"- {x}" for x in brand["products_services"]]))
    if brand.get("trust"):
        out.append(("Trust signals", [f"- {claim} ({src})" for claim, src in brand["trust"]]))
    if brand.get("testimonials"):
        out.append(("Customer stories", [f"- “{q}” — {src}" for q, src in brand["testimonials"]]))
    if brand.get("history"):
        out.append(("History", [f"- **{y}** — {e}" for y, e in brand["history"]]))
    if brand.get("leadership"):
        out.append(("Leadership", [f"- **{n}**, {t} — {b}" for n, t, b in brand["leadership"]]))
    if brand.get("fast_facts"):
        out.append(("Fast facts", [f"- {x}" for x in brand["fast_facts"]]))
    if brand.get("locations"):
        out.append(("Locations", [brand["locations"]]))
    if brand.get("faq"):
        out.append(("FAQ", [f"- **Q:** {q}\\n  **A:** {a}" for q, a in brand["faq"]]))
    if brand.get("contact"):
        out.append(("Contact", [brand["contact"]]))
    if brand.get("careers"):
        out.append(("Careers", [brand["careers"]]))
    if brand.get("investors"):
        out.append(("Investors", [brand["investors"]]))
    if brand.get("press"):
        out.append(("Press", [brand["press"]]))
    if brand.get("esg"):
        out.append(("Sustainability / ESG", [brand["esg"]]))
    if brand.get("nav"):
        out.append(("Site navigation", [", ".join(brand["nav"])]))
    if brand.get("legal"):
        out.append(("Legal footer", [", ".join(brand["legal"])]))
    if brand.get("cookie_consent"):
        out.append(("Cookie consent", [brand["cookie_consent"]]))
    return out


def _brand_block(brand: dict) -> str:
    """Render the full brand as a markdown block for the cockpit appendix / branding.md."""
    lines = [f"**{brand.get('tagline', '')}**"] if brand.get("tagline") else []
    for name, entries in _brand_entries(brand):
        lines.append(f"**{name}**")
        lines.extend(entries)
    d = brand.get("design") or {}
    if d:
        lines.append("**Design language**")
        if d.get("palette"):
            lines.append("- Palette: " + ", ".join(f"{n} {hexc}" for n, hexc in d["palette"]))
        if d.get("typography"):
            lines.append(f"- Typography: heading {d['typography'].get('heading')} · body {d['typography'].get('body')}")
        if d.get("logo"):
            lines.append(f"- Logo: {d['logo'].get('wordmark')} ({d['logo'].get('character')}); usage — {d['logo'].get('usage')}")
        if d.get("imagery"):
            lines.append(f"- Imagery: {d['imagery']}")
        if d.get("tone"):
            lines.append(f"- Tone of voice: {d['tone']}")
    return "\n".join(lines)


def write_branding(sub, outdir: Path) -> Path:
    """Write the per-instance branding.md marketing artifact (Sprint 7)."""
    cfg = sub._meta["cfg"]; rp = outdir / "artifacts/reports"; rp.mkdir(parents=True, exist_ok=True)
    brand = cfg.get("brand", {})
    L = ["# " + cfg["company_name"] + " — brand",
         "",
         "> Company-branding component (Sprint 7). Carried as additive `brand` fields on the "
         "company `org://` actor " + cfg["company"] + " (URI cap / frozen ontology held: a field, "
         "not a new noun).",
         "",
         "## About the company",
         brand.get("about", ""),
         "",
         "### Mission / Vision / Values",
         "**Mission.** " + brand.get("mission", ""),
         "**Vision.** " + brand.get("vision", ""),
         "**Values.**",
         *([f"- **{n}** — {d}" for n, d in brand.get("values", [])] or ["—"]),
         "",
         "### Products & Services",
         *([f"- {x}" for x in brand.get("products_services", [])] or ["—"]),
         "",
         "### Customer stories / social proof",
         *([f"- “{q}” — {src}" for q, src in brand.get("testimonials", [])] or ["—"]),
         "",
         "### Trust signals",
         *([f"- {claim} ({src})" for claim, src in brand.get("trust", [])] or ["—"]),
         "",
         "### History & milestones",
         *([f"- **{y}** — {e}" for y, e in brand.get("history", [])] or ["—"]),
         "",
         "### Fast facts",
         *([f"- {x}" for x in brand.get("fast_facts", [])] or ["—"]),
         "",
         "### Locations",
         brand.get("locations", "—"),
         "",
         "### Leadership",
         *([f"- **{n}**, {t} — {b}" for n, t, b in brand.get("leadership", [])] or ["—"]),
         "",
         "## FAQ",
         *([f"- **Q:** {q}\n  **A:** {a}" for q, a in brand.get("faq", [])] or ["—"]),
         "",
         "## Contact",
         brand.get("contact", "—"),
         "",
         "## Careers",
         brand.get("careers", "—"),
         "",
         "## Investors",
         brand.get("investors", "—"),
         "",
         "## Press",
         brand.get("press", "—"),
         "",
         "## Sustainability / ESG",
         brand.get("esg", "—"),
         "",
         "## Design language",
         *([line for line in _brand_block(brand).splitlines() if line] or ["—"]),
                 ]
    p = rp / "branding.md"
    p.write_text("\n".join(L))
    return p


def run_checks(sub, outdir: Path | None = None) -> list[tuple[str, bool, str]]:
    """Generic PASS/FAIL assertions for a sector instance (mirror the Financial run)."""
    out = []
    outdir = outdir or Path(__file__).resolve().parent
    L = sub._meta["cfg"]["label"]; U = sub._meta["uris"]
    s1 = S1Service(sub)
    out.append(("borrower-like role resolved (role is relationship-scoped)",
                s1.resolve_role(U["orel"], U["client"], {"relationship": U["orel"]}) == sub._meta["cfg"]["client_role"],
                f"got {s1.resolve_role(U['orel'], U['client'], {'relationship': U['orel']})}"))
    out.append(("role scoped (absent elsewhere)", s1.resolve_role(f"relationship://{L}/none", U["client"], {}) is None, ""))
    perm = s1.authorize(U["ops"], "rebalance_commitment", {"relationship": U["prel"], "delegation": U["dops"]})
    out.append(("delegation grants scoped capability", isinstance(perm, Permission), repr(perm)))
    den = s1.authorize(U["ops"], "rebalance_commitment", {"relationship": f"relationship://{L}/none"})
    out.append(("authz denied outside any known relationship", isinstance(den, Denial), repr(den)))
    ok, why = sub.ledger.verify(); out.append(("ledger hash-chain + signatures", ok, why or f"{len(sub.ledger.entries)} entries"))
    rebuilt = {o["uri"] for e in sub.ledger.entries for o in (e.get("state_update") or [])}
    orig = {o["uri"] for o in sub.graph.to_dict()["objects"]}
    out.append(("full-state round-trip (Graph rebuilds from Ledger)",
                not (orig - rebuilt) and len(orig) == len(rebuilt),
                f"{len(orig)} graph objects rebuilt from {len(sub.ledger.entries)} events"))
    g = sub.graph.get(f"trust://{L}/t-{U['g'].split('/')[-1]}")
    lp = sub.graph.get(f"trust://{L}/t-{U['l'].split('/')[-1]}")
    out.append(("trust flywheel (good > lag)", g and lp and g["score"] > lp["score"], f"good {g['score']} lag {lp['score']}"))
    i_esc, i_hum, i_rel = (idx(sub, f"event://{L}/{x}") for x in ("s5-escalate", "owner-human", "action-release"))
    out.append(("§6 floor order in the ledger (escalate < human < release)",
                i_esc >= 0 and i_hum >= 0 and i_rel >= 0 and i_esc < i_hum < i_rel,
                f"[{i_esc} < {i_hum} < {i_rel}]"))
    out.append(("escalation:// recorded", sub.graph.get(U["esc"]) is not None, ""))
    case = sub.graph.get(U["case"])
    hist = [h["status"] for h in (case or {}).get("history", [])]
    out.append(("case lifecycle OPEN->...->CLOSED", hist == ["OPEN", "TRIAGE", "ASSIGNED", "IN_PROGRESS", "BLOCKED", "RESOLVED", "CLOSED"], str(hist)))
    out.append(("learning + future policy updated", sub.graph.get(f"decision://{L}/learning") is not None
                and (sub.graph.get(U["pol"]) or {}).get("version") == 3, ""))
    out.append(("cockpit report written",
                (outdir / "artifacts/reports/cockpit.md").exists()
                and (outdir / "artifacts/reports/cockpit.json").exists(), ""))
    bank = sub.graph.get(U["bank"])
    out.append(("company org actor carries additive brand",
                bool(bank) and "brand" in bank and bank.get("brand", {}).get("tagline", ""),
                f"tagline: {bank.get('brand', {}).get('tagline', '') if bank else ''}"))
    out.append(("brand rendered in cockpit (## Brand appendix + header)",
                (outdir / "artifacts/reports/cockpit.md").exists()
                and "## Brand" in (outdir / "artifacts/reports/cockpit.md").read_text()
                and (outdir / "artifacts/reports/cockpit.json").exists()
                and "brand" in (outdir / "artifacts/reports/cockpit.json").read_text(), ""))
    out.append(("branding.md marketing artifact written",
                (outdir / "artifacts/reports/branding.md").exists(), ""))
    return out


def idx(sub, uri):
    for n, e in enumerate(sub.ledger.entries):
        if e.get("uri") == uri:
            return n
    return -1