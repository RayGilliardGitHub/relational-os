# Sprint 16 — findings (dated)

**2026-09-01 (Sprint 16 build — the new `bayesian-combine` primitive + the named cross-org RULE LIBRARY)**

- **A genuinely NEW inference primitive can extend the rule-authoring vocabulary as ONE general,
  deterministic, strict operator — not rule-specific Python hidden behind the config.**
  `bayesian-combine` was added to `SPEC_VOCAB` and implemented in `_aggregate` as a real
  reliability-likelihood posterior: `O = odds(prior) * Π_i (v_i/(1-v_i))`, `posterior = O/(1+O)`.
  It requires an explicit `0 < prior < 1` (rejected loudly when missing/≤0/≥1/non-numeric), empty
  sources → posterior = prior, a `1.0` source → 1.0, a `0.0` source → 0.0. The per-source
  `verity.confidence` weight is deliberately unused — each independent source contributes ONE equal
  likelihood (distinct from `weighted-mean`). Nothing else in the engine changed; the 3 registry
  rules + shared `_derive` are untouched, deli/cove byte-identical.
- **The closed seam is real and unit-provable.** The primitive expresses the corroboration-synthesis
  family `max` cannot: `bayesian-combine(3×0.7, prior 0.7) = 0.9674 > max = 0.7` — many weak
  independent sources exceed ANY single strong source. This is exactly the "Bayesian posterior
  needs a builtin" example Sprint 15's frontier named; the builtin is now shipped, and the op is
  authorable as data by every org.
- **The new primitive produces a REAL verdict flip on real org data, changing ONLY the rule.**
  On the `inspect` dispute at reconcile threshold 0.98: registry `best-reliability-threshold` (`max`)
  tops out at 0.97 (the strongest witness) and clears nothing → **UNRESOLVED**; the same org under
  the library spec `independent-corroboration` combines its two independent witnesses (0.84 anchored
  + 0.97 record) to posterior **0.9961** ≥ 0.98 → **DETERMINED `rework-partial-credit` (CLOSED)**.
  Same ledger/evidence/threshold; only `reconcile.rule_spec` differs. `max` cannot reach this; the
  new primitive can, with zero engine Python per rule.
- **A rule library needs a NAMED place + `is`-identity to be a library, not a provenance claim.**
  `ac.RULE_LIBRARY` holds named specs created once; `org_under_library_rule(cfg, label, rule, params)`
  reuses the SAME dict object (asserted by `is`, not equality). Cross-org reuse is proven both by
  identity AND by driving each library rule on ≥2 genuinely different orgs/test disputes:
  `majority-of-sources` on `inspect-majority-lib` + `deli-majority` (goods-QC and freight;
  UNRESOLVED vs partial-settlement); `independent-corroboration` on `inspect-corroboration` +
  `cove-corroboration` (goods-QC and clinical; rework-partial-credit / step-therapy-first).
- **The §7L cockpit Q7 surface is a small additive render, not an engine change.** The runner prints
  and writes a Q7 line per org naming the ACTIVE rule + `source: spec-authored (a RULE_LIBRARY data
  dict) / registry (engine function)`; the library table + verdict-flip pitch live in
  `rule-library.{md,json}` + `cockpit-q7-rule-library.md`. Mirrors the Sprint-13 cockpit-Q7 shape.
- **Conformance scales by label list, not new code.** The 5 new fixture families
  (`inspect-majority-lib`, `deli-majority`, `inspect-corroboration`, `cove-corroboration`,
  `inspect-max098`) pass the SAME C1–C5 validator (Sprint-0 venv) as the prior 8 — the frozen
  49 `$defs` + URI cap absorb them additively, and `grep` shows the new fixtures mint only catalog
  schemes (authority/claim/db/decision/dispute/event/evidence/obligation/org/person/relationship/
  right/system/trust). No new noun, no schema edit.
- **Invariants held.** SPEC hash `d10f0010…` (v0.22), schema hash `7fc38c8c…`, **49 `$defs`**,
  `ros/` source untracked-modified 0 (git clean), deli/cove byte-identical under their registry rule,
  full non-regression green (rule_authoring / rule_comparison / adj_engine, the 4 prior CR demos +
  conformances, sectors build_all + conformance_all, S5 reference + conformance, agent demo +
  conformance — all exit 0), and `conformance_adjudication.py` → ALL PASS over **13 labels**.

## Decisions recorded
- Keep SPEC v0.22 (capability/build change, no normative gap → PROTOCOL). No schema edit; the new
  vocabulary primitive is interpreter code inside `adjudication_engine.py`, and the new RULE is data
  in `adjudication_configs.py` `RULE_LIBRARY`. This is the honest split: language runtime vs rules
  written in it.
- The library-reuse orgs run under NEW labels (the established `inspect_variant` pattern); DELI, COVE,
  SCENARIOS, RULE_VARIANTS, SPEC_AUTHORED_RULES are untouched so the Sprint-13/14/15 runners stay
  byte-identical.
- `best-reliability-threshold` at 0.98 is driven as a real lifecycle (`inspect-max098`) to capture
  the UNRESOLVED outcome as real output — not just a derived reconcile.
- `ros/` untouched; the layer is entirely `instances/contested_reality/`.