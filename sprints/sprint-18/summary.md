# Sprint 18 — summary

**Goal.** Sprints 15–17 made the evidence-reconciliation RULE authorable, a cross-org RULE LIBRARY
(with the `bayesian-combine` primitive), and learnable — but the ACTIVE rule + its source +
learned-or-not were rendered only in **runner-side reports** (`cockpit-q7-rule-library.md`,
`cockpit-q7-q8-reconcile-learning.md`), never in the generic engine's own §7L cockpit output. Sprint 18
closes that: the ACTIVE reconcile rule + its source + whether a learning step changed it this run + the
evidence-gated why are now a **first-class §7L Q7/Q8 line rendered BY `adjudication_engine.py`**, so ANY
generically-driven org carries it. Additive, frozen ontology, SPEC v0.22, ~$0.

## What was built (instances/contested_reality/)
- **`adjudication_engine.py`** (engine code — the ONE permitted engine file): appended
  `cockpit_q7q8(cfg, sub, *, library=None)` (structured report), `render_cockpit_q7q8(...)` (plain-text
  §7L Q7/Q8 line), and a private `_cockpit_active_rule` data-only source classifier. `reconcile` /
  `run_scenario` / `_derive` / `SPEC_VOCAB` / `_aggregate` and every existing function body untouched;
  the new functions BUILD ON `rank` / `machine_eligible_best` / `render_tradeoff`.
- **`run_cockpit_q7q8_demo.py`** (new runner, exit 0 = ALL PASS): drives 4 orgs across 3 rule-source
  classes, asserts correctness + determinism + both §7L questions present + agreement with the
  Sprint-16/17 report lines, emits engine-native cockpit renders (`cockpit-q7q8-engine.{md,json}`) +
  fixtures. No config edit (`adjudication_configs.py` stays plain data; the learned spec is added to
  `ac.RULE_LIBRARY` at runtime, the established Sprint-17 pattern).

## Verified output (all exit 0, ALL PASS)
- **4 orgs / 3 rule-source classes, one generic engine call each:**
  - `deli` → ACTIVE `best-reliability-threshold`, source **registry**, learned-this-run False, why "unchanged".
  - `inspect-corroboration` → ACTIVE `independent-corroboration`, source **rule-library**, learned-this-run False.
  - `inspect-learn-b` → ACTIVE `calibrated-threshold-091` (a learned library entry added this run),
    source **learned**, **learned-this-run True**, why = the evidence-gated recalibration reason read off
    that org's own `decision://inspect-lb/reconcile-learning`.
  - `deli-learn` → ACTIVE `calibrated-threshold-091` (same learned spec, cross-org reuse), source
    **learned**, learned-this-run **False** (no learning decision on its own ledger).
- **Always both §7L questions + the full line:** every render carries Q7 (options incl. do-nothing/
  UNRESOLVED baseline + machine-eligible best) and Q8 (recommendation with authority + the §6 human's
  determination), plus ACTIVE rule + source + learned-this-run + why.
- **Deterministic:** the structured dict and rendered line are identical on re-run for every driven org.
- **Agreement with Sprint-16/17 proof:** engine-native line for `inspect-corroboration` matches
  `cockpit-q7-rule-library.md` (rule + determination); for `inspect-learn-b`/`deli-learn` matches
  `cockpit-q7-q8-reconcile-learning.md` (source + learned-or-not); `deli` matches the registry baseline.
- **Generic + data-only:** classification is derived from `cfg` + the org's ledger (source class, and
  learned-this-run from a real `decision://<label>/reconcile-learning` in that org's own ledger) — no
  per-org engine Python; `library=` is an optional data dict.

## Non-regression (all exit 0)
All 5 prior demos (`run_reconcile_learning` / `rule_library` / `rule_authoring` / `rule_comparison` /
`adjudication_engine`), `conformance_adjudication.py` **16 labels** C1–C5, the 4 prior CR demos +
conformances, sector `build_all.py` + `conformance_all.py`, S5 reference demo + conformance, agent demo
+ conformance — ALL PASS. `deli`/`cove` **byte-identical up to the clock** (proved by stripping the
timestamp keys and diffing across two engine-demo runs). Schema hash `7fc38c8c…`, **49 `$defs`**,
SPEC v0.22, `ros/` untouched, only catalog URI schemes — no new noun.

## §16 verdict
**First-class engine render, not a runner-side artifact.** The §7L Q7/Q8 line (ACTIVE rule + source +
learned-or-not this run + the why) is now a generic, data-only function in the engine that ANY
configured org renders identically from its own config + ledger, surfacing the reconcile rule as
first-class operating reality (Q7 options + Q8 recommendation with authority). The Sprint-16/17 cockpit
report files are now a *view* over that engine render, not the only place the line exists. No authority
over-claim: the Q8 recommendation stays machine-eligible-best (§6-floor-gated) and the authorized
determination remains the §6 human's call — the engine reports it, the runner records it, the human
owns it.

## Open issues / next work
- The residual rule-authoring seam from Sprints 15/16 — an op the vocabulary still cannot name (e.g.
  a provenance-conditional if/then, a different posterior shape) — remains the honest frontier; a next
  primitive could close a slice of it.
- `rule-spec-authored` (an inline spec never learned and not matched to a passed library) is the one
  source class that needs the caller to pass the library to be labelled `rule-library` — a documented,
  data-only boundary, not a code gap.
- The engine's §7L cockpit could be extended to the other questions (Q9 ownership/authority, Q10
  verified-outcome+learning) with the same data-only discipline — Q7/Q8+rule-source is the Sprint-18 slice.

## Docs touched (no SPEC bump)
- `contested_reality/docs/ENGINE-Q7Q8-COCKPIT.md` (new)
- `contested_reality/docs/RECONCILE-LEARNING.md` + `docs/USER-AUTHORABLE-RULE-LIBRARY.md` (Sprint-18 appendix)
- `instances/README.md` (Sprint-18 entry)
- `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` ("Update after Sprint 18")
- `sprints/sprint-18/plan.md`, `work/{1,2}-plan.md`, `notes/findings.md`, `summary.md`
- `sprints/sprint-19/PROMPT.md` (next prompt)
- `instances/contested_reality/`: `adjudication_engine.py`, `run_cockpit_q7q8_demo.py`