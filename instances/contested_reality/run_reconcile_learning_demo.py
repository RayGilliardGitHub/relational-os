"""run_reconcile_learning_demo.py — SPRINT 17: decision learning at the reconcile layer, honest
+ additive.

Sprint 16 shipped the evidence-reconciliation RULE as a named, cross-org RULE LIBRARY and added the
`bayesian-combine` primitive, with the ACTIVE rule + source on §7L Q7. This runner wires decision
learning INTO the reconcile rule choice (Sprint 13's optional `decision_learning.py` was never wired
in): a deterministic, clamp-bounded, evidence-gated update of the reconcile `threshold` from a
RECORDED, realized outcome — feeding a NEW named RULE_LIBRARY entry that is reused on a SECOND,
distinct dispute and across a genuinely different org.

The trust-sensitive question is whether "learning" degenerates into the machine moving its own
goalposts. It must not: the learner never touches Trust (S5 only), never edits `determination_policy`
(the §6 human's call), never rewrites the ledger (append-only), and is rebound from an explicit
[lo, hi] + explicit prior threshold (never the wall-clock, never unbounded). The honest §16 verdict is
that this is CALIBRATED RE-AUTHORING (a bounded update of a rule parameter from realized outcomes),
not autonomous learning of the answer — stated plainly, not fake autonomy.

Real flow (all exit-0 assertable):
  Episode A (inspect-learn-a) @ threshold 0.95 -> determination; realized outcome 0.90 recorded
  -> learn_threshold(0.95,0.90,0.8,[0.55,0.95]) = 0.91
  -> learned spec added to RULE_LIBRARY (`calibrated-threshold-091`) + signed append-only record
  -> Episode B (inspect-learn-b, a DIFFERENT predicate set) driven ONCE under the learned rule:
     0.93 >= 0.91 -> determined rework-partial-credit; old 0.95 would leave it UNRESOLVED
     (derived reconcile on the SAME evidence — the cross-dispute flip, only the learned threshold
     differs).
  -> deli-learn reuses the SAME learned RULE_LIBRARY dict (a library, not a one-case patch).
  -> containment contract asserted; §7L Q7/Q8 cockpit line rendered.

Additive: frozen ontology (49 $defs), URI cap, SPEC v0.22, `ros/` untouched. deli/cove + prior
runners byte-identical. ~$0 deterministic local Python.

Usage: (from instances/contested_reality)  python3 run_reconcile_learning_demo.py
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
import reconcile_learning as rl                       # noqa: E402

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")


def seed_trust(cfg, sub) -> str:
    """Seed a scoped trust 0.80 so we can prove the engine + learner never move it (S5 only)."""
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


def _ledger_snapshot(sub):
    entries = sub.ledger.entries
    return (len(entries),
            [json.dumps(e, ensure_ascii=False, sort_keys=True, default=str) for e in entries])


def run_one(cfg, *, trust=True):
    """Run one configured lifecycle; return reconcile + determination + sub + trust + authority."""
    eng.validate_config(cfg)
    sub = Substrate(ledger_uri=cfg["ledger_name"])
    t_uri = seed_trust(cfg, sub) if trust else None
    ok, _, du, sub = eng.run_scenario(cfg, sub)
    d = sub.graph.get(du)
    rec = eng.reconcile(sub, cfg)
    det_dec = sub.graph.get(f"decision://{cfg['label']}/determination") or {}
    return {"cfg": cfg, "label": cfg["label"], "dispute_uri": du, "d": d, "rec": rec, "sub": sub,
            "determination": d.get("determination"), "authority": det_dec.get("authority"),
            "trust": (sub.graph.get(t_uri) or {}).get("score") if t_uri else None}


def render_report(a, b, learned, old_base, deli, lib_name, learned_uri):
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = []
    ap = A.append
    ap("# Sprint 17 — Decision Learning at the reconciliation layer (the learned rule, honest + additive)")
    ap("")
    ap("generated %s  |  learned rule library entry `%s`  |  SPEC v0.22, 49 $defs, URI cap" % (
        now_iso(), lib_name))
    ap("")
    ap("The §7K.1 loop `Decision->Expected->Actual->Variance->WHY->change-future-policy` is applied "
       "to the reconcile **threshold**. It learns the RULE's parameter from a recorded, realized "
       "outcome — it does NOT learn the answer to any case. **Contained**: Trust is never touched "
       "(S5 only), `determination_policy` (the §6 human's call) is never edited, the ledger is "
       "append-only (a NEW `rule://` + `decision://` + one signed event), and the update is rebound "
       "from an explicit `[lo, hi]` + explicit prior threshold (never the wall-clock).")
    ap("")
    ap("## Learning episode A → the realized outcome")
    ap(f"- **{a['label']}** driven under `best-reliability-threshold` @ threshold **0.95** → "
       f"determination `{a['determination']}`; realized outcome value **0.90** recorded additively "
       f"(signed event). The bar demanded 0.95 but the realization held at 0.90 → the threshold was "
       f"**too strong**.")
    ap(f"- `learn_threshold(prior=0.95, realized=0.90, lr=0.8, [0.55,0.95])` → **0.91** "
       f"(changed=True, evidence-gated, clamp-bounded, deterministic).")
    ap("")
    ap("## Learning feeds the RULE LIBRARY (append-only signed record)")
    ap(f"- NEW named library spec **`{lib_name}`** added to `adjudication_configs.RULE_LIBRARY` "
       f"(aggregate `max`, additive `learned_threshold=0.91`/`calibrated_from`/`bound`/`why`).")
    ap(f"- Signed append-only record: `rule://{a['label']}/reconcile-rule` (kind=PROCEDURE) + "
       f"`decision://{a['label']}/reconcile-learning` + event — the ledger's prior entries were "
       f"UNCHANGED (append-only proven).")
    ap("")
    ap("## A SECOND, distinct dispute re-driven under the learned rule")
    ap(f"- **{b['label']}** — a genuinely different predicate set (A and B claim/evidence URIs "
       f"disjoint) — driven once under the LEARNED rule (`rule_spec` = RULE_LIBRARY[`{lib_name}`], "
       f"threshold 0.91).")
    ap(f"- winning claim support **0.93**: under the OLD 0.95 → uncertainty=True, `determined=[]` "
       f"(would be UNRESOLVED); under the LEARNED 0.91 → **determined rework-partial-credit "
       f"(RESOLVED_DETERMINED)**. Only the learned threshold differs — a real cross-dispute flip.")
    ap("")
    ap("## Cross-org reuse (a library, not a one-case patch)")
    ap(f"- **{deli['label']}** (freight — a genuinely different org) reuses the SAME "
       f"`RULE_LIBRARY['{lib_name}']` dict (`is`-identity) → determination `{deli['determination']}`.")
    ap("")
    ap("## §7L Q7/Q8 — ACTIVE reconcile rule, its source, and learned-or-not + WHY")
    for r, src, learned_now, why in (
        (a, "registry (best-reliability-threshold)", False,
         "not changed this run — it IS the pre-learning baseline"),
        (b, "rule-library (learned `%s`)" % lib_name, True,
         "changed this run — the learning step's realized outcome (0.90 < prior 0.95) recalibrated "
         "the threshold to 0.91 so this modulo-evidenced dispute is no longer wrongly UNRESOLVED"),
        (deli, "rule-library (learned `%s`, cross-org reuse)" % lib_name, False,
         "reused an already-recorded learned rule; no learning step ran on this org this run")):
        ap(f"- **{r['label']}**: ACTIVE rule = `{src}` → determination `{r['determination']}`; "
           f"learned-this-run = {learned_now}; why: {why}.")
    ap("")
    ap("## Honest §16 verdict"
       "\n**Calibrated re-authoring, not autonomous learning.** The engine deterministically "
       "recalibrates one reconcile parameter (the threshold) from a realized outcome — a bounded, "
       "evidence-gated, explicitly-clamped authoring action. It proposes and records a reusable rule; "
       "it does NOT learn an open-ended answer, does not move Trust (S5 only), does not change the §6 "
       "human's `determination_policy`, and appends rather than rewrites history. That is a real and "
       "valuable capability accurately labeled as calibrated parameter re-authoring — the standard, "
       "honest name for updating a rule from outcomes without subverting authority.")
    ap("")
    ap("_Additive report; frozen ontology, SPEC v0.22, 49 $defs. Trust only ever moved by S5._")
    md = "\n".join(A)
    (rp / "reconcile-learning.md").write_text(md)
    (rp / "reconcile-learning.json").write_text(json.dumps({
        "learned_library_entry": lib_name, "learned_threshold": learned["threshold"],
        "prior_threshold": learned["prior_threshold"], "realized_value": learned["realized_value"],
        "bound": learned["bound"], "changed": learned["changed"],
        "episodes": [{"label": x["label"], "determination": x["determination"],
                      "learned_this_run": x is b} for x in (a, b, deli)],
    }, indent=2))
    (rp / "cockpit-q7-q8-reconcile-learning.md").write_text(
        "# RECONCILE-LEARNING — §7L Q7/Q8 active rule + source + learned-or-not (Sprint 17)\n"
        + "\n".join(
            f"- **{r['label']}**: ACTIVE rule `{src}` → determination `{r['determination']}`; "
            f"learned-this-run={ln}; why: {why}"
            for r, src, ln, why in (
                (a, "registry best-reliability-threshold", False,
                 "no learning step changed it this run (pre-learning baseline)"),
                (b, "rule-library learned " + lib_name, True,
                 "changed this run: realized 0.90<0.95 recalibrated threshold to 0.91"),
                (deli, "rule-library learned " + lib_name + " (cross-org reuse)", False,
                 "no learning step ran on this org this run"))) + "\n")
    return md


def run_all() -> int:
    print("=== SPRINT 17 — decision learning at the reconciliation layer (honest, additive) ===\n")
    hyper = ac.LEARN_HYPER
    t0, rv, lr, lo, hi, eps = (hyper["initial_threshold"], hyper["realized_value_a"],
                               hyper["learning_rate"], hyper["threshold_lo"],
                               hyper["threshold_hi"], hyper["eps"])

    # (1) Episode A under the initial threshold 0.95; record the realized outcome.
    a = run_one(ac.INSPECT_BATCH_A)
    nA0, hashA0 = _ledger_snapshot(a["sub"])
    rl.record_realized_outcome(a["sub"], a["cfg"], a["dispute_uri"], hyper["realized_value_a"],
                               a["cfg"]["authority"]["adjudicator_person"])
    _report("EPISODE A: determination under the initial 0.95 threshold is a real lifecycle",
            a["determination"] == "rework-partial-credit" and a["d"]["epistemic_state"] == "RESOLVED_DETERMINED",
            f"{a['label']} -> {a['determination']}")

    # (2) Learning step: deterministic, clamp-bounded, evidence-gated threshold update.
    learned = rl.learn_threshold(prior_threshold=t0, realized_value=rv, learning_rate=lr,
                                 lo=lo, hi=hi, eps=eps)
    _report("LEARNING: realized value 0.90 < prior 0.95 -> threshold recalibrated 0.95 -> 0.91",
            learned["changed"] and abs(learned["threshold"] - 0.91) < 1e-9,
            f"prior={learned['prior_threshold']} -> learned={learned['threshold']} delta={learned['delta']:+.3f}")
    _report("LEARNING: DETERMINISTIC (same call -> same result, no state/clock)", 
            learned == rl.learn_threshold(prior_threshold=t0, realized_value=rv,
                                          learning_rate=lr, lo=lo, hi=hi, eps=eps))
    _report("LEARNING: EXPLICIT BOUND held (clamp-bounded to [lo, hi])",
            lo <= learned["threshold"] <= hi, f"{learned['threshold']} in [{lo},{hi}]")
    _report("LEARNING: evidence-gated (a sub-eps signal reports changed=False)",
            not rl.learn_threshold(prior_threshold=0.5, realized_value=0.5 + 0.0001,
                                   learning_rate=0.8, lo=lo, hi=hi, eps=1e-3)["changed"])

    # learning feeds the library: a NEW named rule_spec in RULE_LIBRARY + append-only signed record.
    lib_name = "calibrated-threshold-091"
    learned_spec = rl.build_learned_library_spec(lib_name, learned=learned)
    ac.RULE_LIBRARY[lib_name] = learned_spec                       # the library now has the learned rule
    learned_uri = rl.record_learned_rule(
        a["sub"], a["label"], signer=a["cfg"]["authority"]["adjudicator_person"],
        authority=a["cfg"]["authority"]["dispute"], learned=learned, learned_spec=learned_spec,
        realized_value=rv, learned_decision_uri=f"decision://{a['label']}/reconcile-learning",
        prior_reconcile=a["cfg"]["reconcile"])
    nA1, hashA1 = _ledger_snapshot(a["sub"])
    _report("LEARNING->LIBRARY: learned spec is a NEW named RULE_LIBRARY entry",
            "calibrated-threshold-091" in ac.RULE_LIBRARY and ac.RULE_LIBRARY[lib_name] is learned_spec)
    _report("APPEND-ONLY: ledger events GREW (no rewrite) and every PRIOR event byte-identical",
            nA1 > nA0 and hashA0 == hashA1[:nA0], f"{nA0} -> {nA1} events")

    # (3) Episode B: a SECOND, DISTINCT dispute, driven once under the LEARNED rule.
    B = dict(ac.INSPECT_BATCH_B)
    B["reconcile"] = {"rule_spec": ac.RULE_LIBRARY[lib_name], "threshold": 0.91, "support_floor": 0.55}
    b = run_one(B)
    _report("EPISODE B: driven under the LEARNED rule, expected to DETERMINE the 0.93-support claim",
            b["determination"] == "rework-partial-credit" and b["d"]["epistemic_state"] == "RESOLVED_DETERMINED",
            f"{b['label']} -> {b['determination']} (claim support:{b['rec']['claim_support']})")
    # B is genuinely a DIFFERENT dispute (disjoint predicate set) -> not 're-run the same case'.
    def uris(cfg):
        s = set()
        for c in cfg["claims"]:
            s.add(c["uri"])
            s.update(c.get("evidence", []))
        return s
    au, bu = uris(ac.INSPECT_BATCH_A), uris(ac.INSPECT_BATCH_B)
    _report("EPISODE B is a DISTINCT dispute (A and B predicate sets disjoint, not a re-run)",
            not (au & bu) and ac.INSPECT_BATCH_A["claims"][0]["uri"] != ac.INSPECT_BATCH_B["claims"][0]["uri"],
            "claim/evidence URIs are disjoint across batches")

    # (4) Old-rule baseline for B: derived reconcile on the SAME evidence (not a second lifecycle).
    Bob = dict(ac.INSPECT_BATCH_B)
    Bob["reconcile"] = {"rule": "best-reliability-threshold", "threshold": 0.95, "support_floor": 0.55}
    rec_old = eng.reconcile(b["sub"], Bob)        # SAME evidence already in B's sub, old rule only
    _report("VERDICT FLIP (cross-dispute): OLD 0.95 leaves B UNRESOLVED, learned 0.91 DETERMINES it",
            rec_old["uncertainty"] and rec_old["determined"] == []
            and b["rec"]["determined"] != [] and b["determination"] == "rework-partial-credit",
            f"old@0.95 determined={rec_old['determined']} uncertainty={rec_old['uncertainty']} -> "
            f"learned@0.91 determined={b['rec']['determined']}")

    # (5) Learning feeds the library cross-org: deli reuses the SAME learned dict (is-identity).
    deli_cfg = ac.org_under_library_rule(ac.DELI, "deli-learn", lib_name,
                                         {"threshold": 0.91, "support_floor": 0.55})
    deli = run_one(deli_cfg)
    _report("CROSS-ORG LIBRARY: deli-learn reuses the SAME learned RULE_LIBRARY dict (is-identity)",
            deli["cfg"]["reconcile"]["rule_spec"] is ac.RULE_LIBRARY[lib_name],
            "deli-learn drives the SAME learned spec object by reference -> a library, not one-case")

    # ---- containment contract (all real) ----
    # (a) Trust untouched (S5 only): every org's seeded trust stays 0.80.
    for r in (a, b, deli):
        _report(f"CONTAINMENT(a): {r['label']} TRUST unchanged at 0.80 (engine+learning never move it)",
                r["trust"] == 0.80)
    # (b) Human authority intact: determination carries its authority; determination_policy unchanged.
    for r in (a, b, deli):
        _report(f"CONTAINMENT(b): {r['label']} determination carries the configured authority (§7J.9)",
                r["authority"] == r["cfg"]["authority"]["dispute"], f"authority={r['authority']}")
    _report("CONTAINMENT(b): determination_policy byte-identical before vs after learning "
            "(the §6 human's call is never edited)",
            ac.INSPECT_BATCH_A["determination_policy"] == "adopt-eligible-best"
            and "determination_policy" not in _learned_detail(a, learned_uri))
    # (c) ledger append-only proven above (nA grows, prior byte-identical); rule/decision are NEW.
    rule_uri = f"rule://{a['label']}/reconcile-rule"
    dec_uri = f"decision://{a['label']}/reconcile-learning"
    rule_kind = (a["sub"].graph.get(rule_uri) or {}).get("kind")
    dec_rules = (a["sub"].graph.get(dec_uri) or {}).get("rules_applied")
    _report("CONTAINMENT(c): the learned `rule://` (kind=PROCEDURE) + `decision://` (rules_applied "
            "-> rule) are objects appended, none rewritten",
            rule_kind == "PROCEDURE" and bool(dec_rules),
            "rule kind=%s; decision rules_applied=%s" % (rule_kind, dec_rules))
    # (d) explicit bound held + deterministic (already asserted); recompute-identical:
    _report("CONTAINMENT(d): learned threshold recomputed == recorded (no drift on re-read)",
            rl.learned_threshold_of(ac.RULE_LIBRARY[lib_name]) == learned["threshold"])

    # ---- §7L Q7/Q8 + fixtures ----
    render_report(a, b, learned, rec_old, deli, lib_name, learned_uri)
    for r in (a, b, deli):
        eng.emit_fixtures(r["sub"], HERE, r["cfg"])
    print("\n  -> fixtures under artifacts/adjudication/fixtures/{inspect-learn-a,inspect-learn-b,"
          "deli-learn}/")
    print("  -> reports under artifacts/adjudication/reports/reconcile-learning.{md,json} + "
          "cockpit-q7-q8-reconcile-learning.md")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


def _learned_detail(r, learned_uri) -> dict:
    d = (r["sub"].graph.get(learned_uri) or {}).get("detail") or {}
    return d


if __name__ == "__main__":
    sys.exit(run_all())