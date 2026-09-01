# Sprint 14 — plan

**Goal.** Make the evidence-reconciliation RULE layer itself config-authorable (a tiny deterministic
rule registry in the engine, where a new rule = a registry entry + a pure function, selected from
config with NO engine-side code change for the new rule), re-exercise ≥2 distinct rules so a rule
choice demonstrably changes a verdict, and re-test Sprint 13's §16 verdict ("B+ — materially toward
A") for a clean all-config "A — Yes".

**Baseline locked (Sprint-13 state, real hashes captured 2026-08-31/09-01):**
- SPEC.md `d10f00107b5d7eb4652a0cd595413b83a272f008284ff70819270d9664699122` (v0.22, never bump).
- schema `sprints/sprint-0/artifacts/schema/relational-os.schema.json` hash
  `7fc38c8c0a6e5b76cd55393f2c732417675b224812970951778853a6677642c4`, **49 `$defs`** (frozen ontology).
- deli/cove adjudication fixtures: 26 files, hashes in `/tmp/fx_baseline.sha` — must stay byte-identical.
- All green-baseline runners exit 0 (adjudication demo+conformance, 4 prior CR demos+conformance,
  sectors build+conformance, S5 reference+all-six, agent demo). `ros/` untouched.

## Hard invariants
- Frozen ontology: 49 `$defs` + URI cap + SPEC v0.22 byte-identical. Additive fields only. No new noun.
- Trust only moved by the deterministic S5 formula; the engine never writes Trust.
- Rule layer is engine-internal (a registry + pure functions) — NOT a new service, NOT a new scheme,
  NOT a schema edit. Spec v0.22 unchanged.
- Single-threaded; plan before build; real tool output only; ~$0.

## The residual hinge Sprint 14 closes
Sprint 13's `reconcile()` is one named semantic (`best-reliability-threshold`); only its *parameters*
(threshold, support_floor) were config. A genuinely new rule shape still needed a new rule function in
the engine. Sprint 14 makes the rule **selection** config and the rule **body** a registry entry.

## Sub-sprints
**work/1 — the rule registry (config-authorable reconciliation).**
- Refactor `adjudication_engine.py` `reconcile` into a `RULES` registry: name → pure function.
  Rule contract: `fn(ctx, params) -> verdict` where `ctx={claims, supporting:{claim:uris:[evidence]}, sub}`
  and verdict `{claim_support, disputed, conflict, determined, uncertainty}`.
- Shared `_derive(claim_support, params)` (disputed/conflict/determined/uncertainty from
  `support_floor`/`threshold`) so dispute semantics stay uniform across rules.
- Registry ships ≥2 distinct rules: `best-reliability-threshold` (VERBATIM copy → deli/cove byte-identical)
  + `strict-anchor-only` + `recency-weighted-threshold` (deterministic `as_of`-anchored decay).
- `validate_config`: accept any rule in `RULES` (drop the `== best-reliability-threshold` assertion).
- Accept both reconcile shapes: `{rule, params:{...}}` AND legacy `{rule, threshold, support_floor,...}`
  (merge non-`rule` keys as params) so existing deli/cove configs are untouched.
- `run_scenario` reconcile-check message names the configured rule dynamically.
- DoD: `python3 run_adjudication_engine_demo.py` still ALL PASS; deli/cove fixtures byte-identical
  (diff vs `/tmp/fx_baseline.sha`).

**work/2 — the verdict-change proof (same engine, only config differs).**
- Add `INSPECT_A/B/C` to `adjudication_configs.py` (NOT in `SCENARIOS` → deli/cove demo unchanged):
  one goods-inspection dispute, options/weights/authority/floor identical across A/B/C, differing
  ONLY in `reconcile` (A=best-reliability-threshold 0.92/0.55; B=strict-anchor-only kinds:[ANCHORED];
  C=recency-weighted as_of=2026-08-31 half_life 21d). Evidence crafted so A→determined(rework-partial-
  credit), B→UNRESOLVED (no anchored support), C→UNRESOLVED (ancient audit decays). Verdict flips
  solely by rule choice, zero engine change.
- New `run_rule_comparison_demo.py`: runs A/B/C through the same `run_scenario`, asserts per-rule
  per-claim dispute maps differ, asserts A.determination != B/C (DETERMINED vs UNRESOLVED), asserts
  Trust untouched, emits fixtures + a rule-named §7L cockpit-Q7 line (optional item). Exit 0 = ALL PASS.
- DoD: demo exit 0; asserts prove a claim DISPUTED under A becomes determined/undetermined under B/C.

**work/3 — conformance + full non-regression.**
- Extend `conformance_adjudication.py` labels to also validate `inspect-a/b/c` fixtures (C1–C5, venv).
- Re-run: new demo + conformance, Sprint-13 adjudication demo + conformance (deli/cove byte-identical),
  all four prior CR demos+conformance, sectors, S5 reference+all-six, agent demo.
- Verify 49 `$defs`/URI cap/SPEC v0.22 + `ros/` untouched (hashes + schema defs count + grep URI cap).

**work/4 — documentation + hand-off.**
- `docs/USER-AUTHORABLE-RULE-LAYER.md` (what became config, what remains authored — the rule BODY is
  still Python in the registry; the SELECTION is fully config — honest A/not-A stance).
- Update `instances/README.md`; append "Update after Sprint 14" to STRESS-TEST-SCENARIOS.md.
- Write `sprints/sprint-14/summary.md` + `notes/findings.md`; next prompt `sprints/sprint-15/PROMPT.md`.

## Definition of Done (all exit 0)
- Green baseline first ✓ (real output above).
- ≥3 distinct configured rules exercise a real lifecycle through ONE engine; a rule choice changes a
  DISPUTED / determined / UNRESOLVED verdict (A=rework-partial-credit vs B/C=UNRESOLVED).
- Same engine drives deli/cove byte-identical with their original rule (fixture hash diff empty).
- C1–C5 over the new inspect fixtures green; full non-regression green.
- 49 `$defs`, URI cap, SPEC v0.22 intact; `ros/` untouched.
- Honest §16 stance: argue **A — Yes** only if a truly new rule is added wholly through config, else
  state plainly why not (rule body still authored Python in the registry).