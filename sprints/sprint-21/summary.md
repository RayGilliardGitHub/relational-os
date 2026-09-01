# Sprint 21 — summary

**Goal.** Sprints 13–20 built a configurable adjudication engine (`adjudication_engine.py`) that renders the
full §7L Q1–Q10 morning cockpit for ANY configured org, data-only. Sprint 20 made the recorded Q6 forecast
+ Q9 capacity answered AS DATA — but its own findings disclosed the next honest frontier: **the Q6 forecast
was COMPUTED and RENDERED but not CONNECTED to the org's decision surface** (a projected deterioration did
not by itself change Q3 attention or the Q8 expected-impact / trade-off do-nothing cost). **Sprint 21
closes a bounded slice of that** by making the RECORDED forecast DRIVE the §7L Q3 attention and the Q8
expected-impact / trade-off do-nothing baseline, deterministically and data-only, with the honest no-data
fallback unchanged. Additive, frozen ontology, SPEC v0.22, ~$0.

## What was built (instances/contested_reality/)
- **`adjudication_engine.py`** (the ONE permitted engine file; append + in-place `.q3`/`.q6`/`.q8` +
  render, NOT a rewrite): added a `_num` numeric helper and `_forecast_closure(cfg, sub)` — computed ONCE in
  `cockpit_s7l` to drive Q3/Q6/Q8 so they agree by construction. The closure resolves a **recorded
  threshold** (explicit `forecast_threshold` additive field → the metric's own `target` → the last recorded
  `actual`) and flags **crossing** = `min(projection) < threshold` (the "do nothing and it gets worse"
  condition). Extending `cockpit_s7l`: `.q3` gains a **forecast-driven attention item** (tagged `forecast`)
  when a recorded series crosses; `.q6` now reuses the closure; `.q8`/`q7` gain additive
  `forecast`/`do_nothing_expected_impact`/`tradeoff_do_nothing_impact` fields pricing the do-nothing
  baseline from the projection. `render_cockpit_s7l` renders the Q3 `[forecast]` tag + the Q8/trade-off
  do-nothing line. **The Q8 recommendation is UNCHANGED** — the forecast prices attention + do-nothing but
  never overrules the §6-floor-gated machine-eligible best. Frozen functions (`reconcile`/`run_scenario`/
  `_derive`/`SPEC_VOCAB`/`_aggregate`/`rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`)
  untouched. 49 `$defs`/URI cap/SPEC v0.22 intact; `forecast_threshold` an additive field (**no new noun**);
  `ros/` untouched.
- **`run_forecast_action_demo.py`** (new runner, exit 0 = ALL PASS): drives ≥3 orgs — the Sprint-20
  `deli-forecast` (recorded series that DETERIORATES: projection [0.84,0.82,0.8] crosses target 0.95), a NEW
  on-target control `deli-forecast-flat` (flat [0.96,0.96,0.96], no crossing), and the no-data `deli`
  (unchanged fallback). Asserts full §7L Q1–Q10 on each; the deteriorating org's Q3 carries the `[forecast]`
  item + a crossing do-nothing cost (on_target=False); the flat control adds NO forecast attention + prices
  do-nothing on_target=True; the no-data org keeps today's Q3/Q8/trade-off (byte-identical fallback);
  determinism on re-run; agreement of Q8 with `forecast_metric` + a hand-computed projection; **no §6
  overrule** (Q8 recommendation == `cockpit_q7q8` for every org); no wall-clock. Emits the recorded-org
  fixtures + `cockpit-forecast-action.md` report.

## Verified output (all exit 0, ALL PASS)
- **`deli-forecast` (deteriorating):** Q3 adds `metric://deli-forecast/m-on-time [forecast] — forecast:
  projected to fall below 0.95 (target) — worst 0.8 at period 3`; Q8/trade-off: `forecast-driven do-nothing
  cost: … projects to worst 0.8 (period 3) below recorded target 0.95 by 0.15 — doing nothing lets the
  recorded trend deteriorate (baseline unresolved, priced=True, on-target=False)`.
- **`deli-forecast-flat` (on-target):** NO `[forecast]` Q3 item; Q8/trade-off: `on-target: … projection stays
  at/above recorded target 0.95 (worst 0.96) — no forecast-driven cost to doing nothing
  (on-target=True)`.
- **`deli` (no data):** unchanged Q3/Q8/trade-off fallback; Q6 still `cannot forecast from recorded data`.
- **Conformance:** the `deli-forecast` + `deli-forecast-flat` fixtures pass the Sprint-0 venv C1–C5 ALL PASS
  (26 instances each, **49 `$defs`**).
- **Determinism + agreement:** structured dict + rendered line identical on re-run (all 3 orgs);
  `q8["forecast"]` projections == `forecast_metric` == hand-computed from the recorded points.

## Non-regression (all exit 0)
All 12 C-R runners + `run_cockpit_s7l_demo` + `run_forecast_capacity_demo` + the new
`run_forecast_action_demo` — ALL PASS. `conformance_adjudication.py` **16 labels** C1–C5. Sector
`build_all.py` + `conformance_all.py`, S5 reference demo + conformance, agent demo + conformance — ALL PASS.
`deli`/`cove` fixtures carry **no** Sprint-21 closure keys (they record no series) — **byte-identical up to
the clock**. Schema hash `7fc38c8c…`, **49 `$defs`**, **SPEC v0.22**, `ros/` untouched, only catalog URI
schemes — no new noun.

## §16 verdict
**For an org that records a series, the loop Q6 → Q3 → Q8 is now closed as data.** Q6 projects the
deterministic "if nothing changes" trajectory; Q3 turns a projection that crosses a recorded threshold into
a prioritized attention item (tagged `forecast` — "do nothing and it gets worse" is itself attention,
§7J.5); Q8/the trade-off price the do-nothing baseline from that same projection — all from recorded data,
never the wall-clock. The Q8 recommendation is UNCHANGED (the forecast prices attention + do-nothing but
never overrules the §6-floor-gated machine-eligible best), and the determination stays the §6 human's
`determination_policy` call; S5 alone moves Trust. **What is still not derivable:** an org that has NOT
recorded a series cannot be forced to forecast or to produce a forecast-driven attention item/cost — the
cockpit reports the recorded reality and does not manufacture certainty (correct). A richer/adaptive
forecast model (beyond the deterministic last-actual + mean-delta projection) remains out of scope of the
honest, deterministic, ~$0 stance.

## Open issues / next work
- The **projection holds the recorded trend (last actual + mean delta)** — a transparency-first
  deterministic model, not an adaptive/stochastic forecast. A future sprint could model Q6 more richly, but
  that trades determinism/auditability for complexity.
- The crossing test is standardized on the **higher-is-better rate/quality** case; a metric where "lower is
  better" (e.g. cost) would need the inverse test — a possible future hardening.
- Data-grounding (and the forecast→action closure) stays **conditional on an org recording the series** —
  that is correct, not a gap.

## Docs touched (no SPEC bump)
- `contested_reality/docs/ENGINE-FORECAST-ACTION.md` (new) + additive Sprint-21 note in
  `docs/ENGINE-FORECAST-CAPACITY.md`
- `instances/README.md` (Sprint-21 entry)
- `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` ("Update after Sprint 21")
- `references/forecast-action-closure.md` (skill reference)
- `sprints/sprint-21/{plan.md,work/1-plan.md,notes/findings.md,summary.md}`
- `sprints/sprint-22/PROMPT.md` (next prompt)
- `instances/contested_reality/`: `adjudication_engine.py` (append + in-place closure),
  `run_forecast_action_demo.py` (new)