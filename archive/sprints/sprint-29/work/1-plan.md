# SPRINT 29 — work/1-plan.md  (engine change: recorded per-option requirement -> per-option label)

## Prior state
- plan.md written; green baseline established (all 12 CR demos + conformances + build_all + S5 +
  agent PASS; schema raw hash `7fc38c8c…`; 49 `$defs`; SPEC v0.22).

## This step — the ONLY engine file change (additive)
Modify `instances/contested_reality/adjudication_engine.py` ONLY, and ONLY to extend the Q7/Q8
`capacity_constraint` block (or the shared capacity helper) for the NEW recorded per-option
requirement. Keep all frozen functions byte-identical.

1. **New REPLAYABLE recorder `record_capacity_requirements`** (next to `record_capacity`):
   `record_capacity_requirements(sub, authority_uri, requirements: dict, signer) -> str`.
   - assert `authority_uri` starts with `authority://`;
   - MERGE-not-replace: `obj = {**sub.graph.get(authority_uri), "capacity_requirements": dict(requirements)}`
     (preserve-unknown — the authority's required fields ride along; exactly the record_capacity
     pattern);
   - record a signed `STATE_CHANGE` event (event_id/correlation/causation/idempotency like
     `record_capacity`).
   - C2-safe key `capacity_requirements` (no temporal suffix).

2. **New pure helper `_per_option_capacity_flags(capacity_obj, requirements, options, baseline,
   non_headroom)`** -> `{option: label}`:
   - `available = (capacity_obj.value or 0) - (capacity_obj.load or 0)` as numbers (value + load both
     recorded; guard non-numeric with the existing `_num`).
   - for each option: skip the baseline (never flagged); if a RECORDED requirement exists and it
     `> available` -> `capacity_infeasible`; else -> `capacity_risk` ONLY when `non_headroom`
     (reason != headroom); a consumer with NO recorded requirement stays `capacity_risk` when
     `non_headroom` (byte-compatible with today).
   - pure, deterministic, no wall-clock.

3. **Extend the Q7/Q8 `capacity_constraint` block in `cockpit_s7l`** (where today's `_cc_flags`
   loop lives): read `reqs = (auth_obj or {}).get("capacity_requirements") or {}`; when `reqs` is a
   non-empty dict, compute `_cc_flags = _per_option_capacity_flags(q9_capacity, reqs,
   cfg["options"], q7["baseline"], non_headroom=(_cclabel != "headroom"))`; otherwise keep today's
   loop EXACTLY (byte-identical default). Add an additive `per_option_requirements: {name: req}` +
   `available_capacity: <value>` to the block ONLY when requirements are recorded (orgs that record
   none carry NONE of these — strict superset).

## Byte-identity contract
- Org with NO `capacity_requirements` recorded: `capacity_constraint` block EXACTLY as Sprint 28
  (reason/flag/options_flagged = all capacity_risk non-baseline / baseline absent; a no-requirements
  org carries no `per_option_requirements` / `available_capacity` key).
- Frozen functions (`rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`/`reconcile`/
  `run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/`_capacity_reason`) untouched.

## Execution
- Edit engine, run the Sprint-28 re-baseline demos to confirm the 5 reused orgs stay byte-identical
  (horizon4/horizon3/horizon2 all PASS — the new helper only fires when requirements are recorded).
- Next step (work/2-plan.md) builds the new runner.