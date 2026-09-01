# ENGINE-S7L-COCKPIT — the FULL §7L Q1–Q10 morning cockpit, rendered BY the generic engine (Sprint 19)

**Scope.** Sprints 13–18 built, in `adjudication_engine.py`, a configurable adjudication engine: a
config-authorable reconciliation RULE (registry → declarative `rule_spec` DSL), a cross-org
`RULE_LIBRARY` (with the `bayesian-combine` primitive), RULE learning, and then a **first-class
§7L Q7/Q8 cockpit line** inside the engine (`cockpit_q7q8`/`render_cockpit_q7q8` — ACTIVE rule +
source + learned-or-not + why). Up to Sprint 18 the rest of the §7L morning test
(Q1–Q6, Q9, Q10) was represented only in the **reference** sector cockpit
(`sprints/sprint-5/artifacts/reports/cockpit.md`, drawn by the operating layer `ros/bol.py`), not
in the generic adjudication engine. **Sprint 19 closes that**: `adjudication_engine.cockpit_s7l(cfg,
sub, *, library=None)` renders the **complete §7L Q1–Q10 cockpit** for ANY configured adjudication
org, data-only, with Q7/Q8 delegating to the Sprint-18 line by construction (strict superset).

This document states, per question, what the engine reports and the recorded-data evidence it answers
with; how it is generic + data-only; the ≥2-org proof (correctness + agreement + determinism +
no-fabrication); and the honest §16 verdict on the §7L gate ("#8 becomes authorized, verified, learned
work with the human owning the determination").

---

## 1. What the engine-native §7L Q1–Q10 cockpit reports, per org

Verified output of `run_cockpit_s7l_demo.py` (from `instances/contested_reality`), 4 orgs / 3 rule
sources, each as one identical engine call `cockpit_s7l(cfg, sub, library=...)`:

| org (rule source) | determination | Q5 root-cause (epistemic status + support) | Q10 verified + learning |
|---|---|---|---|
| `deli` (**registry**, best-reliability-threshold) | partial-settlement | `delivered` support 0.97 **DETERMINED**; `late` 0.90 / `shipped` 0.92 contested | verified=True; `evidence://deli/learning-note` |
| `inspect-corroboration` (**rule-library**, independent-corroboration) | rework-partial-credit | `passed` support 0.9961 **DETERMINED**; `failed` 0.931 contested | verified=True; learning-note |
| `inspect-learn-b` (**learned-this-run**, calibrated-threshold-091) | rework-partial-credit | `passed` support 0.93 **DETERMINED** under the learned rule; `failed` 0.88 contested | verified=True; learning-note + `decision://inspect-learn-b/reconcile-learning` |
| `deli-learn` (**learned, not this run**) | partial-settlement | `delivered` 0.97 + `shipped` 0.92 **DETERMINED**; `late` 0.90 contested | verified=True; learning-note |

Every org renders all ten questions. Abridged verbatim render for `inspect-learn-b`:

```
# §7L Q1–Q10 cockpit (engine-native) — org inspect-learn-b
ACTIVE reconcile rule: calibrated-threshold-091  |  source: learned  |  learned-this-run: True  |  why: reconcile threshold recalibrated ...
Q1. what happened?  state/events: 14 recorded events; dispute lifecycle OPEN->...->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=rework-partial-credit; claim epistemic={'passed': 'disputed', 'failed': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (1): claim://inspect-lb/failed — claim disputed (not DETERMINED)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: passed support=0.93 support-carrying (DETERMINED under the active rule); failed support=0.88 contested (not determined)  |  under rule calibrated-threshold-091 (learned)
Q6. what if we do nothing?  cannot forecast from recorded data (no recorded realized-vs-expected series)
Q7. what are our options?  accept-batch, reject-batch-return, rework-partial-credit, ... , unresolved  |  baseline unresolved  |  machine-eligible best: rework-partial-credit
Q8. what should we do?  recommendation rework-partial-credit (authority authority://inspect/adjudicate; floor-gated ['accept-batch', 'reject-batch-return'])  ->  determination rework-partial-credit
Q9. who does it, authority/capacity?  adjudicator person://inspect/adjudicator (authority authority://inspect/adjudicate), obligated party org://inspect/company, appeal authority://inspect/adjudicate-appeal, actors 7
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=rework-partial-credit; outcome=batch beta accepted ...; learning: evidence://inspect-learn-b/learning-note[...]; decision://inspect-learn-b/reconcile-learning[...]
```

## 2. What each question answers, and the recorded-data evidence behind it

| §7L Q | The engine reports (structured `q<N>` dict) | recorded-data evidence |
|---|---|---|
| **Q1 what happened?** | event count + event URIs in order; the recorded `lifecycle_state` walk; dispute `status`/`lifecycle`/`epistemic_state` | the org's own **append-only ledger** (`sub.ledger.entries`) + the `dispute://` object |
| **Q2 what changed?** | recorded deltas: lifecycle from→to, epistemic `UNDETERMINED -> …`, `determination`, per-claim `epistemic_status`, and a significance label (determined vs still-undetermined) | the recorded life-cycle walk + the claims' `epistemic_status` + reconcile verdict |
| **Q3 what matters?** | prioritized attention list = the recorded OPEN/UNRESOLVED dispute + every non-DETERMINED claim, each tagged with a reason | `dispute://` OPEN/UNRESOLVED state + reconcile `determined[]` vs the claims' `epistemic_status` (§7J.5 analogue) |
| **Q4 what is going wrong?** | the OPEN/UNRESOLVED dispute + the reconcile `conflict`/`uncertainty` verdicts as exceptions | recorded dispute state + `reconcile(...)` outcome (§7J.2 analogue) |
| **Q5 why, WITH epistemic status?** | per claim: `epistemic_status` (read from the graph) + `support`, tagged **support-carrying/DETERMINED** vs **contested/not-determined**, plus the active reconcile rule + its source | recorded `claim://*.epistemic_status` + per-claim `support` from the configured reconcile rule (§7K.2) |
| **Q6 what if we do nothing?** | a forecast **only if** a recorded realized-vs-expected **series** exists on the graph; otherwise *explicitly* `cannot forecast from recorded data (no recorded realized-vs-expected series)` | a real `metric://`-style `points`/`series` list; never the wall-clock, never an invented number |
| **Q7 what are our options?** | the resolution set incl. the do-nothing/UNRESOLVED baseline + machine-eligible best + trade-off | **delegated to the Sprint-18 `cockpit_q7q8` line by construction** (§7K.1) |
| **Q8 what should we do?** | recommendation with the authority it requires + the authorized determination | **delegated to the Sprint-18 line by construction** (§7J.9) |
| **Q9 who does it, authority/capacity?** | the §6 adjudicator holding the determination authority, the obligated party (the `dispute_about` obligation's `subject`), appeal authority, actor roster, and the capability statement | `cfg.authority` + the recorded `obligation://` the dispute is `about` (§7K.1/§7J.9) |
| **Q10 did it work, what did we learn?** | `verified`, `status`/`determination`, `resolution_outcome`, and the recorded **learning entries** | the `dispute://` `verified` flag + `evidence://<label>/learning-note.learning` + the optional `decision://<label>/reconcile-learning` from the org's ledger |

## 3. How it is generic and data-only

- **One engine function, no per-org Python.** `cockpit_s7l(cfg, sub, *, library=None)` reads
  everything from `cfg` (options, weights, reconcile, authority, claims, evidence, dispute,
  obligations) and the org's own `sub` graph/ledger; `library` is an optional plain dict of rule
  specs (data). The single code path serves a registry org, a rule-library org, and a learned-this-run
  org identically (proved on 4 orgs).
- **Strict superset of Sprint-18, not a rewrite.** Q7 and Q8 are the *same dict blocks* the
  Sprint-18 `cockpit_q7q8` returns (delegated by construction), and the ACTIVE-rule/source/
  learned-this-run/why surface is reused verbatim — so the engine's Q7/Q8 line is byte-identical
  whichever function drives it (asserted equal on every org).
- **Q5/Q10 come from the org's REAL graph/ledger, not authored literals.** `epistemic_status` is
  read off each recorded `claim://` object; `verified` is read off the `dispute://` object; the
  learning entries are real `evidence://<label>/learning-note` / `decision://<label>/reconcile-learning`
  objects on that org's ledger (asserted).
- **Q6 never fabricates.** A forecast is produced only when a recorded realized-vs-expected series
  exists; otherwise it says plainly it cannot forecast. The single realized-value recorded by the
  learning step is *not* a forecast series and is honestly reported as such (asserted on every org).
- **Deterministic.** Identical inputs → identical structured dict and rendered line (asserted on
  re-run for every org).

## 4. The ≥2-org proof (real, exit-0)

`run_cockpit_s7l_demo.py` (exit 0 = ALL PASS) drives 4 orgs across 3 rule sources and asserts:
(a) ALL TEN §7L questions are present, each with the required recorded-data evidence;
(b) Q7/Q8 of `cockpit_s7l` **equal** the Sprint-18 `cockpit_q7q8` line on the same org;
(c) deterministic (structured dict + rendered line identical on re-run);
(d) **agreement** with the Sprint-16 (`cockpit-q7-rule-library.md`), Sprint-17
(`cockpit-q7-q8-reconcile-learning.md`), and Sprint-18 (`cockpit-q7q8-engine.md`) report lines
where they overlap (inspect-corroboration rule+determination; inspect-learn-b/deli-learn
source+learned-or-not; deli registry baseline; per-org recommendation == Sprint-18 recommendation);
(e) Q5 epistemic status + Q10 verified/learning are read from the org's real graph/ledger;
(f) Q6 never fabricates a forecast.

The report `artifacts/adjudication/reports/cockpit-s7l-engine.{md,json}` captures the per-org render
+ the §16 verdict; fixtures are emitted for all four orgs.

## 5. Verification / non-regression (all exit 0)

- New runner: `python3 run_cockpit_s7l_demo.py` → **ALL PASS** (from `instances/contested_reality`).
- Existing demos re-verified ALL PASS: `run_cockpit_q7q8_demo`, `run_reconcile_learning_demo`,
  `run_rule_library_demo`, `run_rule_authoring_demo`, `run_rule_comparison_demo`,
  `run_adjudication_engine_demo`.
- Conformance: `conformance_adjudication.py` **16 labels** C1–C5 ALL PASS; the 4 prior CR conformances
  ALL PASS.
- Full non-regression: the 4 prior CR demos, sector `build_all.py` + `conformance_all.py`, S5
  reference demo + conformance, agent demo + conformance — ALL PASS. `deli`/`cove` **byte-identical
  up to the clock** (stripping the timestamp keys and diffing across two engine-demo runs — proved).
- Schema hash `7fc38c8c…`, **49 `$defs`**, **SPEC v0.22**, `ros/` untouched, only catalog URI
  schemes — no new noun.

## 6. Honest §16 verdict — is the §7L gate met?

**Yes at the engine-render level, with honest limits.** The engine (`adjudication_engine.cockpit_s7l` /
`render_cockpit_s7l`) now answers **all ten** §7L morning questions with recorded-data evidence for
ANY configured org, data-only. Q8's recommendation (`#8`) is machine-eligible-best, **§6-floor-gated**
(it never auto-picks a gated/irreversible option), carries the authority it requires (§7J.9), and the
authorized **determination is always the §6 human's `determination_policy` call**, which closes in a
**verified, learned outcome** (Q10 reads the recorded `verified` flag + the learning entries). The
engine reports the state; the runner/fixtures record it; the human owns the determination.

**Honest limits**, stated plainly:
- **Q6 cannot forecast on these orgs** — none records a realized-vs-expected series, so the cockpit
  faithfully says "cannot forecast from recorded data". Forecasting would require a metric series the
  adjudication orgs do not yet record (the reference sector cockpit forecasts because it records BI
  projections; the adjudication engine is honest when it does not).
- **Q9 "capability/capacity"** is rendered as the holder-of-authority assignment + the obligated
  party + the actor roster — not a dynamic capacity model. It answers *who* owns the determination
  and under *which* authority, which is the §7J.9/§7K.1 surface actually recorded.
- The cockpit reports the **recorded state** — it does not manufacture certainty where the evidence
  is genuinely UNRESOLVED (UNRESOLVED remains a legal, Trust-safe outcome; the §6 floor is never
  overruled). No authority over-claim: the machine recommends, the human determines, S5 alone moves
  Trust.

*(Evidence: all assertions are real exit-0 output from `run_cockpit_s7l_demo.py` and the full
non-regression + conformance suite; SPEC v0.22, 49 `$defs`, `ros/` + schema untouched, no new noun.)*

---

## 8. Update after Sprint 20 — Q6 forecast + Q9 capacity answered AS DATA where the data exists

Sprint 19's honest limits (§6 above) were the two "Residual seams" its own findings disclosed. **Sprint 20
closes a bounded slice of both, additively** (full write-up: `docs/ENGINE-FORECAST-CAPACITY.md`):

- **Q6 now projects deterministically from a RECORDED series.** An org that records a
  `metric://` realized-vs-expected series (`record_metric_series`) gets a real Q6 forecast:
  `forecast_metric(cfg, sub, metric_uri, *, horizon)` = last recorded `actual` + mean of recorded
  consecutive deltas, forward periods, **labelled a projection; never the wall-clock**. The Q6 row above
  ("a forecast only if a recorded series exists") is now *fired* for recorded-data orgs; the no-data
  fallback ("cannot forecast from recorded data") is unchanged.
- **Q9 now reports a recorded capacity number.** An additive `capacity` field
  (`record_capacity`, merge-not-replace, `{value, unit, load, status}`) on the `authority://` object the
  Q9 question reads gives `.q9.capacity` a number+unit (e.g. `1.0 obligations`); the no-field fallback is
  unchanged.
- **Proof on ≥2 orgs** (`run_forecast_capacity_demo.py`, exit 0 = ALL PASS): `deli-forecast` (records
  both) forecasts Q6 `[0.84, 0.82, 0.8]` + reports capacity `1.0 obligations`; `deli` (no data) keeps the
  honest fallback. Both render the full §7L Q1–Q10; both deterministic + agreeing with the recorded graph;
  the new org's fixtures pass Sprint-0 C1–C5.
- **§16 verdict (updated):** the §7L morning cockpit is now data-grounded on every one of the ten
  questions **WHERE the data exists** — Q6 projects only from a recorded series and Q9 reports only a
  recorded capacity, never a fabricated number; a no-data org plainly says it cannot forecast / has no
  recorded capacity. Q7/Q8 stay the Sprint-18 line; #8 stays §6-floor-gated; the determination stays the
  §6 human's call; S5 alone moves Trust. Additive; 49 `$defs` / SPEC v0.22; `metric://` a first-class noun,
  `capacity` an additive field (no `capacity://`); `ros/` untouched.