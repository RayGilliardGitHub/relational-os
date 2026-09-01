# Sprint 11 — notes / findings

Date: 2026-08-31.

## What the build surfaced
- **The `Recommendation` `$def` was the exact fit** — `by/for/options` required plus additive
  `includes_do_nothing / tradeoff / authority_required / confidence / expected_impact / decision`.
  No new noun; the trade-off rides the case additively in that frozen shape (plus a machine-readable
  `json` ranking). `recommendation://` is NOT in the frozen URI catalog — confirmed; never emitted.
- **§7K.1 already specifies this** ("Trade-off / decision analysis — options incl. do-nothing;
  explains the trade-off, not a bare pick"; "the optimizer needs to know what 'better' means"). The
  experiment implements the normative text; no SPEC change required. SPEC stays v0.22.
- **The weights ARE the business model.** The engine's value vector (SLA 0.45 / emp 0.20 / mgr 0.15 /
  leave 0.10 / cost 0.10) is an authorship; the ranking is then computed. This is the *correct* split
  per §7K.1 but must be disclosed: "computed" ≠ "objective".
- **The local model is genuinely available** (`phi4-mini:3.8b-q8_0` responded on both the Sprint-8 and
  this demo) and independently agreed with the engine's eligible pick (`do-nothing`) on the
  UNKNOWN-coverage scenario. Robust parse + fallback-with-log holds.
- **§6 floor as a gate over the ranking** worked cleanly: an unknown-cost option is penalised AND
  excluded from the machine's auto-pick; `do-nothing` is never gated → UNRESOLVED remains the only
  eligible direction under insufficient basis, and Trust stays untouched. This is the same
  inviolable rule as Sprints 9/10, now driven by the trade-off rather than a prose note.
- **C2 temporal-suffix trap avoided** (Sprint-7 lesson): all added fields use suffixes like
  `_agents/_days/_minutes/_known/_used` — never `at|time|deadline|expires|expiry|effective|due|
  since`. Conformance C2 (RFC3339 recursion) passed.

## Decisions taken
- Additive `recommendation` object (frozen `Recommendation` shape) on the `case://`, not a new
  scheme — matches the frozen-ontology rule; documented, not silent.
- Weights exposed as module constants with a documented sum-to-1.0 assertion; a different weight
  vector is a different auditable business model (deliberate).
- `do-nothing` never floor-gated (changing nothing is never irreversible/unknown-cost) — the
  explicit baseline that prevents a forced winner.

## Honest limits / open gaps (feed the next sprint)
- **Weights are authored, not learned.** To derive them from data the system needs recorded outcome
  histories (realized cost of each prior arrangement/determination) to learn the objective. Current
  primitives record expected/actual outcomes (decision://) but not a *cost ledger* per option nor a
  realized-value post-mortem against the chosen utility. Missing primitive: a per-determination
  `realized_cost`/`outcome_value` back-fill onto `decision://` (additive), sufficient to fit/evaluate
  weights over time.
- The trade-off engine is deterministic and schema-silent; it is not yet wired into the cockpit/§7L
  "options incl. do-nothing + trade-off" question (Q7) as a rendered surface — a natural next step.
- The conflicting-evidence reconciliation and appeal remain engineered (deterministic + additive),
  not a general policy engine the org could configure without code.