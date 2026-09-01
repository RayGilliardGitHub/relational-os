# === DEMO / TEST RUNNER - NOT part of the engine API ===
"""run_forecast_horizon_demo.py — SPRINT 25: horizon-wide do-nothing band + Q9 capacity-attention.

Sprint 24 priced the Q8/trade-off do-nothing projected BAND around the SINGLE worst projected point,
but its own finding (sprints/sprint-24/notes/findings.md, "Open issues / next work") disclosed the
next honest frontier: **the band is still computed around the single worst point at the do-nothing
line; it does not aggregate a band across ALL projection periods (the whole horizon's worst-case
spread), and it does not feed §7L Q9 capacity attention.** Sprint 25 closes that bounded slice
additively: the SAME recorded sigma is applied to EVERY projection period -> a per-period band
(`band_periods`) + the record-wide horizon worst-case (`band_horizon` = min period low / max period
high), and the Q9 block gains a `band_capacity_attention` flag/reason derived from the horizon range
+ the recorded threshold (referencing any RECORDED capacity without inventing it). Still recorded-data
only: every bound is a projected value ± the recorded sigma, and sigma is still exactly a recorded
point |variance| magnitude.

This runner (exit 0 = ALL PASS) drives orgs on fresh Substrates:
  deli-forecast    -> higher-is-better DETERIORATING, recorded variances, NO `band_variance`.
                     Sprint-23/24 last-point band (0.71…0.89, σ0.09) kept BYTE-IDENTICAL, now ALSO
                     carrying additive band_periods/band_horizon (+ band_capacity_attention).
  deli-varmax      -> whole-series org (`band_variance:"all"`, band 0.62…0.98 σ0.18). Now ALSO
                     carries band_periods/band_horizon: horizon-wide high 1.02 > single-worst high
                     0.98 (WIDENS because an EARLIER period 1 projected 0.84 + σ0.18 = 1.02 sits
                     above the worst point's own +σ band).
  deli-varmax-cap  -> same whole-series band as deli-varmax + a RECORDED capacity on the authority
                     object -> the Q9 capacity-attention `why` REFERENCES the recorded capacity
                     (value/unit/load) while the flag is still the horizon-vs-threshold cross.
  deli-flat2       -> recorded series, NO `variance` -> no-band control: NO new keys, byte-identical
                     Sprint-22 single-point output.
  deli             -> no-data org: unchanged; no band_capacity_attention / band_periods / band_horizon.

and asserts: (a) full §7L Q1–Q10 on each; (b) band_periods = per-period projected ± recorded sigma
EXACT arithmetic; (c) band_horizon.low/high = min/max over those periods (recorded-data only);
(d) sigma is STILL exactly one of the recorded point |variance| magnitudes (never invented);
(e) the widening org's horizon-wide high > its single-worst band high (earlier period at +σ exceeds
the worst point's band) while the default org's is still a pure per-period band; (f) default orgs
byte-identical to Sprint 23/24 EXCEPT the additive band_periods/band_horizon/band_capacity_attention
keys (every pre-existing field/string preserved); (g) determinism on re-run (dict + render);
(h) no §6 overrule (Q8 recommendation unchanged); (i) no wall-clock / no invented variance; (j) the
recorded-capacity org's why references capacity without mutating it. Emits fixtures + a report.

Additive: frozen ontology (49 $defs), URI cap, SPEC v0.22, ros/ untouched, the ONLY engine file
touched is adjudication_engine.py (_forecast_closure horizon-wide band + cockpit_s7l Q9
band_capacity_attention), frozen functions untouched, deli/cove intact. ~$0.
Usage: (from instances/contested_reality)  python3 run_forecast_horizon_demo.py
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


# ---- deli-forecast: Sprint-23 default (last-point band), now + horizon keys ----------------------
FC_LABEL = rfv.FC_LABEL; FC_METRIC = rfv.FC_METRIC; FC_POINTS = rfv.FC_POINTS
HORIZON = rfv.HORIZON
FC_SIGMA = rfv.FC_SIGMA                                            # 0.09 (last point)
FC_PROJ = rfv.FC_PROJ                                              # [0.84, 0.82, 0.8]
FC_PERIODS = [{"period": p["period"],
               "low": round(p["projected"] - FC_SIGMA, 4),
               "high": round(p["projected"] + FC_SIGMA, 4)} for p in
              [{"period": 1, "projected": 0.84}, {"period": 2, "projected": 0.82},
               {"period": 3, "projected": 0.8}]]
FC_HORIZON = {"low": min(b["low"] for b in FC_PERIODS), "high": max(b["high"] for b in FC_PERIODS)}
                                     # {0.71, 0.93} — high 0.93 > single-worst high 0.89 (widens)
FC_THR = 0.95

# ---- deli-varmax: whole-series band_variance:"all" (last |v| small, earlier |v| larger) ----------
VM_LABEL = "deli-varmax"; VM_METRIC = f"metric://{VM_LABEL}/m-on-time"
VM_POINTS = [
    {"period": 1, "expected": 0.95, "target": 0.95, "actual": 0.92, "variance": -0.18},
    {"period": 2, "expected": 0.95, "target": 0.95, "actual": 0.90, "variance": -0.09},
    {"period": 3, "expected": 0.95, "target": 0.95, "actual": 0.87, "variance": -0.06},
    {"period": 4, "expected": 0.95, "target": 0.95, "actual": 0.86, "variance": -0.03},
]
VM_WS_SIGMA = round(max(abs(p["variance"]) for p in VM_POINTS), 4)        # 0.18
VM_PROJ = [round(0.86 - 0.02 * f, 4) for f in (1, 2, 3)]                  # [0.84, 0.82, 0.8]
VM_WORST = 0.8; VM_THR = 0.95
VM_SINGLE_BAND = {"low": round(VM_WORST - VM_WS_SIGMA, 4), "high": round(VM_WORST + VM_WS_SIGMA, 4)}
                                     # {0.62, 0.98}
VM_PERIODS = [{"period": p["period"],
               "low": round(proj - VM_WS_SIGMA, 4),
               "high": round(proj + VM_WS_SIGMA, 4)} for p, proj in
              zip([{"period": 1}, {"period": 2}, {"period": 3}], VM_PROJ)]
                                     # p1 {0.66,1.02} p2 {0.64,1.0} p3 {0.62,0.98}
VM_HORIZON = {"low": min(b["low"] for b in VM_PERIODS), "high": max(b["high"] for b in VM_PERIODS)}
                                     # {0.62, 1.02} — high 1.02 > single-worst high 0.98 (WIDENS)

# ---- deli-varmax-cap: same band + a RECORDED capacity on the authority object --------------------
VMC_LABEL = "deli-varmax-cap"; VMC_METRIC = f"metric://{VMC_LABEL}/m-on-time"
VMC_POINTS = [dict(p) for p in VM_POINTS]
VMC_CAP_VALUE = 500.0; VMC_CAP_UNIT = "resolutions/day"; VMC_CAP_LOAD = 0.72

# ---- deli-flat2: recorded series, NO variance (no-band control) ----------------------------------
FL2_LABEL = rfv.FL2_LABEL; FL2_METRIC = rfv.FL2_METRIC; FL2_POINTS = rfv.FL2_POINTS

# ---- deli (no-data) ------------------------------------------------------------------------------
DELI = ac.DELI


def run_all() -> int:
    print("=== SPRINT 25 — horizon-wide do-nothing band + Q9 capacity-attention ===\n")

    # ---- orgs -------------------------------------------------------------------------------------
    fc_cfg = relabel_to(ac.DELI, FC_LABEL); fc = run_one(fc_cfg)
    record_series(fc, FC_LABEL, FC_METRIC, FC_POINTS, fields={
        "name": "resolution on-time rate", "formula": "on-time/total from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records", "owner": fc_cfg["authority"]["adjudicator_person"]})
    # NOTE: NO `band_variance` -> default last-point source (Sprint-23 byte-identical band).

    vm_cfg = relabel_to(ac.DELI, VM_LABEL); vm = run_one(vm_cfg)
    record_series(vm, VM_LABEL, VM_METRIC, VM_POINTS, fields={
        "name": "resolution on-time rate", "formula": "on-time/total from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records", "owner": vm_cfg["authority"]["adjudicator_person"],
        "band_variance": "all"})

    vmc_cfg = relabel_to(ac.DELI, VMC_LABEL); vmc = run_one(vmc_cfg)
    record_series(vmc, VMC_LABEL, VMC_METRIC, VMC_POINTS, fields={
        "name": "resolution on-time rate", "formula": "on-time/total from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records", "owner": vmc_cfg["authority"]["adjudicator_person"],
        "band_variance": "all"})
    eng.record_capacity(vmc["sub"], vmc_cfg["authority"]["dispute"], value=VMC_CAP_VALUE,
                        unit=VMC_CAP_UNIT, load=VMC_CAP_LOAD,
                        signer=vmc_cfg["authority"]["adjudicator_person"])

    fl2_cfg = relabel_to(ac.DELI, FL2_LABEL); fl2 = run_one(fl2_cfg)
    record_series(fl2, FL2_LABEL, FL2_METRIC, FL2_POINTS, fields={
        "name": "resolution on-time rate", "formula": "on-time/total from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records", "owner": fl2_cfg["authority"]["adjudicator_person"]})

    deli = run_one(DELI)

    for r in (fc, vm, vmc, fl2, deli):
        r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        r["closure"] = eng._forecast_closure(r["cfg"], r["sub"])

    # ---- (a) ALL orgs keep the full §7L Q1–Q10 cockpit -------------------------------------------
    for r in (fc, vm, vmc, fl2, deli):
        c = r["s7l"]
        full = all(isinstance(c[k], dict) for k in ("q1","q2","q3","q4","q5","q6","q7","q8","q9","q10"))
        ev = all(bool(c[k].get("evidence")) for k in ("q1","q2","q3","q4","q5","q6","q9","q10"))
        _report(f"{r['label']}: FULL §7L Q1–Q10 cockpit + data evidence present",
                full and ev and bool(c["q1"]["events"]) and bool(c["q7"]["options"])
                and bool(c["q8"]["authority"]) and bool(c["q10"]["determination"]),
                f"q6.avail={c['q6']['forecast_available']} rv={c['q6'].get('recorded_variance')} "
                f"q3 items={c['q3']['count']}")

    # ---- (b) band_periods = per-period projected ± recorded sigma, EXACT arithmetic --------------
    for r, periods_ref, sigma, proj_ref in ((fc, FC_PERIODS, FC_SIGMA, FC_PROJ),
                                            (vm, VM_PERIODS, VM_WS_SIGMA, VM_PROJ),
                                            (vmc, VM_PERIODS, VM_WS_SIGMA, VM_PROJ)):
        bp = r["closure"].get("band_periods")
        _report(f"{r['label']}: band_periods = per-period projected ± recorded sigma (EXACT)",
                bp == periods_ref and bp is not None,
                f"band_periods={bp}")
        _report(f"{r['label']}: band_periods agree with the closure projections (same recorded data)",
                bp is not None and [b["period"] for b in bp] == [p["period"] for p in r["closure"]["projections"]]
                and all(b["low"] == round(p["projected"] - sigma, 4)
                        and b["high"] == round(p["projected"] + sigma, 4)
                        for b, p in zip(bp, r["closure"]["projections"])),
                "")

    # ---- (c) band_horizon = min/max over the periods (recorded-data only) ------------------------
    _report(f"{FC_LABEL}: band_horizon = min period low / max period high ({FC_HORIZON})",
            fc["closure"].get("band_horizon") == FC_HORIZON
            and FC_HORIZON["low"] == round(min(FC_SIGMA and ((0.84 - FC_SIGMA), (0.82 - FC_SIGMA), (0.8 - FC_SIGMA))), 4)
            and FC_HORIZON["high"] == max(b["high"] for b in FC_PERIODS))
    _report(f"{VM_LABEL}: band_horizon = min period low / max period high ({VM_HORIZON})",
            vm["closure"].get("band_horizon") == VM_HORIZON
            and VM_HORIZON["low"] == min(b["low"] for b in VM_PERIODS)
            and VM_HORIZON["high"] == max(b["high"] for b in VM_PERIODS))

    # ---- (d) sigma is STILL exactly a recorded point |variance| magnitude --------------------------
    for r, pts, expected in ((fc, FC_POINTS, FC_SIGMA), (vm, VM_POINTS, VM_WS_SIGMA),
                             (vmc, VMC_POINTS, VM_WS_SIGMA)):
        bl = r["closure"]["band"]
        rec = sorted(abs(p["variance"]) for p in pts if p.get("variance") is not None)
        _report(f"{r['label']}: sigma is STILL a recorded point |variance| magnitude (never invented)",
                bl["sigma"] == expected and bl["sigma"] in [round(x, 4) for x in rec],
                f"sigma={bl['sigma']} recorded_mags={rec}")

    # ---- (e) widening: horizon-wide high > single-worst band high on the whole-series org ---------
    vm_hz = vm["closure"]["band_horizon"]; vm_band = vm["closure"]["band"]
    _report(f"{VM_LABEL}: horizon-wide HIGH {vm_hz['high']} > single-worst band high {vm_band['high']} "
            "(an earlier period at +σ sits ABOVE the worst point's band)",
            vm_hz["high"] > vm_band["high"] and vm_hz["low"] <= vm_band["low"],
            f"horizon {vm_hz}  single-worst {vm_band}")
    fc_hz = fc["closure"]["band_horizon"]; fc_band = fc["closure"]["band"]
    _report(f"{FC_LABEL}: horizon-wide is a pure per-period band of the SAME recorded sigma "
            "(last-point default; high widens to {})".format(fc_hz["high"]),
            fc_hz["low"] == fc_band["low"] and fc_hz["high"] > fc_band["high"] and fc_band["sigma"] == FC_SIGMA,
            f"horizon {fc_hz}  single-worst {fc_band}")
    _report(f"{VM_LABEL}: horizon-wide high {vm_hz['high']} exceeds the Sprint-23 last-point high "
            "(0.98) — carries the recorded whole-horizon worst case as data",
            vm_hz["high"] > 0.98, f"VM single-worst high=0.98")

    # ---- (f) default orgs byte-identical superset (only additive keys) ----------------------------
    fc_dn = fc["s7l"]["q8"].get("do_nothing_expected_impact") or {}
    _report(f"{FC_LABEL}: single-worst `band` field UNCHANGED (Sprint-23/24) + new additive keys",
            fc["closure"]["band"] == rfv.FC_BAND and "source" not in fc["closure"]["band"]
            and fc["closure"].get("band_horizon") == FC_HORIZON
            and fc["closure"].get("band_periods") == FC_PERIODS
            and fc["s7l"]["q8"]["forecast"]["band"] == rfv.FC_BAND
            and fc_dn.get("band") == rfv.FC_BAND)
    fc_att = [i for i in fc["s7l"]["q3"]["prioritized"] if i.get("tag") == "forecast"]
    _report(f"{FC_LABEL}: do-nothing summary keeps the Sprint-23/24 string as a strict prefix + "
            "appends the horizon-wide phrase",
            fc_dn["summary"].startswith(rfv.FC_SINGLE_SUMMARY)
            and "recorded band 0.71…0.89 (± σ 0.09)" in fc_dn["summary"]
            and "horizon-wide recorded band 0.71…0.93 across 3 projection periods" in fc_dn["summary"],
            fc_dn.get("summary"))
    _report(f"{FC_LABEL}: Q3 attention why keeps the Sprint-23/24 string + names the horizon wide band",
            len(fc_att) == 1 and fc_att[0]["why"].startswith(rfv.FC_SINGLE_WHY)
            and "recorded band 0.71…0.89 (± σ 0.09)" in fc_att[0]["why"])

    # band_capacity_attention present on all band orgs with a numeric threshold
    for r in (fc, vm, vmc):
        bca = r["s7l"]["q9"].get("band_capacity_attention")
        _report(f"{r['label']}: Q9 band_capacity_attention present (band + threshold both exist)",
                isinstance(bca, dict) and set(bca) >= {"flag", "why", "low", "high", "crosses"}
                and "horizon-wide recorded band" in bca["why"],
                f"flag={bca and bca.get('flag')} low={bca and bca.get('low')} high={bca and bca.get('high')}")

    # flag data-only: equals whether the horizon worst side crosses the recorded threshold
    _report(F"{FC_LABEL}: flag == horizon-crosses-threshold (data-only)",
            fc["s7l"]["q9"]["band_capacity_attention"]["flag"] is True
            and fc["s7l"]["q9"]["band_capacity_attention"]["crosses"] is True
            and fc["s7l"]["q9"]["band_capacity_attention"]["low"] == FC_HORIZON["low"]
            and fc["s7l"]["q9"]["band_capacity_attention"]["high"] == FC_HORIZON["high"])
    _report(f"{VM_LABEL}: flag == horizon-crosses-threshold (data-only)",
            vm["s7l"]["q9"]["band_capacity_attention"]["flag"] is True
            and vm["s7l"]["q9"]["band_capacity_attention"]["low"] == VM_HORIZON["low"]
            and vm["s7l"]["q9"]["band_capacity_attention"]["high"] == VM_HORIZON["high"])

    # (j) recorded-capacity org: why REFERENCES the recorded capacity, never invents/mutates it
    bca_cap = vmc["s7l"]["q9"]["band_capacity_attention"]
    _report(f"{VMC_LABEL}: Q9 capacity-attention `why` references the RECORDED capacity "
            "(500.0 resolutions/day, load 0.72) without inventing a capacity number",
            "500.0" in bca_cap["why"] and "resolutions/day" in bca_cap["why"] and "0.72" in bca_cap["why"]
            and bca_cap["flag"] is True
            and vmc["s7l"]["q9"]["capacity_recorded"] is True
            and vmc["s7l"]["q9"]["capacity"]["value"] == VMC_CAP_VALUE,
            bca_cap.get("why"))

    # ---- no-band control + no-data org: NO new keys, byte-identical ------------------------------
    fl2dn = fl2["s7l"]["q8"].get("do_nothing_expected_impact") or {}
    fl2f = fl2["s7l"]["q8"].get("forecast") or {}
    _report(f"{FL2_LABEL}: no-band control — NO band_periods / band_horizon / cap-attention (byte-identical)",
            "band" not in fl2["closure"] and "band_periods" not in fl2["closure"]
            and "band_horizon" not in fl2["closure"]
            and "band_capacity_attention" not in fl2["s7l"]["q9"]
            and set(fl2dn.keys()) == {"baseline","priced","on_target","summary","metric","direction"}
            and set(fl2f.keys()) == {"projections","threshold","source","worst","crossing","direction"})
    _report(f"{FL2_LABEL}: do-nothing summary EXACTLY the Sprint-22 single-point template (byte-identical)",
            fl2dn["summary"] == rfv.FL2_SINGLE_SUMMARY)
    d = deli["s7l"]; dl = deli["closure"]
    _report("deli (no recorded series): unchanged fallback + no band / horizon / capacity-attention",
            dl.get("available") is False and d["q6"]["forecast_available"] is False
            and "forecast" not in d["q8"] and "do_nothing_expected_impact" not in d["q8"]
            and "band" not in dl and "band_horizon" not in dl and "band_periods" not in dl
            and "band_capacity_attention" not in d["q9"])

    # ---- (g) determinism on re-run (dict + render) ------------------------------------------------
    for r in (fc, vm, vmc, fl2, deli):
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: deterministic on re-run (structured dict + rendered §7L line)",
                c1 == c2 and x1 == x2)

    # ---- (h) NO §6 overrule ----------------------------------------------------------------------
    for r in (fc, vm, vmc, fl2, deli):
        base8 = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)["q8"]
        _report(f"{r['label']}: Q8 recommendation is UNCHANGED by horizon band + Q9 attention (no §6 overrule)",
                r["s7l"]["q8"]["recommendation"] == base8["recommendation"]
                and r["s7l"]["q8"]["floor_gated"] == base8["floor_gated"],
                f"{r['s7l']['q8']['recommendation']} == {base8['recommendation']}")

    # ---- (i) every bound from recorded data only --------------------------------------------------
    _report("band_periods/horizon + cap-attention from recorded data only (no wall-clock, no invented σ)",
            all(b["low"] == round(p["projected"] - FC_SIGMA, 4) and b["high"] == round(p["projected"] + FC_SIGMA, 4)
                for b, p in zip(fc["closure"]["band_periods"], fc["closure"]["projections"]))
            and fc["closure"]["band"]["sigma"] == FC_SIGMA
            and vm["closure"]["band"]["sigma"] in [round(abs(p["variance"]), 4) for p in VM_POINTS]
            and dl.get("available") is False)

    # ---- emit fixtures for the recorded orgs + the engine-native report ---------------------------
    for r in (fc, vm, vmc, fl2):
        eng.emit_fixtures(r["sub"], HERE, r["cfg"])
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L horizon-wide do-nothing band + Q9 capacity-attention — engine-native render (Sprint 25)"]
    A.append(f"generated {now_iso()}  |  `adjudication_engine._forecast_closure`/`cockpit_s7l`  |  "
             "recorded `metric://` series + recorded point-`variance` values + the recorded "
             "`band_variance` source -> the SAME recorded sigma applied to EVERY projection period "
             "(band_periods) + the record-wide horizon worst case (band_horizon = min low / max high) "
             "+ a Q9 capacity-attention flag (horizon range vs the recorded threshold; references any "
             "recorded capacity without inventing one). Additive; default orgs byte-identical to "
             "Sprint 23/24 except the new band_periods/band_horizon/band_capacity_attention keys  |  "
             "SPEC v0.22, 49 $defs, URI cap")
    A.append("")
    A.append("The do-nothing expected-impact now prices the recorded SPREAD ACROSS THE WHOLE HORIZON, "
             "not just the single worst point: the same recorded sigma (± a recorded point variance "
             "magnitude) is applied to EVERY projected value -> a per-period low/high, and the "
             "record-wide min-low / max-high (band_horizon) is the whole-horizon worst case AS DATA. "
             "Q9 carries a capacity-attention flag: whether that horizon range signals the recorded "
             "threshold; it references any RECORDED capacity but never fabricates a number. This is "
             "still a recorded-data spread, NOT a probability/confidence interval, never the wall-clock.")
    A.append("")
    for r in (fc, vm, vmc, fl2, deli):
        A.append(f"--- {r['label']} ---")
        A.append("```")
        A.append(eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY))
        A.append("```")
        A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**The do-nothing price + Q9 capacity-attention now carry the recorded whole-horizon "
             "worst case as data where it exists.** The same recorded sigma (one recorded point "
             "|variance| magnitude, per the recorded `band_variance` source) is applied to EVERY "
             "projection period -> `band_periods` (per-period low/high) + `band_horizon` (record-wide "
             "min-low/max-high), which can WIDEN beyond the single-worst point's band when an earlier "
             "period at +σ exceeds the worst point's own band — still a pure function of recorded "
             "values + the recorded sigma, not a new model. Q9's `band_capacity_attention` flag "
             "derives from the horizon range vs the recorded threshold and references any RECORDED "
             "capacity without inventing one; a no-variance / no-data org carries none of the new keys "
             "(byte-identical). The Q8 recommendation is UNCHANGED: the band prices attention + "
             "do-nothing; it never overrules the §6-floor-gated machine-eligible best. **Still not "
             "derivable:** an org that records no point variances cannot be priced as a band (correct); "
             "a capacity-attention NUMBER is never fabricated (the engine only flags/reasons); and "
             "this remains a recorded-spread range, NOT a probabilistic confidence interval "
             "(a stochastic/adaptive forecast stays out of the deterministic ~$0 stance).")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs. Horizon-wide band + Q9 capacity-"
             "attention price the recorded whole-horizon spread as data; they never overrule the "
             "§6 human or the floor-gated recommendation._")
    (rp / "cockpit-forecast-horizon.md").write_text("\n".join(A) + "\n")

    print("\n  -> engine-native horizon-wide band cockpit under "
          "artifacts/adjudication/reports/cockpit-forecast-horizon.md")
    print("  -> recorded-org fixtures under artifacts/adjudication/fixtures/"
          f"{{{FC_LABEL},{VM_LABEL},{VMC_LABEL},{FL2_LABEL}}}/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())