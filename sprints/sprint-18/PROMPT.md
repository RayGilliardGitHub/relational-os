# SPRINT 18 — PROMPT (the §7L Q7/Q8 cockpit line, first-class in the engine: ACTIVE rule + source + learned-or-not)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 15–17 made the evidence-reconciliation RULE authorable as a `rule_spec`, a named
cross-org **RULE LIBRARY** (with a new `bayesian-combine` primitive), and then **learnable** (a
deterministic, clamp-bounded, evidence-gated recalibration of the reconcile threshold that feeds a
NEW library entry). In both Sprint 16 and Sprint 17 the ACTIVE rule + its spec-authored-vs-registry /
learned-or-not source + the evidence-gated reason were rendered in **runner-side reports**
(`cockpit-q7-rule-library.md`, `cockpit-q7-q8-reconcile-learning.md`) — but never wired into the
generic engine's OWN §7L cockpit output. Sprint 18 closes that: make the ACTIVE reconcile rule + its
source + whether a learning step changed it + the why a **first-class §7L Q7/Q8 cockpit line inside
`adjudication_engine.py`**, so ANY org's generically-rendered cockpit carries it — not just the
cluster of runner reports.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7J.9 (cockpit /
  authority), §7K.1 (Decision Learning, Trade-off, Policy execution), §7L (ten morning questions,
  esp. Q7 "what are our options?" and Q8 "what should we do?"), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  best-effort ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `/home/rlg/relational-os/instances/contested_reality/adjudication_engine.py` (the generic engine:
    `reconcile`, `_derive`, `SPEC_VOCAB`, `compile_rule_spec`, `run_scenario`, `rank`,
    `machine_eligible_best`, `emit_fixtures`, `render_tradeoff`), `adjudication_configs.py`
    (`RULE_LIBRARY`, DELI/COVE/INSPECT variants, the Sprint-17 `INSPECT_BATCH_A/B` + `LEARN_HYPER`),
    `reconcile_learning.py` (Sprint 17: `learn_threshold`, `build_learned_library_spec`,
    `record_learned_rule`).
  - The two runner reports that currently carry the Q7/Q8 line:
    `run_rule_library_demo.py` (renders Q7 active-rule+source in `cockpit-q7-rule-library.md`) and
    `run_reconcile_learning_demo.py` (renders Q7/Q8 active-rule+source+learned-or-not in
    `cockpit-q7-q8-reconcile-learning.md`). Study HOW they compose the line, so the engine version is
    a superset, not a divergent duplicate.
  - Sprint-17 `sprints/sprint-17/summary.md` + `notes/findings.md` + the docs
    `contested_reality/docs/RECONCILE-LEARNING.md` and `docs/USER-AUTHORABLE-RULE-LIBRARY.md`.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs`; additive
  only; single-threaded; plan-before-build; real tool output; ~$0; footguns (`Graph.get` one-arg,
  `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2 RFC3339
  temporal-suffix trap incl. `calibrated_from`/`bound`/`realized_why` keys, strict C5 tables,
  `eng.reconcile(sub, cfg)` ARG ORDER, the Sprint-0 venv, module-constant-vs-local shadowing, runner
  CWD-sensitivity).

## What Sprint 18 IS and IS NOT
- **IS:** a **§7L cockpit Q7/Q8 line rendered BY THE ENGINE** — a deterministic function (e.g.
  `render_cockpit_q7q8(cfg, sub) -> str` and the structured `cockpit_q7q8(cfg, sub) -> dict`) inside
  `adjudication_engine.py` that reports, for a given org, (a) the ACTIVE reconcile rule (registry name
  or `rule_spec` name), (b) its SOURCE (engine registry function / `RULE_LIBRARY` data spec / a
  **learned** library entry added this run), (c) whether a learning step changed it this run, and
  (d) the underlying decision/evidence-gated reason (the `decision://…/reconcile-learning` `why`, or
  "unchanged"). It must read the org's own ledger/graph so any generically-driven org renders it
  (data-only, no engine Python per org). Prove it with a runner that drives ≥2 different orgs (e.g.
  `inspect-learn-b` under the learned `calibrated-threshold-091`, and `deli` under its registry rule)
  and renders BOTH the runner report AND the engine-native cockpit line, asserting they agree.
- **IS NOT:** a new service, a new URI noun, a schema edit, a Trust change (S5), a change that lets
  the machine overrule the §6 human, or a re-implementation of `run_scenario`/`reconcile` (use the
  shared engine surface). No frontier spend. ~$0 deterministic local Python.

