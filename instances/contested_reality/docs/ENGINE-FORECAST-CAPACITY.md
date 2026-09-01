# ENGINE-FORECAST-CAPACITY — recorded-data Q6 forecast + Q9 capacity for the §7L morning cockpit (Sprint 20)

**Scope.** Sprint 19 made `adjudication_engine.cockpit_s7l` render the full §7L Q1–Q10 cockpit, data-only,
for any configured org — but its own findings (`notes/findings.md`, "Residual seams") were honest about what
it could NOT answer on the adjudication orgs: **Q6 "what if we do nothing?"** (none records a
realized-vs-expected series, so the cockpit truthfully said "cannot forecast from recorded data") and
**Q9 "capability/capacity"** (rendered as holder-of-authority assignment, not a capacity number). **Sprint 20
closes a bounded slice of both**: an org now *records* the missing data additively on its own graph/ledger —
a `metric://` realized-vs-expected series and an additive `capacity` field on the `authority://` object the
Q9 question reads — and `cockpit_s7l`'s `.q6`/`.q9` answer those questions **AS DATA where the data exists**,
with the honest no-data fallback unchanged.

This document states the deterministic projection rule, the replayable recorders, what each org answers, how
it is generic + additive, the ≥2-org proof, and the honest §16 verdict.

---

## 1. The deterministic projection rule (`forecast_metric`)

`forecast_metric(cfg, sub, metric_uri, *, horizon=N)` reads a recorded `metric://` object and its `points`
list (per-period dicts each with an `actual` and optional `expected`/`target`/`variance`), and projects
purely from those RECORDED values — never the wall-clock, never an invented number:

- `last_actual` = the last recorded point's `actual`
- `mean_delta`   = the mean of consecutive recorded actual-deltas (direction of travel; 0 when < 2 points)
- forward projection, for each period `f` in `1..horizon`: `projected(f) = round(last_actual + mean_delta * f, 4)`
- the **last recorded `variance`** is reported alongside, and the result is **labelled a projection**, never
  expanded to an outcome.

When no recorded realized-vs-expected series exists on the given `metric://` object, it returns honestly
`{"available": False, "forecast": "cannot project — no recorded realized-vs-expected series on …"}`
(verified in the runner on a metric the org never recorded).

## 2. The replayable recorders (additive, on the org's own ledger)

- `record_metric_series(sub, label, metric_uri, *, points, fields, signer)` appends ONE signed
  `event://<label>/record-metric-series` STATE_CHANGE carrying the `metric://` object (Metric `$def`:
  required `uri`/`name`/`formula`, plus the additive `points` list and `unit`/`target`/`period`/`source`/
  `owner`); `actual`/`variance` are set to the LAST recorded point. The object's keys are C2-safe (no
  temporal suffix).
- `record_capacity(sub, authority_uri, *, value, unit, signer, load=None)` appends ONE signed
  `event://<label>/record-capacity` STATE_CHANGE merging an additive `capacity` field
  `{value, unit, load, status}` onto the `authority://` object **merge-not-replace** (the authority's
  required fields ride along → §2 preserve-unknown). No new noun, no `$defs` edit.

Both are symmetric with `reconcile_learning.record_realized_outcome`'s append-only, signed-event discipline.

## 3. What `cockpit_s7l` now answers, per org

Verified output of `run_forecast_capacity_demo.py` (from `instances/contested_reality`, exit 0 = ALL PASS):

| org | records? | Q6 ("what if we do nothing?") | Q9 ("who does it, authority/capacity?") |
|---|---|---|---|
| `deli-forecast` (NEW) | a `metric://deli-forecast/m-on-time` series + `capacity` on `authority://deli-forecast/adjudicate` | **deterministic projection** `[0.84, 0.82, 0.8]` (last actual 0.86, mean delta −0.02, horizon 3), recorded variance −0.09 | capacity **`1.0 obligations`** (load 0.6) |
| `deli` (existing) | none | **honest fallback** "cannot forecast from recorded data (no recorded realized-vs-expected series)" | no-capacity (capacity_recorded=False) |

