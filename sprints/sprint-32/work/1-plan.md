# SPRINT 32 — work/1-plan (build step 1: the re-rank module)

## What
A NEW pure module `instances/contested_reality/capacity_rerank.py` exposing
`capacity_rerank(cfg, sub, *, library=None)` that reads the SAME recorded capacity data the engine
already renders on the advisory path and computes the authorized POLICY re-rank. The engine is NOT
touched (additive capability lives in a new file, engine hash `a60f8f7…` must stay unchanged).

## Why a separate module, not an engine helper
The PROMPT prefers "a pure runner + recorded data as Sprint 29/30/31 did; touch
`adjudication_engine.py` ONLY additively if a genuine, small need surfaces". The re-rank reuses
ONLY public/importable engine surface (`cockpit_s7l` → q7.q8.capacity_constraint, `rank`, the
recorded graph), so NO engine change is needed. Keeping the engine byte-identical maximally
preserves "the advisory path never re-ranks" (the re-rank is a distinct, explicit step).

## Algorithm (deterministic, by the frozen `rank` utility)
1. `c = eng.cockpit_s7l(cfg, sub, library=library)`; `cc = c["q8"].get("capacity_constraint")`.
2. `cc` absent → return `None` (no recorded capacity → nothing to re-rank; advisory unchanged).
3. `prior = c["q7"]["machine_eligible_best"]`; `flags = cc.get("options_flagged", {})`.
4. `flags.get(prior) != "capacity_infeasible"` → return the org "no_rerank" info? NO — return a
   block indicating NOTHING to re-rank (prior runnable), so orgs whose best is NOT infeasible prove
   UNCHANGED. I'll return a dict with `"needed": False, "reason": "prior machine best is runnable"`.
   Runner asserts `needed=False` ⟺ Q8 unchanged == `cockpit_q7q8`.
5. Else walk `eng.rank(cfg)`; first `r` with `not r["floor_gated"]` and
   `flags.get(r["option"]) != "capacity_infeasible"` → `replacement`.
6. If none found → `replacement = baseline` (do-nothing/UNRESOLVED), `replacement_is_baseline=True`.
7. Return the full block: `{needed, prior_machine_best, prior_best_capacity_flag, recorded_descriptors,
   available_capacity, per_option_requirements, replacement, replacement_is_baseline, policy,
   floor_respected, reason, note}`.

## Exit criteria
- `capacity_rerank.py` imports clean; engine untouched (hash unchanged).
- Probing the 11 orgs + the new COVE org yields the exact expected replacements from plan.md.