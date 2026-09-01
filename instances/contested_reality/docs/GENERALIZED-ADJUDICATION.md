# Generalized Adjudication Engine — RelationalOS SPECENDIX (Sprint 13)

**Scope.** Sprint 12's honest verdict was **B — Partially**: RelationalOS could *run* the
contested-reality lifecycle, but "the adjudication semantics are expressed as documented additive
fields over a generic envelope rather than a configurable dispute-DSL" — a different org's dispute
still needed re-coding. Sprint 13 makes adjudication a **general, configurable capability** and
renders it on the §7L cockpit question 7. Everything below maps to real, exit-0 output.

**Design constraint honored throughout:** additive only, frozen ontology (49 `$defs`), URI cap,
SPEC v0.22, `ros/` untouched, ~$0 deterministic local Python. The engine is **not** a new service
or a new URI noun.

---

## Where it lives
```
instances/contested_reality/adjudication_engine.py     the GENERIC engine (zero per-scenario code)
instances/contested_reality/adjudication_configs.py    two org scenarios as pure DATA (deli, cove)
instances/contested_reality/run_adjudication_engine_demo.py  runs both, asserts ALL PASS
instances/contested_reality/conformance_adjudication.py      C1–C5 over both fixtures (venv)
instances/contested_reality/decision_learning.py            optional realized-cost weight learning
instances/contested_reality/docs/GENERALIZED-ADJUDICATION.md this document
```
Verified commands (from `instances/contested_reality/`, exit 0):
- `python3 run_adjudication_engine_demo.py` → `RESULT: ALL PASS`
- `/home/rlg/relational-os/archive/sprints/sprint-0/artifacts/.venv/bin/python conformance_adjudication.py`
  → `ADJUDICATION-ENGINE CONFORMANCE: ALL PASS`

---

## What became CONFIGURABLE (data, not code)
The engine reads an adjudication `cfg` entirely as data and runs the same lifecycle for any org
configured for it. Authoring a third org = adding a `configs.py` dict entry; **no engine change**:

| config key | what it controls | org A (deli) | org B (cove) |
|---|---|---|---|
| `claims` / `evidence` | the ≥2 conflicting claims + their recorded evidence (provenance, reliability, `supports`) | delivery timestamps | clinical necessity vs formulary |
| `options` | the resolution option set (must include an unresolved/do-nothing baseline) | 8 incl. unresolved | 8 incl. unresolved |
| `weights` (Σ=1.0) | **the business model** — "what 'better' means" (§7K.1) | evidence .35 contractual .30 relationship .20 cost .15 | medical_necessity .40 safety .25 policy .20 cost .15 |
| `factor_scores[opt][factor]` | each option's modeled value per factor — the org's value judgment, disclosed as data | table | table |
| `floor_gated` + `floor_penalty` | the §6 irreversible/unknown-cost gate | {accept-customer-refund} | {authorize-off-formulary, deny-off-formulary} |
| `reconcile` (rule + `threshold` + `support_floor`) | the evidence-reconciliation rule (deterministic, named) | 0.95 / 0.55 | 0.90 / 0.55 |
| `authority` | adjudicator + appeal (§7J.9) | manager / director | utilization / medical director |
| `determination_policy` | the authoritative human call: adopt-eligible-best / override / unresolved | adopt-eligible-best | adopt-eligible-best |
| `unresolvable` | a thin-evidence sub-dispute that must end UNRESOLVED | yes | yes |
| `learning_model` | optional realized-cost weight learning (rate, clamps, realized cost/outcome) | enabled | enabled |

The **lifecycle is identical and generic** for every config: provision → claims → evidence →
reconcile → dispute OPEN (additive lifecycle + epistemic state) → options ranked
(utility = Σ_factor weight·score − floor_penalty if gated) → §6 machine-eligible best (top
NON-gated; unresolved baseline never gated → no forced winner) → advisory `decision://` (contained:
no `trust://` write), → authorized human determination → verified outcome → learning. Plus, on every
config, the UNRESOLVED branch when no claim reaches the configured sufficiency `threshold`.

