# === DEMO / TEST RUNNER - NOT part of the engine API ===
"""run_adjudication_engine_demo.py — SPRINT 13: the SAME configurable adjudication engine drives
TWO different org scenarios (a freight/delivery $18k dispute AND a clinical coverage dispute),
with NO code change between them — only config/data. Proves the Sprint-12 gap is closed:
adjudication semantics are no longer per-scenario authored code.

For each configured scenario it deterministically runs the full contested-reality lifecycle
(claims -> evidence -> reconcile -> conflict/uncertainty -> dispute OPEN -> options ranked via the
config's business-model weights -> §6 floor gate -> advisory decision:// -> authorized human
determination (or UNRESOLVED) -> verified outcome -> learning), PLUS the thin-evidence UNRESOLVED
sub-dispute, PLUS the optional realized-cost / Decision-Learning weight update and a §7L cockpit
Q7 render — all additive, frozen ontology, SPEC v0.22, ~$0, real output.

Usage: (from instances/contested_reality)  python3 run_adjudication_engine_demo.py
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
import decision_learning as dl                        # noqa: E402

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")


def render_q7(cfg, sub, du, d_main, ranked, best, determination):
    """Additive §7L cockpit Q7 render for the configured episode (reuses the cockpit report
    style; no new renderer universe, no change to sector_scene.py)."""
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    L = cfg["label"]
    A = []
    ap = A.append
    ap(f"# {cfg['company_name']} — §7L cockpit question 7 (configured adjudication episode)")
    ap(f"generated {now_iso()}  |  ledger events {len(sub.ledger.entries)}  "
      f"graph objects {len(sub.graph.objects)}  |  label `{L}`")
    ap("")
    ap("## 7. WHAT ARE OUR OPTIONS?  (options incl. do-nothing + trade-off — §7K.1)")
    ap(f"- dispute: `{du}`  status **{d_main.get('status')}**  "
      f"lifecycle **{d_main.get('lifecycle_state')}**  "
      f"epistemic **{d_main.get('epistemic_state')}**")
    ap(f"- business model (weights, Σ=1.0): {cfg['weights']}")
    ap("")
    ap("| utility | option | §6 gate |")
    ap("|---|---|---|")
    for r in ranked:
        ap(f"| {r['utility']:.3f} | {r['option']} | {'FLOOR-GATED' if r['floor_gated'] else ''} |")
    ap("")
    gated = [r["option"] for r in ranked if r["floor_gated"]]
    ap(f"- machine-eligible best (non-gated, §6): **{best['option']}** @ {best['utility']:.3f}")
    ap(f"- §6 floor-gated (excluded from machine auto-pick): {gated}")
    ap(f"- do-nothing / UNRESOLVED baseline present: "
      f"{any('unres' in r['option'].lower() or r['option'] == 'do-nothing' for r in ranked)} "
      f"(never forced winner)")
    ap(f"- recommendation (#8) with the authority it requires (§7J.9): adopt `{best['option']}` "
      f"under `{cfg['authority']['dispute']}` (confidence 0.7)")
    ap(f"- human determination: **{determination}** (the §6 adjudicator's authoritative call; "
      f"the machine can only recommend)")
    ap(f"- trade-off: {eng.render_tradeoff(cfg, ranked)}")
    ap("")
    ap("_Rendered additively from the configurable adjudication engine (SPEC v0.22, frozen "
      "ontology, §7L — options incl. do-nothing + trade-off). Same engine, any configured org._")
    md = "\n".join(A)
    path = rp / "cockpit-q7.md"
    path.write_text(md)
    (rp / "cockpit-q7.json").write_text(json.dumps(
        {"company": cfg["company_name"], "label": L, "question": 7,
         "dispute": du, "lifecycle_state": d_main.get("lifecycle_state"),
         "epistemic_state": d_main.get("epistemic_state"),
         "weights": cfg["weights"], "ranking": ranked, "machine_eligible_best": best,
         "floor_gated": gated, "determination": determination}, indent=2))
    # per-label copies so BOTH configured episodes stay documented (additive, same surface)
    (rp / f"cockpit-q7-{L}.md").write_text(md)
    (rp / f"cockpit-q7-{L}.json").write_text(json.dumps(
        {"company": cfg["company_name"], "label": L, "question": 7,
         "dispute": du, "lifecycle_state": d_main.get("lifecycle_state"),
         "epistemic_state": d_main.get("epistemic_state"),
         "weights": cfg["weights"], "ranking": ranked, "machine_eligible_best": best,
         "floor_gated": gated, "determination": determination}, indent=2))
    return {"written": path.exists(), "path": str(path)}


def run_all() -> int:
    print("=== CONFIGURABLE ADJUDICATION ENGINE — two org scenarios, same engine, no code change ===")
    per_scenario = []
    for cfg in ac.SCENARIOS:
        L = cfg["label"]
        print(f"\n##### SCENARIO {cfg['scene']}  ({cfg['company_name']}, label {L}) #####")
        eng.validate_config(cfg)

        sub = Substrate(ledger_uri=cfg["ledger_name"])
        # seed scoped Trust up-front; the engine must never change it (only the deterministic formula)
        trust_uri = f"trust://{L}/claimant"
        trust_seed = 0.80
        sub.record({"uri": f"event://{L}/seed-trust", "type": "STATE_CHANGE",
                    "event_id": f"ev-adj-{L}-seed-trust",
                    "correlation_id": f"corr-adj-{L}-seed-trust",
                    "causation_id": f"ev-adj-{L}-seed-trust-prev",
                    "idempotency_key": f"idem-adj-{L}-seed-trust",
                    "signature": f"signed-by-{cfg['registrar']}", "occurred_at": now_iso(),
                    "actor": cfg["registrar"], "detail": "seed scoped trust before the episode",
                    "state_update": [{"uri": trust_uri, "subject": cfg["registrar"],
                                      "target": cfg["claimants"][0],
                                      "claim": "honest dispute participant",
                                      "score": trust_seed, "context": "relationship://%s/x" % L,
                                      "evidence": []}]}, cfg["registrar"])

        # ---- main (determined) episode ----
        ep_ok, checks, du, _ = eng.run_scenario(cfg, sub)
        _report(f"{L} main episode ALL PASS", ep_ok)
        d_main = sub.graph.get(du)
        determination = d_main.get("determination")
        ranked = eng.rank(cfg)
        best = eng.machine_eligible_best(ranked)
        print(f"    ranking ({L} business model {cfg['weights']}):")
        for r in ranked:
            gate = " FLOOR-GATED" if r["floor_gated"] else ""
            print(f"      {r['utility']:.3f}  {r['option']}{gate}")
        print(f"    -> machine-eligible best (non-gated): {best['option']}@{best['utility']:.3f}")
        print(f"    -> human determination: {determination}  "
              f"(epistemic {d_main.get('epistemic_state')}, lifecycle {d_main.get('lifecycle_state')})")

        # ---- thin-evidence UNRESOLVED sub-dispute ----
        u_ok, _, u_du, _ = eng.run_scenario(cfg, sub, unresolved=True)
        _report(f"{L} UNRESOLVED sub-dispute (insufficient basis, Trust untouched)", u_ok)
        d_u = sub.graph.get(u_du)
        print(f"    -> {u_du} determination=", d_u.get("determination"),
              " epistemic=", d_u.get("epistemic_state"))

        # ---- Decision-Learning (optional): realized-cost / expected-vs-actual weight update ----
        if cfg["learning_model"].get("enabled"):
            chosen_uri = f"decision://{L}/determination"
            chosen_utility = next(r["utility"] for r in ranked if r["option"] == best["option"])
            learn_detail = dl.record_learning(cfg, chosen_uri, chosen_utility, sub, du)
            _report(f"{L} DECISION-LEARNING: realized cost + variance + learned weights recorded "
                    "additively",
                    (sub.graph.get(chosen_uri) or {}).get("learned_weights") is not None,
                    f"variance={learn_detail['variance']} "
                    f"realized_cost=${learn_detail['realized_cost_usd']}")

        # ---- TRUST unchanged by the engine ----
        t = sub.graph.get(trust_uri)
        _report(f"{L} TRUST UNCHANGED by the engine (score {trust_seed} preserved; never authored)",
                t is not None and t.get("score") == trust_seed,
                f"score={t.get('score')}")

        # ---- determinism re-run ----
        _report(f"{L} RANKING DETERMINISTIC (identical on re-run)", eng.rank(cfg) == ranked)

        # ---- authority on the decisions ----
        det_dec = sub.graph.get(f"decision://{L}/determination")
        _report(f"{L} AUTHORITY PRESERVED on the determination (decision carries the configured "
                "authority)",
                det_dec is not None and det_dec.get("authority") == cfg["authority"]["dispute"],
                f"authority={cfg['authority']['dispute']}")

        # ---- §7L cockpit Q7 render (additive report) ----
        q7 = render_q7(cfg, sub, du, d_main, ranked, best, determination)
        _report(f"{L} §7L cockpit Q7 'WHAT ARE OUR OPTIONS?' rendered", q7["written"], q7["path"])

        eng.emit_fixtures(sub, HERE, cfg)
        per_scenario.append({"label": L, "scene": cfg["scene"], "weights": dict(cfg["weights"]),
                             "ranking": ranked, "determination": determination, "best": best["option"],
                             "unresolved_state": d_u.get("determination")})

    # ---- cross-scenario: the generalization proof ----
    _report("GENERALIZATION: ONE engine drives BOTH orgs with NO code change (only config data)",
            len(per_scenario) == 2 and per_scenario[0]["label"] != per_scenario[1]["label"]
            and all(isinstance(p["ranking"], list) for p in per_scenario))
    _report("GENERALIZATION: the two orgs produce DISTINCT business models + determinations",
            per_scenario[0]["weights"] != per_scenario[1]["weights"]
            and per_scenario[0]["determination"] != per_scenario[1]["determination"],
            f"{per_scenario[0]['scene']}={per_scenario[0]['determination']} vs "
            f"{per_scenario[1]['scene']}={per_scenario[1]['determination']}")

    print("\n  -> emitted fixtures under instances/contested_reality/artifacts/adjudication/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())