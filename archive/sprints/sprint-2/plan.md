# SPRINT 2 — PLAN  (Trust Engine Minimum; SPEC §8 Sprint 2)

**Spec:** v0.18 | **extends:** Sprint 1 (S1 substrate + S2 Matching) | **domain:** Quoteko
quoting/triage | **role:** customer | **runtime:** sprint-0 `.venv/bin/python`

## Objective
Implement the S5 Accountab/Trust engine minimum on top of the Sprint-1 substrate:
capture + verify one outcome class, update + persist scoped Trust, and show Trust
re-ranking Sprint-2 results (the §5 flywheel). Trust must demonstrably change
routing/pricing in a test harness.

## Sub-sprints
- **2.1 — S5 capture + verify (one outcome class).** `capture(outcome, provenance) →
  signed evidence://` and `verify(evidence, axioms) → verified result` for the crisp,
  objective class "contracted roofing job completed by its committed deadline",
  verified via an anchored completion record. Ends with a verified outcome record
  wired to `relationship://` + `trust://` context, per §3.17 (evidence supports claim
  X to degree Y under procedure Z; no capital-T truth overclaim).  → `work/1-plan.md`
- **2.2 — Trust update + write.** `update(Trust, evidence, weight, recency) → Trust`
  per §5 `T_{k+1}=clamp(T_k + alpha*(outcome_k−expectation_k)*evidence_k, 0, 1)`, keyed
  `(subject, target, claim, context)` per §3.14; cold-start T1 = Sprint-1 seeded
  `trust://`. Compute + WRITE updated `trust://` to graph + signed ledger event.
  → `work/2-plan.md`
- **2.3 — Trust re-ranks S2 (flywheel).** Re-run `match_offers` after the update; a
  contractor whose verified outcome moved its scoped Trust must move differently in
  the ranked output. Harness shows before/after Trust + before/after ranking and
  asserts the change matches the equation.  → `work/3-plan.md`

## Definition of Done (exit criteria)
- `plan.md` + `work/<n>-plan.md` per sub-sprint, written before execution.
- S5 capture→verify→Trust-update→re-rank runs under `sprints/sprint-2/artifacts/` with
  real output; the harness demonstrably shows Trust **changing S2 ranking**.
- Sprint-0 conformance still exits 0 over all three fixture generations (Sprint-0, -1, -2).
- `SPEC.md` updated from genuine findings (bump 0.18 → **0.19**, log appended); schema
  NOT extended unless a real build finding requires it (additive-only).
- `sprints/sprint-2/summary.md` written.
- `sprints/sprint-3/PROMPT.md` written AND echoed as this sprint's final message.

## Non-negotiables
Real tool output only; single-threaded (no subagents); URI cap + frozen ontology held;
~$10/mo budget (local math only, no frontier spend); clean English; `file://` paths;
honest "stuck/failed" over fabrication. Touch nothing outside `relational-os/` except
reading the `~/Documents` mirror (optional sync).