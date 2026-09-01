# SPRINT 16 — PROMPT  (User-authored RULE library: the rule-authoring DSL, reusable + broadened, surfaced on the cockpit)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprint 15 made the reconciliation rule **BODY** authorable as **config text**: a
declarative `rule_spec` (admissible evidence kinds × value_field × optional recency `decay` × one
fixed aggregation op in `eng.SPEC_VOCAB`) that `compile_rule_spec()` compiles into the same pure
support function the registry runs. It proved **parity** (two existing rules re-expressed as specs
reproduce their registry verdicts exactly) and that a **genuinely NEW** `majority-of-sources` rule —
never a registry function — entered the system wholly as a spec dict and flipped the `inspect`
verdict to UNRESOLVED. Its honest §16 verdict is **"A — Yes for declarative, config-text rule
authoring over the shipped vocabulary"**, with the disclosed seam that a rule needing an op *outside*
`SPEC_VOCAB` (e.g. a Bayesian posterior) still requires adding that one builtin to the language.
Sprint 16 takes that seam on: **add at least one genuinely NEW inference primitive to the vocabulary
(authorable once, then usable as data by every org), make spec-authored rules a reusable cross-org
RULE LIBRARY (named specs reused by more than one org), and surface the ACTIVE rule + its
spec-authored-vs-registry source on the §7L cockpit Q7.** Re-test whether the "needs a builtin" seam
for that new primitive now closes.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7J.9 (cockpit /
  authority), §7K.1 (Decision Learning, Trade-off, Policy execution "Condition → Decision → Action";
  extends OPA/Rego to the operating layer), §7L (ten morning questions incl. Q7/Q8), §7J.11 + §C16
  (URI cap), in full.
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md` (single-threaded,
  plan-before-build, real output, best-effort ~$0, additive, never bump SPEC for a capability-only
  change).
- The Sprint-15 engine + its honest finding (read FIRST, in full):
  - `/home/rlg/relational-os/instances/contested_reality/adjudication_engine.py` — the generic engine
    + the rule-authoring DSL: `RULES` registry (unchanged), `SPEC_VOCAB` (= {max, mean, weighted-mean,
    sum, count, majority}), `compile_rule_spec`, `_spec_value/_spec_decay_factor/_spec_admissible/
    _spec_source/_aggregate/_spec_support`, `reconcile` (accepts a registry `rule` OR `rule_spec`),
    `_derive`, `validate_config`, `run_scenario`.
  - `adjudication_configs.py` (deli, cove, `INSPECT` + `RULE_VARIANTS` inspect-best/anchor/rec +
    `SPEC_AUTHORED_RULES` inspect-anchor-spec/rec-spec/majority, `SCENARIOS`),
    `run_adjudication_engine_demo.py`, `run_rule_comparison_demo.py`, `run_rule_authoring_demo.py`
    (Sprint-15 ALL-PASS runner), `conformance_adjudication.py` (8 labels), `decision_learning.py`
    (Sprint-13 optional — reuse unchanged).
  - `/home/rlg/relational-os/instances/contested_reality/docs/USER-AUTHORABLE-RULE-DSL.md` — Sprint
    15's write-up; its **expressiveness frontier** + the "new builtin needed for an out-of-vocabulary
    rule" seam are the exact target. Also `docs/GENERALIZED-ADJUDICATION.md` (Sprint-13 §16 + the
    Sprint-14 additive note) and the Sprint-14 `docs/USER-AUTHORABLE-RULE-LAYER.md`.
  - Sprint-15 `sprints/sprint-15/summary.md` + `notes/findings.md`.
- Project invariants & operational recipes: the `relational-os` skill — frozen ontology / URI cap /
  49 `$defs`; additive fields only; single-threaded; plan-before-build; real tool output; ~$0; the
  footguns incl. `Graph.get` one-arg, `evidence` refs as ARRAYS, `{**graph.get(u), ...}` merge-not-
  replace, C2 RFC3339 temporal-suffix trap, strict C5 tables (dispute.json NOT validated), the
  Sprint-0 venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance,
  module-constant-vs-local shadowing, subpackage self-anchoring, runner CWD-sensitivity, and
  "byte-for-byte reproducible up to the clock" (Sprint-14 finding).

## What Sprint 16 IS and IS NOT
- **IS: (a)** add **≥1 genuinely NEW inference primitive** to the rule-authoring vocabulary — author
  it ONCE as a real, general operator (e.g. a **Bayesian / reliability-likelihood aggregate**, or a
  **meta-evidence corroboration combin**, or another op that is genuinely outside today's
  max/mean/weighted-mean/sum/count/majority family), so that a rule using it is thereafter authored
  as data by any org — then **author a new rule as a spec that uses that primitive** and drive an org
  with it (real verdict); **(b)** make spec-authored rules a **reusable cross-org RULE LIBRARY** —
  define named rule specs once and reuse the SAME named rule across ≥2 DIFFERENT orgs/disputes
  (e.g. run `majority-of-sources` on a second org, not just `inspect`) proving the DSL is not
  single-org specific; **(c)** surface the **ACTIVE rule + spec-authored-vs-registry source** on a
  §7L cockpit **Q7** line (the Sprint-15 optional, now required).
- **IS NOT:** a new service, a new URI noun, a schema edit, a change to the frozen ontology (49
  `$defs`, SPEC v0.22), a change to how Trust updates (S5 deterministic), or anything that replaces
  the human adjudicator (§6 floor, §7J.9). No frontier spend.

## The target (what "done" looks like)
1. **A new vocabulary primitive** (`SPEC_VOCAB` gains at least one genuinely NEW operator) authored as
   a real general aggregate — with its semantics documented. It must be **deterministic** (explicit
   params, never the wall-clock) and **strict** (validated loudly like the existing ops).
2. **A rule authored as a spec that uses the new primitive**, driven on an org with a **real verdict**
   — plus the **same named rule reused on ≥2 different orgs** (a rule library entry, not inspect-only).
   State plainly what the new primitive expresses that the old vocabulary could not (close the seam
   for that op), and any residual seam that still needs a builtin.
3. **Cockpit Q7 line** naming the ACTIVE rule and that it was **spec-authored** (vs registry-authored)
   in the rule-authoring runner/report.
4. **Real output:** the new runner ALL PASS; C1–C5 over the new fixtures green; full non-regression
   green (Sprint-13/14/15 + reference + sector + agent suites). No new noun, 49 `$defs`, SPEC v0.22.
5. **Honest docs** (`docs/USER-AUTHORABLE-RULE-LIBRARY.md` + an additive update to
   `docs/USER-AUTHORABLE-RULE-DSL.md`'s verification/frontier section): the new primitive, the rule
   library (named, reusable specs), the cockpit Q7 surface, the updated expressiveness frontier, and
   the §16 verdict (does the added primitive make part of the old "needs a builtin" seam close? on
   what does unconditional text-DSL authorship still depend, precisely?).
6. Every step signed and on the ledger; the human's determination keeps the authority it requires.

## Mandatory rules
- **Write-first:** `sprints/sprint-16/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication. If adding the new primitive turns
  out not to be a genuine, general operator (only serves one contrived rule), say so plainly and do
  NOT fake a general primitive by special-casing the inference; scope it honestly instead.
