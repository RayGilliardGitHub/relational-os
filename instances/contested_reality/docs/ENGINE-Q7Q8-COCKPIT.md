# ENGINE-Q7Q8-COCKPIT — the §7L Q7/Q8 cockpit line, FIRST-CLASS in the generic engine (Sprint 18)

**Scope.** Sprints 15–17 made the evidence-reconciliation RULE authorable (`rule_spec`), a named
cross-org RULE LIBRARY (with the `bayesian-combine` primitive), and learnable (a deterministic,
clamp-bounded, evidence-gated recalibration of the reconcile `threshold` feeding a new library entry).
In Sprints 16 and 17 the ACTIVE rule + its spec-authored-vs-registry / learned-or-not source + the
evidence-gated reason were rendered in **runner-side reports** (`cockpit-q7-rule-library.md`,
`cockpit-q7-q8-reconcile-learning.md`) — but were never wired into the generic engine's OWN §7L
cockpit output. **Sprint 18 closes that**: the ACTIVE reconcile rule + its source + whether a learning
step changed it this run + the why are a **first-class §7L Q7/Q8 line inside `adjudication_engine.py`**,
so ANY org's generically-rendered cockpit carries it — not just the cluster of runner reports.

This document states what the engine-native line reports, how it is generic + data-only, how it was
proved correct (≥2 orgs, 3 rule-source classes, agreement with the Sprint-16/17 runner lines), and the
honest §16 verdict.

---

## 1. What the engine-native Q7/Q8 line reports, per org

`adjudication_engine.cockpit_q7q8(cfg, sub, *, library=None)` returns a structured dict; the
verified Sprint-18 output (from `run_cockpit_q7q8_demo.py`) per driven org:

| org | ACTIVE rule | source | learned-this-run | why |
|---|---|---|---|---|
| `deli` (freight) | `best-reliability-threshold` | **registry** | False | unchanged (no learning step on this org) |
| `inspect-corroboration` (goods-QC) | `independent-corroboration` | **rule-library** | False | unchanged |
| `inspect-learn-b` (batch beta, driven under the LEARNED rule) | `calibrated-threshold-091` | **learned** | **True** | `reconcile threshold recalibrated lowered (relaxed: the bar demanded more than realized determinations held): prior 0.950 -> 0.910 from a realized outcome value 0.900 ...` |
| `deli-learn` (cross-org reuse of the SAME learned spec) | `calibrated-threshold-091` | **learned** | False | unchanged (reuses a learned rule; no learning step ran on this org this run) |

Each also carries §7L **Q7 (what are our options?)** — the resolution set incl. the do-nothing /
UNRESOLVED baseline + the machine-eligible best — and **Q8 (what should we do?)** — the recommendation
with the authority it requires, plus the §6 human's authorized determination, all read off the org's
own config + ledger.

### The rendered line (`render_cockpit_q7q8`), verbatim for `inspect-learn-b`
```
# §7L Q7/Q8 cockpit (engine-native) — org inspect-learn-b
Q7 options: accept-batch, reject-batch-return, rework-partial-credit, conditional-accept-with-guarantee, request-more-evidence, escalate, unresolved  |  baseline: unresolved  |  machine-eligible best: rework-partial-credit
Q8 recommendation: rework-partial-credit (authority authority://inspect/adjudicate; floor-gated: ['accept-batch', 'reject-batch-return'])  ->  determination: rework-partial-credit
ACTIVE reconcile rule: calibrated-threshold-091  |  source: learned  |  learned-this-run: True
why: reconcile threshold recalibrated lowered (relaxed: the bar demanded more than realized determinations held): prior 0.950 -> 0.910 from a realized outcome value 0.900 (variance signal -0.040, learning_rate 0.8), clamp-bounded to [0.55, 0.95]
```

## 2. How it is generic and data-only

- **One engine function, no per-org Python.** `cockpit_q7q8(cfg, sub, *, library=None)` is a single,
  org-agnostic function. It reads everything from `cfg` (the org's config: `reconcile`, `options`,
  `authority`) and the org's own `sub` graph/ledger. `library`, when given, is a plain dict of named
  rule specs (`ac.RULE_LIBRARY`) used to classify a non-learned spec as `rule-library` — data, not code.
  The single code path renders a registry org, a library org, and a learned-this-run org identically
  (the runner proves all three from ONE engine call).
- **Source classification is read from what actually ran, not a runner side-table.** The class is
  derived from `cfg["reconcile"]`: a `rule` name that is an engine `RULES` function → `registry`; a
  `rule_spec` carrying the Sprint-17 additive learned fields (`learned_param`/`learned_threshold`) →
  `learned`; a `rule_spec` matching a provided library entry (by `is`-identity or `name`) → `rule-library`;
  anything else → `rule-spec-authored`. **No new engine branch is written per org.**
- **learned-this-run is data-derived from the org's OWN ledger.** An org reports `learned-this-run=True`
  only when its active rule is `learned` AND its ledger actually contains a `decision://<label>/reconcile-learning`
  recorded this run. That is why `inspect-learn-b` (whose reconcile-learning decision we record on its
  OWN ledger) reports True, while `deli-learn` (reuses the same learned spec but records no learning on
  its own ledger) reports False — the exact Sprint-17 semantics, now reconstructed from the org's
  source of truth instead of a hard-coded runner table.
