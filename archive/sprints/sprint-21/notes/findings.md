# Sprint 21 — findings

Date: 2026-09-01. Sprint: close the honest frontier Sprint 20 disclosed — the recorded Q6 forecast is
COMPUTED and RENDERED but not CONNECTED to the org's decision surface — by making the recorded forecast
DRIVE the §7L Q3 attention and the Q8 expected-impact / trade-off do-nothing baseline, deterministically
and data-only, with the honest no-data fallback unchanged.

## The residual seam being closed
Sprint 20's `notes/findings.md` ("Residual seams") was explicit: **the Q6 projection was computed and
rendered but not connected to the org's decision surface** — a projected deterioration ("if nothing
changes") did not by itself change §7L Q3 attention or the Q8 expected-impact / trade-off do-nothing
cost, even though §7K.1's Decision→Expected→Variance→WHY loop and §7J.5 attention exist precisely to turn
a measured/forecast gap into prioritized action. Sprint 21 closes a bounded slice of that seam.

## Decisions taken
- **The recorded forecast now drives attention + the do-nothing expected-impact, all from the SAME
  recorded `metric://` series + `forecast_metric`.** A new `_forecast_closure(cfg, sub)` is computed
  ONCE in `cockpit_s7l` and drives Q3, Q6, and Q8 so the three questions agree by construction
  (identical projection, threshold, crossing). This is a strict additive extension of the Sprint-18/20
  engine line.
- **Threshold rule (deterministic, recorded-data only).** The recorded threshold resolves in order:
  an explicit `forecast_threshold` additive field on the `metric://` object → the metric's own `target`
  → the last recorded `actual` (so a targetless declining series still flags). Crossing, for a
  higher-is-better rate metric, is `min(projection) < threshold` — the "do nothing and it gets worse"
  condition.
- **Q3 = attention, never an auto-pick.** A recorded series that crosses gains a `{"tag": "forecast", …}`
  Q3 item; a flat/above-target recorded series adds none; a no-data org keeps today's Q3 exactly.
- **Q8 / trade-off price the do-nothing baseline.** Additive `q8["forecast"]` + `q8["do_nothing_expected_impact"]`
  (baseline, `priced`, `on_target`, summary) + `q7["tradeoff_do_nothing_impact"]`, all derived from that
  same projection. The **Q8 recommendation is UNCHANGED** — the forecast prices attention + do-nothing
  but never overrules the §6-floor-gated machine-eligible best (asserted equal to `cockpit_q7q8`'s for
  every org).

## The ≥3-org proof
`run_forecast_action_demo.py` (exit 0 = ALL PASS) drives three orgs on fresh Substrates:
- `deli-forecast` (deteriorating) — recorded actuals 0.92/0.90/0.87/0.86, target 0.95 → projection
  [0.84,0.82,0.8] crosses → **Q3 `[forecast]` item** + Q8 `do_nothing_expected_impact` on_target=False,
  gap 0.15.
- `deli-forecast-flat` (on-target control) — recorded actuals 0.96/0.97/0.96/0.96, target 0.95 →
  projection [0.96,0.96,0.96] stays above → **no forecast attention**, do-nothing priced on_target=True.
- `deli` (no data) — **unchanged** Q3/Q8/trade-off fallback (no forecast item, no do-nothing fields).

## Corrections / guardrails hit
- **Q3 evidence string.** Making the `.q3.evidence` string mention the forecast unconditionally would have
  changed the no-data org's `q3` dict → I keyed it to whether a forecast item was actually appended, so
  a no-data org's `q3.evidence` is byte-identical to Sprint 20.
- **Threshold key C2-safety.** `forecast_threshold` does not end in a temporal suffix, so a metric object
  carrying it passes the C2 RFC3339/temporal-key probe (verified: all recorded-org fixtures pass C1–C5).
- **Reuse the closure, don't re-derive.** Replacing the inline Q6 forecast block with `fca["q6"]` (computed
  once up front) guarantees Q3/Q6/Q8 agree by construction and avoids double-computing `forecast_metric`.
- **`relabel_to` relocation.** The flat control needed its OWN label (`deli-forecast-flat`) and series URI
  so it owns clean `metric://deli-forecast-flat/*` URIs and its fixtures are distinct.
- **deli/cove byte-identity.** The engine demo's deli/cove fixtures carry **no** Sprint-21 closure keys
  (they record no series): verified they are unchanged up to the clock. The no-data `deli` in the runner is
  asserted to have no forecast/do-nothing fields and the Sprint-20 fallback.

## Assumptions that mattered
- The crossing test uses `min(projection) < threshold` (higher-is-better rate). A metric where lower ranks
  (e.g. cost) would need the inverse; this sprint standardizes on the rate/quality case and documents the
  rule plainly. The runner's two recorded orgs are both "higher-is-better on-time rate" so the test is
  exercised consistently.
- The do-nothing baseline is the `unresolved`/`do-nothing` option in `cfg["options"]` (already the
  floor-gated-exempt baseline from Sprint 13).

## What the sprint gained
- `_num` + `_forecast_closure` (append); `cockpit_s7l` `.q3` forecast-attention append + `.q6` reuse of the
  closure + additive `q7`/`q8` enrichment of the Sprint-18 dicts; `render_cockpit_s7l` Q3-tag + Q8
  do-nothing lines. Frozen functions untouched.
- `run_forecast_action_demo.py` (exit 0) proves the ≥3-org closure + agreement + determinism + no §6
  overrule + no wall-clock; the new-recorded-org fixtures pass the Sprint-0 C1–C5 conformance.
- Docs: `docs/ENGINE-FORECAST-ACTION.md` (new), additive Sprint-21 note in `docs/ENGINE-FORECAST-CAPACITY.md`,
  `instances/README.md` Sprint-21 entry, STRESS-TEST "Update after Sprint 21".

## Honest §16 verdict
**For an org that records a series, the loop Q6→Q3→Q8 is now closed as data.** Q6 projects the
deterministic "if nothing changes" trajectory; Q3 turns a projection that crosses a recorded threshold
into a prioritized attention item (tagged `forecast`); Q8/the trade-off price the do-nothing baseline from
that same projection — all from recorded data, never the wall-clock. The Q8 recommendation is unchanged;
the determination stays the §6 human's `determination_policy` call; S5 alone moves Trust. **What is still
not derivable:** an org that has NOT recorded a series cannot be forced to forecast or to produce a
forecast-driven attention item/cost — the cockpit reports the recorded reality, it does not manufacture
certainty (correct behavior). A richer/adaptive forecast model (beyond the deterministic last-actual +
mean-delta projection) remains out of scope of the honest, deterministic, ~$0 stance.

## No spec change
No normative gap surfaced; SPEC stays v0.22, 49 `$defs`, schema JSON hash `7fc38c8c…`, `ros/` untouched,
only catalog URI schemes (`metric://` a first-class noun; `forecast_threshold` an additive field — no new
noun).