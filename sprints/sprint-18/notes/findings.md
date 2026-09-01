# Sprint 18 — findings

Date: 2026-08-31. Sprint: make the §7L Q7/Q8 cockpit line (ACTIVE reconcile rule + source +
learned-or-not + why) a first-class, data-only render inside `adjudication_engine.py`.

## What was already true (baseline, prior Sprints)
- Sprints 16/17 rendered the ACTIVE-rule-source line ONLY in runner reports
  (`cockpit-q7-rule-library.md`, `cockpit-q7-q8-reconcile-learning.md`) — the generic engine's own §7L
  cockpit output did not carry it. Sprint-17 summary explicitly flagged this as the next thread.

## Decisions taken
- **Data-only source classifier**, not config introspection and not engine-imports-configs: a spec
  is `rule-library` when the caller passes a library dict and the spec matches by `is`-identity or
  `name`; a spec carrying the Sprint-17 additive learned fields (`learned_param`/`learned_threshold`)
  is `learned`; a `rule` name in `RULES` is `registry`. This keeps the generic engine decoupled from
  `adjudication_configs` (which is the org's data, imported by runners, not by the engine).
- **learned-this-run is derived from the org's OWN ledger**, not a runner table: True only when
  `source == "learned"` AND the org's ledger contains a `decision://<label>/reconcile-learning`
  recorded this run. The `why` is read off that decision's `detail.why`. This reconstructs the
  Sprint-17 semantics (inspect-learn-b learned-this-run=True, deli-learn False) from the org's source
  of truth.

## Assumptions that mattered
- The learned-this-run sc0enario requires the reconcile-learning decision to be recorded on the SAME
  org that is driven under the learned rule. Sprint-17 recorded it on episode A's ledger (the learning
  *origin*), not on episode B (the org driven *under* the learned rule). For the engine-native data
  derivation, Sprint-18 records the decision on the org that is driven under the learned rule
  (inspect-learn-b) — legitimate (learning exists to feed future-rule usage) and it makes the org's
  own ledger the honest source of learned-this-run=True.
- No new config entry was added (`adjudication_configs.py` untouched): the learned spec is built and
  added to `ac.RULE_LIBRARY` at runtime (the established Sprint-17 pattern), and org variants reuse
  existing configs + `org_under_library_rule`.

## Corrections / guardrails
- `Graph.get` one-arg + `(graph.get(u) or {})` (untouched engine convention) reused in the new
  functions; no new footgun introduced.
- C2 temporal-suffix trap: the new structured dict / rendered line keys avoid `*_at`/`*_time` suffix
  collisions (the line is written to a *report*, not to a fixture walked by conformance, and the keys
  `active_rule/source/learned_this_run/why/determination` are suffix-safe).
- The rendered line for a reused learned rule (`deli-learn`) reports source=learned but
  learned-this-run=False — the honest "reuse of a learned rule, no learning step on this org" case,
  matching Sprint-17.

## What the sprint gained (summary)
- `adjudication_engine.cockpit_q7q8` + `render_cockpit_q7q8` + private `_cockpit_active_rule`
  (additive; `reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate` untouched).
- `run_cockpit_q7q8_demo.py` drives 4 orgs across 3 rule-source classes and asserts correctness,
  determinism, both §7L questions present, and agreement with the Sprint-16/17 report lines.
- Docs: `docs/ENGINE-Q7Q8-COCKPIT.md`, additive appendices in `RECONCILE-LEARNING.md` +
  `USER-AUTHORABLE-RULE-LIBRARY.md`, `instances/README.md` Sprint-18 entry, STRESS-TEST "Update after
  Sprint 18".

## Residual seams (honest)
- A `rule-spec-authored` inline spec (never learned, not matched to a passed library) reports
  `rule-spec-authored`; if an operator wants the library label they pass the library. This is the
  documented, data-only classification boundary.
- The learned-this-run flag is as strong as the org's ledger discipline: it is True only when the org
  actually carries its reconcile-learning decision. A runner must record it on the driven org (as
  Sprint-18 does) for the engine to report learned-this-run=True there.

## No spec change
- No normative gap surfaced; SPEC stays v0.22, 49 `$defs`, schema hash `7fc38c8c…`, `ros/` untouched.