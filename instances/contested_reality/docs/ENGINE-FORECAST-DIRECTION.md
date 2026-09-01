# ENGINE-FORECAST-DIRECTION — directional forecast→attention→expected-impact (Sprint 22)

**Scope.** Sprint 21 closed the forecast→attention→expected-impact seam (the recorded Q6 forecast now
DRIVES §7L Q3 attention and the Q8/trade-off do-nothing baseline), but its own findings (`sprint-21/
notes/findings.md`, "Assumptions that mattered") disclosed the next honest frontier: **the crossing test
was hardcoded to the higher-is-better / rate case** (`min(projection) < threshold`). A metric where
"lower is better" — a cost, latency, defect rate, or risk — would NOT flag as forecast-driven attention
when it deteriorates by RISING above a recorded ceiling. **Sprint 22 closes that bounded slice**: it makes
the crossing **direction a recorded, additive parameter**, so the same generic, data-only closure path
flags forecast-driven Q3 attention and prices the Q8 do-nothing expected-impact for BOTH directions,
deterministically and data-only, with the Sprint-21 higher-is-better behavior kept **byte-identical by
default**.

This document states the directional crossing rule, how the do-nothing baseline is priced in each
orientation, the honest no-data fallback, how it is generic + additive, the ≥4-org proof, and the §16
verdict.

---

## 1. The directional crossing rule (which recorded series becomes a Q3 attention item)

From a recorded `metric://` realized-vs-expected **series**, its recorded **`direction`**, and the
Sprint-20 `forecast_metric` projection:

- **Direction** — an additive `direction` field on the `metric://` object, defaulting to
  **`"higher-is-better"`** (normalized defensively; an unrecorded / unknown value behaves as
  higher-is-better). An org whose metric is a cost/latency/defect/risk records
  **`direction: "lower-is-better"`**.
- **Threshold** — resolved from the recorded data, unchanged from Sprint 21:
  1. an explicit **`forecast_threshold`** additive field on the `metric://` object (a C2-safe key);
  2. else the metric's own **`target`**;
  3. else the **last recorded `actual`**.
- **Worst** — direction-dependent: higher-is-better → `min(projection)`; lower-is-better → `max(projection)`.
- **Crossing** — direction-dependent, the "do nothing and it gets worse" condition:
  - higher-is-better (rate/quality): `min(projection) < threshold` — a projection falling **below**
    a target is bad **(Sprint-21 unchanged)**;
  - lower-is-better (cost/latency/defect/risk): `max(projection) > threshold` — a projection rising
    **above** a ceiling is bad.
- **Forecast-driven attention (Q3, §7J.5):** when a recorded series exists AND its projection crosses,
  `cockpit_s7l.q3.prioritized` gains an item, worded per direction:
  - higher-is-better: `{"item": <metric_uri>, "why": "forecast: projected to fall below <threshold>
    (<src>) — worst <min> at period <H>", "tag": "forecast"}`;
  - lower-is-better: `{"item": <metric_uri>, "why": "forecast: projected to rise above <threshold>
    (<src>) — worst <max> at period <H>", "tag": "forecast"}`.
- A recorded series that does **not** cross (flat / above its target for higher-is-better, at/below its
  ceiling for lower-is-better) produces **no** forecast attention item.

This is **attention**, never an auto-pick. The Q8 recommendation stays the §6-floor-gated
machine-eligible best; the determination stays the §6 human's `determination_policy` call.

## 2. How the do-nothing baseline is priced (Q8 + the trade-off) in each orientation

When a recorded series exists, the engine adds — to the Sprint-18 `base`-returned `q7`/`q8` dicts, as
**additive fields** — a projected-cost do-nothing expected-impact derived **only** from that same
deterministic projection:

- `q8["forecast"]` — `{projections, threshold, source, worst, crossing, direction}`;
- `q8["do_nothing_expected_impact"]` — `{baseline: <unresolved/do-nothing option>, priced: True,
  on_target: bool, summary: <human phrase>, metric: <uri>, direction: <str>}`;
- `q7["tradeoff_do_nothing_impact"]` — the same summary.

