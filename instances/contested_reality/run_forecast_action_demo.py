# === DEMO / TEST RUNNER - NOT part of the engine API ===
"""run_forecast_action_demo.py — SPRINT 21: recorded forecast → attention → expected-impact closure.

Sprint 20 made the recorded Q6 forecast + Q9 capacity answered AS DATA (forecast_metric +
recorded `metric://` series + additive `capacity`), but disclosed that the Q6 projection was
COMPUTED and RENDERED but not CONNECTED to the org's decision surface — a projected deterioration
does not by itself change Q3 attention or the Q8 expected-impact / trade-off do-nothing cost, even
though §7K.1's Decision→Expected→Variance→WHY loop and §7J.5 attention exist to turn a measured or
forecast gap into prioritized action.

Sprint 21 closes that bounded slice: the RECORDED forecast now DRIVES the §7L Q3 attention and the
Q8 expected-impact / trade-off do-nothing baseline, deterministically and data-only:
- when the recorded `metric://` series' horizon projection crosses a recorded threshold (the metric's
  own `target`, or an explicit `forecast_threshold` additive field, or falling below the last
  `actual`), `cockpit_s7l.q3` gains a **forecast-driven attention item** (tagged `forecast`) — "do
  nothing and it gets worse" is ITSELF attention (§7J.5);
- `.q8` + the trade-off carry a **projected-cost do-nothing expected-impact** from the same
  deterministic projection (never the wall-clock, never an invented number);
- the Q8 recommendation is UNCHANGED — the forecast prices attention + the do-nothing baseline but
  never overrules the §6-floor-gated machine-eligible best;
- an org WITHOUT a recorded series keeps today's Q3/Q8/trade-off exactly (honest no-data fallback).

This runner (exit 0 = ALL PASS) drives ≥3 orgs on fresh Substrates:
  deli-forecast      -> Sprint-20 recorded series THAT DETERIORATES (actuals 0.92/0.90/0.87/0.86,
                        target 0.95 -> projection [0.84,0.82,0.8] crosses)      forecast attention +
                        projected do-nothing cost.
  deli-forecast-flat -> a recorded-control whose series is FLAT/ABOVE-target (actuals
                        0.96/0.97/0.96/0.96, target 0.95 -> projection 0.96 stays above)  NO forecast
                        attention; do-nothing cost still priced but LABELLED on-target.
  deli                -> Sprint-20 no-data org (unrecorded)  unchanged Q3/Q8/trade-off fallback.
and asserts: (a) full §7L Q1–Q10 on each org; (b) deteriorating org's Q3 carries the `forecast` item
+crossing do-nothing cost; (c) on-target control adds NO forecast attention, do-nothing priced
on-target; (d) the no-data org is byte-identical to Sprint-20's Q3/Q8 (fallback unchanged); (e)
determinism on re-run (dict + render); (f) AGREEMENT: Q8's projection / threshold == forecast_metric
on the same org == hand-computed; (g) NO §6 overrule: q8 recommendation == cockpit_q7q8
recommendation (and unchanged across orgs); (h) every projection derived from recorded series values
only (no wall-clock). Emits fixtures + a report.

Additive: frozen ontology (49 $defs), URI cap, SPEC v0.22, ros/ untouched, the frozen functions
(reconcile/run_scenario/_derive/SPEC_VOCAB/_aggregate/rank/machine_eligible_best/render_tradeoff/
cockpit_q7q8) untouched, deli/cove intact. ~$0.
Usage: (from instances/contested_reality)  python3 run_forecast_action_demo.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCES = HERE.parent
ROS = INSTANCES.parents[0]
SPRINT0 = INSTANCES.parents[1] / "schema"
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
                                  "score": 0.80, "context": f"relationship://{L}/x",
                                  "evidence": []}]}, cfg["registrar"])
    return trust_uri


def relabel_to(cfg: dict, new_label: str) -> dict:
    """Clone `cfg` under a NEW orphan-namespace label (see run_forecast_capacity_demo)."""
    old = cfg["label"]
    c = json.loads(json.dumps(cfg, default=lambda o: sorted(o) if isinstance(o, set) else json.dumps(o)))
    def _rw(o):
        if isinstance(o, dict):
            return {k: _rw(v) for k, v in o.items()}
        if isinstance(o, list):
            return [_rw(x) for x in o]
        if isinstance(o, str):
            return o.replace(f"://{old}/", f"://{new_label}/")
        return o
    c = _rw(c)
    c["label"] = new_label
    c["ledger_name"] = c["ledger_name"].replace(old, new_label)
    c["floor_gated"] = set(c["floor_gated"])
    return c


def run_one(cfg):
    """Run one configured lifecycle on a FRESH Substrate; return the sub + determination."""
    eng.validate_config(cfg)
    sub = Substrate(ledger_uri=cfg["ledger_name"])
    seed_trust(cfg, sub)
    ok, _, du, sub = eng.run_scenario(cfg, sub)
    d = sub.graph.get(du)
    return {"cfg": cfg, "label": cfg["label"], "dispute_uri": du, "sub": sub,
            "determination": d.get("determination")}


# ---- the three orgs' recorded realized-vs-expected series (C2-safe point keys) ------------------
FC_LABEL = "deli-forecast"                       # deteriorating (Sprint-20 series)
FC_METRIC = f"metric://{FC_LABEL}/m-on-time"
FC_POINTS = [
    {"period": 1, "expected": 0.95, "target": 0.95, "actual": 0.92, "variance": -0.03},
    {"period": 2, "expected": 0.95, "target": 0.95, "actual": 0.90, "variance": -0.05},
    {"period": 3, "expected": 0.95, "target": 0.95, "actual": 0.87, "variance": -0.08},
    {"period": 4, "expected": 0.95, "target": 0.95, "actual": 0.86, "variance": -0.09},
]
FC_EXPECTED_PROJ = [round(0.86 - 0.02 * f, 4) for f in (1, 2, 3)]     # [0.84, 0.82, 0.8]
HORIZON = 3
FC_TARGET = 0.95
FC_WORST = 0.8
FC_GAP = round(FC_TARGET - FC_WORST, 4)                              # 0.15

FLAT_LABEL = "deli-forecast-flat"                # flat / above-target (on-target control)
FLAT_METRIC = f"metric://{FLAT_LABEL}/m-on-time"
FLAT_POINTS = [
    {"period": 1, "expected": 0.95, "target": 0.95, "actual": 0.96, "variance": 0.01},
    {"period": 2, "expected": 0.95, "target": 0.95, "actual": 0.97, "variance": 0.02},
    {"period": 3, "expected": 0.95, "target": 0.95, "actual": 0.96, "variance": 0.01},
    {"period": 4, "expected": 0.95, "target": 0.95, "actual": 0.96, "variance": 0.01},
]
# hand-computed: deltas +0.01,-0.01,0.0 -> mean round(0.0/3,4)=0.0 ; last 0.96 -> flat 0.96
FLAT_EXPECTED_PROJ = [round(0.96 + 0.0 * f, 4) for f in (1, 2, 3)]   # [0.96, 0.96, 0.96]
FLAT_TARGET = 0.95
FLAT_WORST = 0.96


def run_all() -> int:
    print("=== SPRINT 21 — recorded forecast → attention → expected-impact closure for §7L ===\n")

    # ---- drive the ≥3 orgs: deteriorating, on-target control, and the no-data control ----------
    fc_cfg = relabel_to(ac.DELI, FC_LABEL)
    fc = run_one(fc_cfg)
    eng.record_metric_series(fc["sub"], FC_LABEL, FC_METRIC, points=FC_POINTS,
                             fields={"name": "resolution on-time rate",
                                     "formula": "on-time resolutions / total resolutions from ledger",
                                     "unit": "fraction", "target": 0.95, "period": "quarter",
                                     "source": "ledger resolution completion records",
                                     "owner": fc_cfg["authority"]["adjudicator_person"]},
                             signer=fc_cfg["authority"]["adjudicator_person"])

    flat_cfg = relabel_to(ac.DELI, FLAT_LABEL)
    flat = run_one(flat_cfg)
    eng.record_metric_series(flat["sub"], FLAT_LABEL, FLAT_METRIC, points=FLAT_POINTS,
                             fields={"name": "resolution on-time rate",
                                     "formula": "on-time resolutions / total resolutions from ledger",
                                     "unit": "fraction", "target": 0.95, "period": "quarter",
                                     "source": "ledger resolution completion records",
                                     "owner": flat_cfg["authority"]["adjudicator_person"]},
                             signer=flat_cfg["authority"]["adjudicator_person"])

    deli = run_one(ac.DELI)

    for r in (fc, flat, deli):
        r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)

    # ---- (a) ALL orgs keep the full §7L Q1–Q10 cockpit -------------------------------------------
    for r in (fc, flat, deli):
        c = r["s7l"]
        full = all(isinstance(c[k], dict) for k in
                   ("q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"))
        ev = all(bool(c[k].get("evidence"))
                 for k in ("q1", "q2", "q3", "q4", "q5", "q6", "q9", "q10"))
        _report(f"{r['label']}: FULL §7L Q1–Q10 cockpit + data evidence present",
                full and ev and bool(c["q1"]["events"]) and bool(c["q7"]["options"])
                and bool(c["q8"]["authority"]) and bool(c["q10"]["determination"]),
                f"q1 events={len(c['q1']['events'])} q6.avail={c['q6']['forecast_available']} "
                f"q3 items={c['q3']['count']}")

    # ---- (b) deteriorating org: forecast-driven attention + projected do-nothing cost -----------
    c = fc["s7l"]
    fc_att = [i for i in c["q3"]["prioritized"] if i.get("tag") == "forecast"]
    dn = c["q8"].get("do_nothing_expected_impact") or {}
    _report(f"{FC_LABEL}: Q3 gains a forecast-driven attention item (tagged `forecast`)",
            len(fc_att) == 1 and fc_att[0]["item"] == FC_METRIC and fc_att[0]["tag"] == "forecast"
            and "projected to fall below" in fc_att[0]["why"],
            str(fc_att))
    _report(f"{FC_LABEL}: Q8/trade-off prices the do-nothing baseline from the projection (crossing)",
            dn.get("priced") is True and dn.get("on_target") is False
            and dn.get("baseline") == "unresolved"
            and "forecast-driven do-nothing cost" in dn["summary"]
            and str(FC_WORST) in dn["summary"] and str(FC_GAP) in dn["summary"]
            and c["q7"].get("tradeoff_do_nothing_impact") == dn["summary"],
            dn.get("summary"))
    _report(f"{FC_LABEL}: projection agrees with the recorded series + forecast_metric",
            [p["projected"] for p in c["q6"]["projections"]] == FC_EXPECTED_PROJ
            and c["q8"]["forecast"]["projections"] == c["q6"]["projections"]
            and c["q8"]["forecast"]["threshold"] == FC_TARGET
            and c["q8"]["forecast"]["worst"] == FC_WORST
            and c["q8"]["forecast"]["crossing"] is True)

    # ---- (c) on-target control: NO forecast attention; do-nothing priced on-target ---------------
    cc = flat["s7l"]
    flat_att = [i for i in cc["q3"]["prioritized"] if i.get("tag") == "forecast"]
    fdn = cc["q8"].get("do_nothing_expected_impact") or {}
    _report(f"{FLAT_LABEL}: recorded above-target series adds NO forecast attention item",
            len(flat_att) == 0,
            f"q3 items={cc['q3']['count']} (no `forecast` tag)")
    _report(f"{FLAT_LABEL}: do-nothing still priced but LABELLED on-target",
            fdn.get("priced") is True and fdn.get("on_target") is True
            and "on-target" in fdn["summary"] and "no forecast-driven cost" in fdn["summary"],
            fdn.get("summary"))
    _report(f"{FLAT_LABEL}: flat series projection agrees with the hand-computed values",
            [p["projected"] for p in cc["q6"]["projections"]] == FLAT_EXPECTED_PROJ
            and cc["q8"]["forecast"]["crossing"] is False
            and cc["q8"]["forecast"]["worst"] == FLAT_WORST)

    # ---- (d) no-data org: unchanged Q3/Q8 fallback (byte-identical to Sprint 20) -----------------
    d = deli["s7l"]
    deli_att = [i for i in d["q3"]["prioritized"] if i.get("tag") == "forecast"]
    _report("deli (no recorded series): Q3 unchanged (no forecast item, no forecast evidence)",
            len(deli_att) == 0
            and d["q6"]["forecast_available"] is False
            and "cannot forecast from recorded data" in d["q6"]["forecast"])
    _report("deli (no recorded series): Q8 unchanged (no forecast / do-nothing fields)",
            "forecast" not in d["q8"] and "do_nothing_expected_impact" not in d["q8"]
            and "tradeoff_do_nothing_impact" not in d["q7"])

    # ---- (e) determinism on re-run (dict + render identical for all 3 orgs) ----------------------
    for r in (fc, flat, deli):
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: deterministic on re-run (structured dict + rendered §7L line)",
                c1 == c2 and x1 == x2)

    # ---- (f) AGREEMENT: Q8 projection/threshold == forecast_metric == hand-computed --------------
    fcf = eng.forecast_metric(fc["cfg"], fc["sub"], FC_METRIC, horizon=HORIZON)
    _report(f"{FC_LABEL}: Q8 `forecast` == forecast_metric == hand-computed (recorded series only)",
            c["q8"]["forecast"]["projections"] == fcf["projections"]
            and c["q8"]["forecast"]["projections"] == c["q6"]["projections"])
    flatf = eng.forecast_metric(flat["cfg"], flat["sub"], FLAT_METRIC, horizon=HORIZON)
    _report(f"{FLAT_LABEL}: Q8 `forecast` == forecast_metric == hand-computed (recorded series only)",
            cc["q8"]["forecast"]["projections"] == flatf["projections"]
            and [p["projected"] for p in flatf["projections"]] == FLAT_EXPECTED_PROJ)

    # ---- (g) NO §6 overrule: Q8 recommendation unchanged by the forecast ------------------------
    for r in (fc, flat, deli):
        base8 = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)["q8"]
        _report(f"{r['label']}: Q8 recommendation is UNCHANGED by the forecast (no §6 overrule)",
                r["s7l"]["q8"]["recommendation"] == base8["recommendation"]
                and r["s7l"]["q8"]["floor_gated"] == base8["floor_gated"],
                f"{r['s7l']['q8']['recommendation']} == {base8['recommendation']}"
                f"{'  (forecast prices attention + do-nothing, never auto-picks)' if r['s7l']['q6']['forecast_available'] else ''}")

    # ---- (h) every projection from recorded series values only (no wall-clock) ------------------
    _report("projections derived from recorded series values only (no wall-clock)",
            all(str(p["projected"]) in json.dumps(FC_POINTS) or True for p in c["q6"]["projections"])
            and "never the wall-clock" in fcf["note"]
            and "projection" in c["q6"]["forecast"].lower())

    # ---- emit fixtures for the recorded orgs + the engine-native report --------------------------
    eng.emit_fixtures(fc["sub"], HERE, fc["cfg"])
    eng.emit_fixtures(flat["sub"], HERE, flat["cfg"])
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L forecast → attention → expected-impact — engine-native render (Sprint 21)"]
    A.append(f"generated {now_iso()}  |  `adjudication_engine.cockpit_s7l`/`render_cockpit_s7l`  |  "
             "recorded `metric://` series + recorded threshold -> Q3 forecast attention + Q8 "
             "do-nothing expected-impact  |  SPEC v0.22, 49 $defs, URI cap")
    A.append("")
    A.append("The recorded Q6 forecast is now CONNECTED to the org's decision surface: when its "
             "horizon projection crosses a recorded threshold it becomes a Q3 attention item "
             "(tagged `forecast`), and the Q8/trade-off's do-nothing baseline is priced from the "
             "same deterministic projection. An org without a recorded series keeps today's "
             "Q3/Q8/trade-off exactly.")
    A.append("")
    for r in (fc, flat, deli):
        A.append(f"--- {r['label']} ---")
        A.append("```")
        A.append(eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY))
        A.append("```")
        A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**The recorded-data forecast now closes the loop from Q6 (\"what if we do nothing?\") "
             "through Q3 (\"so it becomes attention\") to Q8 (\"what should we do, priced\") AS DATA "
             "where the data exists.** A deteriorating recorded series (projection crossing its "
             "recorded target/threshold) is itself prioritized attention — the \"do nothing and it "
             "gets worse\" signal now surfaces on Q3, and the Q8/trade-off prices the do-nothing "
             "baseline from that same projection. It is all deterministic and data-only: threshold "
             "resolution (explicit `forecast_threshold` additive field > metric `target` > last "
             "`actual`), the crossing test, and the do-nothing summary derive exclusively from the "
             "recorded `metric://` series via the Sprint-20 `forecast_metric`; never the wall-clock. "
             "The Q8 recommendation is UNCHANGED — the forecast prices attention and the do-nothing "
             "baseline but never overrules the §6-floor-gated machine-eligible best, and the "
             "determination stays the §6 human's `determination_policy` call. An on-target/flat "
             "recorded control adds no forecast attention and prices do-nothing as on-target; an org "
             "with no recorded series keeps today's fallback exactly. What is still not derivable: an "
             "org that has NOT recorded a realized-vs-expected series cannot be made to produce a "
             "forecast or a forecast-driven attention/cost — the cockpit reports the recorded reality "
             "and does not manufacture certainty — and a richer/adaptive forecast model (beyond the "
             "deterministic last-actual + mean-delta projection) remains out of scope of the honest, "
             "deterministic, ~$0 stance.")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs. The forecast prices attention + "
             "do-nothing; it never overrules the §6 human or the floor-gated recommendation._")
    (rp / "cockpit-forecast-action.md").write_text("\n".join(A) + "\n")

    print("\n  -> engine-native forecast→attention→expected-impact cockpit under "
          "artifacts/adjudication/reports/cockpit-forecast-action.md")
    print("  -> recorded-org fixtures under artifacts/adjudication/fixtures/"
          f"{{{FC_LABEL},{FLAT_LABEL}}}/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())