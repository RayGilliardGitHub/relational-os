# User-Authorable Rule Layer — RelationalOS (Sprint 14)

**Scope.** Sprint 13 made adjudication a *configurable* capability but left one residual code
semantic: the evidence-reconciliation RULE was a single named function (`best-reliability-threshold`)
whose only *parameters* were config — a genuinely different rule shape still meant writing a new
function in the engine. Sprint 14 makes the **rule layer itself config-authorable**: a tiny
deterministic registry inside the engine where a NEW rule is added by registering a pure function +
selecting it from config, with **no engine-side change for the new rule**. It then proves the layer
is real by driving one org's dispute through three different configured rules and showing a rule
choice swings the outcome from a determination to **UNRESOLVED**.

Everything below maps to real, exit-0 output. Additive only: frozen ontology (49 `$defs`), URI cap,
SPEC v0.22, `ros/` untouched, ~$0 deterministic local Python. Trust is still only ever moved by the
deterministic S5 formula; the §6 human remains the sole determiner.

---

## Where it lives
```
instances/contested_reality/adjudication_engine.py          registry + reconcile dispatch (generic)
instances/contested_reality/adjudication_configs.py         INSPECT org + 3 rule variants as DATA
instances/contested_reality/run_rule_comparison_demo.py     ONE engine, 3 rules, verdict flip (exit 0 = ALL PASS)
instances/contested_reality/conformance_adjudication.py     C1–C5 over deli/cove + inspect-{best,anchor,rec}
instances/contested_reality/docs/USER-AUTHORABLE-RULE-LAYER.md   this document
```
Verified commands (from `instances/contested_reality/`, exit 0):
- `python3 run_rule_comparison_demo.py` → `RESULT: ALL PASS`
- `python3 run_adjudication_engine_demo.py` → `RESULT: ALL PASS` (deli/cove reproduce)
- `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python conformance_adjudication.py`
  → `ADJUDICATION-ENGINE CONFORMANCE: ALL PASS` (5 labels, C1–C5)

## The config-authorable boundary
`cfg["reconcile"]` is now `{"rule": "<name>", "params": {...}}` (the legacy flat shape
`{rule, threshold, support_floor}` is still accepted, so deli/cove configs are untouched). The rule
**name** and **every parameter** are config. The engine looks the name up in `eng.RULES`:

| config | controls |
|---|---|
| `cfg["reconcile"]["rule"]` | WHICH registered rule resolves the evidence (the config-authorable choice) |
| `params["threshold"]` / `params["support_floor"]` | the sufficiency / credibility floors (shared `_derive`) |
| rule-specific params (`kinds`, `as_of`, `half_life_days`) | e.g. which evidence kinds are admissible; the recency decay reference + half-life |

A **new rule** is: (1) add a pure function to the registry, (2) select it in config. The
**selection** is 100% config; the **body** of the rule (the pure support mapping) is a Python
function in the registry. That distinction is the honest core of this sprint and is stated plainly
under "What is still authored" below.

### The registry contract
```python
RULES = {
    "best-reliability-threshold":     _rule_best_rel,     # default semantics (Sprint-13, unchanged)
    "strict-anchor-only":             _rule_strict_anchor, # NEW: only ANCHORED evidence is admissible
    "recency-weighted-threshold":     _rule_recency,       # NEW: reliability × deterministic time decay
}
# signature: fn(ctx, params) -> {claim_support, disputed, conflict, determined, uncertainty}
# ctx = {"claims", "supporting": {claim_uri:[evidence...]}, "sub"}
```
Each rule computes a per-claim **support** strength; the shared `_derive` turns it into the uniform
dispute verdicts (`disputed` / `conflict` / `determined` / `uncertainty`) from the configured
`support_floor` + `threshold`. `best-reliability-threshold` is a verbatim copy of Sprint 13's logic,
so deli/cove are byte-for-byte reproducible (verified: two consecutive runs differ only in wall-clock
`now_iso()` fields).

## The three rules (all re-run of the IGN inspection dispute, only `reconcile` differs)
`inspect` — Vigilant Quality Assurance, a $54k goods-QC dispute. Claims: buyer `failed` ← resident
inspector TESTIMONY 0.90 (recent, 1d); company `passed` ← automated pass signal ANCHORED 0.84
(recent, 2d) + an independent audit RECORD 0.97 (**old, 52d**). Options/weights/factor-scores/
authority/§6 floor are IDENTICAL across all three runs — only the configured rule (and the label
suffix for clean fixtures) changes.

| rule (config) | `passed` | `failed` | conflict | uncertainty | **determination** |
|---|---|---|---|---|---|
| `best-reliability-threshold` (0.92/0.55) | DETERMINED (0.97) | DISPUTED (0.90) | yes | no | **rework-partial-credit** (CLOSED) |
| `strict-anchor-only` (kinds:[ANCHORED]) | DISPUTED (0.84) | **UNDETERMINED (0.0)** | no | yes | **UNRESOLVED** (OPEN) |
| `recency-weighted-threshold` (as_of 8/31, hl 21d) | DISPUTED (0.7863) | DISPUTED (0.871) | yes | yes | **UNRESOLVED** (OPEN) |