The summary is truthful to the recorded projection and the **orientation** of the gap:
- **higher-is-better crossing** → `"forecast-driven do-nothing cost: <metric> projects to worst <min>
  (period <H>) below recorded <src> <threshold> by <gap> — doing nothing lets the recorded trend
  deteriorate"` (`on_target: False`, gap = threshold − worst);
- **lower-is-better crossing** → `"forecast-driven do-nothing cost: <metric> projects to worst <max>
  (period <H>) above recorded <src> <threshold> by <gap> — doing nothing lets the recorded trend
  deteriorate"` (`on_target: False`, gap = worst − threshold);
- **on-target** → per direction, `"on-target: <metric> projection stays at/above recorded <src>
  <threshold> (worst <min>) — no forecast-driven cost to doing nothing"` (higher) or `"… stays at/below
  recorded <src> <threshold> (worst <max>) — …"` (lower), `on_target: True`.

**No §6 overrule:** the forecast prices attention + the do-nothing baseline; it never changes the Q8
recommendation (asserted equal to `cockpit_q7q8`'s for every org) and never auto-picks an action.

## 3. The honest no-data fallback (unchanged)

An org with **no recorded realized-vs-expected series** keeps today's cockpit exactly: `q3` has no
forecast item, `q6` says *"cannot forecast from recorded data"*, and `q7`/`q8` carry **no**
`forecast` / `do_nothing_expected_impact` / `tradeoff_do_nothing_impact` fields — byte-identical to
Sprint 20/21's fallback.

## 4. What `cockpit_s7l` now reports, per org

Verified output of `run_forecast_direction_demo.py` (from `instances/contested_reality`, exit 0 = ALL PASS):

| org | direction (recorded) | recorded series | Q3 forecast item? | Q8 do-nothing expected-impact |
|---|---|---|---|---|
| `deli-forecast` (deteriorating) | `higher-is-better` (default) | actuals 0.92/0.90/0.87/0.86, target 0.95 → projection [0.84,0.82,0.8] | **YES** tagged `forecast` ("projected to fall below 0.95 (target) — worst 0.8 at period 3") | **forecast-driven cost** (on_target=False), gap 0.15 — byte-identical to Sprint 21 |
| `deli-forecast-flat` (on-target control) | `higher-is-better` (default) | actuals 0.96/0.97/0.96/0.96, target 0.95 → projection [0.96,0.96,0.96] | **NO** | **on-target** (on_target=True) — byte-identical to Sprint 21 |
| `deli-cost` (RISING cost) | `lower-is-better` (explicit) | actuals 12/14/16/18 ms, ceiling/target 16 → projection [20,22,24] | **YES** tagged `forecast` ("projected to rise above 16.0 (target) — worst 24.0 at period 3") | **forecast-driven cost** (on_target=False), gap 8.0 in the RISING orientation ("above recorded target 16.0 by 8.0") |
| `deli-cost-flat` (below-ceiling control) | `lower-is-better` (explicit) | actuals 8/9/8/8 ms, ceiling/target 10 → projection [8,8,8] | **NO** | **on-target** (on_target=True), "stays at/below recorded target 10.0 (worst 8.0)" |
| `deli` (no data) | n/a | none | **NO** | **absent** (fallback unchanged) |

Abridged render (the rising-cost org):

```
Q3. what matters?  prioritized attention (3): …; metric://deli-cost/m-latency [forecast] —
    forecast: projected to rise above 16.0 (target) — worst 24.0 at period 3
Q6. what if we do nothing?  … period 1 -> 20.0; period 2 -> 22.0; period 3 -> 24.0 …
Q8. what should we do?  recommendation partial-settlement … -> determination partial-settlement
    trade-off / do-nothing expected-impact: forecast-driven do-nothing cost: metric://deli-cost/
    m-latency projects to worst 24.0 (period 3) above recorded target 16.0 by 8.0 — doing nothing lets
    the recorded trend deteriorate (baseline unresolved, priced=True, on-target=False)
```

## 5. How it is generic + additive

- **One engine function, no per-org Python.** `_forecast_closure(cfg, sub)` already reads the recorded
  `metric://` series + `forecast_metric`; Sprint 22 adds reading the metric's additive `direction`
  field (default `"higher-is-better"`), so the SAME generic path serves any org that records its
  metric's direction. `cockpit_s7l` computes it ONCE for Q3/Q6/Q8, so they agree by construction.
- **Additive only.** The ONLY engine file touched is `adjudication_engine.py`'s `_forecast_closure`
  (the worst/crossing/summary block, extended to branch on `direction`, plus the additive
  `direction` key on the closure/`q6`/`q8["forecast"]`/`do_nothing` dicts). The **frozen functions**
  (`reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/`rank`/`machine_eligible_best`/
  `render_tradeoff`/`cockpit_q7q8`) are **untouched**. **49 `$defs` / URI cap / SPEC v0.22** intact;
  `direction` is an **additive field** on `metric://` (**no new noun**); `ros/` untouched.
- **Byte-identical default.** The default direction == `"higher-is-better"` reproduces the Sprint-21
  higher-is-better strings exactly (the two `deli-forecast`/`deli-forecast-flat` orgs, recorded WITHOUT
  a `direction` field, are asserted byte-identical to Sprint 21).
- **Deterministic.** No wall-clock anywhere: projection, threshold, worst, crossing, and do-nothing
  summary are pure functions of the recorded series values + the recorded direction. Identical on re-run
  (asserted for all five orgs), and `q8["forecast"]` agreement with `forecast_metric` + hand-computed
  projections is asserted.

## 6. The ≥4/5-org proof (real, exit-0)

`run_forecast_direction_demo.py` (exit 0 = ALL PASS) drives five orgs on fresh Substrates and asserts:
(a) **every org** keeps the full §7L Q1–Q10 cockpit with data evidence;
(b) **higher-is-better byte-identical to Sprint 21**: `deli-forecast` (no explicit direction → default)
   Q3 `[forecast]` item + crossing do-nothing cost and `deli-forecast-flat` (default) NO forecast item +
   on-target do-nothing, strings asserted exactly equal to Sprint 21;
(c) the **lower-is-better** `deli-cost` (explicit `direction`) Q3 carries the `[forecast]` item
   ("projected to rise above …") + Q8/trade-off prices do-nothing in the **rising** orientation
   (on_target=False, "above recorded target 16.0 by 8.0"), `worst == max(projection)`,
   projection == hand-computed [20.0,22.0,24.0] == `forecast_metric`; its `direction` is recorded as an
   additive field on the `metric://` object;
(c2) the **lower-is-better control** `deli-cost-flat` (projection stays below ceiling, [8,8,8]) adds **no**
   forecast attention + prices do-nothing on-target ("stays at/below …");
(d) the **no-data** `deli` keeps today's Q3/Q8/trade-off (no forecast item, no forecast/do-nothing fields);
(e) **determinism** on re-run (dict + render identical for all five);
(f) **agreement**: `q8["forecast"]` projections == `forecast_metric` == hand-computed on all four recorded
   orgs;
(g) **no §6 overrule**: `q8.recommendation` unchanged by the forecast (equal to `cockpit_q7q8` for every org);
(h) every projection derived from recorded series values only (no wall-clock).

It also runs the two new lower-is-better fixtures through the Sprint-0 conformance (C1–C5, frozen schema).

## 7. Verification / non-regression (all exit 0)

- New runner: `python3 run_forecast_direction_demo.py` → **ALL PASS** (from `instances/contested_reality`).
- New lower-is-better conformance: the Sprint-0 venv over `artifacts/adjudication/fixtures/deli-cost` and
  `…/deli-cost-flat` → C1–C5 ALL PASS (26 instances each, 49 `$defs`; the additive `direction` field
  survives the C2 temporal-suffix / RFC3339 probe).
- Existing demos re-verified ALL PASS: the 12 C-R runners + `run_cockpit_s7l_demo` +
  `run_forecast_capacity_demo` + the new Sprint-21 `run_forecast_action_demo` (byte-identical after the
  engine change) ; `conformance_adjudication.py` **16 labels** C1–C5 ALL PASS + the 4 other C-R conformances.
- Sector `build_all.py` + `conformance_all.py`, S5 reference demo + conformance, agent demo +
  conformance — ALL PASS.
- `deli`/`cove` **byte-identical** up to the clock; the two Sprint-21 recorded orgs' Q3/Q8 unchanged
  (direction default). Only `.py` code changed: `adjudication_engine.py` (+ the new runner). `ros/` + schema
  untouched.
- Schema hash `7fc38c8c…`, **49 `$defs`**, **SPEC v0.22**, only catalog URI schemes — no new noun.

## 8. Honest §16 verdict — does the forecast→attention→expected-impact closure now serve BOTH directions as data?

**Yes for the recorded-data case, as data, in both orientations, with the honest no-data fallback intact.**
Where an org records a realized-vs-expected `metric://` series **and** its `direction` (default
`higher-is-better`), the Sprint-22 engine connects **Q6** → **Q3** → **Q8** for BOTH metric directions:
a rate/quality metric (higher-is-better) that is projected to fall below its recorded threshold, and a
cost/latency/defect/risk metric (lower-is-better) that is projected to rise above its recorded ceiling,
each become a **prioritized attention item** (§7J.5, "do nothing and it gets worse"), and **Q8**/the
trade-off price the **do-nothing baseline** from that same projection **in the correct orientation**
(below-target vs above-ceiling) — all from recorded data, never the wall-clock. The **Q8 recommendation is
unchanged**: the forecast prices attention and the do-nothing cost but never overrules the §6-floor-gated
machine-eligible best. The higher-is-better default keeps Sprint 21 byte-identical.

**What is still not derivable:** an org that has **not** recorded a series (or fails to record its metric's
direction) cannot be made to forecast or to produce a forecast-driven attention item/cost in the opposite
orientation — the cockpit reports the recorded reality, it does not manufacture certainty (correct
behavior). A richer/adaptive forecast model (beyond the deterministic last-actual + mean-delta projection)
remains out of scope of the honest, deterministic, ~$0 stance.

*(Evidence: all assertions are real exit-0 output from `run_forecast_direction_demo.py` + the Sprint-0
conformance over the new orgs' fixtures + the full non-regression + conformance suite; SPEC v0.22,
49 `$defs`, `ros/` + schema untouched, no new noun.)*

---

## Update after Sprint 23 — the do-nothing expected-impact is now priced as a recorded-variance band

Sprint 23 adds the next honest slice on top of this directional closure: when the recorded `metric://`
series' last point carries a numeric `variance`, the **do-nothing expected-impact is priced as a
projected BAND** (worst ± the recorded variance as a magnitude → `low … high`), surfaced on the
closure, `q8["forecast"]`, and `do_nothing_expected_impact`, and the do-nothing summary + Q3 attention
`why` append an additive phrase naming the band. This is a **recorded-data spread** (the deterministic
worst bounded by the last recorded variance), **NOT a probability/confidence interval**. A series with
no recorded variance — or no series at all — keeps the Sprint-22 single-point/fallback output
**byte-identical**. The `direction` rule, threshold resolution, and the single-point
worst/gap/threshold/crossing/on_target fields are **unchanged**; the band is strictly additive.

## Update after Sprint 24 — the band's variance SOURCE honors the recorded `direction`-agnostic `band_variance`

Sprint 24 makes the band's variance source a **recorded, additive `band_variance` parameter** on the
`metric://` object (absent / `"last"` → the Sprint-23 last-point variance, byte-identical; `"all"` /
`"minmax"` → the recorded whole-series max |variance|), so an org whose spread WIDENED over time can
price the do-nothing band from the recorded worst-case spread. The whole-series band still obeys this
document's directional rule — the band's **worst side** crosses the threshold per the metric's
`direction` (higher-is-better: `low < threshold`; lower-is-better: `high > threshold`) — SIGMA choice
is direction-agnostic but `low`/`high`/`crosses` remain directional. `deli-varmax` (whole-series,
higher-is-better) and `deli-cost` (last-point, lower-is-better) are both proven. Full detail: the
Sprint-24 addendum (§7) in `docs/ENGINE-FORECAST-VARIANCE.md`.
See `ENGINE-FORECAST-VARIANCE.md` (Sprint 23) for the full band rule + §16 verdict.