# User-Authorable Rule DSL — RelationalOS (Sprint 15)

**Scope.** Sprint 14 made the evidence-reconciliation rule layer config-*selectable*: `cfg["reconcile"] =
{"rule", params}` dispatched through a registry of pure functions, with the rule **name** and every
**parameter** as config — but the rule's **body** (the pure support mapping) was still a Python
function authored in `adjudication_engine.py`; a genuinely new rule needed a one-time new function.
Sprint 15 makes the rule **body** itself authorable as **config TEXT**: a small, deterministic,
declarative **rule-authoring spec** (a dict of rule data) that the engine **compiles** into the very
same pure support function the registry runs. A **new rule is now authored entirely as data/text with
NO engine Python written for it.**

Everything below maps to real, exit-0 output. Additive only: frozen ontology (49 `$defs`), URI cap,
SPEC v0.22, `ros/` untouched, ~$0 deterministic local Python. Trust is still only ever moved by the
deterministic S5 formula; the §6 human remains the sole determiner.

---

## Where it lives
```
instances/contested_reality/adjudication_engine.py     registry rules (unchanged) + the rule-authoring
                                                        DSL interpreter (SPEC_VOCAB, compile_rule_spec)
instances/contested_reality/adjudication_configs.py    INSPECT + 3 registry variants (S14) + 3 spec-authored
                                                        variants (S15) as DATA
instances/contested_reality/run_rule_authoring_demo.py parity (spec == registry) + genuinely-new spec-only
                                                        rule; exit 0 = ALL PASS
instances/contested_reality/conformance_adjudication.py C1–C5 over 8 labels (deli, cove, 3 inspect registry
                                                        + inspect-anchor-spec/rec-spec/majority)
instances/contested_reality/docs/USER-AUTHORABLE-RULE-DSL.md   this document
```
Verified commands (from `instances/contested_reality/`, exit 0):
- `python3 run_rule_authoring_demo.py` → `RESULT: ALL PASS`
- `python3 run_adjudication_engine_demo.py` → `RESULT: ALL PASS` (deli/cove, unchanged)
- `python3 run_rule_comparison_demo.py` → `RESULT: ALL PASS` (Sprint-14 three-registry-rule proof, unchanged)
- `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python conformance_adjudication.py`
  → `ADJUDICATION-ENGINE CONFORMANCE: ALL PASS` (8 labels, C1–C5, 49 `$defs`)

## The rule-authoring format (a rule is config data)
A rule is declared, not coded, by adding a **rule-spec dict** to the org's `reconcile` block:

```python
cfg["reconcile"] = {
    "rule_spec": {
        "name": "majority-of-sources",        # informational (used in cockpit Q7 / reports)
        "aggregate": "<op>",                  # ONE of the fixed vocabulary below (required)
        "value_field": "reliability",         # reliability | confidence | reliability_x_confidence
        "admissible_kinds": None | [...],     # None = every Evidence.kind admissible; else a subset
                                              #   of {OBSERVATION, TESTIMONY, RECORD, ANCHORED}
        "source_threshold": 0.92,             # ONLY used when aggregate == "majority"
        "decay": None | {"as_of": "<RFC3339>", "half_life_days": N},   # optional recency weighting
    },
    # threshold / support_floor may sit inside `rule_spec` or flat here; the engine flattens them
    # into the SAME params used by the SHARED `_derive` — identical floors for spec- and registry rules.
}
```

