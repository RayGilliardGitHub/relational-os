# SPRINT 17 — PROMPT (Decision Learning from the reconciliation layer: the learned rule, honest + additive)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprint 16 turned the evidence-reconciliation RULE into a named, cross-org **RULE LIBRARY**
and added a genuinely NEW inference primitive (`bayesian-combine`), with the ACTIVE rule + source on
§7L Q7. Sprint 17 opens a NEW thread that Sprint 13 explicitly kept optional (`decision_learning.py`
exists but was never wired INTO the reconcile rule choice): **decision learning over the reconciliation
layer** — whether the engine can honestly LEARN a better reconciliation RULE (its params) from realized
outcomes, without subverting the frozen `decision://` evidence, the deterministic S5 Trust, or the §6
human's authority. The trust-sensitive question is whether "learning" degrades into the machine moving
its own goalposts — it must not.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7J.9 (cockpit /
  authority), §7K.1 (Decision Learning, Trade-off, Policy execution in full), §7L (ten morning
  questions incl. Q7/Q8), §7J.11 + §C16 (URI cap), in full.
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  best-effort ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `/home/rlg/relational-os/instances/contested_reality/adjudication_engine.py` (the generic engine +
    rule-authoring DSL `SPEC_VOCAB` incl. the Sprint-16 `bayesian-combine`; `_derive`, `reconcile`,
    `run_scenario`), `adjudication_configs.py` (`RULE_LIBRARY`, DELI/COVE/INSPECT + variants),
    `decision_learning.py` (Sprint-13 optional — currently NOT wired into the reconcile rule).
  - Sprint-16 docs: `instances/contested_reality/docs/USER-AUTHORABLE-RULE-LIBRARY.md` (new) +
    `docs/USER-AUTHORABLE-RULE-DSL.md` (its "Update after Sprint 16" appendix), and the Sprint-13
    `docs/GENERALIZED-ADJUDICATION.md` (the §7K.1 decision-learning section + the Sprint-16 note).
  - Sprint-16 `sprints/sprint-16/summary.md` + `notes/findings.md`.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs`; additive
  only; single-threaded; plan-before-build; real tool output; ~$0; the footguns incl. `Graph.get`
  one-arg, `evidence` refs as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2 RFC3339
  temporal-suffix trap, strict C5 tables, the Sprint-0 venv, module-constant-vs-local shadowing,
  subpackage self-anchoring, runner CWD-sensitivity, byte-for-byte up to the clock.

## What Sprint 17 IS and IS NOT
- **IS:** a decision-Learning step **at the reconcile layer**: define what a "better reconciliation
  rule" means from RECORDED, realized outcomes (not from hindsight on the same case), learn the
  rule's parameter(s) (e.g. the `threshold`, or a `support_floor`, or a `source_threshold`, or a
  `prior` for `bayesian-combine`) as an **additive, clamp-bounded, evidence-gated update** — and
  prove it is **contained**: (a) it cannot lower the §6 human's authority (determination stays the
  human's call), (b) it cannot raise its own scoped Trust (S5 deterministic only), (c) the learned
  rule is recorded as a NEW `rule://`…/`policy://` object + a signed event on the immutable ledger
  (history not rewritten) so an auditor sees the layering; and the NEW rule (if adopted) is a
  `RULE_LIBRARY` dict any org can reuse — i.e. **learning feeds the library**.
- **IS NOT:** a new service, a new URI noun, a schema edit, a change to Trust semantics (S5), a
  change that lets the machine overrule the §6 human (determination_policy unchanged), or anything
  that rewrites past decisions/evidence. No frontier spend. ~$0 deterministic local Python.

## The target (what "done" looks like)
1. A **learning function** (`reconcile_learning.py` or extend `decision_learning.py`) that, given a
   realized outcome for a rule + a set of past reconciled claims/evidence + the true/final
   determination, computes an **additive, clamp-bounded** parameter update and returns a NEW
   `rule_spec`/params dict (bound explicit; deterministic; evidenced). Honest labels: it learns the
   RULE, not the answer.
