# Sprint 14 — config-authorable reconciliation rule layer: rule → verdict
generated 2026-09-01T02:11:11Z  |  one org (`inspect`), three configured rules, SAME engine, only `reconcile` differs

A claim that is DISPUTED/determined/UNDETERMINED depends on which rule the org configured:

| rule (cfg['reconcile']) | passed | failed | conflict | uncertainty | determination |
|---|---|---|---|---|---|
| `best-reliability-threshold` | DETERMINED (0.97) | DISPUTED (0.9) | True | False | **rework-partial-credit** |
| `strict-anchor-only` | DISPUTED (0.84) | UNDETERMINED (0.0) | False | True | **UNRESOLVED** |
| `recency-weighted-threshold` | DISPUTED (0.7863) | DISPUTED (0.9) | True | True | **UNRESOLVED** |

§7L cockpit Q7 extra line (rule choice): the active evidence-reconciliation rule is `inspect-best` → `best-reliability-threshold` → rework-partial-credit | `inspect-anchor` → `strict-anchor-only` → UNRESOLVED | `inspect-rec` → `recency-weighted-threshold` → UNRESOLVED

_Additive report; frozen ontology, SPEC v0.22, 49 $defs. Trust untouched by the engine; the §6 human's determination keeps its authority; determinism asserted per run._