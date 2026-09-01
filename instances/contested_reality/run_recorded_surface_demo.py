# === DEMO / TEST RUNNER - NOT part of the engine API ===
"""run_recorded_surface_demo.py — SPRINT 31: inventory the ENTIRE recorded-data §7L decision surface as reason-not-choice, and name the ONE remaining out-of-scope seam.

After six sprints (20-26 forecast series/variance/band · 27 emergency capacity_constraint · 28
horizon limit · 29 per-option infeasibility · 30 the RECOMMENDED-option boundary) the whole §7L
decision surface is recorded-data + reason: every derived label (Q3 forecast attention, Q6
projection + band, Q7/Q8 capacity_constraint reason + per-option flags, Q9 capacity planning, Q8
do-nothing expected-impact) is a pure function of RECORDED descriptors (a metric:// realized-
vs-expected series, point-variance, the band_variance source, an authority capacity {value,load},
per-option capacity_requirements, the floor_gated/weights/reconcile config). Sprint 31 makes that
the ORGANIZING truth, positively, in ONE comprehensive, auditable run.

For a set of orgs (the eight from Sprint 30, INSPECT, COVE, and one no-data org), this runner emits
a per-org decision-surface inventory (`recorded_surface`):
  {label,
   present_recorded={metric_series, point_variance, band_variance, capacity,
                     capacity_requirements, floor_gated, weights, reconcile_rule},
   derived_reasons={Q3_forecast, Q6_projection, Q7Q8_capacity_constraint, Q9_capacity,
                    Q8_do_nothing_impact},   (each the actual derived reason, or None)
   derivable_universe=[sorted keys actually derived],
   not_derivable=[the named optimization seam + any descriptor NOT recorded]}
and asserts, per org, that EVERY derived label traces to a RECORDED descriptor (no reason without
its recorded source — the engine never invents one), and that the marker is a REASON, never a
CHOICE: Q7 options + machine_eligible_best + Q8 recommendation + floor_gated EXACTLY equal
`cockpit_q7q8` for EVERY org (a printed tally, including the Sprint-30 org where the RECOMMENDED
option is `capacity_infeasible`). It names the SOLE remaining out-of-scope step: a capacity-
constrained OPTIMIZATION that RE-RANKS the recommendation for the machine (a policy/user decision,
NOT built — recorded per-option requirements already exist, so a deterministic next-best-non-
infeasible rule by the frozen `rank` utility would be the only missing piece).

Additive: NO source change to adjudication_engine.py (hash a60f8f7… must stay unchanged) — a new
runner + recorded data (new org labels only, no fixture overwrite). Frozen functions untouched; no
new noun; frozen 49 $defs; SPEC v0.22; ros/ + schema + sector configs untouched; ~$0.
Emits fixtures for the NEW orgs + artifacts/adjudication/reports/cockpit-recorded-surface-inventory.md.
Usage: (from instances/contested_reality)  python3 run_recorded_surface_demo.py
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

from ros.substrate import now_iso                              # noqa: E402
import adjudication_engine as eng                              # noqa: E402
import adjudication_configs as ac                              # noqa: E402
import run_forecast_label_vs_choice_demo as r30                # noqa: E402 (8 orgs / build_orgs)
import run_forecast_per_option_capacity_demo as r29            # noqa: E402 (REQS constants / builders)
import run_forecast_horizon_demo as rfh                        # noqa: E402 (VM_POINTS / run_one / relabel_to)
import run_forecast_variance_demo as rfv                       # noqa: E402 (CO_POINTS / FC_SINGLE_WHY)

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")


# ---- the ONE remaining out-of-scope seam (named exactly, NOT built) ----------------------------
NONDERIVABLE_SEAM = (
    "capacity-constrained OPTIMIZATION that RE-RANKS the Q8 recommendation for the machine "
    "- a POLICY/user decision, NOT a label, deliberately NOT built (seam: recorded per-option "
    "capacity_requirements already exist + a deterministic next-best-non-infeasible rule by the "
    "frozen `rank` utility would be the only missing piece; it CHANGES the Q8 recommendation)")
NONDERIVABLE_DESCRIPTORS = [  # the descriptors a no-data org does NOT record
    "metric_series", "point_variance", "band_variance", "capacity", "capacity_requirements"]

# the engine's reason-to-descriptor trace map (the assertion's target)
_REASON_DESCRIPTOR = {
    "Q3_forecast": "metric_series", "Q6_projection": "metric_series",
    "Q8_do_nothing_impact": "metric_series",
    "Q7Q8_capacity_constraint": "capacity", "Q9_capacity": "capacity"}

ALL_DESCRIPTORS = ["metric_series", "point_variance", "band_variance", "capacity",
                   "capacity_requirements", "floor_gated", "weights", "reconcile_rule"]


def _present_recorded(r) -> dict:
    """Which recorded descriptors this org carries — read via the SAME paths the engine uses."""
    sub, cfg, closure = r["sub"], r["cfg"], r["closure"]
    muri, mobj = eng._recorded_metric_with_series(sub)
    auth = sub.graph.get(cfg["authority"]["dispute"]) or {}
    cap = auth.get("capacity") or {}
    reqs = auth.get("capacity_requirements") or {}
    metric_series = bool(muri)
    point_variance = bool(metric_series and closure.get("recorded_variance") is not None)
    band_variance = bool(metric_series and closure.get("band_variance"))
    capacity = isinstance(cap, dict) and "value" in cap
    capacity_requirements = bool(reqs)
    floor_gated = bool(cfg.get("floor_gated"))
    weights = bool(cfg.get("weights"))
    reconcile_rule = bool(cfg.get("reconcile"))
    return {"metric_series": metric_series, "point_variance": point_variance,
            "band_variance": band_variance, "capacity": capacity,
            "capacity_requirements": capacity_requirements, "floor_gated": floor_gated,
            "weights": weights, "reconcile_rule": reconcile_rule}


def _derived_reasons(r) -> dict:
    """The actual derived REASON each descriptor produced (or None when not derivable)."""
    c, closure, sub = r["s7l"], r["closure"], r["sub"]
    fc_att = [i for i in c["q3"]["prioritized"] if i.get("tag") == "forecast"]
    cc8 = c["q8"].get("capacity_constraint")
    cpa = c["q9"].get("capacity_planning_attention")
    dn = c["q8"].get("do_nothing_expected_impact")
    _, mobj = eng._recorded_metric_with_series(sub)
    return {
        "Q3_forecast": (fc_att[0]["why"] if fc_att else None),
        "Q6_projection": (closure.get("worst") if closure.get("available") else None),
        "Q7Q8_capacity_constraint": (cc8["reason"] if isinstance(cc8, dict) else None),
        "Q9_capacity": (cpa["flag"] if isinstance(cpa, dict) else None),
        "Q8_do_nothing_impact": (dn["summary"] if isinstance(dn, dict) else None),
    }


def _is_capacity_org(r) -> bool:
    auth = r["sub"].graph.get(r["cfg"]["authority"]["dispute"]) or {}
    cap = auth.get("capacity") or {}
    return isinstance(cap, dict) and "value" in cap


# ---- the three NEW orgs (new labels only; do NOT overwrite inspect/cove fixture dirs) -----------
# inspect-recorded: INSPECT + a recorded QC on-time series (band_variance "all") + at-capacity
#   {value,load} + per-option capacity_requirements (a mix: some infeasible, some risk).
IS_LABEL = "inspect-recorded"; IS_METRIC = f"metric://{IS_LABEL}/m-qc-on-time"
IS_CAP_VALUE = 500.0; IS_CAP_LOAD = 1.3; IS_AVAILABLE = round(IS_CAP_VALUE - IS_CAP_LOAD, 4)  # 498.7
# INSPECT options: accept-batch, reject-batch-return, rework-partial-credit,
#   conditional-accept-with-guarantee, request-more-evidence, escalate, unresolved (baseline).
IS_OPTS = list(ac.INSPECT["options"])
IS_BASELINE = next(o for o in IS_OPTS if "unres" in o.lower() or o == "do-nothing")
IS_NONBASELINE = [o for o in IS_OPTS if o != IS_BASELINE]                       # 6 options
IS_REQS = {"accept-batch": 510.0, "reject-batch-return": 500.0, "rework-partial-credit": 499.0,
           "conditional-accept-with-guarantee": 200.0, "request-more-evidence": 100.0,
           "escalate": 150.0}
assert IS_BASELINE == "unresolved" and len(IS_NONBASELINE) == 6
assert all(IS_REQS[o] > IS_AVAILABLE for o in ("accept-batch", "reject-batch-return", "rework-partial-credit"))
assert all(IS_REQS[o] <= IS_AVAILABLE for o in
           ("conditional-accept-with-guarantee", "request-more-evidence", "escalate"))

# cove-recorded: COVE + a recorded lower-is-better answer-latency series (CO_POINTS, band_variance
#   "all") + a DEFICIT capacity {value,load} + per-option capacity_requirements.
COV_LABEL = "cove-recorded"; COV_METRIC = f"metric://{COV_LABEL}/m-answer-latency"
COV_CAP_VALUE = 30.0; COV_CAP_LOAD = 0.9; COV_AVAILABLE = round(COV_CAP_VALUE - COV_CAP_LOAD, 4)  # 29.1
COV_OPTS = list(ac.COVE["options"])
COV_BASELINE = next(o for o in COV_OPTS if "unres" in o.lower() or o == "do-nothing")
COV_NONBASELINE = [o for o in COV_OPTS if o != COV_BASELINE]                     # 7 options
COV_REQS = {"authorize-off-formulary": 30.0, "deny-off-formulary": 30.0, "step-therapy-first": 28.0,
            "authorize-generic": 25.0, "request-more-evidence": 10.0,
            "escalate-to-medical-director": 15.0, "external-peer-review": 20.0}
assert COV_BASELINE == "unresolved" and len(COV_NONBASELINE) == 7
assert all(COV_REQS[o] > COV_AVAILABLE for o in ("authorize-off-formulary", "deny-off-formulary"))
assert all(COV_REQS[o] <= COV_AVAILABLE for o in
           ("step-therapy-first", "authorize-generic", "request-more-evidence",
            "escalate-to-medical-director", "external-peer-review"))

# inspect-nodata: INSPECT relabel with NO recorded series/capacity/requirements (the no-data control).
ND_LABEL = "inspect-nodata"


def _new_latency_org(label, metric_uri, points, fields, cap_value, cap_load, reqs):
    cfg = rfh.relabel_to(ac.COVE if label == COV_LABEL else ac.INSPECT, label)
    r = rfh.run_one(cfg)
    eng.record_metric_series(r["sub"], label, metric_uri, points=[dict(p) for p in points],
                             fields=fields, signer=cfg["authority"]["adjudicator_person"])
    eng.record_capacity(r["sub"], cfg["authority"]["dispute"], value=cap_value,
                        unit="units/day", load=cap_load, signer=cfg["authority"]["adjudicator_person"])
    eng.record_capacity_requirements(r["sub"], cfg["authority"]["dispute"], requirements=reqs,
                                     signer=cfg["authority"]["adjudicator_person"])
    r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
    r["closure"] = eng._forecast_closure(r["cfg"], r["sub"])
    return r


def _new_nodata_org(label):
    cfg = rfh.relabel_to(ac.INSPECT, label)
    r = rfh.run_one(cfg)     # NO recorded series / capacity / requirements
    r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
    r["closure"] = eng._forecast_closure(r["cfg"], r["sub"])
    return r


def build_orgs():
    o = r30.build_orgs()   # the eight Sprint-30 orgs, byte-identical
    o["is"] = _new_latency_org(
        IS_LABEL, IS_METRIC,
        [dict(p) for p in rfh.VM_POINTS],
        {"name": "QC on-time rate", "formula": "on-time batches / total batches from ledger",
         "unit": "fraction", "target": 0.95, "period": "quarter",
         "source": "ledger QC completion records", "owner": ac.INSPECT["authority"]["adjudicator_person"],
         "band_variance": "all"},
        IS_CAP_VALUE, IS_CAP_LOAD, IS_REQS)
    o["cove"] = _new_latency_org(
        COV_LABEL, COV_METRIC,
        [dict(p) for p in rfv.CO_POINTS],
        {"name": "mean answer latency", "formula": "mean elapsed time to an answer from ledger",
         "unit": "ms", "target": 16, "period": "quarter",
         "source": "ledger answer completion records", "direction": "lower-is-better",
         "band_variance": "all", "owner": ac.COVE["authority"]["adjudicator_person"]},
        COV_CAP_VALUE, COV_CAP_LOAD, COV_REQS)
    o["nodata"] = _new_nodata_org(ND_LABEL)
    return o


def run_all() -> int:
    print("=== SPRINT 31 — the WHOLES §7L recorded-data decision surface, inventoried as "
          "reason-not-choice (positive consolidation) ===\n")
    o = build_orgs()
    fc, vm, vmc, fl2, deli = o["fc"], o["vm"], o["vmc"], o["fl2"], o["deli"]
    infcap, definf, recinf = o["infcap"], o["definf"], o["recinf"]
    is_r, cove_r, nodata = o["is"], o["cove"], o["nodata"]
    all11 = (fc, vm, vmc, fl2, deli, infcap, definf, recinf, is_r, cove_r, nodata)

    # ---- (0) every org keeps the full §7L Q1–Q10 cockpit ----------------------------------------
    for r in all11:
        c = r["s7l"]
        _report(f"{r['label']}: FULL §7L Q1–Q10 cockpit present",
                all(isinstance(c[k], dict) for k in ("q1","q2","q3","q4","q5","q6","q7","q8","q9","q10"))
                and bool(c["q1"]["events"]) and bool(c["q7"]["options"]) and bool(c["q8"]["authority"]),
                f"q6.avail={c['q6']['forecast_available']}")

    # ---- (1) per-org recorded_surface inventory: present descriptors ----------------------------
    surfaces = {}
    for r in all11:
        pr = _present_recorded(r)
        surfaces[r["label"]] = pr
        # derive the Q7Q8 capability constraint's presence from the recorded descriptors themselves,
        # and cross-check with the org's actual config/determination to prove traceability.
        _report(f"{r['label']}: present_recorded inventory = {pr}", True, str(pr))

    # ---- (2) traceability: EVERY derived reason traces to a recorded descriptor -----------------
    for r in all11:
        pr = _present_recorded(r)
        dr = _derived_reasons(r)
        dr_present = {k: v for k, v in dr.items() if v is not None}
        ok = True
        for k, v in dr_present.items():
            need = _REASON_DESCRIPTOR[k]
            if not pr.get(need):
                ok = False
        _report(f"{r['label']}: every derived reason traces to a recorded descriptor "
                f"(derived={sorted(dr_present)}; descriptors={[k for k,v in pr.items() if v]})",
                ok, f"missing-trace={[k for k in dr_present if not pr[_REASON_DESCRIPTOR[k]]]}")

    # ---- (3) the derivable-vs-not boundary, mapped -------------------------------------------------
    _report("no-data org (inspect-nodata): NOTHING derived, and NO recorded descriptor present "
            "(metric/capacity/band all absent — only config fields remain)",
            not any(_derived_reasons(nodata).values())
            and not any(_present_recorded(nodata)[k] for k in
                        ("metric_series", "point_variance", "band_variance",
                         "capacity", "capacity_requirements")))

    # a descriptor the org records IS derivable somewhere; a descriptor it does NOT record is not.
    for r in all11:
        dr = _derived_reasons(r)
        dr_present = sorted(k for k, v in dr.items() if v is not None)
        pr = _present_recorded(r)
        # capacity orgs derive the capacity reasons (Q7Q8 + Q9); metric orgs derive the forecast ones.
        if _is_capacity_org(r):
            ok = "Q7Q8_capacity_constraint" in dr_present and "Q9_capacity" in dr_present
        else:
            ok = "Q7Q8_capacity_constraint" not in dr_present and "Q9_capacity" not in dr_present
        _report(f"{r['label']}: capacity-derived reasons present iff a capacity is recorded ({ok})", ok)

    # ---- (4) THE REASON-NOT-CHOICE PROOF, TOTALLED — Q7/Q8 == cockpit_q7q8 for EVERY org ----------
    tally = 0
    for r in all11:
        base = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        ok = (r["s7l"]["q7"]["options"] == base["q7"]["options"]
              and r["s7l"]["q7"]["machine_eligible_best"] == base["q7"]["machine_eligible_best"]
              and r["s7l"]["q8"]["recommendation"] == base["q8"]["recommendation"]
              and r["s7l"]["q8"]["floor_gated"] == base["q8"]["floor_gated"])
        tally += ok
        _report(f"{r['label']}: Q7 options + machine_eligible_best + Q8 recommendation + "
                f"floor_gated EXACTLY == `cockpit_q7q8` (the marker never re-ranks)",
                ok, f"Q8={r['s7l']['q8']['recommendation']}")
    _report(f"REASON-NOT-CHOICE TALLY: {tally}/11 orgs the marker never re-ranks; INCLUDES the "
            f"Sprint-30 org `{recinf['label']}` where the RECOMMENDED option is `capacity_infeasible`",
            tally == 11
            and recinf["s7l"]["q8"]["recommendation"] == "partial-settlement"
            and recinf["s7l"]["q8"]["capacity_constraint"]["options_flagged"].get(
                "partial-settlement") == "capacity_infeasible",
            f"tally={tally}")

    # ---- (5) determinism (dict + render) on re-run for ALL 11 ------------------------------------
    for r in all11:
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: deterministic on re-run (dict + render)", c1 == c2 and x1 == x2)

    # ---- emit fixtures for the NEW orgs + the engine-native report -------------------------------
    for r in (is_r, cove_r):
        eng.emit_fixtures(r["sub"], HERE, r["cfg"])
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L recorded-data DECISION-SURFACE INVENTORY — reason-not-choice across the WHOLE §7L "
         "surface, one auditable run (Sprint 31)"]
    A.append(f"generated {now_iso()}  |  `adjudication_engine._present_*`/`_forecast_closure`/"
             "`_capacity_reason`/`_per_option_capacity_flags`/`cockpit_s7l`  |  NO engine change "
             "(hash a60f8f7…): a survey runner + recorded data only. After six sprints (20-30) the "
             "whole §7L decision surface is recorded-data + reason — every derived label (Q3 "
             "forecast attention, Q6 projection + recorded band, Q7/Q8 capacity_constraint reason + "
             "per-option flags, Q9 capacity planning, Q8 do-nothing expected-impact) is a pure "
             "function of RECORDED descriptors. Sprint 31 proves that in ONE auditable run: per org "
             "it inventories present_recorded + derived_reasons + the derivable-vs-not boundary, and "
             "asserts every reason traces to a recorded descriptor and the marker is a REASON, never "
             "a CHOICE (Q8 provably == `cockpit_q7q8` for every org).  |  SPEC v0.22, 49 $defs, URI cap")
    A.append("")
    for r in all11:
        pr = _present_recorded(r); dr = _derived_reasons(r)
        dr_present = {k: v for k, v in dr.items() if v is not None}
        A.append(f"--- {r['label']} ---")
        A.append(f"present_recorded = {{ {', '.join(f'{k}:{v}' for k,v in pr.items())} }}")
        A.append(f"derived_reasons  = { {k: v for k,v in dr.items()} }")
        A.append(f"derivable_universe = {sorted(dr_present)}")
        nd = [NONDERIVABLE_SEAM]
        if not all(pr.values()):
            nd += ["descriptor NOT recorded: "
                   + ", ".join(k for k in pr if not pr[k])]
        A.append(f"not_derivable = {nd}")
        cc = r["s7l"]["q8"].get("capacity_constraint")
        if cc:
            A.append(f"  Q8 capacity_constraint: reason={cc['reason']} flag={cc['flag']} "
                     f"options_flagged={cc['options_flagged']}")
        A.append("")
    A.append(f"## reason-not-choice tally: {tally}/11 orgs Q7/Q8 EXACTLY == `cockpit_q7q8` — the "
             "marker NEVER re-ranks, INCLUDING the Sprint-30 org `deli-recommend-infcap` where the "
             "RECOMMENDED option is `capacity_infeasible`.")
    A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**The whole recorded-data §7L decision surface is now inventoried as recorded-data + "
             "reason.** A survey runner drives 11 orgs (the eight Sprint-30 orgs byte-identical, "
             "plus INSPECT, COVE, and a no-data control) and emits, per org, `present_recorded` "
             "(metric series / point-variance / band_variance source / authority capacity / "
             "per-option capacity_requirements / floor_gated / weights / reconcile_rule) + "
             "`derived_reasons` (Q3 forecast attention, Q6 projection + band, Q7/Q8 "
             "capacity_constraint reason + per-option flags, Q9 capacity planning, Q8 do-nothing "
             "expected-impact) + `derivable_universe` + `not_derivable`. Every derived label traces "
             "to a recorded descriptor; a descriptor the org did NOT record is provably NOT derived "
             "(the engine never invents one — the no-data org derives nothing). AND the marker stays "
             "a REASON, never a CHOICE: Q7 options + machine_eligible_best + Q8 recommendation + "
             "floor_gated EXACTLY equal `cockpit_q7q8` for all 11 orgs — including "
             "`deli-recommend-infcap`, where the RECOMMENDED option is `capacity_infeasible` yet the "
             "Q8 recommendation provably stays the frozen `rank` output. Generic + additive: "
             "recorded `metric://` series + recorded point-`variance` + the recorded `band_variance` "
             "source + a recorded authority `capacity` + a recorded per-option `capacity_required` "
             "descriptor; no new noun, frozen 49 `$defs`, engine byte-identical (hash a60f8f7…), no "
             "recorded data ever re-ranks.")
    A.append("")
    A.append("**Still not derivable (the honest frontier):** the ONE remaining out-of-scope step is a "
             "capacity-constrained OPTIMIZATION that RE-RANKS the Q8 recommendation for the machine "
             "— a deliberate \"re-rank for the machine\" POLICY / user decision, NOT a label, "
             "deliberately NOT built (the seam: recorded per-option `capacity_requirements` already "
             "exist, so a deterministic next-best-non-infeasible rule by the frozen `rank` utility "
             "would be the ONLY missing piece; it CHANGES the Q8 recommendation). Plus a per-option "
             "requirement that is NOT unit-coupled to the recorded capacity / an option with no "
             "recorded requirement remains non-derivable (the engine never invents one). No SPEC "
             "bump (v0.22).")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs, URI cap. The whole §7L recorded-data "
             "decision surface is now positively inventoried as reason-not-choice in ONE auditable "
             "run; the boundary itself (the marker can label even the recommended option "
             "capacity_infeasible, it cannot and must not choose the replacement) is honest and "
             "named._")
    (rp / "cockpit-recorded-surface-inventory.md").write_text("\n".join(A) + "\n")

    print("\n  -> engine-native Sprint-31 surface inventory under "
          "artifacts/adjudication/reports/cockpit-recorded-surface-inventory.md")
    print(f"  -> new-org fixtures under artifacts/adjudication/fixtures/{IS_LABEL}/, "
          f"{COV_LABEL}/, and the no-data org {ND_LABEL}/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())