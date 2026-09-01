# Sprint 20 — summary

**Goal.** Sprints 13–19 built a configurable adjudication engine (`adjudication_engine.py`) that renders the
full §7L Q1–Q10 morning cockpit for ANY configured org (Sprint 19), data-only. Sprint 19's own honest limits
("Residual seams"): **Q6 cannot forecast** (no org records a realized-vs-expected series) and **Q9
"capability"** is the holder-of-authority assignment, not a capacity number. **Sprint 20 closes a bounded
slice of both** by making an org RECORD the missing data additively on its own graph/ledger — a `metric://`
realized-vs-expected series and an additive `capacity` field on the `authority://` object the Q9 question
reads — so those two questions are answered **AS DATA where the data exists**, with the honest no-data
fallback unchanged. Additive, frozen ontology, SPEC v0.22, ~$0.

## What was built (instances/contested_reality/)
- **`adjudication_engine.py`** (the ONE permitted engine file; append + in-place `.q6`/`.q9`/render-line,
  NOT a rewrite): added `forecast_metric(cfg, sub, metric_uri, *, horizon)` — a **deterministic projection**
  purely from the recorded `metric://` realized-vs-expected series (last recorded `actual` + mean of recorded
  consecutive deltas, forward periods, labelled a projection, never the wall-clock); `record_metric_series` +
  `record_capacity` — REPLAYABLE recorders that append the data to the org's own immutable ledger (one signed
  event, merge-not-replace); `_recorded_metric_with_series` helper; and extended `cockpit_s7l`'s `.q6`/`.q9`
  + `render_cockpit_s7l`'s Q6/Q9 lines to consume the recorded data when present. Frozen functions
  (`reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/`rank`/`machine_eligible_best`/
  `render_tradeoff`/`cockpit_q7q8`) untouched. 49 `$defs`/URI cap/SPEC v0.22 intact; `metric://` a first-class
  catalog noun and `capacity` an additive envelope field (**no `capacity://` noun**); `ros/` untouched.
- **`run_forecast_capacity_demo.py`** (new runner, exit 0 = ALL PASS): drives a NEW org `deli-forecast` (a
  clean relabel of `deli` onto its own namespace; records a `metric://deli-forecast/m-on-time` series +
  `capacity` on `authority://deli-forecast/adjudicate`) and the existing `deli` (no data). Asserts: both keep
  the full §7L Q1–Q10; the recorded org forecasts Q6 `[0.84, 0.82, 0.8]` + reports capacity `1.0 obligations`;
  `deli` keeps the honest Q6 fallback + no-capacity Q9; determinism; agreement with the recorded graph (q6
  projection == hand-computed, q9.capacity == the recorded authority field); no wall-clock; honest
  `forecast_metric` fallback. Emits the deli-forecast fixtures + `cockpit-forecast-capacity.md` report.

## Verified output (all exit 0, ALL PASS)
- **`deli-forecast` (recorded data):** Q6 `project from last actual 0.86 + mean delta -0.02:
  period 1->0.84; period 2->0.82; period 3->0.8 | recorded variance -0.09`; Q9 `… actors 7,
  capacity 1.0 obligations (load 0.6)`. Full §7L Q1–Q10 present.
- **`deli` (no data):** Q6 `cannot forecast from recorded data (no recorded realized-vs-expected series)`;
  Q9 no-capacity (`capacity_recorded=False`). Full §7L Q1–Q10 present.
- **Conformance:** the deli-forecast fixtures pass the Sprint-0 venv C1–C5 ALL PASS (**49 `$defs`**).
- **Determinism + agreement:** structured dict + rendered line identical on re-run; `forecast_metric` pure on
  re-call; projection == hand-computed from the recorded points; q9.capacity == the recorded authority field.

## Non-regression (all exit 0)
All 12 contested-reality runners (the 6 curated CR runners + `run_cockpit_s7l_demo` + the 4 prior CR demos +
the new `run_forecast_capacity_demo`), `conformance_adjudication.py` **16 labels** C1–C5, sector
`build_all.py` + `conformance_all.py`, S5 reference demo + conformance, agent demo + conformance — ALL PASS.
`deli`/`cove` **byte-identical up to the clock** (engine demo run twice, timestamp keys stripped → identical).
Schema hash `7fc38c8c…`, **49 `$defs`**, **SPEC v0.22**, `ros/` untouched, only catalog URI schemes — no new
noun.

## §16 verdict
**The §7L morning cockpit is now data-grounded on every one of the ten questions WHERE the data exists.**
Q6 projects a deterministic "if nothing changes" forecast from a RECORDED realized-vs-expected series, and Q9
reports a RECORDED capacity number+unit — never the wall-clock, never an invented number. Where an org has not
recorded them, the cockpit stays honest: Q6 plainly says it cannot forecast and Q9 reports no capacity rather
than fabricating one. Q7/Q8 stay the Sprint-18 engine line (delegated by construction); #8 is the
machine-eligible best, §6-floor-gated, carrying the authority it requires; the determination is the §6 human's
`determination_policy` call; S5 alone moves Trust. The honest remaining limit: data-grounding is conditional on
the org recording the data — the engine reports the recorded reality and does not manufacture certainty.

## Open issues / next work
- The **projection holds the recorded trend (last actual + mean delta)** — a transparency-first deterministic
  model, not an adaptive/stochastic forecast. A future sprint could model Q6 more richly, but that would trade
  determinism/auditability for complexity.
- **Capacity is a single recorded scalar (+ load)**, not a dynamic capacity/queuing model.
- Data-grounding stays conditional on an org recording the metrics/capacity — that is correct, not a gap.

## Docs touched (no SPEC bump)
- `contested_reality/docs/ENGINE-FORECAST-CAPACITY.md` (new) + additive Sprint-20 note in
  `docs/ENGINE-S7L-COCKPIT.md`
- `instances/README.md` (Sprint-20 entry)
- `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` ("Update after Sprint 20")
- `sprints/sprint-20/{plan.md,work/1-plan.md,notes/findings.md,summary.md}`
- `sprints/sprint-21/PROMPT.md` (next prompt)
- `instances/contested_reality/`: `adjudication_engine.py` (append), `run_forecast_capacity_demo.py` (new)