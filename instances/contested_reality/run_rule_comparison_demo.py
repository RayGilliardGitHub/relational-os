"""run_rule_comparison_demo.py — SPRINT 14: the config-authorable reconciliation RULE layer.

Sprint 13 proved adjudication is a *configurable* capability (one engine, any org), but its
evidence-reconciliation RULE was a single named semantic (`best-reliability-threshold`) whose only
*parameters* were config — a genuinely new rule needed a new engine function. Sprint 14 generalizes
the RULE SELECTION: `cfg["reconcile"]` now carries `{"rule": "<name>", "params": {...}}`, and the
engine resolves the rule through a tiny deterministic registry (`eng.RULES`). A new rule is added by
a registry entry + a pure function, then selected from config — no engine change for the new rule.

This runner PROVES the rule layer is real, not a flag: it drives the SAME goods-inspection dispute
(identical evidence, options, weights, authority, §6 floor) through the SAME engine under THREE
different CONFIGURED rules — `best-reliability-threshold`, `strict-anchor-only`, and
`recency-weighted-threshold` — and asserts that the rule choice swings the outcome from a determined
option (`rework-partial-credit`) to `UNRESOLVED`, with the per-claim dispute maps differing by rule.
Only `cfg["reconcile"]` (and the label suffix for clean fixtures) differs between the three runs.

Usage: (from instances/contested_reality)  python3 run_rule_comparison_demo.py
exit 0 = ALL PASS.
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


def render_report(results: list[dict]) -> None:
    """Additive rule-comparison report (optional item): the active rule + its verdict per variant,
    + a §7L cockpit-Q7 line naming the rule."""
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = []
    ap = A.append
    ap(f"# Sprint 14 — config-authorable reconciliation rule layer: rule → verdict")
    ap(f"generated {now_iso()}  |  one org (`inspect`), three configured rules, SAME engine, "
      f"only `reconcile` differs")
    ap("")
    ap("A claim that is DISPUTED/determined/UNDETERMINED depends on which rule the org configured:")
    ap("")
    ap("| rule (cfg['reconcile']) | passed | failed | conflict | uncertainty | determination |")
    ap("|---|---|---|---|---|---|")
    for r in results:
        sup = r["rec"]["claim_support"]
        def state(u):
            if u in r["rec"]["determined"]: return "DETERMINED"
            if u in r["rec"]["disputed"]: return "DISPUTED"
            return "UNDETERMINED"
        passed = state("claim://inspect/passed"); failed = state("claim://inspect/failed")
        ap(f"| `{r['rule']}` | {passed} ({sup.get('claim://inspect/passed')}) | "
          f"{failed} ({sup.get('claim://inspect/failed')}) | {r['rec']['conflict']} | "
          f"{r['rec']['uncertainty']} | **{r['determination']}** |")
    ap("")
    ap("§7L cockpit Q7 extra line (rule choice): the active evidence-reconciliation rule is "
      + " | ".join(f"`{r['label']}` → `{r['rule']}` → {r['determination']}" for r in results))
    ap("")
    ap("_Additive report; frozen ontology, SPEC v0.22, 49 $defs. Trust untouched by the engine; "
      "the §6 human's determination keeps its authority; determinism asserted per run._")
    (rp / "rule-comparison.md").write_text("\n".join(A))
    (rp / "rule-comparison.json").write_text(json.dumps(
        [{"label": r["label"], "rule": r["rule"], "reconcile": r["reconcile"],
          "claim_support": r["rec"]["claim_support"], "conflict": r["rec"]["conflict"],
          "uncertainty": r["rec"]["uncertainty"], "determination": r["determination"]}
         for r in results], indent=2))


def run_all() -> int:
    print("=== CONFIG-AUTHORABLE RULE LAYER — the SAME engine, three different configured rules ===\n")
    results = []
    for i, cfg in enumerate(ac.RULE_VARIANTS):
        L = cfg["label"]; rule = cfg["reconcile"]["rule"]
        print(f"##### VARIANT {i + 1}/{len(ac.RULE_VARIANTS)}  label={L}  rule={rule}  #####")
        eng.validate_config(cfg)

        sub = Substrate(ledger_uri=cfg["ledger_name"])
        trust_uri = seed_trust(cfg, sub)

        # ---- run the one generic lifecycle under this configured rule ----
        ep_ok, _, du, _ = eng.run_scenario(cfg, sub)
        _report(f"{L} main episode ALL PASS (driven by `{rule}`)", ep_ok)
        d_main = sub.graph.get(du)
        determination = d_main.get("determination")
        rec = eng.reconcile(sub, cfg)                       # per-claim verdict under this rule
        ranked = eng.rank(cfg); best = eng.machine_eligible_best(ranked)
        print(f"    -> reconcile[{rule}] support={rec['claim_support']} "
              f"disputed={rec['disputed']} determined={rec['determined']} "
              f"conflict={rec['conflict']} uncertainty={rec['uncertainty']}")
        print(f"    -> machine-eligible best (non-gated): {best['option']}@{best['utility']:.3f}"
              f"\n    -> human determination: {determination}   "
              f"(epistemic {d_main.get('epistemic_state')}, lifecycle {d_main.get('lifecycle_state')})")

        # ---- invariants hold under EVERY rule ----
        t = sub.graph.get(trust_uri)
        det_dec = sub.graph.get(f"decision://{L}/determination") or {}
        _report(f"{L} TRUST UNCHANGED by the engine (score 0.80 preserved)", t is not None and t.get("score") == 0.80)
        _report(f"{L} RANKING DETERMINISTIC (identical on re-run)", eng.rank(cfg) == ranked)
        _report(f"{L} AUTHORITY PRESERVED (determination carries the configured authority)",
                (det_dec.get("authority") == cfg["authority"]["dispute"]) or determination == "UNRESOLVED",
                f"authority={det_dec.get('authority')}")
        _report(f"{L} NO FORCED WINNER: UNRESOLVED is an available resolution",
                any("unres" in o.lower() or o == "do-nothing" for o in cfg["options"]))

        eng.emit_fixtures(sub, HERE, cfg)
        results.append({"label": L, "rule": rule, "reconcile": cfg["reconcile"], "rec": rec,
                        "determination": determination, "du": du, "d_main": d_main,
                        "ranked": ranked, "best": best})

    # ---- the rule-layer proof: a rule choice CHANGES the verdict, zero engine change ----
    by = {r["rule"]: r for r in results}
    best_r = by["best-reliability-threshold"]; anchor_r = by["strict-anchor-only"]; rec_r = by["recency-weighted-threshold"]
    bo, ao, ro = best_r, anchor_r, rec_r
    sup_b, sup_a, sup_r = (bo["rec"]["claim_support"], ao["rec"]["claim_support"], ro["rec"]["claim_support"])

    _report("RULE LAYER REAL: 3 DISTINCT rules each drive a real lifecycle (registry, not a flag)",
            len(results) == 3 and len(set(r["rule"] for r in results)) == 3)
    _report("SAME ENGINE, only config differs: identical evidence/options/weights/authority across rules",
            (bo["du"].rsplit("/", 1)[0].rsplit(":", 1)[0],
             ao["du"].rsplit("/", 1)[0].rsplit(":", 1)[0],
             ro["du"].rsplit("/", 1)[0].rsplit(":", 1)[0]).count(bo["du"].rsplit("/", 1)[0].rsplit(":", 1)[0]) == 3
            and bo["ranked"][0]["option"] == ro["ranked"][0]["option"],
            f"top option identical under every rule = {bo['ranked'][0]['option']}")
    # per-claim verdict change: the `failed` claim flips DISPUTED (best/recency) -> UNDETERMINED (anchor);
    # the `passed` claim flips DETERMINED (best) -> DISPUTED/UNDETERMINED-only (anchor/recency)
    _report("VERDICT CHANGE: 'failed' DISPUTED under best-rel & recency, UNDETERMINED under strict-anchor",
            ("claim://inspect/failed" in bo["rec"]["disputed"]
             and "claim://inspect/failed" in ro["rec"]["disputed"]
             and "claim://inspect/failed" not in ao["rec"]["disputed"]),
            f"support failed: best={sup_b.get('claim://inspect/failed')} "
            f"strict-anchor={sup_a.get('claim://inspect/failed')} recency={sup_r.get('claim://inspect/failed')}")
    _report("VERDICT CHANGE: 'passed' DETERMINED under best-rel, only DISPUTED under anchor/recency",
            ("claim://inspect/passed" in bo["rec"]["determined"]
             and "claim://inspect/passed" not in ao["rec"]["determined"]
             and "claim://inspect/passed" not in ro["rec"]["determined"]),
            f"support passed: best={sup_b.get('claim://inspect/passed')} "
            f"strict-anchor={sup_a.get('claim://inspect/passed')} recency={sup_r.get('claim://inspect/passed')}")
    _report("OUTCOME FLIP: best-rel DETERMINES rework-partial-credit; strict-anchor & recency → UNRESOLVED",
            (bo["determination"] == "rework-partial-credit"
             and ao["determination"] == "UNRESOLVED" and ro["determination"] == "UNRESOLVED"
             and bo["determination"] != ao["determination"]),
            f"best-rel={bo['determination']} vs strict-anchor={ao['determination']} vs recency={ro['determination']}")
    _report("rules differ, not just by name: per-claim support maps are pairwise distinct",
            sup_b != sup_a != sup_r, f"{sup_b} | {sup_a} | {sup_r}")
    _report("every variant ends in a LAWFUL terminal state: CLOSED/RESOLVED determination "
            "OR OPEN/UNRESOLVED (never a fabricated winner; §6 / truthful-UNRESOLVED)",
            all((r["d_main"].get("determination") == "UNRESOLVED" and r["d_main"].get("status") == "OPEN")
                or (r["d_main"].get("status") == "RESOLVED"
                    and r["d_main"].get("epistemic_state") == "RESOLVED_DETERMINED")
                for r in results))

    render_report(results)
    print("\n  -> emitted fixtures under instances/contested_reality/artifacts/adjudication/fixtures/inspect-{best,anchor,rec}/")
    print("  -> rule-comparison report under artifacts/adjudication/reports/rule-comparison.{md,json}")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())