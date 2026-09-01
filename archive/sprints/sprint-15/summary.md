# Sprint 15 — summary

**Goal.** Close Sprint 14's §16 hinge: make the evidence-reconciliation RULE **body** authorable as
**config text** (a small declarative rule-authoring spec compiled by the engine into the same pure
support function the registry runs), so a NEW rule is added **entirely as data with NO engine Python
for it** — then re-test the §16 verdict for a clean text-DSL **"A — Yes."** Done: the rule BODY is
now a declarative spec; a genuinely new rule enters the system through config alone and changes a
verdict. Additive, frozen ontology, SPEC v0.22, ~$0.

## What was built (instances/contested_reality/)
- **The rule-authoring DSL** in `adjudication_engine.py`: `cfg["reconcile"]["rule_spec"]` declares a
  rule as data — admissible evidence **kinds** × **value_field** (reliability/confidence/×product) ×
  optional recency **decay** (explicit `as_of`) × ONE fixed aggregation op (`eng.SPEC_VOCAB`:
  max/mean/weighted-mean/sum/count/majority) — folded through the **same** shared `_derive` the
  registry rules use. `compile_rule_spec` validates loudly; `_spec_support` evaluates deterministically.
  The three registry rules + `_derive` are untouched (deli/cove byte-identical up to the clock).
- **`adjudication_configs.py`:** three spec-authored variants of the `inspect` org — `strict-anchor-only`
  as a spec, `recency-weighted-threshold` as a spec, and a genuinely NEW
  **`majority-of-sources`** rule that was never a registry function.
- **`run_rule_authoring_demo.py`** (exit 0 = ALL PASS): proves (a) **parity** — the two spec rules
  reproduce the registry support + dispute verdicts exactly (a spec is the same engine, not a
  different one); (b) **a genuinely new spec-only rule** drives a real lifecycle with a real, distinct,
  verdict-changing result; (c) the compiler is strict (out-of-vocabulary op / kind rejected).
- **`conformance_adjudication.py`** now validates **8 labels** (deli, cove, inspect-best/anchor/rec +
  inspect-anchor-spec/rec-spec/majority), C1–C5 green, 49 `$defs`.
- **`docs/USER-AUTHORABLE-RULE-DSL.md`** (format + expressiveness frontier + §16).

## Verified output (all exit 0, ALL PASS)
- **Parity:** spec `strict-anchor` == registry (`passed 0.84 / failed 0.0`); spec `recency` == registry
  (`passed 0.7863 / failed 0.9`); full dispute verdict equal for each.
- **Genuinely-new spec-only rule:** `majority-of-sources` (config text only) gives support `0.5/0.0`,
  distinct from all three registry rules, and flips `inspect` from best-rel DETERMINED
  `rework-partial-credit` (CLOSED) to **UNRESOLVED** (OPEN, uncertainty, no claim disputed). Rule
  entered the system purely as a `rule_spec` dict; zero engine Python for it.
- **Compiler strictness + determinism:** `bayesian-update` op and `REASONED` kind rejected loudly;
  same spec compiles identically on re-run. Trust unchanged (0.80) under every rule; authority
  preserved; rankings deterministic; every variant ends in a lawful terminal state.
- **Sprint-13/14 reproductions:** `run_adjudication_engine_demo.py` (deli/cove) ALL PASS and
  byte-identical up to the clock; `run_rule_comparison_demo.py` (3 registry rules, verdict flip) ALL
  PASS. **Conformance:** 8 labels C1–C5 ALL PASS. **Full non-regression:** the 4 prior CR demos +
  conformances, sectors `build_all.py` + `conformance_all.py`, S5 reference demo + all-six conformance,
  agent demo + conformance — all exit 0.
- **Frozen invariants:** SPEC.md hash `d10f0010…` (v0.22) unchanged; schema hash `7fc38c8c…`, 49
  `$defs`; `ros/` git-clean; new fixtures mint only established URI schemes (no new noun/cap break).

## §16 verdict
Moves from Sprint 14's **argued "A — Yes" for config-selected, registry-backed rule authoring** to a
clean **A — Yes for declarative, config-text rule authoring over the shipped `SPEC_VOCAB`.**
The rule **body** is now authorable as data, and a genuinely new rule (`majority-of-sources`)
enters the system with **no engine Python** and changes a determination-vs-UNRESOLVED verdict —
exactly the boundary Sprint 14 named as the seam for a clean A. The one honest qualifier: "A — Yes" is
scoped to the DSL's vocabulary; a rule needing an op *outside* `SPEC_VOCAB` (e.g. a Bayesian posterior)
still requires adding that one builtin to the language (then authorable as data by every org). That
seam is disclosed precisely, not concealed.

## Open issues / next work
- Extending `SPEC_VOCAB` (e.g. a Bayesian/reliability-likelihood aggregate) would broaden the DSL's
  expressiveness frontier; that is an additive primitive, not a requirement for the Sprint-16 hand-off.
- Optional (deferred, not required): surface the active rule + "spec-authored (vs registry-authored)"
  flag on a §7L cockpit-Q7 line within the rule-authoring runner (the report already names the rule
  and its source; a cockpit render is a small follow-up).

## Docs touched (no SPEC bump)
- `contested_reality/docs/USER-AUTHORABLE-RULE-DSL.md` (new), `USER-AUTHORABLE-RULE-LAYER.md` (Sprint-14,
  appended "rule-BODY boundary addressed")
- `instances/README.md` (Sprint-15 entry)
- `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` ("Update after Sprint 15")
- `sprints/sprint-15/plan.md`, `work/1-plan.md`, `notes/findings.md`, `summary.md`
- `sprints/sprint-16/PROMPT.md` (next prompt)
- `instances/contested_reality/`: `adjudication_engine.py`, `adjudication_configs.py`,
  `run_rule_authoring_demo.py`, `conformance_adjudication.py`