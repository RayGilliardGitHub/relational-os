# Sprint 16 — summary

**Goal.** Take on Sprint 15's disclosed seam and turn the rule-authoring DSL into a reusable,
cross-org **RULE LIBRARY**: add **≥1 genuinely NEW inference primitive** to `SPEC_VOCAB` (authored
once, then usable as data by every org), make spec-authored rules a **named library reused across
≥2 different orgs**, and surface the **ACTIVE rule + its spec-authored-vs-registry source** on a
§7L cockpit **Q7** line — then re-test whether the "needs a builtin" seam closes for that primitive.
Done: `bayesian-combine` added once; the named cross-org `RULE_LIBRARY` proven by identity + ≥2-org
reuse; Q7 active-rule/source rendered; the primitive produces a real verdict flip. Additive, frozen
ontology, SPEC v0.22, ~$0.

## What was built (instances/contested_reality/)
- **New primitive `bayesian-combine`** in `adjudication_engine.py` (`SPEC_VOCAB`): a reliability-
  likelihood posterior / independent-corroboration aggregate — `O = odds(prior)·Π_i(v_i/(1−v_i))`,
  `posterior = O/(1+O)`. Deterministic (explicit author `prior`), strict (bad `prior` rejected
  loudly), general (one real operator in `_aggregate`; the 3 registry rules + shared `_derive`
  untouched). Expresses what `max` CANNOT: many weak independent sources exceed any single source
  (posterior 0.9674 > max 0.7).
- **Named cross-org RULE LIBRARY** (`adjudication_configs.RULE_LIBRARY`) + `org_under_library_rule`
  reuse: `majority-of-sources` on `inspect` + `deli` (goods-QC + freight); the new
  `independent-corroboration` on `inspect` + `cove` (goods-QC + clinical). Reuse proven by `is`-
  identity of the SAME dict.
- **`run_rule_library_demo.py`** (exit 0 = ALL PASS): primitive proof, cross-org reuse, the verdict
  flip, invariants, Q7 render. Emits 5 new fixture families.
- **`conformance_adjudication.py`** now validates **13 labels**, C1–C5 ALL PASS, 49 `$defs`.
- **Cockpit Q7** report names the ACTIVE rule + spec-authored-vs-registry source per org.

## Verified output (all exit 0, ALL PASS)
- **Verdict flip (real, only the rule differs):** on the `inspect` dispute at reconcile threshold
  0.98, registry `max` (strongest witness 0.97) clears nothing → **UNRESOLVED**; library-spec
  `independent-corroboration` (bayesian-combine) combines the 0.84+0.97 independent witnesses →
  posterior **0.9961** ≥ 0.98 → **DETERMINED `rework-partial-credit` (CLOSED)**.
- **Cross-org reuse:** `majority-of-sources` on inspect + deli (UNRESOLVED / partial-settlement);
  `independent-corroboration` on inspect + cove (rework-partial-credit / step-therapy-first); both
  via the shared `RULE_LIBRARY` dict (identity-asserted).
- **Primitive strictness + determinism:** missing/0/1/1.5/"0.6" `prior` all rejected loudly; same
  spec compiles identically on re-run; empty sources → prior; a 1.0 source pins the claim.
- **Conformance:** `conformance_adjudication.py` **13 labels** C1–C5 ALL PASS, 49 `$defs`; new
  fixtures mint only catalog URI schemes (no new noun/cap break).
- **Full non-regression:** `run_rule_authoring_demo.py` / `run_rule_comparison_demo.py` /
  `run_adjudication_engine_demo.py` ALL PASS (deli/cove byte-identical); the 4 prior CR demos +
  conformances; sectors `build_all.py` + `conformance_all.py`; S5 reference demo + conformance;
  agent demo + conformance — all exit 0.
- **Frozen invariants:** SPEC hash `d10f0010…` (v0.22) unchanged; schema hash `7fc38c8c…`, 49
  `$defs`; `ros/` source git-clean; Trust only ever moved by S5; authority preserved.

## §16 verdict
Moves forward cleanly: **A — Yes for declarative, config-text rule authoring over the shipped
vocabulary, NOW INCLUDING the independent-corroboration (Bayesian-likelihood) op family.** The new
primitive is authored ONCE as a genuine, general, deterministic + strict operator; a rule using it is
authored as library data, reused by ≥2 orgs, and flips a real determination-vs-UNRESOLVED verdict —
closing the Sprint-15 told seam for that family. The precise, remaining dependence on a builtin:
any rule shape whose op the vocabulary still cannot name (a *different* posterior, a
provenance-conditional if/then, a *different* multiplicative combination) needs that one op added as
interpreter code — after which it too is authorable-as-data by every org. That is the standard
language-runtime-vs-rules boundary of any DSL, disclosed precisely, not concealed.

## Open issues / next work
- The residual seam is now precisely bounded to "an op the vocabulary cannot name". A next primitive
  could target one of those (e.g. a provenance-conditional op, or a different multiplicative
  combination) — each is additive and would close that slice of the seam the same way.
- The cockpit Q7 active-rule/source line is rendered in the rule-library report + a
  `cockpit-q7-rule-library.md` artifact; wiring it into the generic engine's own §7L cockpit render
  is a possible follow-up (not required for this hand-off).

## Docs touched (no SPEC bump)
- `contested_reality/docs/USER-AUTHORABLE-RULE-LIBRARY.md` (new), plus an "Sprint-16" appendix in
  `contested_reality/docs/USER-AUTHORABLE-RULE-DSL.md`
- `instances/README.md` (Sprint-16 entry)
- `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` ("Update after Sprint 16")
- `sprints/sprint-16/plan.md`, `work/{1,2,3,4}-plan.md`, `notes/findings.md`, `summary.md`
- `sprints/sprint-17/PROMPT.md` (next prompt)
- `instances/contested_reality/`: `adjudication_engine.py`, `adjudication_configs.py`,
  `run_rule_library_demo.py`, `conformance_adjudication.py`