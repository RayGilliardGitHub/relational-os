# Work 3 — `run_reconcile_learning_demo.py` (exit 0 = ALL PASS) + the §7L Q7/Q8 render

Drives the honest learning→library→future-dispute flow WITH a real lifecycle on each dispute, then
asserts the containment contract and renders the cockpit line. Everything is real tool output.

Flow (mirrors the design verified in work 1/2):
1. **Seed trust** (score 0.80) + **Episode A** (`inspect-learn-a` @ initial rule
   best-reliability-threshold, threshold 0.95): run_one → determination rework-partial-credit,
   RESOLVED. Record the REALIZED outcome value 0.90 additively (signed event) → the learner's signal.
   Snapshot A's ledger `(n_events, per-entry hashes)` for the append-only proof.
2. **Learning**: `learn_threshold(0.95, 0.90, 0.8, 0.55, 0.95)` → 0.91, changed=True. Assert
   deterministic re-run equality, in `[0.55,0.95]`, evidence-gated. Build learned spec
   `calibrated-threshold-091`; **add it to `ac.RULE_LIBRARY`**; `record_learned_rule` (append-only
   signed `rule://…/reconcile-rule` kind=PROCEDURE + `decision://…/reconcile-learning` + event).
3. **Episode B** (`inspect-learn-b`) driven ONCE under the LEARNED rule (`rule_spec` =
   `RULE_LIBRARY[name]`, threshold 0.91): determination rework-partial-credit, RESOLVED_DETERMINED.
   Assert a SECOND, genuinely distinct dispute (different predicate set: A vs B claim/evidence URIs
   disjoint) — this is NOT "re-run the same case and claim learning".
4. **Old-rule baseline for B (SAME evidence, derived reconcile only, not a second lifecycle)**:
   provision B's evidence, reconcile under threshold 0.95 → determined=[], uncertainty=True → the
   OLD rule leaves B UNRESOLVED; the learned rule DETERMINES it. The cross-dispute verdict flip,
   ONLY the learned threshold differs (§16-style flip proof).
5. **Learning feeds the library / cross-org reuse**: drive `deli-learn`
   (`org_under_library_rule(DELI, "deli-learn", name, {threshold:0.91, support_floor:0.55})`) with
   the SAME learned `RULE_LIBRARY` dict (`is`-identity against `ac.RULE_LIBRARY[name]`), a genuinely
   different org → the learned rule is a reusable named library spec, not a one-case patch.
6. **Containment contract (all asserted, real):**
   (a) trust untouched — every driven org's `trust://…/claimant` score == 0.80 (S5-only).
   (b) human authority intact — each determination decision carries its configured authority; and
       `determination_policy` is byte-identical before vs after the learning step (learning never
       edits it; the §6 human's call is unchanged).
   (c) ledger append-only — after `record_learned_rule`, A's event count GROWS and every PRIOR event
       is byte-identical (no rewrite); the learned rule/decision are NEW objects appended.
   (d) explicit bound — 0.55 <= 0.91 <= 0.95; recompute-identical (no clock/state dependence).
7. **§7L Q7/Q8 cockpit line**: render `cockpit-q7-q8-reconcile-learning.md` (+ `reconcile-learning.m
   d,json`) per org: ACTIVE reconcile rule, its SOURCE (registry / rule-library / learned this run),
   and whether a learning step changed it this run + the evidence-gated WHY.
8. **Fixtures**: emit for the 3 new labels; print RESULT: ALL PASS (exit 0).

Constraints: additive only; 49 `$defs`; SPEC v0.22; deli/cove & prior runners byte-identical; run
from `instances/contested_reality/`; pure stdlib (python3).