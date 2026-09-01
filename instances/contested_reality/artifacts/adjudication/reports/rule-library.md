# Sprint 16 — the named, cross-org RULE LIBRARY + a NEW inference primitive (`bayesian-combine`)
generated 2026-09-01T05:31:05Z  |  5 library-reuse org lifecycles  |  SPEC_VOCAB=['bayesian-combine', 'count', 'majority', 'max', 'mean', 'sum', 'weighted-mean']

Named rule specs live ONCE in `adjudication_configs.RULE_LIBRARY` and are reused by reference (the same dict) by any org — a real library, not inspect-only. The NEW `bayesian-combine` primitive is authored once in the language and serves every org as data.

## The RULE LIBRARY (named specs; `is`-shared across the orgs below)

| rule (library entry) | aggregate | reused by org(s) | active source |
|---|---|---|---|
| `independent-corroboration` | `bayesian-combine` | inspect-corroboration, cove-corroboration | **spec-authored (rule-library DATA)** |
| `majority-of-sources` | `bayesian-combine` | inspect-majority-lib, deli-majority | **spec-authored (rule-library DATA)** |

## §7L cockpit Q7 — ACTIVE rule + its source (per org)

- **inspect-majority-lib**: ACTIVE reconciliation rule = `majority-of-sources` (aggregate `majority`) — **source: spec-authored (a `RULE_LIBRARY` data dict), not an engine registry function**. Verds: disputed=[], determined=[], conflict=False, uncertainty=True → determination=UNRESOLVED.
- **deli-majority**: ACTIVE reconciliation rule = `majority-of-sources` (aggregate `majority`) — **source: spec-authored (a `RULE_LIBRARY` data dict), not an engine registry function**. Verds: disputed=['claim://deli/delivered', 'claim://deli/shipped'], determined=['claim://deli/delivered', 'claim://deli/shipped'], conflict=True, uncertainty=False → determination=partial-settlement.
- **inspect-corroboration**: ACTIVE reconciliation rule = `independent-corroboration` (aggregate `bayesian-combine`) — **source: spec-authored (a `RULE_LIBRARY` data dict), not an engine registry function**. Verds: disputed=['claim://inspect/passed', 'claim://inspect/failed'], determined=['claim://inspect/passed'], conflict=True, uncertainty=False → determination=rework-partial-credit.
- **cove-corroboration**: ACTIVE reconciliation rule = `independent-corroboration` (aggregate `bayesian-combine`) — **source: spec-authored (a `RULE_LIBRARY` data dict), not an engine registry function**. Verds: disputed=['claim://cove/medically-necessary', 'claim://cove/off-formulary'], determined=['claim://cove/medically-necessary', 'claim://cove/off-formulary'], conflict=True, uncertainty=False → determination=step-therapy-first.

## Verdict-flip proof of the NEW primitive (real reconcile output)

Same `inspect` dispute, reconcile threshold 0.98, only the rule differs:

- `inspect-max098` (max (best-reliability-threshold, registry)) → support {'claim://inspect/passed': 0.97, 'claim://inspect/failed': 0.9} → determined=[] uncertainty=True → **UNRESOLVED**
- `inspect-corroboration` (bayesian-combine (independent-corroboration, library spec)) → support {'claim://inspect/passed': 0.9961, 'claim://inspect/failed': 0.931} → determined=['claim://inspect/passed'] uncertainty=False → **rework-partial-credit**

`max` cannot clear 0.98 (strongest single witness 0.97); `bayesian-combine` of the two independent witnesses (0.84 anchored + 0.97 record) gives a posterior above 0.98 — the corroboration-synthesis semantics `max` cannot express, authorable as data by every org.

## §16 seam

Part of Sprint 15's “needs a builtin” seam NOW closes: the `bayesian-combine` op family (independent corroboration / reliability-likelihood) is in `SPEC_VOCAB`, authored once, and is thereafter authorable-as-data by any org. The residual dependence is now precisely: a rule requiring an op the vocabulary still does NOT name (a different posterior shape, a provenance-conditional if/then, a custom multiplicative combination beyond this one) still needs that one builtin added — interpreter code — after which it too serves every org by config. Authoring a rule as a `rule_spec` from the library still needs no engine Python.

_Additive report; frozen ontology, SPEC v0.22, 49 $defs. Trust untouched by the engine; the §6 human's determination keeps its authority._