# SPRINT 6 — FINDINGS (documentation package)

Collected during the Sprint-6 documentation sprint (no spec change; SPEC stays v0.22).
Real tool output only; single-threaded; ~$0 local computation.

## F6-1 — The conformance/demo runners are CWD-sensitive (operational gotcha, not a spec issue)
`run_s*_conformance.py` locate the Sprint-0 validator with a **relative** path
(`Path("../../sprint-0/artifacts").resolve()`), and the resolver's `resolve()` is against the
**process working directory**, not the script file. Invoking it from the repo root
(`/home/rlg/relational-os`) fails with `ModuleNotFoundError: No module named 'conformance'` —
verified directly (first attempt failed; running from `sprints/sprint-5/artifacts` exits 0).
**Operational rule captured in the docs:** run any conformance runner from inside the
`sprint-N/artifacts/` directory, with the Sprint-0 venv interpreter. Same pattern applies to the
per-generation demo runners (the `ros/` package is imported by absolute file-path insert, but
running from the artifacts dir is the blessed, verified posture). Note: `sprints/COMPLETE.md`
says "cd does not matter" — that claim is inaccurate for conformance and is corrected in the docs.

## F6-2 — Sprint-1's demo runner is named differently (naming nuance, not a bug)
Sprints 2–5 use `run_sN_demo.py`; Sprint-1's native runner is `run_demo.py` (verified:
exit 0, ALL PASS). The run table in `03-run.md` records this so an operator is not surprised.

## F6-3 — The Sprint-0 venv ships without `pip` in bin/ (verified quirk)
`…/.venv/bin/python -m pip list` is unavailable ("pip unavailable"), yet the venv runs
conformance fine because the three deps (`jsonschema 4.26.0`, `referencing 0.37.0`,
`pyyaml 6.0.3`) are present under site-packages. `02-setup.md` therefore documents a
rebuild-of-a-broken-venv path (`python3 -m venv … && pip install jsonschema referencing pyyaml`)
rather than implying the shipped venv needs pip.

## F6-4 — The "audit" the build actually ships is the conformance + round-trip + ledger-verify harness
Re-confirms Sprint-5 F-findings: SPEC §7F's continuous audit *service*, §7G's BI *warehouse*,
§7H gateway, §7E frontends, and §8 Phase-B remain **spec'd, not built**. `04-audit.md` maps
every §7F.1 check class to the concrete check that covers it **today** (conformance C1–C5 +
`Ledger.verify()` + the full-state round-trip) and marks the rest future. `05-bi-reports.md`
maps §7G.1–.7 to built (cockpit projections) vs future (warehouse). No ambiguity introduced.

## Net spec impact
- **SPEC.md: UNCHANGED at v0.22.** No schema/`ros/`/fixture edits; docs-only sprint.
- Documentation package produced under `sprints/sprint-6/artifacts/docs/` (9 files).
- No new nouns, no new URI schemes (frozen ontology held).