### The fixed aggregation vocabulary (`eng.SPEC_VOCAB`) — the language's operators
| `aggregate` | per-claim support (0.0–1.0) |
|---|---|
| `max` | highest admissible source value (decay applied) — "one strong source suffices" |
| `mean` | arithmetic mean of admissible source values |
| `weighted-mean` | values weighted by each source's `verity.confidence` |
| `sum` / `count` | total / number of admissible sources |
| `majority` | (# admissible sources whose value ≥ `source_threshold`) ÷ (# admissible sources) — corroboration by many interdependent sources |

The interpreter (`_spec_value`, `_spec_decay_factor`, `_spec_admissible`, `_aggregate`,
`compile_rule_spec`, `_spec_support`) is the rule-authoring **language runtime**, authored once. It
re-uses the **same** `_derive` (disputed / conflict / determined / uncertainty from `support_floor` +
`threshold`) that every registry rule uses — so after compilation a spec rule is **indistinguishable
in shape** from a registry rule; that shared derive is the parity guarantee.

### Determinism
Same discipline as every rule: a spec's `decay` must anchor to an explicit `as_of` (never the
wall-clock); evidence captured after `as_of` keeps full weight (factor 1.0, no negative decay);
undateable capture is treated fresh. The engine is a pure function of (claims, evidence, spec,
params). The compiler is **strict** — an unknown `aggregate` op, an unknown `value_field`, an unknown
evidence `kind`, a `source_threshold` outside [0,1], or a non-RFC3339 `as_of` all raise loudly
(verified below); nothing is silently coerced.

## Parity: a spec is the SAME engine, not a different one — `run_rule_authoring_demo.py`
Re-express the two existing registry behaviors as specs and assert they reproduce the registry verdict
**exactly** on the identical `inspect` dispute:

| registry rule (S14) | equivalent spec (`rule_spec`) | per-claim support (reg == spec) |
|---|---|---|
| `strict-anchor-only` (kinds:[ANCHORED]) | `{aggregate:"max", value_field:"reliability", admissible_kinds:["ANCHORED"]}` | `passed 0.84 / failed 0.0` — **identical** |
| `recency-weighted-threshold` (as_of 8/31, hl 21d) | `{aggregate:"max", value_field:"reliability", decay:{as_of:"…", half_life_days:21}}` | `passed 0.7863 / failed 0.9` — **identical** |

The runner asserts both per-claim support maps AND the full dispute verdict tuple
(determined/disputed/uncertainty) are equal — proving a spec is not "a different engine", it is the
same engine driven by a config-declared rule body. All 8 fixture labels pass C1–C5.

## A genuinely NEW rule authored ONLY as a spec (never a registry function)
`majority-of-sources` is **not** in `eng.RULES` and was never a Python function. It is entirely the
config dict above: `{aggregate:"majority", value_field:"reliability", source_threshold:0.92}`. It
models a corroboration policy — *a claim is believed only to the fraction of its independent sources
that are individually credible* — the opposite of `best-reliability-threshold`'s "one star witness
suffices".

On the `inspect` dispute (buyer `failed` ← one recent TESTIMONY 0.90; company `passed` ← one recent
ANCHORED 0.84 + one old RECORD 0.97), `majority-of-sources` (bar 0.92) gives:
- `passed = 1/2 = 0.5` (only the 0.97 audit clears the bar) → below both floor(0.55) and threshold;
- `failed = 0/1 = 0.0` (the 0.90 testimony does not clear 0.92) → below both.

So neither claim is disputed, no claim is determined, `uncertainty=True` → the engine honestly ends
**UNRESOLVED** (OPEN, epistemic INSUFFICIENT_EVIDENCE) — **whereas the same org under
`best-reliability-threshold` DETERMINES `rework-partial-credit` (CLOSED)** (passed=0.97 clears
threshold). A rule entered the system **entirely through config text** and **changed the verdict**.
The runner asserts the majority support map is distinct from all three registry support maps
(`0.5/0.0` vs `0.97/0.9` vs `0.84/0.0` vs `0.7863/0.9`). Trust is unchanged (0.80) under every rule;
authority preserved; every run deterministic; every variant ends in a lawful terminal state.

## The expressiveness frontier (stated honestly — no perfection claimed)
A rule-authoring spec expresses: **which evidence kinds are admissible** × **which scalar is drawn
from each source** (reliability / confidence / product) × **an optional recency decay** × **one of a
FIXED set of aggregations**, folded through the shared derive floors. That is a genuine, small,
declarative language — and it demonstrably authors rules the registry never contained.

