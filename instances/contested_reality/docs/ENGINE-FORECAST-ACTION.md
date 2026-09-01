# ENGINE-FORECAST-ACTION — recorded forecast → Q3 attention → Q8 expected-impact closure (Sprint 21)

**Scope.** Sprint 20 made the recorded Q6 forecast (and Q9 capacity) answered **AS DATA** via
`forecast_metric` + a recorded `metric://` realized-vs-expected series — but its own findings disclosed
(the "Residual seams" paragraph) the next honest frontier: **the Q6 projection was COMPUTED and RENDERED
but not CONNECTED to the org's decision surface**. A projected deterioration ("if nothing changes") did
not by itself change §7L **Q3** attention or the **Q8** expected-impact / trade-off "do-nothing" cost,
even though §7K.1's Decision→Expected→Variance→WHY loop and §7J.5 attention exist precisely to turn a
measured/forecast gap into prioritized action. **Sprint 21 closes a bounded slice of that seam**: the
RECORDED forecast now **drives** the Q3 attention and the Q8 expected-impact / do-nothing baseline, all
deterministically and data-only — with the honest no-data fallback unchanged.

This document states the threshold rule that flags a forecast-driven Q3 attention item, how the
do-nothing baseline is priced on Q8/the trade-off, the honest no-data fallback, how it is generic +
additive, the ≥3-org proof, and the §16 verdict.

---

## 1. The threshold rule (which recorded series becomes a Q3 attention item)

From a recorded `metric://` realized-vs-expected **series** and the Sprint-20 `forecast_metric` projection:

- **Threshold** — resolved from the recorded data, in order:
  1. an explicit **`forecast_threshold`** additive field on the `metric://` object (a C2-safe key — no
     temporal suffix);
  2. else the metric's own **`target`** (already a recorded field on the series);
  3. else the **last recorded `actual`** (so a targetless *declining* series still flags).
- **Crossing** — for a higher-is-better rate metric: `min(projection_1..horizon) < threshold`. That is the
  "do nothing and it gets worse" condition.
- **Forecast-driven attention (Q3, §7J.5):** when a recorded series exists AND its projection crosses,
  `cockpit_s7l.q3.prioritized` gains an item:
  `{"item": <metric_uri>, "why": "forecast: projected to fall below <threshold> (<src>) — worst <min>
  at period <H>", "tag": "forecast"}`.
- A recorded series that does **not** cross (flat / above-target) produces **no** forecast attention item.

This is **attention**, never an auto-pick. The Q8 recommendation stays the §6-floor-gated
machine-eligible best; the determination stays the §6 human's `determination_policy` call.

## 2. How the do-nothing baseline is priced (Q8 + the trade-off)

When a recorded series exists, the engine adds — to the Sprint-18 `base`-returned `q7`/`q8` dicts, as
**additive fields** — a projected-cost do-nothing expected-impact derived **only** from that same
deterministic projection:

- `q8["forecast"]` — `{projections, threshold, source, worst, crossing}` (agrees with `forecast_metric`
  by construction);
- `q8["do_nothing_expected_impact"]` — `{baseline: <unresolved/do-nothing option>, priced: True,
  on_target: bool, summary: <human phrase>, metric: <uri>}`;
- `q7["tradeoff_do_nothing_impact"]` — the same summary, so the trade-off view carries it too.

The summary is truthful to the recorded projection:
- **crossing** → `"forecast-driven do-nothing cost: <metric> projects to worst <min> (period <H>) below
  recorded <src> <threshold> by <gap> — doing nothing lets the recorded trend deteriorate"`
  (`on_target: False`);
- **on/above target** → `"on-target: <metric> projection stays at/above recorded <src> <threshold>
  (worst <min>) — no forecast-driven cost to doing nothing"` (`on_target: True`).