- **Additive, keep 49 `$defs` + URI cap + SPEC v0.22.** Re-verify `ros/`, the schema, the reference
  build, and the 12+ sector instances untouched. deli/cove byte-identical up to the clock.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-15 state): `run_rule_authoring_demo.py`, `run_rule_comparison_demo.py`,
  `run_adjudication_engine_demo.py`, `conformance_adjudication.py` (8 labels), all prior contested-
  reality demos + conformances, `build_all.py` + `conformance_all.py`, S5 reference + conformance,
  `agent_demo` + conformance.
- New assertions ALL PASS: ≥1 NEW primitive authored once and exercised via a spec-authored rule with
  a real verdict; the SAME named rule reused on ≥2 different orgs (a real rule library, not inspect-
  only); the cockpit Q7 line names the ACTIVE rule + spec-authored source; the new primitive is
  deterministic + strict; C1–C5 over the new fixtures; full non-regression green.
- Decide-and-document: argue the §16 seam for the NEW primitive now closes (A — Yes includes that op
  as authorable-as-data), and state precisely what still depends on a builtin (any rule shape the
  vocabulary still cannot express).

## Documentation (roll-forward)
- Add `docs/USER-AUTHORABLE-RULE-LIBRARY.md`; update `instances/README.md` (Sprint-16 entry); append
  an "Update after Sprint 16" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-
  SCENARIOS.md`; append a note to `docs/USER-AUTHORABLE-RULE-DSL.md` recording the new primitive +
  broadened frontier.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-16/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize the new vocabulary primitive, the rule library (named reusable
specs across ≥2 orgs), the cockpit Q7 surface, the updated frontier + §16 verdict (with the precise
remaining dependence), and the verified build + conformance commands. Write the **next** sprint's
self-contained prompt at `sprints/sprint-17/PROMPT.md`. Do NOT fake a general primitive by hiding
rule-specific Python behind the config.