# SPRINT 36 — SUMMARY: CORPUS-CONSISTENCY note + honest boundary-doc consolidation (the Sprint-35 reproducibility figure re-run + the two boundary docs cross-checked; engine-free; `adjudication_engine.py` AND `capacity_rerank.py` BYTE-IDENTICAL)

## Goal
Sprint 35 was a pure REPRODUCIBILITY-AUDIT: it re-ran the whole-catalog two-path §7L decision framework
(`adjudication_engine.py` `a60f8f7…`, `capacity_rerank.py` `f7c6a185…`) on this host and confirmed the
Sprint-34 recorded figure — taxonomy {12,6,4}, 4 re-rank replacements, 22/22 advisory non-shadowing, the
Sprint-31/32/33 histories — reproduces, and that the Sprint-34 boundary cheat-sheet
(`DECISION-FRAMEWORK-BOUNDARY.md`) is accurate. **Sprint 36 is a CORPUS-CONSISTENCY note + honest boundary
consolidation**: no new capability, no engine/module change. It (1) re-runs the Sprint-35 reproducibility
FIGURE from the CURRENT corpus in a fresh run and confirms it reproduces byte-identical, (2) cross-checks the
two boundary/cheat-sheet docs (`DECISION-FRAMEWORK-BOUNDARY.md` and `ENGINE-FORECAST-CAPACITY.md` §17/§18)
against each OTHER and the LIVE corpus for any drifted number or stale org list, and (3) writes a short
consolidation note folding Sprint 35 into the canonical docs. **`adjudication_engine.py` (sha256 `a60f8f7…`)
AND `capacity_rerank.py` (sha256 `f7c6a185…`) are BYTE-IDENTICAL** (recorded before AND after); no new
capability, no schema/norm change, no new noun, frozen 49 `$defs`, schema `34264934…`, SPEC v0.22.

## The build: `run_corpus_consistency_demo.py` (new survey/audit runner, exit 0 = ALL PASS)
- **(a)** re-runs the Sprint-35 reproducibility FIGURE in a FRESH run over the current corpus by importing
  `run_reproducibility_demo` wholesale (clean reuse — the whole 22-org two-path survey, taxonomy {12,6,4},
  the 4 re-rank replacements, 22/22 advisory Q8 == `cockpit_q7q8`, floor integrity, determinism, and the
  Sprint-31/32/33 histories) and asserts it reproduces byte-identical.
- **(b)** cross-checks the two boundary docs against each OTHER and the LIVE corpus: parses each class org
  list out of `DECISION-FRAMEWORK-BOUNDARY.md` §3 and verifies it EQUALS the live per-class set (rebuilt
  fresh via `run_two_path_catalog_demo.build_catalog` + Sprint-33 `_surface`); verifies
  `ENGINE-FORECAST-CAPACITY.md` §18/§17 states the same {12,6,4}=22 taxonomy, the "9 added = 7 no-capacity +
  2 best-runnable (deli-atcap/deli-deficit)" split, and the same hashes/invariants; the two docs agree with
  each other and the live corpus — no drifted number, no stale org list.
- Emits `instances/contested_reality/artifacts/adjudication/reports/corpus-consistency.md`. 0 `emit_fixtures`.

## What is proven (all real exit-0 output, on host = Linux 7.0.0-30-generic x86_64 `dad`, CPython 3.12.3, 20 CPU)
- **Sprint-35 figure reproduces from the CURRENT corpus (fresh run):** taxonomy **{12,6,4}** with exact
  per-class label membership; the 4 re-rank replacements (conditional-resolution / conditional-accept-with-
  guarantee / authorize-generic / unresolved baseline); **22/22** advisory Q8 == `cockpit_q7q8` (never
  shadowed), 4/4 distinct replacements, 18/18 non-firing orgs agree; floor integrity 22/22; two_path_surface
  identical on re-run; Sprint-31 tally 11/11 + Sprint-32 re-rank 4/4 + Sprint-33 13-org taxonomy {5,4,4}.
- **Boundary-doc consistency (mutual + corpus):** DECISION-FRAMEWORK-BOUNDARY.md §3's three class org lists
  EQUAL the live per-class sets; ENGINE-FORECAST-CAPACITY.md §18 states the same {12,6,4}=22 + the 9-added
  split; both docs carry the same hashes (`a60f8f7…`/`f7c6a185…`/`34264934…`/49 `$defs`/SPEC v0.22) which
  match live; NO drifted number, NO stale org list found → **no doc fix needed** (a doc audit, not a code
  change).

## Verification (all exit 0, real output)
- Green baseline FIRST: 19 CR demo runners (the 18 canonical + the Sprint-35 one) + 5 CR conformances
  (Sprint-0 venv) + `build_all` + `conformance_all` (12 sectors) + S5 reference demo + conformance + agent
  demo + conformance → ALL PASS.
- NEW runner: `python3 run_corpus_consistency_demo.py` → **RESULT: ALL PASS** (exit 0), incl. the re-run
  Sprint-35 figure (all 22-org + history assertions PASS) + the full cross-doc/corpus consistency block → ALL
  PASS.
- Full non-regression AFTER the new runner (20 CR demos incl. the new one) + the same conformances + S5 +
  agent → ALL PASS.
- Invariants: engine raw sha256 `a60f8f7…` UNCHANGED after; `capacity_rerank.py` raw sha256 `f7c6a185…`
  UNCHANGED after; schema `34264934…`; **49 `$defs`**; SPEC v0.22; `ros/` + schema + sector `configs.py`
  untouched; no new fixture dirs (0 `emit_fixtures` calls in the new runner — only 2 prose mentions); no new
  noun.

## Documents rolled forward
`sprints/sprint-36/summary.md` · `notes/findings.md` · the report
`contested_reality/artifacts/adjudication/reports/corpus-consistency.md` · "Update after Sprint 36" in
`DECISION-FRAMEWORK-BOUNDARY.md` + `ENGINE-FORECAST-CAPACITY.md` (§19) + `instances/README.md` +
`/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` · the `relational-os` skill note ·
`sprints/sprint-36/COMPLETE.md` (series ends — see below). No SPEC bump (v0.22).

## Honest §16 verdict
**The Sprint-35 reproducibility record is reproducible AS A FIGURE from the current corpus, and the two
boundary docs are mutually consistent and consistent with the live corpus** — deterministic local
reproducibility of the one-framework two-path decision surface across the whole catalog is RE-VERIFIED on
this host (~$0, real tool output only), and the Sprint-34 cheat-sheet + ENGINE-FORECAST-CAPACITY §18/§17 stand
as consistent, drift-free canon. **Still not derivable (the honest residual, unchanged by audit):** a
probabilistic/stochastic forecast (the recorded band is a spread, never a CI); a per-option requirement NOT
unit-coupled to the recorded capacity value / an option with no recorded requirement (never invented —
`deli-atcap`/`deli-deficit` prove recorded capacity alone never reaches RE-RANK); and any choice the §6 human
must make that recorded data cannot machine-decide (the re-rank is POLICY-authorized, not a claim of objective
best). Serial sprints 20–36 have closed every derivable seam; what remains — the probabilistic/stochastic
frontier, non-unit-coupled per-option capacity, and the §6-human floor — is the honest boundary the project
refuses to invent, or a choice only a human can make, and every re-audit (33/34/35/36) re-verifies ground
already proven over byte-identical recorded data. **Per PROTOCOL step 8 the series ends: `sprints/sprint-36/
COMPLETE.md` written, no `sprint-37/PROMPT.md`.** No SPEC bump (v0.22).