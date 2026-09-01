# SPRINT 15 — PROMPT  (User-authored RULE text: a config DSL that compiles to the support mapping)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprint 14 made the reconciliation RULE layer config-authorable: `cfg["reconcile"] =
{rule, params}`, and the rule **selection** + every **parameter** are config (a rule choice demonstrably
flips one org's dispute between a DETERMINED `rework-partial-credit` and **UNRESOLVED**, with zero
engine change). Its honest §16 finding is that the rule's pure **support-mapping body** is still a
Python function inside a registry (`eng.RULES`) — a genuinely new combination shape needs a one-time
pure function + a registry entry, reused by config thereafter. Sprint 14's verdict is argued **"A —
Yes" for config-selected, registry-backed rule authoring**, but an **unconditional A** waits on the
rule BODY being authored as user text/config rather than Python. Sprint 15 makes the rule itself
**declared as config data**: a small, deterministic rule-AUTHORING format (a declarative spec that
maps recorded evidence → per-claim support) parsed by the engine into a verified pure support
function — so a NEW rule is added wholly as data/text, with NO engine Python authored for it. Then it
re-tests whether the §16 claim becomes a clean A.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7J.9 (cockpit /
  authority), §7K.1 (Decision Learning, Trade-off, Policy execution "Condition → Decision → Action";
  extends OPA/Rego to the operating layer), §7L (ten morning questions incl. Q7/Q8), §7J.11 + §C16
  (URI cap), in full.
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-
  build, real output, best-effort ~$0, additive, never bump SPEC for a capability-only change).
- The Sprint-14 engine and its honest finding (read FIRST, in full):
  - `/home/rlg/relational-os/instances/contested_reality/adjudication_engine.py` — the generic engine
    with the `RULES` registry + `_derive`/`_parse_rfc3339`/`normalize_reconcile` and the three registered
    rules (`best-reliability-threshold`, `strict-anchor-only`, `recency-weighted-threshold`). The
    `reconcile(sub, cfg)` dispatch + registry are WHAT Sprint 15 generalizes to a declarative spec.
  - `adjudication_configs.py` (the `inspect` org + `RULE_VARIANTS`, `deli`, `cove`, `SCENARIOS`),
    `run_adjudication_engine_demo.py`, `run_rule_comparison_demo.py`, `conformance_adjudication.py`
    (5 labels), `decision_learning.py` (Sprint-13 optional — reuse unchanged).
  - `/home/rlg/relational-os/instances/contested_reality/docs/USER-AUTHORABLE-RULE-LAYER.md` — Sprint
    14's write-up; its "What is still authored" + §16 boundary are the exact target.
  - `/home/rlg/relational-os/instances/contested_reality/docs/GENERALIZED-ADJUDICATION.md` — Sprint-13
    §16 + the Sprint-14 additive note to update.
  - Sprint-14 `sprints/sprint-14/summary.md` + `notes/findings.md`.
- Project invariants & operational recipes: the `relational-os` skill — frozen ontology / URI cap /
  49 `$defs`; additive fields only; single-threaded; plan-before-build; real tool output; ~$0;
  footguns incl. `Graph.get` one-arg and `evidence` refs as ARRAYS, `{**graph.get(u), ...}`
  merge-not-replace, C2 RFC3339 temporal-suffix trap, strict C5 tables (dispute.json NOT validated by
  C5), the Sprint-0 venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for
  conformance, module-constant-vs-local shadowing, subpackage self-anchoring, runner CWD-sensitivity,
  and the byte-for-byte-determinism modulo `now_iso()` note (Sprint-14 finding).

## What Sprint 15 IS and IS NOT
- **IS:** a **config-text rule-AUTHORING layer** — a small, deterministic rule-spec format (declared
  as JSON/dict config data: which evidence fields feed support, in what combination/weights, against
  what params) that the engine *compiles* into the same verified pure support function the registry
  runs today — so a NEW rule is authored ENTIRELY as data/text, with no Python function authored.
  The rule **body** becomes user-authored, not registry-code-authored. You must ship **at least two
  rules authored purely as rule-spec text** (e.g. express `strict-anchor-only` and
  `recency-weighted-threshold` — the existing registry behaviors — as declarative specs, PLUS at least
  ONE genuinely new rule authored only as a spec that the engine had never seen, e.g. a
  `majority-of-sources` or `weighted-evidence-mix` or `reliability-multi-vote` spec), and prove the
  same engine runs them with the **same verdict semantics OR a spec-authored verdict change** — with
  no new engine Python. The §16 A-Yes hinge is the rule BODY being authored as data.
- **IS NOT:** a new service, a new URI noun, a schema edit, a change to the frozen ontology (49
  `$defs`, SPEC v0.22), a change to how Trust updates (S5 deterministic), or anything that replaces
  the human adjudicator (§6 floor, §7J.9). No frontier spend.
- **Optional, additive (do if it fits the same build, else defer):** a cockpit-Q7 line stating the
  ACTIVE rule and that it was **spec-authored** (vs registry-authored), and/or re-render the rule→
  verdict comparison with one spec-authored rule highlighted.

## The target (what "done" looks like)
1. A **rule-authoring format in config data**: a rule is a declarative spec (fields, weights,
   admissible `kinds`, params like `as_of`/`half_life_days`/`majority_frac`) that the engine compiles
   deterministically into the identical pure support function the registry runs. A new rule is added
   by adding a spec dict (config) — no Python. State plainly what the format CAN express and what it
   CANNOT (the honest frontier of a declarative DSL vs arbitrary Python).
2. **≥2 rules authored purely as specs actually exercised**, and at least ONE independent test:
   (a) re-express `strict-anchor-only` and `recency-weighted-threshold` as specs and show the org
   verdicts MATCH the registry versions (so a spec is not a different engine); AND (b) author **one
   genuinely NEW rule only as a spec** (never a registry function) and drive an org/sub-dispute with
   it — showing a new rule can enter the system through config text alone and change/determine a
   verdict. deli/cove (and the default `best-reliability-threshold`) remain byte-for-byte reproducible.
3. Real output: the new runner ALL PASS; C1–C5 over the new fixtures green; full non-regression green
   (Sprint-13/14 + reference + sector + agent suites). No new noun, 49 `$defs`, SPEC v0.22.
4. Honest documentation (`docs/USER-AUTHORABLE-RULE-DSL.md`): the rule-authoring format, the
   expressiveness frontier (what a declarative spec covers; what it cannot and would still need a
   Python/builtin — say so plainly, never fake), and whether the §16 verdict is now **A — Yes**
   unconditionally (or precisely on what it still hinges).
5. Every step signed and on the ledger; the human's determination keeps the authority it requires.

## Mandatory rules
- **Write-first:** `sprints/sprint-15/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication. If the declarative surface turns
  out too small to express a genuinely new rule without a new builtin, say so plainly and specify the
  missing builtin — do NOT fake a "spec-only" rule by smuggling Python in.
