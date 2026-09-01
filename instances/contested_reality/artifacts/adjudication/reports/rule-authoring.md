# Sprint 15 — user-authorable RULE-authoring DSL: rules as CONFIG TEXT
generated 2026-09-01T03:58:59Z  |  one org (`inspect`), registry rules vs spec-authored rules, SAME engine

A rule declared as `cfg['reconcile']['rule_spec']` (config text) compiles to the same pure support function a registry rule runs; a NEW rule enters the system as data alone.

| label | rule source | spec aggregate | passed | failed | conflict | uncertainty | determination |
|---|---|---|---|---|---|---|---|
| `inspect-best` | registry | `best-reliability-threshold` | DETERMINED (0.97) | DISPUTED (0.9) | True | False | **rework-partial-credit** |
| `inspect-anchor` | registry | `strict-anchor-only` | DISPUTED (0.84) | UNDETERMINED (0.0) | False | True | **UNRESOLVED** |
| `inspect-rec` | registry | `recency-weighted-threshold` | DISPUTED (0.7863) | DISPUTED (0.9) | True | True | **UNRESOLVED** |
| `inspect-anchor-spec` | SPEC | `max` | DISPUTED (0.84) | UNDETERMINED (0.0) | False | True | **UNRESOLVED** |
| `inspect-rec-spec` | SPEC | `max` | DISPUTED (0.7863) | DISPUTED (0.9) | True | True | **UNRESOLVED** |
| `inspect-majority` | SPEC | `majority` | UNDETERMINED (0.5) | UNDETERMINED (0.0) | False | True | **UNRESOLVED** |

Parity (identifies whether the spec is a DIFFERENT engine):

| spec label | spec support | matches registry label | identical? |
|---|---|---|---|
| `inspect-anchor-spec` | {'claim://inspect/passed': 0.84, 'claim://inspect/failed': 0.0} | `inspect-anchor` | True |
| `inspect-rec-spec` | {'claim://inspect/passed': 0.7863, 'claim://inspect/failed': 0.9} | `inspect-rec` | True |

§7L cockpit Q7 extra line: the ACTIVE evidence-reconciliation rule for `inspect-majority` is `majority-of-sources`, and it is **spec-authored** (aggregate=`majority`, source_threshold=0.92) → UNRESOLVED.

_Additive report; frozen ontology, SPEC v0.22, 49 $defs. Trust untouched by the engine; the §6 human's determination keeps its authority; determinism asserted per run._