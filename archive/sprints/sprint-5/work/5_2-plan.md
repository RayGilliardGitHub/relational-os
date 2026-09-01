# SPRINT 5 — SUB-SPRINT 5.2 PLAN  (Goals / Metrics / Priority / Dependency)

## Goal
Build the metric-driven planning/rationale surface for Quoteko: a
`Goal -> Metric -> Actual -> Variance -> Decision -> Action -> Outcome` loop, compute
**Priority = f(impact, urgency, confidence, irreversibility, relationship-importance,
cost-of-delay)** (§7J.5), and represent **Dependencies** (`requires, blocks, enables,
derived_from, impacts`, §7J.6) with a transitive impact analysis. The cockpit's
business-health panel derives from **ledger-projected Metrics**.

## What will be built
- `Goal` objects (`goal://`), `Metric` objects (`metric://`) with formula, target,
  threshold, actual (ledger-projected), variance, and forecast fields (§7K.1). Metrics:
  on-time delivery, customer-trust, settled-value.
- `Metric -> Actual -> Variance -> Decision -> Action -> Outcome` loop: metric variance
  (on-time < target) -> decision (re-allocation) -> action (the task) -> outcome (verified).
- `Priority = f(impact, urgency, confidence, irreversibility, relationship-importance,
  cost-of-delay)` — deterministic local formula; attach `priority` + `priority_factors`
  to every attention item (Task / Case).
- `Dependency` objects (`dependency://`) + `BolService.impact_analysis(uri)` returning the
  transitive set of what breaks if a node fails. Show dependency->impact for the
  exception->case->task chain.
- Business-health panel: a function that projects Metrics from the ledger and renders a
  health table (target/actual/variance/status) -> feeds 5.3's cockpit.

## Verification (5.2 DoD)
`business_health_check` asserts: metrics carry actual + variance derived from the ledger;
priority is a deterministic, ordered score and the attention list is priority-ordered;
`dependency://` kinds used; impact analysis returns the expected downstream set for at
least the exception->case->task chain. Conformance stays green (exit 0).

## Objects introduced (URI-cap safe)
`goal://qk/g-customer-trust`, `metric://qk/m-on-time`,
`metric://qk/m-customer-trust`, `metric://qk/m-settled-value`,
`dependency://qk/...` (requires/blocks/enables/derived_from/impacts). Priority carried as
additive `priority`/`priority_factors` on case/task (no new scheme).