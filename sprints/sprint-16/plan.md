# Sprint 16 — plan

**Goal.** Take on Sprint 15's disclosed seam and make the rule-authoring vocabulary a reusable,
cross-org **RULE LIBRARY**: (a) add **≥1 genuinely NEW inference primitive** to `SPEC_VOCAB`,
authored ONCE as a real, general, deterministic + strict operator; (b) make spec-authored rules a
**named, reusable cross-org library** (the SAME named rule reused on view≥2 DIFFERENT orgs/disputes,
not inspect-only); (c) surface the **ACTIVE rule + spec-authored-vs-registry source** on a §7L
cockpit **Q7** line in the rule-authoring runner/report. Then re-test whether the "needs a builtin"
seam closes for the added primitive.

**Baseline locked (real hashes + output, 2026-09-01):**
- SPEC.md `d10f00107b5d7eb4652a0cd595413b83a272f008284ff70819270d9664699122` (**v0.22, never bump**).
- schema `sprints/sprint-0/artifacts/schema/relational-os.schema.json`
  `7fc38c8c0a6e5b76cd55393f2c732417675b224812970951778853a6677642c4`, **49 `$defs`** (frozen ontology).
- `ros/` source untracked-modified count 0 (git clean); SPEC/schema clean.
- Full green baseline (real exit-0, run above): `run_rule_authoring_demo.py` (ALL PASS),
  `run_rule_comparison_demo.py` (ALL PASS), `run_adjudication_engine_demo.py` (ALL PASS, deli/cove),
  `conformance_adjudication.py` (8 labels ALL PASS), sectors `build_all.py` +
  `conformance_all.py` (ANY SECTOR/ALL PASS), agent `run_agent_demo.py` + `conformance_agent.py`,
  S5 reference `run_s5_demo.py` + `run_s5_conformance.py`.

## What is added (all in `instances/contested_reality/` — engine, configs, runner, conformance, docs)

### (a) A genuinely NEW vocabulary primitive: `bayesian-combine`
A **reliability-likelihood posterior** op — the exact family Sprint 15's frontier said needed a new
builtin. It combines the per-source values (each treated as `P(claim | source_i)`, independent given
the claim) under Bayes with an explicit author-`prior`:
```
posterior = odds/(1+odds),  odds = odds(prior) · Π_i (v_i / (1 − v_i))
```
- **Expresses what the old vocabulary could NOT:** `max` can never exceed the single strongest
  witness; `bayesian-combine` lets *many weak-but-independent* sources raise support ABOVE every
  individual source — true independent-corroboration synthesis. That is provable on inputs where
  max < threshold < bayesian-posterior.
- **Deterministic:** all params explicit (`prior` in (0,1)); no wall-clock. Empty source set →
  posterior = `prior` (no evidence → prior). A `1.0` source → posterior 1.0; a `0.0` source → 0.0
  (a certain source pins the claim); else the odds combination.
- **Strict (validated loudly):** `compile_rule_spec` requires `0 < prior < 1` and rejects missing /
  out-of-range / non-numeric `prior`; unknown op still rejected. Runtime is a pure function of
  (sources, prior).
- Weight (`verity.confidence`) is deliberately NOT used — each independent source contributes one
  equal likelihood, a distinct semantic from `weighted-mean`.

### (b) A named, reusable cross-org RULE LIBRARY (`adjudication_configs.RULE_LIBRARY`)
Named rule specs defined once, referenced by name by ANY org config:
`{ "majority-of-sources", "independent-corroboration" (=bayesian-combine, prior given), and the two
parity specs strict-anchor-only / recency-weighted-threshold }`. org drivers reuse the SAME dict.
- `majority-of-sources` driven on **`inspect`** (existing) AND a **`deli`-based second dispute** →
  cross-org reuse (goods-QC + freight), a real rule library, not inspect-only.
- `independent-corroboration` (the NEW primitive) driven on **`inspect`** (a REAL verdict flip: at
  reconcile threshold 0.98, best-rel's single-source max 0.97 clears nothing → **UNRESOLVED**;
  bayesian-combine of the passed claim's 0.84+0.97 anchored/record witnesses → ≥0.98 →
  **determined rework-partial-credit CLOSED**) and on **`cove`** (the same named rule usable as data
  by a second, genuinely different org) — proving the new primitive is general, not single-org.
- deli/cove original configs stay registry `best-reliability-threshold` (byte-identical invariant);
  the library reuse runs under NEW variant labels (the established Sprint-14 `inspect_variant`
  pattern), so SCENARIOS / RULE_VARIANTS / SPEC_AUTHORED_RULES are untouched and the Sprint-15
  runner + 8-label conformance stay green.

### (c) Cockpit §7L Q7 — ACTIVE rule + source
New `run_rule_library_demo.py` renders per-org a cockpit-Q7 block naming the **ACTIVE rule** (name)
and its **source: spec-authored (rule-library data) vs registry (engine function)**, plus a
§16 line. Mirrors the existing `cockpit-q7-*.md` report shape (additive).