2. A **containment contract tested real**: assertions that the learned update (a) never touches
   Trust (S5 untouched), (b) never removes the human's authority (determination_policy intact), (c)
   never rewrites the ledger (append-only; a new decision/rule object + event recorded), (d) is
   rebound from an EXPLICIT prior/floor (never the wall-clock, never unbounded).
3. **Learning feeds the RULE LIBRARY:** a run that takes an org (e.g. `inspect`) whose realized
   outcome indicates the chosen reconcile threshold was too weak/strong, learns a new
   threshold/param, writes the learned `rule` as a NEW `RULE_LIBRARY` entry + signed `decision://`
   event, and re-drives a SECOND, future dispute with the learned rule — showing the library entry
   is a reusable named spec, not a one-case patch. (A second dispute means a DIFFERENT predicate set;
   do not re-run the same case and claim "learning".)
4. A **§7L Q7/Q8 cockpit line** reporting the ACTIVE (learned or not) reconcile rule, its source,
   and whether a learning step changed it this run + why (evidence-gated).
5. **Real output:** the new runner ALL PASS; C1–C5 over any new fixtures green; full non-regression
   green (all Sprint-13/14/15/16 runners + reference + sector + agent suites). No new noun, 49
   `$defs`, SPEC v0.22.
6. **Honest docs** (`docs/RECONCILE-LEARNING.md` + an additive appendix in `USER-AUTHORABLE-RULE-
   LIBRARY.md`): the learning rule, the containment contract, what is learned vs what stays the §6
   human's, and a §16-style verdict — does the engine "learn" without subverting authority/Trust, or
   is it honest to call it **calibrated re-authoring** (the rule author updating a param from
   outcomes), which is a different and defensible claim? Say plainly which.

## Mandatory rules
- **Write-first:** `sprints/sprint-17/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication. If "learning" turns out to be
  only a docile re-authoring, say so plainly and ship the calibrated-re-authoring story truthfully —
  never fake autonomy.
- **Additive, keep 49 `$defs` + URI cap + SPEC v0.22.** Re-verify `ros/`, the schema, the reference
  build, and the 12+ sector instances untouched. deli/cove byte-identical up to the clock.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-16 state): `run_rule_library_demo.py`, `run_rule_authoring_demo.py`,
  `run_rule_comparison_demo.py`, `run_adjudication_engine_demo.py`, `conformance_adjudication.py`
  (13 labels), the 4 prior CR demos + conformances, `build_all.py` + `conformance_all.py`, S5
  reference + conformance, `agent_demo` + conformance.
- New assertions ALL PASS: a learned (additive, clamp-bounded, deterministic) reconcile param from a
  realized outcome on dispute #1, applied (as a NEW `RULE_LIBRARY` named spec + signed event) to a
  SECOND, distinct dispute; Trust untouched (S5 only), authority untouched (determination_policy
  intact), ledger append-only (no rewrite); the §7L Q7/Q8 line reports active rule + learned-or-not
  + evidence-gated reason; the learning layer is additive (new `policy://`/`rule://`-shaped objects
  only — CONFIRM these names fit the frozen catalog or carry them additively on existing `$defs`;
  do NOT invent a noun); C1–C5 over new fixtures green; full non-regression green.
- Decide-and-document a §16 verdict: is this genuine contained learning, or calibrated re-authoring?
  State it plainly with the precise boundary (what the machine may and may not move).

## Documentation (roll-forward)
- Add `docs/RECONCILE-LEARNING.md`; append a Sprint-17 entry to `instances/README.md`; append an
  "Update after Sprint 17" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-
  SCENARIOS.md`; append an additive note to `docs/USER-AUTHORABLE-RULE-LIBRARY.md` (learning → the
  library).
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-17/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize the learning layer (what is learned, how it is contained and
bounded), the learning→library flow across ≥2 distinct disputes, the §7L Q7/Q8 cockpit line, the
honest §16 verdict (genuine learning vs calibrated re-authoring, precisely), and the verified build +
conformance commands. Write the **next** sprint's self-contained prompt at
`sprints/sprint-18/PROMPT.md`. Do NOT fake autonomy or let the machine move Trust/authority.