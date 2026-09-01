# work/2-plan — build `run_reproducibility_demo.py` (new audit runner, exit 0 = ALL PASS)

## Goal (Sprint 35 target #1)
A new runner that (a) captures host/platform facts from the live system, (b) re-runs the Sprint-34
whole-catalog two-path survey over the 22-org catalog and asserts the deterministic `two_path_surface`
+ PATH class for EVERY org EQUALS the Sprint-34 recorded results, and (c) asserts the Sprint-34
consolidated boundary doc's concrete claims against the live engine/module. Emits
`artifacts/adjudication/reports/reproducibility.md`.

## Reuse (no new build logic — the audit IS the point)
Import the Sprint-34 catalog builder + Sprint-33 classify/surface, exactly as `run_two_path_catalog_demo.py`
does: `r34.build_catalog()` for the 22 orgs; `r33._surface`/`_classify`/`_gated_set`/`PATH_*`/`R32_EXPECT`.
Build fresh in memory; NO fixture writes (0 `emit_fixtures`).

## Assertions (each `_report` PASS/FAIL)
- host facts: uname (sysname/release/machine), python version, cpu count — printed + written (not assertable).
- catalog completeness: exactly 22 orgs; labels == the recorded Sprint-34 set.
- taxonomy: {12 ADVISORY-no-capacity, 6 ADVISORY-best-runnable, 4 RE-RANK} == recorded Sprint-34 counts.
- 12 no-capacity org labels match the recorded list; 6 best-runnable match; 4 RE-RANK match (the `R32_EXPECT`
  set), incl. each RE-RANK replacement == the recorded Sprint-32/34 replacement.
- advisory never shadowed: for every org advisory Q8 == `cockpit_q7q8`; where rerank fires replacement is
  distinct (≠ advisory Q8 ≠ machine_eligible_best); else replacement == advisory Q8.
- floor integrity: 22/22, neither advisory Q8 nor rerank replacement is floor-gated vs `rank`/`_gated_set`.
- determinism vs history: two_path_surface identical on re-run (22/22); Sprint-31 tally 11/11 (recompute
  the 11 R31 labels via r32.build short keys, as Sprint-34 does); Sprint-32 4 firings; Sprint-33 {5,4,4}.
- boundary-doc concrete claims (hashed/read live):
  - engine raw sha256 head-8 == `a60f8f71`
  - capacity_rerank.py raw sha256 head-8 == `f7c6a185`
  - schema `.yaml` sha256 head-8 == `34264934` (the documented hash is the `.yaml` — NOT the `.json`
    which is `7fc38c8c`)
  - 49 `$defs` (json loaded in python)
  - SPEC.md Version == 0.22

## Output
- stdout: host facts + per-org PATH/surface + each assertion; final `RESULT: ALL PASS` (or FAILURES)
- `artifacts/adjudication/reports/reproducibility.md` (host/platform + determinism + build results)

## Code notes
- Anchor paths to `Path(__file__).resolve().parent`; keep the same sys.path injection as the other CR runners.
- Hash files with stdlib hashlib + json; read SPEC.md with grep-free stdlib (regex over the file text).
- Import `platform`, `socket`/`os`, `hashlib`, `json`, `re`.
- Engine + `capacity_rerank.py` UNTOUCHED — this module only reads them for hashes.
- Single-threaded; deterministic; ~$0.