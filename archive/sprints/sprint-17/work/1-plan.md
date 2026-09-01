# Work 1 — config data for the learning episodes (additive to adjudication_configs.py)

Imports EXISTING engine unchanged; this is pure DATA (patient of the established `inspect_variant`
pattern). Adds to `adjudication_configs.py` (hidden appendix at the end):

- `inspect_batch(label, dispute_uri, claims, evidence, resolution_outcome)` — clones `INSPECT`
  (same actors/relationships/obligations/economics/options/weights/factor_scores/floor_gated/
  authority/reconcile-default) and swaps ONLY the dispute + claims + evidence + label. This is how the
  generic engine runs a SECOND, distinct batch dispute on the same org (no new engine code).
- `INSPECT_BATCH_A` (label `inspect-learn-a`) — the LEARNING episode:
    * claims: `claim://inspect-la/passed` (company; evidence machine-pass ANCHORED 0.92 + audit-signoff
      RECORD 0.97 → support **0.97**) vs `claim://inspect-la/failed` (buyer; resident-note TESTIMONY
      0.90 → support **0.90**).
    * initial reconcile: registry `best-reliability-threshold`, threshold **0.95**, support_floor 0.55.
    * determination_policy `adopt-eligible-best` (machine-eligible best = rework-partial-credit).
    * the dispute carries an additive `realized_value` **0.90** + the "WHY" of the realized outcome
      (batch accepted with a documented rework); this is the RECORDED, realized outcome the learning
      step derives its signal from (NOT hindsight re-derivation of the reconcile).
- `INSPECT_BATCH_B` (label `inspect-learn-b`) — the SECOND, DISTINCT future dispute (different
  predicate set): claims `claim://inspect-lb/passed` (single beta-machine-pass ANCHORED 0.93 →
  support **0.93**) vs `claim://inspect-lb/failed` (beta-resident-note TESTIMONY 0.88). Under the
  initial 0.95 it is UNDETERMINED → UNRESOLVED; under the learned 0.91 it is DETERMINED → the cross-
  dispute verdict flip.
- `INSPECT_BATCHES = [INSPECT_BATCH_A, INSPECT_BATCH_B]` + a `LEARN_HYPER` block (learning_rate 0.8,
  threshold_lo 0.55, threshold_hi 0.95, eps 1e-6) consumed by `reconcile_learning.py`.

Constraints honored: `evidence` refs are ARRAYS; no additive key ending in `at|time|deadline|expires|
expiry|effective|due|since` (C2 RFC3339 probe); claims `evidence` lists proper; dispute has
about/parties/status; options include the `unresolved` baseline; weights sum 1.0 (reused from INSPECT).
Do NOT touch `DELI`, `COVE`, `SCENARIOS`, `RULE_VARIANTS`, `SPEC_AUTHORED_RULES`, `RULE_LIBRARY`, or
any prior variant — the Sprint-13/14/15/16 runners must stay byte-identical.