# SPRINT 35 — REPRODUCIBILITY (host/platform + verified determinism + build results)

A pure, engine-free reproducibility-audit of the core RelationalOS claim: **deterministic local Python,
~$0, real tool output only**, for the §7L two-path decision surface over the whole ORG CATALOG. No new
capability; `adjudication_engine.py` (`a60f8f7…`) AND `capacity_rerank.py` (`f7c6a185…`) stay
BYTE-IDENTICAL. Report artifact: `instances/contested_reality/artifacts/adjudication/reports/reproducibility.md`.

## Host / platform (captured LIVE by `run_reproducibility_demo.py`)
- uname (system/release/machine): **Linux 7.0.0-30-generic x86_64**
- node: **dad**
- Python: **CPython 3.12.3**
- CPU count: **20**

## Verified determinism: the two-path framework over the whole 22-org catalog on THIS host (ALL PASS)
- ORG CATALOG = the union of every org the CR demo runners construct = **22 orgs** (rebuilt fresh in
  memory from the Sprint-34 builder; no org invented).
- Taxonomy == Sprint-34 recorded: **12 ADVISORY-no-capacity / 6 ADVISORY-best-runnable / 4 RE-RANK = 22**,
  with exact per-class label membership.
- 4 RE-RANK replacements reproduced: `deli-recommend-infcap`→conditional-resolution,
  `inspect-recorded`→conditional-accept-with-guarantee, `cove-recommend-infcap`→authorize-generic,
  `deli-all-infeasible`→unresolved.
- **22/22** advisory Q8 == `cockpit_q7q8` (never shadowed); 4/4 re-rank replacements distinct from the
  advisory Q8 AND the machine_eligible_best; 18/18 non-firing orgs agree (replacement == advisory Q8).
- Floor integrity **22/22** (asserted against the frozen `rank` utility).
- `two_path_surface` identical on re-run (**22/22** deterministic).
- History reproduced from the SAME recorded data: Sprint-31 reason-not-choice tally **11/11**, Sprint-32
  re-rank **4/4**, Sprint-33 13-org taxonomy **{5,4,4}**.

## Boundary doc verified accurate (Sprint-34 cheat-sheet stands as canonical)
Every concrete claim in `instances/contested_reality/docs/DECISION-FRAMEWORK-BOUNDARY.md` PASSED against
live code — no doc fix needed (this is a doc audit, not a code change):
- engine raw sha256 head-8 = **a60f8f71**; `capacity_rerank.py` = **f7c6a185**
- schema `.yaml` sha256 head-8 = **34264934** (the `.json` is `7fc38c8c` — the documented hash is the `.yaml`)
- **49 `$defs`**; **SPEC Version 0.22**

## Build results (green baseline + full non-regression, ALL exit 0)
- Green baseline FIRST: 18 CR demo runners + 5 CR conformances (Sprint-0 venv) + `build_all` +
  `conformance_all` (12 sectors) + S5 reference demo + conformance + agent demo + conformance → ALL PASS.
- New runner `run_reproducibility_demo.py` → **RESULT: ALL PASS** (exit 0; 40 PASS / 0 FAIL).
- Full non-regression AFTER the new runner: **19 CR demos** (incl. the new one) + the 5 conformances +
  build_all + conformance_all + S5 ref + agent → ALL PASS. Engine + `capacity_rerank.py` raw sha256
  unchanged AFTER (a60f8f71 / f7c6a185).
- No fixture writes from the new runner (0 `emit_fixtures` calls).

## Honest §16 verdict
Deterministic local reproducibility of the one-framework two-path decision surface across the WHOLE
catalog is **VERIFIED on this host** (~$0, real tool output only). The still-not-derivable residual is
UNCHANGED: a probabilistic/stochastic forecast (recorded band is a spread, never a CI — nothing invents a
distribution); a per-option requirement NOT unit-coupled to the recorded capacity value / an option with
no recorded requirement (never invented); and any §6-human choice recorded data cannot machine-decide
(the re-rank is POLICY-authorized, not objective best). No SPEC bump (v0.22).