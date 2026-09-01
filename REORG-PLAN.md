# REORG PLAN — RelationalOS → standard layout (from DEFERRED-REORG-NOTE.md)

Status: previously DEFERRED; **now authorized by Raymond** (review + reorg + run the test suite).

## Reviewed context (current, verified 2026-09-01 — the note was Sprint-22-era, paths shifted)
The repo is not a standard Python project and has (verified just now):
- No `pyproject.toml` / setup / Makefile; root has only `SPEC.md PROTOCOL.md README.md docs/ instances/ archive/sprints/`.
- Root `docs/` is EMPTY; the real docs live in `archive/sprints/sprint-6/artifacts/docs/`.
- The canonical `ros/` package lives at `archive/sprints/sprint-5/artifacts/ros/` (9 files: bol/checks/__init__/s1/s2/s3/s4/s5/substrate).
  The `ros/` copies in `archive/sprints/sprint-1..4/` are EARLIER PARTIAL snapshots (NOT identical); sprint-5's is the complete canonical.
- `conformance.py` is a single flat validator at `archive/sprints/sprint-0/artifacts/conformance.py` (+ `run_conformance.py`).
- No root `tests/`; the reusable gate `scripts/verify.sh` lives only in the runbook skill.
- 122 tracked `.py`, 1383 tracked files; remote `git@github.com:RayGilliardGitHub/relational-os.git` (main clean & synced).
- CWD-bound footgun is NARROW: only the 8 sprint conformance scripts (`sprint-{1..5}/artifacts/run_s*_conformance.py`)
  + 2 financial scripts use a bare relative `Path("../../sprint-0/artifacts").resolve()` (cwd-bound). Every CR demo,
  `build_all.py`, `conformance_all.py`, and the sector runners are already `Path(__file__)`-anchored.
- No pytest (system or venv) and the venv has no pip → the reorg test suite must be plain-Python (stdlib + the
  Sprint-0 venv for conformance), not pytest-dependent.

## Target shape (Raymond's chosen depth: "tidy + standard roots", NOT "full src/ + hide artifacts")
```
/home/rlg/relational-os/
  pyproject.toml        NEW  declarative metadata + ruff/pytest config; package `ros` discovered at root
  ros/                  NEW  CANONICAL package = byte-copy of archive/sprints/sprint-5/artifacts/ros/ (verified identical)
  docs/                 populate with the sprint-6 docs package (00-README … QUICKSTART)
  scripts/verify.sh     bring in-tree from the runbook skill; runnable from repo root
  tests/                NEW  plain-python gate (`run_checks.py` exit 0 = green) exercising the whole build
  archive/sprints/              NARRATIVE HISTORY — kept; the 8 conformance scripts made location-independent
  instances/            UNCHANGED (sectors + contested_reality demos already __file__-anchored)
```
- `archive/sprints/` stays as narrative history (plan/work/summary/findings/PROMPT/artifacts), NOT the canonical code home.
- Do NOT delete/hide any sprint artifact.

## Hard constraints preserved
1. Green gate exit 0 from repo root AND from the original deep cwds (daily cockpit, conformance all-six,
   all sectors, all contested_reality demos, agent demo + conformance).
2. Fix the cwd-bound conformance scripts to anchor `SPRINT0` to `Path(__file__).resolve().parent` (the note's #1
   footgun) so they run from repo root; re-verify C2 instance counts UNCHANGED (156/28/35/55/174/316).
3. Keep frozen 49 `$defs`, URI cap, SPEC v0.22; schema hash `34264934…` (yaml) / `7fc38c8c` (json) unchanged;
   `ros/` canonical byte-identical to sprint-5's; `adjudication_engine.py` a60f8f7 / `capacity_rerank.py` f7c6a185
   byte-identical (untouched by reorg).
4. Sprint-0 venv for ALL conformance; plain python3 for demos.
5. Commit + verify + push only after the whole gate is green (raymond-github-maintenance flow).

## Move map / steps
- A. Canonical `ros/`: `cp -r archive/sprints/sprint-5/artifacts/ros ros`; verify FLAT-BYTE identical (sha256 on every file).
- B. `pyproject.toml`: metadata + `[tool.setuptools] packages=["ros"]` + `[tool.ruff]` + `[tool.pytest.ini_options]`
  + a `[project.optional-dependencies]` listing conformance deps (for a future pip install; not needed to run).
- C. `docs/`: copy `archive/sprints/sprint-6/artifacts/docs/*` → `docs/` (9 manuals).
- D. `scripts/verify.sh`: bring the runbook gate in-tree, make its `ROOT` default location-independent.
- E. `tests/run_checks.py`: plain-python orchestrator that runs the whole green gate from repo root (subprocess
  with correct cwds via __file__), asserts every step exit 0 + key invariants; print `RESULT: ALL PASS`.
- F. Fix 10 cwd-bound scripts (8 sprint conformance + 2 financial): replace `Path("../../sprint-0/artifacts").resolve()`
  with an `__file__`-anchored sprint-0 path. Re-run each conformance → instance counts unchanged.
- G. Full non-regression: the green gate from repo root AND from the original deep cwds; engine/rerank/ros/schema
  hashes recorded before and after.
- H. Update `instances/README.md` + this plan's doc pointers to the canonical `ros/` + `docs/` + `tests/` + `scripts/`.
- I. Commit on main; push to origin only after gate green.

## Second pass (Raymond: "do you need to go thru the instances dir and update them to reference the new structure?") — YES
The instance runners still resolved `ros` from `archive/sprints/sprint-5/artifacts` (workable but not the canonical
home). Updated **all 33 instance files** to point at the repo ROOT (canonical `ros/`):
- 29 CR/agent runners: `ROS = INSTANCES.parents[0]` (was `… / "archive/sprints/sprint-5/artifacts"`).
- `sector_scene.py`, `build_all.py`, `run_fin.py`: sys.path to repo root.
- `fin_demo.py`: FIXED an off-by-one the first pass introduced (`parents[1]`→`parents[2]` = repo root) —
  it had broken `import ros`; not caught because financial v1 is not in the original gate. Root cause caught
  because Raymond asked. Financial files (`fin_demo`, `run_fin`, `run_fin_conformance`) are now IN the gate.
- **Deliberate exception:** `capacity_rerank.py` is a FROZEN INVARIANT module (sha256 `f7c6a185…` is a
  recorded sacred byte-identity); it is NOT a runner, and it KEEPS its `S5 = …/archive/sprints/sprint-5/artifacts`
  path (that ros is byte-identical to the canonical root `ros/`, so content is unchanged). Do not edit it.
- Re-ran the full gate AFTER: **41 checks, RESULT: ALL PASS** (the first re-run caught a transient from the
  capacity_rerank edit; reverted it and the gate is green). No code references to `archive/sprints/sprint-5/artifacts`
  remain in `instances/` except capacity_rerank's frozen line.

## Not in scope (honest boundary)
- No `src/`-layout, no artifact-hiding (Raymond chose "tidy + standard roots").
- No `src/` layout / `package` subdir — canonical code home is the ROOT `ros/` + ROOT `instances/`.
- `archive/sprints/sprint-N/artifacts/ros` copies remain as unpromoted narrative snapshots; only sprint-5's is the
  origin of the canonical root `ros/`. `capacity_rerank.py` keeps its sprint-5 S5 path (frozen invariant).