Both orgs still render the **full §7L Q1–Q10** cockpit (all ten questions + their recorded-data evidence
present). Abridged Q6/Q9 render for `deli-forecast`:

```
Q6. what if we do nothing?  project (holding the recorded trend) from last actual 0.86 + mean delta -0.02:
      period 1 -> 0.84; period 2 -> 0.82; period 3 -> 0.8  |  recorded variance -0.09
Q9. who does it, authority/capacity?  adjudicator person://deli-forecast/adjudicator (authority
      authority://deli-forecast/adjudicate), obligated party org://deli-forecast/company, appeal
      authority://deli-forecast/adjudicate-appeal, actors 7, capacity 1.0 obligations (load 0.6)
```

## 4. How it is generic + additive

- **One engine function, no per-org Python.** `cockpit_s7l(cfg, sub, library=...)` reads a recorded
  `metric://` series and a recorded `capacity` field exactly like it reads everything else — from `cfg` +
  the org's own `sub` graph/ledger. No per-org engine branch: an org either has recorded the data (forecast
  + capacity appear) or has not (the existing honest fallback).
- **Additive only.** The ONLY engine file touched is `adjudication_engine.py` (append `forecast_metric`,
  `_recorded_metric_with_series`, `record_metric_series`, `record_capacity`; extend `cockpit_s7l`'s
  `.q6`/`.q9` and `render_cockpit_s7l`'s Q6/Q9 lines). The frozen functions (`reconcile`/`run_scenario`/
  `_derive`/`SPEC_VOCAB`/`_aggregate`/`rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`) are
  untouched; **49 `$defs` / URI cap / SPEC v0.22** intact; `metric://` is a first-class catalog noun and
  `capacity` an additive envelope field — **no `capacity://` scheme**; `ros/` untouched.
- **Deterministic.** No wall-clock anywhere: `forecast_metric` is a pure function of the recorded points +
  the explicit `horizon`; the cockpit dict + rendered line are identical on re-run (asserted for both orgs,
  and `forecast_metric` is asserted pure on re-call).

## 5. The ≥2-org proof (real, exit-0)

`run_forecast_capacity_demo.py` (exit 0 = ALL PASS) drives a NEW org `deli-forecast` (a clean relabel of
`deli` onto its own `deli-forecast://` namespace, so it owns its own `authority://deli-forecast/adjudicate`)
and the existing `deli`, and asserts:
(a) BOTH orgs keep the full §7L Q1–Q10 cockpit, each question with recorded-data evidence;
(b) `deli-forecast` answers Q6 with the deterministic projection `[0.84, 0.82, 0.8]` (from its recorded
    series only) and Q9 with capacity `1.0 obligations` (load 0.6);
