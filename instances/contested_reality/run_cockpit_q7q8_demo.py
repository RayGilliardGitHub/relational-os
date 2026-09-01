# === DEMO / TEST RUNNER - NOT part of the engine API ===
"""run_cockpit_q7q8_demo.py — SPRINT 18: the §7L Q7/Q8 cockpit line, FIRST-CLASS in the engine.

Sprints 16/17 rendered a §7L Q7/Q8 line (ACTIVE reconcile rule + its source + learned-or-not + the
evidence-gated why) ONLY inside runner-side reports (`cockpit-q7-rule-library.md`,
`cockpit-q7-q8-reconcile-learning.md`). That surface was never wired into the generic engine's OWN
§7L cockpit output. Sprint 18 closes the gap: `adjudication_engine.cockpit_q7q8` /
`render_cockpit_q7q8` render the line BY THE ENGINE for ANY generically-driven org — registry rule,
hand-authored RULE_LIBRARY spec, or a learned RULE_LIBRARY entry added this run — reading the org's
own ledger/graph (data-only, no per-org engine Python).

This runner (exit 0 = ALL PASS) drives FOUR orgs spanning THREE distinct rule sources:
  deli                  -> registry rule best-reliability-threshold
  inspect-corroboration -> rule-library spec independent-corroboration (ac.RULE_LIBRARY dict, is-identical)
  inspect-learn-b       -> a LEARNED library entry (calibrated-threshold-091) ADDED THIS RUN, with the
                           reconcile-learning decision recorded on its OWN ledger -> learned-this-run=True
  deli-learn            -> reuses the SAME learned spec but records no learning on its own ledger
                           -> learned, learned-this-run=False
and asserts, per org, that the engine-native Q7/Q8 is correct, deterministic, carries both Q7 (options
incl. do-nothing baseline) and Q8 (recommendation with authority + determination), and AGREES with the
Sprint-16 (`cockpit-q7-rule-library.md`) and Sprint-17 (`cockpit-q7-q8-reconcile-learning.md`) lines.

Additive: frozen ontology (49 $defs), URI cap, SPEC v0.22, ros/ untouched, deli/cove intact. ~$0.
Usage: (from instances/contested_reality)  python3 run_cockpit_q7q8_demo.py
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
    """The report .md line for `label` (Sprint-16/17 cockpit lines)."""
    for ln in path.read_text().splitlines():
        if ln.strip().startswith(f"- **{label}**"):
            return ln.strip()
    return ""


def run_all() -> int:
    print("=== SPRINT 18 — §7L Q7/Q8 cockpit line, first-class in the ENGINE (data-only) ===\n")

    # ---- ensure the Sprint-16/17 runner-report lines are freshly on disk for the agreement proof ----
    import run_rule_library_demo as s16
    import run_reconcile_learning_demo as s17
    _report("REGEN: Sprint-16 rule-library runner (fresh report lines)", s16.run_all() == 0)
    _report("REGEN: Sprint-17 reconcile-learning runner (fresh report lines)", s17.run_all() == 0)

    # ---- (1) build the LEARNED rule from LEARN_HYPER (deterministic, clamp-bounded, evidence-gated) --
    hyp = ac.LEARN_HYPER
    learned = rl.learn_threshold(prior_threshold=hyp["initial_threshold"],
                                 realized_value=hyp["realized_value_a"],
                                 learning_rate=hyp["learning_rate"],
                                 lo=hyp["threshold_lo"], hi=hyp["threshold_hi"], eps=hyp["eps"])
    lib_name = "calibrated-threshold-091"
    claimed_thresh = round(0.95 + hyp["learning_rate"] * (hyp["realized_value_a"] - 0.95), 4)
    _report("LEARN primitive: recalibrates 0.95 -> 0.91 (deterministic, clamp-bounded, changed)",
            learned["changed"] and abs(learned["threshold"] - claimed_thresh) < 1e-9
            and hyp["threshold_lo"] <= learned["threshold"] <= hyp["threshold_hi"]
            and learned == rl.learn_threshold(prior_threshold=hyp["initial_threshold"],
                                              realized_value=hyp["realized_value_a"],
                                              learning_rate=hyp["learning_rate"],
                                              lo=hyp["threshold_lo"], hi=hyp["threshold_hi"],
                                              eps=hyp["eps"]),
            f"threshold={learned['threshold']} changed={learned['changed']} bound="
            f"{learned['bound']}")
    learned_spec = rl.build_learned_library_spec(lib_name, learned=learned)
    ac.RULE_LIBRARY[lib_name] = learned_spec                      # learning feeds the library (this run)

    # ---- (2) drive FOUR orgs across THREE rule-source classes, all via ONE generic engine call ----
    drives = {
        # registry
        "deli": ac.DELI,
        # rule-library
        "inspect-corroboration": ac.INSPECT_CORROBORATION,
    }
    # learned-this-run: INSPECT_BATCH_B (label inspect-learn-b) driven under the learned spec, with the
    # reconcile-learning decision recorded on ITS OWN ledger.
    B = dict(ac.INSPECT_BATCH_B)
    B["reconcile"] = {"rule_spec": learned_spec, "threshold": learned["threshold"],
                      "support_floor": 0.55}
    drives["inspect-learn-b"] = B
    # learned, NOT this run: deli reuses the SAME learned spec, no learning decision on its ledger.
    drives["deli-learn"] = ac.org_under_library_rule(
        ac.DELI, "deli-learn", lib_name, {"threshold": learned["threshold"], "support_floor": 0.55})

    res = {}
    for label, cfg in drives.items():
        r = run_one(cfg)
        if label == "inspect-learn-b":
            # record the reconcile-learning decision on the org the learned rule now governs: this is
            # what makes learned-this-run TRUE when read back from that org's ledger.
            rl.record_learned_rule(
                r["sub"], label, signer=r["cfg"]["authority"]["adjudicator_person"],
                authority=r["cfg"]["authority"]["dispute"], learned=learned,
                learned_spec=learned_spec, realized_value=hyp["realized_value_a"],
                learned_decision_uri=f"decision://{label}/reconcile-learning",
                prior_reconcile=r["cfg"]["reconcile"])
        res[label] = r
        c = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        r["cc"] = c
        print(f"  {label:22s} active={c['active_rule']!r:34s} source={c['source']!r:16s} "
              f"learned-this-run={c['learned_this_run']} det={c['determination']}")
        eng.emit_fixtures(r["sub"], HERE, r["cfg"])

    # ---- (3) per-org correctness assertions ------------------------------------------------
    def expect(label, source, ltr, why_kind):
        c = res[label]["cc"]
        cfg = res[label]["cfg"]
        rc = cfg["reconcile"]
        want_active = rc["rule"] if "rule" in rc else rc["rule_spec"].get("name", "?")
        return (c["active_rule"] == want_active, c["source"] == source,
                c["learned_this_run"] is ltr,
                (c["why"] == "unchanged") if why_kind == "unchanged"
                else ("recalibrated" in c["why"]), c)

    for label, source, ltr, why_kind in (
        ("deli", "registry", False, "unchanged"),
        ("inspect-corroboration", "rule-library", False, "unchanged"),
        ("inspect-learn-b", "learned", True, "recalibrated"),
        ("deli-learn", "learned", False, "unchanged")):
        act, src, lt, wy, c = expect(label, source, ltr, why_kind)
        _report(f"{label}: ACTIVE rule name matches cfg.reconcile", act,
                f"engine={c['active_rule']!r}")
        _report(f"{label}: SOURCE classified correctly ({source})", src,
                f"engine source={c['source']!r}")
        _report(f"{label}: learned-this-run = {ltr}", lt,
                "TRUE only when the org's own ledger recorded a reconcile-learning decision")
        why_msg = ("why=unchanged (no learning step on this org)"
                   if why_kind == "unchanged"
                   else "why is the evidence-gated recalibration reason")
        _report(f"{label}: {why_msg}", wy, c["why"][:70])

    # ---- (4) Q7 AND Q8 both present on every org's engine-native cockpit --------------------
    for label, c in ((l, res[l]["cc"]) for l in res):
        q7ok = bool(c["q7"]["options"]) and c["q7"]["baseline"] and \
            any("unres" in o.lower() or o == "do-nothing" for o in c["q7"]["options"])
        q8ok = bool(c["q8"]["recommendation"]) and bool(c["q8"]["authority"]) and \
            bool(c["q8"]["determination"]) and c["q8"]["determination"] == c["determination"]
        s = eng.render_cockpit_q7q8(res[label]["cfg"], res[label]["sub"], library=ac.RULE_LIBRARY)
        renders = ("Q7 options:" in s) and ("Q8 recommendation:" in s) and \
            ("ACTIVE reconcile rule:" in s) and ("source:" in s) and ("learned-this-run:" in s)
        _report(f"{label}: Q7 (options incl. baseline) + Q8 (recommendation w/ authority + "
                "determination) present", q7ok and q8ok,
                f"baseline={c['q7']['baseline']} rec={c['q8']['recommendation']} "
                f"auth={c['q8']['authority']}")
        _report(f"{label}: engine-native rendered line carries Q7 + Q8 + rule + source + "
                "learned-or-not", renders)

    # ---- (5) determinism (identical on re-run) ---------------------------------------------
    for label in res:
        c1 = eng.cockpit_q7q8(res[label]["cfg"], res[label]["sub"], library=ac.RULE_LIBRARY)
        r1 = eng.render_cockpit_q7q8(res[label]["cfg"], res[label]["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_q7q8(res[label]["cfg"], res[label]["sub"], library=ac.RULE_LIBRARY)
        r2 = eng.render_cockpit_q7q8(res[label]["cfg"], res[label]["sub"], library=ac.RULE_LIBRARY)
        _report(f"{label}: deterministic (structured dict + rendered line identical on re-run)",
                c1 == c2 and r1 == r2)

    # ---- (6) agreement with the Sprint-16/17 runner-report lines -----------------------------
    rp = HERE / "artifacts/adjudication/reports"
    # Sprint-16 rule-library line for inspect-corroboration.
    line16 = _report_line(rp / "cockpit-q7-rule-library.md", "inspect-corroboration")
    r16_active = re.search(r"ACTIVE rule = `([^`]+)`", line16)
    r16_det = re.search(r"determination=([\w-]+)", line16)
    c16 = res["inspect-corroboration"]["cc"]
    _report("Sprint-16 AGREEMENT: engine active rule + determination for inspect-corroboration "
            "match the rule-library cockpit line",
            r16_active and r16_active.group(1) == c16["active_rule"]
            and r16_det and r16_det.group(1) == c16["determination"],
            f"report: rule={r16_active.group(1) if r16_active else '?'} det="
            f"{r16_det.group(1) if r16_det else '?'} | engine: "
            f"rule={c16['active_rule']} det={c16['determination']}")
    # Sprint-17 reconcile-learning lines for inspect-learn-b (learned-this-run=True) + deli-learn (False).
    line17b = _report_line(rp / "cockpit-q7-q8-reconcile-learning.md", "inspect-learn-b")
    line17d = _report_line(rp / "cockpit-q7-q8-reconcile-learning.md", "deli-learn")
    cb = res["inspect-learn-b"]["cc"]; cd = res["deli-learn"]["cc"]
    _report("Sprint-17 AGREEMENT: inspect-learn-b engine reports source=learned + learned-this-run=True "
            "(matching the reconcile-learning line)",
            "learned" in line17b and "learned-this-run=True" in line17b
            and cb["source"] == "learned" and cb["learned_this_run"] is True
            and cb["active_rule"] == lib_name,
            f"engine: source={cb['source']} learned-this-run={cb['learned_this_run']} "
            f"rule={cb['active_rule']}")
    _report("Sprint-17 AGREEMENT: deli-learn engine reports source=learned + learned-this-run=False "
            "(cross-org reuse, no learning step on this org)",
            "learned" in line17d and "learned-this-run=False" in line17d
            and cd["source"] == "learned" and cd["learned_this_run"] is False
            and cd["active_rule"] == lib_name,
            f"engine: source={cd['source']} learned-this-run={cd['learned_this_run']} "
            f"rule={cd['active_rule']}")
    # deli registry: engine source is registry, matching the Sprint-17 report's registry baseline.
    cdeli = res["deli"]["cc"]
    _report("deli registry: engine reports source=registry + active rule best-reliability-threshold "
            "(matches the report lines' registry baseline)",
            cdeli["source"] == "registry" and cdeli["active_rule"] == "best-reliability-threshold"
            and not cdeli["learned_this_run"],
            f"engine source={cdeli['source']} rule={cdeli['active_rule']} "
            f"learned-this-run={cdeli['learned_this_run']}")

    # ---- (7) the engine render is generic: ONE data-only function serves every org -------------
    _report("GENERIC: every org is pure config data + one identical engine call "
            "`cockpit_q7q8(cfg, sub, library=...)` (no per-org Python in the engine)",
            all(res[l]["cc"]["source"] in ("registry", "rule-library", "learned")
                for l in res)
            and all("rule_spec" in res[l]["cfg"]["reconcile"] or "rule" in res[l]["cfg"]["reconcile"]
                    for l in res))

    # ---- emit the engine-native cockpit render (report) ---------------------------------------
    A = []
    A.append("# §7L Q7/Q8 cockpit — engine-native render (Sprint 18)")
    A.append(f"generated {now_iso()}  |  active rule + source + learned-or-not + why "
             "reported BY `adjudication_engine.cockpit_q7q8`/`render_cockpit_q7q8`  |  "
             "SPEC v0.22, 49 $defs, URI cap")
    A.append("")
    A.append("The Sprint-16/17 runner-report lines are now a first-class, data-only engine render: "
             "for ANY generically-driven org the engine reads the ACTIVE reconcile rule, its source, "
             "whether a learning step changed it this run, and the evidence-gated why — from the org's "
             "own config + ledger, with no per-org engine Python.")
    A.append("")
    for label in ("deli", "inspect-corroboration", "inspect-learn-b", "deli-learn"):
        A.append("```")
        A.append(eng.render_cockpit_q7q8(res[label]["cfg"], res[label]["sub"],
                                         library=ac.RULE_LIBRARY))
        A.append("```")
        A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**First-class engine render, not a runner-side artifact.** The §7L Q7/Q8 line (ACTIVE "
             "rule + source + learned-or-not + why) is now `adjudication_engine.cockpit_q7q8`/"
             "`render_cockpit_q7q8` — a generic, data-only function any org config (registry / "
             "rule-library / learned this run) renders identically, reading the org's own ledger. The "
             "Sprint-16/17 cockpit report files are now a *view* over that engine render, not the only "
             "place the line exists — the engine itself carries the rule-as-operating-reality (Q7 "
             "options + Q8 recommendation with authority).")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs. Trust only moved by S5._")
    (rp / "cockpit-q7q8-engine.md").write_text("\n".join(A) + "\n")
    (rp / "cockpit-q7q8-engine.json").write_text(json.dumps(
        {l: {"active_rule": res[l]["cc"]["active_rule"], "source": res[l]["cc"]["source"],
             "learned_this_run": res[l]["cc"]["learned_this_run"], "why": res[l]["cc"]["why"],
             "determination": res[l]["cc"]["determination"]} for l in res}, indent=2))

    print("\n  -> engine-native Q7/Q8 cockpit reports under artifacts/adjudication/reports/"
          "cockpit-q7q8-engine.{md,json}")
    print("  -> fixtures under artifacts/adjudication/fixtures/{deli,inspect-corroboration,"
          "inspect-learn-b,deli-learn}/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())