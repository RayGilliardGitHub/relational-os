# SPRINT 3 — PLAN (Orchestration S3 + human-escalation floor)

**Spec:** v0.19 (→ **0.20**) | **Date:** 2026-09-01 | **Mode:** single-threaded, real output only

## Objective
Build the **S3 Orchestration & Execution** service on top of the Sprint-2 S5 Trust
engine (Quoteko scene), add the **human-escalation floor** (§6/§7B), and demonstrate a
**full S1→S5 cycle on one relationship** where an S3-executed outcome feeds the S5 Trust
update which re-ranks the next S2 match (the flywheel, closed).

## Scope (per SPEC §8/§5/§6; PROMPT.md)
- **3.1** `commit(commitment, authority, terms)` then `execute(commitment, fleet)` across a
  small agent fleet (2–3 `agent://` workers) over the §6 routing seam (local / private-cloud
  / frontier), Trust-weighted. Signed `decision://` for the split; signed `action://`/`event://`
  per worker step. DoD: committed job advanced through ≥2 agent-worker steps with signed
  decisions/actions on the Ledger.
- **3.2** Irreversibility floor — an action with `irreversible(failure)==true` OR
  `cost(failure)==unknowable` MUST escalate to a human before execution. Demonstrate BOTH
  branches: (a) a cheap reversible micro-action auto-executed; (b) an irreversible action that
  escalates to `person://qk/approver`, whose signed DECISION enumerates alternatives and
  commits it. DoD: irreversible action NOT auto-executed; proceeds only after signed human
  acknowledgement; ledger records the escalation.
- **3.3** Full S1→S2→S3→S5(→re-rank S2) cycle on ONE relationship, signed evidence each step,
  S3-executed outcome feeds S5 Trust update which re-ranks the next S2 match (flywheel closed).

## Definition of Done
1. `plan.md` + `work/<n>-plan.md` (each sub-sprint), written before that sub-sprint executes.
2. `sprints/sprint-3/artifacts/` contains `ros/` (Sprint-2 package copied + `s3.py` added),
   `s3_demo.py`, `run_s3_demo.py`, `run_s3_conformance.py`, `fixtures/`, `graph/`.
3. `run_s3_demo.py` → **exit 0**, ALL PASS — shows the full S1→S5 cycle on one relationship
   with signed evidence at each step, the fleet execution, and the irreversible action
   escalating to the human approver.
4. **Sprint-0 conformance still exits 0** over ALL fixture generations so far: Sprint-0, -1,
   -2, AND the new Sprint-3 fixtures (reuse the Sprint-0 validator; exit 0 = no regression).
5. `SPEC.md` updated for GENUINE build findings only (bump to **0.20**, append Version/Review
   Log entry, targeted patches; URI cap + frozen ontology preserved — no new nouns/schemes).
6. `summary.md` written (built, verified output, open issues).
7. `sprints/sprint-4/PROMPT.md` written (Settlement S4 + multi-role/multi-org) and echoed as
   the final message.

## Constraints
- **Single-threaded** (no subagents) per PROTOCOL.
- Real tool output only; no fabricated results/citations.
- URI cap (§7J.11 / App C §C16) & frozen ontology: use only existing schemes
  (`agent:// decision:// event:// evidence:// claim:// expectation:// trust:// obligation://
  commitment:// relationship://`, plus existing person/org/rule/permission/delegation/authority/
  offer/entity). No new nouns, no new URI schemes.
- Budget ~$0: local computation only; deterministic orchestration (no speculative weights, §G.11).
- Clean English; `file://` absolute paths; report status at each long step.

## Sub-sprint breakdown
1. **3.1 — S3 commit→execute** (`work/1-plan.md`)
2. **3.2 — Human-escalation floor** (`work/2-plan.md`)
3. **3.3 — Full S1→S5 loop + conformance + spec update** (`work/3-plan.md`)