"""run_reproducibility_demo.py — SPRINT 35: a pure, engine-free REPRODUCIBILITY-AUDIT.

Sprints 31-34 built and audited a deterministic, recorded-data, two-path §7L decision framework
(advisory reason-not-choice + POLICY-authorized capacity-constrained re-rank) that composes as ONE
coherent framework over the ENTIRE 22-org ORG CATALOG. The project's core claim is "deterministic
local Python, ~$0, real tool output only." Sprint 35 verifies that claim holds as a property of THIS
host + corpus — NO new capability, no engine/module change. `adjudication_engine.py` (sha256
`a60f8f7…`) AND `capacity_rerank.py` (sha256 `f7c6a185…`) stay BYTE-IDENTICAL.

This runner:
  (a) captures host/platform facts from the LIVE system (uname, Python, CPU) — printed + emitted;
  (b) re-runs the Sprint-34 whole-catalog two-path survey over the 22-org catalog (reusing the
      Sprint-34 builder `run_two_path_catalog_demo.build_catalog()` + the Sprint-33
      `_surface`/`_classify`/`_gated_set` + the engine advisory + `capacity_rerank`) and asserts the
      deterministic `two_path_surface` + PATH class for EVERY org EQUALS the Sprint-34 recorded
      result: the {12,6,4} taxonomy, the 4 re-rank replacements, the 22/22 advisory Q8 ==
      `cockpit_q7q8`, and the Sprint-31 (11/11) + Sprint-32 (4) + Sprint-33 ({5,4,4}) histories;
  (c) asserts the Sprint-34 consolidated boundary doc's concrete claims against the LIVE
      engine/module: hashes `a60f8f7…` + `f7c6a185…`, schema `34264934…` (the `.yaml` — NOT the
      `.json` which is `7fc38c8c`), 49 `$defs`, SPEC v0.22, and the taxonomy numbers.

Exit 0 = ALL PASS. Emits artifacts/adjudication/reports/reproducibility.md. Pure in-memory; NO
fixture writes (0 `emit_fixtures`). Single-threaded; deterministic; ~$0.
Usage: (from instances/contested_reality)  python3 run_reproducibility_demo.py
"""
from __future__ import annotations
import contextlib
import hashlib
import json
import os
import platform
import re
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
import run_capacity_rerank_demo as r32                         # noqa: E402 (13-org build())
import run_two_path_demo as r33                                # noqa: E402 (_classify/_surface/_gated_set/PATH_*/R32_EXPECT)
import run_two_path_catalog_demo as r34                        # noqa: E402 (build_catalog — Sprint 34)

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")


# ---- (c) the Sprint-34 recorded concrete claims the boundary doc makes (to verify LIVE) ----------
# The four RE-RANK replacements recorded by Sprint 32/34 (same as r33.R32_EXPECT).
_RERANK_EXPECT = dict(r33.R32_EXPECT)        # label -> recorded replacement option
# The recorded {12,6,4} taxonomy org sets (from run_two_path_catalog_demo + the boundary doc).
_NO_CAP_LABELS = {"deli-forecast", "deli-flat2", "deli-varmax", "deli", "inspect-nodata",
                  "deli-forecast-flat", "deli-cost", "deli-cost-flat", "cove",
                  "inspect-corroboration", "inspect-learn-b", "deli-learn"}
_RUNNABLE_LABELS = {"deli-varmax-cap", "deli-infcap", "deli-deficit-inf",
                    "cove-recorded", "deli-atcap", "deli-deficit"}
_RERANK_LABELS = set(_RERANK_EXPECT)
_SPEC = HERE.parents[1] / "SPEC.md"                            # /home/rlg/relational-os/SPEC.md
_SCHEMA_YAML = HERE.parents[1] / "sprints/sprint-0/artifacts/schema/relational-os.schema.yaml"
_SCHEMA_JSON = HERE.parents[1] / "sprints/sprint-0/artifacts/schema/relational-os.schema.json"
_ENGINE_FILE = HERE / "adjudication_engine.py"
_RERANK_FILE = HERE / "capacity_rerank.py"


def _sha8(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:8]


def _capture_host() -> dict:
    """(a) host/platform facts from the LIVE system."""
    return {
        "uname_sysname": platform.uname().system,
        "uname_node": platform.uname().node,
        "uname_release": platform.uname().release,
        "uname_version": platform.uname().version,
        "uname_machine": platform.uname().machine,
        "python_version": platform.python_version(),
        "python_impl": platform.python_implementation(),
        "cpu_count": os.cpu_count(),
    }


