# Sprint 18 — plan: the §7L Q7/Q8 cockpit line, first-class in the generic engine

**Goal.** Make the ACTIVE reconcile rule + its source + learned-or-not + the why a **first-class
§7L Q7/Q8 cockpit line rendered BY `adjudication_engine.py` itself** — so ANY generically-driven org
(registry rule, hand-authored `RULE_LIBRARY` spec, or a learned library entry added this run) carries
it in the engine's own §7L output, not only in the Sprint-16/17 runner reports. Data-only, no per-org
engine Python, frozen ontology (49 `$defs`, URI cap), SPEC v0.22, ~$0.

**Definition of Done.**
1. `cockpit_q7q8(cfg, sub, *, library=None) -> dict` in `adjudication_engine.py`: structured report —
   active rule name, source class, learned-this-run, evidence-gated `why`, Q7 options/trade-off, Q8
   recommendation + authorized determination, dispute uri.
2. `render_cockpit_q7q8(...) -> str`: plain-text §7L Q7/Q8 line from that dict, valid for ANY org config
   including one whose `reconcile` is a learned `RULE_LIBRARY` entry added at runtime.
3. `run_cockpit_q7q8_demo.py` (exit 0 = ALL PASS) drives ≥3 orgs across distinct rule sources
   (registry / rule-library / learned-this-run), asserts correctness + determinism + agreement with the
   Sprint-16/17 runner-report lines, emits the engine-native cockpit render per org.
4. Full non-regression green; deli/cove byte-identical up to the clock; C1–C5 green; 49 `$defs`; no new
   noun; SPEC v0.22.
5. Honest docs (`docs/ENGINE-Q7Q8-COCKPIT.md` + additive appendices + README + STRESS-TEST note) with a
   §16 verdict (first-class engine render vs runner-side artifact — stated plainly).

## Sub-sprints (each gets `work/<n>-plan.md` before building)
1. **Additive engine functions** — `cockpit_q7q8` + `render_cockpit_q7q8` (plus a tiny private source
   classifier helper) appended to `adjudication_engine.py`. Do NOT touch `reconcile`/`run_scenario`/
   `_derive`/`SPEC_VOCAB`/`_aggregate`. Reuse `rank`/`machine_eligible_best`/`render_tradeoff`.
2. **Runner** — `run_cockpit_q7q8_demo.py`: drive `deli` (registry), `inspect-corroboration`
   (rule-library via `ac.RULE_LIBRARY`), `inspect-learn-b` under a freshly learned spec
   (`calibrated-threshold-091`, decision recorded on that org's ledger → learned-this-run True), and
   `deli-learn` (reused learned → learned, not this run). Assert source class, determinism, both Q7+Q8
   present, and agreement with the Sprint-16/17 report lines. Emit engine-native cockpit renders +
   fixtures.
3. **Non-regression + docs** — re-verify every demo + conformance (deli/cove byte-identical up to
   clock), write `docs/ENGINE-Q7Q8-COCKPIT.md`, append README + STRESS-TEST + rule-library/reconcile-
   learning docs. Final: `summary.md`, `notes/findings.md`, `sprints/sprint-19/PROMPT.md`.

## Exit criteria (all exit 0, real output)
- New runner ALL PASS.
- Baseline all green again (run_reconcile_learning/rule_library/rule_authoring/rule_comparison/
  adjudication_engine demos; conformance_adjudication 16 labels; 4 prior CR conformances; 4 prior CR
  demos; sectors build_all + conformance_all; S5 demo + conformance; agent demo + conformance).
- Schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` untouched, no new noun.

## Budget / protocol
Single-threaded, plan-before-build, real tool output only. ~$0 deterministic local Python.