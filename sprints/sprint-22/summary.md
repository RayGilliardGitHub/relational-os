# Sprint 22 — summary

**Goal.** Sprints 20–21 built a configurable adjudication engine (`adjudication_engine.py`) that renders
the full §7L Q1–Q10 morning cockpit for ANY configured org, data-only; Sprint 20 made the recorded Q6
forecast + Q9 capacity answered AS DATA, and Sprint 21 closed the seam by connecting the recorded forecast
to the decision surface (Q3 attention + the Q8/trade-off do-nothing baseline). **Sprint 21's own findings
disclosed the next honest frontier: the forecast→attention crossing test was hardcoded to the
higher-is-better / rate case** (`min(projection) < threshold`). A metric where "lower is better" — a cost,
latency, defect rate, or risk — would NOT flag as forecast-driven attention when it deteriorates by RISING
above a recorded ceiling. **Sprint 22 closes that bounded slice** by making the crossing **direction a
recorded, additive parameter**, so the SAME data-only closure flags Q3 attention + prices the Q8 do-nothing
baseline for BOTH directions (rate/quality falling below target; cost/latency rising above ceiling), with
the Sprint-21 higher-is-better behavior **byte-identical by default**. Additive, frozen ontology, SPEC
v0.22, ~$0.

## What was built (instances/contested_reality/)
- **`adjudication_engine.py`** (the ONE permitted engine file; extend `_forecast_closure`, NOT a rewrite
  and NOT the frozen functions): made the crossing **direction a recorded, additive `direction` field** on
  the `metric://` object. `direction` defaults to `"higher-is-better"` (rate/quality: `worst=min`,
  `min < threshold` — the Sprint-21 test, byte-identical); an org records `"lower-is-better"` for a
  cost/latency/defect/risk metric (`worst=max`, `max > threshold` — projection rising above a recorded
  ceiling). `worst`/`worst_period` follow the direction; the Q3 attention `why` is worded per direction
  ("projected to fall below …" vs "projected to rise above …"); the do-nothing summary + gap are oriented
  per direction ("below recorded … by" vs "above recorded … by"). The additive `direction` key is carried
  on the closure, `q6`, `q8["forecast"]`, and `do_nothing_expected_impact`. Threshold resolution is
  UNCHANGED (`forecast_threshold` → metric `target` → last `actual`). Frozen functions
  (`reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/`rank`/`machine_eligible_best`/
  `render_tradeoff`/`cockpit_q7q8`) untouched; 49 `$defs`/URI cap/SPEC v0.22 intact; `direction` an additive
  field (**no new noun**); `ros/` untouched. `render_cockpit_s7l` needed no change (it already renders the
  do-nothing summary generically).
- **`run_forecast_direction_demo.py`** (new runner, exit 0 = ALL PASS): drives ≥5 orgs — the two Sprint-21
  higher-is-better orgs `deli-forecast` (deteriorating) and `deli-forecast-flat` (on-target), recorded
  WITHOUT a `direction` field to prove the default (asserted **byte-identical to Sprint 21**); a NEW
  **lower-is-better** rising-cost org `deli-cost` (explicit `direction="lower-is-better"`, actuals
  12/14/16/18 ms, ceiling 16 → projection [20,22,24] → `max > ceiling` → Q3 `[forecast]` item + a
  do-nothing cost priced in the RISING orientation, on_target=False); a second lower-is-better control
  `deli-cost-flat` (projection [8,8,8] stays below ceiling 10 → no forecast attention, do-nothing
  on_target=True); and the no-data `deli` (unchanged fallback). Asserts full §7L Q1–Q10 on each;
  higher-is-better byte-identical; lower-is-better Q3 + rising do-nothing cost; flat controls on-target;
  determinism; agreement of Q8 with `forecast_metric` + hand-computed projection; no §6 overrule;
  no wall-clock. Emits fixtures + a report.

## Verified output (all exit 0, ALL PASS)
- **`deli-forecast` (higher, deteriorating):** direction defaults to `higher-is-better`; Q3 `[forecast]`
  item + Q8/trade-off do-nothing cost **byte-identical to Sprint 21** ("… below recorded target 0.95 by
  0.15 …", on_target=False).
- **`deli-forecast-flat` (higher, on-target):** direction defaults `higher-is-better`; NO forecast item;
  do-nothing on-target **byte-identical to Sprint 21**.
- **`deli-cost` (lower, RISING):** records explicit `direction="lower-is-better"` (on the `metric://`
  object + carried through q6/forecast/do_nothing); Q3 `[forecast]` item "forecast: projected to rise above
  16.0 (target) — worst 24.0 at period 3"; Q8/trade-off do-nothing cost in the RISING orientation:
  "… projects to worst 24.0 (period 3) above recorded target 16.0 by 8.0 — doing nothing lets the recorded
  trend deteriorate" (on_target=False); `worst == max(projection)`, projection [20,22,24] == `forecast_metric`
  == hand-computed.