### The reconciliation rule (the one named deterministic semantic)
`best-reliability-threshold`: a claim's support = max reliability of its supporting evidence refs
(missing → 0). A claim is DISPUTED when support ≥ `support_floor`; CONFLICT is detected when ≥2
rival claims are both disputed; UNCERTAINTY holds while no claim's support ≥ `threshold` (the
single-source verifier cannot reach CLEAR) → that dispute is **UNRESOLVED**. This mirrors Sprint 12's
finding.
Rule parameters come from config, so a different sufficiency standard is a different org's data.
"The reconciliation is per-scenario authored code" is no longer true — only its parameters are per-org.

## The two org scenarios, from the SAME engine (real output, no code change between them)
**A. `deli` — Constellar Freight, $18k delivery dispute** (customer "late" vs company "delivered"
vs supplier "shipped"; receipt 0.9, GPS 0.85, anchored verification 0.97, supplier log 0.92).
Ranking (weights evidence .35 / contractual .30 / relationship .20 / cost .15):
```
0.728 partial-settlement         0.435 request-more-evidence
0.665 conditional-resolution     0.400 unresolved (baseline)
0.620 accept-company-full-payment 0.385 external-adjudication
                                 0.380 escalate
0.285 accept-customer-refund  [FLOOR-GATED]
```
Determination: **partial-settlement** (machine-eligible best, adopted by the adjudicator). The
thin-evidence sub-dispute → **UNRESOLVED** (no source ≥ 0.95).

**B. `cove` — Meridian Health Plan, clinical coverage dispute** (physician "medically necessary" vs
payer "off-formulary"; trial 0.88, formulary policy 1.0, step-therapy meta-analysis 0.82). Ranking
(weights medical_necessity .40 / safety .25 / policy .20 / cost .15):
```
0.777 step-therapy-first           0.540 request-more-evidence
0.740 authorize-generic           0.500 unresolved (baseline)
0.605 escalate-to-medical-director
0.560 external-peer-review         0.480 authorize-off-formulary   [FLOOR-GATED]
                                  0.280 deny-off-formulary        [FLOOR-GATED]
```
Determination: **step-therapy-first** (both extreme spend/denial paths are §6-floor-gated; the
measured option is machine-eligible best). Rare-condition sub-dispute → **UNRESOLVED**.

Cross-scenario (asserted at run time): the SAME engine drives both; distinct business models and
distinct determinations; rankings deterministic on re-run; Trust untouched (score preserved; never
authored); authority preserved on every `decision://`.