- **Additive, keep 49 `$defs` + URI cap + SPEC v0.22.** Re-verify `ros/`, the schema, the reference
  build, and the 12+ sector instances untouched.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (the Sprint-14 state): `run_rule_comparison_demo.py`, `run_adjudication_
  engine_demo.py`, `conformance_adjudication.py` (5 labels), all prior contested-reality demos +
  conformance, `build_all.py` + `conformance_all.py`, S5 reference + conformance, `agent_demo`.
- New assertions ALL PASS: ≥2 rules authored purely as spec-config each drive a real lifecycle;
  the spec-authored versions reproduce the registry verdicts for strict-anchor/recency; the SAME
  engine runs a **genuinely new spec-only rule** that was never a registry function and produces a
  real (possibly different) verdict; deli/cove byte-identical with their original rule; C1–C5 over
  the new fixtures; full non-regression green.
- Decide-and-document: argue **A — Yes** only if a genuinely new rule is added entirely through
  config/text (no new Python), else state plainly why not (e.g. the format still needs a builtin
  primitive the spec cannot conjure).

## Documentation (roll-forward)
- Add `docs/USER-AUTHORABLE-RULE-DSL.md`; update `instances/README.md`; append an "Update after
  Sprint 15" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; append a
  note to `docs/USER-AUTHORABLE-RULE-LAYER.md` (Sprint-14) that its rule-BODY boundary is addressed.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-15/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize the rule-authoring layer (what became authorable as config
text, the format + its expressiveness frontier, the ≥2 spec-authored rules and the ≥1 genuinely-new
spec-only rule with real verdicts and at least one rule-authoring-only change that moved/confirmed a
verdict, verified build + conformance commands) and give an honest verdict on whether the §16
assessment now holds as **A — Yes** unconditionally (and on what it still depends, precisely). Write
the **next** sprint's self-contained prompt at `sprints/sprint-16/PROMPT.md`. Do NOT fake a spec-only
rule by hiding engine Python behind the config.