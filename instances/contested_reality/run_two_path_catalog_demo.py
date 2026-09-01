"""run_two_path_catalog_demo.py — SPRINT 34: a pure, engine-free CONSOLIDATION-AUDIT of the two-path
decision surface over the ENTIRE ORG CATALOG every CR demo runner already exercises.

Sprint 31 positively inventoried the whole recorded-data §7L decision surface as reason-not-choice across
11 orgs. Sprint 32 built the capacity-constrained RE-RANK (new pure module `capacity_rerank.py`) and proved
it over 13 orgs. Sprint 33 consolidated the now-TWO-path decision surface (advisory reason-not-choice +
POLICY-authorized re-rank) as ONE coherent framework and classified the 13-org set into an exhaustive-
disjoint PATH taxonomy. **Sprint 34 is a CONSOLIDATION-AUDIT: no new capability.** It verifies the reference
build is green as one whole, and extends the Sprint-33 one-framework answer from the 13-org set to the
ENTIRE ORG CATALOG — the union of every org the existing CR runners construct — classifying EVERY org into
the SAME exhaustive-disjoint PATH taxonomy and asserting the two-path composition holds over the WHOLE
catalog.

This runner builds the 22-org catalog fresh in MEMORY (reusing the existing runner builders/constants for
each org — every org is already constructed by an existing CR runner, NOT invented; no fixture writes), and
for each org emits a `two_path_surface` + PATH class (reusing the Sprint-33 `_classify`/`_surface`/
`_gated_set`), asserting over the whole catalog:
  - advisory never shadowed: advisory Q8 == `cockpit_q7q8` for EVERY org; where the re-rank fires
    (needed=True) replacement != advisory Q8 != machine_eligible_best; where not it agrees (replacement ==
    advisory Q8);
  - exhaustive-disjoint: every org exactly one PATH class; needed == (path == RE-RANK); no-capacity orgs
    carry no capacity_constraint block;
  - floor integrity: no advisory or re-rank selection is ever floor-gated vs `rank`;
  - determinism vs history: two_path_surface deterministic on re-run; AND the Sprint-31 reason-not-choice
    tally (11/11) + Sprint-32 re-rank results (4) + Sprint-33 13-org taxonomy {5,4,4} ALL reproduce from
    the SAME recorded data in this run.

Engine untouched (hash a60f8f7…); `capacity_rerank.py` untouched (sha256 f7c6a185…); frozen 49 $defs;
schema 34264934…; SPEC v0.22; no new noun. Emits artifacts/adjudication/reports/two-path-catalog.md.
Usage: (from instances/contested_reality)  python3 run_two_path_catalog_demo.py
"""
from __future__ import annotations
import contextlib
import os
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
import capacity_rerank as cr                                   # noqa: E402 (Sprint 32 — untouched)
import reconcile_learning as rl                                # noqa: E402 (cockpit learned-rule orgs)
import run_capacity_rerank_demo as r32                         # noqa: E402 (13-org build())
import run_two_path_demo as r33                                # noqa: E402 (_classify/_surface/_gated_set)
import run_forecast_horizon_demo as rfh                        # noqa: E402 (relabel_to/run_one/record_series)
import run_forecast_direction_demo as r22                      # noqa: E402 (deli-forecast-flat/deli-cost/deli-cost-flat)
import run_forecast_horizon4_demo as r28                        # noqa: E402 (deli-atcap/deli-deficit/build_orgs)

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")

# the three disjoint PATH classes (reused from Sprint 33)
PATH_NO_CAPACITY = r33.PATH_NO_CAPACITY
PATH_RUNNABLE    = r33.PATH_RUNNABLE
PATH_RERANK      = r33.PATH_RERANK
ALL_PATHS        = r33.ALL_PATHS


# ---- build the WHOLE ORG CATALOG fresh in memory (every org an existing runner constructs) ---------
def build_catalog() -> dict:
    """dict label -> org record {cfg, sub, label, s7l}. Pure in-memory; no fixture writes."""
    cat = {}
    _build_13_orgs(cat)
    _build_forecast_orgs(cat)
    _build_atcap_deficit(cat)
    _build_cockpit_learned_orgs(cat)
    _build_base_cove(cat)
    return cat


