# ENGINE-S7L-COCKPIT — the FULL §7L Q1–Q10 morning cockpit, rendered BY the generic engine (Sprint 19)

**Scope.** Sprints 13–18 built, in `adjudication_engine.py`, a configurable adjudication engine: a
config-authorable reconciliation RULE (registry → declarative `rule_spec` DSL), a cross-org
`RULE_LIBRARY` (with the `bayesian-combine` primitive), RULE learning, and then a **first-class
§7L Q7/Q8 cockpit line** inside the engine (`cockpit_q7q8`/`render_cockpit_q7q8` — ACTIVE rule +
source + learned-or-not + why). Up to Sprint 18 the rest of the §7L morning test
(Q1–Q6, Q9, Q10) was represented only in the **reference** sector cockpit
(`archive/sprints/sprint-5/artifacts/reports/cockpit.md`, drawn by the operating layer `ros/bol.py`), not
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
## 9. Update after Sprint 27 — Q7/Q8 carry a recorded-capacity CONSTRAINT (a label, never an overrule)

Sprint 26's finding that the Q9 capacity REASON did not reach the trade-off is closed additively in
`cockpit_s7l`: where the org records a numeric `capacity` AND a band + numeric threshold exist, **both
`q7` and `q8` carry an additive `capacity_constraint` block** (a PARALLEL block — the frozen
`rank`-owned `options`/`tradeoff` and the Sprint-18 `cockpit_q7q8` bytes are untouched):

- `recorded_capacity` (value/unit/load AS RECORDED), `horizon_band` ({low,high} = the closure's
  `band_horizon`), `reason`, `flag`, `options_flagged`, `note`.
- `reason` is ONE deterministic label from recorded numbers only via the shared `_capacity_reason`
  helper (headroom / at-capacity when recorded load >= 1.0 / deficit when the horizon band's worst-side
  magnitude reaches/exceeds the recorded capacity value) — so Q8's `reason` always equals the Q9
  `capacity_planning_attention` label BY CONSTRUCTION. In headroom no option is flagged; at
  at-capacity/deficit the capacity-consuming (non-baseline) options are marked `capacity_risk` — never
  `capacity_infeasible` (no per-option requirement is ever recorded).
- It NEVER removes an option, NEVER changes `machine_eligible_best`/the Q8 recommendation, NEVER
  overrules the §6 human. A no-capacity / no-band / no-data org carries NO `capacity_constraint` key
  (byte-identical superset of Sprint 26). For every org Q7 `options` + Q8
  `recommendation`/`machine_eligible_best` are asserted EQUAL to `cockpit_q7q8`
  (`run_forecast_horizon3_demo.py`, exit 0 = ALL PASS: e.g. `deli-varmax-cap` carrying
  `{reason: "headroom", options_flagged: {}}` — the recorded capacity 500.0 ≫ horizon 0.62…1.02, load
  0.72) while the no-capacity orgs are unchanged. Additive; no new noun; 49 `$defs` / SPEC v0.22.
  `capacity` an additive field (no `capacity://`); `ros/` untouched.

## 10. Update after Sprint 28 — the capacity marker is PROVEN AT ITS LIMIT (at-capacity / deficit)

Sprint 27 proved `capacity_constraint` end-to-end only in **headroom**; its at-capacity / deficit
branches were helper-only. **Sprint 28 (recorded data + a runner, NO engine change)** drives the
non-headroom branches AS DATA on a real §7L Q1–Q10 cockpit, so the whole `capacity_constraint` block
is now demonstrated at every derived reason:

- **`deli-atcap`** (NEW): recorded load **1.25** (>= 1.0) with capacity 500.0 resolutions/day, same
  horizon band as `deli-varmax` `{0.62, 1.02}` → `reason: "at-capacity"`, `flag: True`.
- **`deli-deficit`** (NEW): **lower-is-better** latency series (horizon `{12.0, 32.0}`, sigma 8) +
  recorded capacity VALUE **30.0** (load 0.9) → horizon worst-side high **32.0 >= 30.0** →
  `reason: "deficit"`, `flag: True`.