## The target (what "done" looks like)
1. A generic `cockpit_q7q8(cfg, sub)` in `adjudication_engine.py` returning a structured dict
   (active rule name, source, learned-or-not this run, why, determination), and `render_cockpit_q7q8`
   rendering it as a plain-text §7L Q7/Q8 line — valid for ANY org config, including one whose
   `reconcile` is a learned `RULE_LIBRARY` entry added at runtime. It must NOT change the frozen
   schema/ontology or the byte-identity of existing orgs.
2. A runner (e.g. `run_cockpit_q7q8_demo.py`, exit 0 = ALL PASS) that:
   - drives ≥2 orgs with different rule sources (a registry-rule org, a hand-authored
     `RULE_LIBRARY` org, and a Sprint-17 LEARNING flow org whose reconcile is a learned library entry
     added this run), renders the engine-native Q7/Q8 cockpit line for each, and ASSERTS: (a) the
     active rule name matches the org's `reconcile`; (b) the SOURCE is classified correctly
     (registry / library / learned-this-run) — e.g. a learned entry added this run reports
     source=learned and learned-this-run=True with the evidence-gated `why` from its
     `decision://…/reconcile-learning`; (c) the rendered line carries Q7 (options) + Q8
     (recommendation/determination) per §7L; (d) deterministic (identical on re-run).
   - proves consistency: the engine-native Q7/Q8 line agrees with the existing runner-report lines
     from Sprint 16/17 on the same orgs.
3. **Real output:** new runner ALL PASS; the bike cockpit-render non-regression: the existing
   `run_adjudication_engine_demo.py` / `run_rule_library_demo.py` / `run_reconcile_learning_demo.py`
   still ALL PASS (byte-identical to before — you changed the engine, so re-verify deli/cove
   byte-identical); C1–C5 over any new fixtures green; full non-regression green; no new noun, 49
   `$defs`, SPEC v0.22.
4. **Honest docs** (`docs/ENGINE-Q7Q8-COCKPIT.md` + an additive appendix in
   `USER-AUTHORABLE-RULE-LIBRARY.md` and/or `RECONCILE-LEARNING.md`): the cockpit-Q7/Q8 line is the
   §7L surface reporting the ACTIVE rule + source + learned-or-not; what it shows for each source
   class; and a §16-style verdict on whether the engine now renders the rule as first-class operating
   reality (Q7 options + Q8 recommendation with authority) vs a runner-side artifact. Say plainly
   which.

## Mandatory rules
- **Write-first:** `sprints/sprint-18/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is `instances/contested_reality/adjudication_engine.py`
  (add the new `cockpit_q7q8`/`render_cockpit_q7q8` functions — do NOT rewrite `reconcile`/`run_scenario`/
  `_derive`/`SPEC_VOCAB`/`_aggregate`, which are frozen by Sprint-15/16/17). Keep 49 `$defs` + URI cap +
  SPEC v0.22. Re-verify `ros/`, the schema, the reference build, and the 12+ sector instances
  untouched. deli/cove byte-identical up to the clock.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-17 state): `run_reconcile_learning_demo.py`, `run_rule_library_demo.py`,
  `run_rule_authoring_demo.py`, `run_rule_comparison_demo.py`, `run_adjudication_engine_demo.py`,
  `conformance_adjudication.py` (16 labels), the 4 prior CR demos + conformances, `build_all.py` +
  `conformance_all.py`, S5 reference + conformance, `agent_demo` + conformance.
- New assertions ALL PASS: the engine-native Q7/Q8 line is correct + deterministic for ≥2 orgs with
  different rule sources; a learned-this-run rule reports source=learned + the evidence-gated why;
  Q7 (options) + Q8 (recommendation w/ authority) both present; it agrees with the Sprint-16/17
  runner-report lines; the engine's own cockpit render is produced WITHOUT per-org Python.
- Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema clean.

## Documentation (roll-forward)
- Add `docs/ENGINE-Q7Q8-COCKPIT.md`; append a Sprint-18 entry to `instances/README.md`; append an
  "Update after Sprint 18" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`;
  append an additive note to the rule-library / reconcile-learning docs (the Q7/Q8 line is now a
  first-class engine render).
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-18/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize what the engine-native §7L Q7/Q8 cockpit line reports (active
rule + source + learned-or-not + why per org), how it is generic and data-only, the ≥2-org proof that
it agrees with the runner-report lines, the honest §16 verdict (first-class engine render vs
runner-side artifact), and the verified build + conformance commands. Write the **next** sprint's
self-contained prompt at `sprints/sprint-19/PROMPT.md`.