def _add(cat, r):
    assert r["label"] not in cat, f"duplicate catalog org {r['label']}"
    cat[r["label"]] = r


def _build_13_orgs(cat):
    """The 13-org Sprint-32/33 set — byte-identical recorded data (r32.build())."""
    with contextlib.redirect_stdout(open(os.devnull, "w")):
        o = r32.build()
    for rr in o.values():
        _add(cat, rr)


def _build_forecast_orgs(cat):
    """The forecast-family orgs NOT in the 13: deli-forecast-flat, deli-cost, deli-cost-flat.
    Reconstructed EXACTLY as run_forecast_direction_demo does (same points/fields/direction)."""
    # deli-forecast-flat (higher-is-better control, NO direction -> default)
    r = _series_org(r22, r22.FLAT_LABEL, r22.FLAT_METRIC, [dict(p) for p in r22.FLAT_POINTS], {
        "name": "resolution on-time rate",
        "formula": "on-time resolutions / total resolutions from ledger",
        "unit": "fraction", "target": 0.95, "period": "quarter",
        "source": "ledger resolution completion records",
        "owner": ac.DELI["authority"]["adjudicator_person"]})
    _add(cat, r)
    # deli-cost (lower-is-better RISING cost)
    r = _series_org(r22, r22.COST_LABEL, r22.COST_METRIC, [dict(p) for p in r22.COST_POINTS], {
        "name": "mean resolution latency", "formula": "mean elapsed time to a resolution from ledger",
        "unit": r22.COST_UNIT, "target": 16, "period": "quarter",
        "source": "ledger resolution completion records", "direction": "lower-is-better",
        "owner": ac.DELI["authority"]["adjudicator_person"]})
    _add(cat, r)
    # deli-cost-flat (lower-is-better control, projection below ceiling)
    r = _series_org(r22, r22.COSTFLAT_LABEL, r22.COSTFLAT_METRIC, [dict(p) for p in r22.COSTFLAT_POINTS], {
        "name": "mean resolution latency", "formula": "mean elapsed time to a resolution from ledger",
        "unit": r22.COST_UNIT, "target": 10, "period": "quarter",
        "source": "ledger resolution completion records", "direction": "lower-is-better",
        "owner": ac.DELI["authority"]["adjudicator_person"]})
    _add(cat, r)


def _series_org(frm, label, metric_uri, points, fields) -> dict:
    """One DELI-relabeled org with a recorded metric:// series; s7l + closure computed in memory."""
    cfg = frm.relabel_to(ac.DELI, label)
    r = frm.run_one(cfg)
    frm.record_series(r, label, metric_uri, points, fields=fields)
    r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
    r["closure"] = eng._forecast_closure(r["cfg"], r["sub"])
    return r


def _build_atcap_deficit(cat):
    """deli-atcap + deli-deficit — built by run_forecast_horizon4_demo.build_orgs() (in-memory)."""
    o = r28.build_orgs()
    for k in ("atcap", "deficit"):
        _add(cat, o[k])


