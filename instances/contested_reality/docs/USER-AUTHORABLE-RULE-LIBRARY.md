# User-Authorable Rule Library — RelationalOS (Sprint 16)

**Scope.** Sprint 15 made the evidence-reconciliation rule **BODY** authorable as config TEXT (the
rule-authoring DSL: `SPEC_VOCAB` + `compile_rule_spec`), and honestly disclosed one remaining seam:
an op **outside** `SPEC_VOCAB` (e.g. a Bayesian posterior) still needed a new builtin — interpreter
code — after which it too is authorable as data by every org. Sprint 16 takes that seam on with
three moves: (a) add a **genuinely NEW inference primitive** to the vocabulary once — `bayesian-combine`
(a reliability-likelihood posterior / independent-corroboration aggregate), so a rule using it is
thereafter authored as data by any org; (b) turn spec-authored rules into a **named, reusable
cross-org RULE LIBRARY** (the same spec dict reused across ≥2 different orgs); (c) surface the
**ACTIVE rule + its spec-authored-vs-registry source** on a §7L cockpit **Q7** line.

Everything maps to real, exit-0 output. Additive only: frozen ontology (49 `$defs`), URI cap,
SPEC v0.22, `ros/` untouched, ~$0 deterministic local Python. Trust is only ever moved by the
deterministic S5 formula; the §6 human remains the sole determiner.

---

## Where it lives
```
instances/contested_reality/adjudication_engine.py    registry rules (unchanged) + the rule-authoring
                                                        DSL; NEW `bayesian-combine` primitive
instances/contested_reality/adjudication_configs.py   RULE_LIBRARY (named specs) + reuse org variants
instances/contested_reality/run_rule_library_demo.py  cross-org reuse + the verdict-flip proof; exit 0
instances/contested_reality/conformance_adjudication.py13-label C1–C5 (8 prior + 5 Sprint-16 labels)
instances/contested_reality/docs/USER-AUTHORABLE-RULE-LIBRARY.md   this document
```
Verified commands (from `instances/contested_reality/`, exit 0):
- `python3 run_rule_library_demo.py` → `RESULT: ALL PASS`
- `python3 run_rule_authoring_demo.py` / `run_rule_comparison_demo.py` / `run_adjudication_engine_demo.py`
  → `RESULT: ALL PASS` (unchanged, deli/cove byte-identical)
- `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python conformance_adjudication.py`
  → `ADJUDICATION-ENGINE CONFORMANCE: ALL PASS` (13 labels, C1–C5, 49 `$defs`)
- Full non-regression (sectors build_all + conformance_all; S5 reference; agent demo+conformance;
  the four prior contested-reality demos + conformances) → all exit 0.

## (a) The new primitive: `bayesian-combine`
A general, deterministic, strictly-validated aggregate that combines a claim's admissible source
values as **independent likelihoods** under Bayes:
```
posterior = O / (1 + O),  where O = odds(prior) · Π_i ( v_i / (1 − v_i) )   — v_i = value of source i
```
- `prior` is REQUIRED and authored by the rule (explicit, in `(0,1)`), never the wall-clock →
  deterministic.
- Empty source set → posterior = `prior` (no evidence about the claim → the prior).
- A `1.0` source → posterior 1.0; a `0.0` source → posterior 0.0 (a certain source pins the claim).
- Strict: `compile_rule_spec` rejects a missing / `0` / `1` / `>1` / non-numeric `prior` loudly; the
  op is a real, single, general operator in `_aggregate` (NOT rule-specific Python hidden behind the
  config). `verity.confidence` is deliberately unused — each independent source contributes one equal
  likelihood (a distinct semantic from `weighted-mean`).

**What it expresses that the old vocabulary could NOT:** `max` is bounded by the single strongest
source — it can never exceed the best witness. `bayesian-combine` lets **many weak-but-independent**
sources raise a claim's support ABOVE every individual source (true corroboration synthesis). Unit-proven:
`bayesian-combine(3×0.7, prior 0.7) = 0.9674 > max = 0.7`. No prior op could reach that.

