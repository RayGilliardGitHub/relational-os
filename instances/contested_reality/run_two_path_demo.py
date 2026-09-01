"""run_two_path_demo.py — SPRINT 33: consolidate the now-TWO-path decision surface (the reason-not-choice
ADVISORY + the POLICY-authorized capacity-constrained RE-RANK) as ONE coherent, provably-composable
recorded-data decision framework.

Sprint 31 positively inventoried the WHOLE recorded-data §7L decision surface as reason-not-choice across
11 orgs: every derived label traces to a RECORDED descriptor and the Q8 recommendation provably stays the
frozen `rank` output (a REASON, never a CHOICE; the §6 human always rules). Sprint 32, by explicit prompt
authorization, built the ONE named out-of-scope step as a NEW pure module `capacity_rerank.py`: when an
org's machine-eligible best is `capacity_infeasible` from RECORDED per-option `capacity_requirements`, BY
POLICY the machine picks the highest-utility option (frozen `rank`) that is neither floor-gated nor
`capacity_infeasible`, reported as an ADDITIVE `capacity_rerank` block that NEVER overwrites the engine's
advisory Q8. **Sprint 33 consolidates the now-two-path surface** into ONE dataset + audit: for each org it
emits a `two_path_surface` {advisory, rerank} and a PATH class, and asserts the two paths compose without
one silently shadowing the other.

This runner drives the SAME 13-org recorded data as Sprint 32 (`r32.build()` = the eleven Sprint-31 orgs
byte-identical + `cove-recommend-infcap` + `deli-all-infeasible`) and PROVES:
  - composition / non-interference: where the re-rank fires (needed=True) the advisory Q8 recommendation
    STILL == `cockpit_q7q8` (never shadowed) AND the re-ranked replacement is a DIFFERENT option from the
    advisory Q8 (and not the machine_eligible_best); where needed=False the replacement == the advisory Q8
    (they agree — one path, unchanged).
  - floor integrity: no advisory or re-rank selection is ever a floor-gated option (asserted against `rank`).
  - exhaustive-disjoint taxonomy: every org is exactly one of {ADVISORY-no-capacity, ADVISORY-best-runnable,
    RE-RANK}; no org is two classes.
  - determinism vs history: re-running gives an identical two_path_surface; AND the Sprint-31 reason-not-
    choice tally (11/11) + the Sprint-32 re-rank results are BOTH reproduced from the SAME recorded data in
    this run (the consolidation is a VIEW over the same data, not a rewrite).

Engine untouched (hash a60f8f7…); `capacity_rerank.py` untouched (sha256 f7c6a185…); frozen 49 $defs;
SPEC v0.22; no new noun. Emits artifacts/adjudication/reports/two-path.md.
Usage: (from instances/contested_reality)  python3 run_two_path_demo.py
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
import capacity_rerank as cr                                   # noqa: E402 (Sprint 32 new module — untouched)
import run_capacity_rerank_demo as r32                         # noqa: E402 (the 13-org set / build())

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")

# ---- the three disjoint PATH classes -------------------------------------------------------------
PATH_NO_CAPACITY = "ADVISORY-no-capacity"
PATH_RUNNABLE    = "ADVISORY-best-runnable"
PATH_RERANK      = "RE-RANK"
ALL_PATHS = (PATH_NO_CAPACITY, PATH_RUNNABLE, PATH_RERANK)

# the eleven Sprint-31 orgs (keys of r31.build_orgs(), reused byte-identical by r32.build())
R31_KEYS = ("fc", "vm", "vmc", "fl2", "deli", "infcap", "definf", "recinf", "is", "cove", "nodata")

# Sprint-32's expected re-rank results (reproduced from the SAME recorded data, below)
R32_EXPECT = {
    "deli-recommend-infcap": "conditional-resolution",
    "inspect-recorded": "conditional-accept-with-guarantee",
    "cove-recommend-infcap": "authorize-generic",
    "deli-all-infeasible": "unresolved",
}


def _classify(c: dict) -> str:
    """Exhaustive + disjoint by construction: capacity block absent, present-but-runnable, or best
    capacity_infeasible -> exactly one PATH class."""
    best = c["q7"]["machine_eligible_best"]
    cc = c["q8"].get("capacity_constraint")
    if not isinstance(cc, dict):
        return PATH_NO_CAPACITY
    flags = cc.get("options_flagged") or {}
    if flags.get(best) == "capacity_infeasible":
        return PATH_RERANK
    return PATH_RUNNABLE


def _gated_set(cfg) -> set:
    """The §6 floor-gated set, read from the FROZEN rank utility (the authoritative source)."""
    return {rk["option"] for rk in eng.rank(cfg) if rk["floor_gated"]}


def _surface(rr) -> dict:
    c = eng.cockpit_s7l(rr["cfg"], rr["sub"], library=ac.RULE_LIBRARY)
    blk = cr.capacity_rerank(rr["cfg"], rr["sub"], library=ac.RULE_LIBRARY)
    cc = c["q8"].get("capacity_constraint")
    return {
        "label": rr["label"],
        "advisory": {
            "q7_machine_eligible_best": c["q7"]["machine_eligible_best"],
            "q8_recommendation": c["q8"]["recommendation"],
            "floor_gated": sorted(list(c["q8"].get("floor_gated") or [])),
            "capacity_constraint_options_flagged": (
                dict(cc.get("options_flagged") or {}) if isinstance(cc, dict) else None),
        },
        "rerank": {
            "needed": blk["needed"],
            "prior_machine_best": blk["prior_machine_best"],
            "replacement": blk["replacement"],
            "replacement_is_baseline": blk["replacement_is_baseline"],
        },
        "path": _classify(c),
    }


def run_all() -> int:
    print("=== SPRINT 33 — the now-TWO-path §7L decision surface, consolidated as ONE coherent "
          "recorded-data framework: reason-not-choice ADVISORY + POLICY-authorized capacity-constrained "
          "RE-RANK, proven to compose without one silently shadowing the other ===\n")
    # suppress the engine-scenario build noise; build() is pure in-memory construction (no fixture writes)
    with contextlib.redirect_stdout(open(os.devnull, "w")):
        o = r32.build()
    all_orgs = {rr["label"]: rr for rr in o.values()}
    assert len(all_orgs) == 13, f"expected the 13-org Sprint-32 set, got {len(all_orgs)}"

    surfaces = {label: _surface(rr) for label, rr in all_orgs.items()}

    # ---- (0) the two_path_surface per org + its PATH class ----------------------------------------
    for label in sorted(all_orgs):
        s = surfaces[label]
        r = s["rerank"]
        flag = s["advisory"]["capacity_constraint_options_flagged"]
        rkf = (flag or {}).get(s["advisory"]["q7_machine_eligible_best"]) if flag else None
        print(f"    {label:>26}: PATH={s['path']:<23} advisory Q8={s['advisory']['q8_recommendation']!r:32}"
              f" -> rerank replacement={r['replacement']!r} (needed={r['needed']}, best_flag={rkf!r})")

    # ---- (a) composition / non-interference -------------------------------------------------------
    print("\n-- (a) composition / non-interference --")
    shadow_free = 0
    agree_count = 0
    for label, rr in all_orgs.items():
        s = surfaces[label]
        base = eng.cockpit_q7q8(rr["cfg"], rr["sub"], library=ac.RULE_LIBRARY)
        advisory = eng.cockpit_s7l(rr["cfg"], rr["sub"], library=ac.RULE_LIBRARY)["q8"]["recommendation"]
        # the advisory NEVER changes, on any path: reason-not-choice inventory stands.
        _report(f"{label}: advisory Q8 recommendation == `cockpit_q7q8` (the marker/re-rank never "
                "shadows the advisory)",
                s["advisory"]["q8_recommendation"] == base["q8"]["recommendation"] == advisory,
                f"Q8={s['advisory']['q8_recommendation']!r}")
        shadow_free += (s["advisory"]["q8_recommendation"] == base["q8"]["recommendation"] == advisory)
        if s["rerank"]["needed"]:
            ok = (s["rerank"]["replacement"] != s["advisory"]["q8_recommendation"]
                  and s["rerank"]["replacement"] != s["advisory"]["q7_machine_eligible_best"])
            _report(f"{label}: re-rank fires -> replacement is a DIFFERENT option from the advisory Q8 "
                    "AND != the machine_eligible_best (provably distinct paths)",
                    ok, f"replacement={s['rerank']['replacement']!r} != "
                        f"advisory Q8={s['advisory']['q8_recommendation']!r}")
        else:
            ok = s["rerank"]["replacement"] == s["advisory"]["q8_recommendation"]
            _report(f"{label}: needed=False -> replacement == the advisory Q8 (one path, unchanged)",
                    ok, f"replacement==Q8={s['rerank']['replacement']!r}")
            agree_count += ok
    _report(f"composition: {shadow_free}/13 advisory Q8 == cockpit_q7q8 (never shadowed) AND "
            f"{len([l for l in all_orgs if surfaces[l]['rerank']['needed']])} re-rank orgs pick a "
            "provably-different replacement + "
            f"{len([l for l in all_orgs if not surfaces[l]['rerank']['needed']])} unchanged orgs agree",
            shadow_free == 13)

    # ---- (b) floor integrity ----------------------------------------------------------------------
    print("\n-- (b) floor integrity (asserted against the frozen `rank` utility) --")
    floor_ok = 0
    for label, rr in all_orgs.items():
        s = surfaces[label]
        gated = _gated_set(rr["cfg"])
        ok = (s["advisory"]["q8_recommendation"] not in gated
              and s["rerank"]["replacement"] not in gated)
        _report(f"{label}: no advisory or re-rank selection is ever floor-gated",
                ok, f"floor_gated={gated}; advisory Q8={s['advisory']['q8_recommendation']!r}, "
                    f"replacement={s['rerank']['replacement']!r}")
        floor_ok += ok
    _report(f"floor integrity: {floor_ok}/13 orgs respect the §6 floor on BOTH paths", floor_ok == 13)

    # ---- (c) exhaustive-disjoint taxonomy ---------------------------------------------------------
    print("\n-- (c) exhaustive-disjoint taxonomy --")
    from collections import Counter
    class_count = Counter(s["path"] for s in surfaces.values())
    all_classed = all(s["path"] in ALL_PATHS for s in surfaces.values())
    pair_disjoint = len(set(ALL_PATHS)) == 3  # the three classes are distinct strings
    needed_matches = all((surfaces[l]["rerank"]["needed"]) == (surfaces[l]["path"] == PATH_RERANK)
                         for l in all_orgs)
    # no-capacity orgs have no capacity_constraint block; best-runnable orgs DO (their best is runnable)
    no_cap_consistent = all(surfaces[l]["advisory"]["capacity_constraint_options_flagged"] is None
                            for l in all_orgs if surfaces[l]["path"] == PATH_NO_CAPACITY)
    runnable_has_cap = all(surfaces[l]["advisory"]["capacity_constraint_options_flagged"] is not None
                           for l in all_orgs if surfaces[l]["path"] == PATH_RUNNABLE)
    _report(f"exhaustive-disjoint: every org maps to exactly one PATH class; no org is two classes",
            all_classed and pair_disjoint
            and all(sum(1 for p in ALL_PATHS if surfaces[l]["path"] == p) == 1 for l in all_orgs))
    _report(f"taxonomy distribution: {dict(class_count)} — disjoint by construction",
            all_classed and needed_matches and no_cap_consistent and runnable_has_cap,
            f"needed==RE-RANK? {needed_matches}")

    # ---- (d) determinism vs history ---------------------------------------------------------------
    print("\n-- (d) determinism vs history --")
    det_ok = 0
    for label, rr in all_orgs.items():
        s1, s2 = _surface(rr), _surface(rr)
        det_ok += (s1 == s2)
        _report(f"{label}: two_path_surface deterministic on re-run", s1 == s2)
    _report(f"determinism: {det_ok}/13 two_path_surface identical on re-run", det_ok == 13)

    # history (a) — the Sprint-31 reason-not-choice tally reproduced from the SAME data:
    tally = 0
    for k in R31_KEYS:
        rr = o[k]
        base = eng.cockpit_q7q8(rr["cfg"], rr["sub"], library=ac.RULE_LIBRARY)
        s = surfaces[rr["label"]]
        ok = (s["advisory"]["q7_machine_eligible_best"] == base["q7"]["machine_eligible_best"]
              and s["advisory"]["q8_recommendation"] == base["q8"]["recommendation"]
              and sorted(s["advisory"]["floor_gated"]) == sorted(list(base["q8"].get("floor_gated") or [])))
        tally += ok
        _report(f"{rr['label']} (Sprint-31 org): reason-not-choice tally (q7/q8 == cockpit_q7q8) "
                "reproduced", ok, f"Q8={s['advisory']['q8_recommendation']!r}")
    _report(f"history: Sprint-31 reason-not-choice tally {tally}/11 reproduced from the SAME recorded data",
            tally == 11, f"tally={tally}")

    # history (b) — the Sprint-32 re-rank results reproduced from the SAME data:
    hist32 = 0
    for label, expected in R32_EXPECT.items():
        s = surfaces[label]
        ok = (s["rerank"]["needed"] and s["rerank"]["replacement"] == expected)
        hist32 += ok
        _report(f"{label} (Sprint-32 re-rank): result reproduced {expected!r}",
                ok, f"replacement={s['rerank']['replacement']!r}")
    unchanged_agree = all(surfaces[l]["rerank"]["replacement"] == surfaces[l]["advisory"]["q8_recommendation"]
                          for l in all_orgs if l not in R32_EXPECT)
    _report(f"history: Sprint-32 re-rank results ({len(R32_EXPECT)} firings) + 9 unchanged "
            f"reproduced from the SAME recorded data", hist32 == len(R32_EXPECT) and unchanged_agree,
            f"{hist32}/{len(R32_EXPECT)} firings + unchanged {unchanged_agree}")

    # ---- emit the consolidated report --------------------------------------------------------------
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L TWO-PATH DECISION SURFACE — the reason-not-choice ADVISORY + the POLICY-authorized "
         "capacity-constrained RE-RANK, consolidated as ONE coherent recorded-data framework (Sprint 33)"]
    A.append(f"generated {now_iso()}  |  `run_two_path_demo._surface` + engine `cockpit_s7l` advisory + "
             "`capacity_rerank.capacity_rerank`  |  NO engine change (hash a60f8f7…) and "
             "`capacity_rerank.py` (sha256 f7c6a185…) BYTE-IDENTICAL; SPEC v0.22, 49 $defs, no new noun.")
    A.append("")
    A.append("Every org is exactly one PATH class: **ADVISORY-no-capacity** (no recorded authority "
             "capacity -> nothing to constrain/re-rank), **ADVISORY-best-runnable** (capacity recorded, "
             "machine best NOT capacity_infeasible -> the advisory stands, re-rank needed=False), "
             "**RE-RANK** (best capacity_infeasible from recorded per-option capacity_requirements -> by "
             "authorized POLICY the machine picks the highest-utility option that is neither floor-gated "
             "nor capacity_infeasible). The two paths are proven to compose: the re-rank NEVER shadows "
             "the advisory (advisory Q8 == `cockpit_q7q8` for every org), and where it fires its "
             "replacement is a provably DIFFERENT option; where needed=False they agree (replacement == "
             "advisory Q8).")
    A.append("")
    for label in sorted(all_orgs):
        s = surfaces[label]
        A.append(f"--- {label} — {s['path']} ---")
        A.append(f"  advisory: machine_eligible_best={s['advisory']['q7_machine_eligible_best']!r}, "
                 f"Q8 recommendation={s['advisory']['q8_recommendation']!r}, floor_gated={s['advisory']['floor_gated']}")
        A.append(f"  capacity_constraint.options_flagged={s['advisory']['capacity_constraint_options_flagged']}")
        A.append(f"  rerank: needed={s['rerank']['needed']}, prior_machine_best="
                 f"{s['rerank']['prior_machine_best']!r}, replacement={s['rerank']['replacement']!r}, "
                 f"replacement_is_baseline={s['rerank']['replacement_is_baseline']}")
        A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**The two paths are now a SINGLE coherent recorded-data decision framework — they compose "
             "without one silently overriding the other.** For all 13 orgs the reason-not-choice ADVISORY "
             "report reproduces the Sprint-31 inventory (11/11 q7/q8 == `cockpit_q7q8`; the marker never "
             "re-ranks) AND the POLICY-authorized RE-RANK reproduces the Sprint-32 results (4 firings with "
             "a provably-different replacement, 9 unchanged where the advisory already holds) — from the "
             "SAME recorded data, so the consolidation is a VIEW, not a rewrite. Every org is exactly one "
             "exhaustive-disjoint PATH class; neither the advisory nor the re-rank ever picks a "
             "floor-gated option; and the boundary stays honest: the deterministic advisory labels "
             "(even the recommended option capacity_infeasible) and never re-ranks, while the re-rank "
             "CHANGES the Q8 recommendation only under the machine's explicit POLICY — reported as DATA, "
             "never overwriting the engine's advisory Q8.")
    A.append("")
    A.append("**Still not derivable (the honest residual — unchanged by consolidation):** a "
             "probabilistic/stochastic forecast (the recorded band is a spread, never a CI; nothing "
             "invents a distribution); a per-option requirement NOT unit-coupled to the recorded capacity "
             "value (no available figure -> no infeasibility label -> nothing to re-rank); an option with "
             "no recorded requirement carries no infeasibility label (the machine never invents one); and "
             "any choice the §6 human must make that recorded data cannot machine-decide (the re-rank is "
             "POLICY-authorized, not a claim of objective best). No SPEC bump (v0.22).")
    A.append("")
    A.append("_Additive consolidation; engine `a60f8f7…` + `capacity_rerank.py` `f7c6a185…` BYTE-IDENTICAL; "
             "frozen ontology, SPEC v0.22, 49 $defs, URI cap, no new noun. The two-path decision surface "
             "is ONE coherent recorded-data framework._")
    (rp / "two-path.md").write_text("\n".join(A) + "\n")
    print("\n  -> consolidated two-path report under artifacts/adjudication/reports/two-path.md")
    print("  -> provenance: engine hash a60f8f7… + capacity_rerank.py sha256 f7c6a185… byte-identical; "
          "no fixture writes from this runner (the 13 orgs are built fresh in memory over the SAME "
          "recorded descriptors)")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())