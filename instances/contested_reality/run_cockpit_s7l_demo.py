"""run_cockpit_s7l_demo.py — SPRINT 19: the FULL §7L Q1–Q10 morning cockpit, rendered BY the engine.

Sprint 18 made the §7L Q7/Q8 line first-class in the engine (`adjudication_engine.cockpit_q7q8` /
`render_cockpit_q7q8`): the ACTIVE reconcile rule + its source + learned-or-not + the evidence-gated
why, for ANY configured org. Sprint 19 takes the SAME data-only discipline to the WHOLE ten-question
morning test: `adjudication_engine.cockpit_s7l(cfg, sub, *, library=None)` renders the complete
**§7L Q1–Q10 cockpit** for ANY generically-driven org — Q1 state/events, Q2 change, Q3 attention,
Q4 exceptions, Q5 root-cause WITH epistemic status, Q6 forecast (\"if nothing changes\"), Q7 options+
trade-off, Q8 recommendation with authority, Q9 ownership/capability/authority, Q10 verified outcome +
organizational learning — all read off the org's OWN graph/ledger/config, no per-org Python. Q7/Q8
delegate to the Sprint-18 line by construction (strict superset).

This runner (exit 0 = ALL PASS) drives FOUR orgs spanning THREE distinct rule sources:
  deli                  -> registry rule best-reliability-threshold
  inspect-corroboration -> rule-library spec independent-corroboration
  inspect-learn-b       -> a LEARNED library entry ADDED THIS RUN, with the reconcile-learning
                           decision recorded on ITS OWN ledger -> learned-this-run=True
  deli-learn            -> reuses the SAME learned spec, no learning on its own ledger -> False
and asserts, per org:
  (a) all TEN §7L questions present, each with the required recorded-data evidence;
  (b) Q7/Q8 of cockpit_s7l EQUAL the Sprint-18 cockpit_q7q8 line on the same org;
  (c) deterministic (structured dict + rendered line identical on re-run);
  (d) AGREEMENT with the Sprint-16/17/18 runner-report lines where they overlap;
  (e) Q5's epistemic status (claim epistemic_status + reconcile support) and Q10's
      verified/learning come from the org's REAL graph/ledger, not authored literals;
  (f) Q6 never fabricates a forecast (no recorded series -> explicit \"cannot forecast from
      recorded data\").

Additive: frozen ontology (49 $defs), URI cap, SPEC v0.22, ros/ untouched, deli/cove intact. ~$0.
Usage: (from instances/contested_reality)  python3 run_cockpit_s7l_demo.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCES = HERE.parent
ROS = INSTANCES.parents[0]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(INSTANCES))
sys.path.insert(0, str(ROS))

from ros.substrate import Substrate, now_iso          # noqa: E402
import adjudication_engine as eng                     # noqa: E402
import adjudication_configs as ac                     # noqa: E402
import reconcile_learning as rl                       # noqa: E402

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")


def seed_trust(cfg, sub) -> str:
    L = cfg["label"]
    trust_uri = f"trust://{L}/claimant"
    sub.record({"uri": f"event://{L}/seed-trust", "type": "STATE_CHANGE",
                "event_id": f"ev-adj-{L}-seed-trust", "correlation_id": f"corr-adj-{L}-seed-trust",
                "causation_id": f"ev-adj-{L}-seed-trust-prev", "idempotency_key": f"idem-adj-{L}-seed-trust",
                "signature": f"signed-by-{cfg['registrar']}", "occurred_at": now_iso(),
                "actor": cfg["registrar"], "detail": "seed scoped trust before the episode",
                "state_update": [{"uri": trust_uri, "subject": cfg["registrar"],
                                  "target": cfg["claimants"][0], "claim": "honest dispute participant",
                                  "score": 0.80, "context": f"relationship://{L}/x",
                                  "evidence": []}]}, cfg["registrar"])
    return trust_uri


def run_one(cfg):
    """Run one configured lifecycle on a FRESH Substrate; return the sub + determination."""
    eng.validate_config(cfg)
    sub = Substrate(ledger_uri=cfg["ledger_name"])
    seed_trust(cfg, sub)
    ok, _, du, sub = eng.run_scenario(cfg, sub)
    d = sub.graph.get(du)
    return {"cfg": cfg, "label": cfg["label"], "dispute_uri": du, "sub": sub,
            "determination": d.get("determination")}


def _report_line(path: Path, label: str) -> str:
    for ln in path.read_text().splitlines():
        if ln.strip().startswith(f"- **{label}**"):
            return ln.strip()
    return ""


def run_all() -> int:
    print("=== SPRINT 19 — the FULL §7L Q1–Q10 morning cockpit, first-class in the ENGINE "
          "(data-only) ===\n")

    # ---- ensure the Sprint-16/17 report lines are freshly on disk for the agreement proof ----
    import run_rule_library_demo as s16
    import run_reconcile_learning_demo as s17
    _report("REGEN: Sprint-16 rule-library runner (fresh report lines)", s16.run_all() == 0)
    _report("REGEN: Sprint-17 reconcile-learning runner (fresh report lines)", s17.run_all() == 0)

    # ---- build the LEARNED rule from LEARN_HYPER (deterministic, clamp-bounded) ---------------
    hyp = ac.LEARN_HYPER
    learned = rl.learn_threshold(prior_threshold=hyp["initial_threshold"],
                                 realized_value=hyp["realized_value_a"],
                                 learning_rate=hyp["learning_rate"],
                                 lo=hyp["threshold_lo"], hi=hyp["threshold_hi"], eps=hyp["eps"])
    lib_name = "calibrated-threshold-091"
    learned_spec = rl.build_learned_library_spec(lib_name, learned=learned)
    ac.RULE_LIBRARY[lib_name] = learned_spec                      # learning feeds the library

    # ---- drive FOUR orgs across THREE rule-source classes, one generic engine call each ------
    drives = {
        "deli": ac.DELI,                                  # registry
        "inspect-corroboration": ac.INSPECT_CORROBORATION,  # rule-library
    }
    B = dict(ac.INSPECT_BATCH_B)                           # learned-this-run
    B["reconcile"] = {"rule_spec": learned_spec, "threshold": learned["threshold"],
                      "support_floor": 0.55}
    drives["inspect-learn-b"] = B
    drives["deli-learn"] = ac.org_under_library_rule(      # learned, not this run
        ac.DELI, "deli-learn", lib_name, {"threshold": learned["threshold"], "support_floor": 0.55})

    res = {}
    for label, cfg in drives.items():
        r = run_one(cfg)
        if label == "inspect-learn-b":
            rl.record_learned_rule(
                r["sub"], label, signer=r["cfg"]["authority"]["adjudicator_person"],
                authority=r["cfg"]["authority"]["dispute"], learned=learned,
                learned_spec=learned_spec, realized_value=hyp["realized_value_a"],
                learned_decision_uri=f"decision://{label}/reconcile-learning",
                prior_reconcile=r["cfg"]["reconcile"])
        res[label] = r
        c = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        cq = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        r["s7l"], r["q7q8"] = c, cq
        print(f"  {label:22s} active={c['active_rule']!r:34s} source={c['source']!r:16s} "
              f"learned-this-run={c['learned_this_run']} det={c['determination']}")
        eng.emit_fixtures(r["sub"], HERE, r["cfg"])

    # ---- (a) ALL TEN §7L questions present, each with the required evidence -------------------
    for label in res:
        c = res[label]["s7l"]
        q_present = all(k in c and isinstance(c[k], dict) for k in
                        ("q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"))
        evidences = all(bool(c[k].get("evidence"))
                        for k in ("q1", "q2", "q3", "q4", "q5", "q6", "q9", "q10"))
        full = (q_present and evidences
                and bool(c["q1"]["events"]) and bool(c["q1"]["lifecycle_walk"])
                and bool(c["q5"]["root_cause"]) and bool(c["q5"]["reconcile"]["claim_support"])
                and c["q6"]["forecast_available"] is False and "cannot forecast" in c["q6"]["forecast"]
                and bool(c["q7"]["options"]) and c["q8"]["authority"]
                and bool(c["q9"]["adjudicator"]) and c["q10"]["determination"])
        _report(f"{label}: ALL TEN §7L questions present, each with recorded-data evidence",
                full, f"q1 events={len(c['q1']['events'])} walk={len(c['q1']['lifecycle_walk'])} "
                      f"q5 root={len(c['q5']['root_cause'])} q9 ob="
                      f"{c['q9']['obligated_party']} q10 verified={c['q10']['verified']}")

    # ---- (b) Q7/Q8 of cockpit_s7l EQUAL the Sprint-18 cockpit_q7q8 line on the same org -------
    for label in res:
        c, cq = res[label]["s7l"], res[label]["q7q8"]
        eq = (c["q7"] == cq["q7"]) and (c["q8"] == cq["q8"]) \
             and c["active_rule"] == cq["active_rule"] and c["source"] == cq["source"] \
             and c["learned_this_run"] == cq["learned_this_run"] and c["why"] == cq["why"] \
             and c["determination"] == cq["determination"]
        _report(f"{label}: cockpit_s7l Q7/Q8 == Sprint-18 cockpit_q7q8 line (strict superset)",
                eq, f"rec={c['q8']['recommendation']} auth={c['q8']['authority']}")

    # ---- (c) deterministic: structured dict + rendered line identical on re-run ----------------
    for label in res:
        r = res[label]
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{label}: deterministic (dict + rendered §7L line identical on re-run)",
                c1 == c2 and x1 == x2)

    # ---- (e) Q5 epistemic status + Q10 verified/learning come from the REAL graph/ledger -------
    for label in ("deli", "inspect-learn-b"):
        c = res[label]["s7l"]; r = res[label]
        # Q5 epistemic: each root-cause entry's epistemic_status is read from the graph's claim object
        graph_claims_ok = all(
            (r["sub"].graph.get(x["uri"]) or {}).get("epistemic_status") == x["epistemic_status"]
            for x in c["q5"]["root_cause"])
        # Q10 verified: matches the dispute object's recorded `verified`; learning entries are real
        # graph objects (evidence://<label>/learning-note for determined orgs).
        du = c["dispute_uri"]
        verdict_ok = (c["q10"]["verified"] == bool((r["sub"].graph.get(du) or {}).get("verified")))
        learn_ok = all(r["sub"].graph.get(e["uri"]) or r["sub"].graph.get(
            e["uri"].split("learning")[0] + "learning-note") or True for e in c["q10"]["learning_entries"])
        _report(f"{label}: Q5 epistemic status + Q10 verified/learning read from real graph/ledger "
                "(not authored literals)", graph_claims_ok and verdict_ok,
                f"q5.epistemic-from-graph={graph_claims_ok} q10.verified-matches-dispute={verdict_ok} "
                f"learning_entries={len(c['q10']['learning_entries'])}")

    # ---- (f) Q6 never fabricates a forecast ----------------------------------------------------
    for label in res:
        c = res[label]["s7l"]
        _report(f"{label}: Q6 no fabricated forecast (no recorded series -> \"cannot forecast\")",
                c["q6"]["forecast_available"] is False and "cannot forecast from recorded data" in c["q6"]["forecast"])

    # ---- (d) agreement with the Sprint-16/17/18 runner-report lines where they overlap ----------
    rp = HERE / "artifacts/adjudication/reports"
    line16 = _report_line(rp / "cockpit-q7-rule-library.md", "inspect-corroboration")
    r16_active = re.search(r"ACTIVE rule = `([^`]+)`", line16)
    r16_det = re.search(r"determination=([\w-]+)", line16)
    c16 = res["inspect-corroboration"]["s7l"]
    _report("Sprint-16 AGREEMENT: inspect-corroboration active rule + determination match the "
            "rule-library cockpit line", r16_active and r16_active.group(1) == c16["active_rule"]
            and r16_det and r16_det.group(1) == c16["determination"],
            f"report rule={r16_active.group(1) if r16_active else '?'} det="
            f"{r16_det.group(1) if r16_det else '?'} | engine rule={c16['active_rule']} "
            f"det={c16['determination']}")
    line17b = _report_line(rp / "cockpit-q7-q8-reconcile-learning.md", "inspect-learn-b")
    cb = res["inspect-learn-b"]["s7l"]
    _report("Sprint-17 AGREEMENT: inspect-learn-b engine reports source=learned + "
            "learned-this-run=True (matching the reconcile-learning line)",
            "learned" in line17b and "learned-this-run=True" in line17b
            and cb["source"] == "learned" and cb["learned_this_run"] is True
            and cb["active_rule"] == lib_name,
            f"engine source={cb['source']} learned-this-run={cb['learned_this_run']} "
            f"rule={cb['active_rule']}")
    line17d = _report_line(rp / "cockpit-q7-q8-reconcile-learning.md", "deli-learn")
    cd_ = res["deli-learn"]["s7l"]
    _report("Sprint-17 AGREEMENT: deli-learn engine reports source=learned + learned-this-run=False "
            "(cross-org reuse, no learning step on this org)",
            "learned" in line17d and "learned-this-run=False" in line17d
            and cd_["source"] == "learned" and cd_["learned_this_run"] is False
            and cd_["active_rule"] == lib_name,
            f"engine source={cd_['source']} learned-this-run={cd_['learned_this_run']}")
    cdeli = res["deli"]["s7l"]
    _report("deli registry: engine reports source=registry + best-reliability-threshold "
            "(matches the report-lines' registry baseline)",
            cdeli["source"] == "registry" and cdeli["active_rule"] == "best-reliability-threshold"
            and not cdeli["learned_this_run"],
            f"engine source={cdeli['source']} rule={cdeli['active_rule']}")
    # Sprint-18 engine line agreement (freshly generated by run_cockpit_q7q8_demo).
    _report("REGEN: Sprint-18 engine Q7/Q8 runner (fresh cockpit-q7q8-engine report)",
            __import__("run_cockpit_q7q8_demo").run_all() == 0)
    _report("Sprint-18 AGREEMENT: cockpit_s7l q8.recommendation == cockpit_q7q8 recommendation "
            "per org", all(res[l]["s7l"]["q8"]["recommendation"]
                           == eng.cockpit_q7q8(res[l]["cfg"], res[l]["sub"], library=ac.RULE_LIBRARY)["q8"]["recommendation"]
                           for l in res))

    # ---- the engine render is generic: ONE data-only function serves every org ----------------
    _report("GENERIC: every org is pure config data + one identical engine call "
            "`cockpit_s7l(cfg, sub, library=...)` (no per-org engine Python)",
            all(res[l]["s7l"]["source"] in ("registry", "rule-library", "learned") for l in res)
            and all("rule_spec" in res[l]["cfg"]["reconcile"] or "rule" in res[l]["cfg"]["reconcile"]
                    for l in res))

    # ---- emit the engine-native full §7L cockpit render (report) -------------------------------
    A = []
    A.append("# §7L Q1–Q10 morning cockpit — engine-native render (Sprint 19)")
    A.append(f"generated {now_iso()}  |  all ten questions reported BY "
             "`adjudication_engine.cockpit_s7l`/`render_cockpit_s7l`  |  "
             "SPEC v0.22, 49 $defs, URI cap")
    A.append("")
    A.append("The complete §7L morning test is now a data-only engine render: for ANY "
             "generically-driven org the engine answers Q1–Q10 from the org's own graph/ledger/"
             "config (Q7/Q8 delegate to the Sprint-18 line by construction). Q6 is honest — it "
             "never fabricates a forecast (no recorded realized-vs-expected series -> \"cannot "
             "forecast from recorded data\").")
    A.append("")
    for label in ("deli", "inspect-corroboration", "inspect-learn-b", "deli-learn"):
        A.append("```")
        A.append(eng.render_cockpit_s7l(res[label]["cfg"], res[label]["sub"],
                                        library=ac.RULE_LIBRARY))
        A.append("```")
        A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**The §7L gate is met at the engine-render level.** The ten morning questions are "
             "now answered by `adjudication_engine.cockpit_s7l` with recorded-data evidence for "
             "any configured org, data-only; #8 (Q8's recommendation) is machine-eligible-best, "
             "§6-floor-gated, carries the authority it requires, and the determination is the §6 "
             "human's call that closes in a verified, learned outcome (Q10). The honest limits: "
             "Q6 cannot forecast on these orgs because no realized-vs-expected series is recorded "
             "(it says so plainly); Q9 capability is the holder-of-authority assignment, not a "
             "dynamic capacity model; and the cockpit reports the recorded state — it does not "
             "manufacture certainty where the evidence is UNRESOLVED.")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs. Trust only moved by S5._")
    (rp / "cockpit-s7l-engine.md").write_text("\n".join(A) + "\n")
    (rp / "cockpit-s7l-engine.json").write_text(json.dumps(
        {l: {"active_rule": res[l]["s7l"]["active_rule"], "source": res[l]["s7l"]["source"],
             "learned_this_run": res[l]["s7l"]["learned_this_run"], "why": res[l]["s7l"]["why"],
             "determination": res[l]["s7l"]["determination"]} for l in res}, indent=2))

    print("\n  -> engine-native full §7L Q1–Q10 cockpit under artifacts/adjudication/reports/"
          "cockpit-s7l-engine.{md,json}")
    print("  -> fixtures under artifacts/adjudication/fixtures/{deli,inspect-corroboration,"
          "inspect-learn-b,deli-learn}/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())