### The verdict flip it produces (real output)
At reconcile **threshold 0.98** on the `inspect` ($54k goods-QC) dispute, changing ONLY the rule:
- `best-reliability-threshold` (`max`): the strongest witness is 0.97 → clears nothing →
  **UNRESOLVED** (OPEN).
- `independent-corroboration` (bayesian-combine): the two independent witnesses (0.84 anchored +
  0.97 record) combine to posterior **0.9961** → clears 0.98 → **determined `rework-partial-credit`
  (CLOSED)**.

Same org, same evidence, same threshold — only the `reconcile` rule differs. `max` literally cannot
do this; the new primitive can, and it is authorable as data by every org.

## (b) The named, reusable cross-org RULE LIBRARY
`RULE_LIBRARY` in `adjudication_configs.py` holds named specs **created once**; an org reuses one by
reference (`reconcile = {"rule_spec": RULE_LIBRARY["<name>"], threshold, support_floor}`). Proof of
reuse is `is`-identity (the SAME dict object, not a copy) **and** driving each library rule on ≥2
genuinely different orgs:

| library rule | aggregate | reused by org(s) | outcome |
|---|---|---|---|
| `majority-of-sources` | majority | `inspect-majority-lib` + `deli-majority` (goods-QC **and** freight) | UNRESOLVED / partial-settlement |
| `independent-corroboration` | bayesian-combine | `inspect-corroboration` + `cove-corroboration` (goods-QC **and** clinical) | rework-partial-credit / step-therapy-first |

(`strict-anchor-only` / `recency-weighted-threshold` are also named in the library as the Sprint-15
parity specs.) deli/cove original configs are untouched and stay registry `best-reliability-threshold`,
byte-identical; the reuse runs under new labels via the established `inspect_variant` pattern.

## (c) §7L cockpit Q7 — ACTIVE rule + source
The runner renders a Q7 line per org naming the **ACTIVE rule** and that it is **spec-authored
(a `RULE_LIBRARY` data dict), not an engine registry function** — e.g.
`cockpit-q7-rule-library.md`: `inspect-corroboration: ACTIVE rule = independent-corroboration —
spec-authored (RULE_LIBRARY data), aggregate bayesian-combine → determination=rework-partial-credit`.
The report `rule-library.{md,json}` carries the library table + verdict-flip proof.

## The expressiveness frontier (updated — the seam narrows, honestly)
Sprint 15 left a named seam: an op outside `SPEC_VOCAB` (e.g. a Bayesian posterior) needed a new
builtin. Sprint 16 **adds that builtin** (`bayesian-combine`), so the *independent-corroboration /
reliability-likelihood* family is now **authorable as data by every org** — part of the old seam is
closed. The residual dependence is now precisely:
- A rule requiring an op the vocabulary still does NOT name — e.g. a *different* posterior shape, a
  **provenance-conditional if/then** beyond `admissible_kinds`, or a **custom multiplicative
  combination** distinct from this one — still needs that one primitive added as interpreter code
  (interpreter code), after which it too serves every org by config. This is the standard
  language-runtime-vs-rules-in-it boundary any DSL has, and it is stated plainly, not concealed.
- The per-option factor scores + weights remain the org's authored value judgment (§7K.1, by design);
  the determination remains the §6 human's authoritative call (`determination_policy`). Neither changed.

## §16 assessment
**Verdict: `A — Yes` for declarative, config-text rule authoring over the shipped vocabulary,
now INCLUDING the independent-corroboration (Bayesian-likelihood) op family.** The new primitive is
authored ONCE as a genuine, general, deterministic + strict operator; a rule using it
(`independent-corroboration`) is authored as library data, reused by ≥2 orgs, and produces a real
verdict flip (`max` UNRESOLVED → bayesian DETERMINED) — closing the Sprint-15 told seam for this op
family. What unconditional text-DSL authoring still depends on, precisely: any rule shape whose op
the vocabulary still cannot express needs that one builtin added to the language (interpreter code),
after which it too is authorable-as-data by every org. That is the honest, remaining boundary — a
property of every DSL, not a hidden engine change.

