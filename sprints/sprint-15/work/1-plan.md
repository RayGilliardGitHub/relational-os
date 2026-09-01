# Sprint 15 — work/1: the declarative rule-authoring DSL (interpreter + compile)

**Objective.** Add to `adjudication_engine.py` a small, deterministic declarative **rule-authoring
spec** format and a compiler that turns a config dict into the same pure `{claim_support, …}` support
map the registry rules produce — extending `reconcile()` so `cfg["reconcile"]` may carry a
`rule_spec` (a rule authored as data) in addition to a registry `rule` name. The registry rules and
the shared `_derive` are untouched, so deli/cove remain byte-for-byte reproducible.

## The rule-spec format (config data)
```python
cfg["reconcile"] = {
  "rule_spec": {
    "name": "strict-anchor-only",                 # informational
    "aggregate": "max" | "mean" | "weighted-mean" | "majority" | "sum" | "count",
    "value_field": "reliability" | "confidence" | "reliability_x_confidence",
    "admissible_kinds": None | ["RECORD", ...],   # None = every Evidence.kind admissible
    "source_threshold": float,                    # only used when aggregate == "majority"
    "decay": None | {"as_of": "RFC3339", "half_life_days": N},  # optional recency weighting
  },
  # threshold / support_floor MAY sit inside rule_spec or flat here (normalize_reconcile merges) —
  # the SHARED _derive floors, identical for spec- and registry-authored rules.
}
```
A spec selects **fixed** primitives in `eng.SPEC_OPS` (the DSL vocabulary); `compile_rule_spec()`
validates loudly (unknown op / field / kind ⇒ exception, never silent coercion), applies the
admissible-kind filter, extracts the scalar, applies optional recency decay, aggregates per claim, and
hands the per-claim `sup` to the **same** `_derive(_, params)`. After compile a spec rule is
indistinguishable from a registry rule in shape — that is the parity guarantee.

## Engine changes (additive, no registry rule touched)
1. `_spec_value(ev, value_field)` — extract the scalar to aggregate (missing → 0.0).
2. `_spec_decay(ev, decay)` — deterministic `0.5**(days/half_life)` against the spec `as_of`
   (same semantics as `_rule_recency`).
3. `SPEC_OPS` — fixed vocabulary dict {op_name → pure fn(sv, params)}:
   - `max` → max of transformed values; `mean` → arithmetic mean (0 if none); `sum`;
     `count` → number of admissible sources; `weighted-mean` → mean weighted by `confidence`;
     `majority` → (# admissible sources with value ≥ source_threshold) ÷ max(1, # admissible sources).
4. `compile_rule_spec(rc)` → validates the spec then returns a callable `fn(ctx, params) -> verdict`
   that builds `sup` and calls shared `_derive` (so dispute semantics stay uniform).
5. `reconcile()` — if `rule_spec` in rc → `compile_rule_spec`; elif `rule` → registry lookup; else
   loud error. `normalize_reconcile` unchanged (still merges flat threshold/support_floor into params).

## Determinism
Use only explicit `as_of` (never wall-clock) inside a spec's `decay`; evidence captured after `as_of`
keeps full weight (factor 1.0, no negative decay); undateable capture treated fresh. Outputs are pure
functions of (claims, evidence, spec, params) — repeatable across runs up to the embedded
`now_iso()` envelope fields in the fixtures.

## DoD (this sub-sprint)
- `python3 run_adjudication_engine_demo.py` (deli/cove, registry rules) unchanged → ALL PASS, exit 0.
- Fixture-hash diff vs committed deli/cove baseline → empty (byte-for-byte up to wall-clock).
- `MAJORITY` aggregation validated + compile of anchor/rec/majority specs succeeds deterministically.