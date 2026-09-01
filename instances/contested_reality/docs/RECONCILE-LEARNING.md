# Reconcile Learning — RelationalOS (Sprint 17)

**Scope.** Sprint 13 shipped an OPTIONAL `decision_learning.py` (realized-cost *weight* learning)
that was never wired into the reconcile **RULE** choice. Sprint 17 wires decision learning into the
reconciliation layer itself: a deterministic, clamp-bounded, evidence-gated update of the reconcile
`threshold` from a RECORDED, realized outcome — feeding a NEW named `RULE_LIBRARY` entry that is
reused on a SECOND, distinct dispute and across a genuinely different org. It implements the §7K.1
loop `Decision → Expected → Actual → Variance → WHY → change-future-policy` at the reconciliation
boundary.

The trust-sensitive question is whether "learning" degrades into the machine moving its own
goalposts. It does not (proven by real assertions below). Everything is additive: frozen ontology
(49 `$defs`), URI cap, SPEC v0.22, `ros/` untouched, ~$0 deterministic local Python. Trust is only
ever moved by the deterministic S5 formula; the §6 human remains the sole determiner.

---

## Where it lives
```
instances/contested_reality/reconcile_learning.py         learning functions (new, additive)
instances/contested_reality/adjudication_configs.py       batch orgs + LEARN_HYPER (data)
instances/contested_reality/run_reconcile_learning_demo.py the runner; exit 0 = ALL PASS
instances/contested_reality/conformance_adjudication.py   16-label C1–C5 (13 prior + 3 new)
instances/contested_reality/docs/RECONCILE-LEARNING.md    this document
```
Verified commands (from `instances/contested_reality/`, all exit 0):
- `python3 run_reconcile_learning_demo.py` → `RESULT: ALL PASS`
- `/home/rlg/relational-os/archive/sprints/sprint-0/artifacts/.venv/bin/python conformance_adjudication.py`
  → `ADJUDICATION-ENGINE CONFORMANCE: ALL PASS` (16 labels, C1–C5, 49 `$defs`)
- Full non-regression (Sprint-16 set: rule_library / authoring / comparison / adj_engine, the 4 prior
  CR demos + conformances, sectors build_all + conformance_all, S5 reference + conformance, agent
  demo + conformance) → all exit 0.

## What is learned, and how it is contained + bounded
The learner recalibrates ONE reconcile parameter — the `threshold` (the sufficiency bar above which a
claim is DETERMINED) — from a recorded, realized outcome `v` of a completed prior dispute:

```
delta = learning_rate · (realized_value − prior_threshold)
new_threshold = clamp(prior_threshold + delta, lo, hi)
```
- If the realized value is BELOW the prior threshold — a determination actually held at support the
  bar demanded MORE of — the threshold was **too strong** (it risks UNRESOLVED on valid-but-
  moderately-evidenced disputes) → LOWER it toward the realized value.
- If the realized value EXCEEDS the bar, the bar was below what outcomes provided → RAISE it.
- `partial`: 0.80 → explicit `[lo, hi]`, `eps`-gated (`changed` only when `|delta| >= eps`),
  deterministic (depends only on explicit inputs, never the wall-clock), recompute-identical on
  re-run.

**It learns the RULE's parameter — not the answer to any case.** It does not re-derive hindsight on
the same dispute; the signal comes from a separately-recorded realized outcome, and the learned rule
is only ever applied to a SECOND, distinct dispute.

### Containment contract (all asserted as real exit-0 PASS)
1. **Trust untouched — S5 only.** Every org's seeded `trust://` stays 0.80; neither the engine nor
   the learner ever writes Trust (the S5 formula is the only mover).
