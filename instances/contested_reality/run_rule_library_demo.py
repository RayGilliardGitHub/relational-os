"""run_rule_library_demo.py — SPRINT 16: the named, cross-org RULE LIBRARY + a new inference primitive.

Sprint 15 made the reconciliation rule BODY authorable as config text via the rule-authoring DSL
(SPEC_VOCAB + compile_rule_spec), closing Sprint-14's hinge — but its honest frontier disclosed a
remaining seam: an op OUTSIDE SPEC_VOCAB (e.g. a Bayesian posterior) still needed a new builtin
(interpreter code), after which it too is authorable as data by every org. Sprint 16 takes that seam
on:
  (a) a genuinely NEW inference primitive is added to the vocabulary ONCE — `bayesian-combine`, a
      reliability-likelihood posterior (independent corroboration synthesis) that expresses what
      `max`/`mean`/... cannot: many weak-but-independent sources can raise a claim's support ABOVE
      every single source. It is deterministic (explicit `prior`) and strict (bad `prior` rejected
      loudly).
  (b) spec-authored rules become a REUSABLE cross-org RULE LIBRARY (`ac.RULE_LIBRARY`): named specs
      defined once and referenced by ANY org via the SAME dict — proven with `is`-identity and by
      driving each library rule on >=2 genuinely different orgs (not inspect-only).
  (c) the ACTIVE rule + its spec-authored-vs-registry source is surfaced on a §7L cockpit Q7 line.

Runner (exit 0 = ALL PASS): unit-proves the primitive, drives four library-reuse org lifecycles with
real fixtures/ledgers, asserts a real verdict FLIP the new primitive produces (inspect at reconcile
threshold 0.98: single-source max 0.97 clears nothing -> UNRESOLVED; bayesian-combine of the 0.84 +
0.97 witnesses -> posterior ~0.9961 -> DETERMINED rework-partial-credit CLOSED), and renders the Q7
report. Additive: frozen ontology (49 $defs), URI cap, SPEC v0.22, ros/ untouched. Trust only moved
by the deterministic S5 formula.

Usage: (from instances/contested_reality)  python3 run_rule_library_demo.py
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
    """Run one configured episode; return the per-claim reconcile verdict + determination + the
    Substrate (so a secondary reconcile against the SAME ledger is possible)."""
    L = cfg["label"]
    eng.validate_config(cfg)
    sub = Substrate(ledger_uri=cfg["ledger_name"])
    trust_uri = seed_trust(cfg, sub)
    ep_ok, _, du, sub = eng.run_scenario(cfg, sub)
    d_main = sub.graph.get(du)
    rec = eng.reconcile(sub, cfg)
    ranked = eng.rank(cfg); best = eng.machine_eligible_best(ranked)
    t = sub.graph.get(trust_uri)
    det_dec = sub.graph.get(f"decision://{L}/determination") or {}
    eng.emit_fixtures(sub, HERE, cfg)
    return {"cfg": cfg, "label": L, "ep_ok": ep_ok, "rec": rec, "determination": d_main.get("determination"),
            "d_main": d_main, "trust": t.get("score"), "authority": det_dec.get("authority"),
            "best": best, "ranked": ranked, "sub": sub}


def render_report(results: list[dict], active: list[dict]) -> None:
    """Render the rule-library report: the cross-org library table + a §7L cockpit Q7 line per org
    naming the ACTIVE rule and its spec-authored-vs-registry source (the Sprint-16 Q7 surface)."""
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = []
    ap = A.append
    ap("# Sprint 16 — the named, cross-org RULE LIBRARY + a NEW inference primitive (`bayesian-combine`)")
    ap(f"generated {now_iso()}  |  {len(results)} library-reuse org lifecycles  |  "
       f"SPEC_VOCAB={sorted(eng.SPEC_VOCAB)}")
    ap("")
    ap("Named rule specs live ONCE in `adjudication_configs.RULE_LIBRARY` and are reused by reference "
       "(the same dict) by any org — a real library, not inspect-only. The NEW `bayesian-combine` "
       "primitive is authored once in the language and serves every org as data.")
    ap("")
    by = {r["label"]: r for r in results}

    ap("## The RULE LIBRARY (named specs; `is`-shared across the orgs below)")
    ap("")
    ap("| rule (library entry) | aggregate | reused by org(s) | active source |")
    ap("|---|---|---|---|")
    order = ["inspect-majority-lib", "deli-majority", "inspect-corroboration", "cove-corroboration"]
    seen_rule = {}
    for lab in order:
        r = by[lab]; rc = r["cfg"]["reconcile"]; spec = rc["rule_spec"]
        name = spec["name"]; seen_rule.setdefault(name, []).append(lab)
    for name, labs in sorted(seen_rule.items()):
        ap(f"| `{name}` | `{spec['aggregate']}` | {', '.join(labs)} | **spec-authored (rule-library DATA)** |")
    ap("")
    ap("## §7L cockpit Q7 — ACTIVE rule + its source (per org)")
    ap("")
    for lab in order:
        r = by[lab]; rc = r["cfg"]["reconcile"]; spec = rc["rule_spec"]
        ap(f"- **{lab}**: ACTIVE reconciliation rule = `{spec['name']}` "
           f"(aggregate `{spec['aggregate']}`) — **source: spec-authored "
           f"(a `RULE_LIBRARY` data dict), not an engine registry function**. "
           f"Verds: disputed={r['rec']['disputed']}, determined={r['rec']['determined']}, "
           f"conflict={r['rec']['conflict']}, uncertainty={r['rec']['uncertainty']} → "
           f"determination={r['determination']}.")
    ap("")
    ap("## Verdict-flip proof of the NEW primitive (real reconcile output)")
    ap("")
    ap("Same `inspect` dispute, reconcile threshold 0.98, only the rule differs:")
    ap("")
    for row in active:
        ap(f"- `{row['label']}` ({row['rule']}) → support {row['support']} → "
           f"determined={row['determined']} uncertainty={row['uncertainty']} → **{row['verdict']}**")
    ap("")
    ap("`max` cannot clear 0.98 (strongest single witness 0.97); `bayesian-combine` of the two "
       "independent witnesses (0.84 anchored + 0.97 record) gives a posterior above 0.98 — the "
       "corroboration-synthesis semantics `max` cannot express, authorable as data by every org.")
    ap("")
    ap("## §16 seam")
    ap("")
    ap("Part of Sprint 15's \u201cneeds a builtin\u201d seam NOW closes: the `bayesian-combine` op family "
       "(independent corroboration / reliability-likelihood) is in `SPEC_VOCAB`, authored once, and is "
       "thereafter authorable-as-data by any org. The residual dependence is now precisely: a rule "
       "requiring an op the vocabulary still does NOT name (a different posterior shape, a provenance-conditional "
       "if/then, a custom multiplicative combination beyond this one) still needs that one builtin added — "
       "interpreter code — after which it too serves every org by config. Authoring a rule as a `rule_spec` "
       "from the library still needs no engine Python.")
    ap("")
    ap("_Additive report; frozen ontology, SPEC v0.22, 49 $defs. Trust untouched by the engine; the §6 "
       "human's determination keeps its authority._")
    (rp / "rule-library.md").write_text("\n".join(A))
    (rp / "cockpit-q7-rule-library.md").write_text(
        "# RULE LIBRARY — §7L Q7 active rule + source (Sprint 16)\n"
        + "\n".join(f"- **{lab}**: ACTIVE rule = `{by[lab]['cfg']['reconcile']['rule_spec']['name']}` — "
                    f"**spec-authored (RULE_LIBRARY data)**, aggregate "
                    f"`{by[lab]['cfg']['reconcile']['rule_spec']['aggregate']}` → "
                    f"determination={by[lab]['determination']}"
                    for lab in order) + "\n")


def _primitive_proof():
    """Unit-prove the NEW `bayesian-combine` primitive: deterministic, strict, and able to express
    per-claim support ABOVE the single strongest source — the corroboration-synthesis semantics NO
    old op (`max`/`mean`/...) can produce. This is the hinge that closes Sprint 15's told seam for
    this op family: weak-but-independent sources now combine, authorable as data by any org."""
    _report("bayesian-combine IN VOCAB (new inference primitive is in the shipped language)",
            "bayesian-combine" in eng.SPEC_VOCAB, f"SPEC_VOCAB={sorted(eng.SPEC_VOCAB)}")
    spec = {"aggregate": "bayesian-combine", "value_field": "reliability", "prior": 0.7}
    mx = eng._aggregate("max", [(0.7, 0.5), (0.7, 0.5), (0.7, 0.5)], {})
    bc = eng._aggregate("bayesian-combine", [(0.7, 0.5), (0.7, 0.5), (0.7, 0.5)], spec)
    _report("bayesian-combine expresses what max CANNOT: posterior (0.9674) > strongest source (0.7)",
            bc == 0.9674 and bc > mx,
            f"max={mx}, bayesian-combine(3x0.7, prior 0.7)={bc} — many weak sources exceed ONE strong source")
    _report("bayesian-combine DETERMINISTIC: empty source set -> posterior == prior (no evidence)",
            eng._aggregate("bayesian-combine", [], spec) == 0.7,
            f"posterior(no evidence)={eng._aggregate('bayesian-combine', [], spec)}")
    _report("bayesian-combine treats a certain (1.0) source as pinning the claim",
            eng._aggregate("bayesian-combine", [(0.7, 0.5), (1.0, 0.5)], spec) == 1.0)
    for bad, frag in (({"aggregate": "bayesian-combine"}, "0 < prior < 1"),
                      ({"aggregate": "bayesian-combine", "prior": 0}, "0 < prior < 1"),
                      ({"aggregate": "bayesian-combine", "prior": 1}, "0 < prior < 1"),
                      ({"aggregate": "bayesian-combine", "prior": 1.5}, "0 < prior < 1"),
                      ({"aggregate": "bayesian-combine", "prior": "0.6"}, "0 < prior < 1")):
        try:
            eng.compile_rule_spec(bad); got = (False, "(no error)")
        except ValueError as e:
            got = (frag in str(e), str(e))
        _report(f"COMPILER STRICT: bad prior {bad.get('prior', 'MISSING')!r} rejected loudly",
                got[0], got[1])
    ok = eng.compile_rule_spec({"aggregate": "bayesian-combine", "prior": 0.6})
    _report("COMPILER DETERMINISTIC: same spec compiles to the same verified dict on re-run",
            ok == eng.compile_rule_spec({"aggregate": "bayesian-combine", "prior": 0.6}))


def run_all() -> int:
    print("=== SPRINT 16 — named cross-org RULE LIBRARY + NEW `bayesian-combine` primitive ===\n")
    _primitive_proof()
    print()

    # build a library-driven `inspect` under majority too, so BOTH library rules are shown on
    # >=2 genuinely different orgs (goods-QC + freight / clinical), and by `is`-identity of the
    # SAME RULE_LIBRARY dict (a real library, not a per-org copy).
    inspect_majlib = ac.org_under_library_rule(
        ac.INSPECT, "inspect-majority-lib", "majority-of-sources",
        {"threshold": 0.92, "support_floor": 0.55})
    drives = [inspect_majlib] + list(ac.LIBRARY_REUSE)
    results = {}
    for cfg in drives:
        r = run_one(cfg); results[r["label"]] = r
        print(f"  {r['label']:20s} -> disputed={r['rec']['disputed']} "
              f"determined={r['rec']['determined']} uncertainty={r['rec']['uncertainty']} "
              f"determination={r['determination']}")

    # ---- (b) cross-org RULE LIBRARY reuse: the SAME named spec dict reused by >=2 orgs -------
    def same_dict(lab1, lab2, rule_name):
        return results[lab1]["cfg"]["reconcile"]["rule_spec"] is results[lab2]["cfg"]["reconcile"]["rule_spec"] \
            and results[lab1]["cfg"]["reconcile"]["rule_spec"]["name"] == rule_name
    _report("RULE LIBRARY: `majority-of-sources` reused by the SAME dict on 2 orgs "
            "(inspect-majority-lib + deli-majority) — not inspect-only",
            same_dict("inspect-majority-lib", "deli-majority", "majority-of-sources"),
            f"shared-spec-name={results['inspect-majority-lib']['cfg']['reconcile']['rule_spec']['name']}")
    _report("RULE LIBRARY: the NEW `independent-corroboration` reused by the SAME dict on 2 orgs "
            "(inspect-corroboration + cove-corroboration)",
            same_dict("inspect-corroboration", "cove-corroboration", "independent-corroboration"),
            f"aggregate={results['inspect-corroboration']['cfg']['reconcile']['rule_spec']['aggregate']}")
    _report("RULE LIBRARY entries are authored ONCE and reused (shared dict, not a per-org copy)",
            all(results[c["label"]]["cfg"]["reconcile"]["rule_spec"] is ac.RULE_LIBRARY[rname]
                for c in ac.LIBRARY_REUSE
                for rname in (c["reconcile"]["rule_spec"]["name"],)),
            "every reuse variant points at the SAME RULE_LIBRARY dict by reference")
    _report("RULE LIBRARY has a genuinely NEW primitive-driven rule for any org to author as data",
            "independent-corroboration" in ac.RULE_LIBRARY
            and ac.RULE_LIBRARY["independent-corroboration"]["aggregate"] == "bayesian-combine")
    # every reuse org ends in a lawful terminal state
    for lab in results:
        d = results[lab]["d_main"]
        _report(f"{lab} ends in a lawful terminal state "
                "(CLOSED+RESOLVED_DETERMINED or OPEN+INSUFFICIENT_EVIDENCE for UNRESOLVED)",
                (d.get("determination") == "UNRESOLVED" and d.get("status") == "OPEN")
                or (d.get("status") == "RESOLVED" and d.get("epistemic_state") == "RESOLVED_DETERMINED"))

    # ---- (a) the NEW primitive produces a REAL verdict FLIP on the same org, only the rule ------ 
    # differs. At reconcile threshold 0.98 on the `inspect` dispute: single-source best-reliability
    # (`max`) tops out at 0.97 (the strongest witness) which clears NOTHING -> UNRESOLVED; the two
    # independent witnesses (0.84 anchored + 0.97 record) combine under bayesian-combine to a
    # posterior ~0.9961 which DOES clear 0.98 -> determined rework-partial-credit (CLOSED).
    max098 = dict(ac.INSPECT); max098["label"] = "inspect-max098"
    for k in ("actors", "relationships", "obligations", "claims", "evidence", "dispute",
              "factor_scores", "options", "floor_gated"):
        max098[k] = ac.INSPECT[k]
    max098["reconcile"] = {"rule": "best-reliability-threshold", "threshold": 0.98,
                           "support_floor": 0.55}
    r_max = run_one(max098)
    results["inspect-max098"] = r_max
    r_bay = results["inspect-corroboration"]
    _report("VERDICT FLIP AT 0.98: single-source max (0.97) clears nothing -> UNRESOLVED",
            r_max["rec"]["determined"] == [] and r_max["rec"]["uncertainty"]
            and r_max["determination"] == "UNRESOLVED",
            f"support max={r_max['rec']['claim_support']} -> uncertainty={r_max['rec']['uncertainty']}")
    _report("VERDICT FLIP AT 0.98: bayesian-combine of 0.84+0.97 -> posterior 0.9961 -> DETERMINED "
            "rework-partial-credit (CLOSED)",
            abs(r_bay["rec"]["claim_support"]["claim://inspect/passed"] - 0.9961) < 1e-4
            and "passed" in r_bay["rec"]["determined"][0]
            and r_bay["determination"] == "rework-partial-credit",
            f"support bayesian={r_bay['rec']['claim_support']} -> determined={r_bay['rec']['determined']}")
    _report("the flip is ONLY the rule, org+evidence identical: perturbing `reconcile` at the SAME "
            "threshold flips a determination-vs-UNRESOLVED verdict",
            r_max["determination"] != r_bay["determination"],
            f"max@0.98 -> {r_max['determination']} ; bayesian@0.98 -> {r_bay['determination']}")

    # ---- invariants hold for every library-driven org -------------------------------------------
    for lab in results:
        r = results[lab]
        _report(f"{lab} TRUST UNCHANGED by the engine (score 0.80 preserved)", r["trust"] == 0.80)
        _report(f"{lab} RANKING DETERMINISTIC (identical on re-run)", eng.rank(r["cfg"]) == r["ranked"])
        _report(f"{lab} AUTHORITY PRESERVED (determination carries the configured authority)",
                (r["authority"] == r["cfg"]["authority"]["dispute"]) or r["determination"] == "UNRESOLVED",
                f"authority={r['authority']}")
    _report("ALL library engines run WITHOUT per-org Python (every reconcile is a RULE_LIBRARY spec)",
            all("rule_spec" in results[lab]["cfg"]["reconcile"] for lab in
                ("inspect-majority-lib", "deli-majority", "inspect-corroboration", "cove-corroboration")))

    active = [
        {"label": "inspect-max098", "rule": "max (best-reliability-threshold, registry)",
         "support": results["inspect-max098"]["rec"]["claim_support"],
         "determined": results["inspect-max098"]["rec"]["determined"],
         "uncertainty": results["inspect-max098"]["rec"]["uncertainty"],
         "verdict": results["inspect-max098"]["determination"]},
        {"label": "inspect-corroboration", "rule": "bayesian-combine (independent-corroboration, library spec)",
         "support": results["inspect-corroboration"]["rec"]["claim_support"],
         "determined": results["inspect-corroboration"]["rec"]["determined"],
         "uncertainty": results["inspect-corroboration"]["rec"]["uncertainty"],
         "verdict": results["inspect-corroboration"]["determination"]},
    ]
    render_report(list(results.values()), active)
    (Path(HERE) / "artifacts/adjudication/reports/rule-library.json").write_text(json.dumps(
        [{"label": r["label"], "reconcile": json.loads(json.dumps(r["cfg"]["reconcile"], default=str)),
          "claim_support": r["rec"]["claim_support"], "conflict": r["rec"]["conflict"],
          "uncertainty": r["rec"]["uncertainty"], "determination": r["determination"]}
         for r in results.values()], indent=2, default=str))

    print("\n  -> emitted fixtures under "
          "artifacts/adjudication/fixtures/{inspect-majority-lib,deli-majority,inspect-corroboration,"
          "cove-corroboration,inspect-max098}/")
    print("  -> rule-library report under artifacts/adjudication/reports/rule-library.{md,json} + "
          "cockpit-q7-rule-library.md")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())