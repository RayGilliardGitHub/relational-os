# SPRINT 6 — PLAN (Documentation package)

**Project:** RelationalOS | **Spec:** v0.22 (unchanged) | **Scope:** documentation artifacts only
**Summary:** Turn the verified S0–S5 chain into a first-class operations / user / system
manual package a real business can hand to an operator, an owner, and an engineer.
**Constraint:** every documented command is actually run; real output embedded; schema +
`ros/` code + fixtures untouched; single-threaded; ~$0 local computation (+ ~$10 cap).

## Objectives
1. Produce the manual set under `sprints/sprint-6/artifacts/docs/`:
   - `00-README.md` — index + one-page "what the system is" + reading order + quick start
   - `01-system-manual.md` — architecture & data model for an engineer
   - `02-setup.md` — operations: prerequisites, venv, verify install, full layout
   - `03-run.md` — operations: how to run every demo + conformance runner + the daily cockpit
   - `04-audit.md` — produce the integrity audits (ledger verify, round-trip, conformance C1–C5)
   - `05-bi-reports.md` — produce the BI reports (ledger projections, health panel, cockpit)
   - `06-user-manual.md` — the owner's manual (§7L ten questions, human-oversight discipline, do-nothing)
   - `07-troubleshooting.md` — appendix: failure modes + glossary + URI catalog summary
   - `QUICKSTART.md` — one-page "stand it up in 3 commands and read the cockpit" card
2. Verify EVERY command by running it and capturing real output/exit codes.
3. Honest spec-vs-built separation (§7F audit service, §7G BI warehouse, §7H gateway,
   §7E frontends, §8 Phase B = future deployment; today's working analogues stated).
4. Write `sprints/sprint-6/summary.md`; add a short Documentation section to the project
   `README.md`; do not change the sprint layout.
5. SPEC.md stays at v0.22 (docs sprint). Correct any genuine spec error as a targeted
   patch with a Version/Review Log note — none expected.

## Doc-set breakdown & reading order
Index (`00-README.md`) directs: operator → `02-setup` → `03-run` → `04-audit`; owner →
`06-user-manual` + `05-bi-reports`; engineer → `01-system-manual` → `04-audit` → `05-bi-reports`.
Everyone starts at `QUICKSTART.md`.

## Who each manual is for
- **System manual (01):** engineer / architect — the S1–S5 chain, substrate (Graph=state /
  Ledger=history, content-addressed + signed, §3.16), BOL (Case/Goal-Metric/Task/Dependency +
  derived Exception/Priority), URI cap + frozen ontology, schema + conformance + EBNF,
  technology truth (deterministic local Python, no frontier spend, §G.11). Map every file.
- **Setup (02):** operator — Python 3.12, Sprint-0 venv + deps (jsonschema/referencing/yaml),
  create-if-missing, verify install (run conformance), full directory layout file-by-file.
- **Run (03):** operator — each demo & conformance runner (with the venv interpreter for
  conformance), expected exit codes + meaning, regenerate `graph/current-state.json` +
  fixtures, the daily cockpit (`python3 run_s5_demo.py` → `reports/cockpit.md`).
- **Audit (04):** auditor/engineer — the real integrity audit today = conformance C1–C5 +
  `Ledger.verify()` hash-chain/signature + full-state round-trip (Graph rebuilds from Ledger).
  Map every §7F.1 check class to the concrete check that covers it today; mark per-entity
  continuous auditor as future deployment.
- **BI (05):** owner/analyst — BI today = deterministic ledger projections in `ros/bol.py`
  (`project_on_time`, `project_settled_value`, `project_trust`), business-health panel,
  `reports/cockpit.md` (health table, prioritized attention, §7L ten answers). Map §7G.1–.6
  catalog to what exists today vs what needs the production warehouse (P&L/BS/cash-flow =
  future). Embed the real table/cockpit output.
- **User (06):** owner — §7L ten morning questions and how to read them in the cockpit;
  exception→case→task→verified-outcome→learning cycle; a recommendation that "carries the
  authority it requires"; do-nothing as a real option; human-oversight discipline (§6 floor).
- **Troubleshooting (07):** operator — missing venv/deps, a FAIL = real regression not a doc
  typo, re-run cleanly; glossary + URI catalog summary.

## Execution sequence (one thread)
1. Read files (done): SPEC.md §3.16/§7B–§7L/§8/§F/§G.11/§C16, PROTOCOL, COMPLETE.md,
   S5 summary+findings, README, `ros/` sources, runners, conformance.py, substrate.py.
2. Write `plan.md` (this) + `work/1-vocab.md` (working notes: real commands + expected output
   template + file map) BEFORE drafting.
3. Run every command, capture output/exit codes (conformance with Sprint-0 venv interpreter;
   demos with plain `python3`). Save capture files under `work/` for embedding.
4. Draft the doc set into `artifacts/docs/`, embedding real output; verify each stated command
   ran.
5. Write `summary.md`; patch project `README.md` with a Documentation section.
6. Verify Definition of Done (below); final hand-off message with absolute paths.

## Definition of Done (exit criteria)
- `plan.md` written FIRST; `work/` notes written before drafting.
- `sprint-6/artifacts/docs/` complete: `00-README.md` + manuals 01–07 + `QUICKSTART.md`,
  each command verified by real run with output embedded.
- `QUICKSTART.md` is a one-page 3-command stand-up card, verified by running it.
- `04-audit.md` and `05-bi-reports.md` give concrete runnable procedures with real output AND
  an explicit "what is future" note.
- SPEC held at v0.22; schema + `ros/` code + fixtures untouched.
- `sprint-6/summary.md` written (produced, verified commands/outputs, future-deployment
  boundaries).
- Project `README.md` points at the docs package (added Documentation section; sprint layout
  intact).

## Exit criteria (gate to consider sprint done)
- `find sprint-6 -path '*/artifacts/docs/*'` lists all 9 files.
- README has the Documentation section.