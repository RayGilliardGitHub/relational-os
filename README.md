# RelationalOS — development workspace

An organizational operating system: a chain of integrated services + a business
operating layer, specified formally and built sprint by sprint.

## Read these first
- `SPEC.md` — the working specification (currently **v0.22**). **This is the contract.**
- `PROTOCOL.md` — the sprint lifecycle every session follows.
- `docs/` — the verified manual package (a copy also stays at
  `docs/` as narrative history); `ros/` — canonical package;
  `tests/run_checks.py` + `scripts/verify.sh` — the green gate.

Master/mirror (do **not** edit in place — it is synced from this workspace):
`/home/rlg/Documents/ai-relational-os-spec.md` and `ai-relational-os-spec.pdf`

## How a sprint runs
Each sprint runs in a **fresh Hermes `/new` session** with **no memory** of prior
conversations. The session is fed a self-contained prompt by its absolute path:
A `/new` — paste the prompt file's contents into the fresh session, or reference it and
the session will read it from disk.

```
sprints/sprint-0/PROMPT.md   ← you are here
sprints/sprint-1/             ← Sprint 0 will write PROMPT.md here
sprints/sprint-2/             ← Sprint 1 will write PROMPT.md here
```

Each sprint prompt is self-contained: it tells the fresh session exactly what to
read (`SPEC.md` + `PROTOCOL.md`), what to produce (a `plan.md`, then sub-sprint
plans), how to update the spec from findings, how to verify its Definition of Done,
and — at the end — to write the next sprint's `PROMPT.md`.

## Directory layout
```
relational-os/
  README.md          ← this file
  PROTOCOL.md        ← sprint lifecycle (mandatory, every sprint)
  SPEC.md            ← working specification (v0.22)
  pyproject.toml     ← python package metadata (canonical `ros` package; ruff/pytest config)
  ros/               ← CANONICAL importable package (byte-identical to sprint-5's ros, the origin)
  docs/              ← the verified manual package (Sprint 6)
  scripts/verify.sh  ← quick green/red gate (daily cockpit + conformance-all-six)
  tests/run_checks.py← the full green-gate test suite (exit 0 = ALL PASS), run from any cwd
  instances/         ← sector instances (12 Appendix-B families) + contested_reality + agent demo
  sprints/
    sprint-N/
      PROMPT.md      ← self-contained prompt for this sprint (read first)
      plan.md        ← plan this sprint writes (sub-sprints: work/<n>-plan.md)
      work/          ← per sub-sprint plans + scratch
      notes/         ← findings.md (feeds spec updates)
      artifacts/     ← schema, validator, fixtures, reports produced here (narrative history)
      summary.md     ← written at sprint end
```
The canonical spec lives here (`SPEC.md`). When a sprint changes it, optionally sync
the `.md`/`.pdf` mirror into `/home/rlg/Documents/`.

## System code vs demo/test runners (know which is which)
The real system is a small, importable library; everything else in this repo is a demo or a
test runner that drives it. **Do not confuse a runner with the system.**

| Kind | Files | What it is |
|---|---|---|
| **SYSTEM (library)** | `ros/` (repo root) | The operating layer services: `substrate`, `s1`–`s5`, `bol`, `checks`. |
| **SYSTEM (engine)** | `instances/contested_reality/{adjudication_engine,adjudication_configs,capacity_rerank,decision_learning,reconcile_learning,tradeoff_model}.py` · `instances/agent_demo/agent_adapter.py` | The adjudication/decision engine + the agent's Ollama client. |
| **DEMO/TEST runners** | every `run_*.py` · `conformance_*.py` · `build_all*.py` · `tests/run_checks.py` · `scripts/verify.sh` | Drive the engine over orgs, assert, emit reports/artifacts, run the green gate. Marked with a `# === DEMO / TEST RUNNER …` header. Not part of the engine API. |

Rule of thumb: if you only want the system, read `ros/` + the 7 engine files above. Everything
named `run_*` or `conformance_*` is evidence/demo tooling.

## Documentation
The finished S1→S5 system is documented in a verified manual package (Sprint 6). Primary
copy at the repo root `docs/`; the identical Sprint-6 narrative copy stays at
`docs/`:
- Index & reading order: `docs/00-README.md`
- Quick-start (3 commands to stand up + read the cockpit): `docs/QUICKSTART.md`
- Operator — setup / run: `docs/02-setup.md`, `docs/03-run.md`
- Engineer — system / audit: `docs/01-system-manual.md`, `docs/04-audit.md`
- Owner — BI / user manual: `docs/05-bi-reports.md`, `docs/06-user-manual.md`
- Appendix — troubleshooting & glossary: `docs/07-troubleshooting.md`
- **Green gate / test suite:** `python3 tests/run_checks.py` (full build; exit 0 = ALL PASS)
  or `bash scripts/verify.sh` (daily cockpit + conformance-all-six, quick).
- **Multi-sector instances** (one per SPEC Appendix B family, all conformance-clean): `instances/README.md`
  + builder `instances/sector_scene.py`, configs `instances/configs.py`, build `instances/build_all.py`,
  conformance `instances/conformance_all.py`.
- **Branding component (Sprint 7, built):** each instance carries a per-company brand
  (About/marketing/FAQ/design language) as additive `brand` fields on the company `org://`
  actor and renders it into generated reports + a per-instance `branding.md`. Details:
  `instances/README.md` and `docs/01-system-manual.md §5.1`
  (`sprints/sprint-7/PROMPT.md` was its build prompt).
- **Contested-reality engine (Sprints 9–10, built):** `instances/contested_reality/` reasons
  about contested human reality, not just records it — Fact/Claim/Determination separation,
  the inviolable **UNRESOLVED** outcome, and Trust-safety for weak/conflicting evidence
  (Sprint 9, disputed-fact), extended to a genuine **conflicting-interest** case — the
  remote-work employee↔manager conflict under a shared 30-min SLA + staffing floor — with
  the shared constraint, deterministic conflict detection, a defensible (conditional)
  determination, an **appeal** re-adjudicated by a higher authority, and the preserved signed
  authority chain (Sprint 10). All additive fields on existing primitives; NO new noun, NO
  schema edit, 49 `$defs` intact, SPEC stays v0.22. Details: `instances/contested_reality/docs/`.
  (`sprints/sprint-10/PROMPT.md` was the Sprint 10 build prompt.)