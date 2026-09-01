# Sub-sprint 1 — Plan + baseline

## Objective
Confirm the whole system is green before building anything, and pin the exact recording surfaces I
extend. Nothing is built in this sub-sprint.

## Steps
1. Read SPEC (done), PROTOCOL (done), prior summaries/hand-off, STRESS-TEST brief (done).
2. Read Sprint-10 `run_interest_conflict_demo.py` + `conformance_interest.py` (done) — the
   additive-field pattern (interest/constraint/conflict objects on relationships + case; decision://
   with authority; UNRESOLVED + epistemic_state; MERGE-not-replace; `graph.get(uri) or {}`).
3. Read the schema `Recommendation` $def (done) — `by/for/options` required + additive
   `includes_do_nothing/tradeoff/authority_required/confidence/expected_impact/decision`. Confirm
   NO `recommendation://` scheme in the frozen x-uri-catalog (confirmed: catalog has person/org/
   agent/system/legal_entity… — recommendation is additive only).
4. Read SPEC §7K.1 (done) — "Trade-off / decision analysis: options incl. do-nothing; explains the
   trade-off, not a bare pick"; "Business Model = what better means".
5. Read Sprint-8 agent pattern (`run_agent_demo.py`, `agent_adapter.py`, prompt) (done) for the
   optional model half; note `phi4-mini:3.8b-q8_0` may be absent → fallback chain includes
   `gemma4:e2b-it-qat`, which IS present (verified via /api/tags).
6. Run the full baseline suite and record results.

## Baseline output (this verifies the Definition of Done's "green BEFORE" clause)
- From instances/: `python3 build_all.py` → ALL SECTORS PASS   [already run: PASS]
- `conformance_all.py` → SECTOR CONFORMANCE: ALL SECTORS PASS  [already run: PASS]
- From sprints/sprint-5/artifacts/: `python3 run_s5_demo.py` → RESULT: ALL PASS [already run: PASS]
- From instances/contested_reality/: `python3 run_interest_conflict_demo.py` → ALL PASS [run: PASS]
- `conformance_interest.py` → ALL PASS [run: PASS]
- Sprint-9: `python3 run_dispute_demo.py` + `conformance_dispute.py` → ALL PASS (verify now)

## Exit criteria for this sub-sprint
Reference + Sprint-9/10 demos all ALL PASS; the emission/fixtures/statemachine pattern is pinned;
the additive `Recommendation`-shape object is designed. Then proceed to sub-sprint 2 (build the
model).