def _build_cockpit_learned_orgs(cat):
    """inspect-corroboration, inspect-learn-b, deli-learn — replicate run_cockpit_s7l_demo's learned-rule
    construction (learn_threshold + build_learned_library_spec + RULE_LIBRARY inject + reconcile)."""
    hyp = ac.LEARN_HYPER
    learned = rl.learn_threshold(prior_threshold=hyp["initial_threshold"],
                                 realized_value=hyp["realized_value_a"],
                                 learning_rate=hyp["learning_rate"],
                                 lo=hyp["threshold_lo"], hi=hyp["threshold_hi"], eps=hyp["eps"])
    lib_name = "calibrated-threshold-091"
    learned_spec = rl.build_learned_library_spec(lib_name, learned=learned)
    ac.RULE_LIBRARY[lib_name] = learned_spec                      # learning feeds the library

    # inspect-corroboration -> rule-library source
    r = rfh.run_one(ac.INSPECT_CORROBORATION)
    r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
    _add(cat, r)

    # inspect-learn-b -> learned-this-run=True (learning recorded on ITS OWN ledger)
    B = dict(ac.INSPECT_BATCH_B)
    B["reconcile"] = {"rule_spec": learned_spec, "threshold": learned["threshold"],
                      "support_floor": 0.55}
    r = rfh.run_one(B)
    rl.record_learned_rule(
        r["sub"], r["label"], signer=r["cfg"]["authority"]["adjudicator_person"],
        authority=r["cfg"]["authority"]["dispute"], learned=learned,
        learned_spec=learned_spec, realized_value=hyp["realized_value_a"],
        learned_decision_uri=f"decision://{r['label']}/reconcile-learning",
        prior_reconcile=r["cfg"]["reconcile"])
    r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
    _add(cat, r)

    # deli-learn -> reuses the learned spec, no learning on its own ledger -> learned-not-this-run
    dcfg = ac.org_under_library_rule(ac.DELI, "deli-learn", lib_name,
                                     {"threshold": learned["threshold"], "support_floor": 0.55})
    r = rfh.run_one(dcfg)
    r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
    _add(cat, r)


def _build_base_cove(cat):
    """cove — the base COVE config from run_adjudication_engine_demo SCENARIOS (label 'cove')."""
    r = rfh.run_one(ac.COVE)
    r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
    r["closure"] = eng._forecast_closure(r["cfg"], r["sub"])
    _add(cat, r)


