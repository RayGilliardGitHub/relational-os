"""run_forecast_horizon2_demo.py — SPRINT 26: Q3-attention horizon-wide suffix + Q9 capacity-planning.

Sprint 25 disclosed its own next honest frontier (sprints/sprint-25/notes/findings.md, "Open
issues / next work"): **`band_horizon`/`band_periods` are surfaced on Q6/Q8/do-nothing, but the Q3
forecast-driven attention item's `why` still names only the single worst point + single-worst band,
and the Q9 `band_capacity_attention` is a FLAG that does not drive any recorded capacity-planning
guidance.** Sprint 26 closes that bounded slice additively:

  1. **Q3 attention names the horizon-wide range.** When a recorded-variance band exists AND the
     forecast-driven attention item was created, `_forecast_closure` APPENDS an additive suffix to
     `attention_item["why"]` that names `band_horizon` (` — horizon-wide recorded band {lo}…{hi}
     across {n} projection periods (band_periods/band_horizon, same recorded σ)`) — appended AFTER
     the Sprint-23/24/25 single-worst band phrase (+ any Sprint-24 band_source phrase) so the old
     `why` stays a STRICT PREFIX. The do-nothing summary reuses the SAME shared constant, so
     Q3/Q6/Q8/do-nothing name the same record-wide worst case VERBATIM by construction. No-band /
     no-data orgs: no suffix (unchanged).
  2. **Q9 data-only capacity-planning attention.** In `cockpit_s7l`'s Q9 block, ONLY where the org
     RECORDS a numeric `capacity` on its authority object AND a band + numeric threshold exist, add
     an additive `capacity_planning_attention` = {flag, why}: ONE deterministic rule from recorded
     numbers only (at-capacity when recorded `load >= 1.0`; deficit when the horizon band's worst-
     side magnitude reaches/exceeds the recorded capacity VALUE; otherwise headroom). `why` states
     the recorded capacity value/unit/load + the horizon-wide band and labels headroom/at-capacity/
     deficit as a derived REASON — NEVER a fabricated capacity number, NEVER a directive. Orgs that
     record no capacity carry NO key (byte-identical superset of Sprint 25).

Still recorded-data only: every bound is a projected value ± the recorded σ (a recorded point
|variance| magnitude); the capacity-planning label derives from recorded capacity + recorded load +
the recorded band + the recorded threshold. No new noun, frozen 49 $defs, SPEC v0.22, `ros/`
untouched, the ONLY engine file touched is adjudication_engine.py.

This runner (exit 0 = ALL PASS) drives the SAME ≥5 fresh orgs as Sprint 25 (reusing its builders +
constants so the source recorded data is byte-identical) and asserts (a)–(h) per work/3-runner-plan.
Emits fixtures + artifacts/adjudication/reports/cockpit-forecast-horizon2.md.
Usage: (from instances/contested_reality)  python3 run_forecast_horizon2_demo.py
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
import run_forecast_horizon_demo as rfh               # noqa: E402  (Sprint 25 builders/constants)
import run_forecast_variance_demo as rfv              # noqa: E402  (Sprint-23 byte-identity constants)

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")


# ----- the shared horizon-wide suffix (byte-identical to the engine's _HORIZON_BAND_PHRASE) ------
R26_HORIZON = (" — horizon-wide recorded band {lo}…{hi} across {n} projection periods "
               "(band_periods/band_horizon, same recorded σ)")


def build_orgs():
    """Rebuild the exact Sprint-25 orgs (same recorded series / variance / capacity)."""
    fc_cfg = rfh.relabel_to(ac.DELI, rfh.FC_LABEL); fc = rfh.run_one(fc_cfg)
    rfh.record_series(fc, rfh.FC_LABEL, rfh.FC_METRIC, rfh.FC_POINTS, fields={
        "name": "resolution on-time rate", "formula": "on-time/total from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records", "owner": fc_cfg["authority"]["adjudicator_person"]})
    vm_cfg = rfh.relabel_to(ac.DELI, rfh.VM_LABEL); vm = rfh.run_one(vm_cfg)
    rfh.record_series(vm, rfh.VM_LABEL, rfh.VM_METRIC, rfh.VM_POINTS, fields={
        "name": "resolution on-time rate", "formula": "on-time/total from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records", "owner": vm_cfg["authority"]["adjudicator_person"],
        "band_variance": "all"})
    vmc_cfg = rfh.relabel_to(ac.DELI, rfh.VMC_LABEL); vmc = rfh.run_one(vmc_cfg)
    rfh.record_series(vmc, rfh.VMC_LABEL, rfh.VMC_METRIC, rfh.VMC_POINTS, fields={
        "name": "resolution on-time rate", "formula": "on-time/total from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records", "owner": vmc_cfg["authority"]["adjudicator_person"],
        "band_variance": "all"})
    eng.record_capacity(vmc["sub"], vmc_cfg["authority"]["dispute"], value=rfh.VMC_CAP_VALUE,
                        unit=rfh.VMC_CAP_UNIT, load=rfh.VMC_CAP_LOAD,
                        signer=vmc_cfg["authority"]["adjudicator_person"])
    fl2_cfg = rfh.relabel_to(ac.DELI, rfh.FL2_LABEL); fl2 = rfh.run_one(fl2_cfg)
    rfh.record_series(fl2, rfh.FL2_LABEL, rfh.FL2_METRIC, rfh.FL2_POINTS, fields={
        "name": "resolution on-time rate", "formula": "on-time/total from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records", "owner": fl2_cfg["authority"]["adjudicator_person"]})
    deli = rfh.run_one(ac.DELI)
    for r in (fc, vm, vmc, fl2, deli):
        r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        r["closure"] = eng._forecast_closure(r["cfg"], r["sub"])
    return {"fc": fc, "vm": vm, "vmc": vmc, "fl2": fl2, "deli": deli}


def run_all() -> int:
    print("=== SPRINT 26 — Q3-attention horizon-wide suffix + Q9 capacity-planning ===\n")
    o = build_orgs()
    fc, vm, vmc, fl2, deli = o["fc"], o["vm"], o["vmc"], o["fl2"], o["deli"]

    # ---- (a) ALL orgs keep the full §7L Q1–Q10 cockpit ------------------------------------------
    for r in (fc, vm, vmc, fl2, deli):
        c = r["s7l"]
        full = all(isinstance(c[k], dict) for k in ("q1","q2","q3","q4","q5","q6","q7","q8","q9","q10"))
        ev = all(bool(c[k].get("evidence")) for k in ("q1","q2","q3","q4","q5","q6","q9","q10"))
        _report(f"{r['label']}: FULL §7L Q1–Q10 cockpit + data evidence present",
                full and ev and bool(c["q1"]["events"]) and bool(c["q7"]["options"])
                and bool(c["q8"]["authority"]) and bool(c["q10"]["determination"]),
                f"q6.avail={c['q6']['forecast_available']} q3 items={c['q3']['count']}")

    def _fc_att(r):
        return [i for i in r["s7l"]["q3"]["prioritized"] if i.get("tag") == "forecast"]

    # ---- (b) Q3 attention `why` keeps Sprint-23/24/25 as strict prefix + horizon-wide suffix ----
    fc_att = _fc_att(fc); vm_att = _fc_att(vm); vmc_att = _fc_att(vmc)
    # exact pre-Sprint-26 Q3 why for deli-forecast (Sprint-23 single-worst phrase; no band_source):
    fc_pre26 = rfv.FC_SINGLE_WHY + (" — recorded band 0.71…0.89 (± σ 0.09); worst side "
                                    "0.71 below target 0.95")
    fc_hz = "0.71…0.93 across 3 projection periods"
    _report(f"{fc['label']}: Q3 why == the Sprint-23/24/25 `why` + the horizon-wide suffix EXACTLY "
            "(strict-prefix byte-identity)",
            len(fc_att) == 1
            and fc_att[0]["why"] == fc_pre26 + R26_HORIZON.format(lo=0.71, hi=0.93, n=3)
            and ("horizon-wide recorded band " + fc_hz) in fc_att[0]["why"],
            fc_att[0]["why"])
    _report(f"{fc['label']}: Q3 why still STARTs with the Sprint-23 string (prefix preserved)",
            len(fc_att) == 1 and fc_att[0]["why"].startswith(rfv.FC_SINGLE_WHY))
    for r, att, lo, hi in ((vm, vm_att, 0.62, 1.02), (vmc, vmc_att, 0.62, 1.02)):
        _report(f"{r['label']}: Q3 why keeps the Sprint-23/24/25 band phrase as a prefix AND appends "
                "the horizon-wide suffix (source phrase kept)",
                len(att) == 1 and att[0]["why"].startswith(rfv.FC_SINGLE_WHY)
                and ("recorded band 0.62…0.98 (± σ 0.18)" in att[0]["why"])
                and "(band_variance all)" in att[0]["why"]
                and att[0]["why"].endswith(R26_HORIZON.format(lo=lo, hi=hi, n=3))
                and ("horizon-wide recorded band 0.62…1.02 across 3 projection periods"
                     in att[0]["why"]),
                att[0]["why"])

    # ---- (c) do-nothing summary keeps Sprint-23/24 string + carries the horizon phrase ----------
    fc_dn = fc["s7l"]["q8"].get("do_nothing_expected_impact") or {}
    _report(f"{fc['label']}: do-nothing summary keeps the Sprint-23/24 string as a strict prefix + "
            "the horizon-wide phrase (shared constant)",
            fc_dn["summary"].startswith(rfv.FC_SINGLE_SUMMARY)
            and ("horizon-wide recorded band " + fc_hz) in fc_dn["summary"]
            and fc_dn["summary"].endswith("same recorded σ)"),
            fc_dn.get("summary"))

    # ---- (d) Q9 capacity-planning attention: ONLY the capacity-recording org --------------------
    for r in (fc, vm, fl2, deli):
        _report(f"{r['label']}: Q9 has NO `capacity_planning_attention` key (no recorded capacity "
                "or no band — byte-identical superset)",
                "capacity_planning_attention" not in r["s7l"]["q9"]
                and r["s7l"]["q9"].get("capacity_recorded") is False)
    cpa = vmc["s7l"]["q9"].get("capacity_planning_attention")
    _report(f"{vmc['label']}: Q9 gains `capacity_planning_attention` {{flag,why}} (recorded numeric "
            "capacity + band + threshold all exist)",
            isinstance(cpa, dict) and set(cpa) == {"flag", "why"} and cpa["flag"] is False
            and vmc["s7l"]["q9"]["capacity_recorded"] is True
            and vmc["s7l"]["q9"]["capacity"]["value"] == rfh.VMC_CAP_VALUE,
            str(cpa))
    _report(f"{vmc['label']}: capacity-planning `why` names the RECORDED capacity + horizon band and "
            "labels headroom/deficit as a derived REASON (never invents a number, never a directive)",
            cpa is not None
            and "500.0 resolutions/day (load 0.72)" in cpa["why"]
            and "horizon-wide recorded band 0.62…1.02 across 3 projection periods" in cpa["why"]
            and "derived headroom" in cpa["why"]
            and "not a directive, no invented capacity" in cpa["why"],
            cpa and cpa["why"])
    # the flag is data-only: capacity 500 >> horizon worst-side 0.62 AND load 0.72 < 1.0 -> headroom
    _report(f"{vmc['label']}: capacity-planning flag is a deterministic function of recorded "
            "capacity + load + band (headroom)", cpa is not None
            and cpa["flag"] is False and 500.0 >= 0.62 and 0.72 < 1.0)

    # ---- (e) band_periods / band_horizon / band_capacity_attention UNCHANGED on band orgs --------
    _report(f"{fc['label']}: band_periods/band_horizon intact (0.71…0.93) + Q9 band_capacity_attention "
            "present (Sprint-25 superset untouched)",
            fc["closure"].get("band_periods") == rfh.FC_PERIODS
            and fc["closure"].get("band_horizon") == rfh.FC_HORIZON
            and isinstance(fc["s7l"]["q9"].get("band_capacity_attention"), dict))
    _report(f"{vmc['label']}: band_periods/band_horizon intact (0.62…1.02) + band_capacity_attention "
            "still carries the recorded-capacity reference",
            vmc["closure"].get("band_horizon") == rfh.VM_HORIZON
            and "500.0" in vmc["s7l"]["q9"]["band_capacity_attention"]["why"])
    fl2dn = fl2["s7l"]["q8"].get("do_nothing_expected_impact") or {}
    _report(f"{fl2['label']}: no-band control — NO new keys, do-nothing summary EXACTLY the "
            "Sprint-22 single-point template (byte-identical)",
            "band" not in fl2["closure"] and "band_horizon" not in fl2["closure"]
            and "band_periods" not in fl2["closure"]
            and "band_capacity_attention" not in fl2["s7l"]["q9"]
            and set(fl2dn.keys()) == {"baseline","priced","on_target","summary","metric","direction"}
            and fl2dn["summary"] == rfv.FL2_SINGLE_SUMMARY)
    d = deli["s7l"]; dl = deli["closure"]
    _report("deli (no recorded series): unchanged fallback + no band / horizon / capacity-planning",
            dl.get("available") is False and d["q6"]["forecast_available"] is False
            and "band" not in dl and "band_horizon" not in dl
            and "band_capacity_attention" not in d["q9"]
            and "capacity_planning_attention" not in d["q9"])

    # ---- (f) determinism on re-run (dict + render) ----------------------------------------------
    for r in (fc, vm, vmc, fl2, deli):
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: deterministic on re-run (structured dict + rendered §7L line)",
                c1 == c2 and x1 == x2)

    # ---- (g) NO §6 overrule ----------------------------------------------------------------------
    for r in (fc, vm, vmc, fl2, deli):
        base8 = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)["q8"]
        _report(f"{r['label']}: Q8 recommendation is UNCHANGED by the Q3 suffix + Q9 capacity-"
                "planning (no §6 overrule)",
                r["s7l"]["q8"]["recommendation"] == base8["recommendation"]
                and r["s7l"]["q8"]["floor_gated"] == base8["floor_gated"],
                f"{r['s7l']['q8']['recommendation']} == {base8['recommendation']}")

    # ---- (h) every value from recorded data only (no wall-clock, no invented number) -------------
    _report("Q3 suffix + capacity-planning derived from recorded data only (SAME σ as the band; "
            "flag from recorded capacity+load+band)",
            fc["closure"]["band"]["sigma"] == rfv.FC_SIGMA
            and all(b["low"] == round(p["projected"] - rfv.FC_SIGMA, 4)
                    and b["high"] == round(p["projected"] + rfv.FC_SIGMA, 4)
                    for b, p in zip(fc["closure"]["band_periods"], fc["closure"]["projections"]))
            and vm["closure"]["band"]["sigma"] in [round(abs(p["variance"]), 4) for p in rfh.VM_POINTS]
            and dl.get("available") is False)

    # ---- emit fixtures for the recorded orgs + the engine-native report --------------------------
    for r in (fc, vm, vmc, fl2):
        eng.emit_fixtures(r["sub"], HERE, r["cfg"])
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L Q3-attention horizon-wide suffix + Q9 capacity-planning — engine-native render "
         "(Sprint 26)"]
    A.append(f"generated {now_iso()}  |  `adjudication_engine._forecast_closure`/`cockpit_s7l`  |  "
             "recorded `metric://` series + recorded point-`variance` + the recorded `band_variance` "
             "source + a recorded authority `capacity` -> (1) the q3 forecast-driven attention "
             "`why` now names the SAME record-wide horizon band (band_horizon) that Q6/Q8/do-nothing "
             "carry — appended as a STRICT PREFIX suffix; (2) a Q9 `capacity_planning_attention` "
             "flag/reason derived from recorded capacity + load + the horizon band (headroom / "
             "at-capacity / deficit), ONLY where a capacity is recorded. Additive; default orgs "
             "byte-identical to Sprint 25 except the additive Q3 suffix + the capacity-only key.  | "
             "SPEC v0.22, 49 $defs, URI cap")
    A.append("")
    A.append("The human's FIRST attention line (Q3) now names the recorded whole-horizon worst case "
             "(band_horizon) verbatim with Q6/Q8/do-nothing — the same recorded σ applied to every "
             "projection period, never a new model. And where the org records a numeric `capacity`, "
             "Q9 adds a data-only capacity-planning reason (headroom/at-capacity/deficit from "
             "recorded numbers only) — never a fabricated figure, never a directive.")
    A.append("")
    for r in (fc, vm, vmc, fl2, deli):
        A.append(f"--- {r['label']} ---")
        A.append("```")
        A.append(eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY))
        A.append("```")
        A.append("")
        cpa = r["s7l"]["q9"].get("capacity_planning_attention")
        if cpa:
            A.append(f"Q9 capacity_planning_attention: flag={cpa['flag']}  why={cpa['why']}")
            A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**Q3 and Q9 capacity attention now carry the recorded whole-horizon worst case AS "
             "DATA where it exists.** Q3's forecast-driven attention `why` appends the exact "
             "`band_horizon` range (same shared constant as the do-nothing summary -> verbatim by "
             "construction) behind the Sprint-23/24/25 single-worst phrase, which stays a strict "
             "prefix. Where the org records a numeric `capacity`, Q9's `capacity_planning_attention` "
             "states the recorded capacity value/unit/load vs the horizon-wide band and labels "
             "headroom / at-capacity / deficit as a derived REASON from recorded numbers only — "
             "never an invented capacity value, never a directive. A no-capacity org / no-band / "
             "no-data org carries no new key (byte-identical superset). The Q8 recommendation is "
             "UNCHANGED: attention + capacity reasoning never overrule the §6-floor-gated machine-"
             "eligible best. **Still not derivable:** an org with no recorded point variances cannot "
             "be priced as a band (correct); an org that records no capacity gets no capacity-"
             "planning line (correct); and this remains a recorded-spread range, NOT a probabilistic "
             "confidence interval (a stochastic/adaptive forecast stays out of the deterministic ~$0 "
             "stance).")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs. Q3 + Q9 capacity attention price "
             "the recorded whole-horizon spread as data; they never overrule the §6 human or the "
             "floor-gated recommendation._")
    (rp / "cockpit-forecast-horizon2.md").write_text("\n".join(A) + "\n")

    print("\n  -> engine-native Sprint-26 cockpit under "
          "artifacts/adjudication/reports/cockpit-forecast-horizon2.md")
    print("  -> recorded-org fixtures under artifacts/adjudication/fixtures/"
          f"{{{fc['label']},{vm['label']},{vmc['label']},{fl2['label']}}}/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())