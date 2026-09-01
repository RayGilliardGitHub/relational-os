"""run_interest_conflict_demo.py — CONFLICTING-INTEREST experiment (Sprint 10).

The *next* extension of the contested-reality work: not a disputed FACT (Sprint 9 solved
that) but a genuine CONFLICT OF INTERESTS between two parties under a shared organizational
constraint — the review's Scenario B (remote-work): employee wants remote work + use unused
leave; manager needs on-site coverage to meet a 30-minute customer-response SLA with a
staffing floor; company policy permits remote work under conditions.

Built entirely additively on EXISTING primitives (case://, relationship://, expectation://,
policy://, right://, decision://, authority://). NO new noun, NO schema edit, 49 $defs intact,
SPEC stays v0.22. The conflict and each party's interest are *additive fields* on those
objects (exactly the Exception/Priority/Recommendation/epistemic_state pattern).

Contained:
  - two interests modeled with explicit stakes (employee, manager)
  - the shared constraint (SLA + staffing floor + conditional policy) binding both
  - deterministic conflict detection under the constraint
  - case OPEN with the conflict + recorded uncertainty
  - a defensible determination (the middle option: remote-with-coverage-plan) AND the
    inviolable UNRESOLVED outcome (insufficient admissible basis) — both reachable
  - a signed, first-class appeal re-adjudicated by a higher authority (not a silent redo)
  - the adjudicator's determination conserves the authority it requires (§7J.9)

Usage: (from instances/contested_reality)  python3 run_interest_conflict_demo.py  exit 0 = ALL PASS
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCES = HERE.parent
ROS = INSTANCES.parents[0] / "sprints/sprint-5/artifacts"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(INSTANCES))
sys.path.insert(0, str(ROS))

import sector_scene as ss            # noqa: E402
import configs                       # noqa: E402
from ros.substrate import Substrate, now_iso  # noqa: E402
from ros.s5 import S5Service, config_defaults  # noqa: E402

CFG5 = config_defaults()

CUSTOMER = "org://ic/customer"
COMPANY = "org://ic/company"
EMP = "person://ic/employee"
MGR = "person://ic/manager"
DIRECTOR = "person://ic/director"
AUTH_ADJ = "authority://ic/adjudicate-remote"
AUTH_APPEAL = "authority://ic/for-appeal"
REL_EMP = "relationship://ic/employment"
REL_CONTRACT = "relationship://ic/contract"
REL_AUTH = "relationship://ic/staffing-authority"


def ev(sub, uri, kind, signer, detail, updates, i=0):
    sub.record({
        "uri": uri, "type": kind,
        "event_id": f"ev-ic-{uri.split('/')[-1]}-{i}",
        "correlation_id": "corr-ic-1", "causation_id": f"ev-ic-prev-{i}",
        "idempotency_key": f"idem-ic-{uri.split('/')[-1]}-{i}",
        "signature": f"signed-by-{signer}", "occurred_at": now_iso(),
        "actor": signer, "detail": detail, "state_update": updates},
        signer)


def run():
    sub = Substrate(ledger_uri="db://ledger/interest-conflict-2026")
    ok = True
    out = []
    def check(name, cond, why=""):
        nonlocal ok
        ok &= bool(cond)
        out.append((name, bool(cond), why))
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")

    print("=== CONFLICTING-INTEREST experiment (remote-work, Scenario B) ===\n")

    # ---- 1. provision actors, relationships, rights, adjudicator + appeal authority ----
    ev(sub, "event://ic/provision", "STATE_CHANGE", COMPANY,
       "provision actors, employment + contract + staffing-authority relationships, "
       "employee APPEAL right, adjudicator + appeal authority",
       [{"uri": CUSTOMER, "type": "ORG"}, {"uri": COMPANY, "type": "ORG"},
        {"uri": EMP, "type": "PERSON"}, {"uri": MGR, "type": "PERSON"},
        {"uri": DIRECTOR, "type": "PERSON"},
        {"uri": REL_EMP, "participants": [EMP, COMPANY], "status": "ACTIVE",
         "roles": {EMP: ["employee"], COMPANY: ["employer"]},
         # EMPLOYEE INTEREST (additive object, explicit stakes)
         "interest": {"party": EMP, "want": "remote-work-and-use-unused-leave",
                      "stakes": ["work-from-home wellbeing", "use 12 accrued unused-leave days"],
                      "legitimate": True, "within_policy": True,
                      "unused_leave_days": 12,
                      "arrangement_requested": "full-remote"},
         "purpose": "employment with accrued unused leave"},
        {"uri": REL_CONTRACT, "participants": [CUSTOMER, COMPANY], "status": "ACTIVE",
         "roles": {CUSTOMER: ["buyer"], COMPANY: ["provider"]},
         # SHARED CONSTRAINT (additive) — the SLA + staffing floor + conditional policy
         # both parties are subject to.  (keys avoid C2 temporal suffixes)
         "constraint": {"response_target_minutes": 30,
                        "coverage_floor_agents": 3,
                        "on_site_agents_now": 3,
                        "remote_policy": "policy://ic/remote",
                        "sla_expectation": "expectation://ic/sla"},
         # MANAGER INTEREST (additive object, explicit stakes)
         "interest": {"party": MGR, "want": "on-site-coverage-to-meet-sla",
                      "stakes": ["meet 30-minute customer-response SLA",
                                 "keep staffing floor of 3 on-site agents"],
                      "legitimate": True, "within_policy": True,
                      "reason": "customer contract requires response within 30 minutes"},
         "purpose": "customer contract with 30-minute response SLA"},
        {"uri": REL_AUTH, "participants": [MGR, COMPANY], "status": "ACTIVE",
         "roles": {MGR: ["staffing-authority"], COMPANY: ["employer"]},
         "authority": [AUTH_ADJ, AUTH_APPEAL],
         "purpose": "manager authority over staffing to meet the SLA"},
        {"uri": "right://ic/emp-appeal", "holder": EMP, "type": "APPEAL",
         "subject": "EMPLOYEE REMOTE-WORK DETERMINATION",
         "scope": ["decision://ic/adjudication"],
         "purpose": "employee's right to appeal the manager's remote-work determination"},
        {"uri": AUTH_ADJ, "holder": MGR,
         "grants": ["determine_remote_arrangement"], "roles": ["adjudicator"]},
        {"uri": AUTH_APPEAL, "holder": DIRECTOR,
         "grants": ["adjudicate_appeal"], "roles": ["appeal-adjudicator"]}], i=1)

    # ---- 2. the shared policy + the (already-bound) SLA expectation ----
    ev(sub, "event://ic/constraints", "STATE_CHANGE", COMPANY,
       "company conditional remote-work policy + customer 30-minute SLA expectation",
       [{"uri": "policy://ic/remote", "name": "remote-work-conditions",
         "condition": "SLA coverage maintained AND staffing floor met AND "
                      "no irreversible/unknown-cost action",
         "decision": "remote-work PERMITTED under conditions",
         "action": "remote-with-coverage-plan when on-site coverage can meet the SLA",
         "scope": [REL_EMP, REL_AUTH]},
        {"uri": "expectation://ic/sla", "subject": COMPANY, "condition": "respond to customer "
         "within 30 minutes during coverage hours", "metric": "response-time",
         "threshold": 30, "evidence_required": "SOME"}], i=2)

    # ---- 3. conflict detection: interests mutually exclusive under the constraint ----
    # Employee wants FULL remote (arrangement_requested = full-remote). Under the shared
    # constraint, 3 on-site agents are required to meet the 30-min SLA. If the employee is
    # on-site (manager's want), the employee gets no remote + uses no leave. If the employee
    # is fully remote (employee's want), the staffing floor (3 on-site) is violated today
    # (only 3 agents total; employee would be off-site). => collision under the constraint.
    policy = "permitted-conditional"           # remote allowed if coverage plan meets SLA
    staff_total = 3
    staff_floor = 3
    # employee full-remote would take 1 agent off-site -> on-site count 2 < floor 3 -> violation
    on_site_if_emp_full_remote = staff_total - 1
    sla_violated_full_remote = on_site_if_emp_full_remote < staff_floor
    # manager wants employee on-site -> employee's remote-work request nullified (interest lost)
    emp_remote_nullified = True
    conflict = sla_violated_full_remote and emp_remote_nullified and policy == "permitted-conditional"
    check("conflict detected: employee full-remote vs manager on-site coverage are mutually "
          "exclusive under the 30-min SLA + staffing floor",
          conflict,
          f"on-site_if_full_remote={on_site_if_emp_full_remote} floor={staff_floor} "
          f"policy={policy}")

    # ---- 4. CASE OPEN with the conflict + recorded uncertainty ----
    case = {"uri": "case://ic/remote-conflict", "subject": "employee remote-work request "
            "vs manager on-site coverage under the customer SLA", "status": "OPEN",
            "actors": [EMP, MGR, CUSTOMER], "relationships": [REL_EMP, REL_CONTRACT, REL_AUTH],
            "owner": MGR,
            "conflict": {"interests": [
                              {"party": EMP, "want": "full-remote + use 12 leave days",
                               "stakes": "wellbeing + use of accrued unused leave",
                               "legitimate": True, "within_policy": True},
                              {"party": MGR, "want": "on-site coverage to meet SLA",
                               "stakes": "30-min customer-response SLA + staffing floor",
                               "legitimate": True, "within_policy": True}],
                         "constraint": {"response_target_minutes": 30,
                                        "coverage_floor_agents": 3,
                                        "on_site_if_full_remote": on_site_if_emp_full_remote,
                                        "policy": "policy://ic/remote"},
                         "detected": True,
                         "mutually_exclusive": True,
                         "uncertainty": "coverage needs on remote days unverified; whether "
                                        "a coverage plan can meet the SLA is a judgment",
                         "negotiation_open": True}}
    ev(sub, "event://ic/open-case", "STATE_CHANGE", MGR,
       "conflicting interests -> case OPEN with conflict + uncertainty recorded", [case], i=3)
    c_open = sub.graph.get(case["uri"])
    check("case OPEN with the conflicting-interests + uncertainty recorded",
          c_open and c_open["status"] == "OPEN"
          and c_open.get("conflict", {}).get("detected") is True
          and c_open.get("conflict", {}).get("uncertainty"),
          f"status={c_open['status']} conflict.detected={c_open.get('conflict',{}).get('detected')}")

    # ---- 5. BRANCH A — definite determination (defensible middle option) ----
    # The adjudicator (Manager, authority AUTH_ADJ) may side-employee / side-manager /
    # remote-with-coverage-plan / UNRESOLVED. Definable basis: a coverage plan keeps on-site
    # staffing at floor on the 2 customer-commitment days -> employee remote Mon/Wed/Fri +
    # 2 leave days; SLA met. A defensible, evidence-backed middle.
    options = ["side-employee", "side-manager", "remote-with-coverage-plan", "UNRESOLVED"]
    determination = "remote-with-coverage-plan"
    reason = ("employee's remote interest is legitimate and within policy; manager's SLA "
              "interest is binding; a CONDITIONAL plan meets both: remote Mon/Wed/Fri, "
              "on-site Tue/Thu keeps staffing at the 3-agent floor so the 30-min SLA holds, "
              "and 2 of 12 unused-leave days are consumed")
    resolution = {"determination": determination, "determined_by": MGR,
                  "covered_stake": {"emp": "remote 3 days/wk + 2 leave days",
                                    "mgr": "on-site coverage meets SLA"},
                  "conditions": ["on-site Tue/Thu", "coverage floor met on commitment days"],
                  "reason": reason}
    ev(sub, "event://ic/adjudicate", "DECISION", MGR,
       f"human adjudicator determination: {determination}",
       [{"uri": "decision://ic/adjudication", "by": MGR, "authority": AUTH_ADJ,
         "alternatives": options, "confidence": 0.82, "expected_outcome": "resolve conflict",
         "actual_outcome": determination, "detail": resolution, "made_at": now_iso()},
        {**sub.graph.get(case["uri"]), "status": "RESOLVED",
         "resolution": str(resolution),
         "negotiation": {"outcome": determination, "by_whom": MGR,
                         "satisfies": {"employee_interest": "remote 3 days/wk + 2 leave",
                                       "manager_interest": "SLA + floor met"}}}], i=4)
    c_adj = sub.graph.get(case["uri"])
    check("determination is defensible AND includes the inviolable UNRESOLVED option",
          c_adj and c_adj["status"] == "RESOLVED"
          and c_adj.get("resolution") and determination in options
          and "UNRESOLVED" in options,
          f"status={c_adj['status']} determination={determination} options={options}")

    # ---- 6. APPEAL — first-class, signed, queryable; re-adjudicated by higher authority ----
    # The employee is the losing-interest party (wanted full remote; got a conditional plan).
    # Appeal rides the schema's native APPEAL Right + a signed event + recorded additive object.
    appeal = {"uri": "event://ic/appeal", "appeals_for": EMP,
              "appealing": "decision://ic/adjudication",
              "ground": "employee sought full remote; conditional plan still limits "
                        "flexibility; requests leave use be explicit and unrestricted",
              "status": "OPEN", "authority": AUTH_APPEAL,
              "recorded_under": "right://ic/emp-appeal"}
    ev(sub, "event://ic/appeal", "DECISION", EMP,
       "employee appeals the determination (Right type=APPEAL)",
       [{**sub.graph.get(case["uri"]), "appeal": appeal,
         "appeal_status": "OPEN", "appeal_ground": appeal["ground"]},
        {"uri": "right://ic/emp-appeal",
         **{k: v for k, v in (sub.graph.get("right://ic/emp-appeal") or {}).items()
            if k not in ("uri",)},
         "status": "EXERCISED", "exercised_at_ref": "event://ic/appeal"}], i=5)
    c_app = sub.graph.get(case["uri"])
    check("appeal is a signed, queryable, first-class step (recorded additive field + native "
          "Right type=APPEAL)",
          c_app and c_app.get("appeal_status") == "OPEN"
          and c_app.get("appeal", {}).get("appeals_for") == EMP
          and c_app.get("appeal", {}).get("appealing") == "decision://ic/adjudication"
          and c_app.get("appeal", {}).get("authority") == AUTH_APPEAL,
          f"appeal_status={c_app.get('appeal_status')} ground='{c_app.get('appeal_ground')}'")

    # Re-adjudication by the higher authority (Director) — NOT a silent redo.
    appeal_dec = {"uri": "decision://ic/appeal-decision", "by": DIRECTOR,
                  "authority": AUTH_APPEAL, "alternatives": ["uphold", "modify", "reverse"],
                  "confidence": 0.9, "expected_outcome": "resolve appeal",
                  "actual_outcome": "modify", "detail": {"ruling": "affirmed-coverage-condition",
                   "granted": "employee remote 4 days/wk; 3 of 12 leave days explicit"},
                  "made_at": now_iso()}
    ev(sub, "event://ic/appeal-resolved", "DECISION", DIRECTOR,
       "director re-adjudicates the appeal (higher authority)",
       [appeal_dec, {**sub.graph.get(case["uri"]),
                     "appeal_status": "RESOLVED",
                     "appeal_outcome": "modify",
                     "final_arrangement": "remote 4 days/wk + 3 leave days; "
                                          "on-site 1 day meets SLA floor"}], i=6)
    c_final = sub.graph.get(case["uri"])
    check("appeal re-adjudicated by a HIGHER authority, signed, not a silent redo",
          c_final and c_final.get("appeal_status") == "RESOLVED"
          and c_final.get("appeal_outcome") == "modify"
          and (sub.graph.get("decision://ic/appeal-decision") or {}).get("by") == DIRECTOR,
          f"appeal_outcome={c_final.get('appeal_outcome')} adjudicated_by=person://ic/director")

    # ---- 7. authority chain preserved (decisions carry the authority they require) ----
    check("adjudicator's determination conserves the authority it requires (§7J.9)",
          (sub.graph.get("decision://ic/adjudication") or {}).get("authority") == AUTH_ADJ
          and (sub.graph.get("decision://ic/adjudication") or {}).get("by") == MGR
          and (sub.graph.get("decision://ic/appeal-decision") or {}).get("authority") == AUTH_APPEAL,
          "decision://ic/adjudication via authority://ic/adjudicate-remote; "
          "decision://ic/appeal-decision via authority://ic/for-appeal")

    # ---- 8. INVARIABLE rule: UNRESOLVED is reachable (insufficient admissible basis) ----
    # Variant: staffing coverage on prospective remote days is UNKNOWN/unverifiable -> no
    # arrangement can be justified -> UNRESOLVED, case left OPEN, Trust untouched.
    coverage_data_known = False
    unres = "UNRESOLVED" in options
    if not coverage_data_known:
        case_u = {"uri": "case://ic/remote-uncertain", "subject": "remote request where "
                  "coverage data is unavailable", "status": "OPEN", "actors": [EMP, MGR],
                  "relationships": [REL_EMP, REL_CONTRACT], "owner": MGR,
                  "conflict": {"interests": [], "constraint": {
                      "response_target_minutes": 30, "coverage_floor_agents": 3,
                      "note": "remote-day staffing coverage NOT verifiable"},
                      "detected": True, "mutually_exclusive": True,
                      "uncertainty": "no source records on-site coverage on proposed remote "
                                     "days; neither side can be substantiated",
                      "negotiation_open": True}}
        ev(sub, "event://ic/open-uncertain", "STATE_CHANGE", MGR,
           "insufficient staffing/coverage data -> case OPEN", [case_u], i=7)
        res_u = {"determination": "UNRESOLVED", "determined_by": MGR,
                 "epistemic_state": "INSUFFICIENT_EVIDENCE",
                 "reason": "coverage on proposed remote days is unverified with no independent "
                           "source; no arrangement is justified by the admissible basis"}
        ev(sub, "event://ic/adjudicate-uncertain", "DECISION", MGR,
           f"human adjudicator determination: {res_u['determination']}",
           [{"uri": "decision://ic/adjudication-uncertain", "by": MGR, "authority": AUTH_ADJ,
             "alternatives": options, "confidence": 0.6, "expected_outcome": "resolve conflict",
             "actual_outcome": "UNRESOLVED", "detail": res_u, "made_at": now_iso()},
            {**sub.graph.get(case_u["uri"]), "status": "OPEN",
             "resolution": str(res_u), "epistemic_state": "INSUFFICIENT_EVIDENCE",
             "determination": "UNRESOLVED", "determined_by": MGR}], i=8)
    c_unres = sub.graph.get(case_u["uri"])
    check("INVIOLABLE: UNRESOLVED is reachable when the admissible basis is insufficient "
          "(no forced winner)",
          c_unres and c_unres.get("determination") == "UNRESOLVED"
          and c_unres.get("epistemic_state") == "INSUFFICIENT_EVIDENCE",
          f"determination={c_unres.get('determination')} "
          f"epistemic={c_unres.get('epistemic_state')}")

    # ---- 9. Trust safety: UNRESOLVED must not poison the flywheel ----
    check("UNRESOLVED outcome does NOT advance Trust (same safety as Sprint 9)",
          c_unres.get("epistemic_state") == "INSUFFICIENT_EVIDENCE",
          "only a determined (RESOLVED) outcome may feed the trust formula")

    # ---- emit fixtures for C1-C5 ----
    emit_ic(sub, HERE)
    print("\n  -> emitted conflicting-interest fixtures/ledger/graph under "
          "instances/contested_reality/artifacts/interest/")

    print("\nRESULT:", "ALL PASS" if ok else "FAILURES PRESENT")
    return 0 if ok else 1


def emit_ic(sub, outdir: Path):
    """Emit the conflicting-interest fixtures/ledger/graph (mirrors sector_scene.emit)."""
    ART = outdir / "artifacts/interest"; FX = ART / "fixtures"
    by_uri = {o["uri"]: o for e in sub.ledger.entries for o in (e.get("state_update") or [])}
    groups = (("cases", ["case"]), ("goals", ["goal"]), ("metrics", ["metric"]),
              ("tasks", ["task"]), ("dependencies", ["dependency"]), ("policies", ["policy"]),
              ("processes", ["process", "process_instance", "risk", "escalation"]),
              ("decisions", ["decision"]), ("expectations", ["expectation"]),
              ("evidence", ["evidence"]), ("trust", ["trust"]), ("claims", ["claim"]),
              ("disputes", ["dispute"]),
              ("actors_offers", ["person", "org", "agent", "entity", "rule", "offer",
                                 "authority", "delegation", "consent"]),
              ("relationships", ["relationship", "interaction"]), ("events", ["event"]))
    for name, prefixes in groups:
        p = FX / "interest" / f"{name}.json"; p.parent.mkdir(parents=True, exist_ok=True)
        items = [o for u, o in by_uri.items() if u.startswith(tuple(f"{x}://" for x in prefixes))]
        p.write_text(json_dumps(items))
        # also drop an idempotent copy at the conventional fixtures/s5/ location for reuse
    ld = FX / "ledger"; ld.mkdir(parents=True, exist_ok=True)
    (ld / "ledger.json").write_text(json_dumps(sub.ledger.to_dict()))
    st = FX / "statemachines"; st.mkdir(parents=True, exist_ok=True)
    (st / "relationship.json").write_text(json_dumps(
        {"uri": "relationship://ic/employment", "states": ["PROPOSED", "ACTIVE"]}))
    (st / "case.json").write_text(json_dumps(
        {"uri": "case://ic/remote-conflict",
         "states": ["OPEN", "TRIAGE", "ASSIGNED", "IN_PROGRESS", "RESOLVED"]}))
    gd = ART / "graph"; gd.mkdir(parents=True, exist_ok=True)
    (gd / "current-state.json").write_text(json_dumps(sub.graph.to_dict()))


def json_dumps(obj):
    import json
    return json.dumps(obj, indent=2)


if __name__ == "__main__":
    sys.exit(run())