## Hard invariants (never violate)
- Frozen ontology: 49 `$defs` + URI cap + SPEC v0.22 byte-identical. Additive fields only. No new
  noun / no `bayesian://` scheme. Schema untouched.
- Trust only moved by the deterministic S5 formula; the engine never writes Trust. The §6 human
  keeps the authoritative determination (§7J.9).
- The whole layer is engine-internal + config data in `instances/contested_reality/` — NOT a new
  service. `ros/`, reference build, schema, the 12+ sectors, agent, S5 all untouched.
- Single-threaded; plan before build; real tool output only; ~$0 deterministic local Python.
- **Honesty:** the NEW primitive must be a genuine, general operator (a real likelihood-combination
  semantics), validated loudly, deterministic — NEVER a rule-specific function hidden behind the
  config (`_aggregate` implements one general op; rules reuse it as data). If it only served one
  contrived rule I would say so and not fake generality. It is general.
- deli/cove stay byte-identical up to the clock under their registry rule.

## Sub-sprints
**work/1 — the new primitive + the rule library (engine + configs).**
- `adjudication_engine.py`: add `bayesian-combine` to `SPEC_VOCAB`; implement it generally in
  `_aggregate`; extend `compile_rule_spec` to require `0 < prior < 1` loudly. Registry rules +
  shared `_derive` untouched.
- `adjudication_configs.py`: add `RULE_LIBRARY` (named specs incl. `independent-corroboration` with
  `prior`); add library-reuse org variants (a deli variant under `majority-of-sources`; inspect +
  cove variants under `independent-corroboration`) reusing the SAME library dict entries. SCENARIOS/
  RULE_VARIANTS/SPEC_AUTHORED_RULES untouched.
- DoD: `run_rule_authoring_demo.py` + `run_rule_comparison_demo.py` + `run_adjudication_engine_demo.py`
  still ALL PASS and deli/cove byte-identical up to the clock.

**work/2 — the rule-library runner (`run_rule_library_demo.py`).**
- Prove the primitive: unit asserts that `bayesian-combine` posterior EXCEEDS `max` on synthetic
  weak-multi-source inputs (the property no old op has); assert strict rejection of bad `prior`.
- Drive orgs: `majority-of-sources` on inspect + deli (cross-org reuse); `independent-corroboration`
  on inspect (real flip: UNRESOLVED at 0.98 under best-rel/max → DETERMINED rework-partial-credit
  under bayesian) and on cove. Assert the flip with real reconcile output.
- Cockpit Q7: report block + printed line per org naming ACTIVE rule + spec-vs-registry source.
- Emit fixtures for the new labels.
- DoD: runner ALL PASS, exit 0; cross-org reuse proven; new primitive real + strict + deterministic.

**work/3 — conformance + full non-regression.**
- Extend `conformance_adjudication.py` labels to cover the new library fixtures (C1–C5, Sprint-0 venv).
- Re-run new runner + conformance + every prior suite: rule_authoring / rule_comparison / adj_engine /
  the 4 prior CR demos + conformances, sectors build_all + conformance_all, S5 reference+conformance,
  agent demo+conformance — all exit 0. Verify 49 `$defs` / URI cap / SPEC v0.22 + `ros/` untouched
  (hashes, defs count, no new scheme, no `qk` leak).

**work/4 — documentation + hand-off.**
- `docs/USER-AUTHORABLE-RULE-LIBRARY.md` (the library format, the new primitive's semantics + what it
  expresses the old vocab could not, cross-org reuse proof, cockpit Q7 surface, updated
  expressiveness frontier + residual seam, §16 verdict). Additive "Update after Sprint 16" to
  `docs/USER-AUTHORABLE-RULE-DSL.md` verification/frontier section, `instances/README.md` (Sprint-16
  entry), and `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`.
- `sprints/sprint-16/summary.md` + `notes/findings.md`; next prompt `sprints/sprint-17/PROMPT.md`.

## Definition of Done (all exit 0)
- Green baseline first (locked above) ✓.
- `SPEC_VOCAB` gains ≥1 genuinely NEW, deterministic + strict general primitive
  (`bayesian-combine`) authored once; a new rule authored as a spec that USES it and drives an org
  with a real verdict (inspect: UNRESOLVED → rework-partial-credit flip at threshold 0.98).
- The SAME named library rule reused on ≥2 DIFFERENT orgs (`majority-of-sources` on inspect + deli;
  `independent-corroboration` on inspect + cove) — a real rule library, not inspect-only.
- Cockpit Q7 line names the ACTIVE rule + spec-authored-vs-registry source.
- New primitive deterministic + strict (bad `prior` rejected loudly); C1–C5 over new fixtures green;
  full non-regression green; 49 `$defs` / URI cap / SPEC v0.22 / `ros/` untouched; deli/cove
  byte-identical.
- §16 argued: the `bayesian-combine` op is now authorable-as-data → part of the old seam closes;
  state precisely what still depends on a builtin (any op the vocabulary still cannot express).