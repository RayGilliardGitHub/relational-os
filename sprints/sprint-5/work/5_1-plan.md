# SPRINT 5 — SUB-SPRINT 5.1 PLAN  (Case-led loop + Exception heartbeat + Learning)

## Goal
On the running S1->S5 state (Quoteko), open ONE Case that surfaces a real, ledger-derived
exception and drive it `OPEN -> TRIAGE -> ASSIGNED -> IN_PROGRESS -> (BLOCKED) -> RESOLVED
-> CLOSED`, each transition recorded with signed evidence. Close an
`Exception -> Case -> Task -> verified outcome` cycle and record a **Learning** entry
(§7K.1: `Decision -> Expected -> Actual -> Variance -> WHY -> change-future-policy`).

## What will be built (in `ros/bol.py` + `bol_demo.py`)
- `BolService` operating-layer service over the existing substrate:
  - `metric_actual_from_ledger(...)` — compute a Metric's actual from ledger projections.
  - `open_case(...)` / `transition_case(sub, case, new_status, ...)` — each transition is
    a signed STATE_CHANGE event carrying the updated `case://` object (full coverage rule).
  - `exception_heartbeat(...)` — EXPECTED->ACTUAL->VARIANCE->SIGNIFICANCE->EXCEPTION->ROOT
    ->RECOMMENDED->DECISION->EXECUTION->VERIFIED, recorded as additive fields on the case.
  - `learning_entry(...)` — a `decision://` learning object (envelope: expected, actual,
    variance, why, change_future_policy) + a future-policy change on a `policy://`.
- Exception: **quarterly on-time delivery below target** (target 95%, ledger-projected
  actual below it; the norcrete late job is the root, epistemic status SUPPORTED).
- Case `case://qk/c-on-time-delivery` closes through the full lifecycle.
- A Task `task://qk/t-provider-rebalance` (the §7L #8 work) assigned to a delegated
  worker, executed (provider re-allocation policy + re-ranked S2 match to solarworks),
  and its follow-on job delivered on time — a verified outcome.

## Verification (5.1 DoD)
Demo check `s5_bol_check` asserts: case reaches CLOSED via legal transitions;
exception heartbeat fields populated (expected/actual/variance/significance/root/
recommended/decision/verified_outcome); a `task://` was assigned with authority and
completed; a verified outcome exists (evidence); a Learning entry `decision://` records
Expected->Actual->Variance->WHY->change_future_policy; the policy object changed.
Re-run Sprint-0 conformance over the fixture generations (exit 0).

## Objects introduced (URI-cap safe)
`case://qk/c-on-time-delivery`, `task://qk/t-provider-rebalance` (+ follow-on task),
`policy://qk/provider-allocation`, `decision://qk/s5-learning-on-time`,
`authority://qk/for-operations`, `rule://`/`delegation://` for the ops worker,
`evidence://`, `expectation://`, plus aggregated ledger/graph/statemachine fixtures.
Exception + Priority carried as **envelope fields** (no new schemes).