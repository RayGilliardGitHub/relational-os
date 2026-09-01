# SPRINT 36 — PLAN: CORPUS-CONSISTENCY note + honest boundary-doc consolidation (engine-free audit)

## Mandate (from PROMPT.md)
Sprint 36 is NOT a new capability. It is a positive, engine-untouched audit that:
(a) re-runs the Sprint-35 REPRODUCIBILITY FIGURE from the CURRENT corpus in a fresh run and asserts the
    recorded numbers reproduce byte-identical;
(b) cross-checks the two boundary/cheat-sheet docs (`DECISION-FRAMEWORK-BOUNDARY.md` and
    `ENGINE-FORECAST-CAPACITY.md` §17/§18) against EACH OTHER and the LIVE corpus for any drifted number
    or stale org list;
(c) writes a short consolidation note folding Sprint 35's reproducibility findings into the canonical docs.

`adjudication_engine.py` (a60f8f7…) AND `capacity_rerank.py` (f7c6a185…) stay BYTE-IDENTICAL —
hashes recorded before AND after. No engine change, no `rank`/`capacity_rerank` change, no SPEC bump
(v0.22), frozen 49 `$defs`, schema 34264934…, no new noun. Single-threaded per PROTOCOL; ~$0; real
tool output only.

## Steps (each sub-sprint planned first in work/<n>-plan.md)
1. Read context (done): PROMPT, prior summaries, `run_reproducibility_demo.py` (Sprint 35),
   `run_two_path_catalog_demo.py` (Sprint 34), the two boundary docs, reports, `references/operational.md`.
2. Record BASELINE hashes (done: engine a60f8f71, rerank f7c6a185, schema yaml 34264934/json 7fc38c8c).
3. **Green baseline FIRST** (before any new runner): the 18 canonical CR demo runners (per boundary doc §1)
   + `run_reproducibility_demo.py` (19 CR demos) + 5 CR conformances (Sprint-0 venv) + `build_all.py` +
   `conformance_all.py` + S5 reference demo + conformance + agent demo + conformance — ALL exit 0.
4. **Write** `run_corpus_consistency_demo.py` (NEW audit runner), working dir `work/1-plan.md` first.
   It (a) re-runs the Sprint-35 figure by importing `run_reproducibility_demo` (clean reuse, no dup
   logic) and asserting it reproduces from the current corpus; (b) cross-checks the two boundary docs
   against the LIVE corpus: parse each doc's stated {12,6,4} counts + per-class org list, the hashes
   a60f8f7…/f7c6a185…/34264934…/49 `$defs`/SPEC v0.22, and the 9-added characterization, and assert they
   agree with the live computed taxonomy; (c) reports any drift. Exit 0 = ALL PASS. Emits
   `artifacts/adjudication/reports/corpus-consistency.md`. 0 `emit_fixtures`.
5. **Full non-regression green AFTER** the new runner (20 CR demos) + same conformances + build_all +
   conformance_all + S5 ref + agent. Record hashes AFTER (must equal BEFORE).
6. **Doc consolidation**: "Update after Sprint 36" lines in DECISION-FRAMEWORK-BOUNDARY.md + §19 of
   ENGINE-FORECAST-CAPACITY.md; instances/README.md Sprint-36 entry; STRESS-TEST-SCENARIOS "Update after
   Sprint 36"; `sprints/sprint-36/summary.md` + `notes/findings.md`. No SPEC bump.
7. **The PROTOCOL step-8 termination decision**: Sprint 36 is a ritual re-audit over byte-identical
   inputs (corpus-consistency note of a pure reproducibility audit of engine untouched since Sprint 12).
   It adds NO new capability, NO new proof, NO new audit surface — it folds Sprint 35 into the docs.
   → Write `sprints/sprint-36/COMPLETE.md` (chain done + the honest residual + decisive prior sprint),
   write NO `sprint-37/PROMPT.md`, and say plainly "nothing new left for a sprint; series ends here."
8. Update the `relational-os` skill with the Sprint-36 note.