Real output assertions (`run_rule_comparison_demo.py` → ALL PASS):
- **A claim that was DISPUTED under one rule is UNDETERMINED under another** — `failed` is DISPUTED
  under best-rel (0.90) and recency (0.90) but UNDETERMINED under strict-anchor (0.0, testimony
  inadmissible); `passed` is DETERMINED under best-rel (0.97) but only DISPUTED under anchor/recency.
- **The rule choice changes the overall outcome** — `rework-partial-credit` (DETERMINED, CLOSED)
  vs **UNRESOLVED** (OPEN) under strict-anchor and recency. Zero engine code changed between runs;
  only `cfg["reconcile"]` (data) differed.
- **It is real, not a flag** — three DISTINCT rules run; per-claim support maps are pairwise
  distinct (0.97/0.90 vs 0.84/0.00 vs 0.7863/0.87); Trust unchanged (0.80) under every rule; the §6
  human keeps authority; every run is deterministic; every variant ends in a lawful terminal state
  (verified CLOSED/RESOLVED or honest OPEN/UNRESOLVED).
  - `best-reliability-threshold` and `recency-weighted-threshold` both reach UNRESOLVED and both
    report conflict — but for genuinely different reasons (recency decays the old 0.97 audit below
    CLEAR; nothing reaches the sufficiency threshold even though both claims are credibly debated).
    The per-claim support maps make that distinction visible.

## What is still authored (stated honestly — no perfection claimed)
1. **The reconciliation rule's body is a Python function in the registry.** The engine generalizes
   rule *selection* (fully config) and rule *parameters* (fully config), but the rule *mapping* — the
   pure function that turns evidence into a per-claim support number — is authored code, not a
   config-declared micro-DSL text. Adding a genuinely NEW combination shape (e.g. a Bayesian or a
   majority-of-sources rule) still means authoring that pure function once in `adjudication_engine.py`
   and registering it; it is then reusable across every org by config alone. This is the precise,
   honest boundary of "A — Yes": the "new-category" rule-authoring primitive is a *registry + pure
   functions* whose invocation is config-driven, not yet an end-user-authored textual DSL.
2. **The per-option factor scores + weights** remain the org's authored value judgment (§7K.1, by
   design) and the **determination** remains the §6 human's authoritative call (declared as the org's
   `determination_policy`). Neither changed.
3. **Rule-specific parameters** (e.g. `as_of`, `half_life_days`, `kinds`) are data but are written by
   whoever authors the org config — disclosed per rule, not inferred.

## §16 assessment — does the rule layer now argue **A — Yes**?
**Assessment: a clean "A — Yes" is still not honestly claimable — but the single largest remaining
hinge is now closed, and the boundary is precise.**

What closed: Sprint 13's stated residual ("a genuinely new evidence-combination rule needs a new rule
function; only the parameters of one rule are config") is no longer true. THREE distinct rule shapes
now run through the SAME engine, selected purely by `cfg["reconcile"]["rule"]`, with a real
determination-vs-UNRESOLVED flip from that choice alone. Rule selection is user-authorable; rule
parameters are user-authorable; a rule is reused across orgs by config.

Why it is still not an unqualified **A**: the new "category" claim rests on *authoring a new rule
without engine work at all*. Today that requires a one-time registry entry + a pure Python function —
the function BODY is not yet a config-declared/end-user-authored textual micro-DSL. So the honest
position is: **the rule layer is now config-authorable and demonstrably general (a big "<- A step"),
but the rule *mapping* is registry Python, not a user-authored micro-DSL** — "A — Yes" is argued for
*config-selected, registry-backed rule authoring*, and hangs on accepting that the pure-mapping body
is declared code rather than text. If an org wants an operator to write a rule entirely in config,
that DSL step is precisely what is specified (not faked) as the next work.

*(Evidence: all assertions above are real exit-0 output from `run_rule_comparison_demo.py`,
`run_adjudication_engine_demo.py`, and `conformance_adjudication.py` over 5 labels, plus a full
non-regression re-run of the Sprint-9/10/11/12 + reference + sector + agent suites — all ALL PASS;
SPEC v0.22, 49 `$defs`, `ros/` untouched.)*

---

### Update after Sprint 15 — the rule-BODY boundary addressed
Sprint 15 (`docs/USER-AUTHORABLE-RULE-DSL.md`) closes the exact seam this document named: the rule
BODY is now authorable as config TEXT. `cfg["reconcile"]["rule_spec"]` declares a rule declaratively
(admissible kinds × value field × optional decay × one fixed aggregation) and the engine *compiles*
it into the same pure support function the registry runs. Two existing rules re-expressed as specs
reproduce their registry verdicts exactly (parity — same engine); a genuinely NEW `majority-of-sources`
rule — never a registry function — is authored wholly as a spec dict and changes the `inspect`
verdict (UNRESOLVED vs best-rel's `rework-partial-credit`), with zero engine Python for it. The §16
stance updates to **A — Yes for declarative, config-text rule authoring over the shipped vocabulary**
(the remaining, disclosed seam is a rule needing an op outside `SPEC_VOCAB`, which requires adding
that one builtin to the language — then authorable as data by every org).