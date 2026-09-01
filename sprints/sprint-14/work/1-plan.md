# work/1 — the config-authorable reconciliation rule registry

**Objective.** Generalize `reconcile()` in `adjudication_engine.py` from one hardcoded semantic into a
tiny deterministic rule registry: `RULES: name -> pure fn`. Rule **selection** becomes config
(`cfg["reconcile"]["rule"]`); a new rule = adding a `RULES` entry + a pure function, then selecting it
from config. Default `best-reliability-threshold` must reproduce today's deli/cove output
byte-for-byte.

## Design
- Registry `RULES = {"best-reliability-threshold": _rule_best_rel, "strict-anchor-only": _rule_strict_anchor, "recency-weighted-threshold": _rule_recency}` (module constant, distinct names — avoid shadowing).
- Rule contract: `fn(ctx, params) -> verdict`; `ctx={"claims", "supporting":{claim_uri:[evidence...]}, "sub"}`; verdict `{"claim_support":{uri:float}, "disputed":[uris], "conflict":bool, "determined":[uris], "uncertainty":bool}`.
- Shared `_derive(sup, params)`: `disputed=sup>=support_floor`; `conflict=len(disputed)>=2`;
  `determined=sup>=threshold`; `uncertainty=not determined`. Uniform dispute semantics; the rule is the
  support mapping.
- `_rule_best_rel` = VERBATIM current logic (iterate `cfg` claims in order, `max reliability` of
  supporting refs, `round(.,4)`), returning `_derive(sup, params)` → byte-identical claim_support &
  derived verdicts.
- `_rule_strict_anchor`: support = max reliability among supporting evidence whose `kind` ∈ params
  `kinds` (default `["ANCHORED"]`); everything else → 0.
- `_rule_recency`: support = max over supporting of `reliability * 0.5**((as_of−captured).days/half_life_days)`;
  requires **explicit `as_of`** (RFC3339) + `half_life_days` in params → deterministic, no `now_iso` clock.
  Evidence with captured_at after as_of → factor 1.0 (no negative decay). Parse RFC3339 datetimes.
- `validate_config`: replace `assert rule == "best-reliability-threshold"` with `assert rule in RULES`.
- `normalize_reconcile(rc)`: if `rc.get("params")` use it, else merge `{k:v for k,v in rc.items() if k!="rule"}` → params. Backward compatible with existing deli/cove blocks.
- `reconcile(sub, cfg)`: dispatch via registry; unknown rule raises loudly listing available rules.
- `run_scenario`: reconcile-check message names `cfg["reconcile"]["rule"]` dynamically (was hardcoded,
  stdout-only, no fixture effect).

## DoD
- `python3 run_adjudication_engine_demo.py` from `instances/contested_reality` → RESULT: ALL PASS.
- deli/cove fixtures byte-identical vs baseline `/tmp/fx_baseline.sha` (sha256sum diff empty).
- No schema edit; SPEC hash unchanged; 49 `$defs` intact.