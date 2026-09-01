# SPRINT 1 — PROMPT

You are Hermes Agent in a fresh session. Execute **Sprint 1 of the RelationalOS project**,
then hand off to Sprint 2. This session has **NO memory** of prior conversation — rely ONLY
on the files named below. Read files before acting; do not guess or invent.

## Context — read first, in full
- Canonical spec (the contract): `/home/rlg/relational-os/SPEC.md`  (currently **v0.17**)
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md`
- README / layout: `/home/rlg/relational-os/README.md`
- Spec release mirror (READ-ONLY): `/home/rlg/Documents/ai-relational-os-spec.md` (+ `.pdf`)
- Prior hand-off: `/home/rlg/relational-os/sprints/sprint-0/summary.md` (from Sprint 0)
- **Sprint-0 contracts you must build on:** the normative schema at
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/schema/relational-os.schema.yaml`
  (+ `.json`), the conformance validator at
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/conformance.py`, and the four gating
  surveys under `/home/rlg/relational-os/sprints/sprint-0/artifacts/surveys/`. Reuse them;
  do not re-derive.

## Task
Follow `PROTOCOL.md` exactly: **read the spec first, then plan, then execute, then update
the spec from findings, then verify DoD, then output the next sprint prompt.** You may load
the `system-specification` skill for schema/validator conventions.

## Sprint 1 scope — S1 substrate + S2 Intent/Matching minimum
Per `SPEC.md §8 Sprint 1`: "S1 substrate + S2 minimum. Identity/role resolution thin
integration + an Intent/Matching service for one role (customer) on one domain (e.g. a
quoting or triage flow). DoD: a cycle from identity → matched offer, human-verified, on the
shared ledger." The build order is self-funding: S1 is built thin as substrate only
(not a revenue service); S2 is the FIRST revenue service.

Each sub-sprint STARTS by re-reading `SPEC.md` §4/S1/S2, §5 (the chain/loop), §3.16/§3.19
(ledger/graph, identity≠authn≠authz, Disclosure), Appendix F/C (schema + URI rules), and
Sprint-0's schema + validator; then writes its own plan at
`sprints/sprint-1/work/<n>-plan.md` before executing.

**1.1 — S1 substrate (thin).** Implement the minimum for one customer role: `resolve_identity`,
`authenticate`, `authorize` (capability-based per §7B), `resolve_role`. A runnable service
(local, e.g. Python) that reads from / writes to the shared Relationship Graph + append-only
Ledger exactly as Sprint-0's schema/models define; evidence signed; RFC3339; round-trip
preserve-unknown. **DoD:** an identity→role resolution for a customer against the ledger,
validated by re-running Sprint-0's conformance validator over the new Sprint-1 instances
(exits 0) AND a new S1 check of your own (authz used per relationship, delegation honored).

**1.2 — S2 Intent/Matching (minimum, one domain).** Implement `infer_intent` + `match_offers`
(Trust-weighted per §5) for one customer domain — pick a concrete one (e.g. a quoting or
triage flow) and one fictional company. Produce ranked matches on the shared ledger so each
match is a signed Event; a human verifies before commitment (human-escalation floor only
where irreversible, §3.19/§6). **DoD:** a runnable cycle `identity → intent → matched offer
→ human-verified → on the ledger`, demonstrated end-to-end in a test/example that RUNS.

**1.3 — Ledger/graph wiring check.** Show the §5 loop writing a full S1→S2 slice: a match
event is content-addressed + signed on the Ledger, and current state (the match, its
status) lands on the Graph; Ledger=history / Graph=state not conflated (§3.16). **DoD:** the
round-trip from Graph state back to Ledger events is demonstrable and validated.

## Mandatory rules
- **Real tool output only.** Produce artifacts and RUN them; never fabricate results, file
  contents, or citations. Re-run `sprints/sprint-0/artifacts/run_conformance.py` (venv:
  `sprints/sprint-0/artifacts/.venv/bin/python`) over Sprint-0 fixtures AND any new Sprint-1
  instances to prove no regression.
- **Keep the URI cap and the frozen ontology** (§7J.11, Appendix C §C16). No new ontology
  nouns or URI schemes. Extend the schema ONLY where a genuine build finding requires it
  (additive-only; note in findings). Reuse `sprints/sprint-0/artifacts/schema/` as the source
  of truth; if you extend it, rebuild `.json` via `build_schema.py`.
- **Update `SPEC.md` from findings:** write `sprints/sprint-1/notes/findings.md` as you go;
  apply the genuinely necessary corrections to `SPEC.md` (targeted `patch`, re-verify
  section numbering, bump minor version to **0.18**, append to the Version/Review Log);
  optionally sync the release mirror. Preserve every requirement's meaning.
- **Budget:** hard ~$10/mo cap — prefer local computation, batch any web calls, keep
  prompts lean. S2 may use a local/cheap model tier (Appendix G.4) or a rule-based stand-in;
  do not spend on frontier APIs for this sprint.
- **Raymond:** clean English output, `file://` absolute paths when referring to files,
  honest "stuck/failed" over fabricated success, report status at each long step.
- Do not touch anything outside `/home/rlg/relational-os/` except reading the `~/Documents`
  mirror and the Sprint-0 artifacts.

## Exit criteria (Definition of Done)
- `sprints/sprint-1/plan.md` written first; each sub-sprint has its own `work/<n>-plan.md`.
- S1 substrate + S2 matching minimum run and produce real, verified output under
  `sprints/sprint-1/artifacts/`; Sprint-0 conformance still exits 0.
- `SPEC.md` updated for genuine findings (bumped to 0.18, log appended).
- `sprints/sprint-1/summary.md` written (what was built, verified output, open issues).
- The next sprint's self-contained prompt written at `sprints/sprint-2/PROMPT.md` AND echoed
  as your final message.

## Hand-off requirement
Your **final message** must be the complete, self-contained **Sprint 2 prompt** — the same
text you save to `sprints/sprint-2/PROMPT.md`. It must (a) state the task — per `SPEC.md §8`
Sprint 2 = Trust engine minimum: capture + verify one outcome class; compute and write
Trust; Trust visibly re-ranks S2 results (DoD: Trust demonstrably changes routing/pricing in
a test harness) — with the same read-plan-build-update-verify-handoff protocol, (b)
reference only absolute paths and the current `SPEC.md` (v0.18 by then), (c) carry the same
rules (real output, URI cap/frozen ontology, budget, clean English). Do not summarize your
own Sprint-1 work in that file — that goes in `summary.md`. The prompt must stand alone for
a session that starts with no memory.