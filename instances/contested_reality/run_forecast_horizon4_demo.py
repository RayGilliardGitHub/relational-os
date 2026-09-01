# === DEMO / TEST RUNNER - NOT part of the engine API ===
"""run_forecast_horizon4_demo.py — SPRINT 28: capacity_constraint proven at its LIMIT.

Sprint 27's own finding (archive/sprints/sprint-27/notes/findings.md, "Open issues / next work")
disclosed the honest frontier: the Q7/Q8 `capacity_constraint` marker is proven end-to-end ONLY in
**headroom** (`deli-varmax-cap` -> `reason:"headroom", options_flagged:{}`); its at-capacity /
deficit branches exist in the shared `_capacity_reason` helper but are NEVER exercised on a real
org, so (a) the `capacity_risk` flagging, (b) the derived reason, and (c) the honest "the SAME
machine-eligible options and the SAME Q8 recommendation remain, correctly, with only a
capacity_risk label" are unproven AS DATA on a living Q1–Q10 cockpit.

Sprint 28 closes that bounded slice with recorded data + a runner ONLY (no engine change — the
engine's `_capacity_reason` and the Q7/Q8 `capacity_constraint` block already implement all three
branches; Sprint-27 simply never drove the non-headroom orgs). It drives SEVEN fresh orgs:

  deli-forecast    no capacity, no band_variance          -> NO capacity_constraint (Sprint-27 byte-identical)
  deli-varmax      band, no capacity                      -> NO capacity_constraint
  deli-varmax-cap  band + capacity 500.0, load 0.72       -> capacity_constraint reason HEADROOM (Sprint-27 default)
  deli-flat2       recorded series, no variance/band      -> NO capacity_constraint (no-band control)
  deli             no recorded series data                -> NO capacity_constraint (no-data org)
  deli-atcap   NEW recorded capacity 500.0 res/day, load 1.25 (> =1.0), same whole-series band as
                     deli-varmax        -> reason AT-CAPACITY, flag True
  deli-deficit NEW lower-is-better latency metric, band_horizon {12.0,32.0}, recorded capacity
                     value 30.0 (load 0.9) -> horizon high 32.0 >= capacity 30.0 -> reason DEFICIT, flag True

and asserts (per plan.md work/1-plan items a–g): full §7L Q1–Q10 on all 7; Sprint-27 byte-identity
on the 5 reused orgs; the non-headroom block FULLY exercised on the two new orgs (reason + flag
True + EVERY capacity-consuming non-baseline option marked `capacity_risk`, baseline never flagged,
reason agrees with each org's Q9 `capacity_planning_attention` BY CONSTRUCTION); the marker is a
LABEL at its limit (Q7 options / machine_eligible_best / Q8 recommendation / floor_gated EXACTLY
equal to `cockpit_q7q8` for EVERY org, incl. at-capacity/deficit — no §6 overrule, no re-rank, no
option-removal); superset byte-identity; determinism; real output.

Additive: ONLY a new runner + recorded data. No engine change, no new noun, frozen 49 $defs, SPEC
v0.22, ros/ untouched. Emits fixtures (incl. the two new orgs) + cockpit-forecast-horizon4.md.
Usage: (from instances/contested_reality)  python3 run_forecast_horizon4_demo.py
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCES = HERE.parent
ROS = INSTANCES.parents[0]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(INSTANCES))
sys.path.insert(0, str(ROS))

from ros.substrate import now_iso          # noqa: E402
import adjudication_engine as eng          # noqa: E402
import adjudication_configs as ac          # noqa: E402
import run_forecast_horizon2_demo as r26   # noqa: E402  (Sprint-26/27 org builders/constants)
import run_forecast_horizon_demo as rfh    # noqa: E402  (Sprint-25 builders/constants)
import run_forecast_variance_demo as rfv   # noqa: E402  (Sprint-23 builders/constants, e.g. CO points)

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")


# ---- the TWO new orgs' exact recorded numbers / targets (reproducible) ---------------------------
ATCAP_LABEL = "deli-atcap"
ATCAP_CAP_VALUE = 500.0
ATCAP_CAP_UNIT = "resolutions/day"
ATCAP_CAP_LOAD = 1.25
ATCAP_METRIC = f"metric://{ATCAP_LABEL}/m-on-time"
# same whole-series band as deli-varmax: band_variance "all", sigma 0.18, horizon {0.62, 1.02}

DEFICIT_LABEL = "deli-deficit"
DEFICIT_CAP_VALUE = 30.0
DEFICIT_CAP_UNIT = "resolutions/day"
DEFICIT_CAP_LOAD = 0.9
DEFICIT_METRIC = f"metric://{DEFICIT_LABEL}/m-latency"
# lower-is-better latency series (Sprint-23 CO points): sigma 8, projections [20,22,24],
# horizon {12.0, 32.0}; high 32.0 >= capacity value 30.0 -> deficit
DEFICIT_SIGMA = 8.0
DEFICIT_HORIZON_HIGH = 32.0


def _new_series_org(label, metric_uri, points, fields, cap_value, cap_unit, cap_load):
    """Build a fresh DELI-relabeled org that also RECORDS a metric series + an authority capacity."""
    cfg = rfh.relabel_to(ac.DELI, label)
    r = rfh.run_one(cfg)
    eng.record_metric_series(r["sub"], label, metric_uri, points=points, fields=fields,
                             signer=cfg["authority"]["adjudicator_person"])
    eng.record_capacity(r["sub"], cfg["authority"]["dispute"], value=cap_value,
                        unit=cap_unit, load=cap_load, signer=cfg["authority"]["adjudicator_person"])
    r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
    r["closure"] = eng._forecast_closure(r["cfg"], r["sub"])
    return r


def build_orgs():
    """The five reused Sprint-26/27 orgs + the two NEW non-headroom orgs."""
    o = r26.build_orgs()
    # ---- NEW org 1: at-capacity (recorded load 1.25 >= 1.0), same band as deli-varmax ----------
    atcap = _new_series_org(
        ATCAP_LABEL, ATCAP_METRIC, [dict(p) for p in rfh.VM_POINTS],
        {"name": "resolution on-time rate", "formula": "on-time/total from ledger",
         "unit": "fraction", "target": 0.95, "period": "quarter",
         "source": "ledger resolution completion records", "owner": ac.DELI["authority"]["adjudicator_person"],
         "band_variance": "all"},
        ATCAP_CAP_VALUE, ATCAP_CAP_UNIT, ATCAP_CAP_LOAD)
    # ---- NEW org 2: deficit (lower-is-better latency, horizon high reaches recorded capacity) ---
    deficit = _new_series_org(
        DEFICIT_LABEL, DEFICIT_METRIC, [dict(p) for p in rfv.CO_POINTS],
        {"name": "mean resolution latency", "formula": "mean elapsed time to a resolution from ledger",
         "unit": "ms", "target": 16, "period": "quarter", "source": "ledger resolution completion records",
         "direction": "lower-is-better", "band_variance": "all",
         "owner": ac.DELI["authority"]["adjudicator_person"]},
        DEFICIT_CAP_VALUE, DEFICIT_CAP_UNIT, DEFICIT_CAP_LOAD)
    return {**o, "atcap": atcap, "deficit": deficit}


def run_all() -> int:
    print("=== SPRINT 28 — capacity_constraint proven at its LIMIT (at-capacity / deficit) ===\n")
    o = build_orgs()
    fc, vm, vmc, fl2, deli = o["fc"], o["vm"], o["vmc"], o["fl2"], o["deli"]
    atcap, deficit = o["atcap"], o["deficit"]
    all7 = (fc, vm, vmc, fl2, deli, atcap, deficit)

    # deli options (the NON-baseline capacity-consuming set the marker flags at non-headroom)
    deli_opts = list(ac.DELI["options"])
    baseline = next(x for x in deli_opts if "unres" in x.lower() or x == "do-nothing")
    non_baseline = [x for x in deli_opts if x != baseline]
    _report("baseline is the do-nothing/UNRESOLVED option (never flagged), 8 options total",
            baseline == "unresolved" and len(deli_opts) == 8 and len(non_baseline) == 7,
            f"baseline={baseline} n_opts={len(deli_opts)}")

    # ---- (a) ALL orgs keep the full §7L Q1–Q10 cockpit -----------------------------------------
    for r in all7:
        c = r["s7l"]
        full = all(isinstance(c[k], dict) for k in ("q1","q2","q3","q4","q5","q6","q7","q8","q9","q10"))
        ev = all(bool(c[k].get("evidence")) for k in ("q1","q2","q3","q4","q5","q6","q9","q10"))
        _report(f"{r['label']}: FULL §7L Q1–Q10 cockpit + data evidence present",
                full and ev and bool(c["q1"]["events"]) and bool(c["q7"]["options"])
                and bool(c["q8"]["authority"]) and bool(c["q10"]["determination"]),
                f"q6.avail={c['q6']['forecast_available']} q3 items={c['q3']['count']}")

    # ---- (b) Sprint-27 byte-identity on the five reused orgs -----------------------------------
    cpa = vmc["s7l"]["q9"].get("capacity_planning_attention")
    vcc7 = vmc["s7l"]["q7"].get("capacity_constraint")
    vcc8 = vmc["s7l"]["q8"].get("capacity_constraint")
    _report(f"{vmc['label']}: REUSED headroom org — `capacity_constraint` reason STILL headroom, "
            "flag False, options_flagged STILL {} (Sprint-27 default byte-identical)",
            isinstance(vcc7, dict) and vcc7 == vcc8 and vcc7["reason"] == "headroom"
            and vcc7["flag"] is False and vcc7["options_flagged"] == {},
            str(vcc8))
    _report(f"{vmc['label']}: Q9 capacity_planning_attention UNCHANGED (derived headroom, flag False)",
            isinstance(cpa, dict) and cpa["flag"] is False and "derived headroom" in cpa["why"],
            str(cpa))
    fc_att = [i for i in fc["s7l"]["q3"]["prioritized"] if i.get("tag") == "forecast"]
    _report(f"{fc['label']}: Q3 `why` STILL the Sprint-26/27 horizon-suffix string (byte-identity)",
            len(fc_att) == 1
            and fc_att[0]["why"] == (r26.rfv.FC_SINGLE_WHY
                                     + (" — recorded band 0.71…0.89 (± σ 0.09); worst side "
                                        "0.71 below target 0.95")
                                     + r26.R26_HORIZON.format(lo=0.71, hi=0.93, n=3)),
            fc_att[0]["why"])
    for r in (fc, vm, fl2, deli):
        _report(f"{r['label']}: NO `capacity_constraint` on Q7 or Q8 (no recorded capacity / no band "
                "— Sprint-27 byte-identical)",
                "capacity_constraint" not in r["s7l"]["q7"] and "capacity_constraint" not in r["s7l"]["q8"]
                and "capacity_planning_attention" not in r["s7l"]["q9"])

    # ---- (c) the NON-HEADROOM block is now FULLY exercised on the two new orgs ------------------
    for r, expect_reason in ((atcap, "at-capacity"), (deficit, "deficit")):
        cc7 = r["s7l"]["q7"].get("capacity_constraint")
        cc8 = r["s7l"]["q8"].get("capacity_constraint")
        cpa_r = r["s7l"]["q9"].get("capacity_planning_attention")
        flagged = dict(cc8["options_flagged"]) if isinstance(cc8, dict) else None
        _report(f"{r['label']}: non-headroom block present on BOTH Q7 and Q8, reason = {expect_reason}, "
                "flag True (recorded load / horizon worst-side makes it NON-headroom)",
                isinstance(cc7, dict) and isinstance(cc8, dict) and cc7 == cc8
                and cc8["reason"] == expect_reason and cc8["flag"] is True,
                str(cc8))
        _report(f"{r['label']}: options_flagged marks EVERY capacity-consuming NON-baseline option "
                f"`capacity_risk` ({len(non_baseline)} flagged), baseline `{baseline}` NEVER flagged",
                flagged is not None
                and set(flagged) == set(non_baseline) and all(v == "capacity_risk" for v in flagged.values())
                and baseline not in flagged,
                f"flagged={sorted(flagged or {})}")
        _report(f"{r['label']}: constraint reason AGREES with the Q9 capacity label BY CONSTRUCTION "
                "(shared `_capacity_reason`) — flag True on both",
                isinstance(cpa_r, dict) and cpa_r["flag"] is True and cc8["reason"] == expect_reason,
                str(cpa_r))
        _report(f"{r['label']}: block is a LABEL — never a removal, never a directive (note names the "
                "UNCHANGED Q8 recommendation + §6 human)",
                isinstance(cc8, dict) and "UNCHANGED" in cc8.get("note", "")
                and "human always rules" in cc8.get("note", ""))

    # ---- explicit reproducibility of the two derived reasons (recorded numbers only) ------------
    _report("at-capacity arithmetic: recorded load 1.25 >= 1.0 (reason), horizon worst-side low 0.62 "
            "< recorded capacity 500.0 (so NOT deficit)",
            atcap["closure"]["band_horizon"] == {"low": 0.62, "high": 1.02}
            and atcap["s7l"]["q8"]["capacity_constraint"]["reason"] == "at-capacity"
            and 1.25 >= 1.0 and 0.62 < ATCAP_CAP_VALUE,
            f"horizon={atcap['closure']['band_horizon']}")
    _report("deficit arithmetic: lower-is-better horizon worst-side HIGH 32.0 = max period (projected "
            "+ sigma 8.0) >= recorded capacity VALUE 30.0",
            deficit["closure"]["band_horizon"] == {"low": 12.0, "high": 32.0}
            and deficit["closure"]["band"]["sigma"] == DEFICIT_SIGMA
            and deficit["s7l"]["q8"]["capacity_constraint"]["reason"] == "deficit"
            and DEFICIT_HORIZON_HIGH >= DEFICIT_CAP_VALUE,
            f"horizon={deficit['closure']['band_horizon']} sigma={deficit['closure']['band']['sigma']}")

    # ---- (d) the marker is a LABEL at its limit: Q7 options+best + Q8 recommendation EQUAL ------
    for r in all7:
        base = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: Q7 `options` (count + uris) + `machine_eligible_best` + Q8 "
                "`recommendation` + `floor_gated` EXACTLY equal to `cockpit_q7q8` (no §6 overrule, "
                "no re-rank, no option-removal — ALSO at the marker's non-headroom limit)",
                r["s7l"]["q7"]["options"] == base["q7"]["options"]
                and len(r["s7l"]["q7"]["options"]) == 8
                and r["s7l"]["q7"]["machine_eligible_best"] == base["q7"]["machine_eligible_best"]
                and r["s7l"]["q8"]["recommendation"] == base["q8"]["recommendation"]
                and r["s7l"]["q8"]["floor_gated"] == base["q8"]["floor_gated"],
                f"Q8={r['s7l']['q8']['recommendation']} == {base['q8']['recommendation']}")
        _report(f"{r['label']}: Q8 recommendation STILL `partial-settlement` / machine-eligible best "
                "UNCHANGED even when capacity_constraint shows a non-headroom reason",
                r["s7l"]["q8"]["recommendation"] == "partial-settlement"
                and r["s7l"]["q7"]["machine_eligible_best"] == "partial-settlement",
                f"flag={r['s7l']['q8'].get('capacity_constraint', {}).get('reason', '(none)')}")

    # ---- (e) superset byte-identity + recorded-data provenance ----------------------------------
    for r in (vmc, atcap, deficit):
        _report(f"{r['label']}: Q7/Q8 pre-existing keys intact (options/baseline/machine_eligible_best/"
                "recommendation/authority/floor_gated + do_nothing_expected_impact) — only the additive "
                "capacity_constraint block added",
                all(k in r["s7l"]["q7"] for k in ("options","baseline","machine_eligible_best"))
                and all(k in r["s7l"]["q8"] for k in ("recommendation","authority","floor_gated"))
                and "do_nothing_expected_impact" in r["s7l"]["q8"])
        cc = r["s7l"]["q8"]["capacity_constraint"]
        auth = r["sub"].graph.get(r["cfg"]["authority"]["dispute"]) or {}
        cap = auth.get("capacity") or {}
        _report(f"{r['label']}: every capacity_constraint value traces to a RECORDED field "
                "(authority.capacity {value,load} + closure.band_horizon + recorded threshold)",
                cc["recorded_capacity"] == ("%s %s (load %s)" % (cap.get("value"), cap.get("unit", ""),
                                                                 cap.get("load", "—")))
                and cc["horizon_band"] == r["closure"]["band_horizon"]
                and cc["reason"] in ("headroom", "at-capacity", "deficit"),
                f"recorded_capacity={cc['recorded_capacity']} threshold={r['closure'].get('threshold')}")

    # ---- (f) determinism (dict + render) on ALL orgs -------------------------------------------------
    for r in all7:
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: deterministic on re-run (structured dict + rendered §7L line)",
                c1 == c2 and x1 == x2)

    # ---- emit fixtures for the recorded orgs + the engine-native report --------------------------
    for r in (fc, vm, vmc, fl2, atcap, deficit):
        eng.emit_fixtures(r["sub"], HERE, r["cfg"])
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L capacity_constraint proven at its LIMIT — at-capacity / deficit — engine-native "
         "render (Sprint 28)"]
    A.append(f"generated {now_iso()}  |  `adjudication_engine._capacity_reason`/`cockpit_s7l`  |  "
             "the recorded authority `capacity` {value, unit, load} + the record-wide horizon band "
             "(band_horizon) + the recorded threshold -> one additive `capacity_constraint` block on "
             "Q7 AND Q8. Sprint-27 proved ONLY the headroom branch on a real org; Sprint 28 drives "
             "two NEW orgs that RECORD the non-headroom situation and proves the FULL block as data: "
             "`deli-atcap` (recorded load 1.25 >= 1.0 -> reason at-capacity) and `deli-deficit` "
             "(lower-is-better horizon worst-side high 32.0 >= recorded capacity value 30.0 -> "
             "reason deficit). In the non-headroom case EVERY capacity-consuming non-baseline option "
             "is marked `capacity_risk` (NEVER `capacity_infeasible`, NEVER the do-nothing baseline). "
             "A label/default, never a removal, never a directive; the Q8 recommendation is provably "
             "UNCHANGED everywhere. Additive; no engine change, no new noun, SPEC v0.22, 49 $defs, "
             "URI cap")
    A.append("")
    A.append("The capacity marker is now demonstrated at ALL THREE of its derived reasons on real "
             "orgs — headroom (default, Sprint-27 `deli-varmax-cap`), at-capacity (new `deli-atcap`, "
             "recorded load 1.25), deficit (new `deli-deficit`, recorded horizon high 32.0 >= "
             "recorded capacity value 30.0) — and at every reason it is a LABEL: the SAME machine-"
             "eligible options and the SAME Q8 recommendation remain, correctly, with only a "
             "capacity_risk label on the capacity-consuming non-baseline options. The marker never "
             "re-ranks, never removes an option, never overrules the §6 human.")
    A.append("")
    for r in (fc, vm, vmc, fl2, deli, atcap, deficit):
        A.append(f"--- {r['label']} ---")
        A.append("```")
        A.append(eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY))
        A.append("```")
        A.append("")
        cc = r["s7l"]["q8"].get("capacity_constraint")
        if cc:
            A.append(f"Q8 capacity_constraint: reason={cc['reason']}  flag={cc['flag']}  "
                     f"recorded_capacity={cc['recorded_capacity']}  "
                     f"horizon_band={cc['horizon_band']}  "
                     f"options_flagged={cc['options_flagged']}")
            A.append(f"  note: {cc['note']}")
            A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**The Sprint-27 capacity marker is now proven end-to-end at its LIMIT — the "
             "non-headroom branches are exercised AS DATA on a living Q1–Q10 cockpit.** The shared "
             "`_capacity_reason` helper, which already backed the Sprint-26 Q9 `capacity_planning_"
             "attention` label and the Sprint-27 Q7/Q8 `capacity_constraint.reason`, is now driven by "
             "two orgs that RECORD the non-headroom situation from recorded numbers only: "
             "`deli-atcap` records load 1.25 (>= 1.0 -> at-capacity) and `deli-deficit` records a "
             "lower-is-better latency series whose horizon worst-side high 32.0 reaches the recorded "
             "capacity VALUE 30.0 (-> deficit). Both emit an identical `capacity_constraint` block on "
             "Q7 and Q8: reason, flag True, `options_flagged` marking EVERY capacity-consuming "
             "non-baseline option `capacity_risk`, and NEVER the do-nothing/UNRESOLVED baseline — and "
             "the reason agrees with each org's Q9 `capacity_planning_attention` label BY "
             "CONSTRUCTION. **The marker is a LABEL at its limit:** for every org — including the "
             "at-capacity and deficit ones — the Q7 `options` (same count + uris) + `machine_"
             "eligible_best` and the Q8 `recommendation`/`floor_gated` are EXACTLY equal to the frozen "
             "`cockpit_q7q8` line (the §6 human always rules; the marker never re-ranks, never removes "
             "an option). The default stays byte-identical: no-capacity / no-band / no-data orgs carry "
             "no `capacity_constraint` key, and the Sprint-27 headroom org is unchanged. **What is "
             "still not derivable (the honest frontier):** the marker never CHOOSES a different option "
             "for the machine (the §6 human always does), and a genuinely capacity-constrained "
             "OPTIMIZATION that RE-RANKS the recommendation stays explicitly out of scope of the "
             "deterministic advisory stance — it cannot, without a recorded per-option capacity "
             "requirement, ever reach `capacity_infeasible`.")
    A.append("")
    A.append("_Additive; no engine change, frozen ontology, SPEC v0.22, 49 $defs, URI cap. The "
             "capacity marker is now a recorded-data reason at headroom / at-capacity / deficit; it "
             "never overrules the §6 human or the floor-gated recommendation._")
    (rp / "cockpit-forecast-horizon4.md").write_text("\n".join(A) + "\n")

    print("\n  -> engine-native Sprint-28 cockpit under "
          "artifacts/adjudication/reports/cockpit-forecast-horizon4.md")
    print("  -> recorded-org fixtures under artifacts/adjudication/fixtures/"
          f"{{{fc['label']},{vm['label']},{vmc['label']},{fl2['label']},{ATCAP_LABEL},{DEFICIT_LABEL}}}/ "
          "(deli no-data org emits no fixtures)")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())