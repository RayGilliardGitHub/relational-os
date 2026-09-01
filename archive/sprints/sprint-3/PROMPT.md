# SPRINT 3 — PROMPT

You are Hermes Agent in a fresh session. Execute **Sprint 3 of the RelationalOS project**
(the S3 Orchestration minimum + human floor), then hand off to Sprint 4. This session has
**NO memory** of prior conversation — rely ONLY on the files named below. Read files
before acting; do not guess or invent.

## Context — read first, in full
- Canonical spec (the contract): `/home/rlg/relational-os/SPEC.md` (now **v0.19**)
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md`
- README / layout: `/home/rlg/relational-os/README.md`
- Prior hand-off: `/home/rlg/relational-os/sprints/sprint-2/summary.md` (from Sprint 2)
  and `/home/rlg/relational-os/sprints/sprint-2/notes/findings.md` (F1–F3)
- Spec release mirror (READ-ONLY): `/home/rlg/Documents/ai-relational-os-spec.md` (+ `.pdf`)
- **Sprint-0 contracts you build on:** the normative schema at
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/schema/relational-os.schema.yaml`
  (+ `.json`), `build_schema.py`, the conformance validator
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/conformance.py` +
  `run_conformance.py`, and the fixtures under
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/fixtures/`. Reuse them; do not
  re-derive.
- **Sprint-1 build you extend:** the S1 substrate + S2 Intent/Matching service under
  `/home/rlg/relational-os/sprints/sprint-1/artifacts/` (`ros/` package, Quoteko
  quoting/triage scene, fixtures, checks, run scripts). Reuse its substrate/signing/
  ledger-graph wiring and its scene.
- **Sprint-2 build you extend:** the S5 Trust engine under
  `/home/rlg/relational-os/sprints/sprint-2/artifacts/` (`ros/s5.py`: capture/verify/
  update/write + flywheel re-rank, plus `s5_demo.py`/`run_s2_demo.py`/`run_s2_conformance.py`
  and the `/fixtures` with the updated, scoped `trust://`). **Copy the Sprint-2 `ros/`
  package into your Sprint-3 artifacts (not a git import)**, or set `PYTHONPATH` to include
  the Sprint-2 `artifacts` dir, so the S3 orchestration can consume the running S5 loop.

## Task
Follow `PROTOCOL.md` exactly: read the spec first, then plan (`plan.md` + a
`work/<n>-plan.md` per sub-sprint, written BEFORE executing), then execute, then update
the spec from findings, then verify DoD, then output the next sprint prompt. You may load
the `system-specification` skill.

## Sprint 3 scope — Orchestration (S3) + human floor
Per `SPEC.md §8` (Sprint 3) and `§5`/`§6`/`§7B`: **commit → execute with an agent fleet
across the routing seam; irreversible actions escalate to a human.** DoD: **a full
S1→S5 cycle on one relationship, end-to-end, with signed evidence at each step.**

Each sub-sprint STARTS by re-reading `SPEC.md` §4 (S3 Orchestration), §6 (routing seam +
human-escalation floor, LEVEL A normative), §5 (integration loop: identity→intent→offer→
commitment→execute→outcome→evidence→trust→**re-ranks S2**), §3.4/§7B (authority/delegation,
capability-based authz, revocation), §3.12 (Decision), and §3.16/§7C (Ledger=history /
Graph=state); then `sprints/sprint-0` schema/validator; and `sprints/sprint-1/artifacts`
and `sprints/sprint-2/artifacts`. Then it writes its own plan at
`sprints/sprint-3/work/<n>-plan.md` before executing.

**3.1 — S3 commit→execute (one relationship).** Implement the orchestration hand-off
that takes the Sprint-2 result (a ranked, Trust-weighted matched offer + human
acceptance) and commits + executes it: `commit(commitment, authority, terms)` (per §5
`commitment = agree(offer, terms)`) then `execute(commitment, fleet)` where the S3
agent splits the work across a small **agent fleet** (2–3 `agent://` workers) across the
**routing seam** (§6 rating seam: each task → local/private-cloud/frontier, Trust-weighted).
Each `agent://` worker performs a bounded, delegable action; record a signed `decision://`
for the split and signed `action://`/`event://` per worker step. **DoD:** a committed job
advanced through at least 2 agent-worker steps with signed decisions/actions on the Ledger.

