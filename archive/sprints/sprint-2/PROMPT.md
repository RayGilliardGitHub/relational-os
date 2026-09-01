# SPRINT 2 — PROMPT

You are Hermes Agent in a fresh session. Execute **Sprint 2 of the RelationalOS project**
(the Trust engine minimum), then hand off to Sprint 3. This session has **NO memory** of
prior conversation — rely ONLY on the files named below. Read files before acting; do not
guess or invent.

## Context — read first, in full
- Canonical spec (the contract): `/home/rlg/relational-os/SPEC.md` (now **v0.18**)
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md`
- README / layout: `/home/rlg/relational-os/README.md`
- Prior hand-off: `/home/rlg/relational-os/sprints/sprint-1/summary.md` (from Sprint 1)
  and `/home/rlg/relational-os/sprints/sprint-1/notes/findings.md` (F1–F6)
- Spec release mirror (READ-ONLY): `/home/rlg/Documents/ai-relational-os-spec.md` (+ `.pdf`)
- **Sprint-0 contracts you build on:** the normative schema at
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/schema/relational-os.schema.yaml`
  (+ `.json`), `build_schema.py`, the conformance validator
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/conformance.py` +
  `run_conformance.py`, and the fixtures under
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/fixtures/`. Reuse them; do not
  re-derive.
- **Sprint-1 build you extend:** the working S1 substrate + S2 Intent/Matching service
  under `/home/rlg/relational-os/sprints/sprint-1/artifacts/` (`ros/` package, Quoteko
  quoting/triage scene, fixtures, checks, run scripts). Reuse its substrate/signing/
  ledger-graph wiring and its scene; it is the seat your Trust engine plugs into.

## Task
Follow `PROTOCOL.md` exactly: read the spec first, then plan (`plan.md` + a
`work/<n>-plan.md` per sub-sprint, written BEFORE executing), then execute, then update
the spec from findings, then verify DoD, then output the next sprint prompt. You may load
the `system-specification` skill.

## Sprint 2 scope — Trust engine minimum
Per `SPEC.md §8`: Sprint 2 = **capture + verify one outcome class; compute and write
Trust; Trust visibly re-ranks S2 results.** DoD: **Trust demonstrably changes
routing/pricing in a test harness.**

Each sub-sprint STARTS by re-reading `SPEC.md` §3.13/§3.14/§3.17 (Dispute, scoped
Trust, Claim/Evidence/verification), §5 (the Trust function + flywheel), §3.11
(Expectation), and Appendix F; `sprints/sprint-0` schema/validator; and
`sprints/sprint-1/artifacts`. Then it writes its own plan at
`sprints/sprint-2/work/<n>-plan.md` before executing.

**2.1 — S5 capture + verify (one outcome class).** Implement `capture(outcome,
provenance) → signed evidence` and `verify(evidence, axioms) → verified result` for
ONE crisp, objective outcome class in the existing Quoteko scene (e.g. "quote → job
completed on time, per a completion/anchor record"). Produce a real, signed `evidence://`
per the schema; a claim-verification against it per §3.17 (evidence supports claim X to
degree Y under procedure Z; no capital-T truth overclaim). **DoD:** a verified outcome
record, wired to a `relationship://` + `trust://` context.

**2.2 — Trust update + write.** Implement `update(Trust, evidence, weight, recency) →
Trust` per the §5 bounded/scoped equation, `T_{k+1}(c) = clamp(T_k(c) +
alpha*(outcome_k - expectation_k)*evidence_k, 0, 1)`, keyed on
`(subject, target, claim, context)` per §3.14 — NOT a single global score. Cold-start
T1 already seeded in Sprint 1 is your starting point. Compute and WRITE the updated
`trust://` to the shared Graph + a signed Ledger event. **DoD:** a Trust value changes
because of verified evidence (not arbitrarily), stays in [0,1], is relationship/context-
scoped, and is persisted.

**2.3 — Trust re-ranks S2 (the flywheel).** Re-run `match_offers` (Sprint-1's S2) after
the Trust update. A contractor whose verified good/bad outcome moved its scoped Trust
must move differently in the ranked output than before (same fit, different Trust →
different rank/score). **DoD:** a test harness shows before/after Trust and before/
after S2 ranking, and asserts the ordering changed as the equation predicts.

## Mandatory rules
- **Real tool output only.** Producing artifacts and RUNNING them is mandatory; never
  fabricate results, file contents, or citations. Re-run `run_conformance.py`
  (`sprints/sprint-0/artifacts/.venv/bin/python`) over Sprint-0 fixtures AND the Sprint-1
  fixtures AND any new Sprint-2 instances to prove no regression (exit 0). Sprint-1's
  `run_s1_conformance.py` pattern (reusing the Sprint-0 validator pointed at new
  fixtures) is the template — extend it for the Sprint-2 fixtures.
- **Keep the URI cap and the frozen ontology** (§7J.11, Appendix C §C16). No new ontology
  nouns, no new URI schemes. `trust://` `evidence://` `claim://` `expectation://`
  `outcome`/`event` already exist. Extend the schema ONLY where a genuine build finding
  requires it (additive-only; note in findings; if extended, rebuild `.json` via
  `build_schema.py`).
- **Update `SPEC.md` from findings:** write `sprints/sprint-2/notes/findings.md` as you
  go; apply genuinely necessary corrections (targeted `patch`, re-verify section
  numbering, bump minor version to **0.19**, append to the Version/Review Log);
  optionally sync the release mirror. Preserve every requirement's meaning.
- **Budget:** hard ~$10/mo cap — prefer local computation, batch web calls, keep prompts
  lean. No frontier-API spend for this sprint; the Trust equation is deterministic local
  math (§G.11: do NOT hardcode speculative weights — keep the seeded/verified evidence
  driving updates).
- **Raymond:** clean English output, `file://` absolute paths, honest "stuck/failed" over
  fabricated success, report status at each long step.
- **Single-threaded** per PROTOCOL: do all work yourself, in ONE process; do NOT use
  `delegate_task`/subagents.
- Do not touch anything outside `/home/rlg/relational-os/` except reading the
  `~/Documents` mirror and the Sprint-0/Sprint-1 artifacts.

## Exit criteria (Definition of Done)
- `sprints/sprint-2/plan.md` written first; each sub-sprint has `work/<n>-plan.md`.
- S5 capture→verify→Trust-update→re-rank run under `sprints/sprint-2/artifacts/` with real
  output; the test harness **demonstrably shows Trust changing S2 routing/pricing**.
- Sprint-0 conformance still exits 0 over all three fixture generations (Sprint-0, -1, -2).
- `SPEC.md` updated for genuine findings (bumped to 0.19, log appended).
- `sprints/sprint-2/summary.md` written (what was built, verified output, open issues).
- The next sprint's self-contained prompt written at `sprints/sprint-3/PROMPT.md` AND
  echoed as your final message.

## Hand-off requirement
Your **final message** must be the complete, self-contained **Sprint 3** prompt (per
`SPEC.md §8`, Sprint 3 = Orchestration (S3) + human floor) — the same text you save to
`sprints/sprint-3/PROMPT.md`. It must (a) state the task with the same
read-plan-build-update-verify-handoff protocol, (b) reference only absolute paths and the
current `SPEC.md` (v0.19 by then), (c) carry the same rules (real output, URI cap/frozen
ontology, budget, clean English, single-threaded). Do not summarize your own Sprint-2 work
in that file — that goes in `summary.md`. The prompt must stand alone for a session that
starts with no memory.