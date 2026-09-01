# SPRINT 36 — PROMPT (a pure, engine-free CROSS-HOST/CORPUS-CONSISTENCY note + the honest-boundary doc consolidation; verify the Sprint-35 reproducibility record is reproducible AS A FIGURE, and that the boundary cheat-sheet line up with the present corpus. NO new capability; `adjudication_engine.py` AND `capacity_rerank.py` stay BYTE-IDENTICAL.)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here; read
before acting; never fabricate; **every documented command MUST be run and its real output captured.**
Sprint 35 was a pure REPRODUCIBILITY-AUDIT: it re-ran the whole-catalog two-path §7L decision framework
(engine `a60f8f7…`, `capacity_rerank.py` `f7c6a185…`) on the host `dad` (Linux 7.0.0-30-generic x86_64,
CPython 3.12.3, 20 CPU) over the whole 22-org ORG CATALOG, confirmed the {12,6,4} taxonomy + 4 re-rank
replacements + 22/22 advisory non-shadowing + the Sprint-31/32/33 histories all reproduce byte-identical,
AND verified the Sprint-34 consolidated boundary cheat-sheet (`DECISION-FRAMEWORK-BOUNDARY.md`) is accurate
against live code (every cited hash/def/version matched). **Sprint 36 is a CORPUS-CONSISTENCY note + honest
boundary consolidation**: no new capability, no engine/module change — it (a) re-verifies the Sprint-35
reproducibility FIGURE (the exact numbers it recorded) reproduces from the current corpus in a fresh run,
(b) checks that the two boundary/cheat-sheet documents (`DECISION-FRAMEWORK-BOUNDARY.md` and the
ENGINE-FORECAST-CAPACITY §18/§17) are mutually consistent and consistent with the live corpus (no
drifted number, no stale org list), and (c) writes a short consolidation note folding the Sprint-35
reproducibility findings into the canonical documents. Survey/audit only.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7K.1, §7L (the ten morning
  questions), §7J.11 + §C16 (URI cap), the frozen 49 `$defs`.
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output, additive,
  never bump SPEC for a capability-only change; consolidation/audit sprints stay at v0.22).
- Read FIRST, in full:
  - `instances/contested_reality/run_reproducibility_demo.py` (Sprint 35 — the reproducibility audit runner),
    `run_two_path_catalog_demo.py` (Sprint 34), `run_two_path_demo.py` (Sprint 33), `run_capacity_rerank_demo.py`
    (Sprint 32), `run_recorded_surface_demo.py` (Sprint 31).
  - `instances/contested_reality/adjudication_engine.py` (hash `a60f8f7…`, DO NOT TOUCH),
    `capacity_rerank.py` (hash `f7c6a185…`, DO NOT TOUCH), `adjudication_configs.py`.
  - `instances/contested_reality/docs/DECISION-FRAMEWORK-BOUNDARY.md` (Sprint-34 cheat-sheet) +
    `instances/contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` (§17/§18) + the reports
    `instances/contested_reality/artifacts/adjudication/reports/reproducibility.md` (Sprint 35) +
    `.../two-path-catalog.md` (Sprint 34).
  - `sprints/sprint-35/{reproducibility.md,summary.md,notes/findings.md}` + `sprints/sprint-34/summary.md`.
- Project invariants (the `relational-os` skill): frozen ontology / URI cap / 49 `$defs` (§C16); additive only;
  single-threaded; plan-before-build; real tool output; ~$0; footguns (two interpreters: plain `python3` for
  demos, the Sprint-0 venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for
  conformance; runner CWD-sensitivity; the schema hash `34264934…` is the `.yaml` not the `.json`
  (`7fc38c8c`); `**Version:**` bold in SPEC.md).

## What Sprint 36 IS and IS NOT
- **IS:** a positive, engine-untouched CORPUS-CONSISTENCY audit + honest boundary consolidation. It (1)
  re-runs the Sprint-35 reproducibility runner and confirms the recorded FIGURE (the {12,6,4} taxonomy, the
  4 re-rank replacements, 22/22 advisory non-shadowing, Sprint-31 11/11 + Sprint-32 4/4 + Sprint-33 {5,4,4},
  the boundary-doc hashes) reproduces from the CURRENT corpus in a fresh run, (2) cross-checks the two
  boundary/cheat-sheet docs against each other and the live corpus for any drifted/stale number or org list,
  and (3) writes a short consolidation note folding Sprint 35 into the canonical docs. Survey/audit runner +
  recorded data ONLY; `adjudication_engine.py` AND `capacity_rerank.py` provably byte-identical (hashes
  `a60f8f7…` + `f7c6a185…` recorded before and after).
- **IS NOT:** a new capability; a change to `rank`/`capacity_rerank`/the engine; a probabilistic/stochastic
  forecast; a new URI/schema/`$defs` edit; a Trust (S5) change; breaking any prior sprint's proof or any
  reused org's default output.

