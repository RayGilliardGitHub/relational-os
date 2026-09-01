# SPRINT 35 — SUMMARY: REPRODUCIBILITY-AUDIT of the "deterministic local Python, ~$0, real tool output" claim over the WHOLE corpus (engine-free; `adjudication_engine.py` AND `capacity_rerank.py` BYTE-IDENTICAL)

## Goal
Sprints 31–34 built and audited a deterministic, recorded-data, two-path §7L decision framework
(advisory reason-not-choice + POLICY-authorized capacity-constrained re-rank) as ONE coherent whole over
the ENTIRE 22-org ORG CATALOG. The project's core claim is "deterministic local Python, ~$0, real tool
output only." **Sprint 35 is a REPRODUCIBILITY-AUDIT**: it verifies that claim holds as a property of THIS
host + corpus — no new capability, no engine/module change. It (1) re-runs the whole-catalog two-path
runner + the other CR demo runners and confirms byte-identical deterministic output vs the Sprint-34
recorded results, (2) verifies the CR corpus' green baseline as one command-set, (3) verifies the
Sprint-34 consolidated boundary cheat-sheet (`DECISION-FRAMEWORK-BOUNDARY.md`) is ACCURATE against the live
code (every cited hash/def/version/taxonomy matches), and (4) writes a short `reproducibility.md`
recording host/platform + verified determinism + build results. **`adjudication_engine.py` (sha256
`a60f8f7…`) AND `capacity_rerank.py` (sha256 `f7c6a185…`) are BYTE-IDENTICAL** (hashes recorded before AND
after); no new capability, no schema/norm change, no new noun, frozen 49 `$defs`, schema `34264934…`,
SPEC v0.22.

## The build: `run_reproducibility_demo.py` (new survey/audit runner, exit 0 = ALL PASS)
- **(a) captures host/platform facts LIVE** (uname, Python, CPU) — printed + emitted.
- **(b)** re-runs the Sprint-34 whole-catalog two-path survey over the 22-org catalog (reusing the
  Sprint-34 builder `run_two_path_catalog_demo.build_catalog()` + the Sprint-33 `_surface`/`_classify`/
  `_gated_set` + the engine advisory + `capacity_rerank`) and asserts the deterministic `two_path_surface`
  + PATH class for EVERY org EQUALS the Sprint-34 recorded result.
- **(c)** asserts the Sprint-34 consolidated boundary doc's concrete claims against the LIVE engine/module
  (hashes `a60f8f7…`+`f7c6a185…`, schema `34264934…`, 49 `$defs`, SPEC v0.22, taxonomy numbers).
- Emits `instances/contested_reality/artifacts/adjudication/reports/reproducibility.md`. 0 `emit_fixtures`.

## What is proven (all real exit-0 output)
- **Determinism on THIS host** (host = Linux 7.0.0-30-generic x86_64 `dad`, CPython 3.12.3, 20 CPU):
  taxonomy **{12 ADVISORY-no-capacity, 6 ADVISORY-best-runnable, 4 RE-RANK}** with exact per-class label
  membership; the 4 re-rank replacements (`deli-recommend-infcap`→conditional-resolution,
  `inspect-recorded`→conditional-accept-with-guarantee, `cove-recommend-infcap`→authorize-generic,
  `deli-all-infeasible`→unresolved); **22/22 advisory Q8 == `cockpit_q7q8`** (never shadowed), 4/4 distinct
  replacements (≠ advisory Q8 ≠ machine_eligible_best), 18/18 non-firing orgs agree; floor integrity 22/22;
  `two_path_surface` identical on re-run (22/22).
- **History reproduced from the SAME recorded data**: Sprint-31 tally **11/11**, Sprint-32 re-rank **4/4**,
  Sprint-33 13-org taxonomy **{5,4,4}**.
- **Boundary doc verified ACCURATE**: every concrete claim in `DECISION-FRAMEWORK-BOUNDARY.md` PASSED
  against live code — engine sha256 `a60f8f71`, `capacity_rerank.py` `f7c6a185`, schema `.yaml`
  `34264934` (`.json` `7fc38c8c` — the documented hash is the `.yaml`), 49 `$defs`, SPEC v0.22, taxonomy
  numbers. No doc fix was needed.

## Verification (all exit 0, real output)
- Green baseline FIRST: 18 CR demo runners + 5 CR conformances (Sprint-0 venv) + `build_all` +
  `conformance_all` (12 sectors) + S5 reference demo + conformance + agent demo + conformance → ALL PASS.
- NEW runner: `python3 run_reproducibility_demo.py` → **RESULT: ALL PASS** (exit 0; 40 PASS / 0 FAIL).
- Full non-regression AFTER the new runner (19 CR demos incl. the new one) + the same conformances + S5 +
  agent → ALL PASS (30/30).
- Invariants: engine raw sha256 `a60f8f7…` UNCHANGED after; `capacity_rerank.py` raw sha256 `f7c6a185…`
  UNCHANGED after; schema `34264934…`; **49 `$defs`**; SPEC v0.22; `ros/` + schema + sector `configs.py`
  untouched; no new fixture dirs (0 `emit_fixtures`); no new noun.

## Documents rolled forward
`sprints/sprint-35/reproducibility.md` (host + determinism + build results) · `sprints/sprint-35/summary.md` ·
`notes/findings.md` · the report `contested_reality/artifacts/adjudication/reports/reproducibility.md` ·
`instances/README.md` Sprint-35 entry · `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`
"Update after Sprint 35" · the `relational-os` skill note · `sprints/sprint-36/PROMPT.md`. No SPEC bump (v0.22).

## Honest §16 verdict
**Deterministic local reproducibility of the one-framework two-path decision surface across the WHOLE
catalog is VERIFIED on this host (~$0, real tool output only).** The whole-catalog two-path taxonomy
{12,6,4}, the 22/22 advisory non-shadowing, the 4 re-rank replacements, and the Sprint-31/32/33 histories
all reproduce byte-identical on this machine, and the Sprint-34 consolidated boundary doc stands as
canonical (every cited hash/def/version matched live). **Still not derivable (the honest residual,
unchanged by audit):** a probabilistic/stochastic forecast (the recorded band is a spread, never a CI);
a per-option requirement NOT unit-coupled to the recorded capacity value / an option with no recorded
requirement (never invented — `deli-atcap`/`deli-deficit` prove recorded capacity alone never reaches
RE-RANK); and any choice the §6 human must make that recorded data cannot machine-decide (the re-rank is
POLICY-authorized, not a claim of objective best). No SPEC bump (v0.22).