# === DEMO / TEST RUNNER - NOT part of the engine API ===
"""run_rule_authoring_demo.py — SPRINT 15: the declarative rule-AUTHORING layer.

Sprint 14 made the reconciliation rule *selection* + *parameters* config through a registry of pure
functions, but the rule BODY was still a Python function authored in `adjudication_engine.py` (a
genuinely new rule needed a new registry function). Sprint 15 makes the rule BODY a piece of CONFIG
TEXT: `cfg["reconcile"]["rule_spec"]` is a small declaring dict (admissible evidence kinds, the
scalar to extract, an optional recency decay, and one of a FIXED aggregation vocabulary) that the
engine *compiles* into the same pure support map the registry runs — so a NEW rule is added wholly
as data, with NO engine Python authored for it.

This runner drives ONE org (`inspect`) under registry rules AND under the equivalent spec-authored
rules, and proves:
  (a) PARITY  — `strict-anchor-only` and `recency-weighted-threshold` re-expressed as specs produce
      the EXACT same per-claim support + dispute verdicts as the registry versions (a spec is the
      same engine, not a different one).
  (b) NEW RULE — `majority-of-sources` (a genuinely NEW rule authored ONLY as a spec dict — never a
      registry function) drives a real lifecycle and produces a DISTINCT support map and a real,
      DIFFERENT verdict: inspect flips from best-rel's DETERMINED `rework-partial-credit` to
      UNRESOLVED, purely from a rule that entered the system through config text.

Usage: (from instances/contested_reality)  python3 run_rule_authoring_demo.py
exit 0 = ALL PASS. Deterministic local Python, ~$0. Additive: frozen ontology (49 $defs), URI cap,
SPEC v0.22, ros/ untouched. Trust only ever moved by the deterministic S5 formula; verification of
the enforcement of the compiler's strictness (loud rejection of an unknown op / bad kind) is
included below.
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

from ros.substrate import Substrate, now_iso          # noqa: E402
import adjudication_engine as eng                     # noqa: E402
import adjudication_configs as ac                     # noqa: E402

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
                                  "score": 0.80, "context": "relationship://%s/x" % L,
                                  "evidence": []}]}, cfg["registrar"])
    return trust_uri


def run_one(cfg):
    """Run one configured episode; return the per-claim reconcile verdict + determination."""
    L = cfg["label"]
    eng.validate_config(cfg)
    sub = Substrate(ledger_uri=cfg["ledger_name"])
    trust_uri = seed_trust(cfg, sub)
    ep_ok, _, du, _ = eng.run_scenario(cfg, sub)
    d_main = sub.graph.get(du)
    rec = eng.reconcile(sub, cfg)
    ranked = eng.rank(cfg); best = eng.machine_eligible_best(ranked)
    t = sub.graph.get(trust_uri)
    det_dec = sub.graph.get(f"decision://{L}/determination") or {}
    eng.emit_fixtures(sub, HERE, cfg)
    return {"cfg": cfg, "label": L, "ep_ok": ep_ok, "rec": rec, "determination": d_main.get("determination"),
            "d_main": d_main, "trust": t.get("score"), "authority": det_dec.get("authority"),
            "best": best, "ranked": ranked}


def render_report(results: list[dict], parity: list[dict]) -> None:
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = []
    ap = A.append
    ap("# Sprint 15 — user-authorable RULE-authoring DSL: rules as CONFIG TEXT")
    ap(f"generated {now_iso()}  |  one org (`inspect`), registry rules vs spec-authored rules, SAME engine")
    ap("")
    ap("A rule declared as `cfg['reconcile']['rule_spec']` (config text) compiles to the same pure "
      "support function a registry rule runs; a NEW rule enters the system as data alone.")
    ap("")
    by = {r["label"]: r for r in results}
    ap("| label | rule source | spec aggregate | passed | failed | conflict | uncertainty | determination |")
    ap("|---|---|---|---|---|---|---|---|")
    order = ["inspect-best", "inspect-anchor", "inspect-rec", "inspect-anchor-spec",
             "inspect-rec-spec", "inspect-majority"]
    for lab in order:
        r = by[lab]
        rc = r["cfg"]["reconcile"]
        if "rule_spec" in rc:
            src = "SPEC"; agg = rc["rule_spec"]["aggregate"]
        else:
            src = "registry"; agg = rc["rule"]
        sup = r["rec"]["claim_support"]
        def state(u):
            if u in r["rec"]["determined"]: return "DETERMINED"
            if u in r["rec"]["disputed"]: return "DISPUTED"
            return "UNDETERMINED"
        ap(f"| `{lab}` | {src} | `{agg}` | {state('claim://inspect/passed')} "
           f"({sup.get('claim://inspect/passed')}) | {state('claim://inspect/failed')} "
           f"({sup.get('claim://inspect/failed')}) | {r['rec']['conflict']} | "
           f"{r['rec']['uncertainty']} | **{r['determination']}** |")
    ap("")
    ap("Parity (identifies whether the spec is a DIFFERENT engine):")
    ap("")
    ap("| spec label | spec support | matches registry label | identical? |")
    ap("|---|---|---|---|")
    for p in parity:
        ap(f"| `{p['spec_label']}` | {p['sup']} | `{p['reg_label']}` | {p['identical']} |")
    ap("")
    ap("§7L cockpit Q7 extra line: the ACTIVE evidence-reconciliation rule for `inspect-majority` "
      f"is `majority-of-sources`, and it is **spec-authored** "
      f"(aggregate=`majority`, source_threshold=0.92) → {by['inspect-majority']['determination']}.")
    ap("")
    ap("_Additive report; frozen ontology, SPEC v0.22, 49 $defs. Trust untouched by the engine; "
      "the §6 human's determination keeps its authority; determinism asserted per run._")
    (rp / "rule-authoring.md").write_text("\n".join(A))
    (rp / "rule-authoring.json").write_text(json.dumps(
        [{"label": r["label"], "reconcile": json.loads(json.dumps(r["cfg"]["reconcile"], default=str)),
          "claim_support": r["rec"]["claim_support"], "conflict": r["rec"]["conflict"],
          "uncertainty": r["rec"]["uncertainty"], "determination": r["determination"]}
         for r in results], indent=2, default=str))


def run_all() -> int:
    print("=== USER-AUTHORABLE RULE-AUTHORING DSL — registry rules vs spec-authored rules ===\n")

    # registry reference variants (Sprint 14) — the ground truth a spec must reproduce
    registry_cfgs = {v["label"]: v for v in ac.RULE_VARIANTS}
    results = {}
    for lab in ("inspect-best", "inspect-anchor", "inspect-rec"):
        r = run_one(registry_cfgs[lab]); results[lab] = r
        print(f"  REGISTRY {lab:18s} → determined={r['rec']['determined']} "
              f"determination={r['determination']}")

    # spec-authored variants — anchor & rec must REPRODUCE the registry (parity); majority is NEW
    for lab in ("inspect-anchor-spec", "inspect-rec-spec", "inspect-majority"):
        cfg = next(c for c in ac.SPEC_AUTHORED_RULES if c["label"] == lab)
        r = run_one(cfg); results[lab] = r
        agg = cfg["reconcile"]["rule_spec"]["aggregate"]
        print(f"  SPEC-ONLY {lab:24s} agg={agg:12s} → determined={r['rec']['determined']} "
              f"determination={r['determination']}")

    # ---- PARITY: a spec-authored rule reproduces the registry verdict EXACTLY ----------------
    _report("SPEC == REGISTRY: strict-anchor spec reproduces registry support (passed/failed)",
            results["inspect-anchor-spec"]["rec"]["claim_support"]
            == results["inspect-anchor"]["rec"]["claim_support"],
            f"spec={results['inspect-anchor-spec']['rec']['claim_support']} "
            f"reg={results['inspect-anchor']['rec']['claim_support']}")
    _report("SPEC == REGISTRY: strict-anchor spec reproduces the registry dispute verdict",
            (results["inspect-anchor-spec"]["rec"]["determined"],
             results["inspect-anchor-spec"]["rec"]["disputed"],
             results["inspect-anchor-spec"]["rec"]["uncertainty"])
            == (results["inspect-anchor"]["rec"]["determined"],
                results["inspect-anchor"]["rec"]["disputed"],
                results["inspect-anchor"]["rec"]["uncertainty"]))
    _report("SPEC == REGISTRY: recency spec reproduces registry support (passed/failed)",
            results["inspect-rec-spec"]["rec"]["claim_support"]
            == results["inspect-rec"]["rec"]["claim_support"],
            f"spec={results['inspect-rec-spec']['rec']['claim_support']} "
            f"reg={results['inspect-rec']['rec']['claim_support']}")
    _report("SPEC == REGISTRY: recency spec reproduces the registry dispute verdict",
            (results["inspect-rec-spec"]["rec"]["determined"],
             results["inspect-rec-spec"]["rec"]["disputed"],
             results["inspect-rec-spec"]["rec"]["uncertainty"])
            == (results["inspect-rec"]["rec"]["determined"],
                results["inspect-rec"]["rec"]["disputed"],
                results["inspect-rec"]["rec"]["uncertainty"]))

    # ---- a spec is a real rule, not a flag: it drives a full lifecycle ------------------------
    _report("SPEC-AUTHORED RULES DRIVE REAL LIFECYCLES (3 spec labels each end in a lawful terminal state)",
            all((results[lab]["d_main"].get("determination") == "UNRESOLVED" and results[lab]["d_main"].get("status") == "OPEN")
                or (results[lab]["d_main"].get("status") == "RESOLVED"
                    and results[lab]["d_main"].get("epistemic_state") == "RESOLVED_DETERMINED")
                for lab in ("inspect-anchor-spec", "inspect-rec-spec", "inspect-majority")))

    # ---- the genuinely NEW spec-only rule: distinct support + a real, different verdict --------
    maj = results["inspect-majority"]["rec"]["claim_support"]
    best_sup = results["inspect-best"]["rec"]["claim_support"]
    anch_sup = results["inspect-anchor"]["rec"]["claim_support"]
    rec_sup = results["inspect-rec"]["rec"]["claim_support"]
    _report("NEW RULE IS REAL: majority-of-sources support map is distinct from EVERY registry rule",
            maj != best_sup and maj != anch_sup and maj != rec_sup and results["inspect-majority"]["rec"]["claim_support"]
            == {"claim://inspect/passed": 0.5, "claim://inspect/failed": 0.0},
            f"majority={maj} vs best={best_sup} anchor={anch_sup} rec={rec_sup}")
    _report("NEW RULE AUTHORED ONLY AS CONFIG TEXT entered the system (never a registry function)",
            "rule_spec" in results["inspect-majority"]["cfg"]["reconcile"]
            and "rule" not in results["inspect-majority"]["cfg"]["reconcile"])
    _report("NEW RULE CHANGES THE VERDICT: majority → UNRESOLVED, best-rel → rework-partial-credit",
            results["inspect-majority"]["determination"] == "UNRESOLVED"
            and results["inspect-best"]["determination"] == "rework-partial-credit",
            f"majority={results['inspect-majority']['determination']} "
            f"vs best-rel={results['inspect-best']['determination']}")
    _report("NEW RULE'S REASON IS DISTINCT: majority reports NO claim disputed + uncertainty=True "
            "(no decisive majority for either side)",
            results["inspect-majority"]["rec"]["uncertainty"]
            and results["inspect-majority"]["rec"]["disputed"] == [])

    # ---- invariants hold for every spec-authored rule -----------------------------------------
    for lab in ("inspect-anchor-spec", "inspect-rec-spec", "inspect-majority"):
        r = results[lab]
        _report(f"{lab} TRUST UNCHANGED by the engine (score 0.80 preserved)", r["trust"] == 0.80)
        _report(f"{lab} RANKING DETERMINISTIC (identical on re-run)", eng.rank(r["cfg"]) == r["ranked"])
        _report(f"{lab} AUTHORITY PRESERVED (determination carries the configured authority)",
                (r["authority"] == r["cfg"]["authority"]["dispute"]) or r["determination"] == "UNRESOLVED",
                f"authority={r['authority']}")
        _report(f"{lab} NO FORCED WINNER: UNRESOLVED is an available resolution",
                any("unres" in o.lower() or o == "do-nothing" for o in r["cfg"]["options"]))

    # ---- the compiler is strict: an out-of-vocabulary spec fails loudly (proves this is a real
    #      declarative language, not a permissive flag) -----------------------------------------
    def expect_reject(spec, frag):
        try:
            eng.compile_rule_spec(spec)
            return False, "(no error raised)"
        except ValueError as e:
            return frag in str(e), str(e)
    ok1, why1 = expect_reject({"aggregate": "bayesian-update"}, "unknown aggregate op")
    _report("COMPILER STRICT: an out-of-vocabulary op (`bayesian-update`) is rejected loudly",
            ok1, why1)
    ok2, why2 = expect_reject({"aggregate": "max", "value_field": "reliability",
                               "admissible_kinds": ["REASONED"]}, "unknown evidence kind")
    _report("COMPILER STRICT: an unknown evidence kind is rejected loudly", ok2, why2)

    # ---- determinism: compiling the same spec twice yields identical support ------------------
    s1 = eng.compile_rule_spec(ac.SPEC_MAJORITY_SPEC["reconcile"]["rule_spec"])
    s2 = eng.compile_rule_spec(ac.SPEC_MAJORITY_SPEC["reconcile"]["rule_spec"])
    _report("COMPILER DETERMINISTIC: same spec compiles to the same verified dict", s1 == s2)

    parity = [
        {"spec_label": "inspect-anchor-spec", "reg_label": "inspect-anchor",
         "sup": results["inspect-anchor-spec"]["rec"]["claim_support"],
         "identical": results["inspect-anchor-spec"]["rec"]["claim_support"] == anch_sup},
        {"spec_label": "inspect-rec-spec", "reg_label": "inspect-rec",
         "sup": results["inspect-rec-spec"]["rec"]["claim_support"],
         "identical": results["inspect-rec-spec"]["rec"]["claim_support"] == rec_sup},
    ]
    render_report(list(results.values()), parity)

    print("\n  -> emitted fixtures under artifacts/adjudication/fixtures/inspect-{anchor,rec,}"
          "{,-spec}/ + inspect-majority/")
    print("  -> rule-authoring report under artifacts/adjudication/reports/rule-authoring.{md,json}")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())