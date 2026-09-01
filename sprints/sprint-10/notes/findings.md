# Sprint 10 — Findings (conflicting-interest / remote-work experiment)

Date: 2026-09-01.

## What was discovered / demonstrated
- **A conflicting INTEREST (not a disputed fact) is now representable and runnable.** Two legitimate,
  mutually-exclusive interests (employee: remote+leave; manager: on-site coverage to meet a 30-min SLA)
  are detected under a **shared constraint** (SLA + staffing floor + conditional policy), opened as an
  OPEN `case://`, recorded with uncertainty, resolved to a **defensible determination** (the conditional
  middle `remote-with-coverage-plan`), with the **inviolable UNRESOLVED** outcome reachable when the
  admissible basis is insufficient. This is the Scenario-B capability the Sprint-9 review flagged as the
  remaining test of the word *relational*.
- **Appeal is now a first-class, signed, queryable step** — riding the schema's **native `right://`
  type=APPEAL** literal (the `Right` `$def` already enumerates `APPEAL`) + a signed `event://` + an
  additive `appeal` object — and is **re-adjudicated by a higher authority** (Director,
  `authority://ic/for-appeal`) rather than a silent redo. Authority (§7J.9) and signature are preserved
  on both the determination and the appeal decision.
- **Additive-field pattern extends cleanly from facts to interests:** the Sprint-9 epistemic-state
  pattern (carry the non-frozen state as additive fields) transfers to interests/conflict/negotiation/
  appeal with zero schema change. The frozen `case://` lifecycle (OPEN→…→RESOLVED→CLOSED) is reused
  unchanged.
- **C5 case-transition table is strict** (OPEN→TRIAGE→ASSIGNED→IN_PROGRESS→RESOLVED, and TRIAGE does
  NOT transition directly to RESOLVED): a naive `[OPEN, TRIAGE, RESOLVED]` state file fails C5. Fixed
  by the fully legal walk `[OPEN, TRIAGE, ASSIGNED, IN_PROGRESS, RESOLVED]`.

## Decisions
1. **No new noun.** `interest://` and `negotiation://` were *considered* and **rejected** — interests,
   conflict, negotiation, and appeal are **additive fields/objects** on existing primitives (`case://`,
   `relationship://`, `decision://`, `policy://`, `expectation://`, `right://`, `authority://`). This
   keeps the frozen ontology and URI cap byte-identical (49 `$defs`, SPEC v0.22). The Prompt explicitly
   allowed a new noun only as an explicit, documented decision; it was not warranted.
2. **Appeal rides `right://` type=APPEAL** — the schema already has that Right literal, so no additive
   enum/status invention was needed for the appeal's legal basis. The appeal's lifecycle state is
   carried additively (`appeal_status`, `appeal_outcome`) since `right://` has no such enum.
3. **Interests ride relationship objects** (one per party) and the shared constraint rides the contract
   `relationship://` — the relationship is the correct "shared context" both parties are bound by
   (matches §3.14 scoped-Trust/context semantics).

## Pitfalls discovered (worth recording)
1. **`Graph.get()` takes one positional arg only** (no default sentinel): `graph.get(uri, {})` raises
   `TypeError: Graph.get() takes 2 positional arguments but 3 were given`. Use `(graph.get(uri) or {})`,
   and note a missing key returns `None`, not `{}`.
2. **C5 relationship & case state machines are strict** (see above). When emitting `statemachines/*.json`
   for a new instance, write a *fully legal* walk of the transition table, not a plausible-but-illegal
   short one — the Sprint-9 dispute fell back to passing C5 by *not* emitting `case.json`; Sprint 10
   emitted a correct one (and caught the `TRIAGE↛RESOLVED` rule the hard way).
3. **Additive key naming still matters for C2 RFC3339:** the avenue of "additive fields end in a
   temporal suffix" (Sprint-7 lesson) is easy to re-trip. Kept keys like `response_target_minutes`,
   `coverage_floor_agents`, `unused_leave_days`, `exercised_at_ref` (the `_ref` avoids `at`/`time`).
4. **MERGE-not-replace holds** (recurring Sprint-9 lesson): recording the appeal update onto the case
   spread the existing object (`{**graph.get(uri), ...}`) so the required fields + earlier additive
   `conflict` survived C4 round-trip.

## Honest limits (unchanged / explicit)
- The adjudicator is a **human**; the conditional plan's defensibility is authored, not computed.
- **No optimizer/business-model** for "what *better* means" (§7K.1) — the ranking of side-employee vs
  side-manager vs remote-with-coverage-plan vs do-nothing is not machine-computed from the org's own
  constraints. **This is the next genuine frontier.**
- No advisory real-local-model recommendation in this minimal experiment (the Sprint-8 `agent_demo`
  advisory-`decision://` + §6-floor pattern is the natural additive extension).

## Spec impact
**None.** SPEC stays v0.22 — additive demonstration only, no schema edit, no new noun, no version bump.