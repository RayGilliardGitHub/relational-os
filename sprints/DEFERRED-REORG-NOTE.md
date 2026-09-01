# Planned sprint — reorganize project directories into a standard layout

**Status: EXECUTED 2026-09-01.** Raymond lifted the deferral; the reorg was carried out per
`REORG-PLAN.md` and proven green by `tests/run_checks.py` (38 checks, RESULT: ALL PASS, from repo
root) + `scripts/verify.sh` (ALL GREEN from a deep cwd). Canonical `ros/` now at repo root,
`docs/` + `tests/` + `scripts/` populated, `pyproject.toml` added, and the 8 CWD-bound sprint
conformance scripts + `fin_demo.py` re-anchored to `Path(__file__)` (instance counts unchanged:
156/28/35/55/174/316). This note is now a record of why the standard roots were added.

**Historical status: DEFERRED by Raymond.** Not to be authored/executed now.
Author it toward the END of the current sprint run (after ~5 more sprints from Sprint 22, i.e.
around sprint-28+), when the current build line is effectively complete.

Trigger recalled from conversation (Sprint 22 hand-off): "you need to add a sprint to organize the
project dirs into a more standard configuration." Raymond's ordering decision: finish the next ~5
sprints, then put the reorg at the end.

## Why it's needed (verified structure, Sprint 22)
The repo is not a standard Python project. Confirmed:
- Root has NO `pyproject.toml` / setup / Makefile; only `SPEC.md`, `PROTOCOL.md`, `README.md`.
- `docs/` at root is EMPTY (0 tracked files); the real docs live deep in
  `sprints/sprint-6/artifacts/docs/`.
- The canonical `ros/` package lives at `sprints/sprint-5/artifacts/ros/` and is COPY-DUPLICATED into
  every earlier sprint (`sprint-{1..5}/artifacts/ros/` — 7 copies tracked). No canonical package.
- No `tests/` (conformance is a single flat `sprints/sprint-0/artifacts/conformance.py` + per-instance
  conformance_* scripts).
- `scripts/` at root is absent; the reusable gate `scripts/verify.sh` lives only in the skill
  `~/.hermes/skills/software-development/relational-os-runbook/scripts/verify.sh`.
- 1063 tracked files; 106 `.py` (35 in instances/, 71 in sprints/); runner/demo copies accumulate
  across sprint dirs.

## Target shape (Raymond's chosen depth at ask time: "reorg to standard configuration")
- Add `pyproject.toml` with metadata + tool config (ruff/pytest) + a canonical `ros/` package.
- Promote `ros/` (+ `sector_scene.py`, `configs.py`, `build_all.py`, `conformance_all.py`) to a
  canonical, importable location so runners don't reach into `sprints/<N>/artifacts/`.
- Populate root `docs/`, `tests/`, `scripts/` (bring `verify.sh` in-tree).
- Keep `sprints/` as NARRATIVE HISTORY (plan/work/summary/findings/PROMPT per sprint + artifacts) —
  NOT the canonical code home.
- Do NOT discard/hide sprint artifacts (depth choice: "tidy + standard roots", not "full src/ layout +
  hide artifacts").

## Hard constraints to preserve (footguns — from the runbook + skill):
- Every `run_*_conformance.py`/instance runner that reaches a sibling `../../sprint-0/artifacts`
  relative path is CWD-bound → after relocating ros/conformance, FIX them to anchor to
  `Path(__file__).resolve().parent` and re-run from a few cwds to prove location-independence.
- `Path.parents[N]` off-by-one (repo root = `parents[0]` when one dir under it).
- Sprint-0 venv interpreter `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python`
  for ALL conformance (pure python3 for demos). The venv has no bin/pip but deps are in site-packages;
  `ros/` is pure stdlib.
- The repo is the PUBLIC GitHub mirror `RayGilliardGitHub/relational-os` (origin remote confirmed).
  Relocating files is a tracked-tree change → the reorg commit + full non-regression must be verified
  before any push (`raymond-github-maintenance` skill for the publish flow).
- Keep 49 `$defs` / URI cap / SPEC v0.22; `res/` etc. untouched; schema hash `7fc38c8c…` unchanged.
- Whatever moves, the canonical green gate: `run_s5_demo.py` + `run_s5_conformance.py` (all six gens),
  `instances/build_all.py` + `conformance_all.py`, all contested_reality demos + 16-label
  conformance_adjudication, agent demo + conformance — all exit 0 from repo root AND from a deep cwd.

## When to author it
When ~5 more sprints are done (i.e. around writing the sprint that precedes the reorg), a fresh
session should write `sprints/sprint-<N>/PROMPT.md` following this brief with the THEN-current
verified structure (paths in this note are Sprint-22-era and may have shifted). Do not author it now.