*(Evidence: all assertions are real exit-0 output from `run_rule_library_demo.py`,
`run_rule_authoring_demo.py`, `run_rule_comparison_demo.py`, `run_adjudication_engine_demo.py`, and
`conformance_adjudication.py` over 13 labels, plus the full non-regression suite — all ALL PASS;
SPEC v0.22, 49 `$defs`, `ros/` untouched, only catalog URI schemes in the new fixtures.)*

---

## Sprint 17 appendix — learning feeds the library (the learned rule is a library entry)
Sprint 17 (see `RECONCILE-LEARNING.md`) adds the missing loop: **the reconciliation RULE's parameter
can now be learned from realized outcomes**, and the learned artifact is a **new named `RULE_LIBRARY`
entry** — so the library is not just hand-authored; it grows from recorded experience.

- **What is learned:** one reconcile parameter (the `threshold`) via a deterministic, clamp-bounded,
  evidence-gated update `learn_threshold(prior, realized, lr, [lo, hi])` from a RECORDED, realized
  outcome (the §7K.1 Decision→Expected→Actual→Variance→WHY→change-future-policy loop). It learns the
  RULE, not the answer to any case.
- **Learning→library flow:** episode A (`inspect-learn-a`) realizes an outcome value 0.90 under a
  0.95 threshold → learns 0.91 → a NEW library spec `calibrated-threshold-091` (aggregate `max` +
  additive `learned_threshold`/`calibrated_from`/`bound`/`why`) is added to `ac.RULE_LIBRARY` and
  recorded as an append-only signed `rule://` (kind=PROCEDURE) + `decision://` (with `rules_applied`).
- **Reuse:** `inspect-learn-b` (a SECOND, distinct dispute) and `deli-learn` (a genuinely different
  org) both reuse the SAME `RULE_LIBRARY["calibrated-threshold-091"]` dict by `is`-identity — the
  learned rule is a reusable, library-shared named spec, not a one-case patch.
- **Containment (so the library can't be moved toward self-serving goalposts):** Trust is never
  touched (S5 only), `determination_policy` is never edited (the §6 human's call), the ledger is
  append-only (prior events byte-identical), and every learned update is rebound from an explicit
  `[lo, hi]` + explicit prior — never the wall-clock, never unbounded.
- **Honest verdict:** this is **calibrated re-authoring** (a bounded update of a rule parameter from
  outcomes), not autonomous learning — a real and additive extension of the library authoring story
  established here. `run_reconcile_learning_demo.py` → ALL PASS;
  `conformance_adjudication.py` → **16 labels** C1–C5 ALL PASS (49 `$defs`).

## Sprint 18 appendix — the Q7/Q8 line is now a first-class ENGINE render (the library's operating surface)
Sprint 18 makes the §7L Q7/Q8 cockpit line a **generic engine render**: `adjudication_engine`
`cockpit_q7q8(cfg, sub, *, library=None)` / `render_cockpit_q7q8(...)` reports the ACTIVE reconcile
rule, its source class (registry / **rule-library** / learned / rule-spec-authored), learned-or-not
this run, and the evidence-gated why — data-only, from the org's own config + ledger. For a
`RULE_LIBRARY` spec the source reports **rule-library** (matched by `is`-identity/name against the
library you pass in); for a learned library entry it reports **learned** (and learned-this-run=True
only when that org's ledger actually recorded its reconcile-learning decision this run). The
Sprint-16 `cockpit-q7-rule-library.md` line is now a *view* over that engine render, not the only
place the rule-as-operating-reality (Q7 options + Q8 recommendation with authority) is surfaced.
`run_cockpit_q7q8_demo.py` proves a 4-org / 3-source-class agreement with the Sprint-16/17 report
lines. **§16 verdict: first-class engine render.** Full write-up:
`docs/ENGINE-Q7Q8-COCKPIT.md`.