## The target (what "done" looks like)
1. **A new runner `run_corpus_consistency_demo.py`** that (a) re-runs the Sprint-35 reproducibility figure
   (reusing `run_reproducibility_demo`'s assertions: the whole 22-org two-path survey, taxonomy {12,6,4}, the
   4 re-rank replacements, 22/22 advisory non-shadowing, floor integrity, determinism on re-run, the
   Sprint-31/32/33 histories) and asserts it reproduces from the CURRENT corpus; (b) cross-checks the two
   boundary documents' concrete figures against the live corpus (same hashes `a60f8f7…`+`f7c6a185…`, schema
   `34264934…`, 49 `$defs`, SPEC v0.22, the {12,6,4} org lists); (c) reports any drift. Exit 0 = ALL PASS.
   Emits `instances/contested_reality/artifacts/adjudication/reports/corpus-consistency.md`.
2. **No engine / no `capacity_rerank.py` change:** both byte-identical (hash `a60f8f7…` + `f7c6a185…`
   recorded before and after); non-regression green; reused orgs' default bytes intact.
3. **Green baseline verified as one whole** (the whole-build command set; each exit 0), BEFORE and AFTER the
   new runner.
4. **Real output:** new runner ALL PASS; the two boundary docs verified mutually consistent + consistent
   with the live corpus (any discrepancy is a DOC bug to fix in the affected `.md`, not a code change);
   frozen 49 `$defs`; schema `34264934…`; SPEC v0.22.
5. **Documentation:** `sprints/sprint-36/summary.md` + `notes/findings.md` + the `corpus-consistency.md`
   report + `sprints/sprint-37/PROMPT.md`; a short "Update after Sprint 36" consolidation line into the
   canonical docs (DECISION-FRAMEWORK-BOUNDARY.md + ENGINE-FORECAST-CAPACITY.md + instances/README + the
   completeness-review STRESS-TEST-SCENARIOS) noting the reproducibility + cross-doc consistency is
   re-verified; if any stale/missing line was found in a boundary doc, fix it with a targeted edit only.

## Mandatory rules
- **Write-first:** `sprints/sprint-36/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Terminate when there is nothing new to do (PROTOCOL step 8).** Before writing
  `sprints/sprint-37/PROMPT.md`, decide whether a sprint 37 would add new capability, a new
  proof, or a genuinely new audit surface — or only re-verify ground already proven from the
  same recorded data. If it would add nothing new (every derivable seam closed; what remains is
  the honest residual — a boundary the project refuses to invent, or a §6-human choice no machine
  can make — plus ritual re-audit over byte-identical inputs), then DO NOT write a `sprint-37/PROMPT.md`.
  Instead write `sprints/sprint-36/COMPLETE.md` (chain done + the residual boundary + the decisive
  prior sprint), write no successor, and say plainly in your final message "nothing new left for a
  sprint; series ends here." The prompt chain is a means to the work, not an obligation to run forever.
- **Real tool output only**; honest "stuck/failed" over fabrication. On a doc discrepancy, report it plainly
  and fix the DOC, never the code.
- **Additive/audit**: keep frozen functions + `capacity_rerank.py` + the 49 `$defs`/URI cap/SPEC v0.22
  untouched; re-verify `ros/`, schema `34264934…`, sector instances, the Sprint-31/32/33/34/35 reuse bytes,
  and the engine + `capacity_rerank.py` hashes `a60f8f7…` + `f7c6a185…`.
- **Single-threaded** per PROTOCOL — no subagents. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST: every CR demo runner (19 incl. the Sprint-35 one) + all 5 CR conformances
  (Sprint-0 venv) + `build_all.py` + `conformance_all.py` + S5 reference demo + conformance + agent demo +
  conformance.
- New `run_corpus_consistency_demo.py` ALL PASS (reproduces the Sprint-35 figure; boundary docs cross-doc +
  corpus consistent).
- Full non-regression green after the new runner (20 CR demos); SPEC v0.22; 49 `$defs`; `ros/` + schema clean;
  schema hash `34264934…`; engine `a60f8f7…` AND `capacity_rerank.py` `f7c6a185…` byte-identical (record both).

## Documentation (roll-forward)
Additive `corpus-consistency.md` + a "Update after Sprint 36" consolidation line in
`DECISION-FRAMEWORK-BOUNDARY.md` and `ENGINE-FORECAST-CAPACITY.md` + an instances/README.md Sprint-36 entry +
a completeness-review STRESS-TEST-SCENARIOS note + `sprints/sprint-36/summary.md` + `notes/findings.md`.
Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces. Update the `relational-os` skill's
Sprint-36 note.

## Hand-off requirement
Your **final message** must summarize: the host/platform facts (re-confirmed or updated), that the Sprint-35
reproducibility figure reproduces from the CURRENT corpus (the {12,6,4} taxonomy + 4 re-rank replacements +
22/22 advisory non-shadowing + the Sprint-31/32/33 histories all reproduced byte-identical in a fresh run),
that the two boundary docs are mutually consistent and consistent with the live corpus (and any doc fix
made), the whole-build green baseline as one command, the byte-identical default (`a60f8f7…` + `f7c6a185…`
unchanged; no new noun; frozen 49 `$defs`; schema `34264934…`; SPEC v0.22), the honest §16 verdict
(deterministic local reproducibility of the one-framework two-path decision surface across the whole catalog
is re-verified on this host, WHILE the still-not-derivable residual is unchanged: probabilistic/stochastic
forecast; a per-option requirement NOT unit-coupled to recorded capacity / an option with no recorded
requirement — never invented; any §6-human choice recorded data cannot machine-decide), and the verified
build + conformance commands.