- **The why is the evidence-gated reason.** For learned-this-run it is read off that
  `decision://<label>/reconcile-learning` object's `detail.why` (the clamp-bounded recalibration reason);
  otherwise it is `"unchanged"`. Deterministic: identical inputs → identical dict and rendered line
  (asserted on every driven org).

## 3. The ≥2-org proof (real, exit-0)

`run_cockpit_q7q8_demo.py` drives **4 orgs across 3 rule-source classes** and asserts, per org:
(a) the ACTIVE rule name matches the org's `cfg["reconcile"]`; (b) the SOURCE is classified correctly
(registry / rule-library / learned-this-run); (c) both §7L Q7 and Q8 are present (options incl. the
do-nothing baseline; recommendation with authority + determination); (d) deterministic on re-run.

**Agreement with the Sprint-16/17 runner lines** (asserted against the freshly regenerated report files):
- `inspect-corroboration`: engine `active_rule=independent-corroboration`,
  `determination=rework-partial-credit` — matches `cockpit-q7-rule-library.md`.
- `inspect-learn-b`: engine `source=learned, learned-this-run=True, rule=calibrated-threshold-091` —
  matches `cockpit-q7-q8-reconcile-learning.md`.
- `deli-learn`: engine `source=learned, learned-this-run=False` — matches the Sprint-17 reuse line.
- `deli`: engine `source=registry, rule=best-reliability-threshold` — the registry baseline.

**Generic and data-only:** all four orgs are pure config data + one identical engine call
`cockpit_q7q8(cfg, sub, library=...)`; no per-org Python exists in the engine.

## 4. Verification / non-regression (all exit 0)

- New runner: `python3 run_cockpit_q7q8_demo.py` → **ALL PASS** (from `instances/contested_reality`).
- Existing demos re-verified ALL PASS (engine change is purely additive): `run_reconcile_learning_demo`,
  `run_rule_library_demo`, `run_rule_authoring_demo`, `run_rule_comparison_demo`,
  `run_adjudication_engine_demo`.
- Conformance: `conformance_adjudication.py` **16 labels** C1–C5 ALL PASS (covers the Sprint-18-driven
  fixtures `deli`, `inspect-corroboration`, `inspect-learn-b`, `deli-learn`); the 4 prior CR conformances
  ALL PASS.
- Full non-regression: the 4 prior CR demos, sector `build_all.py` + `conformance_all.py`, S5 reference
  demo + conformance, agent demo + conformance — ALL PASS. `deli`/`cove` **byte-identical up to the clock**
  (proved by stripping the timestamp keys and diffing across two runs).
- Schema hash `7fc38c8c…`, **49 `$defs`**, **SPEC v0.22**, `ros/` untouched, only catalog URI schemes
  (incl. the frozen `rule://`/`decision://`) — no new noun.

## 5. Honest §16 verdict

**First-class engine render, not a runner-side artifact.** The §7L Q7/Q8 line (ACTIVE rule +
source + learned-or-not this run + the evidence-gated why) is now `adjudication_engine.cockpit_q7q8` /
`render_cockpit_q7q8` — a generic, data-only function that ANY configured org renders identically,
reading the org's own config and ledger. The engine now surfaces the reconcile rule as **first-class
operating reality** (Q7 options + Q8 recommendation with authority), exactly as §7L Q7/Q8 and §7J.9
(the cockpit) intend. The Sprint-16/17 cockpit-report files are now a *view* over that engine render,
not the only place the line exists — this is the honest, non-hyperbolic statement of where the surface
lives. It does NOT over-claim authority: the "what should we do" recommendation is machine-eligible-best
(§6-floor-gated, never a determination), and the authorized determination remains the §6 human's
`determination_policy` call — the engine reports it, the runner/fixtures record it, the human owns it.

*(Evidence: all assertions are real exit-0 output from `run_cockpit_q7q8_demo.py` and the full
non-regression + conformance suite; SPEC v0.22, 49 `$defs`, `ros/` untouched, no new noun.)*

---

## Update after Sprint 19 — the Q7/Q8 line is now part of the FULL §7L Q1–Q10 cockpit

Sprint 19 extends the same data-only discipline to the whole §7L morning test. 
`adjudication_engine.cockpit_s7l(cfg, sub, *, library=None)` / `render_cockpit_s7l(...)` render the
**complete Q1–Q10 cockpit** for ANY configured org, with **Q7/Q8 delegating to the Sprint-18
`cockpit_q7q8` line BY CONSTRUCTION** (the same dict blocks — strict superset, not a re-derivation).
So the line documented above is unchanged and remains the authoritative Q7/Q8 render; it is now
*also* carried inside the full 10-question cockpit, and the runner asserts that on every org
`cockpit_s7l`'s `q7`/`q8`, `active_rule`, `source`, `learned_this_run`, `why`, and `determination`
are **equal** to the Sprint-18 `cockpit_q7q8` output on the same org. See
`docs/ENGINE-S7L-COCKPIT.md` for the full §7L Q1–Q10 cockpit, its per-question evidence, the ≥2-org
proof (exit-0 `run_cockpit_s7l_demo.py`), and the honest §16 verdict on the §7L gate.