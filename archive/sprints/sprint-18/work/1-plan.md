# Sprint 18 / work — 1-plan: additive engine Q7/Q8 cockpit functions

**Before:** nothing to build here — this plan precedes the ONLY engine-file change permitted.
**What:** append two public functions (+ one private helper) to
`instances/contested_reality/adjudication_engine.py`:
- `cockpit_q7q8(cfg, sub, *, library=None) -> dict`
- `render_cockpit_q7q8(cfg, sub, *, library=None) -> str`

**Source classifier (data-only, cannot import configs):** from `cfg['reconcile']`:
- `"rule" in rc` → source `"registry"` if `rc['rule'] in RULES` else `"registry-unknown"`; active name =
  `rc['rule']`.
- else `rule_spec` → active name = `spec.get('name') or 'anonymous-rule-spec'`. If the raw spec carries
  the Sprint-17 additive learned fields (`learned_param` or `learned_threshold`) → source `"learned"`.
  Else if `library is not None` and the spec matches a library entry by `is`-identity or by `name` →
  source `"rule-library"`. Else source `"rule-spec-authored"`.

**learned-this-run + why (from the org's OWN ledger, not the runner):** the org reports
`learned_this_run = (source == "learned") and bool(decision://<label>/reconcile-learning)`.
`why` = that decision's `detail.why` (the evidence-gated reason) when learned-this-run, else `"unchanged"`.
This makes a learned rule driven on an org that recorded its reconcile-learning decision this run report
learned-this-run=True, while a reuse org that merely points at the same learned spec (e.g. deli-learn)
reports learned + learned_this_run=False — exactly the Sprint-17 semantics, but data-derived.

**Q7 / Q8 (per §7L):** Q7 = the resolution options incl. the do-nothing/UNRESOLVED baseline rendered as
the trade-off (`render_tradeoff(cfg, rank(cfg))` — deterministic). Q8 = the machine-eligible best
(non-gated) recommendation with the authority it requires, plus the §6 human's authorized determination
read off `sub.graph` for `cfg['dispute']['uri']`.

**Additive only:** no edits to `reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`,
`validate_config`, or any existing function body. New functions are appended at the module bottom.
Reuse existing `rank`, `machine_eligible_best`, `render_tradeoff`, `normalize_reconcile` where read-only.

**Determinism:** all inputs explicit (cfg + sub graph + optional data dict); no wall-clock.
**Signed-off after:** a minimal in-place sanity check (import + one call on a registry org) before the
runner is written.