(c) `deli` keeps the honest Q6 fallback and the no-capacity Q9;
(d) determinism (structured dict + rendered §7L line identical on re-run; `forecast_metric` pure on re-call);
(e) AGREEMENT: the q6 projection equals the hand-computed projection from the recorded points, q9.capacity
    equals the recorded `capacity` field on the authority object (read off the org's own graph), and every
    projection is derived from recorded series values only (no wall-clock);
(f) the recorded-data `deli-forecast` fixtures pass the Sprint-0 C1–C5 conformance (frozen schema, 49 $defs).

## 6. Verification / non-regression (all exit 0)

- New runner: `python3 run_forecast_capacity_demo.py` → **ALL PASS** (from `instances/contested_reality`).
- New-org conformance: the Sprint-0 venv over `artifacts/adjudication/fixtures/deli-forecast` → C1–C5 ALL PASS.
- Existing demos re-verified ALL PASS: the 6 curated C-R runners (`run_adjudication_engine_demo`,
  `run_rule_comparison_demo`, `run_rule_authoring_demo`, `run_rule_library_demo`,
  `run_reconcile_learning_demo`, `run_cockpit_q7q8_demo`) + `run_cockpit_s7l_demo` + the 4 prior CR demos.
- Conformance: `conformance_adjudication.py` **16 labels** C1–C5 ALL PASS. Sector `build_all.py` +
  `conformance_all.py`, S5 reference demo + conformance, agent demo + conformance — ALL PASS.
- `deli`/`cove` **byte-identical up to the clock** (running the engine demo twice and diffing with the
  timestamp keys stripped — proved identical). Schema hash `7fc38c8c…`, **49 `$defs`**, **SPEC v0.22**,
  `ros/` untouched, only catalog URI schemes — no new noun.

## 7. Honest §16 verdict — is the §7L morning cockpit now data-grounded on all ten?

**Yes on every one of the ten questions WHERE the data exists, and the engine says so when it does not.**
Q6 projects a deterministic "if nothing changes" forecast from a RECORDED realized-vs-expected series, and
Q9 reports a RECORDED capacity number+unit — never the wall-clock, never an invented number. Where an org
has not recorded the series/capacity, the cockpit stays honest: Q6 plainly says it cannot forecast and Q9
reports no capacity rather than fabricating one. Q7/Q8 remain the Sprint-18 engine line (delegated by
construction); #8 stays the machine-eligible best, §6-floor-gated, carrying the authority it requires; the
determination remains the §6 human's `determination_policy` call; S5 alone moves Trust.

The honest remaining limit is that **data-grounding is conditional on the org recording the data**: a
no-data org cannot be *forced* to forecast or measured for capacity, and the engine reports the recorded
reality rather than manufacturing certainty where the evidence is UNRESOLVED. That is the correct behavior —
forecasting and capacity measurement are only sound where the realized-vs-expected series and the capacity
assignment are actually recorded, and the cockpit never overclaims otherwise.

*(Evidence: all assertions are real exit-0 output from `run_forecast_capacity_demo.py` + the Sprint-0
conformance over the new org's fixtures + the full non-regression + conformance suite; SPEC v0.22,
49 `$defs`, `ros/` + schema untouched, no new noun.)*

---

## 8. Update after Sprint 21 — the recorded Q6 projection now DRIVES Q3 attention + the Q8 do-nothing

Sprint 20's honest residual seam (see its `notes/findings.md` "Residual seams") was that **the Q6
projection was computed and rendered but not CONNECTED to the org's decision surface**. **Sprint 21** (see
`ENGINE-FORECAST-ACTION.md`) closes a bounded slice: the SAME recorded `metric://` series + `forecast_metric`
projection now also:

- **Q3 (attention):** when `min(projection) < threshold`, `cockpit_s7l.q3` gains a **forecast-driven
  attention item** tagged `forecast` ("do nothing and it gets worse" is itself attention, §7J.5). The
  threshold resolves from the recorded data: explicit `forecast_threshold` additive field → the metric's
  own `target` → the last recorded `actual`. A flat/above-target recorded series adds **no** forecast item.
- **Q8 (what should we do?):** `q8["forecast"]` (projections/threshold/source/worst/crossing) +
  `q8["do_nothing_expected_impact"]` (baseline, `priced`, `on_target`, summary) + a `q7`
  `tradeoff_do_nothing_impact` line — the do-nothing baseline priced from that same projection,
  truthfully labelled forecast-driven-cost (`on_target=False`) or on-target (`on_target=True`).

It is **additive and data-only**: `_forecast_closure(cfg, sub)` is computed ONCE in `cockpit_s7l` so
Q3/Q6/Q8 agree by construction; the frozen `cockpit_q7q8`/`render_tradeoff`/`rank` are untouched (the
`base`-returned dicts are enriched additively). The **Q8 recommendation is UNCHANGED** — the forecast
prices attention + do-nothing but never overrules the §6-floor-gated machine-eligible best. The **no-data
fallback is unchanged** (no forecast item, no do-nothing fields on q7/q8). `run_forecast_action_demo.py`
proves it on ≥3 orgs (deteriorating `deli-forecast`, on-target `deli-forecast-flat`, no-data `deli`) and
the new recorded-org fixtures pass Sprint-0 C1–C5. SPEC stays v0.22, 49 `$defs`, `forecast_threshold` an
additive field (**no new noun**), `ros/` untouched.