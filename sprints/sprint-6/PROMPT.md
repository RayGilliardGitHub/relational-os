# SPRINT 6 — PROMPT  (Documentation package: operations · user · system · audit · BI)

You are Hermes Agent in a fresh session. Execute **Sprint 6 of the RelationalOS project**:
produce a **first-class documentation package** for the now-complete system — setup,
running, producing the audits, and producing the BI reports, i.e. an **operations manual,
a user manual, and a system manual** (expand into whatever a real company would hand an
onboarding operator, an owner, and an engineer). This session has **NO memory** of prior
conversation — rely ONLY on the files named below. Read files before acting; do not guess
or invent. **Everything you document MUST be real: run the actual runners and capture their
real output; do not write a command you have not executed.**

## Context — read first, in full
- Canonical spec (the contract): `/home/rlg/relational-os/SPEC.md` (currently **v0.22**)
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md`
- README / layout: `/home/rlg/relational-os/README.md`
- Project closing hand-off: `/home/rlg/relational-os/sprints/COMPLETE.md`
- Prior sprint summary: `/home/rlg/relational-os/sprints/sprint-5/summary.md` and findings
  `/home/rlg/relational-os/sprints/sprint-5/notes/findings.md`
- The **working system is what you document** (all real, all exit 0):
  - Sprint-0 contract: schema + `conformance.py` + fixture generation under
    `/home/rlg/relational-os/sprints/sprint-0/artifacts/` (the 49-`$defs` JSON Schema,
    the EBNF grammar `schema/relational-os-lifecycle.ebnf`, the venv
    `schema/../.venv/`, the 156 fixtures, the four surveys under `surveys/`).
  - The `ros/` package + runners: `/home/rlg/relational-os/sprints/sprint-5/artifacts/`
    (substrate Graph+Ledger, services S1–S5, the Business Operating Layer `ros/bol.py`,
    `run_s5_demo.py`, `run_s5_conformance.py`) — and the same layout at `sprint-1/-2/-3/-4`.
  - The produced outputs: `graph/current-state.json`, `fixtures/ledger/ledger-quoteko.json`,
    and the cockpit report `sprint-5/artifacts/reports/cockpit.md` + `cockpit.json`.
- Spec release mirror (READ-ONLY reference for cross-checks): `/home/rlg/Documents/ai-relational-os-spec.md` (+ `.pdf`).

## What Sprint 6 IS and is NOT
- **IS:** a documentation sprint that turns the verified S0–S5 chain into a package a real
  business could hand to (a) an operator who must set it up and run it, (b) an owner who
  reads the cockpit each morning, (c) an engineer who must keep the integrity audits and BI
  reports coming. It is a **first-class business deliverable**, not a notes-dump.
- **IS NOT:** new system build, new schema, new URI/nouns, or a re-implementation. Do NOT
  touch the schema/`ros/` code. This sprint produces **documentation artifacts only** and
  must **verify** every command it publishes by running it.
- Honour the **URI cap / frozen ontology** (§7J.11/§C16) — this is prose; no new nouns.

## Task — produce the documentation package under `sprints/sprint-6/artifacts/docs/`
Write a set of manuals, with a top-level `00-README.md` index that tells a reader which
document to open and in what order. Reasonable structure (expand/merge freely for a
first-class feel — an appendix/glossary, quickstart card, and troubleshooting are
encouraged):

1. **00-README.md — index.** Purpose, who each manual is for, reading order, what the
   system is in one page, and a quick-start box (3 commands to stand it up and see the
   cockpit).

2. **01-system-manual.md — the system.** Architecture and data model for an engineer:
   Substrate (Graph=state / Ledger=history, content-addressed + signed, §3.16), the S1–S5
   service chain, the Business Operating Layer (Case/Goal-Metric/Task/Dependency +
   Exception/Priority as derived fields), the URI cap and frozen ontology, the schema +
   conformance validator + EBNF, and the technology truth (deterministic local Python,
   no frontier-API spend, §G.11). Map every file/artifact to what it is.

3. **02-setup.md — operations: set up the system.** Prerequisites (Python 3.12, the
   Sprint-0 venv and its `jsonschema`/`referencing`/`yaml` dependencies), how to create the
   venv if missing, how to verify the install (run the conformance runner), and the full
   directory layout with a file-by-file description.

4. **03-run.md — operations: run the system.** Exactly how to run each demo runner
   (`run_s{5..1}_demo.py`) and each conformance runner (`run_s{5..1}_conformance.py`), with
   the Sprint-0 venv interpreter for conformance; expected exit codes and the meaning of
   the output; how to regenerate `graph/current-state.json` and the fixtures; and how to
   run the **daily cockpit** (`python3 run_s5_demo.py` → `reports/cockpit.md`).

5. **04-audit.md — produce the audits.** What an integrity audit is in this system and the
   commands that actually produce it: the Ledger hash-chain + signature verify
   (`Ledger.verify()`), the **full-state round-trip** (whole Graph rebuilds from the whole
   Ledger), and the conformance checks C1–C5 (schema validity, instance/scheme/RFC-3339,
   ledger chain, round-trip preserve-unknown, state-machine legality). Show the command(s)
   and a representative real PASS output. **Be honest:** the §7F continuous audit *service*
   and the audit-finding remediation queue are spec'd but NOT built in Sprints 0–5 — state
   clearly that today's integrity audit IS the conformance + round-trip + ledger-verify
   harness (map each §7F.1 check class to the concrete check that covers it today, and mark
   the per-entity continuous auditor as future deployment).

6. **05-bi-reports.md — produce the BI reports.** What BI means here and the commands that
   produce it today: the deterministic ledger projections in `ros/bol.py`
   (`project_on_time`, `project_settled_value`, `project_trust`), the business-health panel,
   and `reports/cockpit.md` (health table, prioritized attention, §7L ten answers). Map the
   §7G.1–7G.6 report catalog to what exists today (cockpit health/attention) vs what needs
   the production BI warehouse (P&L/balance-sheet/cash-flow, §7G.1) — mark the latter future.
   Include the real table/cockpit output.

7. **06-user-manual.md — the owner's manual.** The §7L ten morning questions and how to read
   them in the cockpit; how an exception→case→task→verified-outcome→learning cycle looks and
   where it appears; what to do with a recommendation that "carries the authority it
   requires"; how to treat do-nothing as a real option; human-oversight discipline (§6 floor).

8. **Appendix — troubleshooting & glossary.** Common failure modes and their fixes (missing
   venv / deps, a "FAIL" in a conformance check meaning a real regression not a doc typo,
   how to re-run cleanly), and a glossary of key terms + the URI catalog summary.

## Mandatory rules
- **Real tool output only.** For EVERY command you document, actually RUN it in this session
  and capture its output/exit code. Do NOT write a command you have not executed. Never
  fabricate output, file contents, or citations. Run conformance with the Sprint-0 venv
  interpreter (`sprints/sprint-0/artifacts/.venv/bin/python`), demos with plain `python3`.
- **Ground every claim.** Any statement about what the system does must trace to a SPEC
  section, a fixture, a runner's output, or an artifact you opened. Cite `SPEC.md §X` where
  relevant.
- **Honest separation of EXISTS vs SPEC'D-NOT-BUILT.** The build delivered a deterministic
  local chain + the operating layer. The §7F audit *service*, §7G BI *warehouse*, §7H
  external gateway, §7E frontend/IoT, real graph/ledger store, confidential-compute
  anchoring, and the §8 Phase-B backlog are spec'd but NOT built — mark them explicitly as
  future deployment everywhere they are implied, and wherever possible state what to run
  *today* as the working analogue.
- **Single-threaded** per PROTOCOL — all work yourself, ONE process, NO `delegate_task`/
  subagents.
- **Do not touch anything outside `/home/rlg/relational-os/`** except reading the
  `~/Documents` mirror. Do NOT modify the schema, the `ros/` code, or the fixtures.
- This is a **documentation** sprint: `SPEC.md` should generally NOT change. If the
  documentation surfaces a genuine spec error, fix it with a targeted `patch`, keep version
  **0.22**, and add a short Version/Review Log line noting the correction. Do not bump the
  version for a docs sprint.
- **Budget:** hard ~$10/mo cap — local computation only, no frontier-API spend.
- **Raymond:** clean English output, `file://` absolute paths, honest "stuck/failed" over
  fabricated success, report status at each long step.

