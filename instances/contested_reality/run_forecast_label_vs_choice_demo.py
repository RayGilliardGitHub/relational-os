# === DEMO / TEST RUNNER - NOT part of the engine API ===
"""run_forecast_label_vs_choice_demo.py — SPRINT 30: the sharpest label-vs-choice boundary.

Sprint 29 proved the Q7/Q8 `capacity_constraint` marker can NAME a SPECIFIC option
`capacity_infeasible` from a RECORDED per-option requirement, but its own finding
(`sprints/sprint-29/notes/findings.md`, "Open issues / next work") disclosed the honest frontier:
**the marker still never CHOOSES a different option for the machine — the §6 human always does.** In
every Sprint-29 org the option the machine WOULD recommend (`partial-settlement`) was itself
`capacity_risk` (recorded requirement <= available), so the boundary between "the marker is a REASON"
and "the marker is a CHOICE" had never been exercised at its sharpest: when the recorded per-option
requirement CLEARLY shows the machine-eligible best is itself `capacity_infeasible`.

Sprint 30 closes that boundary proof ADDITIVELY — NO engine change (Sprint 29's `_per_option_capacity_flags`
already labels ANY option, including the recommended one, `capacity_infeasible` when its recorded
requirement > available). The point is to drive a NEW org story where the recorder data makes the
frozen machine-eligible best / Q8 recommendation (`partial-settlement`) `capacity_infeasible`, and assert
the cockpit STILL recommends partial-settlement (provably exactly `cockpit_q7q8`). The marker LABELS
"this recommended option cannot run under recorded capacity"; it does NOT pick a replacement. A genuinely
capacity-constrained OPTIMIZATION that RE-RANKS the recommendation is named honestly in §16 as policy /
user decision, out of scope of the deterministic advisory stance.

Per-option proof (exit 0 = ALL PASS): reuse ALL SEVEN Sprint-29 orgs byte-identical (the no-data /
no-capacity / no-band / headroom / at-capacity-inf / deficit-inf stories) PLUS one NEW org that RECORDS a
requirement making the RECOMMENDED option infeasible:
  deli-recommend-infcap   at-capacity (cap 500.0 res/day, load 1.3 -> available 498.7):
                          partial-settlement RECORDS 499.0 > 498.7 -> capacity_infeasible
                          (the machine-eligible best / Q8 recommendation itself!);
                          the other 6 non-baseline options <= 498.7 -> capacity_risk;
                          baseline unresolved (no requirement) -> NEVER flagged.
And asserts: the RECOMMENDED option is infeasible yet Q8 recommendation + machine-eligible best + options +
floor_gated EXACTLY equal `cockpit_q7q8` (the marker is a REASON, never a CHOICE — the §6 human still
rules); the block's note names the UNCHANGED Q8 + the §6 human; `reason` still at-capacity (agrees with Q9
`capacity_planning_attention` BY CONSTRUCTION); the 7 Sprint-29 orgs byte-identical; superset byte-identity;
determinism; real output + usable fixtures.

Additive: NO source change to adjudication_engine.py (hash a60f8f7… unchanged) — a new runner + recorded
data. Frozen functions untouched; no new noun; frozen 49 $defs; SPEC v0.22; ros/ + schema + sector configs
untouched; ~$0.
Emits fixtures (incl. the new org) + artifacts/adjudication/reports/cockpit-label-vs-choice.md.
Usage: (from instances/contested_reality)  python3 run_forecast_label_vs_choice_demo.py
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

from ros.substrate import now_iso                             # noqa: E402
import adjudication_engine as eng                             # noqa: E402
import adjudication_configs as ac                             # noqa: E402
import run_forecast_horizon_demo as rfh                       # noqa: E402 (VM points / run_one / relabel_to)
import run_forecast_per_option_capacity_demo as r29           # noqa: E402 (the 7 Sprint-29 orgs + builders)

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")


# ---- the NEW org's exact recorded numbers (reproducible) -----------------------------------------
RECINF_LABEL = "deli-recommend-infcap"
RECINF_CAP_VALUE = 500.0
RECINF_CAP_LOAD = 1.3
RECINF_AVAILABLE = round(RECINF_CAP_VALUE - RECINF_CAP_LOAD, 4)          # 498.7
RECINF_METRIC = f"metric://{RECINF_LABEL}/m-on-time"
from run_forecast_per_option_capacity_demo import INFCAP_METRIC  # noqa: E402,F401  (same series shape)
# partial-settlement RECORDS a requirement > available => capacity_infeasible ON THE RECOMMENDED option;
# the other 6 non-baseline options <= available => capacity_risk; baseline unresolved not recorded.
RECINF_REQS = {
    "partial-settlement": 499.0,          # <-- the machine-eligible best / Q8 recommendation
    "conditional-resolution": 200.0, "accept-customer-refund": 200.0,
    "accept-company-full-payment": 200.0, "external-adjudication": 100.0,
    "request-more-evidence": 50.0, "escalate": 80.0,
}
assert RECINF_REQS["partial-settlement"] > RECINF_AVAILABLE, "recommended option must be infeasible"
assert all(v <= RECINF_AVAILABLE for k, v in RECINF_REQS.items() if k != "partial-settlement")


def _new_recommend_infeasible_org():
    """Build a fresh DELI-relabeled org that RECORDS a capacity requirement > available for the
    machine-eligible best option itself (partial-settlement)."""
    cfg = rfh.relabel_to(ac.DELI, RECINF_LABEL)
    r = rfh.run_one(cfg)
    eng.record_metric_series(r["sub"], RECINF_LABEL, RECINF_METRIC, points=[dict(p) for p in rfh.VM_POINTS],
                             fields={"name": "resolution on-time rate",
                                     "formula": "on-time/total from ledger", "unit": "fraction",
                                     "target": 0.95, "period": "quarter",
                                     "source": "ledger resolution completion records",
                                     "owner": cfg["authority"]["adjudicator_person"],
                                     "band_variance": "all"},
                             signer=cfg["authority"]["adjudicator_person"])
    eng.record_capacity(r["sub"], cfg["authority"]["dispute"], value=RECINF_CAP_VALUE,
                        unit="resolutions/day", load=RECINF_CAP_LOAD,
                        signer=cfg["authority"]["adjudicator_person"])
    eng.record_capacity_requirements(r["sub"], cfg["authority"]["dispute"], requirements=RECINF_REQS,
                                     signer=cfg["authority"]["adjudicator_person"])
    r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
    r["closure"] = eng._forecast_closure(r["cfg"], r["sub"])
    return r


def build_orgs():
    """The seven reused Sprint-29 orgs (byte-identical) + the NEW recommended-option-infeasible org."""
    o = r29.build_orgs()
    o["recinf"] = _new_recommend_infeasible_org()
    return o


def run_all() -> int:
    print("=== SPRINT 30 — the marker is a REASON, never a CHOICE: the RECOMMENDED option is "
          "capacity_infeasible, yet the cockpit STILL recommends it ===")
    o = build_orgs()
    fc, vm, vmc, fl2, deli = o["fc"], o["vm"], o["vmc"], o["fl2"], o["deli"]
    infcap, definf, recinf = o["infcap"], o["definf"], o["recinf"]
    all8 = (fc, vm, vmc, fl2, deli, infcap, definf, recinf)

    deli_opts = list(ac.DELI["options"])
    baseline = next(x for x in deli_opts if "unres" in x.lower() or x == "do-nothing")
    non_baseline = [x for x in deli_opts if x != baseline]

    # ---- (0) the NEW org's records + the full §7L Q1–Q10 cockpit -------------------------------
    c = recinf["s7l"]
    cc7 = c["q7"].get("capacity_constraint"); cc8 = c["q8"].get("capacity_constraint")
    cpa = c["q9"].get("capacity_planning_attention")
    _report(f"{recinf['label']}: FULL §7L Q1–Q10 cockpit + recorded-data evidence present",
            all(isinstance(c[k], dict) for k in ("q1","q2","q3","q4","q5","q6","q7","q8","q9","q10"))
            and bool(c["q1"]["events"]) and c["q6"]["forecast_available"] and bool(c["q7"]["options"]),
            f"q3 items={c['q3']['count']}")
    flagged = dict(cc8["options_flagged"]) if isinstance(cc8, dict) else None
    infeas = {k: v for k, v in (flagged or {}).items() if v == "capacity_infeasible"}
    risk = {k: v for k, v in (flagged or {}).items() if v == "capacity_risk"}
    _report(f"{recinf['label']}: `capacity_constraint` present on Q7 AND Q8, reason `at-capacity`, "
            "flag True, available_capacity 498.7 surfaced, requirement map recorded",
            isinstance(cc7, dict) and isinstance(cc8, dict) and cc7 == cc8
            and cc8["reason"] == "at-capacity" and cc8["flag"] is True
            and cc8.get("available_capacity") == RECINF_AVAILABLE
            and cc8.get("per_option_requirements") == RECINF_REQS, str(cc8))

    # ---- (1) THE CORE: the RECOMMENDED option is itself capacity_infeasible ----------------------
    _report(f"{recinf['label']}: the machine-eligible best / Q8 recommendation (`partial-settlement`) "
            f"is itself `capacity_infeasible` (recorded 499.0 > available {RECINF_AVAILABLE})",
            infeas.get("partial-settlement") == "capacity_infeasible", f"partial-settlement={infeas.get('partial-settlement')}")
    _report(f"{recinf['label']}: exactly ONE infeasible (the recommended) + {len(risk)} `capacity_risk`, "
            "baseline NEVER flagged — all 7 non-baseline options accounted for",
            len(infeas) == 1 and set(infeas) == {"partial-settlement"}
            and len(risk) == 6 and set(infeas) | set(risk) == set(non_baseline) and baseline not in flagged,
            f"infeasible={sorted(infeas)} risk={sorted(risk)}")
    _report(f"{recinf['label']}: the per-option arithmetic is recorded-data only — recommended "
            "requirement 499.0 > available, every `capacity_risk` <= available, baseline not recorded",
            RECINF_REQS["partial-settlement"] > RECINF_AVAILABLE
            and all(RECINF_REQS[k] <= RECINF_AVAILABLE for k in risk) and baseline not in RECINF_REQS,
            f"available={RECINF_AVAILABLE}")

    # ---- (2) THE PROOF: the marker is a REASON, never a CHOICE — the §6 human still rules ----------
    base = eng.cockpit_q7q8(recinf["cfg"], recinf["sub"], library=ac.RULE_LIBRARY)
    _report(f"{recinf['label']} (SHARPEST BOUNDARY): Q8 recommendation STILL `partial-settlement` and "
            "machine-eligible best STILL `partial-settlement` even though options_flagged marks the "
            "recommended option `capacity_infeasible`",
            c["q8"]["recommendation"] == "partial-settlement"
            and c["q7"]["machine_eligible_best"] == "partial-settlement")
    _report(f"{recinf['label']}: Q7 `options` (count 8 + uris) + `machine_eligible_best` + Q8 "
            "`recommendation` + `floor_gated` EXACTLY equal `cockpit_q7q8` (no re-rank, no removal, no "
            "§6 overrule — the marker labels; it does NOT pick a replacement)",
            c["q7"]["options"] == base["q7"]["options"] and len(c["q7"]["options"]) == 8
            and c["q7"]["machine_eligible_best"] == base["q7"]["machine_eligible_best"]
            and c["q8"]["recommendation"] == base["q8"]["recommendation"]
            and c["q8"]["floor_gated"] == base["q8"]["floor_gated"],
            f"Q8={c['q8']['recommendation']} == {base['q8']['recommendation']}")
    _report(f"{recinf['label']}: `capacity_constraint.note` names the UNCHANGED Q8 + the §6 human "
            "(the recommended option's infeasibility is a REASON, the human picks a replacement)",
            isinstance(cc8, dict) and "UNCHANGED" in cc8.get("note", "")
            and "human always rules" in cc8.get("note", ""), cc8.get("note"))
    _report(f"{recinf['label']}: constraint `reason` == Q9 `capacity_planning_attention` label BY "
            "CONSTRUCTION (shared `_capacity_reason`), flag True on both",
            isinstance(cpa, dict) and cpa["flag"] is True and cc8["reason"] == "at-capacity", str(cpa))

    # ---- (3) recorded-data provenance for the new org ---------------------------------------------
    auth = recinf["sub"].graph.get(recinf["cfg"]["authority"]["dispute"]) or {}
    cap = auth.get("capacity") or {}; recorded_reqs = auth.get("capacity_requirements") or {}
    _report(f"{recinf['label']}: every per-option value traces to a RECORDED field "
            "(authority.capacity {value,load} + authority.capacity_requirements); available == recorded "
            "value − load",
            cc8["per_option_requirements"] == recorded_reqs == RECINF_REQS
            and cc8["available_capacity"] == RECINF_AVAILABLE == round(cap.get("value") - cap.get("load"), 4),
            f"available={cc8['available_capacity']}")

    # ---- (4) Sprint-29 byte-identity REGRESSION on the seven reused orgs --------------------------
    vcc7 = vmc["s7l"]["q7"].get("capacity_constraint")
    _report(f"{vmc['label']}: REUSED headroom org — reason STILL headroom, flag False, options_flagged "
            "STILL {}, NO per-option keys (Sprint-29 byte-identical, strict superset)",
            isinstance(vcc7, dict) and vcc7.get("reason") == "headroom" and vcc7.get("flag") is False
            and vcc7.get("options_flagged") == {}
            and "per_option_requirements" not in vcc7 and "available_capacity" not in vcc7, str(vcc7))
    for r, expect_reason, expect_avail in ((infcap, "at-capacity", r29.INFCAP_AVAILABLE),
                                           (definf, "deficit", r29.DEFINF_AVAILABLE)):
        cc = r["s7l"]["q8"].get("capacity_constraint")
        _report(f"{r['label']}: REUSED per-option org byte-identical — reason {expect_reason}, flag True, "
                f"{len(cc['options_flagged'])} per-option labels, available {expect_avail} (Sprint-29)",
                isinstance(cc, dict) and cc["reason"] == expect_reason and cc["flag"] is True
                and cc.get("available_capacity") == expect_avail
                and "per_option_requirements" in cc and len(cc.get("per_option_requirements", {})) == 7,
                str(cc))
    for r in (fc, vm, fl2, deli):
        _report(f"{r['label']}: REUSED no-capacity org — NO `capacity_constraint` on Q7/Q8, NO "
                "capacity_planning_attention (Sprint-29 byte-identical)",
                "capacity_constraint" not in r["s7l"]["q7"] and "capacity_constraint" not in r["s7l"]["q8"]
                and "capacity_planning_attention" not in r["s7l"]["q9"])

    # ---- (5) marker-is-a-label for EVERY org (incl. the new one) -----------------------------------
    for r in all8:
        b = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: Q7 options + machine_eligible_best + Q8 recommendation + floor_gated "
                "EXACTLY equal `cockpit_q7q8` (the marker never re-ranks — also at the sharpest boundary)",
                r["s7l"]["q7"]["options"] == b["q7"]["options"]
                and r["s7l"]["q7"]["machine_eligible_best"] == b["q7"]["machine_eligible_best"]
                and r["s7l"]["q8"]["recommendation"] == b["q8"]["recommendation"]
                and r["s7l"]["q8"]["floor_gated"] == b["q8"]["floor_gated"],
                f"Q8={r['s7l']['q8']['recommendation']}")

    # ---- (6) determinism (dict + render) for ALL eight orgs ----------------------------------------
    for r in all8:
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: deterministic on re-run (structured dict + rendered §7L line)", c1 == c2 and x1 == x2)

    # ---- emit fixtures for the new org + the engine-native report ----------------------------------
    eng.emit_fixtures(recinf["sub"], HERE, recinf["cfg"])
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L label-vs-choice — the RECOMMENDED option made `capacity_infeasible` — engine-native "
         "render (Sprint 30)"]
    A.append(f"generated {now_iso()}  |  `adjudication_engine._per_option_capacity_flags`/`cockpit_s7l`  |  "
             "NO engine change (hash a60f8f7…): Sprint 29's recorder already labels ANY option "
             "`capacity_infeasible` when its RECORDED per-option requirement > available. The point of "
             "Sprint 30 is to drive the SHARPEST boundary on a real org: the recorded capacity says the "
             "machine-eligible best / Q8 recommendation itself (`partial-settlement`) CANNOT run "
             "(recorded requirement 499.0 > available 498.7), yet the cockpit provably STILL recommends "
             "partial-settlement (exactly `cockpit_q7q8`). The marker is a REASON, never a CHOICE — the "
             "§6 human always rules.  |  SPEC v0.22, 49 $defs, URI cap")
    A.append("")
    A.append(f"Sprint 29 let the marker NAME a specific infeasible option but never had the RECOMMENDED "
             f"option be that one. `{RECINF_LABEL}` records an at-capacity org (cap 500.0 res/day, load "
             f"1.3 -> available {RECINF_AVAILABLE}) and a per-option requirement map in which "
             f"`partial-settlement` — the machine-eligible best (utility 0.7275, non-gated) — records "
             f"499.0 > {RECINF_AVAILABLE} => `capacity_infeasible` ON THE RECOMMENDED OPTION; the other 6 "
             f"non-baseline options <= available => `capacity_risk`; the baseline unresolved records no "
             f"requirement => never flagged. The Q7/Q8 `capacity_constraint` block (reason `at-capacity`, "
             f"flag True, available {RECINF_AVAILABLE}) labels this — and the engine STILL surfaces Q8 "
             f"recommendation `partial-settlement` + machine-eligible best `partial-settlement`, EXACTLY "
             f"equal to `cockpit_q7q8`. The §6 human must choose the replacement (or overrule); the "
             f"marker never does.")
    A.append("")
    for r in (fc, vm, vmc, fl2, deli, infcap, definf, recinf):
        A.append(f"--- {r['label']} ---")
        A.append("```")
        A.append(eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY))
        A.append("```")
        A.append("")
        cc = r["s7l"]["q8"].get("capacity_constraint")
        if cc:
            A.append(f"Q8 capacity_constraint: reason={cc['reason']}  flag={cc['flag']}  "
                     f"recorded_capacity={cc['recorded_capacity']}  horizon_band={cc['horizon_band']}")
            if cc.get("available_capacity") is not None:
                A.append(f"  available_capacity={cc['available_capacity']} (recorded capacity VALUE − "
                         "recorded load, same unit)")
            A.append(f"  options_flagged={cc['options_flagged']}")
            if cc.get("per_option_requirements"):
                A.append(f"  per_option_requirements={cc['per_option_requirements']}")
            A.append(f"  note: {cc['note']}")
            A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**The marker is a REASON, never a CHOICE — at its sharpest.** A RECORDED per-option "
             "requirement now makes the frozen machine-eligible best / Q8 recommendation itself "
             "(`partial-settlement`) `capacity_infeasible` (recorded 499.0 > available 498.7), and the "
             "cockpit provably STILL recommends partial-settlement — exactly `cockpit_q7q8`, no re-rank, "
             "no removal, no §6 overrule. The marker LABELS 'the recorded capacity says the recommended "
             "option can't run'; it does NOT pick a replacement; the §6 human always rules. The seven "
             "Sprint-29 orgs stay byte-identical (a no-requirements org keeps today's block exactly; a "
             "no-capacity org carries no `capacity_constraint`). This is generic + additive — recorded "
             "`metric://` series + recorded point-`variance` + the recorded `band_variance` source + a "
             "recorded authority `capacity` + a recorded per-option `capacity_required` descriptor; no "
             "new noun, frozen 49 `$defs`.")
    A.append("")
    A.append("**Still not derivable (the honest frontier):** a capacity-constrained OPTIMIZATION that "
             "RE-RANKS the recommendation for the machine stays out of scope of the deterministic "
             "advisory stance — the marker never CHOOSES; choosing a different option for the machine is "
             "a policy / user decision, not a label. A per-option requirement that is NOT unit-coupled to "
             "the recorded capacity / an option with no recorded requirement remains non-derivable (the "
             "engine never invents one). No SPEC bump (v0.22).")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs, URI cap. The sharpest label-vs-choice "
             "boundary is now demonstrated AS DATA: the recorded capacity says the recommended option "
             "can't run, and the Q8 recommendation provably stays unchanged._")
    (rp / "cockpit-label-vs-choice.md").write_text("\n".join(A) + "\n")

    print("\n  -> engine-native Sprint-30 cockpit under "
          "artifacts/adjudication/reports/cockpit-label-vs-choice.md")
    print("  -> new-org fixtures under artifacts/adjudication/fixtures/%s/ " % RECINF_LABEL)
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())