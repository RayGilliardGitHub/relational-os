# §7L Q7/Q8 cockpit — engine-native render (Sprint 18)
generated 2026-09-01T05:08:28Z  |  active rule + source + learned-or-not + why reported BY `adjudication_engine.cockpit_q7q8`/`render_cockpit_q7q8`  |  SPEC v0.22, 49 $defs, URI cap

The Sprint-16/17 runner-report lines are now a first-class, data-only engine render: for ANY generically-driven org the engine reads the ACTIVE reconcile rule, its source, whether a learning step changed it this run, and the evidence-gated why — from the org's own config + ledger, with no per-org engine Python.

```
# §7L Q7/Q8 cockpit (engine-native) — org deli
Q7 options: accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline: unresolved  |  machine-eligible best: partial-settlement
Q8 recommendation: partial-settlement (authority authority://deli/adjudicate; floor-gated: ['accept-customer-refund'])  ->  determination: partial-settlement
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False
why: unchanged
```

```
# §7L Q7/Q8 cockpit (engine-native) — org inspect-corroboration
Q7 options: accept-batch, reject-batch-return, rework-partial-credit, conditional-accept-with-guarantee, request-more-evidence, escalate, unresolved  |  baseline: unresolved  |  machine-eligible best: rework-partial-credit
Q8 recommendation: rework-partial-credit (authority authority://inspect/adjudicate; floor-gated: ['accept-batch', 'reject-batch-return'])  ->  determination: rework-partial-credit
ACTIVE reconcile rule: independent-corroboration  |  source: rule-library  |  learned-this-run: False
why: unchanged
```

```
# §7L Q7/Q8 cockpit (engine-native) — org inspect-learn-b
Q7 options: accept-batch, reject-batch-return, rework-partial-credit, conditional-accept-with-guarantee, request-more-evidence, escalate, unresolved  |  baseline: unresolved  |  machine-eligible best: rework-partial-credit
Q8 recommendation: rework-partial-credit (authority authority://inspect/adjudicate; floor-gated: ['accept-batch', 'reject-batch-return'])  ->  determination: rework-partial-credit
ACTIVE reconcile rule: calibrated-threshold-091  |  source: learned  |  learned-this-run: True
why: reconcile threshold recalibrated lowered (relaxed: the bar demanded more than realized determinations held): prior 0.950 -> 0.910 from a realized outcome value 0.900 (variance signal -0.040, learning_rate 0.8), clamp-bounded to [0.55, 0.95]
```

```
# §7L Q7/Q8 cockpit (engine-native) — org deli-learn
Q7 options: accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline: unresolved  |  machine-eligible best: partial-settlement
Q8 recommendation: partial-settlement (authority authority://deli/adjudicate; floor-gated: ['accept-customer-refund'])  ->  determination: partial-settlement
ACTIVE reconcile rule: calibrated-threshold-091  |  source: learned  |  learned-this-run: False
why: unchanged
```

## §16 verdict

**First-class engine render, not a runner-side artifact.** The §7L Q7/Q8 line (ACTIVE rule + source + learned-or-not + why) is now `adjudication_engine.cockpit_q7q8`/`render_cockpit_q7q8` — a generic, data-only function any org config (registry / rule-library / learned this run) renders identically, reading the org's own ledger. The Sprint-16/17 cockpit report files are now a *view* over that engine render, not the only place the line exists — the engine itself carries the rule-as-operating-reality (Q7 options + Q8 recommendation with authority).

_Additive; frozen ontology, SPEC v0.22, 49 $defs. Trust only moved by S5._
