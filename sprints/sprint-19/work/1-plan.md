# SPRINT 19 — work/1-plan.md (build the engine §7L Q1–Q10 cockpit)

Implement `cockpit_s7l(cfg, sub, *, library=None) -> dict` and
`render_cockpit_s7l(...) -> str`, appended to `adjudication_engine.py`. Reuse the Sprint-18
`cockpit_q7q8`/`_cockpit_active_rule` and the shared surfaces (`reconcile`, `rank`,
`machine_eligible_best`, `render_tradeoff`). Q7/Q8 are the Sprint-18 dict verbatim (strict
superset — by identity, not re-derivation, so the assertion Q7/Q8(cockpit_s7l) == Q7/Q8(cockpit_q7q8)
holds by construction). All reads data-only from `cfg` + `sub.graph` + `sub.ledger`.

Structured dict keys (q1..q10), each with the recorded-data evidence:
- q1 state/events over the period: counted ledger events (event:// objects, in order),
  the dispute's recorded lifecycle walk (lifecycle_state values), status, epistemic_state.
- q2 change/delta: the state deltas recorded in the ledger — claims claimed->disputed,
  dispute OPEN->...->CLOSED (or UNRESOLVED), epistemic UNDETERMINED->RESOLVED_DETERMINED /
  INSUFFICIENT_EVIDENCE, determination recorded; change->significance.
- q3 prioritized attention (§7J.5 analogue): actionable now = OPEN/UNRESOLVED disputes,
  UNDETERMINED/claimed/disputed claims, determined-this-run flag.
- q4 exceptions (§7J.2 analogue): OPEN/UNRESOLVED disputes, reconcile uncertainty/conflict,
  any still-undetermined epistemic state; each tagged as the exception.
- q5 root-cause WITH epistemic status: per disputed claim {uri, statement, proposer,
  epistemic_status (read from the graph), support} + the reconcile verdict (determined/
  disputed/conflict/uncertainty + claim_support). Root-cause = the claim(s) whose support
  actually carries the determination (or the honest UNDETERMINED if none).
- q6 forecast "if nothing changes": a recorded realized-vs-expected series on the graph
  (metric:// or any object with a per-period realized/expected list); if none → explicit
  "cannot forecast from recorded data (no recorded realized-vs-expected series)". Never a
  wall-clock, never an invented number.
- q7 options + trade-off: delegate to base q7 (options, baseline, machine_eligible_best,
  tradeoff).
- q8 recommendation w/ authority + determination: delegate to base q8.
- q9 ownership/capability/authority: the §6 determination authority + its holder (cfg
  authority + actor), the obligated party (the dispute "about" obligation's subject), the
  actor roster, the appeal authority. capability = who can act (holder of each authority).
- q10 verified outcome + organizational learning: dispute `verified`, `resolution_outcome`,
  and the recorded learning — `evidence://<label>/learning-note.learning` and the optional
  `decision://<label>/reconcile-learning` (detail.learning / learned_threshold) — all read
  from the org's graph, never authored literals.

render_cockpit_s7l: plain-text `§7L Q1–Q10 cockpit (engine-native) — org <label>` block,
one line per question prefixed `Q<n>.`, plus the ACTIVE rule/source/learned-this-run/why line
reused from base, deterministic.

Guardrails: read claims/evidence from the GRAPH (their recorded epistemic_status /
reliability), not just cfg; for the `unresolved` thin-evidence dispute use the
`cfg['unresolvable']` claims; never a field key ending in a C2 temporal suffix; arrays for
`evidence`. Deterministic — identical inputs → identical dict + render.