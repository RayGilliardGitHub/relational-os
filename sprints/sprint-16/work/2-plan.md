# work/2 — plan: the rule-library runner (`run_rule_library_demo.py`)

Do FIRST: work/1 is done (new `bayesian-combine` primitive added + RULE_LIBRARY + three reuse org
variants; prior Sprint runners STILL ALL PASS verified above; the primitive is strict and
`posterior 0.9674 > max 0.7` proves the unique combination power).

Build ONE new runner `instances/contested_reality/run_rule_library_demo.py` (exit 0 = ALL PASS) that
proves Sprint 16 end-to-end with real signed lifecycles + fixtures:

1. **Primitive is real + general (unit-level, on `_aggregate` directly):**
   - `bayesian-combine` posterior EXCEEDS `max` on many-weak-sources input (the property NO old op
     has): assert `posterior(3×0.7, prior 0.7) == 0.9674 > max == 0.7`, and one empty-source set →
     posterior == prior (no evidence → prior).
   - Strictness: bad `prior` (missing / 0 / 1 / 1.5 / "0.6") all rejected loudly; unknown op still
     rejected; determinism: same spec → same support on re-run.
2. **A new rule authored as a spec that USES the primitive, driven on an org with a REAL verdict:**
   run `inspect-corroboration` (library `independent-corroboration`, threshold 0.98). Assert the
   **flip**: at threshold 0.98 the same org under best-rel/`max` (passed=0.97) clears nothing →
   **UNRESOLVED**; under bayesian-combine the passed claim's 0.84+0.97 witnesses posterior ≈
   **0.9961** ≥ 0.98 → **determined rework-partial-credit (CLOSED)**. Assert both real reconcile
   outputs.
3. **Cross-org rule reuse (a real library, not inspect-only):** the SAME named library rule spec
   dict used by view≥2 DIFFERENT orgs:
   - `majority-of-sources` on inspect (existing) AND on `deli-majority` (freight) → 2 orgs.
   - `independent-corroboration` on `inspect-corroboration` AND on `cove-corroboration` (clinical).
   Assert each library rule's org configs reference the exact SAME `RULE_LIBRARY` dict object
   (`is`, not a copy), and each drives a lawful terminal lifecycle (CLOSED or UNRESOLVED).
4. **Cockpit §7L Q7 — ACTIVE rule + spec-authored-vs-registry source:** per org, print + render a
   Q7 line naming the ACTIVE rule and `source=spec-authored (rule-library DATA)` vs
   `registry (engine function)`; emit a `cockpit-q7-rule-library.md|.json` report (Sprint-13 shape).
5. Emit fixtures for `deli-majority`, `inspect-corroboration`, `cove-corroboration` (the engine's
   `emit_fixtures` reads `cfg["label"]`).

DoD (work/2): new runner ALL PASS, exit 0; cross-org reuse proven (`is`-identity + ≥2 orgs/rule);
the new primitive flips a real verdict (0.98); Q7 line names rule + source; fixtures emitted.