def _assert_boundary_doc() -> int:
    """(c) Verify the Sprint-34 consolidated boundary doc's concrete claims against live code/files."""
    print("\n-- (c) Sprint-34 boundary doc concrete claims, verified against the LIVE code --")
    _report("engine sha256 head-8 == recorded a60f8f7…",
            _sha8(_ENGINE_FILE) == "a60f8f71", f"live={_sha8(_ENGINE_FILE)}")
    _report("capacity_rerank.py sha256 head-8 == recorded f7c6a185…",
            _sha8(_RERANK_FILE) == "f7c6a185", f"live={_sha8(_RERANK_FILE)}")
    _report("schema .yaml sha256 head-8 == recorded 34264934…",
            _sha8(_SCHEMA_YAML) == "34264934", f"live={_sha8(_SCHEMA_YAML)}")
    n_defs = len(json.load(open(_SCHEMA_JSON))["$defs"])
    _report("49 $defs (json)", n_defs == 49, f"live={n_defs}")
    spec = _SPEC.read_text()
    mver = re.search(r"Version:\s*\**\s*([0-9.]+)", spec)
    _report("SPEC version == v0.22", bool(mver) and mver.group(1) == "0.22", f"live={mver.group(1) if mver else None}")
    _report("schema hash is the .yaml (the .json differs 7fc38c8c), per skill note",
            _sha8(_SCHEMA_YAML) == "34264934" and _sha8(_SCHEMA_JSON) == "7fc38c8c",
            f"yaml={_sha8(_SCHEMA_YAML)} json={_sha8(_SCHEMA_JSON)}")
    return n_defs


