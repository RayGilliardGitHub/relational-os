# Work 2 — `reconcile_learning.py`: the deterministic, clamp-bounded reconcile-rule learner

Pure stdlib; additive; imports only `ros.substrate.now_iso` (for signing). It is the **§7K.1
Decision→Expected→Actual→Variance→WHY→change-future-policy** loop applied to the reconcile THRESHOLD.
Honest label on every function: it recalibrates the RULE's parameter from a recorded, realized
outcome — it does NOT learn the answer to any case, and it never moves Trust/authority/history.

Functions:
- `learn_threshold(prior_threshold, realized_value, learning_rate, lo, hi, eps=1e-6) -> dict`
  Pure, deterministic. `delta = learning_rate·(realized_value − prior_threshold)`;
  `new = round(clamp(prior_threshold + delta, lo, hi), 4)`; `changed = |delta| >= eps`.
  WHY: if the realized value < prior threshold (a determination actually held at support the bar
  demanded MORE of) the threshold was too strong → LOWER it toward the realized value (relax);
  if realized value > prior threshold the bar was below what outcomes provided → RAISE it
  (stiffen). Explicit bound `[lo,hi]`; never the wall-clock; recompute-identical on re-run.
- `build_learned_library_spec(name, *, learned_threshold, prior_threshold, realized_value,
  learning_rate, bound, why) -> rule_spec dict` — a NEW named `RULE_LIBRARY` entry: aggregate `max`,
  value_field `reliability`, plus additive `learned_threshold`/`learned_param`/`calibrated_from`/
  `bound`/`why` (rule_spec is plain data; the engine preserves unknown fields). This is "learning
  feeds the library": the learned artifact IS the rule the org can reuse.
- `record_learned_rule(sub, label, *, signer, authority, prior_reconcile, learned_spec,
  t_prime, learned_decision_uri, realized_value)` — APPEND-ONLY signed record: a NEW `rule://{label}/
  reconcile-rule` (Rule $def: kind=`PROCEDURE`, text=the reconcile-threshold procedure description,
  plus additive learned fields) and a `decision://{label}/reconcile-learning` (Decision $def required
  `[uri,by,authority]` + `rules_applied:[rule_uri]` + confidence + expected/actual + detail), both in
  ONE signed `event://{label}/reconcile-learning` appended to the immutable ledger (history not
  rewritten — never touches an existing event). Returns the rule_uri.
- `record_realized_outcome(sub, cfg, dispute_uri, outcome_value, signer)` — signed event recording the
  realized outcome value additively ON the dispute (merge-not-replace `{**graph.get(du), ...}`) so an
  auditor sees the realized outcome the learner derived its signal from. Returns nothing.

Conventions honored: no additive key ends in `at|time|deadline|expires|expiry|effective|due|since`
(C2 RFC3339 probe); `evidence`/`rules_applied` are arrays; merge-not-replace on existing objects;
`Graph.get()` one positional arg. The signer is the org registrar/an adjudicator (a bounded operator),
NOT any autonomous entity; it never changes `determination_policy` (the §6 human's call stays intact —
asserted by the runner).