- **`deli-cost-flat` (lower, below ceiling):** NO forecast attention; do-nothing priced on-target
  ("stays at/below recorded target 10.0 (worst 8.0) … no forecast-driven cost", on_target=True).
- **`deli` (no data):** unchanged Q3/Q8/trade-off fallback; Q6 still "cannot forecast from recorded data".
- **Conformance:** the new `deli-cost` + `deli-cost-flat` fixtures pass the Sprint-0 venv C1–C5 ALL PASS
  (26 instances each, **49 `$defs`**); the additive `direction` field survives the C2 temporal-suffix probe.
- **Determinism + agreement:** structured dict + rendered line identical on re-run (all 5 orgs);
  `q8["forecast"]` projections == `forecast_metric` == hand-computed on all 4 recorded orgs.

## Non-regression (all exit 0)
All C-R runners (12 + `run_cockpit_s7l_demo` + `run_forecast_capacity_demo` + the Sprint-21
`run_forecast_action_demo` — byte-identical after the engine change + the new `run_forecast_direction_demo`)
ALL PASS. `conformance_adjudication.py` **16 labels** C1–C5. Sector `build_all.py` + `conformance_all.py`,
S5 reference demo + conformance, agent demo + conformance — ALL PASS. `deli`/`cove` fixtures carry **no**
closure keys and the two Sprint-21 recorded orgs' Q3/Q8 unchanged (direction default) — **byte-identical up
to the clock**. Only `.py` code changed: `adjudication_engine.py` + the new runner. Schema hash
`7fc38c8c…`, **49 `$defs`**, **SPEC v0.22**, `ros/` untouched, only catalog URI schemes — no new noun.

## §16 verdict
**For an org that records a series + its metric's `direction`, the loop Q6 → Q3 → Q8 now closes AS DATA
for BOTH metric directions.** A rate/quality metric (higher-is-better) whose projection is projected to fall
below its recorded threshold/target, and a cost/latency/defect/risk metric (lower-is-better) whose projection
is projected to rise above its recorded ceiling, each become a prioritized attention item on Q3 (§7J.5 —
"do nothing and it gets worse"), and Q8/the trade-off price the do-nothing baseline from that same
projection **in the correct orientation** (below-target vs above-ceiling). It is all deterministic and
data-only — direction, threshold resolution (explicit `forecast_threshold` → `target` → last `actual`), the
crossing test, and the do-nothing summary derive exclusively from the recorded series + the recorded
direction; never the wall-clock. The higher-is-better default keeps Sprint-21 byte-identical. The **Q8
recommendation is UNCHANGED** (the forecast prices attention + do-nothing but never overrules the
§6-floor-gated machine-eligible best), and the determination stays the §6 human's `determination_policy`
call. **What is still not derivable:** an org that has NOT recorded a realized-vs-expected series cannot be
forced to forecast or to produce a forecast-driven attention item/cost — the cockpit reports the recorded
reality and does not manufacture certainty (correct). A richer/adaptive forecast model (beyond the
deterministic last-actual + mean-delta projection) remains out of scope of the honest, deterministic, ~$0
stance.

## Open issues / next work
- The **projection holds the recorded trend (last actual + mean delta)** — a transparency-first
  deterministic model, not adaptive/stochastic. A future sprint could model Q6 more richly, but trades
  determinism/auditability for complexity.
- The crossing is now **directional**, but the direction must be RECORDED on the metric; an org that has a
  series but no recorded `direction` is treated as higher-is-better (the documented, byte-identical
  default) — a possible future hardening is to flag an unrecorded-direction cost-series as ambiguous, but
  that would invent data, so it is correctly out of the deterministic stance.
- Data-grounding (and the forecast→action closure) stays **conditional on an org recording the series +
  direction** — that is correct, not a gap.

## Docs touched (no SPEC bump)
- `contested_reality/docs/ENGINE-FORECAST-DIRECTION.md` (new) + additive Sprint-22 note in
  `docs/ENGINE-FORECAST-ACTION.md`
- `instances/README.md` (Sprint-22 entry)
- `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` ("Update after Sprint 22")
- `~/.hermes/skills/software-development/relational-os/references/forecast-direction-closure.md` (new) +
  additive Sprint-22 note in `references/forecast-action-closure.md`
- `sprints/sprint-22/{plan.md,work/1-plan.md,notes/findings.md,summary.md}`
- `sprints/sprint-23/PROMPT.md` (next prompt)
- `instances/contested_reality/`: `adjudication_engine.py` (extend `_forecast_closure`),
  `run_forecast_direction_demo.py` (new)