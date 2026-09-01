# SPRINT 5 — SUMMARY

**Project:** RelationalOS | **Spec:** v0.21 → **v0.22** | **Date:** 2026-09-01
**Result:** Sprint 5 complete — the **Business Operating Layer (the product)** is built and
**verified** on the running S1→S5 state for the fictional Quoteko company. A full
`Exception → Case → Task → verified outcome → Learning` cycle closes on the shared
Graph + Ledger, the **Cockpit** shows business health + prioritized attention + an AI
recommendation carrying the authority it requires (§7J.9), and the **§7L ten morning
questions are answered WITH evidence**. Conformance exits 0 over all **six** generations.

## What was built (all under `sprints/sprint-5/artifacts/`)
Extends the copied Sprint-4 `ros/` package with the operating layer (the product):

- **Business Operating Layer — `ros/bol.py`.** `BolService` over the existing substrate:
  Case lifecycle (OPEN→TRIAGE→ASSIGNED→IN_PROGRESS→BLOCKED→RESOLVED→CLOSED, signed evidence
  per transition), the §7J.2 Exception heartbeat (EXPECTED→ACTUAL→VARIANCE→SIGNIFICANCE→
  EXCEPTION→ROOT→RECOMMENDED→DECISION→EXECUTION→VERIFIED, with §7K.2 epistemic status),
  Goal/Metric + the §7J.1 Goal→Metric→Actual→Variance→Decision→Action→Outcome loop,
  Priority = f(impact, urgency, confidence, irreversibility, relationship-importance,
  cost-of-delay) with priority-ordered attention, Dependencies (§7J.6
  requires/blocks/enables/derived_from/impacts) with a transitive impact analysis, and a
  §7K.1 Learning entry (Decision→Expected→Actual→Variance→WHY→change-future-policy) that
  updates a `policy://`. Ledger projections (`project_on_time`, `project_settled_value`,
  `project_trust`) drive the business-health panel from history.

- **Demo / builders — `bol_demo.py`.** `build_s51` (case-led loop + exception + learning),
  `build_s52` (goals/metrics/priority/dependency + health panel), `build_s53` (cockpit),
  plus fixture emission and the cockpit report writer.

- **Runners.** `run_s5_demo.py` (re-runs ALL Sprint-1..4 checks + the 3 new Sprint-5 checks)
  and `run_s5_conformance.py` (Sprint-0 validator verbatim, repointed at all six
  generations).

## Verified output (ran this sprint, real tool output)
`python3 run_s5_demo.py` → **exit 0, ALL PASS**:
- All re-used Sprint-1/2/3/4 checks pass unchanged on the full state (s1, roundtrip, s5,
  flywheel, s3, escalate, loop, s4, role, org) — **no regression**.
- **5.1** case `case://qk/c-on-time-delivery` completes OPEN→TRIAGE→ASSIGNED→IN_PROGRESS→
  BLOCKED→RESOLVED→CLOSED; exception heartbeat populated (expected 0.95, actual 0.833,
  variance −0.117, CRITICAL; root SUPPORTED); #8 task `task://qk/t-provider-rebalance`
  assigned to `agent://w-ops` under `authority://qk/for-operations` (priority 0.695); the
  re-allocated rallied solarworks delivery settled (`met`) + captured/verified on time
  (forward-period on-time **1.0**, solarworks Trust → 1.0); Learning entry
  `decision://qk/s5-learning-on-time` + provider-allocation policy → **v3**.
- **5.2** health panel (3 ledger-projected metrics: on-time CRITICAL, customer-trust OK,
  settled-value WARN); priority-ordered attention; dependency→impact analysis traces
  task→[case, metric, goal, policy, followup task].
- **5.3** cockpit report written (`reports/cockpit.md` + `.json`); §7L #1–#10 answered with
  cited ledger/graph evidence; #8 assigned authorized work; #9 authority+capacity; #10
  verified outcome + Learning.
- Full-state round-trip: **160 graph objects rebuilt from 97 ledger events** (exit 0).

`<sprint0-venv>/bin/python run_s5_conformance.py` → **exit 0**: Sprint-0 **156**, Sprint-1
**28**, Sprint-2 **35**, Sprint-3 **55**, Sprint-4 **174**, Sprint-5 **316** — ALL PASS, one
shared validator (no regression over any generation).

## What the spec gained (v0.21 → v0.22)
- **URI cap / frozen ontology respected — the operating layer is a PURE assembly.** Schema
  artifacts **byte-identical** (49 `$defs`), validator unmodified. Exception, Priority, the
  AI Recommendation, and Q9 capacity are **additive envelope fields** on `case://`/`task://`
  (no `exception:// priority:// recommendation:// capacity://` schemes). Learning is a
  `decision://` + a `policy://` change.
- Four genuine additive normative clarifications:
  1. §3.16 — signed state deltas are **immutable snapshots** (deep-copied); a mutating
     operating object's later in-place edit must not retroactively break an earlier signing
     (F2).
  2. §7J.5 / §C16 — derived values (Exception/Priority/Recommendation) and Q9 capacity are
     additive fields; capacity is Q9's `assigned_capacity` field (F1/F6).
  3. §8 — Sprint 5 (S1→S5 chain) marked **COMPLETE**; the §7L test is answerable for one
     company (F4).
  4. Version bumped to **0.22**; Version/Review Log appended; §7J.1–11 numbering re-verified.
- Full findings: `sprints/sprint-5/notes/findings.md` (F1–F6).

## Open issues / notes
- Deterministic local operating layer only (§G.11): the Priority weights, the forecast, and
  the root-cause nomination are explicit, documented local logic — not learned or frontier-API
  behavior. No frontier spend (~$0); single-threaded, no subagents.
- The ledger projections count the *signed completion records* written by the harness
  (F3): the on-time metric stores `actual` rounded to 3 decimals; the projection check is
  tolerance-aware.
- `capacity://` exists as a `$def` but is not in `x-uri-catalog`; Q9 capacity is therefore an
  additive field, not a URI (F6). A future phase could promote a `capacity://` scheme
  (additive-only per §C16) if allocation reasoning needs it — not required for the DoD.
- The launched BOL works on the harness's seeded outcome records and one Quoteko company; a
  real deployment still needs: real connectors (S2 matching, S4 payments, §7H gateway),
  a real graph/ledger store (§7C), AI routing for root-cause/forecast over real data
  (currently deterministic local), and the §8 Phase-B beyond-backlog (process mining,
  scenario, decision learning, memory, universal query, benchmarking).
- Release mirror (`~/Documents/ai-relational-os-spec.md/.pdf`) not re-synced (optional,
  consistent with Sprints 1–4).

## Hand-off
This is the FINAL sprint. The project's closing hand-off is at
`/home/rlg/relational-os/sprints/COMPLETE.md`, describing the finished S1→S5 chain, its
proven loops, the cockpit, and how to run every demo/conformance runner.