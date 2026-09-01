"""run_forecast_horizon3_demo.py — SPRINT 27: recorded-capacity CONSTRAINT on the Q7/Q8 trade-off.

Sprint 26 disclosed the next honest frontier (sprints/sprint-26/notes/findings.md, "Open issues /
next work"): **the Q9 `capacity_planning_attention` is a derived, labeled REASON, but it does NOT
connect to the §7L Q7/Q8 trade-off — an org that records a capacity deficit / at-capacity reason
still sees the SAME machine-eligible options and the SAME Q8 recommendation as if its capacity were
unbounded.** Sprint 27 closes that bounded slice additively: where the org records a numeric
`capacity`, that recorded capacity becomes a data-only CONSTRAINT on the Q7/Q8 trade-off — an
additive **`capacity_constraint`** marker + reason on the affected option(s), derived from recorded
capacity + load + the horizon band + the recorded threshold, WITHOUT removing any option (the §6
human always rules) and WITHOUT changing the Q8 recommendation's ranking (still the frozen
`rank`/`machine_eligible_best`).

ONE deterministic rule, shared with the Q9 `capacity_planning_attention` label by construction (via
the extracted `_capacity_reason` helper): headroom / at-capacity (recorded load >= 1.0) / deficit
(horizon band's worst-side magnitude reaches/exceeds the recorded capacity VALUE). In headroom no
option is flagged (`options_flagged: {}`); in at-capacity/deficit the capacity-consuming
(non-baseline) options are marked `capacity_risk` — NEVER `capacity_infeasible`, because no per-option
capacity requirement is ever recorded. The marker rides as a PARALLEL `capacity_constraint` block on
`q7` and `q8` (preferred over mutating the frozen `rank`-owned `options`).

Still recorded-data only, additive (the ONLY engine file touched is adjudication_engine.py), no new
noun, frozen 49 $defs, SPEC v0.22, `ros/` untouched.

This runner (exit 0 = ALL PASS) drives the SAME ≥5 fresh orgs as Sprint 26 (reusing its builders +
constants so the source recorded data is byte-identical) and asserts Sprint-26 byte-identity of Q3 /
Q9 plus the new Q7/Q8 capacity-constraint marker on ONLY the capacity-recording org. Emits fixtures +
artifacts/adjudication/reports/cockpit-forecast-horizon3.md.
Usage: (from instances/contested_reality)  python3 run_forecast_horizon3_demo.py
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
import run_forecast_horizon2_demo as r26   # noqa: E402  (Sprint-26 org builders/constants)
import run_forecast_horizon_demo as rfh    # noqa: E402  (Sprint-25 builders/constants)

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")


def run_all() -> int:
    print("=== SPRINT 27 — recorded-capacity CONSTRAINT on the Q7/Q8 trade-off ===\n")
    # Same ≥5 fresh orgs + same recorded data as Sprint 26 (byte-identical source):
    o = r26.build_orgs()
    fc, vm, vmc, fl2, deli = o["fc"], o["vm"], o["vmc"], o["fl2"], o["deli"]

    # ---- (a) ALL orgs keep the full §7L Q1–Q10 cockpit -----------------------------------------
    for r in (fc, vm, vmc, fl2, deli):
        c = r["s7l"]
        full = all(isinstance(c[k], dict) for k in ("q1","q2","q3","q4","q5","q6","q7","q8","q9","q10"))
        ev = all(bool(c[k].get("evidence")) for k in ("q1","q2","q3","q4","q5","q6","q9","q10"))
        _report(f"{r['label']}: FULL §7L Q1–Q10 cockpit + data evidence present",
                full and ev and bool(c["q1"]["events"]) and bool(c["q7"]["options"])
                and bool(c["q8"]["authority"]) and bool(c["q10"]["determination"]),
                f"q6.avail={c['q6']['forecast_available']} q3 items={c['q3']['count']}")

    # ---- (b) Sprint-26 byte-identity: Q3 horizon suffix + Q9 capacity_planning_attention -------
    fc_att = [i for i in fc["s7l"]["q3"]["prioritized"] if i.get("tag") == "forecast"]
    _report(f"{fc['label']}: Q3 `why` STILL the Sprint-26 string (strict-prefix horizon suffix "
            "unchanged — Sprint-26 byte-identity)",
            len(fc_att) == 1
            and fc_att[0]["why"] == (r26.rfv.FC_SINGLE_WHY
                                     + (" — recorded band 0.71…0.89 (± σ 0.09); worst side "
                                        "0.71 below target 0.95")
                                     + r26.R26_HORIZON.format(lo=0.71, hi=0.93, n=3)),
            fc_att[0]["why"])
    cpa = vmc["s7l"]["q9"].get("capacity_planning_attention")
    _report(f"{vmc['label']}: Q9 `capacity_planning_attention` UNCHANGED (Sprint-26 byte-identity "
            "{flag,why}, derived headroom)",
            isinstance(cpa, dict) and cpa["flag"] is False
            and "500.0 resolutions/day (load 0.72)" in cpa["why"]
            and "horizon-wide recorded band 0.62…1.02 across 3 projection periods" in cpa["why"]
            and "derived headroom" in cpa["why"], str(cpa))
    for r in (fc, vm, fl2, deli):
        _report(f"{r['label']}: NO `capacity_planning_attention` (+ no `capacity_constraint`) — "
                "Sprint-26 byte-identity",
                "capacity_planning_attention" not in r["s7l"]["q9"]
                and "capacity_constraint" not in r["s7l"]["q7"]
                and "capacity_constraint" not in r["s7l"]["q8"])

    # ---- (c) Q7/Q8 capacity_constraint on ONLY the capacity-recording org ---------------------
    vcc7 = vmc["s7l"]["q7"].get("capacity_constraint")
    vcc8 = vmc["s7l"]["q8"].get("capacity_constraint")
    _report(f"{vmc['label']}: Q7 AND Q8 both carry `capacity_constraint` (recorded numeric capacity "
            "+ band + threshold all exist)", isinstance(vcc7, dict) and isinstance(vcc8, dict)
            and vcc7 == vcc8, str(vcc8))
    _report(f"{vmc['label']}: block names the RECORDED capacity + load + the horizon-wide recorded band",
            isinstance(vcc8, dict) and vcc8.get("recorded_capacity") == "500.0 resolutions/day (load 0.72)"
            and vcc8.get("horizon_band") == {"low": 0.62, "high": 1.02})
    _report(f"{vmc['label']}: reason = headroom (recorded load 0.72 < 1.0; horizon worst-side 0.62 "
            "< recorded capacity 500.0) — NO option marked infeasible",
            isinstance(vcc8, dict) and vcc8["reason"] == "headroom"
            and vcc8["flag"] is False and vcc8["options_flagged"] == {})
    _report(f"{vmc['label']}: constraint reason AGREES with the Q9 capacity label BY CONSTRUCTION "
            "(shared `_capacity_reason` rule)", isinstance(vcc8, dict)
            and vcc8["reason"] == "headroom"
            and cpa is not None and cpa["flag"] is False and vcc8["flag"] is False)
    _report(f"{vmc['label']}: block is a LABEL — never a removal, never a directive (note names the "
            "UNCHANGED Q8 recommendation + §6 human)",
            isinstance(vcc8, dict)
            and "UNCHANGED" in vcc8.get("note", "") and "human always rules" in vcc8.get("note", ""))

    # ---- (d) other orgs carry NO capacity_constraint key (byte-identical superset) -------------
    for r in (fc, vm, fl2, deli):
        _report(f"{r['label']}: NO `capacity_constraint` key on Q7 or Q8 (no recorded capacity / "
                "no band — byte-identical), Q7 `options` + Q8 `recommendation` untouched",
                "capacity_constraint" not in r["s7l"]["q7"]
                and "capacity_constraint" not in r["s7l"]["q8"]
                and r["s7l"]["q7"]["options"] and r["s7l"]["q8"]["recommendation"])

    # ---- (e) Q7 option set UNCHANGED + Q8 recommendation/machine-eligible-best EQUAL to q7q8 ----
    for r in (fc, vm, vmc, fl2, deli):
        base = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: Q7 `options` (count + uris) UNCHANGED vs `cockpit_q7q8`, and Q8 "
                "`recommendation` + `machine_eligible_best` EQUAL (no §6 overrule, no re-rank)",
                r["s7l"]["q7"]["options"] == base["q7"]["options"]
                and r["s7l"]["q7"]["machine_eligible_best"] == base["q7"]["machine_eligible_best"]
                and r["s7l"]["q8"]["recommendation"] == base["q8"]["recommendation"]
                and r["s7l"]["q8"]["floor_gated"] == base["q8"]["floor_gated"],
                f"{r['s7l']['q8']['recommendation']} == {base['q8']['recommendation']}")

    # ---- (f) superset byte-identity: prior keys intact on the capacity org -----------------------
    _report(f"{vmc['label']}: Q7/Q8 pre-existing keys intact (options/baseline/machine_eligible_best/"
            "recommendation/authority/floor_gated + do_nothing_expected_impact) — only the additive "
            "capacity_constraint block added",
            all(k in vmc["s7l"]["q7"] for k in ("options","baseline","machine_eligible_best"))
            and all(k in vmc["s7l"]["q8"] for k in ("recommendation","authority","floor_gated"))
            and "do_nothing_expected_impact" in vmc["s7l"]["q8"]
            and vmc["s7l"]["q8"]["recommendation"] == "partial-settlement")

    # ---- (g) determinism on re-run (dict + render) ----------------------------------------------
    for r in (fc, vm, vmc, fl2, deli):
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: deterministic on re-run (structured dict + rendered §7L line)",
                c1 == c2 and x1 == x2)

    # ---- (h) every value from recorded data only (no wall-clock, no invented number) ------------
    auth = vmc["sub"].graph.get(vmc["cfg"]["authority"]["dispute"]) or {}
    recorded_cap = auth.get("capacity") or {}
    _report("`capacity_constraint` derived from RECORDED data only (recorded authority capacity == "
            "the graph field; horizon band == the closure's band_horizon; reason from recorded "
            "load/band/capacity)",
            vcc8 is not None
            and vcc8["recorded_capacity"] == ("%s %s (load %s)"
                                              % (recorded_cap.get("value"), recorded_cap.get("unit", ""),
                                                 recorded_cap.get("load", "—")))
            and vcc8["horizon_band"] == vmc["closure"]["band_horizon"])

    # ---- (i) the non-headroom branch is real (rule not vacuous): helper flags at-capacity/deficit
    _report("helper-level proof of the non-vacuous rule: at-capacity (load 1.2) + deficit "
            "(horizon worst-side >= capacity) both flag True; our headroom org flags False",
            eng._capacity_reason({"value": 5.0, "unit": "x/day", "load": 1.2},
                                 {"low": 0.62, "high": 1.02}, "higher-is-better")[1] is True
            and eng._capacity_reason({"value": 0.5, "unit": "frac", "load": 0.7},
                                     {"low": 0.62, "high": 1.02}, "higher-is-better")[0] == "deficit"
            and eng._capacity_reason({"value": 500.0, "unit": "res/day", "load": 0.72},
                                     {"low": 0.62, "high": 1.02}, "higher-is-better")
            == ("headroom", False))

    # ---- emit fixtures for the recorded orgs + the engine-native report --------------------------
    for r in (fc, vm, vmc, fl2):
        eng.emit_fixtures(r["sub"], HERE, r["cfg"])
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L recorded-capacity CONSTRAINT on the Q7/Q8 trade-off — engine-native render (Sprint 27)"]
    A.append(f"generated {now_iso()}  |  `adjudication_engine._capacity_reason`/`cockpit_s7l`  |  "
             "recorded authority `capacity` {value, unit, load} + the record-wide horizon band "
             "(band_horizon) + the recorded threshold -> an additive `capacity_constraint` block on "
             "Q7 AND Q8, emitted ONLY where a numeric capacity + band + threshold are recorded. It "
             "names the recorded capacity/load/band, derives ONE reason (headroom / at-capacity / "
             "deficit) from recorded numbers only — the SAME rule as the Sprint-26 Q9 "
             "capacity_planning_attention label (shared `_capacity_reason`, agree by construction) — "
             "and in `options_flagged` marks capacity-consuming non-baseline options `capacity_risk` "
             "when _not_ headroom (NEVER `capacity_infeasible`: no per-option requirement is ever "
             "recorded). A label/default, never a removal, never a directive; the Q8 recommendation "
             "is provably UNCHANGED. Additive; the capacity org carries ONLY this block; no-capacity "
             "orgs are byte-identical.  |  SPEC v0.22, 49 $defs, URI cap")
    A.append("")
    A.append("The recorded capacity now reaches the §7L Q7/Q8 trade-off as a data-only REASON: the "
             "org's recorded capacity/load and the whole-horizon recorded band are named ON the "
             "trade-off, and any option the recorded numbers put at- or over-capacity is flagged "
             "`capacity_risk` — never removed, never re-ranked, never overruling the §6 human. When "
             "the recorded data shows headroom (as here: capacity 500 ≫ horizon 0.62…1.02, load "
             "0.72), no option is flagged. The Q8 recommendation + machine-eligible best stay the "
             "frozen `rank` output.")
    A.append("")
    for r in (fc, vm, vmc, fl2, deli):
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
    A.append("**The recorded capacity now reaches the Q7/Q8 trade-off as a data-only REASON.** Where "
             "the org records a numeric `capacity` (plus a band + numeric threshold), both Q7 and Q8 "
             "carry an additive `capacity_constraint` block naming the recorded capacity value/unit/"
             "load and the horizon-wide recorded band, with one deterministic REASON derived from "
             "recorded numbers only via the SAME shared rule as the Q9 `capacity_planning_attention` "
             "label (agree by construction): headroom / at-capacity (load >= 1.0) / deficit (horizon "
             "worst-side >= capacity value). In headroom no option is flagged; at at-capacity/deficit "
             "the capacity-consuming non-baseline options are marked `capacity_risk` — never "
             "`capacity_infeasible`, because a per-option capacity requirement is never recorded. It "
             "is a label/default: it NEVER removes an option, NEVER changes the frozen "
             "`rank`/`machine_eligible_best`, and NEVER overrules the §6 human — the Q8 recommendation "
             "is provably UNCHANGED (asserted EQUAL to `cockpit_q7q8` for every org, and the Q7 option "
             "set unchanged). The default is byte-identical: a no-capacity / no-band / no-data org "
             "carries NO `capacity_constraint` key. **What is still not derivable (the honest "
             "frontier):** the marker is a reason, not a choice — it never CHOOSES a different option "
             "for the machine (the §6 human always does), and a genuinely capacity-constrained "
             "optimization that RE-RANKS the recommendation stays explicitly out of scope of the "
             "deterministic advisory stance (it cannot, without a recorded per-option capacity "
             "requirement, ever reach `capacity_infeasible`).")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs. `capacity_constraint` labels what the "
             "recorded capacity makes risky on the trade-off; it never overrules the §6 human or the "
             "floor-gated recommendation._")
    (rp / "cockpit-forecast-horizon3.md").write_text("\n".join(A) + "\n")

    print("\n  -> engine-native Sprint-27 cockpit under "
          "artifacts/adjudication/reports/cockpit-forecast-horizon3.md")
    print("  -> recorded-org fixtures under artifacts/adjudication/fixtures/"
          f"{{{fc['label']},{vm['label']},{vmc['label']},{fl2['label']}}}/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())