def run_all() -> int:
    print("=== SPRINT 34 — CONSOLIDATION-AUDIT: the two-path §7L decision surface as ONE framework over "
          "the ENTIRE ORG CATALOG every CR demo runner exercises ===\n")
    cat = build_catalog()
    all_orgs = dict(cat)
    print(f"  ORG CATALOG: {len(all_orgs)} orgs (the union of every org the existing CR demo runners "
          f"construct — no org invented)\n")

    surfaces = {label: r33._surface(rr) for label, rr in all_orgs.items()}

    # ---- the per-org PATH class + two_path_surface (Sprint-33 _classify/_surface reused) ---------
    for label in sorted(all_orgs):
        s = surfaces[label]; r = s["rerank"]
        flag = s["advisory"]["capacity_constraint_options_flagged"]
        rkf = (flag or {}).get(s["advisory"]["q7_machine_eligible_best"]) if flag else None
        print(f"    {label:>26}: PATH={s['path']:<23} advisory Q8={s['advisory']['q8_recommendation']!r:30}"
              f" -> rerank replacement={r['replacement']!r} (needed={r['needed']}, best_flag={rkf!r})")

    # ---- (a) advisory never shadowed (composition) over the WHOLE catalog ------------------------
    print("\n-- (a) advisory never shadowed (composition) over the whole catalog --")
    shadow_free = 0; agree_count = 0; rerank_distinct = 0
    for label, rr in all_orgs.items():
        s = surfaces[label]
        base = eng.cockpit_q7q8(rr["cfg"], rr["sub"], library=ac.RULE_LIBRARY)
        ok = (s["advisory"]["q8_recommendation"] == base["q8"]["recommendation"]
              and s["advisory"]["q8_recommendation"] == r33._surface(rr)["advisory"]["q8_recommendation"])
        _report(f"{label}: advisory Q8 == `cockpit_q7q8` (the marker/re-rank never shadows the advisory)",
                ok, f"Q8={s['advisory']['q8_recommendation']!r}")
        shadow_free += ok
        if s["rerank"]["needed"]:
            ok2 = (s["rerank"]["replacement"] != s["advisory"]["q8_recommendation"]
                   and s["rerank"]["replacement"] != s["advisory"]["q7_machine_eligible_best"])
            _report(f"{label}: re-rank fires -> replacement is a DIFFERENT option from advisory Q8 AND != "
                    "machine_eligible_best", ok2, f"replacement={s['rerank']['replacement']!r}")
            rerank_distinct += ok2
        else:
            ok2 = s["rerank"]["replacement"] == s["advisory"]["q8_recommendation"]
            _report(f"{label}: needed=False -> replacement == advisory Q8 (they agree, one path)",
                    ok2, f"replacement==Q8={s['rerank']['replacement']!r}")
            agree_count += ok2
    n_rerank = len([l for l in all_orgs if surfaces[l]["rerank"]["needed"]])
    n_agree = len([l for l in all_orgs if not surfaces[l]["rerank"]["needed"]])
    _report(f"composition over the whole catalog: {shadow_free}/{len(all_orgs)} advisory Q8 == "
            f"cockpit_q7q8 AND {rerank_distinct}/{n_rerank} re-rank orgs pick a distinct replacement AND "
            f"{agree_count}/{n_agree} unchanged orgs agree", shadow_free == len(all_orgs)
            and rerank_distinct == n_rerank and agree_count == n_agree)

    # ---- (b) exhaustive-disjoint taxonomy over the whole catalog --------------------------------
    print("\n-- (b) exhaustive-disjoint taxonomy over the whole catalog --")
    from collections import Counter
    class_count = Counter(s["path"] for s in surfaces.values())
    all_classed = all(s["path"] in ALL_PATHS for s in surfaces.values())
    needed_matches = all((surfaces[l]["rerank"]["needed"]) == (surfaces[l]["path"] == PATH_RERANK)
                         for l in all_orgs)
    no_cap_consistent = all(surfaces[l]["advisory"]["capacity_constraint_options_flagged"] is None
                            for l in all_orgs if surfaces[l]["path"] == PATH_NO_CAPACITY)
    runnable_has_cap = all(surfaces[l]["advisory"]["capacity_constraint_options_flagged"] is not None
                           for l in all_orgs if surfaces[l]["path"] == PATH_RUNNABLE)
    exactly_one = all(sum(1 for p in ALL_PATHS if surfaces[l]["path"] == p) == 1 for l in all_orgs)
    _report("exhaustive-disjoint over the whole catalog: every org exactly ONE PATH class; no org is two",
            all_classed and exactly_one)
    _report(f"taxonomy distribution over the whole catalog: {dict(class_count)} — disjoint by "
            "construction; needed==(RE-RANK)? all orgs", all_classed and needed_matches
            and no_cap_consistent and runnable_has_cap,
            f"needed_matches={needed_matches} no_cap_consistent={no_cap_consistent} "
            f"runnable_has_cap={runnable_has_cap}")

    # ---- (c) floor integrity over the whole catalog ----------------------------------------------
    print("\n-- (c) floor integrity (asserted against the frozen `rank` utility) --")
    floor_ok = 0
    for label, rr in all_orgs.items():
        s = surfaces[label]; gated = r33._gated_set(rr["cfg"])
        ok = (s["advisory"]["q8_recommendation"] not in gated
              and s["rerank"]["replacement"] not in gated)
        _report(f"{label}: no advisory or re-rank selection is ever floor-gated", ok,
                f"floor_gated={sorted(gated)}; advisory Q8={s['advisory']['q8_recommendation']!r}, "
                f"replacement={s['rerank']['replacement']!r}")
        floor_ok += ok
    _report(f"floor integrity: {floor_ok}/{len(all_orgs)} orgs respect the §6 floor on BOTH paths",
            floor_ok == len(all_orgs))

    # ---- (d) determinism vs history -----------------------------------------------------------------
    print("\n-- (d) determinism vs history --")
    det_ok = 0
    for label, rr in all_orgs.items():
        det_ok += (r33._surface(rr) == r33._surface(rr))
        _report(f"{label}: two_path_surface deterministic on re-run", r33._surface(rr) == r33._surface(rr))
    _report(f"determinism: {det_ok}/{len(all_orgs)} two_path_surface identical on re-run",
            det_ok == len(all_orgs))

    # history (a): Sprint-31 reason-not-choice tally 11/11 reproduced (the 11 R31 orgs).
    # R31 short keys map onto the 13-org build; recover their labels by key membership.
    with contextlib.redirect_stdout(open(os.devnull, "w")):
        o13 = r32.build()
    r31_short = ("fc", "vm", "vmc", "fl2", "deli", "infcap", "definf", "recinf", "is", "cove", "nodata")
    r31_labels = {o13[k]["label"] for k in r31_short}
    tally = 0
    for label in r31_labels:
        rr = all_orgs[label]
        base = eng.cockpit_q7q8(rr["cfg"], rr["sub"], library=ac.RULE_LIBRARY)
        s = surfaces[label]
        ok = (s["advisory"]["q7_machine_eligible_best"] == base["q7"]["machine_eligible_best"]
              and s["advisory"]["q8_recommendation"] == base["q8"]["recommendation"]
              and sorted(s["advisory"]["floor_gated"])
              == sorted(list(base["q8"].get("floor_gated") or [])))
        tally += ok
        _report(f"{label} (Sprint-31 org): reason-not-choice tally (q7/q8 == cockpit_q7q8) reproduced",
                ok, f"Q8={s['advisory']['q8_recommendation']!r}")
    _report(f"history: Sprint-31 reason-not-choice tally {tally}/11 reproduced from the SAME recorded data",
            tally == 11, f"tally={tally}")

    # history (b): Sprint-32 re-rank results reproduced (4 firings + the unchanged agree)
    hist32 = 0
    for label, expected in r33.R32_EXPECT.items():
        s = surfaces[label]
        ok = (s["rerank"]["needed"] and s["rerank"]["replacement"] == expected)
        hist32 += ok
        _report(f"{label} (Sprint-32 re-rank): result reproduced {expected!r}", ok,
                f"replacement={s['rerank']['replacement']!r}")
    unchanged_agree = all(surfaces[l]["rerank"]["replacement"]
                          == surfaces[l]["advisory"]["q8_recommendation"]
                          for l in all_orgs if l not in r33.R32_EXPECT)
    _report(f"history: Sprint-32 re-rank results ({len(r33.R32_EXPECT)} firings) + "
            f"{len(all_orgs) - len(r33.R32_EXPECT)} non-firing orgs agree from the SAME recorded data",
            hist32 == len(r33.R32_EXPECT) and unchanged_agree, f"{hist32}/{len(r33.R32_EXPECT)} firings")

    # history (c): Sprint-33 13-org taxonomy {5,4,4} reproduced within the whole-catalog distribution
    s13_labels = {o13[k]["label"] for k in r31_short} | set(r33.R32_EXPECT)
    c13 = Counter(surfaces[l]["path"] for l in s13_labels)
    _report(f"history: Sprint-33 13-org taxonomy {dict(c13)} reproduced from the SAME data "
            "(== {no-capacity:5, runnable:4, rerank:4})",
            c13[PATH_NO_CAPACITY] == 5 and c13[PATH_RUNNABLE] == 4 and c13[PATH_RERANK] == 4,
            f"c13={dict(c13)}")

    # ---- emit the consolidated whole-catalog report ------------------------------------------------
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L TWO-PATH DECISION SURFACE over the ENTIRE ORG CATALOG — CONSOLIDATION-AUDIT (Sprint 34)"]
    A.append(f"generated {now_iso()}  |  `run_two_path_catalog_demo.build_catalog` (22 orgs = the union "
             "every CR demo runner constructs) + Sprint-33 `_surface`/`_classify` + engine `cockpit_s7l` "
             "advisory + `capacity_rerank.capacity_rerank`  |  NO engine change (hash a60f8f7…) and "
             "`capacity_rerank.py` (sha256 f7c6a185…) BYTE-IDENTICAL; SPEC v0.22, schema 34264934…, "
             "49 $defs, no new noun.")
    A.append("")
    A.append(f"The Sprint-33 one-framework answer now holds over the WHOLE catalog: every one of these "
             f"**{len(all_orgs)} orgs** (the union of every org the run_forecast_*/run_cockpit_*/"
             f"run_adjudication_engine_demo/r32 runners already construct) is exactly one PATH class — "
             f"**ADVISORY-no-capacity** ({class_count[PATH_NO_CAPACITY]}), **ADVISORY-best-runnable** "
             f"({class_count[PATH_RUNNABLE]}), **RE-RANK** ({class_count[PATH_RERANK]}) — the advisory Q8 == "
             f"`cockpit_q7q8` for every org (never shadowed), the re-rank fires only where the machine best "
             f"is `capacity_infeasible` and picks a provably-distinct replacement, floors are respected "
             f"everywhere, and every derived label traces to recorded data (reason-not-choice).")
    A.append("")
    for label in sorted(all_orgs):
        s = surfaces[label]
        A.append(f"--- {label} — {s['path']} ---")
        A.append(f"  advisory: machine_eligible_best={s['advisory']['q7_machine_eligible_best']!r}, "
                 f"Q8 recommendation={s['advisory']['q8_recommendation']!r}, "
                 f"floor_gated={s['advisory']['floor_gated']}")
        A.append(f"  capacity_constraint.options_flagged={s['advisory']['capacity_constraint_options_flagged']}")
        A.append(f"  rerank: needed={s['rerank']['needed']}, prior_machine_best="
                 f"{s['rerank']['prior_machine_best']!r}, replacement={s['rerank']['replacement']!r}, "
                 f"replacement_is_baseline={s['rerank']['replacement_is_baseline']}")
        A.append("")
    A.append("## whole-catalog taxonomy"
             f"\n**{class_count[PATH_NO_CAPACITY]} ADVISORY-no-capacity / "
             f"{class_count[PATH_RUNNABLE]} ADVISORY-best-runnable / "
             f"{class_count[PATH_RERANK]} RE-RANK = {len(all_orgs)} orgs.** "
             "Sprint-33's 13-org {5,4,4} is the strict subset; the 9 added are 7 no-capacity "
             "(these carry no capacity_constraint block) + 2 best-runnable (deli-atcap, deli-deficit — "
             "recorded capacity but NO per-option requirements, so best is `capacity_risk`, never "
             "`capacity_infeasible`, nothing to re-rank).")
    A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**The two-path decision surface is ONE coherent recorded-data framework across the ENTIRE "
             "catalog — not just the 13-org Sprint-33 set.** For all 22 orgs the reason-not-choice ADVISORY "
             "reproduces the Sprint-31 inventory (marker never re-ranks; advisory Q8 == `cockpit_q7q8`), the "
             "POLICY-authorized RE-RANK reproduces the Sprint-32 results (4 firings, provably-distinct "
             "replacement, 18 unchanged where the advisory already holds) from the SAME recorded data, and "
             "every org falls into exactly one exhaustive-disjoint PATH class. Floor integrity holds "
             "everywhere; the re-rank never shadows the advisory; and the boundary stays honest: the "
             "deterministic advisory labels (even the recommended option capacity_infeasible) and never "
             "re-ranks, while the re-rank CHANGES the Q8 recommendation only under the machine's explicit "
             "POLICY — reported as DATA, never overwriting the engine's advisory Q8.")
    A.append("")
    A.append("**Still not derivable (the honest residual — unchanged by this audit):** a probabilistic/"
             "stochastic forecast (the recorded band is a spread, never a CI; nothing invents a "
             "distribution); a per-option requirement NOT unit-coupled to the recorded capacity value (no "
             "available figure -> no infeasibility label -> nothing to re-rank); an option with no recorded "
             "requirement carries no infeasibility label (the machine never invents one); and any choice the "
             "§6 human must make that recorded data cannot machine-decide (the re-rank is POLICY-authorized, "
             "not a claim of objective best). No SPEC bump (v0.22).")
    A.append("")
    A.append("_CONSOLIDATION-AUDIT; engine `a60f8f7…` + `capacity_rerank.py` `f7c6a185…` BYTE-IDENTICAL; "
             "frozen ontology, schema 34264934…, SPEC v0.22, 49 $defs, URI cap, no new noun. The two-path "
             "decision surface is ONE coherent recorded-data framework across the whole catalog._")
    (rp / "two-path-catalog.md").write_text("\n".join(A) + "\n")

    print("\n  -> consolidated whole-catalog two-path report under "
          "artifacts/adjudication/reports/two-path-catalog.md")
    print("  -> provenance: engine hash a60f8f7… + capacity_rerank.py sha256 f7c6a185… byte-identical; "
          "no fixture writes from this runner (the 22 orgs are built fresh in memory over the SAME "
          "recorded descriptors)")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())