## §7L cockpit Q7 (optional item, done)
`artifacts/adjudication/reports/cockpit-q7.md` (+ `.json`, + per-label `cockpit-q7-{deli,cove}.*`)
render **"7. WHAT ARE OUR OPTIONS?"** for a configured episode — weights, ranked options, §6-gated set,
machine-eligible best, do-nothing/UNRESOLVED baseline, the needed authority (#8), and the human
determination. Additive report on the existing cockpit/report path; `sector_scene.py` untouched.

## Decision-Learning / realized-cost weights (optional item, done)
`decision_learning.py` records `realized_cost_usd`, `outcome_value`, `expected_utility`, `variance`,
and `learned_weights` **additively** on the chosen `decision://` and the dispute, and deterministically
re-weights the business model from expected-vs-actual variance (clamp-bounded to [lo,hi], renormalized
to Σ=1.0) — the objective is learned over time, not just the ranking. Real output, both orgs:
- deli: expected 0.728 realized 0.55 → variance +0.177, realized cost $6,000,
  weights → evidence .347 contractual .300 relationship .202 cost .150.
- cove: expected 0.777 realized 0.70 → variance +0.078, realized cost $18,000,
  weights → medical_necessity .399 safety .250 policy .200 cost .150.
The engine never writes Trust; the weight update is the deterministic S5/S4-external *organizational
learning* step, not a Trust mutation.

---

## What is STILL authored (stated honestly — no perfection claimed)
1. **The per-option factor scores** (`factor_scores`) are the org's modeled *value judgment* — which
   option is good for which outcome. They are now **data** (config), not code, but they remain an
   authored business choice, exactly as §7K.1 says: *"the optimizer needs to know what 'better' means
   before it can optimize . . . the value system is authored."* The engine computes the ranking; it
   does not derive desirability from first principles.
2. **The determination itself** is the §6 *human adjudicator's* authoritative call (declared as the
   org's `determination_policy` + optional explicit `determination`). The engine never manufactures a
   determination — consistent with §6 and §7J.9. "Adopt-eligible-best" is itself a config choice; a
   different org may declare "override" to an explicit option or "unresolved".
3. **The reconciliation rule *name*** (`best-reliability-threshold`) is the one implemented semantic;
   its parameters are config, but a genuinely new rule type would still require adding a rule
   function. (Parameterizing the rule — the largest remaining code surface — is the candidate next
   step; see Sprint 14 prompt.)
4. **The lifecycle state names** (OPEN → … → CLOSED) are emitted as the proven Sprint-12 legal walk,
   not yet a separate config declaration.

## §16 verdict — did the "new category" assessment move?

**Assessment: now argued "B-plus — materially toward A," still not an unqualified "A — Yes".**

What moved it:
- **Adjudication is now general and configurable** — the exact capability §16 named as the missing
  differentiator ("the adjudication semantics must become a general, configurable capability rather
  than a per-scenario authored model"). Two different org disputes (different weights, options,
  evidence reconciliation parameters, floor gates, authorities) run through ONE engine with zero
  code change, both conformance-green on the frozen 49 `$defs`.
- **The whole loop is rendered on the §7L cockpit Q7** — the second thing §16 said was missing: "the
  loop must render onto the §7L cockpit so a Fed-org executive hands the 'what are our options and
  what should we do' question to it daily."
- Combined with earlier Demonstrable assets (truthful UNRESOLVED, error-vs-deception Trust,
  immutable auditor-reconstructable ledger, human-only determination), the "organizational
  accountability under contested reality" claim is now operationally general, not per-scenario.

Why it is still not a clean **A** (the residual hinges, stated plainly):
- The **value model itself (factor scores + weights) is and must remain authored** organizational
  judgment — that is a *feature* of §7K.1, not a defect, but it means RelationalOS explains and
  optimizes against a stated objective rather than conjuring one. "New category" as *offering a new
  primitive the incumbents lack* is earned by the relationship-and-disagreement ontology + truthful
  UNRESOLVED; generalizing the *semantics* is now proven, but the semantics are still
  parameter-driven rather than a full user-authored dispute DSL.
- Reconciling truly **novel** evidence-combination shapes still needs a new rule function (only the
  parameters of one rule are config today).

**Bottom line:** the honest verdict moves from **B — Partially** toward **B+ — Partially, now
generically** — the differentiating claim (adjudication as a configurable capability, rendered on the
daily cockpit) is no longer "next work, not a finished fact": it is demonstrably built. Claiming a
clean **A** would require a user-authorable dispute DSL (rule authoring over arbitrary evidence
combinations) — the natural Sprint-14 step — and is stated as such rather than faked.

*(Evidence: all assertions above are real exit-0 output from `run_adjudication_engine_demo.py`,
`conformance_adjudication.py`, and the re-run of the whole Sprint-9/10/11/12 + reference + sector +
agent suites — all ALL PASS.)*

---

## Sprint 14 — update: the reconciliation rule is now config-authorable (residual hinge #3 closed)

The §16 residual "a genuinely new evidence-combination rule needs a new rule function (only the
parameters of one rule are config today)" is no longer true after Sprint 14. `reconcile` is now a
deterministic rule registry (`eng.RULES`) in `adjudication_engine.py`; `cfg["reconcile"]` is
`{rule, params}` and the rule **selection** + every **parameter** are config. Three distinct rules
(`best-reliability-threshold`, `strict-anchor-only`, `recency-weighted-threshold`) run through the
SAME engine, and one org (`inspect`, $54k goods-QC) flips from a DETERMINED `rework-partial-credit`
under best-rel to **UNRESOLVED** under strict-anchor and recency purely by the configured rule — zero
engine change. deli/cove reproduce byte-for-byte under their original rule.

**Honest §16 boundary now:** the rule *selection* and *parameters* are user-authorable config; the
rule's pure support-*mapping body* is still registry Python (a new combination shape needs a one-time
pure function + a registry entry, reusable by config thereafter). So the verdict argues **"A — Yes for
config-selected, registry-backed rule authoring"** and still stops short of claiming a fully
end-user-authored textual dispute micro-DSL (the rule BODY is not yet config text). Specified plainly,
not faked, in `docs/USER-AUTHORABLE-RULE-LAYER.md`.