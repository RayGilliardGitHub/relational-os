# Sprint 15 — plan

**Goal.** Make the evidence-reconciliation RULE **body** authorable as config TEXT — a small,
deterministic, declarative **rule-authoring spec** (a dict of rule data) that the engine *compiles*
into the identical pure support function the registry runs today — so a NEW rule is added **entirely
as data/text with NO engine Python authored for it**. Then re-test Sprint 14's §16 verdict
("argued A — Yes for config-selected, registry-backed rule authoring; the rule BODY is still Python")
for a clean, unconditional text-DSL **"A — Yes"**.

The Sprint-14 runner already proved rule *selection* + *parameters* are config and a rule choice
flips a verdict with zero engine change. The residual hinge is the rule's pure support-*mapping body*:
today that is a Python function in `eng.RULES`. Sprint 15 closes it by adding a small declarative
rule-authoring language to the engine and proving at least two existing rules re-expressed as specs
reproduce their registry verdicts, plus one genuinely NEW rule added *only as a spec* (never a
registry function) that drives a real, distinct verdict.

**Baseline locked (real hashes + output, 2026-09-01):**
- SPEC.md `d10f00107b5d7eb4652a0cd595413b83a272f008284ff70819270d9664699122` (**v0.22, never bump**).
- schema `sprints/sprint-0/artifacts/schema/relational-os.schema.json`
  `7fc38c8c0a6e5b76cd55393f2c732417675b224812970951778853a6677642c4`, **49 `$defs`** (frozen ontology).
- `ros/` git-clean (untouched); SPEC/schema canonical.
- Full green baseline (all exit 0): `run_rule_comparison_demo.py` (3 rules, verdict flip),
  `run_adjudication_engine_demo.py` (deli/cove), `conformance_adjudication.py` (5 labels, C1–C5),
  the 4 prior contested-reality demos + conformances (dispute/interest/tradeoff/lifecycle),
  sectors `build_all.py` + `conformance_all.py`, S5 reference `run_s5_demo.py` + `run_s5_conformance.py`,
  agent `run_agent_demo.py` + `conformance_agent.py`.

## Hard invariants
- Frozen ontology: 49 `$defs` + URI cap + SPEC v0.22 byte-identical. Additive fields only. No new noun.
- Trust only moved by the deterministic S5 formula; the engine never writes Trust. The §6 human
  keeps the authoritative determination (§7J.9).
- The rule-authoring layer is engine-internal (a DSL interpreter inside `adjudication_engine.py` +
  rule data in `adjudication_configs.py`) — NOT a new service, NOT a new scheme, NOT a schema edit.
- Single-threaded; plan before build; real tool output only; ~$0 deterministic local Python.
- **Honesty:** authoring a genuinely new rule must be *spec data only*. The DSL interpreter's
  primitive vocabulary is engine code (any DSL has a runtime) and is authored ONCE; a NEW RULE is a
  spec dict and reuses that vocabulary. A rule that genuinely needs a primitive OUTSIDE the shipped
  vocabulary (e.g. a Bayesian posterior) still needs a new builtin — say so plainly, never fake it.
- deli/cove (registry `best-reliability-threshold`) must stay byte-for-byte reproducible.

## The residual hinge Sprint 15 closes
Sprint 14 made `cfg["reconcile"]={"rule", params}` and the rule `SELECTION` + every `PARAMETER`
config; the rule BODY stayed a Python function in `eng.RULES`. Sprint 15 makes the rule BODY a
declarative spec: `cfg["reconcile"]={"rule_spec": {...}}` (or alongside a registry rule name / params).
The engine carries a tiny deterministic **rule-authoring DSL interpreter** (fixed primitive
vocabulary: evidence `admissible_kinds` filter, scalar `value_field` extraction
(reliability / confidence / reliability×confidence), optional recency `decay` against an explicit
`as_of`, and a fixed `aggregate` op set incl. `max`, `mean`, `weighted-mean`, and a `majority`
per-source-threshold vote — all folded through the SHARED `_derive` floors). A spec dict selects +
configures these primitives; `compile_rule_spec()` validates and returns the same pure
`{claim_support, …}` support map a registry function returns. Adding a new rule = adding a spec dict
IN CONFIG — no engine Python.

