"""run_agent_demo.py — REAL local-LLM agent inside the RelationalOS chain (Sprint 8).

Builds a sector scene with the verified sector_scene builder, THEN runs an **agent overlay**
that takes a REAL local Ollama model's judgement for (a) the #8 recommendation and (b) the
rally-evidence verify classification. Both are recorded as **effect-free signed `decision://`
records** (advisory only); the agent never executes an ACTION and never sets its own Trust. The
deterministic `update_trust` formula is applied over the model-classified evidence on a graph
clone to prove the model feeds the formula but does not decide its own score. The §6 floor order
(escalate < human < release) is re-asserted.

Usable as a library: `run_agent_sector(label)` returns (ok, sub, rec, vrec, logs). The module
`__main__` runs the `tech` sector as a self-contained demo.

Usage:  (from instances/)  python3 agent_demo/run_agent_demo.py      exit 0 = ALL PASS
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
sys.path.insert(0, str(ROS))

import sector_scene as ss            # noqa: E402
import configs                       # noqa: E402
from ros.substrate import Substrate, now_iso  # noqa: E402
from ros.bol import project_on_time, project_trust  # noqa: E402
from ros.s5 import S5Service, config_defaults  # noqa: E402
import agent_adapter as aa           # noqa: E402

CFG5 = config_defaults()


def env_context(cfg, sub) -> str:
    """The live evidence given to the model — built from the scene's actual ledger/graph."""
    on, total = project_on_time(sub)
    rate = round(on / total, 3) if total else 1.0
    g_trust = project_trust(sub, cfg["partner_good"], sub._meta["uris"]["prel"])
    l_trust = project_trust(sub, cfg["partner_lag"], sub._meta["uris"]["prel"])
    ex = sub._meta["s51_exception"]
    return "\n".join([
        f"COMPANY: {cfg['company_name']} ({cfg['sector']} sector, fictional)",
        f"OUTCOME CLASS: committed {cfg['outcome']}",
        f"LEDGER-BASED ON-TIME: {on}/{total} = {rate:.3f}  (target {ex['expected']}; variance {ex['variance']})",
        f"SCOPED TRUST good partner: {round(g_trust,3) if g_trust else 'n/a'}  laggard: {round(l_trust,3) if l_trust else 'n/a'}",
        f"EXCEPTION: {ex['significance']}; root status {ex.get('root_cause_status','UNKNOWN')}",
        f"ALLOWED OPTIONS: [re-balance to partner_good] [gate the laggard] [do nothing]",
    ])


def rally_evidence(sub) -> dict | None:
    """Find the rallied (good-partner) outcome evidence in the graph for the verify classifier."""
    L = sub._meta["cfg"]["label"]
    for obj in sub.graph.objects.values():
        if obj.get("uri", "").startswith(f"evidence://{L}/") and "routed" in obj["uri"]:
            return obj
    return None


