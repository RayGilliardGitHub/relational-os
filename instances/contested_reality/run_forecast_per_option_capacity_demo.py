"""run_forecast_per_option_capacity_demo.py — SPRINT 29: per-option capacity_infeasible.

Sprint 28 proved the Q7/Q8 `capacity_constraint` marker at its LIMIT — at-capacity (`deli-atcap`)
and deficit (`deli-deficit`) — but its own finding (`sprints/sprint-28/notes/findings.md`) disclosed
the next honest frontier: **the marker can label the whole `capacity_risk`, but `capacity_infeasible`
is STRUCTURALLY UNREACHABLE because NO PER-OPTION capacity requirement is ever recorded** — the
engine compares the org-level recorded `load` and the horizon band's worst-side to the recorded
capacity VALUE, so it can flag a whole option set as risky but can never say a SPECIFIC option is
infeasible under capacity, and never price it per option.

Sprint 29 closes that bounded slice additively — the recorded capacity becomes PER-OPTION:
1. a REPLAYABLE recorder `record_capacity_requirements(sub, authority_uri, requirements, signer)`
   appends an additive `capacity_requirements` map ({option: nonneg amount}) ON THE SAME authority://
   object that carries the additive `capacity` — unit-coupled by construction (the authority holds
   the {value, unit, load} capacity AND the per-option requirements, so `available = capacity.value
   - capacity.load` derives in the SAME recorded unit);
2. the Q7/Q8 `capacity_constraint` block, when requirements are recorded, labels a SPECIFIC option
   `capacity_infeasible` iff its RECORDED requirement > available; otherwise `capacity_risk` as today.
   The baseline (do-nothing/UNRESOLVED) is NEVER flagged; `reason`/`flag` still come from the frozen
   org-level `_capacity_reason` rule; and the block still NEVER removes an option, NEVER re-ranks,
   NEVER overrules the §6 human — the Q8 recommendation stays EXACTLY the `rank` output even when a
   SPECIFIC option is infeasible.

Per-option proof (exit 0 = ALL PASS): reuse the Sprint-28 five byte-identical orgs (fc/vm/vmc/fl2/
deli) PLUS two NEW orgs that RECORD per-option requirements:
  deli-infcap       at-capacity (cap 500.0 res/day, load 1.3 -> available 498.7): heavy options (3)
                    record 499.0 > 498.7 -> `capacity_infeasible`; lighter options (4) <= available
                    -> `capacity_risk`; baseline unresolved NOT recorded -> never flagged.
  deli-deficit-inf  deficit (lower-is-better latency, cap 30.0, load 0.9 -> available 29.1): heavy
                    options (3) record 30.0 > 29.1 -> `capacity_infeasible`; lighter (4) <= available
                    -> `capacity_risk`; baseline never flagged.
And asserts: the per-option distinction (some infeasible, some risk, baseline absent) derived from
RECORDED numbers only; `reason` still at-capacity/deficit from the org-level rule (agrees with each
org's Q9 capacity_planning_attention BY CONSTRUCTION); the marker is STILL a LABEL — q7 options +
machine_eligible_best + q8 recommendation EQUAL to `cockpit_q7q8` for EVERY org (even when SOME
option is infeasible); Sprint-28 byte-identity on the 5 reused orgs; superset byte-identity;
determinism; real output + usable fixtures.

Additive: the ONLY engine file touched is adjudication_engine.py (new recorder + `_per_option_capacity_flags`
helper + the additive extension of the existing Q7/Q8 capacity_constraint block). Frozen functions
untouched; no new noun; frozen 49 $defs; SPEC v0.22; ros/ + schema + sector configs untouched; ~$0.
Emits fixtures (incl. the 2 new orgs) + artifacts/adjudication/reports/cockpit-forecast-per-option-capacity.md.
Usage: (from instances/contested_reality)  python3 run_forecast_per_option_capacity_demo.py
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
import run_forecast_horizon2_demo as r26   # noqa: E402  (5 reused orgs' builders)
import run_forecast_horizon_demo as rfh    # noqa: E402  (VM points / constants)
import run_forecast_variance_demo as rfv   # noqa: E402  (CO points / latency series)

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")


# ---- the two NEW orgs' exact recorded numbers (reproducible) -----------------------------------
INFCAP_LABEL = "deli-infcap"
INFCAP_CAP_VALUE = 500.0
INFCAP_CAP_LOAD = 1.3
INFCAP_AVAILABLE = round(INFCAP_CAP_VALUE - INFCAP_CAP_LOAD, 4)          # 498.7
INFCAP_METRIC = f"metric://{INFCAP_LABEL}/m-on-time"
# heavy options record a requirement > available -> capacity_infeasible; lighter -> capacity_risk
INFCAP_REQS = {
    "accept-customer-refund": 499.0, "accept-company-full-payment": 499.0,
    "external-adjudication": 499.0,          # 3 heavy -> capacity_infeasible via rule
    "partial-settlement": 200.0, "conditional-resolution": 200.0,
    "request-more-evidence": 50.0, "escalate": 100.0,   # 4 lighter -> capacity_risk
}
assert all(v > INFCAP_AVAILABLE for v in
           (INFCAP_REQS["accept-customer-refund"], INFCAP_REQS["accept-company-full-payment"],
            INFCAP_REQS["external-adjudication"]))
assert all(v <= INFCAP_AVAILABLE for k, v in INFCAP_REQS.items() if k not in
           ("accept-customer-refund", "accept-company-full-payment", "external-adjudication"))

DEFINF_LABEL = "deli-deficit-inf"
DEFINF_CAP_VALUE = 30.0
DEFINF_CAP_LOAD = 0.9
DEFINF_AVAILABLE = round(DEFINF_CAP_VALUE - DEFINF_CAP_LOAD, 4)          # 29.1
DEFINF_METRIC = f"metric://{DEFINF_LABEL}/m-latency"
DEFINF_REQS = {
    "external-adjudication": 30.0, "accept-company-full-payment": 30.0,
    "accept-customer-refund": 30.0,          # 3 heavy -> capacity_infeasible
    "partial-settlement": 20.0, "conditional-resolution": 20.0,
    "request-more-evidence": 10.0, "escalate": 15.0,   # 4 lighter -> capacity_risk
}
assert all(v > DEFINF_AVAILABLE for v in
           (DEFINF_REQS["external-adjudication"], DEFINF_REQS["accept-company-full-payment"],
            DEFINF_REQS["accept-customer-refund"]))
assert all(v <= DEFINF_AVAILABLE for k, v in DEFINF_REQS.items() if k not in
           ("external-adjudication", "accept-company-full-payment", "accept-customer-refund"))


def _new_per_option_org(label, metric_uri, points, fields, cap_value, cap_unit, cap_load, reqs):
    """Build a fresh DELI-relabeled org that RECORDS a metric series + an authority capacity AND the
    per-option capacity requirements (the new Sprint-29 recorded descriptor)."""
    cfg = rfh.relabel_to(ac.DELI, label)
    r = rfh.run_one(cfg)
    eng.record_metric_series(r["sub"], label, metric_uri, points=points, fields=fields,
                             signer=cfg["authority"]["adjudicator_person"])
    eng.record_capacity(r["sub"], cfg["authority"]["dispute"], value=cap_value,
                        unit=cap_unit, load=cap_load, signer=cfg["authority"]["adjudicator_person"])
    eng.record_capacity_requirements(r["sub"], cfg["authority"]["dispute"], requirements=reqs,
                                     signer=cfg["authority"]["adjudicator_person"])
    r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
    r["closure"] = eng._forecast_closure(r["cfg"], r["sub"])
    return r


def build_orgs():
    """The five reused Sprint-28 orgs + the two NEW per-option-requirement orgs."""
    o = r26.build_orgs()
    infcap = _new_per_option_org(
        INFCAP_LABEL, INFCAP_METRIC, [dict(p) for p in rfh.VM_POINTS],
        {"name": "resolution on-time rate", "formula": "on-time/total from ledger",
         "unit": "fraction", "target": 0.95, "period": "quarter",
         "source": "ledger resolution completion records", "owner": ac.DELI["authority"]["adjudicator_person"],
         "band_variance": "all"},
        INFCAP_CAP_VALUE, "resolutions/day", INFCAP_CAP_LOAD, INFCAP_REQS)
    definf = _new_per_option_org(
        DEFINF_LABEL, DEFINF_METRIC, [dict(p) for p in rfv.CO_POINTS],
        {"name": "mean resolution latency", "formula": "mean elapsed time to a resolution from ledger",
         "unit": "ms", "target": 16, "period": "quarter", "source": "ledger resolution completion records",
         "direction": "lower-is-better", "band_variance": "all",
         "owner": ac.DELI["authority"]["adjudicator_person"]},
        DEFINF_CAP_VALUE, "resolutions/day", DEFINF_CAP_LOAD, DEFINF_REQS)
    return {**o, "infcap": infcap, "definf": definf}


def run_all() -> int:
    print("=== SPRINT 29 — per-option capacity_infeasible from a RECORDED per-option requirement ===\n")
    o = build_orgs()
    fc, vm, vmc, fl2, deli = o["fc"], o["vm"], o["vmc"], o["fl2"], o["deli"]
    infcap, definf = o["infcap"], o["definf"]
    all7 = (fc, vm, vmc, fl2, deli, infcap, definf)

    # deli options: 8 total, baseline = "unresolved", 7 non-baseline capacity-consuming options
    deli_opts = list(ac.DELI["options"])
    baseline = next(x for x in deli_opts if "unres" in x.lower() or x == "do-nothing")
    non_baseline = [x for x in deli_opts if x != baseline]
    _report("baseline is the do-nothing/UNRESOLVED option (never flagged), 8 options, 7 non-baseline",
            baseline == "unresolved" and len(deli_opts) == 8 and len(non_baseline) == 7,
            f"baseline={baseline} n={len(deli_opts)}")

    # ---- (a) ALL orgs keep the full §7L Q1–Q10 cockpit -----------------------------------------
    for r in all7:
        c = r["s7l"]
        full = all(isinstance(c[k], dict) for k in ("q1","q2","q3","q4","q5","q6","q7","q8","q9","q10"))
        ev = all(bool(c[k].get("evidence")) for k in ("q1","q2","q3","q4","q5","q6","q9","q10"))
        _report(f"{r['label']}: FULL §7L Q1–Q10 cockpit + data evidence present",
                full and ev and bool(c["q1"]["events"]) and bool(c["q7"]["options"])
                and bool(c["q8"]["authority"]) and bool(c["q10"]["determination"]),
                f"q6.avail={c['q6']['forecast_available']} q3 items={c['q3']['count']}")

    # ---- (b) Sprint-28 byte-identity on the five reused orgs -----------------------------------
    vcc7 = vmc["s7l"]["q7"].get("capacity_constraint")
    vcc8 = vmc["s7l"]["q8"].get("capacity_constraint")
    _report(f"{vmc['label']}: REUSED headroom org — `capacity_constraint` reason STILL headroom, flag "
            "False, options_flagged STILL {} — and NO per-option keys (Sprint-28 byte-identical)",
            isinstance(vcc7, dict) and vcc7 == vcc8 and vcc7["reason"] == "headroom"
            and vcc7["flag"] is False and vcc7["options_flagged"] == {}
            and "per_option_requirements" not in vcc8 and "available_capacity" not in vcc8,
            str(vcc8))
    cpa = vmc["s7l"]["q9"].get("capacity_planning_attention")
    _report(f"{vmc['label']}: Q9 capacity_planning_attention UNCHANGED (derived headroom, flag False)",
            isinstance(cpa, dict) and cpa["flag"] is False and "derived headroom" in cpa["why"], str(cpa))
    fc_att = [i for i in fc["s7l"]["q3"]["prioritized"] if i.get("tag") == "forecast"]
    _report(f"{fc['label']}: Q3 `why` STILL the Sprint-26/27/28 horizon-suffix string (byte-identity)",
            len(fc_att) == 1
            and fc_att[0]["why"] == (r26.rfv.FC_SINGLE_WHY
                                     + (" — recorded band 0.71…0.89 (± σ 0.09); worst side "
                                        "0.71 below target 0.95")
                                     + r26.R26_HORIZON.format(lo=0.71, hi=0.93, n=3)),
            fc_att[0]["why"])
    for r in (fc, vm, fl2, deli):
        _report(f"{r['label']}: NO `capacity_constraint` on Q7 or Q8 (no recorded capacity / no band "
                "— Sprint-28 byte-identical + no per-option anything)",
                "capacity_constraint" not in r["s7l"]["q7"] and "capacity_constraint" not in r["s7l"]["q8"]
                and "capacity_planning_attention" not in r["s7l"]["q9"])

    # ---- (c) per-option infeasibility derived from RECORDED numbers (the Sprint-29 core) -------------
    for r, expect_reason, reqs, available in (
            (infcap, "at-capacity", INFCAP_REQS, INFCAP_AVAILABLE),
            (definf, "deficit", DEFINF_REQS, DEFINF_AVAILABLE)):
        cc7 = r["s7l"]["q7"].get("capacity_constraint")
        cc8 = r["s7l"]["q8"].get("capacity_constraint")
        cpa_r = r["s7l"]["q9"].get("capacity_planning_attention")
        flagged = dict(cc8["options_flagged"]) if isinstance(cc8, dict) else None
        _report(f"{r['label']}: per-option block present on BOTH Q7 and Q8, reason = {expect_reason}, "
                "flag True (org-level rule unchanged), requirement map + available capacity surfaced",
                isinstance(cc7, dict) and isinstance(cc8, dict) and cc7 == cc8
                and cc8["reason"] == expect_reason and cc8["flag"] is True
                and cc8.get("per_option_requirements") == reqs
                and cc8.get("available_capacity") == available,
                str(cc8))
        infeas = {k: v for k, v in (flagged or {}).items() if v == "capacity_infeasible"}
        risk = {k: v for k, v in (flagged or {}).items() if v == "capacity_risk"}
        _report(f"{r['label']}: `options_flagged` DISTINGUISHES {len(infeas)} `capacity_infeasible` "
                f"(reported requirement > available {available}) from {len(risk)} `capacity_risk`, "
                "baseline NEVER flagged",
                flagged is not None
                and len(infeas) == 3 and len(risk) == 4
                and set(infeas) | set(risk) == set(non_baseline)
                and set(infeas) == {k for k, v in reqs.items() if v > available}
                and set(risk) == {k for k, v in reqs.items() if v <= available}
                and baseline not in flagged,
                f"infeasible={sorted(infeas)} risk={sorted(risk)}")
        _report(f"{r['label']}: the per-option formula is recorded-data only — every `capacity_infeasible` "
                "option's RECORDED requirement > available, every `capacity_risk` option's <= available, "
                "baseline (no recorded requirement) never flagged",
                all(reqs[k] > available for k in infeas)
                and all(reqs[k] <= available for k in risk)
                and baseline not in reqs,
                f"available={available} reqs={reqs}")
        _report(f"{r['label']}: constraint reason AGREES with the Q9 capacity label BY CONSTRUCTION "
                "(shared `_capacity_reason`) — flag True on both, per-option does not touch the org reason",
                isinstance(cpa_r, dict) and cpa_r["flag"] is True and cc8["reason"] == expect_reason,
                str(cpa_r))
        _report(f"{r['label']}: block is a LABEL — never a removal, never a re-rank, no §6 overrule "
                "(note names the UNCHANGED Q8 + §6 human)",
                isinstance(cc8, dict) and "UNCHANGED" in cc8.get("note", "")
                and "human always rules" in cc8.get("note", ""))

    # ---- clarity: Q8 recommendation / machine-eligible best are NOT touched by infeasibility ------
    for r, expect_reason in ((infcap, "at-capacity"), (definf, "deficit")):
        cc8 = r["s7l"]["q8"]["capacity_constraint"]
        _report(f"{r['label']}: Q8 recommendation STILL the frozen `rank` output (= partial-settlement) "
                "even though SOME option is `capacity_infeasible` (the marker labels; the §6 human rules)",
                r["s7l"]["q8"]["recommendation"] == "partial-settlement"
                and r["s7l"]["q7"]["machine_eligible_best"] == "partial-settlement"
                and "capacity_infeasible" in cc8["options_flagged"].values(),
                f"cc={cc8['reason']}")

    # ---- (d) the marker is STILL a LABEL: q7/q8 EXACTLY equal to cockpit_q7q8 for EVERY org ----
    for r in all7:
        base = eng.cockpit_q7q8(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: Q7 `options` (count+uris) + `machine_eligible_best` + Q8 "
                "`recommendation` + `floor_gated` EXACTLY equal to `cockpit_q7q8` (no §6 overrule, no "
                "re-rank, no option-removal — ALSO when a SPECIFIC option is infeasible)",
                r["s7l"]["q7"]["options"] == base["q7"]["options"]
                and len(r["s7l"]["q7"]["options"]) == 8
                and r["s7l"]["q7"]["machine_eligible_best"] == base["q7"]["machine_eligible_best"]
                and r["s7l"]["q8"]["recommendation"] == base["q8"]["recommendation"]
                and r["s7l"]["q8"]["floor_gated"] == base["q8"]["floor_gated"],
                f"Q8={r['s7l']['q8']['recommendation']} == {base['q8']['recommendation']}")

    # ---- (e) superset byte-identity + recorded-data provenance ----------------------------------
    for r in (vmc, infcap, definf):
        _report(f"{r['label']}: Q7/Q8 pre-existing keys intact (options/baseline/machine_eligible_best/"
                "recommendation/authority/floor_gated + do_nothing_expected_impact)",
                all(k in r["s7l"]["q7"] for k in ("options","baseline","machine_eligible_best"))
                and all(k in r["s7l"]["q8"] for k in ("recommendation","authority","floor_gated"))
                and "do_nothing_expected_impact" in r["s7l"]["q8"])
    for r, reqs, available in ((infcap, INFCAP_REQS, INFCAP_AVAILABLE),
                               (definf, DEFINF_REQS, DEFINF_AVAILABLE)):
        cc = r["s7l"]["q8"]["capacity_constraint"]
        auth = r["sub"].graph.get(r["cfg"]["authority"]["dispute"]) or {}
        cap = auth.get("capacity") or {}
        recorded_reqs = auth.get("capacity_requirements") or {}
        _report(f"{r['label']}: every per-option value traces to a RECORDED field (authority.capacity "
                "{value,load} + authority.capacity_requirements) — available == recorded value − load",
                cc["per_option_requirements"] == recorded_reqs == reqs
                and cc["available_capacity"] == available
                and cc["recorded_capacity"] == ("%s %s (load %s)" % (cap.get("value"), cap.get("unit", ""),
                                                                     cap.get("load", "—")))
                and cc["horizon_band"] == r["closure"]["band_horizon"],
                f"available={cc['available_capacity']} reqs_len={len(recorded_reqs)}")

    # ---- (f) determinism (dict + render) on ALL orgs ------------------------------------------------
    for r in all7:
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: deterministic on re-run (structured dict + rendered §7L line)",
                c1 == c2 and x1 == x2)

    # ---- emit fixtures for the recorded/new orgs + the engine-native report -------------------------
    for r in (fc, vm, vmc, fl2, infcap, definf):
        eng.emit_fixtures(r["sub"], HERE, r["cfg"])
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L PER-OPTION capacity_infeasible — from a RECORDED per-option requirement — engine-native "
         "render (Sprint 29)"]
    A.append(f"generated {now_iso()}  |  `adjudication_engine._per_option_capacity_flags`/"
             "`cockpit_s7l`  |  a NEW REPLAYABLE recorder `record_capacity_requirements` appends an "
             "additive `capacity_requirements` map on the SAME authority:// object that carries the "
             "recorded `capacity` {value, unit, load} — so AVAILABLE = recorded capacity VALUE − "
             "recorded load, unit-coupled by construction — and the Q7/Q8 `capacity_constraint` block "
             "now labels a SPECIFIC option `capacity_infeasible` iff its RECORDED requirement > "
             "available, else `capacity_risk` as today. Baseline (do-nothing/UNRESOLVED) never "
             "flagged; `reason`/`flag` still come from the frozen org-level `_capacity_reason`; no "
             "re-rank, no removal, no §6 overrule — the Q8 recommendation stays EXACTLY equal to "
             "`cockpit_q7q8` even when SOME option is infeasible.  |  SPEC v0.22, 49 $defs, URI cap")
    A.append("")
    A.append(f"Sprint 28 proved the marker at-headroom/at-capacity/deficit but left `capacity_infeasible` "
             "STRUCTURALLY UNREACHABLE (no per-option requirement was ever recorded). Sprint 29 makes "
             "the recorded capacity PER-OPTION. `deli-infcap` records an at-capacity org (cap 500.0 "
             f"res/day, load 1.3 -> available {INFCAP_AVAILABLE}); its three heavy options record 499.0 "
             f"> {INFCAP_AVAILABLE} -> `capacity_infeasible`, its four lighter options <= available -> "
             f"`capacity_risk`. `deli-deficit-inf` records a deficit org (lower-is-better latency, cap "
             f"30.0, load 0.9 -> available {DEFINF_AVAILABLE}); its three heavy options record 30.0 > "
             f"{DEFINF_AVAILABLE} -> `capacity_infeasible`, its four lighter -> `capacity_risk`. Both "
             "keep `reason` at-capacity / deficit from the org-level rule (agreeing with each org's Q9 "
             "`capacity_planning_attention` BY CONSTRUCTION). The marker is still a LABEL — a name on "
             "the trade-off, never a choice: no option removed, no re-rank, no overrule of the §6 "
             "human — the Q8 recommendation provably stays `partial-settlement`.")
    A.append("")
    for r in (fc, vm, vmc, fl2, deli, infcap, definf):
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
    A.append("**Sprint 28's frontier is closed: the Q7/Q8 `capacity_constraint` marker can now reach "
             "`capacity_infeasible` for a SPECIFIC option, from a RECORDED per-option requirement and "
             "recorded available number only.** A new REPLAYABLE recorder `record_capacity_requirements` "
             "appends the per-option requirement map on the SAME authority:// object as the recorded "
             "`capacity` — so AVAILABLE = recorded capacity VALUE − recorded load, unit-coupled by "
             "construction — and the block labels an option `capacity_infeasible` iff its recorded "
             "requirement > available, else `capacity_risk`. Proven on real orgs: `deli-infcap` "
             f"(at-capacity; heavy 499.0 > {INFCAP_AVAILABLE} -> infeasible) and `deli-deficit-inf` "
             f"(deficit; heavy 30.0 > {DEFINF_AVAILABLE} -> infeasible), each with some `capacity_risk` "
             "and the baseline never flagged. It is still a LABEL and only additive data: no option is "
             "removed, the frozen `rank`/`machine_eligible_best`/`cockpit_q7q8` are untouched, the §6 "
             "human always rules — the Q8 recommendation is provably UNCHANGED even when a SPECIFIC "
             "option is infeasible. Orgs that record NO per-option requirement keep the Sprint-28 block "
             "byte-identical (strict superset; no `per_option_requirements`/`available_capacity` key). "
             "**Still not derivable (the honest frontier):** a genuinely capacity-constrained "
             "OPTIMIZATION that RE-RANKS the recommendation for the machine stays out of scope of the "
             "deterministic advisory stance (the marker never CHOOSES), and a per-option requirement "
             "that is NOT unit-coupled to the capacity remains non-derivable (an org with no recorded "
             "capacity value/load, or an option with no recorded requirement, carries no infeasibility "
             "label — the engine never invents one).")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs, URI cap. A RECORDED per-option capacity "
             "requirement now lets the marker name a single infeasible option; it never re-ranks, never "
             "removes, never overrules the §6 human or the floor-gated recommendation._")
    (rp / "cockpit-forecast-per-option-capacity.md").write_text("\n".join(A) + "\n")

    print("\n  -> engine-native Sprint-29 cockpit under "
          "artifacts/adjudication/reports/cockpit-forecast-per-option-capacity.md")
    print("  -> recorded/new-org fixtures under artifacts/adjudication/fixtures/"
          f"{{{fc['label']},{vm['label']},{vmc['label']},{fl2['label']},{INFCAP_LABEL},{DEFINF_LABEL}}}/ "
          "(deli no-data org emits no fixtures)")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())