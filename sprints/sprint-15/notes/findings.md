# Sprint 15 — findings (dated)

**2026-09-01 (Sprint 15 build — the declarative rule-AUTHORING layer: a rule as CONFIG TEXT)**

- **A rule's support-mapping BODY can be compiled from a declarative spec, not authored as a
  function.** `cfg["reconcile"]["rule_spec"]` = a dict (admissible evidence kinds × value_field ×
  optional recency decay × ONE fixed aggregation op) that `eng.compile_rule_spec()` validates loudly
  and `eng._spec_support()` evaluates into the SAME pure support map `_derive` consumes. The three
  registry rules are untouched; the shared `_derive` (floors/threshold) is identical for spec- and
  registry-authored rules — that sharing is what makes parity provable.
- **A spec is the SAME engine, not a different one (parity proof).** `strict-anchor-only` →
  `{aggregate:"max", value_field:"reliability", admissible_kinds:["ANCHORED"]}` and
  `recency-weighted-threshold` → `{aggregate:"max", value_field:"reliability",
  decay:{as_of, half_life_days}}` reproduce the registry per-claim support EXACTLY on the `inspect`
  dispute (`0.84/0.0` and `0.7863/0.9`), and the full dispute verdict tuple matches. Lesson: when a
  DSL is compiled onto the same shared derive + floors as existing code, "did I build a different
  engine?" is an assertable question — test it directly, don't argue it.
- **A genuinely new rule can enter the system entirely as config text.** `majority-of-sources`
  (`aggregate:"majority"`, `value_field:"reliability"`, `source_threshold:0.92`) was never a registry
  function; it is authored only as the `rule_spec` dict, drives a real lifecycle, and CHANGES the
  verdict on `inspect`: best-rel DETERMINES `rework-partial-credit` (CLOSED); majority →
  **UNRESOLVED** (OPEN, uncertainty, no claim disputed): `passed=1/2=0.5` (only the 0.97 audit clears
  the 0.92 bar), `failed=0/1=0.0` (the 0.90 testimony does not), both under `support_floor=0.55`. This
  is a real corroboration policy (many interdependent sources), genuinely distinct from any registry
  rule's support map (`0.5/0.0` vs `0.97/0.9` vs `0.84/0.0` vs `0.7863/0.9`). Zero engine Python for it.
- **The compiler MUST be strict, and it is.** An out-of-vocabulary op (`bayesian-update`), an unknown
  evidence kind (`REASONED`), an out-of-range `source_threshold`, and a non-RFC3339 `as_of` all raise
  ValueError loudly (asserted in the runner). A declarative rule layer that silently coerced unknown
  fields would be indistinguishable from a flag; strictness is the proof it is a real language. New
  findings: `validate_config` and the `run_scenario` reconcile-check message both assumed a registry
  `rule` key existed — relaxed to accept `rule_spec` (a spec is validated at config time).
- **Determinism discipline carries over unchanged.** A spec's `decay` MUST anchor to an explicit
  `as_of` (never the wall-clock); captured-after-`as_of` keeps factor 1.0; undateable treated fresh.
  Spec output is a pure function of (claims, evidence, spec, params). Fixtures remain "byte-for-byte
  up to the clock" (wall-clock `occurred_at`/`made_at` envelope fields vary run-to-run; verified by a
  normalized two-run signature equal for all 26 deli/cove files).
- **The honest frontier of the rule DSL is NOT arbitrary Python.** The vocabulary expresses the
  family "admissible filter × scalar × optional decay × one fixed aggregation" (+ shared derive). A
  rule needing an op OUTSIDE `SPEC_VOCAB` (e.g. a Bayesian posterior, a custom multiplicative
  combination, a provenance-dependent if/then) still needs that ONE primitive added to the language
  (interpreter code) — after which it serves every org by config. We did not smuggle a bespoke
  function behind the `majority` spec: `majority` is a genuine, general operator. State this plainly;
  never fake "spec-only" by hiding Python behind the config.
- **Invariants held.** SPEC hash `d10f0010…` (v0.22), schema hash `7fc38c8c…`, **49 `$defs`**,
  `ros/` git-clean, and the new spec fixtures mint only established URI schemes
  (authority/claim/db/decision/dispute/event/evidence/obligation/org/person/relationship/right/system/
  trust). deli/cove byte-identical up to the clock. Full non-regression green.

## Decisions recorded
- Keep SPEC v0.22 (no normative gap; capability/build-only change per PROTOCOL).
- The rule DSL interpreter lives inside `adjudication_engine.py` (the runtime); the NEW rule is data
  in `adjudication_configs.py` (`SPEC_AUTHORED_RULES`). This is the honest split: language runtime vs
  rules written in it.
- New spec labels (`inspect-anchor-spec`, `inspect-rec-spec`, `inspect-majority`) are NOT added to
  `SCENARIOS`/`RULE_VARIANTS` (deli/cove + Sprint-14 demo stay byte-identical); they are driven by
  `run_rule_authoring_demo.py` and covered by the extended `conformance_adjudication.py` (8 labels).
- `ros/` untouched; the layer is entirely `instances/contested_reality/`.