At BOTH, `options_flagged` marks EVERY capacity-consuming NON-baseline option `capacity_risk` and NEVER
the baseline (`unresolved`); the reason equals the org's Q9 `capacity_planning_attention` **BY
CONSTRUCTION**. **The marker is a LABEL at its limit:** the Q7 `options` (count + uris) +
`machine_eligible_best` + Q8 `recommendation`/`floor_gated` EXACTLY equal `cockpit_q7q8` for EVERY org
(incl. the at-capacity/deficit ones) — the Q8 `partial-settlement` recommendation provably unchanged.
The Sprint-27 headroom + all no-capacity/no-band/no-data orgs are byte-identical. Proof: the §9
`run_forecast_horizon3_demo.py` plus the new `run_forecast_horizon4_demo.py` (exit 0 = ALL PASS, ≥7
orgs). SPEC v0.22, 49 `$defs`, `ros/` untouched, no new noun.

## 11. Update after Sprint 29 — the Q7/Q8 `capacity_constraint` can now label a SPECIFIC option `capacity_infeasible` (from a RECORDED per-option requirement)

Sprint 28's honest frontier (`archive/sprints/sprint-28/notes/findings.md`, "Open issues / next work"):
`capacity_infeasible` was **structurally unreachable** because no per-option capacity requirement was
ever recorded — the engine could flag a whole `capacity_risk` set but never name the particular option
the recorded capacity cannot run. **Sprint 29 makes the recorded capacity PER-OPTION** so the marker
labels a specific option:

- A new REPLAYABLE recorder `record_capacity_requirements(sub, authority_uri, requirements, signer)`
  records an additive `capacity_requirements` map on the SAME `authority://` object as the additive
  `capacity` — so `available = capacity.value − capacity.load` is unit-coupled by construction.
- In `cockpit_s7l`'s Q7/Q8 `capacity_constraint` block, when requirements are recorded, the additive
  `_per_option_capacity_flags` rule labels each option: `capacity_infeasible` iff its RECORDED
  requirement > available; otherwise `capacity_risk` (non-headroom). The block also surfaces the
  recorded `per_option_requirements` map + `available_capacity`. A no-requirements org keeps the
  Sprint-28 block byte-identical (no per-option keys). `reason`/`flag` still come from the org-level
  `_capacity_reason`; the baseline is never flagged; frozen functions untouched.

Real proof (`run_forecast_per_option_capacity_demo.py`, exit 0 = 88 PASS): the five Sprint-28 orgs are
byte-identical; two NEW orgs RECORD per-option requirements:
- `deli-infcap` (at-capacity, cap 500.0 res/day load 1.3 → available 498.7): heavy options record
  499.0 (> 498.7) → `capacity_infeasible`; lighter options ≤ available → `capacity_risk`.
- `deli-deficit-inf` (deficit, cap 30.0 load 0.9 → available 29.1): heavy options record 30.0 (> 29.1)
  → `capacity_infeasible`; lighter → `capacity_risk`.

On both, `options_flagged` = 3 `capacity_infeasible` + 4 `capacity_risk` (baseline never flagged),
every label traces to a recorded requirement vs available, and the Q7 options + Q8 recommendation are
still EXACTLY the frozen `cockpit_q7q8` output (`partial-settlement`) even though SOME option is
infeasible — the marker is still a LABEL, never a re-rank, never a removal, never an overrule of the
the §6 human. Both new orgs' fixtures pass Sprint-0 C1–C5; full non-regression green; SPEC v0.22, 49
`$defs`, `ros/` untouched.

## 12. Update after Sprint 30 — the marker is a REASON, never a CHOICE: the RECOMMENDED option itself made `capacity_infeasible`

Sprint 29's honest boundary (see `archive/sprints/sprint-29/notes/findings.md`): the per-option marker can NAME
a specific infeasible option, but it **never CHOOSES a different option for the machine — the §6 human
always does.** Sprint 30 drives the SHARPEST version of that boundary, with NO engine change: a new org
`deli-recommend-infcap` (`run_forecast_label_vs_choice_demo.py`, exit 0 = ALL PASS) RECORDS a per-option
requirement that makes the machine-eligible best / Q8 recommendation ITSELF (`partial-settlement`)
`capacity_infeasible`:

- recorded capacity 500.0 res/day, load 1.3 → available **498.7** (at-capacity, `reason` unchanged);
- `partial-settlement` RECORDS **499.0** (> 498.7) → **`capacity_infeasible` ON THE RECOMMENDED OPTION**;
- the other 6 non-baseline options → `capacity_risk`; the `unresolved` baseline (no recorded requirement)
  → never flagged.

