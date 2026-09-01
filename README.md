# RelationalOS — development workspace

An organizational operating system: a chain of integrated services + a business
operating layer, specified formally and built sprint by sprint.

## Read these first
- `SPEC.md` — the working specification (currently **v0.22**). **This is the contract.**
- `PROTOCOL.md` — the sprint lifecycle every session follows.
- `docs/` — supporting research and reference material.

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
  docs/              ← research & reference
  sprints/
    sprint-N/
      PROMPT.md      ← self-contained prompt for this sprint (read first)
      plan.md        ← plan this sprint writes (sub-sprints: work/<n>-plan.md)
      work/          ← per sub-sprint plans + scratch
      notes/         ← findings.md (feeds spec updates)
      artifacts/     ← schema, validator, fixtures, reports produced here
      summary.md     ← written at sprint end
```
The canonical spec lives here (`SPEC.md`). When a sprint changes it, optionally sync
the `.md`/`.pdf` mirror into `/home/rlg/Documents/`.

## Documentation
The finished S1→S5 system is documented in a verified manual package (Sprint 6):
- Index & reading order: `sprints/sprint-6/artifacts/docs/00-README.md`
- Quick-start (3 commands to stand up + read the cockpit): `sprints/sprint-6/artifacts/docs/QUICKSTART.md`
- Operator — setup / run: `sprints/sprint-6/artifacts/docs/02-setup.md`, `…/03-run.md`
- Engineer — system / audit: `sprints/sprint-6/artifacts/docs/01-system-manual.md`, `…/04-audit.md`
- Owner — BI / user manual: `sprints/sprint-6/artifacts/docs/05-bi-reports.md`, `…/06-user-manual.md`
- Appendix — troubleshooting & glossary: `sprints/sprint-6/artifacts/docs/07-troubleshooting.md`
- **Multi-sector instances** (one per SPEC Appendix B family, all conformance-clean): `instances/README.md`
  + builder `instances/sector_scene.py`, configs `instances/configs.py`, build `instances/build_all.py`,
  conformance `instances/conformance_all.py`.
- **Branding component (Sprint 7, built):** each instance carries a per-company brand
  (About/marketing/FAQ/design language) as additive `brand` fields on the company `org://`
  actor and renders it into generated reports + a per-instance `branding.md`. Details:
  `instances/README.md` and `sprints/sprint-6/artifacts/docs/01-system-manual.md §5.1`
  (`sprints/sprint-7/PROMPT.md` was its build prompt).