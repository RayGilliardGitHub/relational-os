# SPRINT 5 — PLAN  (Business Operating Layer — the product)

**Spec:** v0.21 -> v0.22 | **Project:** RelationalOS | **Date:** 2026-09-01
**Protocol:** `PROTOCOL.md` (read-before-write, plan-before-build, real tool output,
single-threaded, URI cap, ~$0 local computation).

## Objective
Turn the verified S1->S5 service chain (Sprint-4 end-state) into the **Business
Operating Layer** an owner uses every morning: Cases, Goals/Metrics, Task & Work Queue,
Exceptions, Priority/Attention, Dependency/Impact, and the **Cockpit** (§7J.9). Satisfy
the **§7L Business Indispensability Test** for the fictional Quoteko company: answer all
ten morning questions WITH evidence from the ledger/graph, turn #8 into assigned,
authorized Task work that closes in a verified, learned outcome (#10), and show business
health + prioritized attention in the cockpit.

## Context (absolute paths, read first)
- Canonical spec (contract): `/home/rlg/relational-os/SPEC.md` (v0.21)
- Protocol: `/home/rlg/relational-os/PROTOCOL.md`
- Sprint-0 contracts (reuse, do not re-derive): schema + `conformance.py` + fixtures in
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/`
- Sprint-1/2/3/4 `ros/` package + builders to **copy** (not git import) into Sprint-5
  artifacts: `/home/rlg/relational-os/sprints/sprint-4/artifacts/`
- Task brief: `/home/rlg/relational-os/sprints/sprint-5/PROMPT.md`

## Method
Copy the Sprint-4 `artifacts/` tree into Sprint-5 (self-contained, per contract), then
ADD the operating-layer service `ros/bol.py`, the demo builders (`bol_demo.py`),
`run_s5_demo.py`, and `run_s5_conformance.py`. Chain on the S1->S5 end-state
(`build_s2() -> build_s3() -> build_s41/42/43`), then the three operating sub-sprints.

**Representation within the URI cap (§7J.11 / §C16):** the operating layer uses ONLY the
five existing first-class nouns already in the schema/catalog — `case:// goal://
metric:// task:// dependency://` — plus the existing assemblies already in the `$defs`
(`process://`, `risk://`, `SLA`, `Policy`, `Escalation`). Derived values (§7J.2
Exception, §7J.5 Priority) are carried as **additive envelope fields** on those objects
(schema `additionalProperties: true`), NOT new URI schemes. Organizational Learning
(§7K.1) is recorded as a `decision://` learning entry + a section 7K Policy change.

## Sub-sprints (sequential; each writes work/<n>-plan.md before executing)
- **5.1 — Case-led loop + exception heartbeat + Learning.** Open a Case (an
  ExCom exception: on-time delivery below target) and drive it
  OPEN->TRIAGE->ASSIGNED->IN_PROGRESS->(BLOCKED)->RESOLVED->CLOSED with signed evidence
  per transition; run the §7J.2 exception heartbeat (EXPECTED->ACTUAL->VARIANCE->
  SIGNIFICANCE->EXCEPTION->ROOT->RECOMMENDED->DECISION->EXECUTION->VERIFIED); close one
  exception->case->task->verified-outcome cycle; record a Learning entry
  (Decision->Expected->Actual->Variance->WHY->change-future-policy).
- **5.2 — Goals/Metrics/Priority/Dependency.** Goal->Metric->Actual->Variance->
  Decision->Action->Outcome loop; compute Priority = f(impact, urgency, confidence,
  irreversibility, relationship-importance, cost-of-delay); represent Dependencies
  (requires, blocks, enables, derived_from, impacts) with a transitive impact analysis;
  business-health panel derived from ledger-projected Metrics.
- **5.3 — The Cockpit + §7L.** Produce the cockpit output (business health, prioritized
  attention "seven things today", AI recommendation with the authority it requires) and
  answer the §7L ten questions with cited ledger/graph evidence.

## Definition of Done (PROMPT.md exit criteria)
- `plan.md` first; each sub-sprint has `work/<n>-plan.md`.
- `artifacts/` has the extended `ros/` package (incl. `bol.py` operating layer), the
  exception heartbeat, a cockpit/report generator, a demo runner and a conformance
  runner, all with real tool output; the harness answers §7L with evidence, turns #8
  into assigned authorized work closing in a verified learned outcome (#10), and shows
  health + prioritized attention in the cockpit.
- Sprint-0 conformance (`.venv/bin/python run_conformance.py`) still exits 0 over all
  SIX fixture generations (Sprint-0, -1, -2, -3, -4, -5).
- `SPEC.md` updated for genuine findings only, bumped to **0.22**, log appended, §8
  roadmap marks the S1->S5 chain complete.
- `sprints/sprint-5/summary.md` (built / verified / open issues).
- Closing hand-off at `sprints/COMPLETE.md` (final sprint; no next-sprint PROMPT).

## Constraints
Real tool output only. Single-threaded, no subagents. Hold the URI cap + frozen
ontology (extend schema only on a genuine build finding, additive-only, rebuild .json).
~$0 budget (deterministic local logic per §G.11). Clean English, `file://` paths, report
status at each long step. Touch nothing outside `/home/rlg/relational-os/` except
reading prior artifacts and the `~/Documents` mirror.