The Q8 recommendation **provably STAYS `partial-settlement`** (and machine-eligible best the same),
exactly `cockpit_q7q8` — no re-rank, no removal, no §6 overrule. The `capacity_constraint.note` names
the UNCHANGED Q8 + the §6 human. This is the sharpest demonstration that the marker is a REASON never a
CHOICE: it says "the recorded capacity says the recommended option can't run," and the human (not the
machine) must choose the replacement. The seven Sprint-29 orgs stay byte-identical (a no-requirements org
keeps today's block exactly); full non-regression green; SPEC v0.22, 49 `$defs`, `ros/` and the frozen
49-`$defs`/URI cap unchanged; `adjudication_engine.py` untouched (pure recorded data + a runner).

## 13. Update after Sprint 31 — the whole §7L decision surface is inventoried as reason-not-choice (positive consolidation, NO engine change)

Sprint 31 (`run_recorded_surface_demo.py`, new, exit 0 = ALL PASS) is the OPPOSITE of another capability
sprint: it makes the label-vs-choice boundary the ORGANIZING truth of a full INVENTORY of the recorded-data
decision surface. `adjudication_engine.py` is byte-identical (hash `a60f8f7…` unchanged) — a survey runner
+ recorded data only, exactly as Sprint 30. It drives 11 orgs (the eight Sprint-30 orgs byte-identical,
plus `inspect-recorded`, `cove-recorded`, and `inspect-nodata` — all new labels, no fixture overwrite) and
emits a structured `recorded_surface` per org:

- **present_recorded** = {metric_series, point_variance, band_variance, capacity, capacity_requirements,
  floor_gated, weights, reconcile_rule} — which RECORDED descriptors the org actually carries;
- **derived_reasons** = {Q3_forecast, Q6_projection, Q7Q8_capacity_constraint, Q9_capacity,
  Q8_do_nothing_impact} — the actual derived REASON each produced, or None;
- **derivable_universe** = the sorted set of every derived reason;
- **not_derivable** = the named optimization seam + any descriptor the org does NOT record.

It asserts per org: (a) every derived label traces to a recorded descriptor (Q3/Q6/Q8-forecast →
metric_series; Q7Q8/Q9-capacity → capacity; the no-data org derives NOTHING — the engine never invents a
reason the org did not record), and (b) the **reason-not-choice proof, totalled**: Q7 `options` +
`machine_eligible_best` + Q8 `recommendation` + `floor_gated` EXACTLY equal `cockpit_q7q8` for ALL 11 orgs —
print "11/11 orgs the marker never re-ranks; INCLUDES the Sprint-30 org `deli-recommend-infcap` where the
RECOMMENDED option is `capacity_infeasible`". This is positive consolidation: after six sprints the WHOLE
§7L decision surface is provably recorded-data + a REASON, and no recorded data ever re-ranks the Q8
recommendation (it provably stays the frozen `rank` output on every org). The §16 verdict is honest: the
surface is now fully inventoried as reason-not-choice; the ONE remaining out-of-scope step is a
capacity-constrained OPTIMIZATION that re-ranks for the machine (a policy / user decision, deliberately NOT
built; its seam = recorded per-option `capacity_requirements` + a deterministic next-best-non-infeasible
rule by the frozen `rank` utility), plus a per-option requirement not unit-coupled / no recorded
requirement. No SPEC bump (v0.22).

## 14. Update after Sprint 32 — the capacity-constrained RE-RANK of the §7L Q8 recommendation for the machine (an EXPLICIT authorized POLICY step, distinct from the reason-not-choice advisory)

Sprint 32 (`capacity_rerank.py`, NEW module + `run_capacity_rerank_demo.py`, NEW runner, exit 0 = ALL PASS)
builds the ONE step Sprint 30/31 named and deliberately left out of scope — **because this prompt
explicitly asked for it**. The engine is UNTOUCHED (hash `a60f8f7…` byte-identical); the re-rank is a NEW
pure module that reuses the engine's public surface (the `capacity_constraint` block `cockpit_s7l`
renders from recorded data + the frozen `rank` utility). When an org's machine-eligible best is
`capacity_infeasible` (from RECORDED per-option `capacity_requirements` > available = recorded
capacity.value − recorded load), the re-rank computes the **highest-utility option that is neither
floor-gated nor `capacity_infeasible`** — a deterministic next-best-non-infeasible rule by the frozen
`rank` utility, reported as an additive `capacity_rerank` block (`prior_machine_best`,
`prior_best_capacity_flag`, `recorded_descriptors`, `available_capacity`, `per_option_requirements`,
`replacement`, `replacement_is_baseline`, `all_capacity_consuming_infeasible`, `floor_respected`,
`policy`, `why`).