## Definition of Done (exit criteria)
- `sprints/sprint-6/plan.md` written FIRST (objectives, the doc-set breakdown, DoD), then a
  `sprints/sprint-6/work/` plan (or per-document notes) written before drafting. Planning
  always precedes execution.
- `sprints/sprint-6/artifacts/docs/` contains the complete package: `00-README.md` index +
  the manuals above (or an equivalent first-class set), each **verified**: the documented
  commands were actually run and their real output embedded.
- `sprints/sprint-6/artifacts/docs/QUICKSTART.md` — a one-page "stand it up in 3 commands and
  read the cockpit" card, verified by running it.
- An `AUDIT.md` and `BI.md` (or the equivalent in the set) that each give a concrete,
  runnable procedure with real output AND an honest "what is future" note.
- SPEC correctness held: schema and `ros/` untouched; any genuine corrections to `SPEC.md`
  applied as targeted patches and logged (version stays 0.22).
- `sprints/sprint-6/summary.md` written — what was produced, the verified commands/outputs,
  and the decided future-deployment boundaries.
- Point the README index of the project (`/home/rlg/relational-os/README.md`) at the new
  docs package (add a short "Documentation" section; do not remove the sprint layout).

## Hand-off requirement
Your **final message** must summarize the documentation package (what was produced, the
verified setup/run/audit/BI commands) and point to `sprints/sprint-6/summary.md` + the
package index `sprints/sprint-6/artifacts/docs/00-README.md` (absolute paths). No next-sprint
prompt is required (this completes the project's story with a user-facing manual).