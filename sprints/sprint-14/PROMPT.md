# SPRINT 14 — PROMPT  (User-authorable dispute DSL: generalize the RULE layer)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprint 13 proved adjudication is now a *configurable capability*: one generic engine
(`instances/contested_reality/adjudication_engine.py`) drives ≥2 different org disputes
(`deli`, `cove`) from config data alone, with the business-model weights, resolution options,
per-option factor scores, floor-gated set + penalty, authority, and determination policy all in
`adjudication_configs.py` — no per-scenario code. Its honest residual finding is that **the
evidence-reconciliation RULE is still a single named semantic** (`best-reliability-threshold`):
only its *parameters* (`threshold`, `support_floor`) are config; a genuinely different rule shape
(e.g. recency-decay, Bayesian combination, majority-of-sources, strict-anchor-only) still requires
writing a new rule function in the engine. Sprint 13's §16 verdict is "B+ — materially toward A", and
it says a user-authorable dispute DSL is the step that would let the verdict be argued as a clean
"A — Yes". Sprint 14 makes the rule layer itself user-authorable, then re-tests the §16 claim.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). Read §6 (human floor), §7J.9 (cockpit /
  authority), §7K.1 (Decision Learning, Trade-off, Policy execution: "Condition → Decision → Action";
  extends OPA/Rego to the operating layer), §7L (ten morning questions incl. Q7/Q8), §7J.11 + §C16
  (URI cap), in full.
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-
  build, real output, best-effort ~$0, additive, never bump SPEC for a capability-only change).
- The engine and its recipe (read FIRST, in full):
  - `/home/rlg/relational-os/instances/contested_reality/adjudication_engine.py` — the generic engine;
    the `reconcile(sub, cfg)` function and the `reconcile` config block are what Sprint 14 generalizes.
  - `adjudication_configs.py` (the two org scenarios as data), `run_adjudication_engine_demo.py`
    (the generalization proof), `conformance_adjudication.py` (C1–C5), `decision_learning.py`
    (Sprint-13 optional realized-cost weights — reuse unchanged).
  - `/home/rlg/relational-os/instances/contested_reality/docs/GENERALIZED-ADJUDICATION.md` — the §16
    verdict and the exact residual hinge Sprint 14 targets.
  - The Sprint-13 `summary.md` + `notes/findings.md` (`sprints/sprint-13/`).
- Project invariants & operational recipes: the `relational-os` skill — frozen ontology / URI cap /
  49 `$defs`; additive fields only; single-threaded; plan-before-build; real tool output; ~$0; footguns
  incl. `Graph.get` one-arg and `evidence` refs as ARRAYS, `{**graph.get(u), ...}` merge-not-replace,
  C2 RFC3339 temporal-suffix trap, strict C5 tables, the Sprint-0 venv
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance, the
  module-constant-vs-local shadowing trap, subpackage self-anchoring, and runner CWD-sensitivity.

## What Sprint 14 IS and IS NOT
- **IS:** an **additive, config-authorable rule layer** — a small, deterministic rule registry where a
  new reconciliation rule is DECLARED in config (name + parameters + a pure mapping from the recorded
  evidence to per-claim support / conflict / uncertainty verdicts) rather than written as engine code.
  The engine delegates to the configured rule. You must ship **at least two distinct, working rules**
  (the existing `best-reliability-threshold` PLUS a genuinely different one, e.g.
  `recency-weighted-threshold` or `majority-of-sources` or `strict-anchor-only`), each expressible as
  config data, and re-prove the SAME engine drives the existing `deli`/`cove` orgs plus at least one
  org or sub-dispute that materially changes its DISPUTED / determined / UNRESOLVED outcome solely by
  choosing a different configured rule — with NO engine-side code change for the new rule.
- **IS NOT:** a new service, a new URI noun, a schema edit, or a change to the frozen ontology (49
  `$defs`, SPEC v0.22). No change to how Trust updates (S5 deterministic). Nothing auto-executes or
  replaces the human adjudicator (§6 floor, §7J.9 unchanged). No frontier spend.
- **Optional, additive (do if it fits the same build, else defer):** re-render the §7L cockpit Q7 to
  show the rule choice (the report already shows the weights/ranking/gating; add one line naming the
  active reconciliation rule + its verdict), and/or show learned-weights drift across two config-driven
  runs of one org.

## The target (what "done" looks like)
1. A **config-authorable reconciliation layer**: `reconcile` in config becomes
   `{"rule": "<name>", "params": {...}}` where `<name>` resolves via a tiny deterministic registry
   inside the engine; a *new* rule is added by adding a (config-safe) registry entry + a pure function,
   then selecting it from config. The existing `deli`/`cove` outputs remain byte-for-byte reproducible
   with their current rule/params (the registry must default to identical behavior).
2. **≥2 distinct rules actually exercised**: run enough orgs/sub-disputes that at least one selects a
   DIFFERENT rule from the other and that choice changes a verdict (e.g. a claim that was DISPUTED
   under one rule becomes DETERMINED/UNDETERMINED under another), demonstrating the rule layer is real,
   not a flag.
3. Real output: all engine runs ALL PASS; C1–C5 over the new fixtures green; full non-regression green
   (Sprints 9–13 + reference + sector + agent suites). No new noun, 49 `$defs` intact, SPEC v0.22.
4. Honest documentation (`docs/USER-AUTHORABLE-RULE-LAYER.md`): what became config-authorable, what is
   still authored (the rule *mapping* itself is authored code in the registry; the *selection* is config
   — say so plainly), and whether the §16 verdict can now be argued **A — Yes** (or precisely on what it
   still hinges, e.g. rules are still Python functions, not end-user-authored micro-DSL text).
5. Every step signed and on the ledger; the human's determination keeps the authority it requires.

## Mandatory rules
- **Write-first:** `sprints/sprint-14/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive, keep 49 `$defs` + URI cap + SPEC v0.22.** Re-verify `ros/`, the schema, the reference
  build, and the 12+ sector instances untouched.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (the Sprint-13 state): `run_adjudication_engine_demo.py`, `conformance_
  adjudication.py`, all four prior contested-reality demos + conformance, `build_all.py` +
  `conformance_all.py`, S5 reference + conformance, `agent_demo`.
- New assertions ALL PASS: ≥2 distinct configured rules each drive a real lifecycle; the same engine
  changes only by config between rules; a rule choice changes a DISPUTED/determined/UNRESOLVED verdict;
  existing `deli`/`cove` reproducible byte-identical with their original rule; C1–C5 over new fixtures;
  full non-regression green.
- Decide-and-document cache for the §16 verdict: argue **A — Yes** if a truly new rule was added
  entirely through config/data, or state plainly why not (rule body still authored Python).

## Documentation (roll-forward)
- Add/extend `docs/USER-AUTHORABLE-RULE-LAYER.md`; update `instances/README.md`; append an
  "Update after Sprint 14" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-14/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize the config-authorable rule layer (what became configurable,
where it lives, the ≥2 rules with real verdicts and at least one rule-change that moved a verdict,
verified build + conformance commands) and give an honest verdict on whether the §16 assessment now
holds as **A — Yes** (and on what precisely it would still depend, if anything). Write the **next**
sprint's self-contained prompt at `sprints/sprint-15/PROMPT.md`. If a rule cannot be generalized
without a new primitive or user-authored micro-DSL text, say so plainly and specify it rather than
faking it.