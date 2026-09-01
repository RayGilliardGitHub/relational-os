# SPRINT 3 · SUB-SPRINT 2 — Human-escalation floor (irreversibility)

**DoD:** the irreversible action is NOT auto-executed; it proceeds only after a signed human
acknowledgement, and the Ledger records the escalation. Both branches run.

## Build (extends ros/s3.py)
- Risk classifier `risk(action) -> (irreversible, cost_knowable)` per §6:
  an action is `irreversible(failure)==true` OR `cost(failure)==unknowable` → must escalate.
- **Branch (a) reversible:** a cheap, reversible micro-action (e.g. `prepare_work_order`)
  is auto-executed by a worker directly — full autonomy where failure is cheap+reversible.
- **Branch (b) irreversible:** `release_final_payment` (payout cannot be undone; cost unknowable)
  → `escalate_to_human(task, person://qk/approver)` records a signed escalation `decision://`
  (reason: irreversible/unknowable) and marks the task pending; the action is NOT executed.
- `human_acknowledge(approver, alternatives, ...) -> signed DECISION` by `person://qk/approver`
  enumerating alternatives (release-in-full / hold-pending-inspection / release-partial /
  open-dispute) and committing the action; ONLY THEN is the worker authorized to `execute_task`.

## Verify
- Self-check `escalate_check` asserts, from the Ledger event order:
  1. no `release_final_payment` ACTION event precedes the human DECISION event (not auto-executed);
  2. an escalation decision exists (escalated, not executed) BEFORE the human commit;
  3. the human DECISION enumerates ≥3 alternatives and is signed;
  4. the irreversible action executes only after both.