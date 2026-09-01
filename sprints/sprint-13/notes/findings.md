# Sprint 13 — findings (dated)

**2026-08-31/09-01 (Sprint 13 build)**
- **The generalization was a data/architecture question, not an engine-shape question.** The Sprint-12
  lifecycle (`run_full_dispute.py`) had the right *surfaces* (claim/epistemic/dispute/decision/Trust),
  but its utility() function, option set, reconciliation logic, and weights were authored per scenario.
  Moving those into a config dict (`adjudication_configs.py`) with a generic `run_scenario(cfg, sub)`
  driver removed the per-scenario code with NO change to the frozen ontology. This validated the
  project's standing rule: accept-as-additive, never mine new nouns.
- **The value model is the last authored thing, and it SHOULD be** (§7K.1). The per-option factor
  scores and the weight vector are organizational judgment expressed as data. The engine computes the
  ranking; it does not (and must not) conjure desirability. Documented as "still authored" — by design.
- **The reconciliation rule is the one residual code semantic.** `best-reliability-threshold` is a
  named deterministic rule; its parameters (floor, threshold) are config, but a genuinely new rule
  type (e.g. Bayesian combination, recency-decay) needs a new rule function. That is the cleanest
  next step toward a user-authorable dispute DSL (proposed for Sprint 14).
- **Decision-Learning can be done additively and deterministically.** Recording `realized_cost_usd` +
  an additive `learned_weights` on the `decision://`, and re-weighting via a clamped, renormalized
  expected-vs-actual variance update, needed no new noun and no Trust change. It is the §7K.1
  Decision→Expected→Actual→Variance→Learning loop, live.
- **Schema gotchas resurfaced (all schema-compliant, no schema edit):**
  - `Relationship` requires `status`; configs initially omitted it → C2 failed until `status: ACTIVE`
    added.
  - `Obligation.source` is a frozen enum `[IMPOSED, VOLUNTARILY_UNDERTAKEN]`; a domain intuituous
    `PROFESSIONAL_STANDARD` was rejected — replaced with `IMPOSED`. (Same class of fix the skill's
    enum notes describe.)
  - Evidence `supports` must point at the supporting CLAIM uri, not be `None`, or reconciliation
    computes 0 support (this is what cleanly produces the UNRESOLVED branch for thin evidence).
- **Exact-vs-substring membership on option names** bit twice (the dispute-open UNRESOLVED check and
  the baseline detection): "unresolved" is not `== "unres"`. Fixed with `any("unres" in o.lower() ...)`.
- **`x = {...},` trailing comma makes a 1-tuple** — a dict literal followed by a comma is a tuple
  (a "singleton"), which broke `detail["why"]`. Kept scanning for it; Python makes it silent.
- **C5 only validates the state-machine files that EXIST** (relationship.json, case.json). dispute.json
  is not validated by C5, so emitting the proven Sprint-12 legal walk is a safe no-op there.
- **The §16 verdict moves B → B+ (materially toward A), not a clean A.** The two things §16
  explicitly named as missing (configurable adjudication + §7L cockpit render) are now demonstrated.
  A clean "A" waits on a user-authorable dispute DSL (arbitrary rule authoring) — stated plainly, not
  faked.

## Decisions recorded
- Keep SPEC v0.22: no normative gap, so no version bump (matches PROTOCOL's "never bump for a
  docs/capability-only change").
- New engine files use labels `deli`/`cove`; they are deliberately NOT added to `configs.SECTORS`
  so `build_all.py` / `conformance_all.py` / the sector fixtures are byte-identical (non-regression
  proven).
- `ros/` untouched: the engine provisions via `Substrate` directly, so no `label` parameter change
  was needed and the reference build stays byte-identical.