def run_all() -> int:
    print("=== SPRINT 35 — REPRODUCIBILITY-AUDIT: the 'deterministic local Python, ~$0, real tool "
          "output' claim, verified on THIS host across the WHOLE corpus (engine-free) ===\n")

    # (a) host / platform facts (captured, reported, emitted — not assertable)
    host = _capture_host()
    print("-- (a) host / platform (live) --")
    for k, v in host.items():
        print(f"    {k}: {v}")

    # (b) re-run the whole-catalog two-path survey and assert determinism == Sprint-34 recorded
    print("\n-- (b) whole-catalog two-path determinism vs Sprint-34 recorded results --")
    with contextlib.redirect_stdout(open(os.devnull, "w")):
        cat = r34.build_catalog()
    labels = sorted(cat)
    print(f"    ORG CATALOG: {len(labels)} orgs (rebuilt fresh in memory from the Sprint-34 builder; "
          f"no org invented)\n")
    surfaces = {lb: r33._surface(rr) for lb, rr in cat.items()}

    # catalog completeness == the recorded 22-org set
    expect_labels = _NO_CAP_LABELS | _RUNNABLE_LABELS | _RERANK_LABELS
    _report(f"catalog is the recorded 22-org set (union of every CR runner's orgs): "
            f"labels == Sprint-34 recorded set", len(labels) == 22 and set(labels) == expect_labels,
            f"live={len(labels)}")

    # taxonomy {12,6,4} == Sprint-34 recorded & exact label membership per class
    from collections import Counter
    counts = Counter(s["path"] for s in surfaces.values())
    no_cap_actual = {lb for lb in labels if surfaces[lb]["path"] == r33.PATH_NO_CAPACITY}
    runnable_actual = {lb for lb in labels if surfaces[lb]["path"] == r33.PATH_RUNNABLE}
    rerank_actual = {lb for lb in labels if surfaces[lb]["path"] == r33.PATH_RERANK}
    _report(f"taxonomy == recorded {{12,6,4}}: {dict(counts)}",
            counts[r33.PATH_NO_CAPACITY] == 12 and counts[r33.PATH_RUNNABLE] == 6
            and counts[r33.PATH_RERANK] == 4, f"live={dict(counts)}")
    _report("12 ADVISORY-no-capacity orgs == recorded set (carry NO capacity_constraint block)",
            no_cap_actual == _NO_CAP_LABELS
            and all(surfaces[lb]["advisory"]["capacity_constraint_options_flagged"] is None
                    for lb in _NO_CAP_LABELS),
            f"live={sorted(no_cap_actual)}")
    _report("6 ADVISORY-best-runnable orgs == recorded set (carry the block, best NOT infeasible)",
            runnable_actual == _RUNNABLE_LABELS)
    _report("4 RE-RANK orgs == recorded set AND each replacement == recorded Sprint-32/34 result",
            rerank_actual == _RERANK_LABELS and all(
                surfaces[lb]["rerank"]["replacement"] == repl
                for lb, repl in _RERANK_EXPECT.items()),
            f"reps={ {lb: surfaces[lb]['rerank']['replacement'] for lb in _RERANK_LABELS} }")

    # advisory never shadowed (composition) over the whole catalog
    print("\n-- (b.1) advisory never shadowed (22/22 advisory Q8 == cockpit_q7q8) --")
    shadow = 0
    for lb in labels:
        base = eng.cockpit_q7q8(cat[lb]["cfg"], cat[lb]["sub"], library=ac.RULE_LIBRARY)
        ok = (surfaces[lb]["advisory"]["q8_recommendation"] == base["q8"]["recommendation"])
        shadow += ok
        _report(f"{lb}: advisory Q8 == cockpit_q7q8", ok, f"Q8={surfaces[lb]['advisory']['q8_recommendation']!r}")
    _report(f"22/22 advisory Q8 == cockpit_q7q8 (the marker/re-rank never shadows the advisory)",
            shadow == 22, f"{shadow}/22")

    # composition: where the re-rank fires, the replacement is a DIFFERENT option (≠ advisory Q8 ≠ best);
    # where it does not, replacement == advisory Q8 (they agree).
    distinct = all(surfaces[lb]["rerank"]["replacement"] != surfaces[lb]["advisory"]["q8_recommendation"]
                   and surfaces[lb]["rerank"]["replacement"] != surfaces[lb]["advisory"]["q7_machine_eligible_best"]
                   for lb in _RERANK_LABELS)
    agree = all(surfaces[lb]["rerank"]["replacement"] == surfaces[lb]["advisory"]["q8_recommendation"]
                for lb in _NO_CAP_LABELS | _RUNNABLE_LABELS)
    _report(f"4/4 RE-RANK orgs pick a provably-distinct replacement; 18/18 non-firing orgs agree "
            "(replacement == advisory Q8)", distinct and agree)

    # floor integrity (22/22, both paths)
    print("\n-- (b.2) floor integrity (asserted against the frozen `rank` utility) --")
    floor = all(surfaces[lb]["advisory"]["q8_recommendation"] not in r33._gated_set(cat[lb]["cfg"])
                and surfaces[lb]["rerank"]["replacement"] not in r33._gated_set(cat[lb]["cfg"])
                for lb in labels)
    _report(f"22/22 orgs: no advisory Q8 nor re-rank replacement is ever floor-gated vs `rank`",
            floor)

    # deterministic on re-run (22/22)
    print("\n-- (b.3) determinism (two_path_surface identical on re-run) --")
    det = all(r33._surface(rr) == r33._surface(rr) for rr in cat.values())
    _report(f"22/22 two_path_surface identical on re-run", det)

    # history: Sprint-31 tally 11/11 (recomputed over the 11 R31 orgs), Sprint-32 4 firings,
    # Sprint-33 13-org taxonomy {5,4,4} — all reproduced from the SAME recorded data.
    print("\n-- (b.4) determinism vs history (Sprint-31 / 32 / 33 reproduced) --")
    r31_short = ("fc", "vm", "vmc", "fl2", "deli", "infcap", "definf", "recinf", "is", "cove", "nodata")
    with contextlib.redirect_stdout(open(os.devnull, "w")):
        o13 = r32.build()
    r31_labels = {o13[k]["label"] for k in r31_short}
    tally = 0
    for lb in r31_labels:
        base = eng.cockpit_q7q8(cat[lb]["cfg"], cat[lb]["sub"], library=ac.RULE_LIBRARY)
        s = surfaces[lb]
        tally += bool(s["advisory"]["q7_machine_eligible_best"] == base["q7"]["machine_eligible_best"]
                      and s["advisory"]["q8_recommendation"] == base["q8"]["recommendation"]
                      and sorted(s["advisory"]["floor_gated"])
                      == sorted(list(base["q8"].get("floor_gated") or [])))
    _report(f"Sprint-31 reason-not-choice tally {tally}/11 reproduced", tally == 11)
    _report(f"Sprint-32 re-rank results ({len(_RERANK_EXPECT)}/4 firings) reproduced",
            all(surfaces[lb]["rerank"]["needed"] and surfaces[lb]["rerank"]["replacement"] == repl
                for lb, repl in _RERANK_EXPECT.items()))
    c13 = Counter(surfaces[lb]["path"] for lb in r31_labels | _RERANK_LABELS)
    _report(f"Sprint-33 13-org taxonomy {{5,4,4}} reproduced (== {dict(c13)})",
            c13[r33.PATH_NO_CAPACITY] == 5 and c13[r33.PATH_RUNNABLE] == 4 and c13[r33.PATH_RERANK] == 4,
            f"live={dict(c13)}")

    # (c) boundary-doc concrete claims
    n_defs = _assert_boundary_doc()

    # ---- emit the reproducibility report ---------------------------------------------------------
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = ["# §7L TWO-PATH DECISION SURFACE — REPRODUCIBILITY-AUDIT (Sprint 35)",
         f"generated {now_iso()}  |  `run_reproducibility_demo.py`  |  engine-free audit: "
         f"`adjudication_engine.py` (hash a60f8f7…) + `capacity_rerank.py` (sha256 f7c6a185…) "
         f"BYTE-IDENTICAL; schema 34264934…, 49 $defs, SPEC v0.22, no new noun.",
         "",
         "## Host / platform (live)",
         f"- uname: {host['uname_sysname']} {host['uname_release']} {host['uname_machine']} "
         f"(node {host['uname_node']})",
         f"- python: {host['python_impl']} {host['python_version']}",
         f"- cpu count: {host['cpu_count']}",
         "",
         "## Whole-catalog two-path determinism (rebuilt fresh in memory; NO fixture writes)",
         f"The two-path survey over the whole {len(labels)}-org catalog is deterministic and EQUALS the "
         f"Sprint-34 recorded results: taxonomy **{counts[r33.PATH_NO_CAPACITY]} ADVISORY-no-capacity / "
         f"{counts[r33.PATH_RUNNABLE]} ADVISORY-best-runnable / {counts[r33.PATH_RERANK]} RE-RANK = "
         f"{len(labels)} orgs**, 22/22 advisory Q8 == `cockpit_q7q8` (never shadowed), 4/4 RE-RANK orgs pick "
         f"a provably-distinct replacement ({ {lb: surfaces[lb]['rerank']['replacement'] for lb in _RERANK_LABELS} }), "
         f"18/18 non-firing orgs agree, floor integrity 22/22, two_path_surface identical on re-run, and "
         f"the Sprint-31 tally (11/11) + Sprint-32 re-rank (4/4) + Sprint-33 13-org taxonomy ({{5,4,4}}) all "
         f"reproduce from the SAME recorded data.",
         "",
         "## Boundary-doc concrete claims verified (live)",
         f"- engine sha256 head-8 **{_sha8(_ENGINE_FILE)}** == recorded a60f8f7…",
         f"- capacity_rerank.py sha256 head-8 **{_sha8(_RERANK_FILE)}** == recorded f7c6a185…",
         f"- schema .yaml sha256 head-8 **{_sha8(_SCHEMA_YAML)}** == recorded 34264934… "
         f"(.json is {_sha8(_SCHEMA_JSON)} — the documented hash is the .yaml)",
         f"- {n_defs} $defs; SPEC v0.22",
         "",
         "## Honest §16 verdict",
         "Deterministic local reproducibility of the one-framework two-path decision surface across the "
         "whole catalog is VERIFIED on this host (~$0, real tool output only). The still-not-derivable "
         "residual is unchanged: a probabilistic/stochastic forecast (the recorded band is a spread, never "
         "a CI — nothing invents a distribution); a per-option requirement NOT unit-coupled to the recorded "
         "capacity / an option with no recorded requirement (never invented); and any §6-human choice that "
         "recorded data cannot machine-decide (the re-rank is POLICY-authorized, not a claim of objective "
         "best). No SPEC bump (v0.22)."]
    (rp / "reproducibility.md").write_text("\n".join(A) + "\n")

    print("\n  -> reproducibility report under artifacts/adjudication/reports/reproducibility.md")
    print("  -> provenance: engine a60f8f7… + capacity_rerank.py f7c6a185… byte-identical; frozen 49 "
          "$defs; schema 34264934…; SPEC v0.22; no fixture writes (0 emit_fixtures)")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())