PROVEN: RE-RANK fires on `deli-recommend-infcap` (partial-settlement → conditional-resolution),
`inspect-recorded` (rework-partial-credit → conditional-accept-with-guarantee),
`cove-recommend-infcap` (NEW — step-therapy-first → authorize-generic), and `deli-all-infeasible` (NEW —
every capacity-consuming option infeasible → unresolved baseline, `replacement_is_baseline` True); the
re-ranked Q8 == the recomputed highest non-infeasible non-gated utility option by the frozen `rank`.
UNCHANGED (best NOT infeasible → byte-identical to `cockpit_q7q8`): the nine other orgs incl.
`cove-recorded` and no-data `inspect-nodata`. **The advisory path NEVER re-ranks**: even where re-rank
fires the engine's Q8 recommendation still equals `cockpit_q7q8` — the Sprint-31 reason-not-choice
inventory stands untouched; the §6 floor is respected (a floor-gated option is never auto-picked); the
fallback to the do-nothing/UNRESOLVED baseline is stated. Deterministic; the two NEW fixture dirs pass
Sprint-0 C1-C5; full non-regression green; engine `a60f8f7…`, schema `7fc38c8c…`, 49 `$defs`, SPEC v0.22.

**§14 verdict — is the ONE remaining Q8 frontier now derivable?** Yes, as an explicit authorized POLICY
step distinct from the deterministic advisory label-vs-choice boundary: the advisory path still labels
(the marker stays a REASON, never a CHOICE) and never re-ranks; the re-rank computes a capacity-
constrained replacement from recorded data under POLICY, respects the §6 floor, and is deterministic +
additive (new module, engine byte-identical). **Still not derivable (honest residual):** a probabilistic
/stochastic forecast (the recorded band is a spread, never a CI); a per-option requirement NOT unit-
coupled to the recorded capacity value / an option with no recorded requirement (the machine never
invents one); and any choice the §6 human must make that recorded data cannot machine-decide. No SPEC
bump (v0.22).
## 15. Update after Sprint 33 — the now-TWO-path decision surface consolidated as ONE coherent recorded-data framework: the reason-not-choice ADVISORY and the POLICY-authorized capacity-constrained RE-RANK proven to compose without one silently shadowing the other

The §7L Q7/Q8 morning line now lives on TWO deliberately distinct pathways over the same recorded data: the
default **reason-not-choice ADVISORY** (Sprint 31 — the marker is a REASON, never a CHOICE; the Q8
recommendation provably stays the frozen `rank` output, the §6 human always rules) and the **POLICY-authorized
capacity-constrained RE-RANK** (Sprint 32 — `capacity_rerank.capacity_rerank`, a new additive module that, when
the machine-eligible best is `capacity_infeasible` from recorded per-option `capacity_requirements`, picks the
highest-utility option that is neither floor-gated nor `capacity_infeasible`, emitted as DATA and never
overwriting the advisory Q8). **Sprint 33 consolidates them as ONE framework** — `run_two_path_demo.py` (new
runner; **`adjudication_engine.py` sha256 `a60f8f7…` AND `capacity_rerank.py` sha256 `f7c6a185…` byte-identical**)
drives the same 13 orgs and classifies each into an exhaustive-disjoint PATH class:
- **ADVISORY-no-capacity** (5) — no recorded capacity → the advisory is the single answer;
- **ADVISORY-best-runnable** (4) — capacity recorded, best runnable → `needed=False`, replacement == advisory Q8;
- **RE-RANK** (4) — best `capacity_infeasible` → by POLICY a replacement is chosen (a different option).

PROVEN (ALL PASS): (a) **composition** — advisory Q8 == `cockpit_q7q8` for all 13 (the re-rank never shadows
it); where it fires the replacement is a different option and ≠ the machine_eligible_best; where `needed=False`
they agree; (b) **floor integrity** — no advisory or re-rank selection is floor-gated (asserted against `rank`);
(c) **exhaustive-disjoint taxonomy**; (d) **determinism vs history** — identical `two_path_surface` on re-run,
and the Sprint-31 reason-not-choice tally (11/11) + the Sprint-32 re-rank results both reproduce from the SAME
recorded data. §15 verdict: the two paths are ONE coherent recorded-data framework; the deterministic advisory
label-vs-choice boundary still holds on the default path. Still not derivable: a probabilistic/stochastic
forecast; a per-option requirement not unit-coupled to the recorded capacity / an option with no recorded
requirement (never invented); any §6-human choice recorded data cannot machine-decide (the re-rank is
POLICY-authorized, not objective best). No SPEC bump (v0.22); no new noun.
