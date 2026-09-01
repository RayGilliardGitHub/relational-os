# REORG-DEPLOY — promote the runnable reference build OUT of sprints/ into a sprint-free deployment layout

**Why.** Raymond: "the docs should describe how to run the system; the sprints were just the development
cycle." The docs mention sprints because the runnable artifacts physically live under `sprints/N/artifacts/`.
To make the docs fully sprint-free, promote the runnable system to canonical, sprint-free homes. This is the
"real fix" Raymond chose (vs a low-risk doc reframe).

**Invariants that must survive (byte-verified):** schema hash `34264934…`(.yaml)/`7fc38c8c`(.json), 49 `$defs`,
SPEC v0.22, engine `a60f8f71`, `capacity_rerank.py` `f7c6a185` (both untouched), ros canonical byte-identical,
conformance C2 counts 156/28/35/55/174/316, and the full green gate (41-checks) exit 0.

## Target canonical layout (sprint-free)
```
/home/rlg/relational-os/
  ros/        package                                  (DONE)
  schema/     validator + schema: conformance.py, run_conformance.py (=gen-0),
              run_conformance_all.py (all-six, canonical), relational-os.schema.{yaml,json}, *.ebnf
  reference/  the reference build: run_s5_demo.py, s3/s4/s5_demo.py, bol_demo.py, make_fixtures.py
              + produced fixtures/ graph/ reports/ (self-emits)   [gen-5 corpus]
  data/fixtures/  conformance corpus: gen-0/ … gen-4/ (moved from sprint-0..4)  [gen-5 in reference/fixtures]
  .venv/      conformance interpreter (moved from sprint-0/artifacts; gitignored)
  tests/  scripts/  instances/             (instances unchanged except re-anchored validator import)
  sprints/                                pure narrative history (PROMPT/plan/work/notes/summaries stay)
```
`sprints/N/artifacts` RETAIN their historical PROMPT/plan/summaries/work; the runnable files/fixtures are
promoted out and the narrative runner scripts are re-anchored so nothing is left broken.

## Move map (git mv; keep history)
- `sprints/sprint-0/artifacts/{conformance.py,run_conformance.py}` → `schema/`
- `sprints/sprint-0/artifacts/schema/*` → `schema/` (schema files + EBNF + build_schema.py)
- `sprints/sprint-0/artifacts/fixtures` → `data/fixtures/gen-0`
- `sprints/sprint-{1,2,3,4}/artifacts/fixtures` → `data/fixtures/gen-{1,2,3,4}`
- `sprints/sprint-5/artifacts/{run_s5_demo.py,s3_demo.py,s4_demo.py,s5_demo.py,bol_demo.py,make_fixtures.py,fixtures,graph,reports}` → `reference/`
- `.venv` ← `sprints/sprint-0/artifacts/.venv` (local gitignored move)
- new `schema/run_conformance_all.py` = lifted `run_s5_conformance.py` logic, re-anchored to `data/fixtures/gen-0..4` + `reference/fixtures`

## Re-anchor (the risky part — must not break the byte-invariant CR corpus)
- Validator importers: instances `conformance_*`, `conformance_all.py`, `conformance_agent.py`,
  `financial/run_fin_conformance.py` → SPRINT0 now `schema/`.
- CR demos' schema-hash path (`sprints/sprint-0/artifacts/schema/…`) → `schema/…` (schema files identical → hash unchanged).
- `tests/run_checks.py`, `scripts/verify.sh`, `instances/final_verify.sh`: VENV→`.venv/bin/python`,
  reference-build cwd→`reference/`, all-six conformance→`schema/run_conformance_all.py`.
- Per-gen narrative `run_sN_conformance.py` (sprints/1..5) → SPRINT0 `schema/`, fixture root `data/fixtures/gen-N` / `reference/fixtures`.

## Then
1. Full gate from repo root + a deep cwd; must be 41/41 ALL PASS and counts unchanged.
2. Rewrite the OPERATIONAL docs (`docs/*`, `README.md`, `instances/README.md`) sprint-free, referencing the
   canonical homes + the gate. (Narrative sprint PROMPT/summary/findings are HISTORY — not edited.)
3. Verify invariants (schema hash, 49 defs, SPEC, engine/rerank/ros); commit + push after green.

## Honest boundary
`sprints/N/` stays as narrative history (docs + prompts + summaries + work). The historical per-sprint
`run_sN_conformance.py` scripts stay (re-anchored). No capability change, no SPEC bump, no schema edit.