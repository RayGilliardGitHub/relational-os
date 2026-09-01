# Sprint 13 — Generalize the adjudication engine + render on the §7L cockpit

**Sprint goal.** Sprint 12 proved RelationalOS can *run* the contested-reality lifecycle, but its
honest finding is that the adjudication semantics are per-scenario authored code, not a
configurable engine. Sprint 13 makes that capability *general*: a generic, rule-driven
`adjudication_engine.py` that runs a contested-reality lifecycle for ANY org configured for it
(business-model weight vector, resolution policy, evidence-reconciliation rule, authority,
constraint object) + ≥2 recorded conflicting claims — producing lifecycle, epistemic status,
resolution options, utility ranking, §6-floor gated pick, and an authorized human determination
(or UNRESOLVED), all recorded additively. The SAME engine drives ≥2 different org scenarios with
NO code change between them (only config/data), proving the generalization.

**Baseline (verified, all exit 0, before any build):**
- S5 reference demo + all-six conformance; CR dispute/interest/tradeoff/lifecycle demos +
  conformance; agent demo + conformance; `build_all.py` + `conformance_all.py`. ALL PASS.

**Constraints (frozen):** 49 `$defs`, URI cap, SPEC v0.22, single-threaded, ~$0, additive-only.
The engine lives under `instances/contested_reality/` (self-contained; explicit `adj` label;
NOT added to `configs.SECTORS` so `build_all`/`conformance_all` don't change). `ros/` untouched.

## Sub-sprints

1. **work/1-plan.md — configurable engine + two scenarios.**
   Build `adjudication_engine.py` (generic, config-validated driver) + `adjudication_configs.py`
   (two org scenarios as pure data: **A. delivery** financial $18k dispute;
   **B. coverage** clinical payer/provider/patient dispute with a different factor model) +
   `run_adjudication_engine_demo.py` that runs BOTH through the same engine and asserts ALL PASS.
   Emit fixtures for C1–C5.

2. **work/2-plan.md — §7L cockpit-Q7 render + decision-learning (optional, additive).**
   Emit an additive `cockpit-q7.md`/`.json` report for a configured episode reusing the cockpit
   report render style (no new renderer universe, no `sector_scene.py` change). Implement the
   realized-cost / expected-vs-actual weight update: record `realized_cost_usd` + `outcome_value`
   additively on each `decision://`; deterministically, clamp-bounded, update the business-model
   weights toward factors that distinguish well-performing options; commit `learned_weights`
   additively on the case/dispute.

3. **work/3-plan.md — conformance + non-regression.**
   `conformance_adjudication.py` (C1–C5 over the new fixtures via the Sprint-0 validator), plus
   re-run the entire baseline suite to prove no regression. Decide-and-document the §16 verdict.

4. **work/4-plan.md — documentation + hand-off.**
   `docs/GENERALIZED-ADJUDICATION.md` (what is configurable / what stays authored), update
   `instances/README.md`, append the STRESS-TEST-SCENARIOS.md note, write `summary.md` +
   `notes/findings.md`, write `sprints/sprint-14/PROMPT.md`.

## Definition of Done
- The SAME engine runs ≥2 different scenarios from config with NO code change between them;
  output ALL PASS with epistemic-status + lifecycle + determination/UNRESOLVED recorded additively.
- §6 floor + §7J.9 authority preserved; TRUST unchanged by the engine (only the deterministic
  formula); C1–C5 over the new fixtures ALL PASS; full non-regression suite ALL PASS.
- Optional Q7 render + decision-learning done with real output.
- Honest `docs/GENERALIZED-ADJUDICATION.md` + §16 verdict documented.

## Exit criteria
`run_adjudication_engine_demo.py` exit 0; `conformance_adjudication.py` exit 0; all baseline
demos + conformance re-run exit 0. Every step signed and on the ledger.