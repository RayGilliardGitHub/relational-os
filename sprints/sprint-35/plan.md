# SPRINT 35 — PLAN: REPRODUCIBILITY-AUDIT (engine-free; verify the "deterministic local Python, ~$0, real tool output" claim holds on THIS host and across the WHOLE corpus)

## Positioning
Sprints 31–34 built + audited a deterministic, recorded-data, two-path §7L decision framework
(advisory reason-not-choice + POLICY re-rank) and proved it over the whole 22-org ORG CATALOG.
Sprint 35 is a pure REPRODUCIBILITY-AUDIT: no new capability, `adjudication_engine.py`
(`a60f8f7…`) AND `capacity_rerank.py` (`f7c6a185…`) stay BYTE-IDENTICAL. It (1) verifies the
determinism claim on THIS host by re-running the whole-catalog two-path runner + other CR demos and
confirming byte-identical deterministic output vs the Sprint-34 recorded {12,6,4} taxonomy, 4 re-rank
replacements, 22/22 advisory non-shadowing, and the Sprint-31/32/33 reproductions; (2) re-verifies the
boundary cheat-sheet (`DECISION-FRAMEWORK-BOUNDARY.md`) is ACCURATE against live code (every cited hash /
def / version / taxonomy matches); (3) verifies the whole-build green baseline as one command-set
(each exit 0); and (4) writes `reproducibility.md`. SPEC stays v0.22.

## Live invariants (verified this session, before any build)
- engine `sha256sum` first 8 = `a60f8f71`; `capacity_rerank.py` = `f7c6a185`
- schema `.yaml` sha256 (first 8) = `34264934` (the documented hash is the `.yaml`, not the `.json`
  which is `7fc38c8c`); 49 `$defs` (json loaded in python3); SPEC **Version: 0.22**
- host: Linux `7.0.0-30-generic x86_64`; Python 3.12.3 (plain `python3`); 20 CPUs
- CR runner dir: 25 `run_*_demo.py` (18 are the CR decision-surface demos named in the boundary doc)
  + 5 `conformance_*.py`

## Steps (ordered; single-threaded; real output only; ~$0)
1. **Green baseline FIRST** (Sprint-34 committed state). From `instances/contested_reality` run the 18
   CR demo runners (the boundary-doc set) + the 5 CR conformances (Sprint-0 venv);
   `instances/build_all.py` + `<venv> conformance_all.py`; S5 reference demo + conformance; agent demo +
   conformance. Capture exit codes — ALL must be 0. (work/1-plan.md → work/1.md)
2. **Write `run_reproducibility_demo.py`** (new survey/audit runner, exit 0 = ALL PASS): captures
   host/platform facts from the live system; builds the whole 22-org catalog fresh in memory (reusing
   the Sprint-34 builder `run_two_path_catalog_demo.build_catalog` + Sprint-33 `_surface`/`_classify`/
   `_gated_set`); asserts for EVERY org the deterministic `two_path_surface` + PATH class EQUALS the
   Sprint-34 recorded results ({12,6,4} taxonomy, 4 re-rank replacements, 22/22 advisory Q8 ==
   `cockpit_q7q8`, Sprint-31 11/11 + Sprint-32 4 firings + Sprint-33 {5,4,4} reproductions);
   and asserts the boundary doc's concrete claims (hashes `a60f8f7…`+`f7c6a185…`, schema `34264934…`,
   49 `$defs`, SPEC v0.22, taxonomy numbers). Emits
   `instances/contested_reality/artifacts/adjudication/reports/reproducibility.md`. No fixture writes
   (0 `emit_fixtures`). (work/2-plan.md → work/2.md)
3. **Run it** → `RESULT: ALL PASS`. (work/3.md)
4. **Full non-regression green AFTER** the new runner (now 19 CR demos) + the same conformances + S5 +
   agent. Record engine + `capacity_rerank.py` sha256 BEFORE and AFTER (must both be unchanged).
   (work/4.md)
5. **Documentation roll-forward**: `sprints/sprint-35/reproducibility.md` (host/platform + determinism +
   build results), `summary.md`, `notes/findings.md`, `sprints/sprint-35/PROMPT.md`
   (actually sprint-36/PROMPT.md), instances/README Sprint-35 entry, STRESS-TEST-SCENARIOS "Update after
   Sprint 35" note, `relational-os` skill Sprint-35 note. If the audit found any stale/missing line in
   the boundary doc, fix it with a targeted edit (doc only, never code). No SPEC bump.
6. **Hand-off**: final message per PROMPT requirements.

## Rules
- Write-first (plan/work plans before each build step).
- Real tool output only; honest "stuck/failed" on any failure.
- Additive/audit: frozen functions, `capacity_rerank.py`, 49 `$defs`, URI cap, SPEC v0.22 untouched.
- If the boundary doc cites any number/hash that does NOT match live output → that is a DOC bug; fix the
  doc, never the code.
- Single-threaded (no subagents). Clean English, absolute `file://` paths, status at each step.