# Sprint 22 — findings

Date: 2026-09-01. Sprint: close the honest frontier Sprint 21 disclosed — the forecast→attention crossing
test was hardcoded to the higher-is-better / rate case (`min(projection) < threshold`), so a metric where
"lower is better" (cost/latency/defect/risk) would NOT flag as forecast-driven attention when it
deteriorates by RISING above a recorded ceiling. Sprint 22 closes that bounded slice by making the crossing
**direction a recorded, additive parameter** on the `metric://` object.

## The residual seam being closed
Sprint 21's `notes/findings.md` ("Assumptions that mattered") was explicit: the crossing test used
`min(projection) < threshold` and standardized on the rate/quality case, leaving the inverse (cost/latency,
where `max(projection) > threshold` is bad) as "a possible future hardening". Sprint 22 closes that slice.

## Decisions taken
- **Direction is a RECORDED, additive `direction` field on the `metric://` object.** Default is
  `"higher-is-better"` (rate/quality: lower is worse) — normalized defensively so an unrecorded/unknown value
  behaves as higher-is-better, giving Sprint-21 **byte-identical** output. An org whose metric is a
  cost/latency/defect/risk records `direction: "lower-is-better"` (higher is worse).
- **Crossing is per direction.** higher-is-better: `worst = min(projection)`, crossing = `worst < threshold`
  (falling below a target). lower-is-better: `worst = max(projection)`, crossing = `worst > threshold`
  (rising above a ceiling). The do-nothing summary + gap are oriented per direction ("below recorded … by"
  vs "above recorded … by").
- **Threshold resolution is UNCHANGED** from Sprint 21: explicit `forecast_threshold` additive field → the
  metric's own `target` → the last recorded `actual`.
- **Q3 = attention, never an auto-pick.** A recorded series that crosses gains a `{"tag": "forecast", …}`
  Q3 item, worded per direction ("projected to fall below …" / "projected to rise above …"); a flat
  on-target series adds none; a no-data org keeps today's Q3 exactly.
- **Q8 / trade-off price the do-nothing baseline per direction.** Additive `q8["forecast"]` (+`direction`),
  `q8["do_nothing_expected_impact"]` (+`direction`, `on_target`), `q7["tradeoff_do_nothing_impact"]`. The
  **Q8 recommendation is UNCHANGED** — the forecast prices attention + do-nothing but never overrules the
  §6-floor-gated machine-eligible best.

## The ≥4/5-org proof
`run_forecast_direction_demo.py` (exit 0 = ALL PASS) drives five orgs on fresh Substrates:
- `deli-forecast` (higher-is-better, deteriorating) — recorded WITHOUT a `direction` field → default.
  Q3 `[forecast]` + Q8/trade-off do-nothing cost **byte-identical to Sprint 21** (asserted).
- `deli-forecast-flat` (higher-is-better, on-target) — default. NO forecast item; do-nothing priced
  on-target; **byte-identical to Sprint 21** (asserted).
- `deli-cost` (NEW lower-is-better, rising) — explicit `direction="lower-is-better"`, actuals 12/14/16/18 ms,
  ceiling/target 16 → projection [20,22,24] → `max > ceiling` → Q3 `[forecast]` item + do-nothing cost in
  the RISING orientation (on_target=False), gap 8.0. `worst == max(projection)`, agreement with
  `forecast_metric` + hand-computed [20,22,24].
- `deli-cost-flat` (lower-is-better, below ceiling) — explicit direction, projection [8,8,8] stays below
  ceiling 10 → NO forecast attention, do-nothing priced on-target.
- `deli` (no data) — unchanged Q3/Q8/trade-off fallback.

## Corrections / guardrails hit
- **Default keeps byte-identity.** Reading `direction` defensively (normalize anything not
  `"lower-is-better"` → `"higher-is-better"`) guarantees the two Sprint-21 recorded orgs (no `direction`
  field) stay byte-identical; the runner asserts this explicitly.
- **`direction` is C2-safe.** It ends in neither a temporal suffix nor any RFC3339-probe key, so a metric
  object carrying it passes the C2 temporal-suffix probe (verified: `deli-cost` + `deli-cost-flat` fixtures
  C1–C5 ALL PASS, 26 instances each). Never name an additive metric key `*_at`/`since_*`.
- **Float vs int in summary strings.** The do-nothing summary formats thresholds numerically; a metric whose
  ceiling is 16 renders "16.0", so the runner's string assertions must match "16.0"/"8.0" (not "16"/"8").
  This is a test-authoring nuance, not an engine defect.
- **Reuse the closure, don't re-derive.** `_forecast_closure` remains the single source; Q3/Q6/Q8 agree by
  construction (identical projection, threshold, crossing, direction). `render_cockpit_s7l` needed no change
  (its do-nothing line reads the summary generically).
- **`relabel_to` relocation.** The new lower-is-better orgs own clean `metric://deli-cost/*` and
  `metric://deli-cost-flat/*` namespaces + distinct fixtures.

## Assumptions that mattered
- The higher-is-better default == the Sprint-21 test exactly; nothing changes for an org that records a
  series but no direction (documented). Treating an unrecorded-direction COST series as higher-is-better is
  the safe deterministic default (the alternative — guessing the direction — would invent data, out of
  scope).
- The do-nothing baseline is the `unresolved`/`do-nothing` option in `cfg["options"]` (the floor-gated-exempt
  baseline from Sprint 13), priced on_target=False when crossed in either orientation.
- The projections/expected-impact derive from recorded series values + the recorded direction only
  (no wall-clock, no invented number).

## What the sprint gained
- `adjudication_engine.py`: `_forecast_closure` extended to read the recorded `direction` (default
  higher-is-better), compute `worst`/`crossing`/summary per direction, and carry the additive `direction`
  key on the closure/`q6`/`q8["forecast"]`/`do_nothing`. Frozen functions untouched.
- `run_forecast_direction_demo.py` (exit 0) proves the ≥4/5-org directional closure + agreement +
  determinism + no §6 overrule + byte-identical higher-is-better default + no wall-clock; the new
  lower-is-better fixtures pass the Sprint-0 C1–C5 conformance.
- Docs: `docs/ENGINE-FORECAST-DIRECTION.md` (new), additive Sprint-22 note in
  `docs/ENGINE-FORECAST-ACTION.md`, `instances/README.md` (Sprint-22 entry), STRESS-TEST "Update after
  Sprint 22", `references/forecast-direction-closure.md` (new) + additive note in
  `references/forecast-action-closure.md`.

## Honest §16 verdict
**For an org that records a series + its metric's `direction`, the loop Q6→Q3→Q8 is now closed as data in
BOTH directions.** The deterministic projection (last actual + mean delta) becomes prioritized attention on
Q3 when it crosses the recorded threshold in either orientation (a rate/quality metric falling below its
target; a cost/latency/defect/risk metric rising above its ceiling), and Q8/the trade-off price the
do-nothing baseline from that same projection truthfully. The Q8 recommendation is unchanged; the
determination stays the §6 human's `determination_policy` call; S5 alone moves Trust. **What is still not
derivable:** an org that has NOT recorded a series cannot be forced to forecast or to produce a
forecast-driven attention/cost — the cockpit reports the recorded reality, it does not manufacture certainty
(correct). A richer/adaptive forecast model remains out of scope of the honest, deterministic, ~$0 stance.

## No spec change
No normative gap surfaced; SPEC stays v0.22, 49 `$defs`, schema JSON hash `7fc38c8c…`, `ros/` untouched,
only catalog URI schemes (`metric://` a first-class noun; `direction` an additive field — no new noun).