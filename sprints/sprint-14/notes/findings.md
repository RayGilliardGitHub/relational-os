# Sprint 14 — findings (dated)

**2026-09-01 (Sprint 14 build — the config-authorable reconciliation RULE layer)**

- **A rule can be generalized as a registry of pure functions whose selection + parameters are
  config — with zero ontology/schema change.** The reconciliation rule operates purely on already
  schema-valid evidence fields (`reliability`, `kind`, `captured_at`, `supports`), so compiling it
  into a set of registered pure support-mappings required NO new noun, NO schema edit, and NO new
  URI — a config-data interpretation of the existing frozen 49 `$defs`. This re-affirms the standing
  rule: accept-as-additive / config-data, never mine new nouns. `eng.RULES` + `eng.reconcile()`
  dispatch in `adjudication_engine.py`; `cfg["reconcile"]={rule,params}` (legacy flat
  `{rule,threshold,support_floor}` still accepted via `normalize_reconcile` so deli/cove configs are
  byte-untouched).
- **The engine's reconciliation check wrongly ASSUMED every main episode has rival conflict.** The
  Sprint-13 check asserted `rec["conflict"] is True`. `strict-anchor-only` legitimately produces a
  single-sided disputed set (only `passed` has admissible ANCHORED support; `failed`→0) → conflict
  False, uncertainty True. Relaxed to `rec["conflict"] or rec["uncertainty"]` (the rule reports the
  state is contested OR underdetermined) — correct for every rule and every org; deli/cove unchanged
  (both have conflict True). Lesson: a genuinely different rule shape stresses hardcoded
  single-semantic assumptions in the *driver*, not just the rule.
- **Rule-specific params must be DETERMINISTIC.** `recency-weighted-threshold` recency-decays
  evidence by `(as_of − captured_at)`; to keep a repeatable build the `as_of` reference MUST be an
  explicit RFC3339 param (never the wall-clock `now_iso()`). Evidence captured after `as_of` keeps
  full weight (factor 1.0, no negative decay); undateable/future captures treated as fresh. This is
  the same determinism discipline as the weight/ranking logic — an explicit reference, not the clock.
- **Byte-for-byte determinism can only be asserted modulo wall-clock `now_iso()` fields.** Fixtures
  embed `occurred_at`/`captured_at`/`made_at` (+ shuffled `event_id`/`idempotency_key`), which vary
  run-to-run even with an unchanged engine. Verified deli/cove reproduction by re-running the new
  engine twice and diffing after **normalizing** those timestamp/id fields → 26 files, 0 non-timestamp
  diffs. Lesson: "byte-for-byte reproducible" for this build means reproducible up to the clock; claim
  it that way in verification scripts.
- **`emit_fixtures` had a latent org-label bug (FIXED, harmless):** the dispute state-machine file
  was hardcoded to `dispute://<label>/delivery`, so even `cove` (and any non-deli org) wrote a wrong
  dispute URI into `statemachines/dispute.json`. C5 does not validate `dispute.json` (only
  relationship.json/case.json), so it never failed conformance — but it was factually wrong. Fixed to
  emit the configured `cfg["dispute"]["uri"]`. deli's URI (`dispute://deli/delivery`) is unchanged.
- **The §16 verdict can be argued "A — Yes for config-selected, registry-backed rule authoring" but
  not an unconditional text-DSL "A".** The rule *name* + *parameters* are now user-authorable config
  and a rule choice demonstrably moves a determination-vs-UNRESOLVED outcome (`inspect`: best-rel →
  rework-partial-credit; strict-anchor & recency → UNRESOLVED). What remains authored is the pure
  support-*mapping body* (a Python function in the registry), not a config-textural micro-DSL. That
  boundary is the honest seam for a clean A and is specified (not faked) as the natural Sprint-15
  step: a declarative, config-text rule spec compiled to a verified support function.

## Decisions recorded
- Keep SPEC v0.22: no normative gap, no version bump (capability/build-only change per PROTOCOL).
- New `inspect` variants deliberately NOT added to `adjudication_configs.SCENARIOS` (which stays
  `[DELI, COVE]`) and NOT to `configs.SECTORS` — driven only by `run_rule_comparison_demo.py`, so the
  Sprint-13 demo + sector build are byte-identical (non-regression proven).
- `ros/` untouched; the rule layer lives entirely in `instances/contested_reality/adjudication_engine.py`
  + config data.