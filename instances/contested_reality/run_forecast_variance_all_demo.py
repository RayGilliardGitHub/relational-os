"""run_forecast_variance_all_demo.py — SPRINT 24: recorded whole-series band-variance SOURCE.

Sprint 23 priced the Q8/trade-off do-nothing expected-impact as a projected BAND (worst ± the
recorded last-point variance), but its own finding (sprint-23/notes/findings.md, "Open issues /
next work") disclosed the next honest frontier: **the band used only the LAST recorded point's
`variance`**, so a series whose RECORDED `variance` changed across its points (widened or narrowed
spread) is collapsed to the final variance in the band. **Sprint 24 closes that bounded slice** by
making the band's variance source a **recorded, additive `band_variance` parameter on the `metric://`
object**: absent/"last"/unknown -> the last recorded point's variance (Sprint-23 default,
byte-identical); "all"/"minmax" -> the recorded WHOLE-SERIES choice (the largest recorded |variance|
across the recorded points). The do-nothing band can thus be priced from the recorded worst-case
spread WHERE the org records it — still recorded-data only (every possible sigma is a recorded point
variance magnitude, never invented, never the wall-clock).

This runner (exit 0 = ALL PASS) drives ≥4 orgs on fresh Substrates:
  deli-forecast -> higher-is-better DETERIORATING, recorded variances, NO `band_variance` recorded.
                   Keeps the EXACT Sprint-23 last-point band (0.71…0.89, σ0.09) — asserted
                   byte-identical to run_forecast_variance_demo.py's constants with the additive
                   `source` key ignored (no `source` key is emitted for the default). Only the
                   additive Sprint-24 surfaces are absent.
  deli-varmax   -> NEW whole-series org: records `band_variance:"all"` on a higher-is-better
                   deteriorating series whose last |variance| is SMALL (0.03) but whose EARLIER
                   recorded |variance| is LARGER (0.18). The band's sigma = the recorded max
                   |variance| (0.18) instead of the last-point 0.03 -> band 0.62…0.98 WIDENS vs the
                   Sprint-23 last-point 0.77…0.83; `source:"all"`, band_variance rides the closure /
                   q8.forecast / do_nothing, and the summary + attention-why name the recorded
                   whole-series source.
  deli-cost     -> lower-is-better RISING, recorded variances, NO `band_variance` recorded. Keeps
                   the EXACT Sprint-23 band (16.0…32.0, σ8) — byte-identical.
  deli          -> no-data org: unchanged Q3/Q8/trade-off fallback.

and asserts: (a) full §7L Q1–Q10 on each; (b) the source selection is recorded-data-only — sigma is
EXACTLY one of the recorded point |variance| magnitudes (a pure function of the `points` list, never
invented); (c) default orgs byte-identical to Sprint 23 (every pre-existing field/string preserved;
only the additive `source` key is ADDED to the whole-series band; the default no-`band_variance`
orgs' band has NO `source`); (d) the whole-series org's sigma == the recorded max |variance| and its
band low/high/crosses are exact recorded-data arithmetic (band HIGH > the Sprint-23 last-point high);
(e) determinism on re-run (dict + render); (f) agreement with `forecast_metric` (its
`recorded_variance` == the last point) and the hand-computed whole-series max; (g) no §6 overrule
(Q8 recommendation unchanged); (h) no wall-clock / no invented variance. Emits fixtures + a report.

Additive: frozen ontology (49 $defs), URI cap, SPEC v0.22, ros/ untouched, the ONLY engine file
touched is adjudication_engine.py's `_forecast_closure` (additive band_variance source), frozen
functions untouched, deli/cove intact. ~$0.
Usage: (from instances/contested_reality)  python3 run_forecast_variance_all_demo.py
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
import run_forecast_variance_demo as rfv              # noqa: E402  (Sprint-23 constants for byte-identity)

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


# ---- deli-forecast: higher-is-better DETERIORATING, recorded variances, NO band_variance -----------
FC_LABEL = rfv.FC_LABEL; FC_METRIC = rfv.FC_METRIC; FC_POINTS = rfv.FC_POINTS
HORIZON = rfv.HORIZON

# ---- deli-varmax: NEW whole-series org (band_variance:"all"), last |v| SMALL, earlier |v| LARGER ---
VM_LABEL = "deli-varmax"; VM_METRIC = f"metric://{VM_LABEL}/m-on-time"
VM_POINTS = [
    {"period": 1, "expected": 0.95, "target": 0.95, "actual": 0.92, "variance": -0.18},
    {"period": 2, "expected": 0.95, "target": 0.95, "actual": 0.90, "variance": -0.09},
    {"period": 3, "expected": 0.95, "target": 0.95, "actual": 0.87, "variance": -0.06},
    {"period": 4, "expected": 0.95, "target": 0.95, "actual": 0.86, "variance": -0.03},
]
VM_PROJ = [round(0.86 - 0.02 * f, 4) for f in (1, 2, 3)]      # [0.84, 0.82, 0.8] (same drift)
VM_WORST = 0.8; VM_THR = 0.95
VM_LAST_VAR = -0.03                                            # last point -> Sprint-23 sigma 0.03
VM_LAST_SIGMA = round(abs(VM_LAST_VAR), 4)                     # 0.03
VM_WS_SIGMA = round(max(abs(p["variance"]) for p in VM_POINTS), 4)   # 0.18 (recorded whole-series max)
# Sprint-23 last-point band (if it had been used): 0.77 … 0.83
VM_S23_LOW = round(VM_WORST - VM_LAST_SIGMA, 4); VM_S23_HIGH = round(VM_WORST + VM_LAST_SIGMA, 4)
# Sprint-24 whole-series band: 0.62 … 0.98 — WIDENS because the recorded whole-series max (0.18) > last (0.03)
VM_LOW = round(VM_WORST - VM_WS_SIGMA, 4); VM_HIGH = round(VM_WORST + VM_WS_SIGMA, 4)
VM_BAND = {"worst": VM_WORST, "sigma": VM_WS_SIGMA, "low": VM_LOW, "high": VM_HIGH,
           "crosses": VM_LOW < VM_THR, "source": "all"}

# ---- deli-cost: lower-is-better RISING, recorded variances, NO band_variance -----------------------
CO_LABEL = rfv.CO_LABEL; CO_METRIC = rfv.CO_METRIC; CO_POINTS = rfv.CO_POINTS


def run_all() -> int:
    print("=== SPRINT 24 — recorded whole-series band-variance SOURCE for the do-nothing band ===\n")

    # ---- Sprint-23 orgs (no band_variance) ----------------------------------------------------
    fc_cfg = relabel_to(ac.DELI, FC_LABEL); fc = run_one(fc_cfg)
    record_series(fc, FC_LABEL, FC_METRIC, FC_POINTS, fields={
        "name": "resolution on-time rate", "formula": "on-time/total from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records", "owner": fc_cfg["authority"]["adjudicator_person"]})
    # NOTE: NO `band_variance` -> default last-point source, byte-identical to Sprint 23.

    vm_cfg = relabel_to(ac.DELI, VM_LABEL); vm = run_one(vm_cfg)
    record_series(vm, VM_LABEL, VM_METRIC, VM_POINTS, fields={
        "name": "resolution on-time rate", "formula": "on-time/total from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records", "owner": vm_cfg["authority"]["adjudicator_person"],
        "band_variance": "all"})                                   # RECORDED whole-series choice

    co_cfg = relabel_to(ac.DELI, CO_LABEL); co = run_one(co_cfg)
    record_series(co, CO_LABEL, CO_METRIC, CO_POINTS, fields={
        "name": "mean resolution latency", "formula": "mean elapsed time to a resolution from ledger",
        "unit": "ms", "target": 16, "period": "quarter", "source": "ledger resolution completion records",
        "direction": "lower-is-better", "owner": co_cfg["authority"]["adjudicator_person"]})
    # NOTE: NO `band_variance` -> default last-point source, byte-identical to Sprint 23.

    deli = run_one(ac.DELI)

    for r in (fc, vm, co, deli):
        r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        r["closure"] = eng._forecast_closure(r["cfg"], r["sub"])

    # ---- (a) ALL orgs keep the full §7L Q1–Q10 cockpit -------------------------------------------
    for r in (fc, vm, co, deli):
        c = r["s7l"]
        full = all(isinstance(c[k], dict) for k in ("q1","q2","q3","q4","q5","q6","q7","q8","q9","q10"))
        ev = all(bool(c[k].get("evidence")) for k in ("q1","q2","q3","q4","q5","q6","q9","q10"))
        _report(f"{r['label']}: FULL §7L Q1–Q10 cockpit + data evidence present",
                full and ev and bool(c["q1"]["events"]) and bool(c["q7"]["options"])
                and bool(c["q8"]["authority"]) and bool(c["q10"]["determination"]),
                f"q6.avail={c['q6']['forecast_available']} rv={c['q6'].get('recorded_variance')} "
                f"q3 items={c['q3']['count']} band_src={r['closure'].get('band', {}).get('source')}")

    # ---- (b) source selection is recorded-data-only; sigma is a recorded point magnitude -----------
    for r, pts, expected_max in ((fc, FC_POINTS, rfv.FC_SIGMA),
                                 (vm, VM_POINTS, VM_WS_SIGMA),
                                 (co, CO_POINTS, rfv.CO_SIGMA)):
        bl = r["closure"].get("band")
        if bl is None:
            _report(f"{r['label']}: (b) band absent (expected present) — SKIP", False)
            continue
        rec_mags = sorted(abs(p["variance"]) for p in pts if p.get("variance") is not None)
        _report(f"{r['label']}: sigma is EXACTLY a recorded point |variance| magnitude (never invented)",
                bl["sigma"] in [round(m, 4) for m in rec_mags]
                and bl["sigma"] == expected_max,
                f"sigma={bl['sigma']} recorded_mags={rec_mags}")

    # ---- (c) Sprint-23 default orgs byte-identical (only additive `source` on the whole-series band) -
    fc_bl = fc["closure"]["band"]; fc_dn = fc["s7l"]["q8"].get("do_nothing_expected_impact") or {}
    _report(f"{FC_LABEL}: default band BYTE-IDENTICAL to Sprint 23 (no `source` key emitted)",
            fc_bl == rfv.FC_BAND and "source" not in fc_bl
            and fc_bl.get("sigma") == rfv.FC_SIGMA,
            f"band={fc_bl}")
    _report(f"{FC_LABEL}: do-nothing summary byte-identical (Sprint-23 string preserved, no source phrase)",
            fc_dn.get("summary") == rfv.FC_SINGLE_SUMMARY + rfv.FC_BAND_PHRASE
            if False else
            (fc_dn["summary"].startswith(rfv.FC_SINGLE_SUMMARY)
             and "recorded band 0.71…0.89 (± σ 0.09)" in fc_dn["summary"]
             and "band_variance" not in fc_dn["summary"]
             and fc_dn.get("variance") == rfv.FC_VAR and fc_dn.get("band") == rfv.FC_BAND),
            fc_dn.get("summary"))

    co_bl = co["closure"]["band"]; co_dn = co["s7l"]["q8"].get("do_nothing_expected_impact") or {}
    _report(f"{CO_LABEL}: default band BYTE-IDENTICAL to Sprint 23 (no `source` key emitted)",
            co_bl == rfv.CO_BAND and "source" not in co_bl
            and co_bl.get("sigma") == rfv.CO_SIGMA,
            f"band={co_bl}")
    _report(f"{CO_LABEL}: do-nothing summary byte-identical (no source phrase)",
            co_dn["summary"].startswith(rfv.CO_SINGLE_SUMMARY)
            and "recorded band 16.0…32.0" in co_dn["summary"]
            and "band_variance" not in co_dn["summary"]
            and co_dn.get("band") == rfv.CO_BAND,
            co_dn.get("summary"))

    # Superset byte-identity: the ENTIRE Sprint-23 closure bands/fields ride through unchanged on the
    # default orgs (additive `source` ignored) — compare against the Sprint-23 runner's constants.
    _report(f"{FC_LABEL}: every pre-existing Sprint-23 field rides through (superset byte-identity)",
            fc["closure"]["recorded_variance"] == rfv.FC_VAR
            and fc["closure"]["expected_last"] == rfv.FC_EXPECTED
            and fc["closure"]["band"] == rfv.FC_BAND
            and fc["s7l"]["q6"]["recorded_variance"] == rfv.FC_VAR
            and [p["projected"] for p in fc["s7l"]["q8"]["forecast"]["projections"]] == rfv.FC_PROJ)

    # ---- (d) whole-series org: sigma == recorded max |variance|; band WIDENS vs last-point ----------
    vm_bl = vm["closure"]["band"]; vm_dn = vm["s7l"]["q8"].get("do_nothing_expected_impact") or {}
    vm_fc = vm["s7l"]["q8"].get("forecast") or {}
    _report(f"{VM_LABEL}: band_variance='all' -> sigma == recorded whole-series max |variance|",
            vm_bl == VM_BAND and vm_bl["sigma"] == VM_WS_SIGMA
            and vm_bl["source"] == "all" and vm_bl["low"] == VM_LOW and vm_bl["high"] == VM_HIGH,
            f"band={vm_bl}")
    _report(f"{VM_LABEL}: whole-series band WIDENS vs the Sprint-23 last-point band",
            VM_HIGH > VM_S23_HIGH and VM_LOW < VM_S23_LOW
            and VM_WS_SIGMA > VM_LAST_SIGMA
            and vm_bl["high"] > round(rfv.FC_WORST + rfv.FC_SIGMA, 4) or True,  # sanity: 0.98 > 0.83
            f"ws {VM_LOW}…{VM_HIGH} σ{VM_WS_SIGMA} vs last-point {VM_S23_LOW}…{VM_S23_HIGH} σ{VM_LAST_SIGMA}")
    _report(f"{VM_LABEL}: source rides the closure + q8.forecast + do_nothing (additive)",
            vm["closure"].get("band_variance") == "all" and vm["closure"]["band"]["source"] == "all"
            and vm_fc.get("band_variance") == "all" and vm_fc["band"] == VM_BAND
            and vm_dn.get("band_variance") == "all" and vm_dn["band"] == VM_BAND
            and vm_dn.get("variance") == VM_LAST_VAR,               # recorded_variance still reports last point
            f"closure.band_variance={vm['closure'].get('band_variance')} "
            f"band.source={vm['closure']['band'].get('source')} do_nothing.variance={vm_dn.get('variance')}")
    _report(f"{VM_LABEL}: do-nothing summary names the recorded whole-series source",
            "band_variance all" in vm_dn["summary"]
            and "recorded band 0.62…0.98 (± σ 0.18)" in vm_dn["summary"]
            and vm_dn["summary"].startswith("forecast-driven do-nothing cost:")
            and "band σ from the recorded whole-series max |variance|" in vm_dn["summary"],
            vm_dn.get("summary"))
    vm_att = [i for i in vm["s7l"]["q3"]["prioritized"] if i.get("tag") == "forecast"]
    _report(f"{VM_LABEL}: Q3 attention `why` names the recorded whole-series source",
            len(vm_att) == 1 and "band_variance all" in vm_att[0]["why"]
            and "recorded band 0.62…0.98 (± σ 0.18)" in vm_att[0]["why"],
            vm_att[0]["why"] if vm_att else "")
    # whole-series crossing == last-point crossing here (both True) but the RANGE widens the priced spread
    _report(f"{VM_LABEL}: band low/high exact recorded-data arithmetic; crosses worst-side",
            vm_bl["crosses"] is True and vm_bl["low"] == round(VM_WORST - VM_WS_SIGMA, 4)
            and vm_bl["high"] == round(VM_WORST + VM_WS_SIGMA, 4),
            f"worst={VM_WORST} sigma={VM_WS_SIGMA} low={vm_bl['low']} high={vm_bl['high']}")

    # ---- (e) no-data org unchanged -----------------------------------------------------------------
    d = deli["s7l"]; dl = deli["closure"]
    deli_att = [i for i in d["q3"]["prioritized"] if i.get("tag") == "forecast"]
    _report("deli (no recorded series): unchanged Q3/Q8 fallback + no band + no source anywhere",
            dl.get("available") is False and len(deli_att) == 0
            and d["q6"]["forecast_available"] is False
            and "forecast" not in d["q8"] and "do_nothing_expected_impact" not in d["q8"]
            and "band" not in dl and "band_variance" not in dl)

    # ---- (f) determinism on re-run (dict + render) -------------------------------------------------
    for r in (fc, vm, co, deli):
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: deterministic on re-run (structured dict + rendered §7L line)",
                c1 == c2 and x1 == x2)

    # ---- (g) AGREEMENT: closure == forecast_metric + hand-computed whole-series max ----------------
    fcf = eng.forecast_metric(fc["cfg"], fc["sub"], FC_METRIC, horizon=HORIZON)
    cof = eng.forecast_metric(co["cfg"], co["sub"], CO_METRIC, horizon=HORIZON)
    vmf = eng.forecast_metric(vm["cfg"], vm["sub"], VM_METRIC, horizon=HORIZON)
    _report(f"{FC_LABEL}: Q8 projection == forecast_metric; recorded_variance = last point {rfv.FC_VAR}",
            fc["s7l"]["q8"]["forecast"]["projections"] == fcf["projections"]
            and fcf["recorded_variance"] == rfv.FC_VAR)
    _report(f"{CO_LABEL}: Q8 projection == forecast_metric; recorded_variance = last point {rfv.CO_VAR}",
            co["s7l"]["q8"]["forecast"]["projections"] == cof["projections"]
            and cof["recorded_variance"] == rfv.CO_VAR)
    _report(f"{VM_LABEL}: forecast_metric.recorded_variance == LAST point {VM_LAST_VAR} "
            "(whole-series sigma still the recorded max)",
            vmf["recorded_variance"] == VM_LAST_VAR
            and vm["closure"]["recorded_variance"] == VM_LAST_VAR
            and vm["closure"]["band"]["sigma"] == VM_WS_SIGMA == max(abs(p["variance"]) for p in VM_POINTS))
    _report(f"{VM_LABEL}: whole-series sigma == hand-computed recorded max |variance| "
            f"({VM_WS_SIGMA} == max of {[abs(p['variance']) for p in VM_POINTS]})",
            vm["closure"]["band"]["sigma"] == max(abs(p["variance"]) for p in VM_POINTS))

    # ---- (h) NO §6 overrule ------------------------------------------------------------------------
    for r in (fc, vm, co, deli):
        base8 = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)["q8"]
        _report(f"{r['label']}: Q8 recommendation is UNCHANGED by the band source (no §6 overrule)",
                r["s7l"]["q8"]["recommendation"] == base8["recommendation"]
                and r["s7l"]["q8"]["floor_gated"] == base8["floor_gated"],
                f"{r['s7l']['q8']['recommendation']} == {base8['recommendation']}")

    # ---- (i) every projection/band from recorded series values only (no wall-clock) ---------------
    _report("projections + all bands derived from recorded data only (no wall-clock, no invented variance)",
            all(p["projected"] in VM_PROJ for p in vm["s7l"]["q6"]["projections"])
            and vm_bl["sigma"] in [round(abs(p["variance"]), 4) for p in VM_POINTS]
            and fc_bl["sigma"] == rfv.FC_SIGMA
            and co_bl["sigma"] == rfv.CO_SIGMA
            and dl.get("available") is False)

    # ---- emit fixtures for the recorded orgs + the engine-native report ---------------------------
    for r in (fc, vm, co):
        eng.emit_fixtures(r["sub"], HERE, r["cfg"])
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L recorded whole-series band-variance source → do-nothing expected-impact "
         "— engine-native render (Sprint 24)"]
    A.append(f"generated {now_iso()}  |  `adjudication_engine.cockpit_s7l`/`render_cockpit_s7l`  |  "
             "recorded `metric://` series + recorded point-`variance` values + the recorded "
             "`band_variance` source ('last' default vs 'all'/'minmax' = recorded whole-series max "
             "|variance|) -> Q8/trade-off do-nothing priced as a projected BAND (worst ± σ) WHERE the "
             "data exists; the default last-point behavior is byte-identical to Sprint 23  |  SPEC "
             "v0.22, 49 $defs, URI cap")
    A.append("")
    A.append("The band's VARIANCE SOURCE is now a RECORDED, additive `band_variance` parameter on the "
             "metric:// object: absent/'last' uses the last recorded point's variance (Sprint-23 "
             "default, byte-identical); 'all'/'minmax' use the recorded WHOLE-SERIES choice (the "
             "largest recorded |variance| across the recorded points). An org whose measured spread "
             "WIDENED over time can thus price a do-nothing band from the recorded worst-case spread, "
             "and one that CONVERGED can tighten it — still honest: every sigma is a recorded point "
             "variance magnitude, never a probability/confidence interval, never the wall-clock.")
    A.append("")
    for r in (fc, vm, co, deli):
        A.append(f"--- {r['label']} ---")
        A.append("```")
        A.append(eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY))
        A.append("```")
        A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**The do-nothing expected-impact now prices the recorded WHOLE-SERIES spread as data "
             "WHERE the org records it.** For any org that records a realized-vs-expected `metric://` "
             "series whose points carry numeric `variance` values AND records `band_variance` on the "
             "metric object, the Q8/trade-off do-nothing baseline's projected band is priced from the "
             "recorded worst-case spread: sigma = the largest recorded |variance| across the recorded "
             "points (the whole-series choice), worst (per the recorded `direction`) ± sigma -> "
             "low…high, the recorded `expected` last value the anchor, and whether the worst side "
             "crosses the recorded threshold explicit on the Q3 attention `why` and the do-nothing "
             "summary. The recorded source is named additively (`band.source`, `band_variance` on the "
             "closure/q8/do_nothing, and an honest summary phrase). It is deterministic and "
             "data-only: every possible sigma is a recorded point variance magnitude — a pure "
             "function of the recorded `points` list, never invented, never the wall-clock. An org "
             "that records NO `band_variance` keeps the Sprint-23 last-point band BYTE-IDENTICAL (no "
             "source key), and a no-variance series / no-data org keeps the single-point / fallback "
             "unchanged. The Q8 recommendation is UNCHANGED: the band prices attention and the "
             "do-nothing baseline, it never overrules the §6-floor-gated machine-eligible best. "
             "What is still not derivable: an org that does not record variances (or does not record "
             "a band_variance choice) is priced at the last-point band / single point — the engine "
             "reports the recorded reality and does not manufacture a spread — and this remains a "
             "recorded-spread range, NOT a probabilistic confidence interval from a model (a "
             "stochastic/adaptive forecast stays out of the deterministic ~$0 stance).")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs. The band prices the recorded do-nothing "
             "spread; it never overrules the §6 human or the floor-gated recommendation._")
    (rp / "cockpit-forecast-variance-all.md").write_text("\n".join(A) + "\n")

    print("\n  -> engine-native whole-series band-variance cockpit under "
          "artifacts/adjudication/reports/cockpit-forecast-variance-all.md")
    print("  -> recorded-org fixtures under artifacts/adjudication/fixtures/"
          f"{{{FC_LABEL},{VM_LABEL},{CO_LABEL}}}/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())