**No §6 overrule:** the forecast prices attention + the do-nothing baseline; it never changes the Q8
recommendation (asserted equal to `cockpit_q7q8`'s for every org) and never auto-picks an action.

## 3. The honest no-data fallback (unchanged)

An org with **no recorded realized-vs-expected series** keeps today's cockpit exactly: `q3` has no
forecast item (and its `evidence` string is byte-identical), `q6` says *"cannot forecast from recorded
data"*, and `q7`/`q8` carry **no** `forecast` / `do_nothing_expected_impact` / `tradeoff_do_nothing_impact`
fields. The no-data org's Q3/Q8/trade-off are byte-identical to Sprint 20's.

## 4. What `cockpit_s7l` now reports, per org

Verified output of `run_forecast_action_demo.py` (from `instances/contested_reality`, exit 0 = ALL PASS):

| org | recorded series | Q3 forecast item? | Q8 do-nothing expected-impact |
|---|---|---|---|
| `deli-forecast` (deteriorating) | actuals 0.92/0.90/0.87/0.86, target 0.95 → projection [0.84,0.82,0.8] | **YES** tagged `forecast` ("projected to fall below 0.95 (target) — worst 0.8 at period 3") | **forecast-driven cost** (on_target=False), gap 0.15 |
| `deli-forecast-flat` (on-target control) | actuals 0.96/0.97/0.96/0.96, target 0.95 → projection [0.96,0.96,0.96] | **NO** | **on-target** (on_target=True), "no forecast-driven cost" |
| `deli` (no data) | none | **NO** | **absent** (Sprint-20 fallback unchanged) |

Abridged render (deteriorating org):

```
Q3. what matters?  prioritized attention (3): …; metric://deli-forecast/m-on-time [forecast] —
    forecast: projected to fall below 0.95 (target) — worst 0.8 at period 3
Q6. what if we do nothing?  … period 1 -> 0.84; period 2 -> 0.82; period 3 -> 0.8 …
Q8. what should we do?  recommendation partial-settlement … -> determination partial-settlement
    trade-off / do-nothing expected-impact: forecast-driven do-nothing cost: metric://deli-forecast/
    m-on-time projects to worst 0.8 (period 3) below recorded target 0.95 by 0.15 — doing nothing lets
    the recorded trend deteriorate (baseline unresolved, priced=True, on-target=False)
```

## 5. How it is generic + additive

- **One engine function, no per-org Python.** `_forecast_closure(cfg, sub)` reads the recorded
  `metric://` series + `forecast_metric` exactly like the engine reads everything else — from `cfg` +
  the org's own `sub` graph/ledger — and `cockpit_s7l` computes it ONCE for Q3/Q6/Q8 so the three
  questions agree by construction (identical projection, threshold, crossing).
- **Additive only.** The ONLY engine file touched is `adjudication_engine.py`: a `_num` helper +
  `_forecast_closure` (append), an in-place `.q3` append, a `.q6` that reuses the closure, additive
  `q7`/`q8` enrichment, and `render_cockpit_s7l` Q3-tag + Q8 do-nothing lines. The **frozen functions**
  (`reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/`rank`/`machine_eligible_best`/
  `render_tradeoff`/`cockpit_q7q8`) are **untouched** — the closure enriches the `base`-returned dicts,
  it never rewrites `cockpit_q7q8`. **49 `$defs` / URI cap / SPEC v0.22** intact; `metric://` a
  first-class catalog noun and `forecast_threshold` an additive envelope field — **no new scheme**;
  `ros/` untouched.
- **Deterministic.** No wall-clock anywhere: projection, threshold, crossing, and do-nothing summary are
  pure functions of the recorded series values. The cockpit dict + rendered line are identical on re-run
  (asserted for all three orgs), and `q8["forecast"]` agreement with `forecast_metric` + a hand-computed
  projection is asserted.

## 6. The ≥3-org proof (real, exit-0)

`run_forecast_action_demo.py` (exit 0 = ALL PASS) drives three orgs on fresh Substrates and asserts:
(a) **every org** keeps the full §7L Q1–Q10 cockpit with data evidence;
(b) the **deteriorating** `deli-forecast` gains a `forecast`-tagged Q3 item + a projected (crossing,
   on_target=False) do-nothing cost, its projection == the hand-computed [0.84,0.82,0.8] and
   `forecast_metric` (agreement);
(c) the **on-target** `deli-forecast-flat` adds **no** forecast attention, prices do-nothing as on-target
   (on_target=True), projection == hand-computed [0.96,0.96,0.96];
(d) the **no-data** `deli` keeps today's Q3/Q8/trade-off (no forecast item, no forecast/do-nothing fields);
(e) **determinism** on re-run (dict + render identical for all three);
(f) **agreement**: `q8["forecast"]` projections == `forecast_metric` == hand-computed on the recorded orgs;
(g) **no §6 overrule**: `q8.recommendation` unchanged by the forecast (equal to `cockpit_q7q8` for every org);
(h) every projection derived from recorded series values only (no wall-clock).

It also runs the new-recorded-org fixtures through the Sprint-0 conformance (C1–C5, frozen schema).

## 7. Verification / non-regression (all exit 0)

- New runner: `python3 run_forecast_action_demo.py` → **ALL PASS** (from `instances/contested_reality`).
- New-recorded-org conformance: the Sprint-0 venv over `artifacts/adjudication/fixtures/deli-forecast`
  and `…/deli-forecast-flat` → C1–C5 ALL PASS (26 instances each, 49 `$defs`).
- Existing demos re-verified ALL PASS: all 12 C-R runners + `run_cockpit_s7l_demo` + the 4 prior CR
  demos + `run_forecast_capacity_demo`; `conformance_adjudication.py` **16 labels** C1–C5 ALL PASS.
- Sector `build_all.py` + `conformance_all.py`, S5 reference demo + conformance, agent demo +
  conformance — ALL PASS.
- `deli`/`cove` **byte-identical** up to the clock: the engine demo's deli/cove fixtures carry **no**
  Sprint-21 closure keys (they have no recorded series), so they are unchanged by this sprint.
- Schema hash `7fc38c8c…`, **49 `$defs`**, **SPEC v0.22**, `ros/` untouched, only catalog URI schemes —
  no new noun.

## 8. Honest §16 verdict — does the recorded-data forecast now close the Q6→Q3→Q8 loop?

**Yes for the recorded-data case, as data, with the honest no-data fallback intact.** Where an org records
a realized-vs-expected `metric://` series, the Sprint-21 engine connects all three: **Q6** projects the
deterministic "if nothing changes" trajectory (`forecast_metric`), **Q3** turns a projection that crosses
a recorded threshold into a **prioritized attention item** (tagged `forecast` — "do nothing and it gets
worse" is now attention, §7J.5), and **Q8**/the trade-off price the **do-nothing baseline** from that same
projection — all from recorded data, never the wall-clock. The **Q8 recommendation is unchanged**: the
forecast prices attention and the do-nothing cost but never overrules the §6-floor-gated
machine-eligible best, and the determination stays the §6 human's `determination_policy` call.

**What is still not derivable:** an org that has **not** recorded a series cannot be made to forecast or
to produce a forecast-driven attention item or cost — the cockpit reports the recorded reality, it does
not manufacture certainty (correct behavior). A richer/adaptive forecast model (beyond the deterministic
last-actual + mean-delta projection) remains out of scope of the honest, deterministic, ~$0 stance. The
forecast-to-action seam is now **data-grounded for any org that records the data**, and truthful about the
no-data case.

*(Evidence: all assertions are real exit-0 output from `run_forecast_action_demo.py` + the Sprint-0
conformance over the new orgs' fixtures + the full non-regression + conformance suite; SPEC v0.22,
49 `$defs`, `ros/` + schema untouched, no new noun.)*