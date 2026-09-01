# SPRINT 36 — COMPLETE: the §7L two-path decision-surface series ENDS here (no sprint 37)

**Spec:** v0.22 | **Date:** 2026-09-01 | **Engine + module:** `adjudication_engine.py` (sha256 head-8
`a60f8f71`) AND `capacity_rerank.py` (sha256 head-8 `f7c6a185`) — **BYTE-IDENTICAL** to Sprint 12/32 state;
**schema** 34264934… (`.yaml`) / 7fc38c8c (`.json`), **49 `$defs`**, URI cap, **no new noun**.

## What Sprint 36 was and what it proved
A pure, engine-free **CORPUS-CONSISTENCY note + honest boundary-doc consolidation** (`run_corpus_consistency_demo.py`,
exit 0 = ALL PASS; the report `instances/contested_reality/artifacts/adjudication/reports/corpus-consistency.md`):
1. **The Sprint-35 reproducibility figure reproduces from the CURRENT corpus** (reused `run_reproducibility_demo`
   wholesale in a fresh run): whole 22-org two-path survey, taxonomy **{12,6,4}**, the 4 re-rank replacements
   (conditional-resolution / conditional-accept-with-guarantee / authorize-generic / unresolved baseline),
   **22/22** advisory Q8 == `cockpit_q7q8` (never shadowed), floor integrity 22/22, two_path_surface
   deterministic on re-run, and the Sprint-31 (11/11) + Sprint-32 (4/4) + Sprint-33 ({5,4,4}) histories — all
   byte-identical.
2. **The two boundary docs are mutually consistent and consistent with the live corpus**: every class org
   list parsed from `DECISION-FRAMEWORK-BOUNDARY.md` §3 equals the live per-class set; `ENGINE-FORECAST-CAPACITY.md`
   §18/§17 states the same {12,6,4}=22 taxonomy + the "9 added = 7 no-capacity + 2 best-runnable
   (deli-atcap/deli-deficit)" split + the same hashes; no drifted number, no stale org list, **no doc fix needed**.
3. The consolidation note was folded into both boundary docs (+ instances/README + STRESS-TEST-SCENARIOS).

## Why the series ends here (PROTOCOL step 8 — terminate when there is nothing new)
Sprint 36 is another ritual re-audit over **byte-identical inputs** (the corpus-consistency note of a
reproducibility audit of an engine untouched since Sprint 12). Sprints 20–32 added the whole recorded-data
§7L decision surface (forecast/capacity/flag → re-rank) with genuinely new capability each time; sprints
33–36 were consolidation/reproducibility/consistency audits — the signal PROTOCOL calls out as "the additive
series has already ended." A **sprint 37 would add no new capability, no new proof, and no new audit
surface** — it would only re-verify ground already proven over the same recorded data. Per PROTOCOL: write no
`sprint-37/PROMPT.md`, and say plainly **"nothing new left for a sprint; series ends here."**

## The residual boundary (the honest, still-not-derivable frontier — unchanged)
- a **probabilistic/stochastic forecast** — the recorded band is a spread, never a CI; nothing invents a
  distribution;
- a **per-option requirement NOT unit-coupled to the recorded capacity** / an **option with no recorded
  requirement** — never invented (`deli-atcap`/`deli-deficit` prove recorded capacity alone never reaches
  RE-RANK);
- **any §6-human choice recorded data cannot machine-decide** — the re-rank is POLICY-authorized, not a
  claim of objective best.
These remain the boundary the project deliberately refuses to cross without prompt authorization (they are
capability/policy decisions, not derivations).

## The decisive prior sprint
**Sprint 32** (`capacity_rerank.py`, the capacity-constrained RE-RANK of the Q8 recommendation for the
machine as an explicit authorized POLICY step) was the last genuine capability; sprints 33/34/35/36
consolidate + re-verify it, so the one-framework two-path answer holds across the whole 22-org catalog and
is reproducible and corpus-consistent on this host. See `sprints/sprint-32/summary.md` for the capability
and `sprints/sprint-33|34|35/summary.md` for the consolidation, reproducibility, and now the
corpus-consistency-turned-complete chain.

## Green baseline / non-regression (all exit 0, real tool output)
- 19 CR demo runners (green-baseline) → ALL PASS; **20 CR demo runners** after the new one → ALL PASS
  (incl. `run_corpus_consistency_demo.py`).
- 5 CR conformances (Sprint-0 venv) + `build_all.py` + `conformance_all.py` + S5 reference demo +
  conformance + agent demo + conformance → ALL PASS.
- Engine `a60f8f71` + `capacity_rerank.py` `f7c6a185` unchanged BEFORE and AFTER; schema 34264934…/7fc38c8c;
  49 `$defs`; SPEC v0.22; `ros/` + schema + sector `configs.py` untouched; no new noun.

**Per PROTOCOL the prompt chain is complete: `sprints/sprint-36/COMPLETE.md`, NO `sprint-37/PROMPT.md`.**