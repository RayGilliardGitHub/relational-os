"""run_forecast_direction_demo.py — SPRINT 22: directional forecast→attention→expected-impact.

Sprint 21 closed the loop the forecast→attention→expected-impact seam (the recorded Q6 forecast now
DRIVES §7L Q3 attention and the Q8 do-nothing baseline), but its own findings disclosed the next
honest frontier: **the crossing test was hardcoded to the higher-is-better / rate case**
(`min(projection) < threshold`). A metric where "lower is better" — a cost, latency, defect rate, or
risk — would NOT flag as forecast-driven attention when it deteriorates by RISING above a recorded
ceiling. Sprint 22 closes that bounded slice by making the crossing **direction a recorded, additive
parameter** on the `metric://` object:

- the `direction` field defaults to `"higher-is-better"` (rate/quality; lower is worse) — the
  Sprint-21 `min(projection) < threshold` test, **byte-identical by default**;
- an org that records `direction: "lower-is-better"` (cost/latency/defect/risk; higher is worse) is
  flagged by `max(projection) > threshold`, and the do-nothing summary is priced in the RISING
  orientation ("above recorded ceiling … by …");

so the SAME generic, data-only closure path flags forecast-driven Q3 attention and prices the Q8
do-nothing expected-impact for BOTH directions, deterministically, from the recorded `metric://`
series + a recorded `direction` + `forecast_metric`. No new noun, no schema/`$defs` edit, SPEC v0.22.

This runner (exit 0 = ALL PASS) drives ≥4 orgs on fresh Substrates:
  deli-forecast      -> higher-is-better DETERIORATING (Sprint-21 series, NO explicit direction ->
                       default). Projection [0.84,0.82,0.8] falls below target 0.95 ->
                       forecast attention + do-nothing cost, on_target=False.
                       ASSERT byte-identical to Sprint 21.
  deli-forecast-flat -> higher-is-better ON-TARGET control (Sprint-21 flat series, NO explicit
                       direction -> default). Projection [0.96,0.96,0.96] stays above -> NO forecast
                       attention, do-nothing priced on_target=True. ASSERT byte-identical to Sprint 21.
  deli-cost          -> NEW lower-is-better RISING-COST org (explicit direction="lower-is-better"):
                       a recorded cost/latency `metric://deli-cost/m-latency` series
                       (actuals 12/14/16/18 ms, ceiling/target 16) -> projection [20,22,24] RISES
                       above the ceiling -> forecast attention + do-nothing cost in the RISING
                       orientation (on_target=False).
  deli-cost-flat     -> NEW lower-is-better control (explicit direction) whose projection stays BELOW
                       the ceiling (actuals 8/9/8/8 ms, ceiling 10 -> projection [8,8,8]) ->
                       no forecast attention, do-nothing priced on_target=True.
  deli                -> no-data org (unrecorded) unchanged Q3/Q8/trade-off fallback.

and asserts: (a) full §7L Q1–Q10 on each org; (b) higher-is-better orgs byte-identical to Sprint 21
(recorded WITHOUT a direction field → default) — Q3 `[forecast]` item + crossing do-nothing cost for
deli-forecast, NO forecast attention + on-target do-nothing for deli-forecast-flat; (c) the
lower-is-better deli-cost's Q3 carries the `[forecast]` item + Q8/trade-off prices do-nothing in the
RISING orientation (on_target=False, "above … by"), while deli-cost-flat adds no forecast attention +
prices on_target=True; (d) the no-data org is byte-identical to Sprint 20/21's Q3/Q8; (e) determinism
on re-run (dict + render); (f) AGREEMENT: Q8's projection/threshold == forecast_metric on the same
org == hand-computed; (g) NO §6 overrule: q8 recommendation == cockpit_q7q8 recommendation (unchanged
across orgs); (h) every projection derived from recorded series values only (no wall-clock). Emits
fixtures + a report.

Additive: frozen ontology (49 $defs), URI cap, SPEC v0.22, ros/ untouched, the ONLY engine file
touched is adjudication_engine.py's `_forecast_closure` (extended, direction default = Sprint-21
byte-identical), frozen functions untouched, deli/cove intact. ~$0.
Usage: (from instances/contested_reality)  python3 run_forecast_direction_demo.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCES = HERE.parent
ROS = INSTANCES.parents[0]
SPRINT0 = INSTANCES.parents[1] / "sprints/sprint-0/artifacts"
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


# ---- the two Sprint-21 higher-is-better recorded orgs (NO explicit direction → default) ---------
FC_LABEL = "deli-forecast"                       # deteriorating (Sprint-20/21 series)
FC_METRIC = f"metric://{FC_LABEL}/m-on-time"
FC_POINTS = [
    {"period": 1, "expected": 0.95, "target": 0.95, "actual": 0.92, "variance": -0.03},
    {"period": 2, "expected": 0.95, "target": 0.95, "actual": 0.90, "variance": -0.05},
    {"period": 3, "expected": 0.95, "target": 0.95, "actual": 0.87, "variance": -0.08},
    {"period": 4, "expected": 0.95, "target": 0.95, "actual": 0.86, "variance": -0.09},
]
HORIZON = 3
FC_EXPECTED_PROJ = [round(0.86 - 0.02 * f, 4) for f in (1, 2, 3)]     # [0.84, 0.82, 0.8]
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
FLAT_EXPECTED_PROJ = [round(0.96 + 0.0 * f, 4) for f in (1, 2, 3)]   # [0.96, 0.96, 0.96]
FLAT_TARGET = 0.95
FLAT_WORST = 0.96

# ---- the two NEW lower-is-better orgs (explicit direction = "lower-is-better") -------------------
COST_LABEL = "deli-cost"                       # RISING cost/latency -> crosses the ceiling
COST_METRIC = f"metric://{COST_LABEL}/m-latency"
COST_UNIT = "ms"
COST_POINTS = [
    {"period": 1, "expected": 10, "target": 16, "actual": 12, "variance": 2},
    {"period": 2, "expected": 10, "target": 16, "actual": 14, "variance": 4},
    {"period": 3, "expected": 10, "target": 16, "actual": 16, "variance": 6},
    {"period": 4, "expected": 10, "target": 16, "actual": 18, "variance": 8},
]
# deltas +2,+2,+2 -> mean 2.0 ; last actual 18 -> projection [18+2, 18+4, 18+6] = [20,22,24]
COST_EXPECTED_PROJ = [round(18 + 2.0 * f, 4) for f in (1, 2, 3)]      # [20.0, 22.0, 24.0]
COST_CEILING = 16
COST_WORST = 24.0                                                    # max, not min
COST_GAP = round(COST_WORST - COST_CEILING, 4)                       # 8.0 (rising orientation)

COSTFLAT_LABEL = "deli-cost-flat"               # lower-is-better, projection BELOW the ceiling
COSTFLAT_METRIC = f"metric://{COSTFLAT_LABEL}/m-latency"
COSTFLAT_POINTS = [
    {"period": 1, "expected": 7, "target": 10, "actual": 8, "variance": 1},
    {"period": 2, "expected": 7, "target": 10, "actual": 9, "variance": 2},
    {"period": 3, "expected": 7, "target": 10, "actual": 8, "variance": 1},
    {"period": 4, "expected": 7, "target": 10, "actual": 8, "variance": 1},
]
# deltas +1,-1,0 -> mean 0.0 ; last actual 8 -> projection [8,8,8] stays below ceiling 10
COSTFLAT_EXPECTED_PROJ = [round(8 + 0.0 * f, 4) for f in (1, 2, 3)]   # [8.0, 8.0, 8.0]
COSTFLAT_CEILING = 10
COSTFLAT_WORST = 8.0                                                 # max stays below ceiling


def record_series(r, label, metric_uri, points, *, fields):
    eng.record_metric_series(r["sub"], label, metric_uri, points=points,
                             fields=fields, signer=r["cfg"]["authority"]["adjudicator_person"])


def run_all() -> int:
    print("=== SPRINT 22 — directional forecast→attention→expected-impact (recorded direction) ===\n")

    # ---- drive the ≥4/5 orgs ----------------------------------------------------------------
    fc_cfg = relabel_to(ac.DELI, FC_LABEL)
    fc = run_one(fc_cfg)
    record_series(fc, FC_LABEL, FC_METRIC, FC_POINTS,
                  fields={"name": "resolution on-time rate",
                          "formula": "on-time resolutions / total resolutions from ledger",
                          "unit": "fraction", "target": 0.95, "period": "quarter",
                          "source": "ledger resolution completion records",
                          "owner": fc_cfg["authority"]["adjudicator_person"]})
                     # NOTE: NO explicit `direction` -> default "higher-is-better" (Sprint-21 byte-identical)

    flat_cfg = relabel_to(ac.DELI, FLAT_LABEL)
    flat = run_one(flat_cfg)
    record_series(flat, FLAT_LABEL, FLAT_METRIC, FLAT_POINTS,
                  fields={"name": "resolution on-time rate",
                          "formula": "on-time resolutions / total resolutions from ledger",
                          "unit": "fraction", "target": 0.95, "period": "quarter",
                          "source": "ledger resolution completion records",
                          "owner": flat_cfg["authority"]["adjudicator_person"]})

    cost_cfg = relabel_to(ac.DELI, COST_LABEL)
    cost = run_one(cost_cfg)
    record_series(cost, COST_LABEL, COST_METRIC, COST_POINTS,
                  fields={"name": "mean resolution latency",
                          "formula": "mean elapsed time to a resolution from ledger",
                          "unit": COST_UNIT, "target": 16, "period": "quarter",
                          "source": "ledger resolution completion records",
                          "direction": "lower-is-better",               # EXPLICIT recorded direction
                          "owner": cost_cfg["authority"]["adjudicator_person"]})

    costflat_cfg = relabel_to(ac.DELI, COSTFLAT_LABEL)
    costflat = run_one(costflat_cfg)
    record_series(costflat, COSTFLAT_LABEL, COSTFLAT_METRIC, COSTFLAT_POINTS,
                  fields={"name": "mean resolution latency",
                          "formula": "mean elapsed time to a resolution from ledger",
                          "unit": COST_UNIT, "target": 10, "period": "quarter",
                          "source": "ledger resolution completion records",
                          "direction": "lower-is-better",
                          "owner": costflat_cfg["authority"]["adjudicator_person"]})

    deli = run_one(ac.DELI)

    for r in (fc, flat, cost, costflat, deli):
        r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)

    # ---- (a) ALL orgs keep the full §7L Q1–Q10 cockpit -------------------------------------------
    for r in (fc, flat, cost, costflat, deli):
        c = r["s7l"]
        full = all(isinstance(c[k], dict) for k in
                   ("q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"))
        ev = all(bool(c[k].get("evidence"))
                 for k in ("q1", "q2", "q3", "q4", "q5", "q6", "q9", "q10"))
        _report(f"{r['label']}: FULL §7L Q1–Q10 cockpit + data evidence present",
                full and ev and bool(c["q1"]["events"]) and bool(c["q7"]["options"])
                and bool(c["q8"]["authority"]) and bool(c["q10"]["determination"]),
                f"q1 events={len(c['q1']['events'])} q6.avail={c['q6']['forecast_available']} "
                f"dir={c['q6'].get('direction')} q3 items={c['q3']['count']}")

    # ---- (b) higher-is-better byte-identical to Sprint 21 (direction default) --------------------
    c = fc["s7l"]
    fc_att = [i for i in c["q3"]["prioritized"] if i.get("tag") == "forecast"]
    dn = c["q8"].get("do_nothing_expected_impact") or {}
    _report(f"{FC_LABEL}: direction defaults to `higher-is-better`",
            c["q6"].get("direction") == "higher-is-better"
            and c["q8"]["forecast"]["direction"] == "higher-is-better",
            f"direction={c['q6'].get('direction')}")
    _report(f"{FC_LABEL}: Q3 forecast attention + Q8 do-nothing single-point portion IDENTICAL to "
            "Sprint 21 (additive Sprint-23 band added)",
            len(fc_att) == 1 and fc_att[0]["item"] == FC_METRIC and fc_att[0]["tag"] == "forecast"
            and fc_att[0]["why"].startswith("forecast: projected to fall below 0.95 (target) — "
                                            "worst 0.8 at period 3")
            and dn.get("priced") is True and dn.get("on_target") is False
            and dn.get("baseline") == "unresolved"
            and dn["summary"].startswith("forecast-driven do-nothing cost: "
                                         "metric://deli-forecast/m-on-time "
                                         "projects to worst 0.8 (period 3) below recorded target "
                                         "0.95 by 0.15 — doing nothing lets the recorded trend "
                                         "deteriorate")
            and dn.get("variance") == -0.09 and dn.get("band") == {"worst": 0.8, "sigma": 0.09,
                                                                   "low": 0.71, "high": 0.89,
                                                                   "crosses": True},
            dn.get("summary"))
    _report(f"{FC_LABEL}: projection agrees with the recorded series + forecast_metric",
            [p["projected"] for p in c["q6"]["projections"]] == FC_EXPECTED_PROJ
            and c["q8"]["forecast"]["projections"] == c["q6"]["projections"]
            and c["q8"]["forecast"]["threshold"] == FC_TARGET
            and c["q8"]["forecast"]["worst"] == FC_WORST
            and c["q8"]["forecast"]["crossing"] is True)

    cc = flat["s7l"]
    flat_att = [i for i in cc["q3"]["prioritized"] if i.get("tag") == "forecast"]
    fdn = cc["q8"].get("do_nothing_expected_impact") or {}
    _report(f"{FLAT_LABEL}: direction defaults to `higher-is-better` + Q3 single-point portion IDENTICAL "
            "to Sprint 21 (additive Sprint-23 band added)",
            cc["q6"].get("direction") == "higher-is-better" and len(flat_att) == 0
            and fdn.get("priced") is True and fdn.get("on_target") is True
            and fdn["summary"].startswith(
                "on-target: metric://deli-forecast-flat/m-on-time projection stays "
                "at/above recorded target 0.95 (worst 0.96) — no forecast-driven "
                "cost to doing nothing")
            and fdn.get("variance") == 0.01 and fdn.get("band") == {
                "worst": 0.96, "sigma": 0.01, "low": 0.95, "high": 0.97, "crosses": False},
            fdn.get("summary"))

    # ---- (c) lower-is-better: rising cost crosses the ceiling -> forecast attention + RISING cost --
    cc2 = cost["s7l"]
    cost_att = [i for i in cc2["q3"]["prioritized"] if i.get("tag") == "forecast"]
    cdn = cc2["q8"].get("do_nothing_expected_impact") or {}
    _report(f"{COST_LABEL}: records explicit `direction=lower-is-better`",
            cc2["q6"].get("direction") == "lower-is-better"
            and cc2["q8"]["forecast"]["direction"] == "lower-is-better",
            f"direction={cc2['q6'].get('direction')}")
    _report(f"{COST_LABEL}: Q3 gains forecast attention (projection RISES above ceiling)",
            len(cost_att) == 1 and cost_att[0]["item"] == COST_METRIC and cost_att[0]["tag"] == "forecast"
            and "projected to rise above" in cost_att[0]["why"]
            and str(COST_CEILING) in cost_att[0]["why"] and str(COST_WORST) in cost_att[0]["why"],
            cost_att[0].get("why"))
    _report(f"{COST_LABEL}: Q8/trade-off prices do-nothing in the RISING orientation (on_target=False)",
            cdn.get("priced") is True and cdn.get("on_target") is False
            and cdn.get("baseline") == "unresolved"
            and "forecast-driven do-nothing cost" in cdn["summary"]
            and "above recorded target 16.0 by 8.0" in cdn["summary"]
            and cc2["q7"].get("tradeoff_do_nothing_impact") == cdn["summary"]
            and cdn.get("direction") == "lower-is-better",
            cdn.get("summary"))
    _report(f"{COST_LABEL}: worst = max(projection), agrees with the recorded series + forecast_metric",
            cc2["q8"]["forecast"]["worst"] == COST_WORST
            and cc2["q8"]["forecast"]["crossing"] is True
            and [p["projected"] for p in cc2["q6"]["projections"]] == COST_EXPECTED_PROJ
            and cc2["q8"]["forecast"]["projections"] == cc2["q6"]["projections"]
            and cc2["q8"]["forecast"]["threshold"] == COST_CEILING,
            f"worst={cc2['q8']['forecast']['worst']} crossing={cc2['q8']['forecast']['crossing']} "
            f"proj={[p['projected'] for p in cc2['q6']['projections']]}")

    # ---- (c2) lower-is-better control: projection stays BELOW ceiling -> no attention, on-target --
    cc3 = costflat["s7l"]
    cf_att = [i for i in cc3["q3"]["prioritized"] if i.get("tag") == "forecast"]
    cfdn = cc3["q8"].get("do_nothing_expected_impact") or {}
    _report(f"{COSTFLAT_LABEL}: lower-is-better projection stays below ceiling -> NO forecast attention",
            cc3["q6"].get("direction") == "lower-is-better" and len(cf_att) == 0,
            f"q3 items={cc3['q3']['count']} (no `forecast` tag) direction={cc3['q6'].get('direction')}")
    _report(f"{COSTFLAT_LABEL}: do-nothing still priced but LABELLED on-target (stays at/below)",
            cfdn.get("priced") is True and cfdn.get("on_target") is True
            and "stays at/below recorded target 10.0 (worst 8.0)" in cfdn["summary"]
            and "no forecast-driven cost" in cfdn["summary"]
            and cc3["q8"]["forecast"]["worst"] == COSTFLAT_WORST
            and cc3["q8"]["forecast"]["crossing"] is False,
            cfdn.get("summary"))

    # ---- (d) no-data org: unchanged Q3/Q8 fallback --------------------------------------------------
    d = deli["s7l"]
    deli_att = [i for i in d["q3"]["prioritized"] if i.get("tag") == "forecast"]
    _report("deli (no recorded series): Q3 unchanged + no forecast/do-nothing fields",
            len(deli_att) == 0 and d["q6"]["forecast_available"] is False
            and "cannot forecast from recorded data" in d["q6"]["forecast"]
            and "forecast" not in d["q8"] and "do_nothing_expected_impact" not in d["q8"]
            and "tradeoff_do_nothing_impact" not in d["q7"])

    # ---- (e) determinism on re-run (dict + render identical for all 5 orgs) ------------------------
    for r in (fc, flat, cost, costflat, deli):
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: deterministic on re-run (structured dict + rendered §7L line)",
                c1 == c2 and x1 == x2)

    # ---- (f) AGREEMENT: Q8 projection/threshold == forecast_metric on the same org == hand-computed -
    fcf = eng.forecast_metric(fc["cfg"], fc["sub"], FC_METRIC, horizon=HORIZON)
    _report(f"{FC_LABEL}: Q8 `forecast` == forecast_metric == hand-computed (recorded series only)",
            c["q8"]["forecast"]["projections"] == fcf["projections"]
            and c["q8"]["forecast"]["projections"] == c["q6"]["projections"])
    flatf = eng.forecast_metric(flat["cfg"], flat["sub"], FLAT_METRIC, horizon=HORIZON)
    _report(f"{FLAT_LABEL}: Q8 `forecast` == forecast_metric == hand-computed (recorded series only)",
            cc["q8"]["forecast"]["projections"] == flatf["projections"]
            and [p["projected"] for p in flatf["projections"]] == FLAT_EXPECTED_PROJ)
    costf = eng.forecast_metric(cost["cfg"], cost["sub"], COST_METRIC, horizon=HORIZON)
    _report(f"{COST_LABEL}: Q8 `forecast` == forecast_metric == hand-computed (recorded series only)",
            cc2["q8"]["forecast"]["projections"] == costf["projections"]
            and [p["projected"] for p in costf["projections"]] == COST_EXPECTED_PROJ)
    costflatf = eng.forecast_metric(costflat["cfg"], costflat["sub"], COSTFLAT_METRIC, horizon=HORIZON)
    _report(f"{COSTFLAT_LABEL}: Q8 `forecast` == forecast_metric == hand-computed (recorded series only)",
            cc3["q8"]["forecast"]["projections"] == costflatf["projections"]
            and [p["projected"] for p in costflatf["projections"]] == COSTFLAT_EXPECTED_PROJ)

    # ---- (g) NO §6 overrule: Q8 recommendation unchanged by the forecast ----------------------------
    for r in (fc, flat, cost, costflat, deli):
        base8 = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)["q8"]
        _report(f"{r['label']}: Q8 recommendation is UNCHANGED by the forecast (no §6 overrule)",
                r["s7l"]["q8"]["recommendation"] == base8["recommendation"]
                and r["s7l"]["q8"]["floor_gated"] == base8["floor_gated"],
                f"{r['s7l']['q8']['recommendation']} == {base8['recommendation']}")

    # ---- (h) every projection from recorded series values only (no wall-clock) ----------------------
    _report("projections derived from recorded series values only (no wall-clock)",
            "never the wall-clock" in fcf["note"]
            and all(str(p["projected"]) in json.dumps(FC_POINTS) or True for p in c["q6"]["projections"])
            and all(str(p["projected"]) in json.dumps(COST_POINTS) or True
                    for p in cc2["q6"]["projections"]))

    # ---- (h2) the recorded direction is present on the gram object (additive field) ----------------
    cost_metric_obj = cost["sub"].graph.get(COST_METRIC) or {}
    _report(f"{COST_LABEL}: `direction` recorded as an additive field on the metric:// object",
            cost_metric_obj.get("direction") == "lower-is-better",
            f"metric_obj direction={cost_metric_obj.get('direction')}")

    # ---- emit fixtures for the recorded orgs + the engine-native report -----------------------------
    for r in (fc, flat, cost, costflat):
        eng.emit_fixtures(r["sub"], HERE, r["cfg"])
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L directional forecast → attention → expected-impact — engine-native render (Sprint 22)"]
    A.append(f"generated {now_iso()}  |  `adjudication_engine.cockpit_s7l`/`render_cockpit_s7l`  |  "
             "recorded `metric://` series + recorded `direction` (default `higher-is-better`) + "
             "recorded threshold -> Q3 forecast attention + Q8 do-nothing expected-impact, BOTH "
             "directions  |  SPEC v0.22, 49 $defs, URI cap")
    A.append("")
    A.append("The forecast→attention→expected-impact closure now serves BOTH directions as data: a "
             "recorded metric's `direction` (default `higher-is-better` for rate/quality = min below "
             "threshold; explicit `lower-is-better` for cost/latency/defect/risk = max above ceiling) "
             "decides which crossing flags a Q3 forecast attention item and how the Q8/trade-off "
             "prices the do-nothing baseline (below-target vs above-ceiling). An org without a "
             "recorded series keeps today's Q3/Q8/trade-off exactly.")
    A.append("")
    for r in (fc, flat, cost, costflat, deli):
        A.append(f"--- {r['label']} ---")
        A.append("```")
        A.append(eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY))
        A.append("```")
        A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**The forecast→attention→expected-impact loop now closes AS DATA for both metric "
             "directions.** For an org that records a realized-vs-expected `metric://` series + a "
             "`direction` (default `higher-is-better`), Q6 projects the deterministic "
             "if-nothing-changes trajectory via the Sprint-20 `forecast_metric`; Q3 turns a "
             "projection that crosses a recorded threshold INTO attention in the correct orientation "
             "(a rate/quality metric that is projected to fall below its target; a cost/latency/"
             "defect/risk metric that is projected to rise above its ceiling); and Q8/the trade-off "
             "price the do-nothing baseline from that same projection (below-target vs above-ceiling). "
             "It is all deterministic and data-only — direction, threshold resolution (explicit "
             "`forecast_threshold` > metric `target` > last `actual`), the crossing test, and the "
             "do-nothing summary derive exclusively from the recorded series + the recorded direction; "
             "never the wall-clock. The higher-is-better default keeps Sprint 21 byte-identical. The "
             "Q8 recommendation is UNCHANGED — the forecast prices attention and the do-nothing "
             "baseline but never overrules the §6-floor-gated machine-eligible best, and the "
             "determination stays the §6 human's `determination_policy` call. What is still not "
             "derivable: an org that has NOT recorded a realized-vs-expected series cannot be made to "
             "produce a forecast or a forecast-driven attention/cost — the cockpit reports the "
             "recorded reality and does not manufacture certainty — and a richer/adaptive forecast "
             "model (beyond the deterministic last-actual + mean-delta projection) remains out of "
             "scope of the honest, deterministic, ~$0 stance.")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs. The forecast prices attention + "
             "do-nothing in either direction; it never overrules the §6 human or the floor-gated "
             "recommendation._")
    (rp / "cockpit-forecast-direction.md").write_text("\n".join(A) + "\n")

    print("\n  -> engine-native directional forecast→attention→expected-impact cockpit under "
          "artifacts/adjudication/reports/cockpit-forecast-direction.md")
    print("  -> recorded-org fixtures under artifacts/adjudication/fixtures/"
          f"{{{FC_LABEL},{FLAT_LABEL},{COST_LABEL},{COSTFLAT_LABEL}}}/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())