**3.2 — Human-escalation floor (irreversibility).** Any action with
`irreversible(failure)==true` OR `cost(failure)==unknowable` MUST escalate to a human
before execution (§6, LEVEL A normative; §7B). Demonstrate BOTH branches: (a) a cheap,
reversible micro-action auto-executed by a worker; (b) an irreversible action (e.g.
releasing final payment / irreversible subcontracting) that escalates to a **human**
`person://qk/approver`, whose signed DECISION/acceptance enumerates the alternatives and
commits the action. **DoD:** the irreversible action is NOT auto-executed; it proceeds
only after a signed human acknowledgement, and the ledger records the escalation.

**3.3 — Full S1→S5 cycle end-to-end.** Chain the whole loop on ONE relationship:
S1 identity/role → S2 intent/match (Trust-weighted) → **S3 commit + execute across the
fleet** → S2/S5 re-rank under updated Trust → S5 captures the resulting OUTCOME as signed
`evidence://`, updates the scoped `trust://`, and writes it. **DoD:** a test harness shows
the full cycle on one relationship with signed evidence at each step, and that the S3-executed
outcome feeds the S5 Trust update which re-ranks the next S2 match — closing the loop.

## Mandatory rules
- **Real tool output only.** Producing artifacts and RUNNING them is mandatory; never
  fabricate results, file contents, or citations. Re-run `run_conformance.py`
  (`sprints/sprint-0/artifacts/.venv/bin/python`) over Sprint-0 fixtures AND the Sprint-1
  AND Sprint-2 AND any new Sprint-3 fixtures to prove no regression (exit 0). Use the
  `run_s1_conformance.py` / `run_s2_conformance.py` pattern (reuse the Sprint-0 validator,
  repoint `FIXTURES` at each generation root).
- **Keep the URI cap and the frozen ontology** (§7J.11, Appendix C §C16). No new ontology
  nouns, no new URI schemes. `agent:// decision:// event:// evidence:// claim://
  expectation:// trust:// obligation:// commitment:// relationship://` already exist.
  Extend the schema ONLY where a genuine build finding requires it (additive-only; note
  in findings; if extended, rebuild `.json` via `build_schema.py`).
- **Update `SPEC.md` from findings:** write `sprints/sprint-3/notes/findings.md` as you
  go; apply genuinely necessary corrections (targeted `patch`, re-verify section
  numbering, bump minor version to **0.20**, append to the Version/Review Log);
  optionally sync the release mirror. Preserve every requirement's meaning.
- **Budget:** hard ~$10/mo cap — prefer local computation, batch web calls, keep prompts
  lean. No frontier-API spend for this sprint; orchestration is deterministic local logic
  (§G.11: do NOT hardcode speculative weights — keep seeded/verified evidence driving S2).
- **Raymond:** clean English output, `file://` absolute paths, honest "stuck/failed" over
  fabricated success, report status at each long step.
- **Single-threaded** per PROTOCOL: do all work yourself, in ONE process; do NOT use
  `delegate_task`/subagents.
- Do not touch anything outside `/home/rlg/relational-os/` except reading the
  `~/Documents` mirror and the Sprint-0/Sprint-1/Sprint-2 artifacts.

## Exit criteria (Definition of Done)
- `sprints/sprint-3/plan.md` written first; each sub-sprint has `work/<n>-plan.md`.
- S3 commit→execute→escalate→re-rank loop runs under `sprints/sprint-3/artifacts/` with
  real output; the harness **demonstrably shows a full S1→S5 cycle on one relationship
  with signed evidence at each step**, and irreversible actions escalating to a human.
- Sprint-0 conformance still exits 0 over all fixture generations produced so far
  (Sprint-0, -1, -2, -3).
- `SPEC.md` updated for genuine findings (bumped to 0.20, log appended).
- `sprints/sprint-3/summary.md` written (what was built, verified output, open issues).
- The next sprint's self-contained prompt written at `sprints/sprint-4/PROMPT.md` AND
  echoed as your final message.

## Hand-off requirement
Your **final message** must be the complete, self-contained **Sprint 4** prompt (per
`SPEC.md §8`, Sprint 4 = Settlement (S4) + multi-role/multi-org extension) — the same
text you save to `sprints/sprint-4/PROMPT.md`. It must (a) state the task with the same
read-plan-build-update-verify-handoff protocol, (b) reference only absolute paths and the
current `SPEC.md` (v0.20 by then), (c) carry the same rules (real output, URI cap/frozen
ontology, budget, clean English, single-threaded). Do not summarize your own Sprint-3 work
in that file — that goes in `summary.md`. The prompt must stand alone for a session that
starts with no memory.