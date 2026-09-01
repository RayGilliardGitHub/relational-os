# Sprint 19 — summary

**Goal.** Sprints 13–18 made a configurable adjudication engine render the ACTIVE reconcile rule +
source + learned-or-not + why as a first-class §7L **Q7/Q8** line. Sprint 19 takes the same data-only
discipline to the **whole ten-question morning test**: the generic engine now renders the complete
**§7L Q1–Q10 cockpit** for ANY configured org, data-only, with Q7/Q8 delegating to the Sprint-18 line
by construction (strict superset). Additive, frozen ontology, SPEC v0.22, ~$0.

## What was built (instances/contested_reality/)
- **`adjudication_engine.py`** (the ONE permitted engine file; append-only, NOT a rewrite):
  added `cockpit_s7l(cfg, sub, *, library=None)` (structured dict of all ten §7L questions),
  `render_cockpit_s7l(...)` (plain-text §7L Q1–Q10 cockpit), and two private data-read helpers
  (`_ledger_dispute_walk`, `_recorded_forecast_series`, `_graph_objects`). Every existing frozen
  function (`reconcile`, `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`, `rank`,
  `machine_eligible_best`, `render_tradeoff`, `cockpit_q7q8`, `_cockpit_active_rule`) is untouched;
  the new functions BUILD ON them. Q7/Q8 ARE the Sprint-18 `cockpit_q7q8` dict blocks (superset by
  construction; asserted equal on every org).
- **`run_cockpit_s7l_demo.py`** (new runner, exit 0 = ALL PASS): drives 4 orgs across 3 rule-source
  classes and asserts all six PROMPT requirements; emits `cockpit-s7l-engine.{md,json}` + fixtures.
  No config edit (`adjudication_configs.py` stays plain data; the learned spec is added to
  `ac.RULE_LIBRARY` at runtime).

## Verified output (all exit 0, ALL PASS)
- **4 orgs / 3 rule sources, one generic engine call each:**
  - `deli` → registry best-reliability-threshold; Q5 root `delivered`@0.97 DETERMINED; determination partial-settlement; verified + learning-note.
  - `inspect-corroboration` → rule-library independent-corroboration; Q5 `passed`@0.9961 DETERMINED; determination rework-partial-credit.
  - `inspect-learn-b` → **learned-this-run** calibrated-threshold-091 (reconcile-learning recorded on ITS OWN ledger); determination rework-partial-credit; Q10 shows learning-note + reconcile-learning.
  - `deli-learn` → learned, learned-this-run False (cross-org reuse of the same learned spec).
- **All ten §7L questions + evidence present** on every org (Q1 state/events + ledger count + lifecycle walk; Q2 delta + significance + claim epistemic; Q3 attention; Q4 exceptions; Q5 root-cause with per-claim epistemic_status + support under the active rule; Q6 honest forecast; Q7/Q8 the Sprint-18 line; Q9 ownership/capability/authority; Q10 verified + learning).
- **Assertions green:** (b) Q7/Q8 of `cockpit_s7l` == Sprint-18 `cockpit_q7q8` on every org; (c) deterministic (dict + render identical on re-run); (d) agreement with the Sprint-16 rule-library, Sprint-17 reconcile-learning, and Sprint-18 engine report lines; (e) Q5 epistemic + Q10 verified/learning read from the org's real graph/ledger (not authored literals); (f) Q6 **never fabricates** (no recorded series -> explicit "cannot forecast from recorded data").

## Non-regression (all exit 0)
The 6 curated runners (`run_cockpit_q7q8_demo` / `run_reconcile_learning_demo` / `run_rule_library_demo`
/ `run_rule_authoring_demo` / `run_rule_comparison_demo` / `run_adjudication_engine_demo`),
`conformance_adjudication.py` **16 labels** C1–C5, the 4 prior CR demos + conformances, sector
`build_all.py` + `conformance_all.py`, S5 reference demo + conformance, agent demo + conformance — ALL
PASS. `deli`/`cove` **byte-identical up to the clock** (stripping timestamp keys, diffing two runs —
proved). Schema hash `7fc38c8c…`, **49 `$defs`**, SPEC v0.22, `ros/` untouched, only catalog URI
schemes — no new noun.

## §16 verdict
**The §7L gate is met at the engine-render level.** The engine (`adjudication_engine.cockpit_s7l` /
`render_cockpit_s7l`) answers all ten §7L morning questions with recorded-data evidence for any
configured org, data-only; #8 (Q8's recommendation) is machine-eligible-best, §6-floor-gated, carries
the authority it requires (§7J.9), and the authorized determination is the §6 human's
`determination_policy` call that closes in a verified, learned outcome (Q10). Honest limits: Q6 cannot
forecast where no realized-vs-expected series is recorded (it says so plainly — never a fabricated
number); Q9 "capability" is the holder-of-authority assignment + obligated party, not a dynamic
capacity model; and the cockpit reports the recorded state — it does not manufacture certainty where
the evidence is UNRESOLVED (UNRESOLVED stays a legal, Trust-safe outcome; the §6 floor is never
overruled; S5 alone moves Trust).

## Open issues / next work
- **Q6 forecasting** is the honest frontier: these adjudication orgs do not record a realized-vs-expected
  series, so the cockpit truthfully cannot forecast. A future sprint could record a metric/BI series on
  an org (or reuse the reference sector's `metric://` recording) so Q6 can actually project "if nothing
  changes" — the analogue of the reference cockpit's BI projections.
- **Q9 capability** is rendered as the recorded holder-of-authority assignment, not a dynamic capacity/
  load model; a future sprint could carry an additive capacity field on the authority/actor and read it.
- `rule-spec-authored` (an inline spec never learned and not matched to a passed library) stays the one
  source class needing the library to be passed for the `rule-library` label — the documented, data-only
  boundary from Sprint 18.

## Docs touched (no SPEC bump)
- `contested_reality/docs/ENGINE-S7L-COCKPIT.md` (new) + Sprint-19 appendix in `docs/ENGINE-Q7Q8-COCKPIT.md`
- `instances/README.md` (Sprint-19 entry)
- `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` ("Update after Sprint 19")
- `sprints/sprint-19/{plan.md,work/1-plan.md,notes/findings.md,summary.md}`
- `sprints/sprint-20/PROMPT.md` (next prompt)
- `instances/contested_reality/`: `adjudication_engine.py` (append), `run_cockpit_s7l_demo.py`