## Sub-sprints
**work/1 — the declarative rule-authoring DSL (interpreter + compile).**
- In `adjudication_engine.py`: define the rule-spec format + `compile_rule_spec(spec, params)` and a
  tiny fixed `SPEC_OPS` vocabulary (validate loudly against it). Extend `reconcile()` to accept a
  `cfg["reconcile"]["rule_spec"]` in addition to a registry `rule`. Keep the registry rules exactly
  as-is (deli/cove byte-identical). `normalize_reconcile` still merges flat `threshold`/`support_floor`
  so derive floors come from the same params path for both spec- and registry-authored rules.
- DoD: `python3 run_adjudication_engine_demo.py` (deli/cove) unchanged ALL PASS; fixtures byte-identical.

**work/2 — parity: re-express `strict-anchor-only` and `recency-weighted-threshold` as specs and show
verdicts MATCH the registry (a spec is the same engine, not a different one).**
- Add spec-authored variants of the inspect dispute: `inspect-anchor-spec` and `inspect-rec-spec`
  (reconcile uses `rule_spec` that reproduces anchor / recency semantics), plus the genuinely NEW
  spec-only `inspect-majority` using a `majority` aggregation the registry never had.
- New `run_rule_authoring_demo.py`: runs registry anchor/rec vs spec anchor/rec and asserts IDENTICAL
  per-claim support + dispute verdicts; runs the NEW spec-only `majority` rule and asserts its
  per-claim support map is distinct from ALL registry rules and produces a real verdict, designed to
  flip inspect to **UNRESOLVED** (vs best-rel → `rework-partial-credit`) — a rule entered the system
  through config text alone and changed the verdict. Emits fixtures for the new labels.
- DoD: new runner ALL PASS, exit 0; parity proven; new rule real.

**work/3 — conformance + full non-regression.**
- Extend `conformance_adjudication.py` labels to also validate the new spec-authored fixtures
  (C1–C5, Sprint-0 venv). Re-run the new runner + conformance, Sprint-13 adjudication demo &
  conformance (deli/cove + 3 inspect registry variants byte-identical), the 4 prior CR demos +
  conformances, sectors build+conformance, S5 reference+conformance, agent demo+conformance.
- Verify 49 `$defs` / URI cap / SPEC v0.22 + `ros/` untouched (hashes, defs count, no new scheme).

**work/4 — documentation + hand-off.**
- `docs/USER-AUTHORABLE-RULE-DSL.md` (the rule-authoring format; the expressiveness frontier — what a
  declarative spec covers, what it cannot and would still need a builtin primitive; the §16 verdict
  and on what, precisely, it now holds). Update `instances/README.md`; append "Update after Sprint 15"
  to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; append a note to the
  Sprint-14 `docs/USER-AUTHORABLE-RULE-LAYER.md` that its rule-BODY boundary is addressed.
- Write `sprints/sprint-15/summary.md` + `notes/findings.md`; the next prompt
  `sprints/sprint-16/PROMPT.md`.

## Definition of Done (all exit 0)
- Green baseline first (real output above) ✓.
- ≥2 rules authored purely as spec-config (strict-anchor, recency) each drive a real lifecycle and
  reproduce the registry verdicts exactly (parity, not a different engine).
- The SAME engine runs a **genuinely new spec-only rule** (`majority-of-sources`) that was never a
  registry function and produces a real, distinct verdict (inspect: support 0.50/0.0, UNRESOLVED vs
  best-rel rework-partial-credit). Rule added wholly as config text — zero new engine Python for it.
- deli/cove byte-identical with their original rule; C1–C5 over the new fixtures green; full
  non-regression green.
- 49 `$defs`, URI cap, SPEC v0.22 intact; `ros/` untouched.
- Honest §16 stance: argue **A — Yes** unconditionally ONLY if a new rule is added entirely through
  config/text composing the shipped vocabulary; state precisely which out-of-vocabulary shapes (e.g.
  Bayesian) would still need a new builtin primitive (and that a new primitive then serves all orgs).