What it **cannot** express without a NEW primitive (a builtin) in the vocabulary:
- A rule needing a bespoke *per-rule transformation* the fixed ops don't name, e.g. a **Bayesian
  posterior**, a **custom multiplicative combination** of fields, a **provenance-dependent
  if/then** beyond `admissible_kinds`, or an aggregation not in `SPEC_VOCAB`. Adding such a rule
  requires adding that one primitive to `SPEC_VOCAB` (interpreter code) — after which it serves
  every org by config. This is the precise, remaining seam, and it is stated plainly: **the
  rule-authoring DSL covers the family of "filter + scalar + decay + aggregate" rules; it does not
  pretend to be arbitrary Python.** We did not smuggle a bespoke function in behind the `majority`
  spec — `majority` is a genuine, generally-useful operator of the language.
- The per-option **factor scores + weights** remain the org's authored value judgment (§7K.1, by
  design) and the **determination** remains the §6 human's authoritative call (`determination_policy`).
  Neither changed.

Determinism corner (best-effort ~$0): fixtures embed wall-clock envelope fields (`occurred_at`,
`made_at`), so "byte-for-byte reproducible" means *reproducible up to the clock* (Sprint-14 finding);
the rules themselves are pure functions of explicit inputs.

## §16 assessment — is the rule layer now **A — Yes** unconditionally?
**The rule BODY is now authorable as config text, and a genuinely new rule enters the system with NO
engine Python.** `cfg["reconcile"]["rule_spec"]` is a user-authored declarative spec that the engine
compiles into the identical pure support function the registry runs; Sprint 15 proves (a) two existing
rules re-expressed as specs reproduce their registry verdicts exactly (parity → same engine), and (b)
a genuinely new rule — `majority-of-sources`, never a registry function — drives a real lifecycle
and changes a determination-vs-UNRESOLVED verdict, authored only as config. That closes the precise
boundary Sprint 14 named. **Verdict: `A — Yes` for declarative, config-text rule authoring over the
shipped vocabulary** — the majority-of-sources rule was added wholly as data, no new engine Python.

The one honest qualifier: "A — Yes" is scoped to the **rule-authoring DSL's vocabulary**. It is not a
claim that *arbitrary* Python expressiveness is available as config. A rule that requires an op the
vocabulary does not yet contain (e.g. a Bayesian update) needs that one builtin added to the language
— after which it, too, is authorable as data by every org. That is the same seam any DSL has (the
language runtime vs the rules written in it), and it is disclosed precisely above rather than
concealed. Absent that, the config-text rule-authoring claim holds: a new rule = a spec dict.

*(Evidence: all assertions are real exit-0 output from `run_rule_authoring_demo.py`,
`run_adjudication_engine_demo.py`, `run_rule_comparison_demo.py`, and `conformance_adjudication.py`
over 8 labels, plus a full non-regression re-run of the Sprint-9/10/11/12 + reference + sector +
agent suites — all ALL PASS; SPEC v0.22, 49 `$defs`, `ros/` untouched.)*

---

## Update after Sprint 16 — the vocabulary is broadened; the frontier is a library
Sprint 16 takes the one disclosed seam and narrows it. The rule-authoring vocabulary now includes a
**genuinely NEW inference primitive, `bayesian-combine`** (a reliability-likelihood posterior /
independent-corroboration aggregate), authored ONCE as a general, deterministic + strict operator and
then authorable as data by ANY org. A rule using it (`independent-corroboration`) lives in the named,
cross-org **`RULE_LIBRARY`** and is reused by ≥2 orgs (goods-QC + clinical); on the `inspect` dispute
at reconcile threshold 0.98 it **flips the verdict** `max` cannot reach: single-source `max` (0.97)
clears nothing → **UNRESOLVED**, while its two independent witnesses combine to posterior 0.9961 →
**DETERMINED `rework-partial-credit`** — the "independent corroboration exceeds one strong source"
family the old vocabulary could not express. The §7L cockpit Q7 report names the ACTIVE rule and its
spec-authored-vs-registry source. See `USER-AUTHORABLE-RULE-LIBRARY.md`. Verdict: **A — Yes** for
declarative config-text rule authoring over the shipped vocabulary *including* the Bayesian-likelihood
family; a rule needing an op the vocabulary still does not name (a different posterior, a
provenance-conditional if/then, a different multiplicative combination) still needs that one builtin —
the precise, remaining dependence.