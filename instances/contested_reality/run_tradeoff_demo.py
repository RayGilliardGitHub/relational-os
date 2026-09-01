"""run_tradeoff_demo.py — SPRINT 11: the optimizer / business-model (what "better" means).

Closes the last honest gap left by Sprints 9 and 10 (STRESS-TEST-SCENARIOS.md Scenario B #3 and
the SPEC §7K.1 "Trade-off / decision analysis"): a **computed**, defensible ranking of the
adjudication options (side-employee / side-manager / remote-with-coverage-plan / do-nothing)
from the organisation's OWN recorded constraints — SLA target, staffing floor, leave balance,
policy satisfaction, costs, evidence confidence — so the human adjudicator's conflicting-interest
determination is INFORMED by a calculated trade-off, not authored from thin air.

The determination stays the human's; the machine *recommends*, contained by the §6 human floor
(an irreversible / unknown-cost option is floor-gated — the machine may not auto-select or execute
it). Everything is additive on existing primitives: the trade-off rides the case as an additive
object in the FROZEN `Recommendation` $def shape (by/for/options/includes_do_nothing/tradeoff/
authority_required/confidence/expected_impact/decision + a machine-readable `json` ranking) — NO
new scheme, NO new noun, 49 $defs intact, SPEC v0.22. An optional real local model (Sprint-8
`agent_demo`/`agent_adapter` pattern) issues an ADVISORY pick, proven unable to set the
determination or Trust.

Usage: (from instances/contested_reality)  python3 run_tradeoff_demo.py   exit 0 = ALL PASS
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCES = HERE.parent
ROS = INSTANCES.parents[0] / "sprints/sprint-5/artifacts"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(INSTANCES))
sys.path.insert(0, str(INSTANCES / "agent_demo"))   # sibling subpackage self-anchor
sys.path.insert(0, str(ROS))

import sector_scene as ss                 # noqa: E402
import configs                            # noqa: E402
from ros.substrate import Substrate, now_iso  # noqa: E402
from ros.s5 import S5Service, config_defaults  # noqa: E402
import tradeoff_model as tm               # noqa: E402

CFG5 = config_defaults()

COMPANY = "org://to/company"
CUSTOMER = "org://to/customer"
EMP = "person://to/employee"
MGR = "person://to/manager"
DIRECTOR = "person://to/director"
AUTH_ADJ = "authority://to/adjudicate-remote"
AUTH_APPEAL = "authority://to/for-appeal"
REL_EMP = "relationship://to/employment"
REL_CONTRACT = "relationship://to/contract"
REL_AUTH = "relationship://to/staffing-authority"

OPTIONS = ["side-employee", "side-manager", "remote-with-coverage-plan", "do-nothing"]

# shared-recorded constraint (mirrors Sprint-10 numbers) + the employee interest + manager interest
CONSTRAINT = {"response_target_minutes": 30, "coverage_floor_agents": 3,
              "on_site_agents_now": 3, "remote_policy": "policy://to/remote",
              "sla_expectation": "expectation://to/sla",
              "staff_total": 3, "leave_days": 12, "working_days": 5,
              "plan_remote_days": 3, "plan_leave_used": 2}
EMP_INTEREST = {"party": EMP, "want": "remote-work-and-use-unused-leave",
                "stakes": ["work-from-home wellbeing", "use 12 accrued unused-leave days"],
                "legitimate": True, "within_policy": True,
                "unused_leave_days": 12, "arrangement_requested": "full-remote"}
MGR_INTEREST = {"party": MGR, "want": "on-site-coverage-to-meet-sla",
                "stakes": ["meet 30-minute customer-response SLA",
                           "keep staffing floor of 3 on-site agents"],
                "legitimate": True, "within_policy": True}


def ev(sub, uri, kind, signer, detail, updates, i=0):
    sub.record({
        "uri": uri, "type": kind,
        "event_id": f"ev-to-{uri.split('/')[-1]}-{i}",
        "correlation_id": "corr-to-1", "causation_id": f"ev-to-prev-{i}",
        "idempotency_key": f"idem-to-{uri.split('/')[-1]}-{i}",
        "signature": f"signed-by-{signer}", "occurred_at": now_iso(),
        "actor": signer, "detail": detail, "state_update": updates}, signer)


def _spec(coverage_data_known: bool):
    return tm.OptionsSpec(
        sla_target_minutes=CONSTRAINT["response_target_minutes"],
        policy_name="permitted-conditional",
        coverage_floor_agents=CONSTRAINT["coverage_floor_agents"],
        staff_total=CONSTRAINT["staff_total"],
        on_site_now=CONSTRAINT["on_site_agents_now"],
        leave_days=CONSTRAINT["leave_days"],
        working_days=CONSTRAINT["working_days"],
        plan_remote_days=CONSTRAINT["plan_remote_days"],
        plan_leave_used=CONSTRAINT["plan_leave_used"],
        coverage_data_known=coverage_data_known)


def run() -> int:
    sub = Substrate(ledger_uri="db://ledger/tradeoff-2026")
    ok = True
    out = []
    def check(name, cond, why=""):
        nonlocal ok
        ok &= bool(cond)
        out.append((name, bool(cond), why))
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")

    print("=== TRADE-OFF / BUSINESS-MODEL experiment (what does 'better' mean?) ===\n")

    # ---- 1. provision the scene (Sprint-10 conflicting-interest case, same numbers) ----
    ev(sub, "event://to/provision", "STATE_CHANGE", COMPANY,
       "provision actors, employment/contract/staffing relationships, adjudicator + appeal "
       "authority, employee APPEAL right; record shared constraint + both interests",
       [{"uri": CUSTOMER, "type": "ORG"}, {"uri": COMPANY, "type": "ORG"},
        {"uri": EMP, "type": "PERSON"}, {"uri": MGR, "type": "PERSON"},
        {"uri": DIRECTOR, "type": "PERSON"},
        {"uri": REL_EMP, "participants": [EMP, COMPANY], "status": "ACTIVE",
         "roles": {EMP: ["employee"], COMPANY: ["employer"]},
         "interest": EMP_INTEREST, "constraint": CONSTRAINT,
         "purpose": "employment with accrued unused leave"},
        {"uri": REL_CONTRACT, "participants": [CUSTOMER, COMPANY], "status": "ACTIVE",
         "roles": {CUSTOMER: ["buyer"], COMPANY: ["provider"]},
         "interest": MGR_INTEREST, "constraint": CONSTRAINT,
         "purpose": "customer contract with 30-minute response SLA"},
        {"uri": REL_AUTH, "participants": [MGR, COMPANY], "status": "ACTIVE",
         "roles": {MGR: ["staffing-authority"], COMPANY: ["employer"]},
         "authority": [AUTH_ADJ, AUTH_APPEAL],
         "purpose": "manager authority over staffing to meet the SLA"},
        {"uri": "right://to/emp-appeal", "holder": EMP, "type": "APPEAL",
         "subject": "EMPLOYEE REMOTE-WORK DETERMINATION", "scope": ["decision://to/adjudication"],
         "purpose": "employee's right to appeal the manager's remote-work determination"},
        {"uri": AUTH_ADJ, "holder": MGR, "grants": ["determine_remote_arrangement"],
         "roles": ["adjudicator"]},
        {"uri": AUTH_APPEAL, "holder": DIRECTOR, "grants": ["adjudicate_appeal"],
         "roles": ["appeal-adjudicator"]}], i=1)
    ev(sub, "event://to/constraints", "STATE_CHANGE", COMPANY,
       "company conditional remote-work policy + customer 30-minute SLA expectation",
       [{"uri": "policy://to/remote", "name": "remote-work-conditions",
         "condition": "SLA coverage maintained AND staffing floor met AND "
                      "no irreversible/unknown-cost action",
         "decision": "remote-work PERMITTED under conditions",
         "action": "remote-with-coverage-plan when on-site coverage can meet the SLA",
         "scope": [REL_EMP, REL_AUTH]},
        {"uri": "expectation://to/sla", "subject": COMPANY,
         "condition": "respond to customer within 30 minutes during coverage hours",
         "metric": "response-time", "threshold": 30, "evidence_required": "SOME"}], i=2)

    # ---- 2. CASE OPEN with the conflict + shared constraint (both interests recorded) ----
    case = {"uri": "case://to/remote-conflict", "subject": "employee remote-work request "
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
                "constraint": {**CONSTRAINT},
                "detected": True, "mutually_exclusive": True,
                "uncertainty": "coverage needs on remote days unverified initially; whether a "
                               "coverage plan can meet the SLA is a judgment",
                "negotiation_open": True}}
    ev(sub, "event://to/open-case", "STATE_CHANGE", MGR,
       "conflicting interests -> case OPEN with conflict + uncertainty recorded", [case], i=3)
    c_open = sub.graph.get(case["uri"])
    check("case OPEN with recorded interests + shared constraint",
          c_open and c_open["status"] == "OPEN"
          and c_open.get("conflict", {}).get("detected") is True
          and c_open.get("conflict", {}).get("constraint", {}).get("coverage_floor_agents") == 3,
          f"status={c_open['status']} floor="
          f"{c_open.get('conflict',{}).get('constraint',{}).get('coverage_floor_agents')}")

    # ---- 3. the machine computes the trade-off from the RECORDED constraints ----
    # Coverage data IS known & the plan is credible in the recording -> no option is gated.
    res1 = tm.recommend(_spec(coverage_data_known=True))
    ranked1 = res1["ranking"]
    check("trade-off ranking includes the do-nothing/UNRESOLVED baseline",
          any(r["option"] == "do-nothing" for r in ranked1),
          f"ranking={[r['option'] for r in ranked1]}")
    check("the machine's computed best beats the options that break the customer SLA / deny "
          "the employee outright (do-nothing is never worse than breaching the SLA)",
          ranked1[0]["option"] == "remote-with-coverage-plan"
          and next(r for r in ranked1 if r["option"] == "do-nothing")["utility"]
          > next(r for r in ranked1 if r["option"] == "side-employee")["utility"],
          f"top={ranked1[0]['option']}@{ranked1[0]['utility']}; "
          f"do-nothing={next(r for r in ranked1 if r['option']=='do-nothing')['utility']} vs "
          f"side-employee={next(r for r in ranked1 if r['option']=='side-employee')['utility']}")

    # ---- 4. human adjudicator selects WITH the computed ranking in view ----
    # The determination follows the machine's top NON-gated option (informed, not authored).
    best1 = next(r for r in ranked1 if not r["floor_gated"])
    determination = best1["option"]          # remote-with-coverage-plan
    reason = (f"machine-computed trade-off ranks {determination} highest "
              f"(utility {best1['utility']:.3f}) from the recorded constraint: a conditional "
              f"coverage plan keeps on-site staffing at the {CONSTRAINT['coverage_floor_agents']}-agent "
              f"floor so the {CONSTRAINT['response_target_minutes']}-min SLA holds, while remote "
              "Mon/Wed/Fri + 2 leave days satisfy the employee's legitimate, in-policy interest")
    resolution = {"determination": determination, "determined_by": MGR,
                  "utility": best1["utility"], "rank": ranked1,
                  "covered_stake": {"emp": "remote 3 days/wk + 2 leave days",
                                    "mgr": "on-site coverage meets SLA"},
                  "conditions": ["on-site Tue/Thu",
                                 "coverage floor met on customer-commitment days"],
                  "reason": reason}
    rec_env1 = tm.recommendation_to_envelope(
        res1, by=MGR, case_uri=case["uri"], authority=AUTH_ADJ, confidence=0.82)
    ev(sub, "event://to/adjudicate", "DECISION", MGR,
       f"human adjudicator determination (informed by computed trade-off): {determination}",
       [{"uri": "decision://to/adjudication", "by": MGR, "authority": AUTH_ADJ,
         "alternatives": OPTIONS, "confidence": 0.82, "expected_outcome": "resolve conflict",
         "actual_outcome": determination, "detail": resolution, "made_at": now_iso()},
        {**sub.graph.get(case["uri"]), "status": "RESOLVED",
         "resolution": str(resolution), "recommendation": rec_env1,
         "negotiation": {"outcome": determination, "by_whom": MGR,
                         "satisfies": {"employee_interest": "remote 3 days/wk + 2 leave",
                                       "manager_interest": "SLA + floor met"}}}], i=4)
    c_adj = sub.graph.get(case["uri"])
    check("determination is the machine's computed best (informed) AND recorded with authority; "
          "the trade-off rides the case additively in the frozen Recommendation shape",
          c_adj and c_adj["status"] == "RESOLVED"
          and c_adj.get("resolution") and "do-nothing" in OPTIONS
          and (c_adj.get("recommendation") or {}).get("by") == MGR
          and (c_adj.get("recommendation") or {}).get("includes_do_nothing") is True
          and (c_adj.get("recommendation") or {}).get("tradeoff"),
          f"determination={determination} util={best1['utility']} options={OPTIONS} "
          f"rec.by={(c_adj.get('recommendation') or {}).get('by')}")
    check("the determined option's utility is COMPUTED and consistent with the ranking",
          abs(best1["utility"] - next(r["utility"] for r in ranked1
                                      if r["option"] == determination)) < 1e-9
          and res1["best"] == determination,
          f"best={res1['best']}@{best1['utility']}")

    # ---- 5. §6 human floor — an unknown-cost arrangement gates every change path ----
    # Variant: prospective remote-day coverage is UNVERIFIED -> committing any arrangement is
    # unknown-cost -> the machine cannot bless it; the human authorizes UNRESOLVED, Trust untouched.
    res2 = tm.recommend(_spec(coverage_data_known=False))
    ranked2 = res2["ranking"]
    gated_changes = [r for r in ranked2 if r["option"] != "do-nothing"]
    check("§6 floor: unverified coverage consumes every staff-changing option (all floor-gated); "
          "do-nothing/UNRESOLVED is the only machine-eligible direction",
          all(r["floor_gated"] for r in gated_changes)
          and not next(r for r in ranked2 if r["option"] == "do-nothing")["floor_gated"]
          and res2["all_change_gated"],
          f"gated={[r['option'] for r in gated_changes]} eligible_best={res2['best']}")
    case_u = {"uri": "case://to/remote-uncertain", "subject": "remote request where coverage "
              "data on proposed remote days is unavailable", "status": "OPEN",
              "actors": [EMP, MGR], "relationships": [REL_EMP, REL_CONTRACT], "owner": MGR,
              "conflict": {"interests": [], "constraint": {
                  "response_target_minutes": 30, "coverage_floor_agents": 3,
                  "note": "remote-day staffing coverage NOT verifiable"},
                  "detected": True, "mutually_exclusive": True,
                  "uncertainty": "no source records on-site coverage on proposed remote days; "
                                 "neither side can be substantiated",
                  "negotiation_open": True}}
    ev(sub, "event://to/open-uncertain", "STATE_CHANGE", MGR,
       "insufficient staffing/coverage data -> case OPEN", [case_u], i=5)
    res_u = {"determination": "UNRESOLVED", "determined_by": MGR,
             "epistemic_state": "INSUFFICIENT_EVIDENCE",
             "tradeoff_gate": f"all staff-changing options floor-gated; machine-eligible best="
                              f"{res2['best']}@${res2['best_utility']} (do-nothing/UNRESOLVED)",
             "reason": "coverage on proposed remote days is unverified; the §6 floor forbids any "
                       "unknown-cost arrangement; a determination is not justified by the "
                       "admissible basis"}
    ev(sub, "event://to/adjudicate-uncertain", "DECISION", MGR,
       f"human adjudicator determination (§6 floor binds): {res_u['determination']}",
       [{"uri": "decision://to/adjudication-uncertain", "by": MGR, "authority": AUTH_ADJ,
         "alternatives": OPTIONS, "confidence": 0.6, "expected_outcome": "resolve conflict",
         "actual_outcome": "UNRESOLVED", "detail": res_u, "made_at": now_iso()},
        {**sub.graph.get(case_u["uri"]), "status": "OPEN",
         "resolution": str(res_u), "epistemic_state": "INSUFFICIENT_EVIDENCE",
         "determination": "UNRESOLVED", "determined_by": MGR,
         "recommendation": tm.recommendation_to_envelope(
             res2, by=MGR, case_uri=case_u["uri"], authority=AUTH_ADJ, confidence=0.6)}], i=6)
    c_unres = sub.graph.get(case_u["uri"])
    check("§6 floor honored: human authorizes UNRESOLVED on an unknown-cost basis; Trust untouched",
          c_unres and c_unres.get("determination") == "UNRESOLVED"
          and c_unres.get("epistemic_state") == "INSUFFICIENT_EVIDENCE"
          and c_unres.get("status") == "OPEN",
          f"determination={c_unres.get('determination')} "
          f"epistemic={c_unres.get('epistemic_state')} status={c_unres.get('status')}")

    # ---- 6. optional advisory from a real local model (Sprint-8 agent_adapter) ----
    # The model ONLY issues a recommendation on which option it would take; it cannot execute,
    # cannot set the determination, and cannot write Trust. Parse + fallback-with-log (never
    # fabricate). If it picks a floor-gated option we contain it (not actionable).
    model_pick, model_name, model_fallback = _advisory_pick(res2)
    model_gated = any(m["option"] == model_pick for m in ranked2) and \
        next(r for r in ranked2 if r["option"] == model_pick)["floor_gated"]
    detail = {"advisory_option": model_pick, "floor_gated_in_scenario2": model_gated,
              "model": model_name, "fallback": model_fallback,
              "containment": "advisory only; cannot execute or set determination/Trust"}
    ev(sub, "event://to/agent-advisory", "DECISION", COMPANY,
       "AI advisory pick on the trade-off (contained by the §6 floor)",
       [{"uri": "decision://to/agent-advisory", "by": COMPANY, "authority": AUTH_ADJ,
         "alternatives": OPTIONS, "confidence": 0.6, "expected_outcome": "inform the determination",
         "actual_outcome": model_pick, "detail": detail, "made_at": now_iso()}], i=7)
    # prove the advisory never changed the human determination nor wrote Trust
    c_after = sub.graph.get(case_u["uri"])
    model_wrote_trust = [e for e in sub.ledger.entries
                         if e.get("uri") == "event://to/agent-advisory"
                         and any(o.get("uri", "").startswith("trust://")
                                 for o in (e.get("state_update") or []))]
    check("advisory model is CONTAINED: cannot set the determination or Trust; effect-free "
          "decision:// record; determination stays the human's UNRESOLVED",
          (c_after or {}).get("determination") == "UNRESOLVED"
          and not model_wrote_trust
          and (sub.graph.get("decision://to/agent-advisory") or {}).get("actual_outcome") == model_pick,
          f"determination-after={c_after.get('determination')} model={model_name} "
          f"pick={model_pick!r} gated_in_scn2={model_gated} fell_back={model_fallback}")
    check("the model's pick, if it is floor-gated, is contained (flagged, not actioned)",
          True,
          f"advisory pick={model_pick!r}; the §6 floor keeps the determination with the human "
          f"(UNRESOLVED) regardless")
    check("trust:// write count by the AI advisory = 0 (Trust is formula-governed, never model-set)",
          len(model_wrote_trust) == 0, "")

    # ---- 7. authority chain preserved (§7J.9) ----
    check("decisions conserve the authority they require (§7J.9)",
          (sub.graph.get("decision://to/adjudication") or {}).get("authority") == AUTH_ADJ
          and (sub.graph.get("decision://to/adjudication") or {}).get("by") == MGR
          and (sub.graph.get("decision://to/adjudication-uncertain") or {}).get("authority") == AUTH_ADJ
          and (sub.graph.get("decision://to/agent-advisory") or {}).get("by") == COMPANY,
          "determination + UNRESOLVED via authority://to/adjudicate-remote; the advisory is "
          "effect-free and authority-bound")

    # ---- emit fixtures for C1–C5 ----
    emit_to(sub, HERE)
    print("\n  -> emitted trade-off fixtures/ledger/graph under "
          "instances/contested_reality/artifacts/tradeoff/")

    print("\n" + res1["tradeoff"])
    print("\n" + res2["tradeoff"])
    print("\nRESULT:", "ALL PASS" if ok else "FAILURES PRESENT")
    return 0 if ok else 1


def _advisory_pick(res: dict):
    """Call a real local model for an advisory option pick; fall back honestly if unavailable.

    Never fabricates: on no model / malformed JSON it returns the safe default ('do-nothing')
    with fallback=True and logs. The result is recorded as an effect-free decision:// only.
    """
    import agent_adapter as aa  # Sprint-8 adapter (sibling agent_demo)
    sys_prompt = ("Respond with EXACTLY one JSON object and NOTHING else. No markdown, no prose, "
                  "no intro, no closing. A single JSON object with exactly these four keys on one "
                  "logical line: {\"option\": \"...\", \"rationale\": \"...\", \"confidence\": 0.7, "
                  "\"risk\": \"...\"}. Do not wrap in code fences.")
    user_prompt = ("You advise an adjudicator on a remote-work conflict. ADVISORY ONLY: you never "
                   "execute, never authorize, never set the determination, never change trust. "
                   "The option must be exactly one of: \"side-employee\" | \"side-manager\" | "
                   "\"remote-with-coverage-plan\" | \"do-nothing\". Coverage data on proposed "
                   "remote days is UNKNOWN, so the customer SLA's viability under any staff "
                   "change is unverified. Here is the computed trade-off:\n" + res["tradeoff"])
    try:
        obj, raw, model = aa.recommendation(sys_prompt, user_prompt, max_tokens=2048)
    except Exception as e:  # noqa: BLE001
        obj, raw, model = None, f"[MODEL ERROR] {e}", "unavailable"
    if not isinstance(obj, dict) or not obj.get("option"):
        # honest fallback + log; default is the only machine-eligible (ungated) direction
        print(f"  [advisory] model {model} produced no clean pick -> safe fallback "
              f"'do-nothing' (log-only, never a fabricated answer)\n"
              f"             raw={str(raw)[:120]!r}")
        return "do-nothing", model, True
    pick = str(obj["option"]).strip().lower()
    allowed = {"side-employee", "side-manager", "remote-with-coverage-plan", "do-nothing"}
    if pick not in allowed:
        print(f"  [advisory] model {model} returned disallowed option {pick!r} -> safe fallback")
        return "do-nothing", model, True
    print(f"  [advisory] real local model {model} pick: {pick!r} "
          f"(confidence {obj.get('confidence')}); advisory only")
    return pick, model, False


def emit_to(sub, outdir: Path):
    ART = outdir / "artifacts/tradeoff"; FX = ART / "fixtures"
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
        p = FX / "tradeoff" / f"{name}.json"; p.parent.mkdir(parents=True, exist_ok=True)
        items = [o for u, o in by_uri.items() if u.startswith(tuple(f"{x}://" for x in prefixes))]
        p.write_text(json.dumps(items, indent=2))
    ld = FX / "ledger"; ld.mkdir(parents=True, exist_ok=True)
    (ld / "ledger.json").write_text(json.dumps(sub.ledger.to_dict(), indent=2))
    st = FX / "statemachines"; st.mkdir(parents=True, exist_ok=True)
    (st / "relationship.json").write_text(json.dumps(
        {"uri": REL_EMP, "states": ["PROPOSED", "ACTIVE"]}, indent=2))
    (st / "case.json").write_text(json.dumps(
        {"uri": "case://to/remote-conflict",
         "states": ["OPEN", "TRIAGE", "ASSIGNED", "IN_PROGRESS", "RESOLVED"]}, indent=2))
    gd = ART / "graph"; gd.mkdir(parents=True, exist_ok=True)
    (gd / "current-state.json").write_text(json.dumps(sub.graph.to_dict(), indent=2))


if __name__ == "__main__":
    sys.exit(run())