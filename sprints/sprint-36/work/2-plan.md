# work/2-plan.md — write + run `run_corpus_consistency_demo.py`

New audit runner `instances/contested_reality/run_corpus_consistency_demo.py`:
(a) calls `run_reproducibility_demo.run_all()` (reuse the Sprint-35 figure wholesale) and asserts it exits 0
    → the recorded FIGURE reproduces from the CURRENT corpus in a fresh run;
(b) cross-checks the two boundary docs — `docs/DECISION-FRAMEWORK-BOUNDARY.md` (Sprint 34, §3 taxonomy
    table) and `docs/ENGINE-FORECAST-CAPACITY.md` (§18 whole-catalog + §17 13-org) — against EACH OTHER and
    the LIVE corpus (rebuilt fresh via `run_two_path_catalog_demo.build_catalog` + Sprint-33 `_surface`):
    parse each doc's {12,6,4} counts + per-class org list, the hashes a60f8f7…/f7c6a185…/34264934…/49
    `$defs`/SPEC v0.22, and the "9 added = 7 no-capacity + 2 best-runnable (deli-atcap/deli-deficit)"
    characterization; assert mutual + corpus consistency; report drift.
Exit 0 = ALL PASS. Emits `artifacts/adjudication/reports/corpus-consistency.md`; 0 `emit_fixtures`.

## Run
```
cd instances/contested_reality && python3 run_corpus_consistency_demo.py   # expect RESULT: ALL PASS, exit 0
grep -c emit_fixtures run_corpus_consistency_demo.py                        # expect 0 (or only prose mentions)
```
Verify: every assertion PASS; report emitted; engine + capacity_rerank sha256 STILL a60f8f71/f7c6a185.