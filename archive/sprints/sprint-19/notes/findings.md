# Sprint 19 — findings

Date: 2026-09-01. Sprint: make the FULL §7L Q1–Q10 morning cockpit a first-class, data-only render
inside `adjudication_engine.py`.

## What was already true (baseline, prior Sprints)
- Sprints 13–18 built the configurable adjudication engine: a config-authorable reconciliation RULE
  (registry → declarative `rule_spec`), a named cross-org `RULE_LIBRARY` (with `bayesian-combine`),
  RULE learning, and (Sprint 18) a first-class §7L **Q7/Q8** line inside the engine
  (`cockpit_q7q8`/`render_cockpit_q7q8`). The rest of §7L (Q1–Q6, Q9, Q10) existed only in the
  **reference** sector cockpit (`sprints/sprint-5/artifacts/reports/cockpit.md` via `ros/bol.py`),
  not in the generic adjudication engine.
- The Sprint-18 summary explicitly listed "the engine's §7L cockpit could be extended to the other
  questions (Q9 ownership/authority, Q10 verified-outcome+learning) with the same data-only
  discipline" as the next thread.

## Decisions taken
- **Full Q1–Q10 as one generic data-only function.** `cockpit_s7l(cfg, sub, *, library=None)` reads
  every question's evidence off the org's OWN graph/ledger/config: `sub.ledger.entries` for Q1/Q2,
  the `dispute://` object for Q4/Q10, `reconcile(sub, cfg)` per-claim support for Q5, the recorded
  `claim://*.epistemic_status` + the reconcile verdict for Q5, `cfg.authority` + the `dispute_about`
  `obligation://` subject for Q9, and the recorded `evidence://<label>/learning-note` +
  `decision://<label>/reconcile-learning` for Q10. No per-org engine Python.
- **Q7/Q8 delegate to the Sprint-18 line by construction (strict superset).** The new function
  computes `base = cockpit_q7q8(cfg, sub, library=library)` and reuses its `q7`/`q8` dict blocks and
  its active-rule/source/learned/why/determination surface verbatim — so the engine's Q7/Q8 line is
  byte-identical whichever function drives it. This makes assertion "(b) Q7/Q8(cockpit_s7l) ==
  Q7/Q8(cockpit_q7q8)" hold structurally, and the runner asserts it explicitly.
- **Q6 is honest, not aspirational.** A forecast is produced ONLY when a recorded realized-vs-expected
  *series* exists on the graph (a `metric://`-style `points`/`series` list); otherwise Q6 plainly says
  "cannot forecast from recorded data". The single `realized_value` the learning step records is NOT a
  forecast series and is honestly reported as such. Never the wall-clock, never an invented number.
- **Q5/Q10 evidence is the org's real graph, not authored literals.** `epistemic_status` is read off
  each recorded `claim://` object; `verified` off the `dispute://` object; the learning entries are
  real `evidence://<label>/learning-note` / `decision://<label>/reconcile-learning` objects on that
  org's ledger (all asserted).

## Assumptions that mattered
- The term "over the period" (Q1/Q2) is, for a driven episode, "everything recorded this run": the
  engine reports the full set of ledger `event://` entries and the dispute's recorded lifecycle walk.
  This matches how the adjudication orgs are driven (one signed sequence per episode). No wall-clock
  is used for any question.
- The lifecycle walk (`_ledger_dispute_walk`) is reconstructed from every `state_update` object that
  touches the `dispute://` URI across the ledger, preserving first-seen order — deterministic and
  auditable.
- `_graph_objects` reads the graph as a list of objects (the Sprint-18 fixtures use this shape); the
  fallback uri-map path covers a plain-dict graph.

## Corrections / guardrails
- `Graph.get` one-arg + `(graph.get(u) or {})` (the engine convention) reused everywhere.
- C2 temporal-suffix trap respected: no additive field key ends in `at|time|deadline|expires|expiry|
  effective|due|since`; the cockpit keys (`epistemic_status`, `determination`, `verified`,
  `lifecycle_state`, `resolution_outcome`, …) are suffix-safe. The rendered report is not walked by
  the C2 tester, but the discipline is kept regardless.
- The discovered dead/redundant branch in my first implementation (an `if/else` that did the same work
  both ways) was removed before finalizing — the QA/verify pass caught it.
- `render_cockpit_s7l` wording fixed during smoke-testing: the Q2 line originally double-printed the
  epistemic prefix ("UNDETERMINED -> UNDETERMINED -> …") and a "discontinuity" typo on Q1; both fixed.
- The only engine change is the two appended functions + three private helpers; the frozen functions
  and their bodies are untouched (verified by full non-regression + deli/cove byte-identical up to the
  clock). `adjudication_configs.py` was NOT modified (its git `M` is the pre-existing, uncommitted
  Sprint-17 `inspect_batch` block that was in the tree before this session).

## What the sprint gained
- `adjudication_engine.cockpit_s7l` + `render_cockpit_s7l` + private data-read helpers (additive;
  frozen functions untouched).
- `run_cockpit_s7l_demo.py` drives 4 orgs / 3 rule sources and asserts the six PROMPT requirements
  (all ten Q present with evidence; Q7/Q8 == Sprint-18 line; determinism; agreement with the
  Sprint-16/17/18 lines; real-graph Q5/Q10; no-fabrication Q6).
- Docs: `docs/ENGINE-S7L-COCKPIT.md` (new), Sprint-19 appendix in `docs/ENGINE-Q7Q8-COCKPIT.md`,
  `instances/README.md` Sprint-19 entry, STRESS-TEST "Update after Sprint 19".

## Residual seams (honest)
- **Q6 forecasting**: the adjudication orgs record no realized-vs-expected series, so the cockpit
  truthfully cannot forecast. A future sprint could add a `metric://`/BI series (the reference sector
  already records BI projections) so Q6 can actually project "if nothing changes".
- **Q9 capability**: rendered as holder-of-authority assignment + obligated party + actor roster, not
  a dynamic capacity/load model (the reference cockpit's `capacity 1.0` is a sector-side additive
  field; the adjudication orgs carry no such field).
- The `rule-spec-authored` classification boundary from Sprint 18 (needs the library passed to be
  labelled `rule-library`) carries forward unchanged.

## No spec change
- No normative gap surfaced; SPEC stays v0.22, 49 `$defs`, schema hash `7fc38c8c…`, `ros/` untouched.