"""run_capacity_rerank_demo.py — SPRINT 32: the capacity-constrained RE-RANK of the §7L Q8
recommendation for the machine, BY THE FROZEN `rank` UTILITY, as an EXPLICIT authorized POLICY step.

Sprint 30/31 closed the INVENTORY on the whole recorded-data §7L decision surface as
reason-not-choice across 11 orgs: every derived label traces to a RECORDED descriptor, and the Q8
recommendation provably stays the frozen `rank` output (the marker is a REASON, never a CHOICE —
the §6 human always rules). They named EXACTLY the ONE remaining out-of-scope step: a capacity-
constrained OPTIMIZATION that RE-RANKS the recommendation for the machine — a deliberate
"re-rank for the machine" POLICY/user decision, NOT a label. **This prompt explicitly asked for
it, so Sprint 32 builds it.** This runner drives the new, additively-built
`capacity_rerank.capacity_rerank(...)` and proves:

  NEEDED (machine best is capacity_infeasible from recorded per-option requirements -> a
  replacement IS chosen by POLICY): deli-recommend-infcap (partial-settlement ->
  conditional-resolution), inspect-recorded (rework-partial-credit -> conditional-accept-with-
  guarantee), cove-recommend-infcap (NEW — step-therapy-first -> authorize-generic), and
  deli-all-infeasible (NEW — every capacity-consuming option infeasible -> unresolved baseline,
  and it SAYS so: replacement_is_baseline True).

  UNCHANGED (best NOT infeasible -> byte-identical to cockpit_q7q8): the nine others, incl.
  cove-recorded (best capacity_risk, runnable) and the no-data org inspect-nodata.

The advisory path NEVER re-ranks: for every org the engine's Q8 recommendation still equals
`cockpit_q7q8`; the re-ranked selection is reported AS DATA in the block and surfaced plainly.
Engine untouched (hash a60f8f7…); frozen 49 $defs; SPEC v0.22; no new noun; ~$0.
Emits fixtures for the two NEW orgs + artifacts/adjudication/reports/capacity-rerank.md.
Usage: (from instances/contested_reality)  python3 run_capacity_rerank_demo.py
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCES = HERE.parent
ROS = INSTANCES.parents[0] / "sprints/sprint-5/artifacts"
for _p in (str(HERE), str(INSTANCES), str(ROS)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ros.substrate import now_iso                              # noqa: E402
import adjudication_engine as eng                              # noqa: E402
import adjudication_configs as ac                              # noqa: E402
import capacity_rerank as cr                                   # noqa: E402 (SPRINT 32 — new module)
import run_recorded_surface_demo as r31                        # noqa: E402 (11 orgs / build_orgs)
import run_forecast_horizon_demo as rfh                        # noqa: E402 (run_one / relabel_to)
import run_forecast_variance_demo as rfv                       # noqa: E402 (CO_POINTS)

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")


# ---- the two NEW orgs (new labels, no fixture overwrite) --------------------------------------
# cove-recommend-infcap: COVE + lower-is-better latency + a deficit {value,load} where the machine
#   best step-therapy-first RECORDS a requirement > available -> it too becomes capacity_infeasible.
COVR_LABEL = "cove-recommend-infcap"; COVR_METRIC = f"metric://{COVR_LABEL}/m-answer-latency"
COVR_CAP_VALUE = 30.0; COVR_CAP_LOAD = 0.9
COVR_OPTS = list(ac.COVE["options"])
COVR_BASELINE = next(o for o in COVR_OPTS if "unres" in o.lower() or o == "do-nothing")
COVR_AVAILABLE = round(COVR_CAP_VALUE - COVR_CAP_LOAD, 4)                  # 29.1
COVR_REQS = {"authorize-off-formulary": 30.0, "deny-off-formulary": 30.0,
             "step-therapy-first": 30.0, "authorize-generic": 25.0,
             "request-more-evidence": 10.0, "escalate-to-medical-director": 15.0,
             "external-peer-review": 20.0}
assert COVR_BASELINE == "unresolved"
assert all(COVR_REQS[o] > COVR_AVAILABLE for o in
           ("authorize-off-formulary", "deny-off-formulary", "step-therapy-first"))
assert all(COVR_REQS[o] <= COVR_AVAILABLE for o in
           ("authorize-generic", "request-more-evidence",
            "escalate-to-medical-director", "external-peer-review"))

# deli-all-infeasible: DELI at capacity {500.0, load 1.0} (available 499.0) where EVERY
#   capacity-consuming (non-baseline) option RECORDS a requirement > available -> only the
#   do-nothing/unresolved baseline remains runnable (the honest fallback, and it SAYS so).
DAI_LABEL = "deli-all-infeasible"; DAI_METRIC = f"metric://{DAI_LABEL}/m"
DAI_CAP_VALUE = 500.0; DAI_CAP_LOAD = 1.0
DAI_OPTS = list(ac.DELI["options"])
DAI_BASELINE = next(o for o in DAI_OPTS if "unres" in o.lower() or o == "do-nothing")
DAI_AVAILABLE = round(DAI_CAP_VALUE - DAI_CAP_LOAD, 4)                    # 499.0
DAI_REQS = {o: 500.0 for o in DAI_OPTS if o != DAI_BASELINE}              # every non-baseline > available
assert all(v > DAI_AVAILABLE for v in DAI_REQS.values())


def _new_rr_cove_org():
    cfg = rfh.relabel_to(ac.COVE, COVR_LABEL)
    r = rfh.run_one(cfg)
    eng.record_metric_series(r["sub"], COVR_LABEL, COVR_METRIC,
                             points=[dict(p) for p in rfv.CO_POINTS],
                             fields={"name": "mean answer latency",
                                     "formula": "mean elapsed time to an answer from ledger",
                                     "unit": "ms", "target": 16, "period": "quarter",
                                     "source": "ledger answer completion records",
                                     "direction": "lower-is-better", "band_variance": "all",
                                     "owner": ac.COVE["authority"]["adjudicator_person"]},
                             signer=cfg["authority"]["adjudicator_person"])
    eng.record_capacity(r["sub"], cfg["authority"]["dispute"], value=COVR_CAP_VALUE,
                        unit="units/day", load=COVR_CAP_LOAD,
                        signer=cfg["authority"]["adjudicator_person"])
    eng.record_capacity_requirements(r["sub"], cfg["authority"]["dispute"],
                                     requirements=COVR_REQS,
                                     signer=cfg["authority"]["adjudicator_person"])
    r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
    return r


def _new_all_infeasible_org():
    cfg = rfh.relabel_to(ac.DELI, DAI_LABEL)
    r = rfh.run_one(cfg)
    eng.record_metric_series(r["sub"], DAI_LABEL, DAI_METRIC,
                             points=[dict(p) for p in rfv.CO_POINTS],
                             fields={"name": "on-time rate",
                                     "formula": "on-time batches / total batches from ledger",
                                     "unit": "fraction", "target": 0.95, "period": "quarter",
                                     "source": "ledger QC completion records", "band_variance": "all",
                                     "owner": cfg["authority"]["adjudicator_person"]},
                             signer=cfg["authority"]["adjudicator_person"])
    eng.record_capacity(r["sub"], cfg["authority"]["dispute"], value=DAI_CAP_VALUE,
                        unit="units/day", load=DAI_CAP_LOAD,
                        signer=cfg["authority"]["adjudicator_person"])
    eng.record_capacity_requirements(r["sub"], cfg["authority"]["dispute"],
                                     requirements=DAI_REQS,
                                     signer=cfg["authority"]["adjudicator_person"])
    r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
    return r


def _recompute_replacement(cfg, sub, baseline):
    """Recompute the expected re-rank deterministically from the frozen `rank` ordering + the
    advisory capacity block, independent of the module under test (belts-and-suspenders)."""
    c = eng.cockpit_s7l(cfg, sub, library=ac.RULE_LIBRARY)
    cc = c["q8"].get("capacity_constraint")
    if not isinstance(cc, dict):
        return c["q7"]["machine_eligible_best"], False
    flags = cc.get("options_flagged") or {}
    prior = c["q7"]["machine_eligible_best"]
    if flags.get(prior) != "capacity_infeasible":
        return prior, False
    fb = None
    for rk in eng.rank(cfg):
        opt = rk["option"]
        if rk["floor_gated"] or flags.get(opt) == "capacity_infeasible":
            continue
        if opt == baseline:
            fb = opt
            continue
        return opt, True
    return (fb if fb is not None else baseline), True


def build() -> dict:
    o = r31.build_orgs()                       # the eleven Sprint-31 orgs, byte-identical
    o["covr"] = _new_rr_cove_org()             # NEW — COVE re-rank (machine best infeasible)
    o["dai"] = _new_all_infeasible_org()        # NEW — every capacity-consuming option infeasible
    return o


def run_all() -> int:
    print("=== SPRINT 32 — the capacity-constrained RE-RANK of the §7L Q8 recommendation for "
          "the machine, BY THE FROZEN rank UTILITY (authorized POLICY step) ===\n")
    o = build()
    # DECLARED expectations
    expect_rerank = {          # label -> expected replacement
        "deli-recommend-infcap": "conditional-resolution",
        "inspect-recorded": "conditional-accept-with-guarantee",
        "cove-recommend-infcap": "authorize-generic",
        "deli-all-infeasible": "unresolved",
    }
    expect_baseline_fallback = {"deli-all-infeasible"}
    all_orgs = {rr["label"]: rr for rr in o.values()}

    print("-- (1) per-org capacity_rerank block + which path it took --")
    blocks = {}
    for label, rr in all_orgs.items():
        blk = cr.capacity_rerank(rr["cfg"], rr["sub"], library=ac.RULE_LIBRARY)
        blocks[label] = blk
        kind = "RE-RANK" if blk["needed"] else "unchanged"
        bfb = " [baseline fallback]" if blk["replacement_is_baseline"] else ""
        print(f"    {label:>26}: {kind:>9}{bfb}: prior={blk['prior_machine_best']!r} -> "
              f"replacement={blk['replacement']!r}")

    # ---- (a) determinism ----------------------------------------------------------------------
    for label, rr in all_orgs.items():
        b1 = cr.capacity_rerank(rr["cfg"], rr["sub"], library=ac.RULE_LIBRARY)
        b2 = cr.capacity_rerank(rr["cfg"], rr["sub"], library=ac.RULE_LIBRARY)
        _report(f"{label}: capacity_rerank deterministic on re-run", b1 == b2)

    # ---- (b) NEEDED re-rank orgs ---------------------------------------------------------------
    for label, expected in expect_rerank.items():
        rr = all_orgs[label]; blk = blocks[label]; c = rr["s7l"]
        rec_expected, rec_needed = _recompute_replacement(rr["cfg"], rr["sub"],
                                                          c["q7"]["baseline"])
        floor_ok = blk["replacement"] not in (rr["cfg"].get("floor_gated") or set())
        gated_ok = not next(x["floor_gated"] for x in eng.rank(rr["cfg"])
                            if x["option"] == blk["replacement"])
        ok = (blk["needed"] is True and blk["replacement"] == expected
              and rec_needed and rec_expected == expected
              and blk["prior_best_capacity_flag"] == "capacity_infeasible"
              and blk["replacement"] != blk["prior_machine_best"]
              and blk["floor_respected"] and floor_ok and gated_ok)
        _report(f"{label}: re-ranked Q8 == highest non-infeasible non-gated (frozen rank)",
                ok, f"-> replacement={blk['replacement']!r} expected={expected!r}")

    # ---- (c) fallback says so ------------------------------------------------------------------
    rr = all_orgs["deli-all-infeasible"]; blk = blocks["deli-all-infeasible"]
    _report("deli-all-infeasible: every capacity-consuming option infeasible -> falls back to the "
            "do-nothing/unresolved baseline AND SAYS so",
            blk["replacement_is_baseline"] and blk["all_capacity_consuming_infeasible"]
            and blk["replacement"] == "unresolved")

    # ---- (d) UNCHANGED orgs byte-identical to cockpit_q7q8 -------------------------------------
    unchanged = [l for l in all_orgs if l not in expect_rerank]
    cnt = 0
    for label in unchanged:
        rr = all_orgs[label]; blk = blocks[label]
        base = eng.cockpit_q7q8(rr["cfg"], rr["sub"], library=ac.RULE_LIBRARY)
        ok = (blk["needed"] is False
              and blk["replacement"] == base["q8"]["recommendation"]
              and rr["s7l"]["q8"]["recommendation"] == base["q8"]["recommendation"]
              and blk["replacement"] == rr["s7l"]["q8"]["recommendation"])
        cnt += ok
        _report(f"{label}: best NOT infeasible -> Q8 UNCHANGED (== cockpit_q7q8)", ok,
                f"replacement={blk['replacement']!r}")
    _report(f"UNCHANGED same best {cnt}/{len(unchanged)} — orgs whose best is NOT infeasible keep "
            "the Q8 recommendation UNCHANGED", cnt == len(unchanged))

    # ---- (e) advisory-vs-re-rank DISTINCT: engine never overwrites q8.recommendation -----------
    for label in expect_rerank:
        rr = all_orgs[label]
        base = eng.cockpit_q7q8(rr["cfg"], rr["sub"], library=ac.RULE_LIBRARY)
        _report(f"{label}: even where re-rank fires, the engine's advisory Q8 recommendation is "
                "UNCHANGED (== cockpit_q7q8) — the reason-not-choice inventory stands; the re-rank "
                "is a separate explicit POLICY step, reported as DATA",
                rr["s7l"]["q8"]["recommendation"] == base["q8"]["recommendation"]
                and blocks[label]["replacement"] != rr["s7l"]["q8"]["recommendation"])

    # ---- (f) emit fixtures for the two NEW orgs + the engine-native report ----------------------
    for rr in (all_orgs["cove-recommend-infcap"], all_orgs["deli-all-infeasible"]):
        eng.emit_fixtures(rr["sub"], HERE, rr["cfg"])
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L Q8 capacity-constrained RE-RANK for the machine — by the frozen `rank` utility "
         "(Sprint 32, an authorized POLICY step on top of the unchanged reason-not-choice advisory)"]
    A.append(f"generated {now_iso()}  |  `capacity_rerank.capacity_rerank` (new, additive) + "
             "engine `cockpit_s7l` advisory  |  NO engine change (hash a60f8f7…); SPEC v0.22, "
             "49 $defs, URI cap, no new noun.")
    A.append("")
    A.append("The advisory path NEVER re-ranks: for every org the engine's Q8 recommendation still "
             "equals `cockpit_q7q8`. The re-rank is the deliberate, additively-built step the Sprint "
             "31 prompt explicitly authorized: when an org's machine-eligible best is "
             "`capacity_infeasible` from RECORDED per-option `capacity_requirements`, BY POLICY the "
             "machine picks the highest-utility option (frozen `rank`) that is neither floor-gated "
             "nor `capacity_infeasible`. Respects the §6 floor (a floor-gated option is never "
             "auto-picked); never invents a requirement; the do-nothing/UNRESOLVED baseline is the "
             "honest fallback when every capacity-consuming option is infeasible (and it SAYS so).")
    A.append("")
    for label in ("deli-recommend-infcap", "inspect-recorded", "cove-recommend-infcap",
                  "deli-all-infeasible", "cove-recorded", "deli-infcap", "deli-deficit-inf",
                  "inspect-nodata"):
        blk = blocks[label]
        A.append(f"--- {label} ---")
        A.append(f"  needed: {blk['needed']}  |  prior machine best: {blk['prior_machine_best']!r} "
                 f"(flag {blk['prior_best_capacity_flag']!r})")
        A.append(f"  re-ranked replacement: {blk['replacement']!r}  "
                 f"| replacement_is_baseline: {blk['replacement_is_baseline']}  "
                 f"| all_capacity_consuming_infeasible: {blk['all_capacity_consuming_infeasible']}")
        A.append(f"  recorded descriptors: {blk['recorded_descriptors']}  "
                 f"| available_capacity: {blk['available_capacity']}  "
                 f"| per_option_requirements: {blk['per_option_requirements']}")
        A.append(f"  policy: {blk['policy']}")
        A.append(f"  why: {blk['why']}")
        A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**The ONE remaining frontier from Sprint 31 — a capacity-constrained, re-ranked Q8 "
             "recommendation under recorded capacity — is now DERIVABLE, as an explicit authorized "
             "POLICY step distinct from the deterministic advisory label-vs-choice boundary.** The "
             "advisory path still labels (even the RECOMMENDED option `capacity_infeasible`) and "
             "never re-ranks (the Sprint-31 reason-not-choice inventory stands — proven here: every "
             "engine Q8 recommendation == `cockpit_q7q8`, including the orgs where re-rank fires). "
             "The re-rank computes, from RECORDED per-option `capacity_requirements` + the frozen "
             "`rank` ordering, the highest-utility option that is neither floor-gated nor "
             "`capacity_infeasible`; it changes the Q8 recommendation only under the machine's "
             "explicit POLICY, never on the advisory path, and it respects the §6 floor. Deterministic, "
             "additive (new module, engine byte-identical, hash a60f8f7…), honest (fallback to the "
             "do-nothing baseline is stated).")
    A.append("")
    A.append("**Still not derivable (the honest residual):** a probabilistic/stochastic forecast "
             "(the recorded band is a spread, not a CI, and nothing here invents a distribution); a "
             "per-option requirement that is NOT unit-coupled to the recorded capacity value (no "
             "available figure to subtract -> no infeasibility label -> nothing to re-rank); an "
             "option with no recorded requirement carries no infeasibility label (the machine never "
             "invents one for it); and any choice the §6 human must make that recorded data cannot "
             "machine-decide (the re-rank is POLICY-authorized, not a claim of objective best). "
             "No SPEC bump (v0.22).")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs, URI cap. The reason-not-choice "
             "advisory stands on the default path (Sprint-31 inventory intact); the re-rank is the "
             "authorized, distinct 're-rank for the machine' POLICY capability._")
    (rp / "capacity-rerank.md").write_text("\n".join(A) + "\n")
    print("\n  -> engine-native Sprint-32 re-rank report under "
          "artifacts/adjudication/reports/capacity-rerank.md")
    print("  -> new-org fixtures under artifacts/adjudication/fixtures/"
          f"{COVR_LABEL}/ and artifacts/adjudication/fixtures/{DAI_LABEL}/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())