2. **Human authority intact.** `determination_policy` is byte-identical before vs after the learning
   step (never edited by learning — it is the §6 human's authoritative call), and every determination
   decision still carries its configured `authority://` (§7J.9).
3. **Ledger append-only.** The learning steps APPEND one signed `event://{L}/reconcile-learning`
   carrying a NEW `rule://{L}/reconcile-rule` (kind=PROCEDURE) and a NEW
   `decision://{L}/reconcile-learning` (with `rules_applied` → the rule). Ledger events GROW and every
   PRIOR event is byte-identical — no rewrite, history intact, an auditor sees the layering.
4. **Explicit bound, not the wall-clock.** Rebound from explicit `[lo, hi]` + an explicit prior
   threshold; never unbounded.

These four are enforced by `run_reconcile_learning_demo.py` as real assertions, not prose.

## Learning feeds the RULE LIBRARY (the flow across ≥2 distinct disputes)
1. **Episode A** (`inspect-learn-a`, a batch-"alpha" goods-QC dispute) runs under the initial
   `best-reliability-threshold` at threshold **0.95** → it determines `rework-partial-credit`
   (winning-claim support 0.97). Its realized outcome value **0.90** is recorded additively (signed
   event): the 0.95 bar demanded more than the realization held → the threshold was too strong.
2. **Learning step:** `learn_threshold(prior=0.95, realized=0.90, lr=0.8, [0.55,0.95])` → **0.91**
   (changed=True; deterministic; clamp-bounded; evidence-gated). The learned rule is a NEW named
   `RULE_LIBRARY` spec `calibrated-threshold-091` (aggregate `max`, additive `learned_threshold` /
   `calibrated_from` / `bound` / `why`), appended as the signed `rule://` + `decision://` record.
3. **Episode B** (`inspect-learn-b`) — a genuinely SECOND, distinct dispute (batch beta, a different
   predicate set: its claim/evidence URIs are disjoint from A's, so this is NOT a re-run of the same
   case) — is driven once under the LEARNED rule (`rule_spec` = `RULE_LIBRARY["calibrated-threshold-091"]`,
   threshold 0.91). Its winning-claim support is **0.93**: the OLD 0.95 would leave it UNRESOLVED
   (`determined=[]`, uncertainty=True); the LEARNED 0.91 DETERMINES it
   (`rework-partial-credit`, CLOSED). **A real cross-dispute verdict flip, caused only by the learned
   threshold** (verified as a derived reconcile of the SAME evidence under the old rule, not a re-run).
4. **Cross-org reuse:** `deli-learn` (freight — a genuinely different org) reuses the SAME
   `RULE_LIBRARY["calibrated-threshold-091"]` dict by reference (`is`-identity) → it is a **library,
   not a one-case patch**.

The runner renders a §7L **Q7/Q8 cockpit line** per org naming the ACTIVE rule, its SOURCE
(registry / rule-library / learned-this-run), and whether a learning step changed it this run + the
evidence-gated WHY (`artifacts/adjudication/reports/cockpit-q7-q8-reconcile-learning.md`).

## The honest §16 verdict: **calibrated re-authoring, not autonomous learning**
The engine deterministically recalibrates ONE reconcile parameter (the threshold) from a realized
outcome — a **bounded, evidence-gated authoring action**, accurately named **calibrated
re-authoring**. It does NOT learn an open-ended answer, does not move Trust (S5 only), does not
change the §6 human's `determination_policy`, and appends rather than rewrites history. That is a
real and useful capability: the rule author (here a bounded calibrator acting on recorded outcomes)
updates a parameter from experience, and the updated rule is a reusable, library-shared, immutable-
ledger-recorded artifact. What it is NOT is the machine silently moving its own goalposts — the
containment contract above is asserted, not claimed.

*(Evidence: all assertions are real exit-0 output from `run_reconcile_learning_demo.py` and
`conformance_adjudication.py` (16 labels) plus the full non-regression suite — all ALL PASS; SPEC
v0.22, 49 `$defs`, `ros/` untouched, only catalog URI schemes in the new fixtures.)*

## Sprint 18 appendix — the Q7/Q8 line is now a FIRST-CLASS engine render (not a runner-side artifact)
Sprint 18 closes the gap the Sprint-17 summary flagged: the §7L Q7/Q8 cockpit line (ACTIVE reconcile
rule + its source + learned-or-not-this-run + the evidence-gated WHY) is no longer rendered only in
this runner's report — it is now `adjudication_engine.cockpit_q7q8(cfg, sub, *, library=None)` /
`render_cockpit_q7q8(...)`, a generic, data-only engine function ANY org renders identically by
reading its own config + ledger (no per-org Python). `run_cockpit_q7q8_demo.py` proves it drives 4
orgs across 3 rule-source classes (registry `deli`; rule-library `inspect-corroboration`; learned-this-
run `inspect-learn-b`; learned-reuse `deli-learn`) and THAT the engine-native line agrees with the
runner-report lines. **§16 verdict: first-class engine render** — the line now lives in the engine
itself; this `cockpit-q7-q8-reconcile-learning.md` file (and its Sprint-16 sibling) is a *view* over
that engine render, not the only place the Q7/Q8 surface exists. Full write-up:
`docs/ENGINE-Q7Q8-COCKPIT.md`.