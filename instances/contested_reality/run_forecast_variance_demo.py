"""run_forecast_variance_demo.py — SPRINT 23: recorded-variance projected band for do-nothing pricing.

Sprint 22 closed the crossing-direction seam but its own finding (sprint-22/notes/findings.md) disclosed
the next honest frontier: the Q8/trade-off do-nothing expected-impact was priced as a SINGLE POINT gap
(worst vs the recorded threshold) that IGNORES the RECORDED variance the engine already computes and
renders on Q6. Sprint 23 closes that bounded slice additively: when the recorded `metric://` series'
last point carries a numeric `variance`, the do-nothing pricing reports a projected BAND
(worst ± the recorded variance = low…high), surfaced on the closure, `q8["forecast"]`,
`do_nothing_expected_impact`, and the do-nothing summary + Q3 attention `why`. A series with NO
recorded variance keeps the Sprint-22 single-point output BYTE-IDENTICAL. This is a recorded-data
spread (the projected worst bounded by the recorded last variance), NOT a probability/confidence
interval, never the wall-clock.

This runner (exit 0 = ALL PASS) drives ≥4 orgs on fresh Substrates:
  deli-forecast -> higher-is-better DETERIORATING with RECORDED variances (Sprint-22 series). GAINS
                   the band (0.71…0.89, σ0.09) + an additive summary phrase; every pre-existing
                   single-point field/string is preserved (superset byte-identity, asserted against
                   the Sprint-22 values with the additive keys ignored).
  deli-flat2    -> NEW variance-less control: a recorded series whose points carry NO `variance`.
                   Stays EXACTLY the Sprint-22 single-point output — no band, no variance/expected
                   anchor, summary byte-identical.
  deli-cost     -> lower-is-better RISING with RECORDED variances. Projection [20,22,24] crosses the
                   16 ceiling; band high 32.0 prices a WORSE do-nothing than the single point 24.0.
  deli          -> no-data org (unrecorded): unchanged Q3/Q8/trade-off fallback.

and asserts: (a) full §7L Q1–Q10 on each; (b) the band is derived ONLY from recorded values — worst
(per direction) + recorded last variance (magnitude σ) + the recorded threshold, low/high EXACT
recorded-data arithmetic; (c) on the variance-carrying orgs the do-nothing summary surfaces the
recorded variance while every pre-existing single-point field/branch stays byte-identical (the
Sprint-22 fields compared with the additive keys ignored), and the Q3 attention `why` names the band;
(d) the variance-less control is EXACTLY the single-point output (no additive keys anywhere); (e)
determinism on re-run (dict + render); (f) AGREEMENT: the projection used in Q3/Q8 == forecast_metric
on the same org (incl. its `recorded_variance`); (g) NO §6 overrule (Q8 recommendation unchanged);
(h) every projection/band value derived from recorded series values only (no wall-clock, no invented
variance). Emits fixtures + a report.

Additive: frozen ontology (49 $defs), URI cap, SPEC v0.22, ros/ untouched, the ONLY engine file
touched is adjudication_engine.py's `_forecast_closure` + `render_cockpit_s7l` (additive band),
frozen functions untouched, deli/cove intact. ~$0.
Usage: (from instances/contested_reality)  python3 run_forecast_variance_demo.py
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
    eng.validate_config(cfg)
    sub = Substrate(ledger_uri=cfg["ledger_name"])
    seed_trust(cfg, sub)
    ok, _, du, sub = eng.run_scenario(cfg, sub)
    d = sub.graph.get(du)
    return {"cfg": cfg, "label": cfg["label"], "dispute_uri": du, "sub": sub,
            "determination": d.get("determination")}


def record_series(r, label, metric_uri, points, *, fields):
    eng.record_metric_series(r["sub"], label, metric_uri, points=points, fields=fields,
                             signer=r["cfg"]["authority"]["adjudicator_person"])


# ---- deli-forecast: higher-is-better DETERIORATING, recorded variances present --------------------
FC_LABEL = "deli-forecast"; FC_METRIC = f"metric://{FC_LABEL}/m-on-time"
FC_POINTS = [
    {"period": 1, "expected": 0.95, "target": 0.95, "actual": 0.92, "variance": -0.03},
    {"period": 2, "expected": 0.95, "target": 0.95, "actual": 0.90, "variance": -0.05},
    {"period": 3, "expected": 0.95, "target": 0.95, "actual": 0.87, "variance": -0.08},
    {"period": 4, "expected": 0.95, "target": 0.95, "actual": 0.86, "variance": -0.09},
]
HORIZON = 3
FC_PROJ = [round(0.86 - 0.02 * f, 4) for f in (1, 2, 3)]      # [0.84, 0.82, 0.8]
FC_WORST = 0.8; FC_THR = 0.95; FC_VAR = -0.09; FC_EXPECTED = 0.95
FC_SIGMA = round(abs(FC_VAR), 4); FC_LOW = round(FC_WORST - FC_SIGMA, 4)
FC_HIGH = round(FC_WORST + FC_SIGMA, 4)                        # 0.71 … 0.89, band crosses True
FC_BAND = {"worst": FC_WORST, "sigma": FC_SIGMA, "low": FC_LOW, "high": FC_HIGH, "crosses": True}
FC_SINGLE_SUMMARY = ("forecast-driven do-nothing cost: metric://deli-forecast/m-on-time "
                     "projects to worst 0.8 (period 3) below recorded target 0.95 by 0.15 — "
                     "doing nothing lets the recorded trend deteriorate")
FC_SINGLE_WHY = "forecast: projected to fall below 0.95 (target) — worst 0.8 at period 3"

# ---- deli-flat2: NEW variance-less control (recorded series, NO `variance` on any point) ----------
FL2_LABEL = "deli-flat2"; FL2_METRIC = f"metric://{FL2_LABEL}/m-on-time"
FL2_POINTS = [  # NOTE: no `variance` key on any point -> no band -> byte-identical single-point
    {"period": 1, "expected": 0.95, "target": 0.95, "actual": 0.96},
    {"period": 2, "expected": 0.95, "target": 0.95, "actual": 0.97},
    {"period": 3, "expected": 0.95, "target": 0.95, "actual": 0.96},
    {"period": 4, "expected": 0.95, "target": 0.95, "actual": 0.96},
]
FL2_PROJ = [round(0.96 + 0.0 * f, 4) for f in (1, 2, 3)]       # [0.96, 0.96, 0.96]
FL2_WORST = 0.96; FL2_THR = 0.95
FL2_SINGLE_SUMMARY = ("on-target: metric://deli-flat2/m-on-time projection stays at/above recorded "
                      "target 0.95 (worst 0.96) — no forecast-driven cost to doing nothing")

# ---- deli-cost: lower-is-better RISING, recorded variances present ---------------------------------
CO_LABEL = "deli-cost"; CO_METRIC = f"metric://{CO_LABEL}/m-latency"
CO_POINTS = [
    {"period": 1, "expected": 10, "target": 16, "actual": 12, "variance": 2},
    {"period": 2, "expected": 10, "target": 16, "actual": 14, "variance": 4},
    {"period": 3, "expected": 10, "target": 16, "actual": 16, "variance": 6},
    {"period": 4, "expected": 10, "target": 16, "actual": 18, "variance": 8},
]
CO_PROJ = [round(18 + 2.0 * f, 4) for f in (1, 2, 3)]          # [20.0, 22.0, 24.0]
CO_WORST = 24.0; CO_THR = 16.0; CO_VAR = 8.0; CO_EXPECTED = 10.0
CO_SIGMA = round(abs(CO_VAR), 4); CO_LOW = round(CO_WORST - CO_SIGMA, 4)
CO_HIGH = round(CO_WORST + CO_SIGMA, 4)                        # 16.0 … 32.0 (high 32 > ceiling 16)
CO_BAND = {"worst": CO_WORST, "sigma": CO_SIGMA, "low": CO_LOW, "high": CO_HIGH, "crosses": True}
CO_SINGLE_SUMMARY = ("forecast-driven do-nothing cost: metric://deli-cost/m-latency projects to "
                     "worst 24.0 (period 3) above recorded target 16.0 by 8.0 — doing nothing lets "
                     "the recorded trend deteriorate")


def run_all() -> int:
    print("=== SPRINT 23 — recorded-variance projected band for the do-nothing expected-impact ===\n")

    fc_cfg = relabel_to(ac.DELI, FC_LABEL); fc = run_one(fc_cfg)
    record_series(fc, FC_LABEL, FC_METRIC, FC_POINTS, fields={
        "name": "resolution on-time rate", "formula": "on-time/total from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records", "owner": fc_cfg["authority"]["adjudicator_person"]})

    fl2_cfg = relabel_to(ac.DELI, FL2_LABEL); fl2 = run_one(fl2_cfg)
    record_series(fl2, FL2_LABEL, FL2_METRIC, FL2_POINTS, fields={
        "name": "resolution on-time rate", "formula": "on-time/total from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records", "owner": fl2_cfg["authority"]["adjudicator_person"]})

    co_cfg = relabel_to(ac.DELI, CO_LABEL); co = run_one(co_cfg)
    record_series(co, CO_LABEL, CO_METRIC, CO_POINTS, fields={
        "name": "mean resolution latency", "formula": "mean elapsed time to a resolution from ledger",
        "unit": "ms", "target": 16, "period": "quarter", "source": "ledger resolution completion records",
        "direction": "lower-is-better", "owner": co_cfg["authority"]["adjudicator_person"]})

    deli = run_one(ac.DELI)

    for r in (fc, fl2, co, deli):
        r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        r["closure"] = eng._forecast_closure(r["cfg"], r["sub"])

    # ---- (a) ALL orgs keep the full §7L Q1–Q10 cockpit -------------------------------------------
    for r in (fc, fl2, co, deli):
        c = r["s7l"]
        full = all(isinstance(c[k], dict) for k in ("q1","q2","q3","q4","q5","q6","q7","q8","q9","q10"))
        ev = all(bool(c[k].get("evidence")) for k in ("q1","q2","q3","q4","q5","q6","q9","q10"))
        _report(f"{r['label']}: FULL §7L Q1–Q10 cockpit + data evidence present",
                full and ev and bool(c["q1"]["events"]) and bool(c["q7"]["options"])
                and bool(c["q8"]["authority"]) and bool(c["q10"]["determination"]),
                f"q6.avail={c['q6']['forecast_available']} rv={c['q6'].get('recorded_variance')} "
                f"q3 items={c['q3']['count']}")

    # ---- (b) band derived ONLY from recorded values; low/high EXACT arithmetic --------------------
    cfc = fc["s7l"]; fcl = fc["closure"]
    _report(f"{FC_LABEL}: band derived from recorded worst + recorded variance + threshold",
            fcl.get("band") == FC_BAND and fcl.get("recorded_variance") == FC_VAR
            and fcl.get("expected_last") == FC_EXPECTED
            and fcl["band"]["low"] == round(FC_WORST - abs(FC_VAR), 4)
            and fcl["band"]["high"] == round(FC_WORST + abs(FC_VAR), 4)
            and fcl["band"]["crosses"] is True, f"band={fcl.get('band')}")
    cco = co["s7l"]; col = co["closure"]
    _report(f"{CO_LABEL}: band's worst side (high) prices a WORSE do-nothing than the single point",
            col.get("band") == CO_BAND and col.get("recorded_variance") == 8.0
            and col.get("expected_last") == 10.0
            and col["band"]["high"] > col["band"]["worst"]           # 32.0 > 24.0
            and col["band"]["high"] > CO_THR,                         # 32.0 > 16.0 ceiling
            f"high={col['band']['high']} worst={col['band']['worst']} ceiling={CO_THR}")

    # ---- (c) variance orgs: additive band rides closure + q8.forecast + do_nothing ----------------
    dn = cfc["q8"].get("do_nothing_expected_impact") or {}
    fcast = cfc["q8"].get("forecast") or {}
    _report(f"{FC_LABEL}: additive band/variance/expected anchor present + do-nothing summary "
            "surfaces the recorded variance",
            dn.get("band") == FC_BAND and dn.get("variance") == FC_VAR
            and dn.get("expected_last") == FC_EXPECTED
            and fcast.get("band") == FC_BAND and fcast.get("recorded_variance") == FC_VAR
            and fcast.get("expected_last") == FC_EXPECTED
            and "recorded band 0.71…0.89 (± σ 0.09)" in dn["summary"]
            and "recorded band" in dn["summary"], dn.get("summary"))
    _report(f"{FC_LABEL}: every pre-existing Sprint-22 single-point field/string BYTE-IDENTICAL "
            "(additive keys ignored)",
            dn.get("priced") is True and dn.get("on_target") is False
            and dn.get("baseline") == "unresolved" and dn.get("metric") == FC_METRIC
            and dn.get("direction") == "higher-is-better"
            and dn["summary"].startswith(FC_SINGLE_SUMMARY)
            and fcast["worst"] == FC_WORST and fcast["threshold"] == FC_THR
            and fcast["crossing"] is True
            and [p["projected"] for p in fcast["projections"]] == FC_PROJ
            and cfc["q6"]["recorded_variance"] == FC_VAR)
    fc_att = [i for i in cfc["q3"]["prioritized"] if i.get("tag") == "forecast"]
    _report(f"{FC_LABEL}: Q3 attention `why` preserves the Sprint-22 string + names the band",
            len(fc_att) == 1 and fc_att[0]["why"].startswith(FC_SINGLE_WHY)
            and "recorded band 0.71…0.89 (± σ 0.09)" in fc_att[0]["why"], fc_att[0]["why"] if fc_att else "")

    cdn = cco["q8"].get("do_nothing_expected_impact") or {}
    _report(f"{CO_LABEL}: do-nothing summary surfaces the recorded band (rises above ceiling)",
            cdn.get("band") == CO_BAND and cdn.get("variance") == 8.0
            and any("recorded band 16.0…32.0" in c for c in (cdn["summary"],))
            and cdn["summary"].startswith(CO_SINGLE_SUMMARY)
            and cdn.get("on_target") is False,
            cdn.get("summary"))

    # ---- (d) variance-less control is EXACTLY the single-point output -----------------------------
    cfl2 = fl2["s7l"]; fl2l = fl2["closure"]
    fl2dn = cfl2["q8"].get("do_nothing_expected_impact") or {}
    fl2f = cfl2["q8"].get("forecast") or {}
    _report(f"{FL2_LABEL}: recorded series exists but NO recorded variance -> closure has no band",
            fl2l.get("available") is True and "band" not in fl2l
            and "recorded_variance" not in fl2l and "expected_last" not in fl2l
            and cfl2["q6"]["recorded_variance"] is None, f"closure keys={sorted(fl2l.keys())}")
    _report(f"{FL2_LABEL}: do-nothing + forecast are EXACTLY the Sprint-22 single-point output "
            "(no additive keys)",
            set(fl2dn.keys()) == {"baseline","priced","on_target","summary","metric","direction"}
            and fl2dn["summary"] == FL2_SINGLE_SUMMARY     # byte-identical, not a prefix
            and fl2dn.get("on_target") is True and fl2dn.get("band") is None
            and set(fl2f.keys()) == {"projections","threshold","source","worst","crossing","direction"}
            and fl2f["worst"] == FL2_WORST and fl2f["crossing"] is False
            and [p["projected"] for p in fl2f["projections"]] == FL2_PROJ,
            fl2dn.get("summary"))

    # ---- (d2) no-data org unchanged ---------------------------------------------------------------
    d = deli["s7l"]; dl = deli["closure"]
    deli_att = [i for i in d["q3"]["prioritized"] if i.get("tag") == "forecast"]
    _report("deli (no recorded series): unchanged Q3/Q8 fallback + no band anywhere",
            dl.get("available") is False and len(deli_att) == 0
            and d["q6"]["forecast_available"] is False
            and "forecast" not in d["q8"] and "do_nothing_expected_impact" not in d["q8"]
            and "band" not in dl and "recorded_variance" not in dl)

    # ---- (e) determinism on re-run (dict + render) ------------------------------------------------
    for r in (fc, fl2, co, deli):
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: deterministic on re-run (structured dict + rendered §7L line)",
                c1 == c2 and x1 == x2)

    # ---- (f) AGREEMENT: Q3/Q8 projection == forecast_metric (incl. recorded_variance) -------------
    fcf = eng.forecast_metric(fc["cfg"], fc["sub"], FC_METRIC, horizon=HORIZON)
    _report(f"{FC_LABEL}: Q8 projection/threshold == forecast_metric, recorded_variance agrees",
            cfc["q8"]["forecast"]["projections"] == fcf["projections"]
            and cfc["q8"]["forecast"]["projections"] == cfc["q6"]["projections"]
            and fcf["recorded_variance"] == FC_VAR
            and cfc["q8"]["forecast"]["band"] == FC_BAND)
    fl2f_metric = eng.forecast_metric(fl2["cfg"], fl2["sub"], FL2_METRIC, horizon=HORIZON)
    _report(f"{FL2_LABEL}: forecast_metric reports NO recorded variance (honest no-variance data)",
            fl2f_metric["available"] is True and fl2f_metric["recorded_variance"] is None
            and fl2f_metric["expected_last"] == 0.95)
    cof = eng.forecast_metric(co["cfg"], co["sub"], CO_METRIC, horizon=HORIZON)
    _report(f"{CO_LABEL}: Q8 projection == forecast_metric, recorded_variance = {CO_VAR}",
            cco["q8"]["forecast"]["projections"] == cof["projections"]
            and cof["recorded_variance"] == CO_VAR)

    # ---- (g) NO §6 overrule ----------------------------------------------------------------------
    for r in (fc, fl2, co, deli):
        base8 = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)["q8"]
        _report(f"{r['label']}: Q8 recommendation is UNCHANGED by the band/forecast (no §6 overrule)",
                r["s7l"]["q8"]["recommendation"] == base8["recommendation"]
                and r["s7l"]["q8"]["floor_gated"] == base8["floor_gated"],
                f"{r['s7l']['q8']['recommendation']} == {base8['recommendation']}")

    # ---- (h) every projection/band from recorded series values only (no wall-clock) --------------
    _report("projections + band derived from recorded data only (no wall-clock, no invented variance)",
            all(p["projected"] in FC_PROJ for p in cfc["q6"]["projections"])         # derived set
            and fcl["band"]["low"] == FC_LOW and fcl["band"]["high"] == FC_HIGH
            and col["band"]["low"] == CO_LOW and col["band"]["high"] == CO_HIGH
            and cfl2["q6"]["recorded_variance"] is None)                            # control: no fabrication

    # ---- emit fixtures for the recorded orgs + the engine-native report ---------------------------
    for r in (fc, fl2, co):
        eng.emit_fixtures(r["sub"], HERE, r["cfg"])
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L recorded-variance band → do-nothing expected-impact — engine-native render (Sprint 23)"]
    A.append(f"generated {now_iso()}  |  `adjudication_engine.cockpit_s7l`/`render_cockpit_s7l`  |  "
             "recorded `metric://` series + recorded last-point `variance` (magnitude σ) -> Q8/"
             "trade-off do-nothing priced as a projected BAND (worst ± σ) where the data exists; a "
             "no-variance series keeps the Sprint-22 single-point output byte-identical  |  SPEC "
             "v0.22, 49 $defs, URI cap")
    A.append("")
    A.append("The do-nothing expected-impact now prices the RECORDED SPREAD, not just the single "
             "point: when the org's recorded `metric://` series carries a numeric `variance` on its "
             "last point, the closure reports a projected band low…high = worst ± |recorded variance| "
             "and whether the WORST side of the band crosses the recorded threshold. This is a "
             "recorded-data spread — it bounds the deterministic projection by the recorded historical "
             "variance — NOT a probability/confidence interval and never the wall-clock.")
    A.append("")
    for r in (fc, fl2, co, deli):
        A.append(f"--- {r['label']} ---")
        A.append("```")
        A.append(eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY))
        A.append("```")
        A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**The do-nothing expected-impact now prices the recorded spread as data WHERE it "
             "exists.** For any org that records a realized-vs-expected `metric://` series whose last "
             "point carries a numeric `variance`, the Q8/trade-off do-nothing baseline is priced as a "
             "projected band — worst (per the recorded `direction`) ± the recorded variance as a "
             "magnitude — reported as low…high, the recorded `expected` last value surfaced as the "
             "anchor, and whether the worst side crosses the threshold made explicit on the Q3 "
             "attention `why` and the do-nothing summary. It is deterministic and data-only: worst, "
             "the recorded variance, and the threshold are the only inputs to low/high and crosses; "
             "never the wall-clock, never an invented variance. A series with no recorded variance — "
             "or a no-data org — keeps the Sprint-22 single-point/fallback behavior BYTE-IDENTICAL. "
             "The Q8 recommendation is UNCHANGED: the band prices attention and the do-nothing "
             "baseline, it never overrules the §6-floor-gated machine-eligible best. What is still "
             "not derivable: a series that does NOT record a variance cannot be made to produce a "
             "band (the engine reports the recorded reality, it does not manufacture a spread), and "
             "this is a recorded spread, NOT a probabilistic confidence interval from a model — a "
             "stochastic/adaptive forecast remains out of scope of the honest, deterministic, ~$0 "
             "stance.")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs. The band prices the recorded do-nothing "
             "spread; it never overrules the §6 human or the floor-gated recommendation._")
    (rp / "cockpit-forecast-variance.md").write_text("\n".join(A) + "\n")

    print("\n  -> engine-native recorded-variance band cockpit under "
          "artifacts/adjudication/reports/cockpit-forecast-variance.md")
    print("  -> recorded-org fixtures under artifacts/adjudication/fixtures/"
          f"{{{FC_LABEL},{FL2_LABEL},{CO_LABEL}}}/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())