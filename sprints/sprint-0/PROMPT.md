# SPRINT 0 — PROMPT

You are Hermes Agent in a fresh session. Your job is to execute **Sprint 0 of the
RelationalOS project**, then hand off to Sprint 1. This session has **NO memory** of
prior conversation — rely ONLY on the files named below. Read files before acting; do
not guess or invent.

## Context — read first, in full
- Canonical spec (the contract): `/home/rlg/relational-os/SPEC.md`  (currently v0.16)
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md`
- README / layout: `/home/rlg/relational-os/README.md`
- Spec mirror (read-only): `/home/rlg/Documents/ai-relational-os-spec.md` (+ `.pdf`)
- Prior hand-off: none (this is the first sprint). In future sprints, also read the
  prior `summary.md`.

## Task
Follow `PROTOCOL.md` exactly: **read the spec first, then plan, then execute, then
update the spec from findings, then verify DoD, then output the next sprint prompt.**
You may load the `system-specification` skill for the schema/validator conventions.

## Sprint 0 scope — deliver the implementation contract
Three sub-sprints; each starts by reading `SPEC.md` and writing its own plan at
`sprints/sprint-0/work/<n>-plan.md` before its own execution.

**0.1 — Formal schema.** Expand Appendix F into a **machine-validatable** schema for
every §3 primitive and the §7J operating objects (Case, Goal, Metric, Task,
Dependency), plus the Appendix C identity / relationship / domain-object conventions
and the §7K semantics as far as they are structural. Choose one representation
(JSON Schema + YAML anchors, or OpenAPI; it must be validatable) and put the schema
in `sprints/sprint-0/artifacts/`. Validate your own schema file syntactically.

**0.2 — Validator and fixtures.** Write a small conformance validator (Go or Python,
per Appendix G) that checks instances against the 0.1 schema. Build **executable
fixtures**: (a) the 20 interactions of Appendix E, (b) the §7L ten-question operating
loop for one chosen fictional company, (c) the Case lifecycle (OPEN→…→CLOSED with
REOPEN). These must RUN and pass. Put them in `sprints/sprint-0/artifacts/`.

**0.3 — The four committed surveys** (from `SPEC.md §7D-E` and `§8 Sprint 0`):
1. §7I data-source & licensing reality (news + social: licensed vs cost, API limits,
   T.o.S., resilient fallback e.g. GDELT). DoD: a ranked source matrix.
2. §7H jurisdiction & tax-filing set (federal/state/local, e-file, filing calendar,
   providers). DoD: verified filing-calendar seed per target jurisdiction + vendor list.
3. §7G BI report-catalog validation (three statements + management package vs
   authoritative references). DoD: validated, versioned report catalog.
4. §7I employee/customer data boundary (what sentiment data is legally/ethically
   ingestible under Consent/Disclosure, per jurisdiction). DoD: intake allow-list +
   privacy-policy skeleton.
Each survey is a written report with real citations, saved under
`sprints/sprint-0/artifacts/surveys/`. **This is real research — use web_search /
extraction; cite sources; do not invent.**

## Mandatory rules
- **Single-threaded. Do all work yourself, sequentially, in this one process.** Do NOT
  use `delegate_task`/subagents and do NOT hand off any stage to a child agent — they
  have repeatedly failed. Sub-sprints are phases YOU execute directly, in order,
  never parallel-farmed.
- **Real tool output only.** Produce artifacts and RUN them; cite sources. Never
  fabricate results, file contents, or citations.
- **Keep the URI cap and the frozen ontology** (§7J.11 / Appendix C §C16). Do NOT add
  new ontology nouns or URI schemes. Update the spec ONLY where a genuine finding from
  the build requires a correction.
- **Update `SPEC.md` from findings:** write `sprints/sprint-0/notes/findings.md` as you
  go, then apply the genuinely necessary corrections to `SPEC.md` (patch, renumber,
  bump minor version to 0.17, append to the Version/Review Log). Optional: sync the
  `.md`/`.pdf` mirror to `/home/rlg/Documents/`.
- **Budget:** the user has a hard ~$10/mo cap. Keep tool/API use lean; prefer local
  computation; batch web calls.
- **Raymond:** clean English output, `file://` absolute paths when referring to files,
  honest "stuck/failed" over fabricated success, report status at each long step.
- Do not touch anything outside `/home/rlg/relational-os/` except reading the `~/Documents`
  mirror.

## Exit criteria (Definition of Done)
- `sprints/sprint-0/plan.md` written first; each sub-sprint has its own `work/<n>-plan.md`.
- Schema validatable (0.1), validator + fixtures pass when run (0.2), four surveys
  with real citations (0.3) — all under `sprints/sprint-0/artifacts/`.
- `SPEC.md` updated to reflect genuine findings, version bumped, log appended.
- `sprints/sprint-0/summary.md` written (what was built, verified output, open issues).
- The next sprint's self-contained prompt written at `sprints/sprint-1/PROMPT.md` AND
  echoed as your final message, referencing only absolute paths and the current `SPEC.md`.

## Hand-off requirement
Your **final message** must be the complete, self-contained **Sprint 1 prompt** — the
same text you save to `sprints/sprint-1/PROMPT.md`. It must (a) state the task (Sprint 1 =
S1 substrate + S2 Intent/Matching minimum, per `SPEC.md §8`) with the same
read-plan-build-update-verify-handoff protocol, (b) reference only absolute paths and
the current `SPEC.md`, and (c) require the same rules (real output, URI cap/frozen
ontology, budget, clean English). Do not summarize your own sprint in that file — that
goes in `summary.md`. The prompt must stand alone for a session that starts with no
memory.