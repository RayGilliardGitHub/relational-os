# contested_reality — the adjudication / decision engine

The **system** is a small engine library; everything `run_*_demo.py` / `conformance_*.py` here is
evidence/demo/test tooling that drives it. This README is the boundary marker.

## SYSTEM (the engine — importable library, not demo code)
- `adjudication_engine.py` — the §7L decision engine (reconcile rules, cockpit Q1–Q10, Q7/Q8 constraint
  blocks). Recorded identity: sha256 head-8 `a60f8f71`.
- `adjudication_configs.py` — every org is DATA here (config per org).
- `capacity_rerank.py` — the POLICY-authorized capacity-constrained re-rank. **Frozen invariant** (sha256
  head-8 `f7c6a185`); do not edit.
- `decision_learning.py`, `reconcile_learning.py`, `tradeoff_model.py` — supporting library modules.

## DEMO / TEST RUNNERS (NOT part of the engine API)
- every `run_*.py` (marked with a `# === DEMO / TEST RUNNER …` header) — drives the engine over orgs,
  asserts, emits reports under `artifacts/`.
- `conformance_{adjudication,dispute,interest,lifecycle,tradeoff}.py` — the C1–C5 validation gates.

## Depends on
The canonical `ros/` package at the repo ROOT (promoted from `archive/sprints/sprint-5/artifacts/ros/` by the
reorg; byte-identical). Runners resolve `ros` from the repo root.

## Reproducibility note (this whole surface is deterministic local Python, ~$0)
The one-framework two-path decision surface over the 22-org catalog is re-verified by
`run_reproducibility_demo.py` + `run_corpus_consistency_demo.py`; the series ended at Sprint 36
(`archive/sprints/sprint-36/COMPLETE.md`). See `docs/` for the engine documents.