def run_agent_sector(label: str) -> tuple[bool, object, dict, dict, dict]:
    """Run the real-LLM agent pathway for one sector. Returns (all_ok, sub, rec, vrec, logs)."""
    cfg = configs.SECTORS[label]
    checks: list[tuple[str, bool, str]] = []
    print(f"  [{label:6}] {cfg['company_name']:22} ({cfg['sector']}) — building scene + agent overlay …")

    # ---- build the verified base scene ----
    sub = Substrate(ledger_uri=f"db://ledger/agent-{label}-2026")
    ss.build_scene(cfg, sub)
    L, U = cfg["label"], sub._meta["uris"]
    s5 = S5Service(sub, label=L)

    # ---- inject the model's #8 recommendation (advisory) ----
    rec_sys = json.loads((HERE / "prompts/recommend.json").read_text())["role"]
    rec_user = (json.loads((HERE / "prompts/recommend.json").read_text())["task"]
                + "\n\n" + env_context(cfg, sub))
    obj, raw, model = aa.recommendation(rec_sys, rec_user, max_tokens=2048)
    used_model = obj is not None
    default_option = cfg["rec_option"][:60]
    rec = {
        "option": (obj or {}).get("option", f"[fallback] {default_option}"),
        "rationale": (obj or {}).get("rationale", "model produced no structured output; safe default used"),
        "confidence": float((obj or {}).get("confidence", 0.85)),
        "risk": (obj or {}).get("risk", "unknown"),
        "_model": model,
        "_fallback": not used_model,
    }
    rec["confidence"] = max(0.0, min(1.0, rec["confidence"]))
    sub.record({
        "uri": f"event://{L}/agent-recommend", "type": "DECISION",
        "event_id": f"ev-{L}-agent-rec", "correlation_id": f"corr-{L}-agent",
        "causation_id": f"ev-{L}-s5-case-closed", "idempotency_key": f"idem-{L}-agent-rec",
        "signature": f"signed-by-{U['ops']}", "occurred_at": now_iso(), "actor": U["ops"],
        "detail": f"AI (#8) recommendation from live ledger evidence (model={model})",
        "state_update": [{"uri": f"decision://{L}/agent-recommend", "by": U["ops"],
                          "authority": U["auth"], "alternatives": [rec["option"], "gate laggard", "do nothing"],
                          "confidence": rec["confidence"], "expected_outcome": "re-balance to verified on-time partner",
                          "actual_outcome": rec["option"], "detail": rec, "made_at": now_iso()}]},
        U["ops"])
    checks.append((f"model produced structured #8 recommendation from live evidence",
                   used_model, f"model={model} option={rec['option'][:50]!r} conf={rec['confidence']:.2f}"))

    # ---- inject the model's evidence-verify classification (advisory) ----
    ev = rally_evidence(sub)
    v_sys = json.loads((HERE / "prompts/verify.json").read_text())["role"]
    v_user = (json.loads((HERE / "prompts/verify.json").read_text())["task"]
              + "\n\n" + json.dumps(ev, indent=2))
    vobj, vraw, vmodel = aa.recommendation(v_sys, v_user, max_tokens=2048)
    v_used = vobj is not None
    vrec = {
        "on_time": bool((vobj or {}).get("on_time", True)),
        "confidence": float((vobj or {}).get("confidence", 0.9)),
        "procedure": (vobj or {}).get("procedure", "anchored-timestamp"),
        "note": (vobj or {}).get("note", "no structured output; safe default"),
        "_model": vmodel,
        "_fallback": not v_used,
    }
    vrec["confidence"] = max(0.0, min(1.0, vrec["confidence"]))
    sub.record({
        "uri": f"event://{L}/agent-verify", "type": "DECISION",
        "event_id": f"ev-{L}-agent-verify", "correlation_id": f"corr-{L}-agent",
        "causation_id": f"ev-{L}-s5-case-closed", "idempotency_key": f"idem-{L}-agent-ver",
        "signature": f"signed-by-{U['ops']}", "occurred_at": now_iso(), "actor": U["ops"],
        "detail": f"AI evidence classification of rally outcome (model={vmodel})",
        "state_update": [{"uri": f"decision://{L}/agent-verify", "by": U["ops"],
                          "authority": U["auth"], "alternatives": ["on_time", "late"],
                          "confidence": vrec["confidence"], "expected_outcome": "on_time",
                          "actual_outcome": "on_time" if vrec["on_time"] else "late",
                          "detail": vrec, "made_at": now_iso()}]},
        U["ops"])
    checks.append((f"model produced structured evidence classification",
                   v_used, f"model={vmodel} on_time={vrec['on_time']} conf={vrec['confidence']:.2f} proc={vrec['procedure']}"))

    # ---- prove Trust update is deterministic over the model-CLASSIFIED evidence ----
    clone = sub.clone_graph()
    sub2 = Substrate(ledger_uri=f"db://ledger/agent-clone-{label}"); sub2.graph = clone
    ev_score = vrec["confidence"]
    prior = None
    for o in clone.objects.values():
        if o.get("uri", "").startswith("trust://") and o.get("target") == cfg["partner_good"]:
            prior = float(o.get("score"))
            break
    if prior is None:
        prior = 0.6
    from types import SimpleNamespace
    vr = SimpleNamespace(
        on_time=vrec["on_time"], degree=ev_score,
        evidence_uri=ev["uri"], outcome_uri=f"event://{L}/outcome-routed-{cfg['rallied'][0]}",
        provider=cfg["partner_good"])
    s5b = S5Service(sub2, label=L)
    trust = s5b.update_trust(subject=cfg["company"], target=cfg["partner_good"], claim=cfg["claim"],
                             context=U["prel"], verify=vr, evidence_score=ev_score, i=9000,
                             alpha=CFG5["alpha"], expectation=CFG5["expectation"],
                             recency=CFG5["recency"], signer=U["ops"])
    outcome = 1.0 if vr.on_time else 0.0
    t_expected = max(0.0, min(1.0, prior + CFG5["alpha"] * (outcome - CFG5["expectation"]) * ev_score * CFG5["recency"]))
    checks.append(("Trust update is the deterministic formula over model-classified evidence (model cannot self-set)",
                   abs(trust["score"] - round(t_expected, 3)) < 1e-9,
                   f"T={prior:.3f} + {CFG5['alpha']}*({outcome:.0f}-{CFG5['expectation']})*{ev_score:.2f}*{CFG5['recency']} -> {trust['score']:.3f}"))

    # ---- control properties ----
    entries = sub.ledger.entries

    def idx(uri):
        for n, e in enumerate(entries):
            if e.get("uri") == uri:
                return n
        return -1

    i_esc = idx(f"event://{L}/s5-escalate")
    i_hum = idx(f"event://{L}/owner-human")
    i_rel = idx(f"event://{L}/action-release")
    checks.append(("§6 floor order holds with the real agent present (escalate < human < release)",
                   0 <= i_esc < i_hum < i_rel, f"[{i_esc} < {i_hum} < {i_rel}]"))

    def action_after(uri):
        for n, e in enumerate(entries):
            if e.get("uri") == uri and e.get("type") == "ACTION":
                return n
        return -1

    rec_act = action_after(f"event://{L}/agent-recommend")
    ver_act = action_after(f"event://{L}/agent-verify")
    checks.append(("AI overlay (recommend + verify) is advisory-only: never an ACTION",
                   rec_act == -1 and ver_act == -1,
                   f"recommend ACTION idx={rec_act}, verify ACTION idx={ver_act} (both must be -1)"))
    agent_trust_writes = [e for e in entries if e.get("actor") == U["ops"]
                          and any(o.get("uri", "").startswith("trust://") for o in (e.get("state_update") or []))]
    checks.append(("agent never wrote a trust:// object (trust is formula-governed)",
                   len(agent_trust_writes) == 0, ""))

    logs = {"recommend": rec, "recommend_raw": raw, "verify": vrec, "verify_raw": vraw,
            "evidence_context": env_context(cfg, sub), "checks": checks}
    ok = all(c[1] for c in checks)
    return ok, sub, rec, vrec, logs


def main() -> int:
    label = "tech"
    print(f"=== REAL-LLM AGENT demo: {configs.SECTORS[label]['company_name']} "
          f"({configs.SECTORS[label]['sector']}) ===\n")
    ok, sub, rec, vrec, logs = run_agent_sector(label)
    for name, cok, why in logs["checks"]:
        print(f"  [{'PASS' if cok else 'FAIL'}] {name}{'  — ' + why if why else ''}")
    L = configs.SECTORS[label]["label"]
    ss.emit(sub, HERE)
    (HERE / "model-log.json").write_text(json.dumps(logs, indent=2))
    print("\n  -> fixtures/ledger/graph + model-log.json under instances/agent_demo/artifacts/")
    print("RESULT:", "ALL PASS" if ok else "FAILURES PRESENT")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())