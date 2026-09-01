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
## 9. Update after Sprint 25 — Q9 capacity-attention from the horizon-wide band

Sprint 25 adds an **additive `band_capacity_attention`** to `q9` when a projected band exists AND the
recorded threshold is numeric: `{flag, why, low, high, crosses}`. The flag is data-only — whether the
record-wide HORIZON range (the same recorded sigma applied to every projection period → `band_horizon`)
signals the recorded threshold (higher-is-better: `low < threshold`; lower-is-better: `high >
threshold`). `why` references any RECORDED `capacity` (value/unit/load) on the authority object
WITHOUT inventing or mutating it; if none is recorded the flag derives from the band + threshold alone.
A no-band / no-variance / no-data org carries no `band_capacity_attention` key (byte-identical). This
extends the Sprint-20 recorded-capacity reporting with a flag/reason from the recorded band — it never
fabricates a capacity NUMBER. `run_forecast_horizon_demo.py` proves it, incl. `deli-varmax-cap` whose
`why` references a recorded capacity while leaving the capacity object intact. SPEC v0.22, 49 `$defs`,
`ros/` untouched.
## 10. Update after Sprint 26 — Q9 capacity-planning attention (a derived REASON, never a directive)

Sprint 26 adds an **additive `capacity_planning_attention` = {flag, why}** to `q9`, emitted ONLY where
the org RECORDS a numeric `capacity` on its authority object AND a band + numeric threshold exist. ONE
deterministic rule from recorded numbers only:
- **at-capacity** when the recorded `load >= 1.0`;
- **deficit** when the horizon band's worst-side magnitude (band_horizon low for higher-is-better, high
  for lower-is-better) reaches/exceeds the recorded capacity VALUE;
- otherwise **headroom**.
`why` states the recorded capacity value/unit/load and the horizon-wide band, and labels
headroom/at-capacity/deficit as a derived REASON — it NEVER invents a capacity figure and NEVER issues a
directive. An org that records no capacity (or has no band) carries NO `capacity_planning_attention` key
(byte-identical superset of Sprint 25); the Sprint-25 `band_capacity_attention` flag is untouched. Proof:
`run_forecast_horizon2_demo.py` — `deli-varmax-cap` (recorded capacity 500.0 resolutions/day, load 0.72,
horizon band 0.62…1.02) yields `{flag: False, why: "… derived headroom from recorded numbers only …"}`
while `deli-forecast`, `deli-varmax`, `deli-flat2`, and no-data `deli` carry no such key. SPEC v0.22, 49
`$defs`, `ros/` untouched.
## 11. Update after Sprint 27 — the recorded capacity reaches the Q7/Q8 trade-off as a data-only REASON

Sprint 26's own finding (its `notes/findings.md`, "Open issues / next work") was honest that the Q9
`capacity_planning_attention` REASON **did not connect to the §7L Q7/Q8 trade-off** — an org that
recorded a capacity deficit / at-capacity reason still saw the SAME machine-eligible options and the
SAME Q8 recommendation as if its capacity were unbounded. **Sprint 27 closes that bounded slice
additively**: where the org records a numeric `capacity` AND a band + numeric threshold exist (the
same condition that emits the Q9 reason), `cockpit_s7l` adds an additive **`capacity_constraint`**
block on BOTH **`q7`** (the trade-off) and **`q8`** (next to `do_nothing_expected_impact`), as a
**parallel block** — the frozen `rank`-owned `options`/`tradeoff` bytes are untouched (the prompt's
preferred decision, documented in `sprints/sprint-27/plan.md`):

- `recorded_capacity` — the recorded capacity value/unit/load AS RECORDED (never invented);
- `horizon_band` — the record-wide `band_horizon` {low, high} on the closure;
- `reason` — ONE deterministic label from recorded numbers only, via the **shared** `_capacity_reason`
  helper (headroom / at-capacity when recorded load >= 1.0 / deficit when the horizon band's worst-side
  magnitude reaches/exceeds the recorded capacity value) — so **the Q8 `reason` always equals the Q9
  `capacity_planning_attention` label BY CONSTRUCTION** (the Sprint-26 Q9 block was refactored to call
  the same helper; output byte-identical);
- `flag` — True iff not headroom;
- `options_flagged` — a map marking the capacity-consuming (non-baseline) options **`capacity_risk`**
  when the reason is not headroom. NEVER `capacity_infeasible`: no per-option capacity requirement is
  ever recorded, so infeasibility is never derivable. The baseline (`do-nothing`/`unresolved`) is
  never flagged (consumes no capacity). In headroom, `{}` (no option flagged);
- `note` — states it is never an invented figure, never a directive, never a removal; the Q8
  recommendation is UNCHANGED; the §6 human always rules.

It **never removes an option, never changes `machine_eligible_best`/Q8, never overrules the §6 human**,
and never invents a capacity figure or a per-option requirement. The default and every no-capacity /
no-band / no-data org carry **NO** `capacity_constraint` key (byte-identical superset of Sprint 26).
Proof: `run_forecast_horizon3_demo.py` — `deli-varmax-cap` (recorded capacity 500.0 resolutions/day,
load 0.72, horizon band 0.62…1.02) carries `capacity_constraint` on Q7 and Q8 with
`{recorded_capacity: "500.0 resolutions/day (load 0.72)", horizon_band: {0.62, 1.02}, reason:
"headroom", flag: False, options_flagged: {}}` (headroom: load < 1.0 AND horizon worst-side 0.62 <
capacity 500.0 → **NO option marked infeasible**), while `deli-forecast`, `deli-varmax`, `deli-flat2`,
no-data `deli` carry no such key; for every org Q7 `options` + Q8 `recommendation`/`machine_eligible_best`
are asserted EQUAL to `cockpit_q7q8` (no §6 overrule, no re-rank). SPEC v0.22, 49 `$defs`, no new noun
(`capacity_constraint`/`recorded_capacity`/`horizon_band`/`reason`/`options_flagged`/`note`/`flag` are
additive, C2-safe — no `at|time|deadline|expires|expiry|effective|due|since` suffix), `ros/` untouched.

## 12. Update after Sprint 28 — the capacity marker is now PROVEN AT ITS LIMIT (at-capacity / deficit)

Sprint 27's own finding (its `notes/findings.md`, "Open issues / next work") was honest that the
`capacity_constraint` marker was proven end-to-end **ONLY in headroom** (`deli-varmax-cap` →
`reason: "headroom", options_flagged: {}`); its at-capacity / deficit branches existed in the shared
`_capacity_reason` helper but were **never exercised on a real org** (only helper-level), so (a) the
`capacity_risk` flagging, (b) the derived reason itself, and (c) the honest "the SAME machine-eligible
options and the SAME Q8 recommendation remain, correctly, with only a capacity_risk label" were
unproven AS DATA on a living §7L Q1–Q10 cockpit.

**Sprint 28 closes that bounded slice with recorded data + a runner ONLY — no engine change.** The
engine already implements all three branches of `_capacity_reason` and the Q7/Q8 `capacity_constraint`
block; Sprint-27 simply never drove the non-headroom orgs. Sprint 28 adds two NEW orgs that RECORD the
non-headroom situation from recorded numbers only, and re-asserts the full block on each:

- **`deli-atcap` (at-capacity)** — same whole-series band as `deli-varmax` (`band_variance:"all"`,
  horizon `{0.62, 1.02}`, sigma 0.18, higher-is-better), with a RECORDED capacity 500.0 resolutions/day
  and a recorded **load 1.25 (>= 1.0)**. `_capacity_reason`: horizon worst-side low 0.62 < capacity
  500.0 (so NOT deficit), load 1.25 >= 1.0 → **`reason: "at-capacity"`, `flag: True`**.
- **`deli-deficit` (deficit)** — a **lower-is-better** latency series (Sprint-23 CO points: actuals
  12/14/16/18, variances 2/4/6/8, `band_variance:"all"` → sigma 8, projections [20,22,24], horizon
  `{12.0, 32.0}`) with a RECORDED capacity VALUE **30.0** resolutions/day (load 0.9). `_capacity_reason`
  (lower-is-better → worst-side = high): horizon high **32.0 >= capacity value 30.0** →
  **`reason: "deficit"`, `flag: True`**.

On BOTH non-headroom orgs, `options_flagged` marks **EVERY capacity-consuming NON-baseline option**
`capacity_risk` (7 options for the deli set) and **NEVER the baseline** (`unresolved`, do-nothing —
consumes no capacity); the `reason` equals the org's Q9 `capacity_planning_attention` label **BY
CONSTRUCTION** (shared `_capacity_reason`). **The marker is a LABEL at its limit:** for EVERY org —
including the at-capacity and deficit ones — `q7.options` (same count + uris) + `q7.machine_eligible_best`
+ `q8.recommendation`/`floor_gated` are EXACTLY equal to the frozen `cockpit_q7q8` line (no §6 overrule,
no re-rank, no option-removal); the Q8 recommendation stays `partial-settlement`. The Sprint-27 headroom
org + all no-capacity / no-band / no-data orgs are byte-identical (no new key, no changed byte).

Proof: `run_forecast_horizon4_demo.py` (exit 0 = ALL PASS) drives ≥7 orgs (fc, vm, vmc-headroom,
fl2, deli, deli-atcap, deli-deficit), asserts full §7L Q1–Q10 on all, the non-headroom block fully
exercised on the two new orgs, the marker-is-a-label EQUALITY for every org, byte-identity of the
five reused orgs, determinism, and recorded-data provenance (every `capacity_constraint` value traces
to a recorded field). The two new orgs' fixtures pass Sprint-0 C1–C5. **Honest §16 verdict:** the marker
is now demonstrated across ALL THREE of its derived reasons (headroom / at-capacity / deficit) on real
orgs WHILE the Q8 recommendation provably stays unchanged even at at-capacity/deficit. **Still not
derivable:** a capacity-constrained OPTIMIZATION that re-ranks the recommendation (out of scope — the
§6 human always rules; the marker never CHOOSES), and `capacity_infeasible` (structurally unreachable
until a RECORDED per-option capacity requirement exists). No engine change; SPEC v0.22, 49 `$defs`,
no new noun, `ros/` untouched.

## 13. Update after Sprint 29 — the capacity marker can now reach `capacity_infeasible` for a SPECIFIC option (from a RECORDED per-option requirement)

Sprint 28's own finding (`sprints/sprint-28/notes/findings.md`, "Open issues / next work") was honest
that the marker can label the whole `capacity_risk` but `capacity_infeasible` is **STRUCTURALLY
UNREACHABLE**, because NO PER-OPTION capacity requirement is ever recorded — the engine compares the
org-level recorded `load` / the horizon band's worst-side to the recorded capacity VALUE, so it can
flag a whole option set as risky but can never say a SPECIFIC option is infeasible under capacity, and
never price capacity per option. **Sprint 29 closes that bounded slice additively: the recorded
capacity becomes PER-OPTION.**

Two additive pieces, the ONLY engine change in the whole project:

- **A new REPLAYABLE recorder `record_capacity_requirements(sub, authority_uri, requirements, signer)`**
  (in `adjudication_engine.py`, next to `record_capacity`): it appends an additive
  `capacity_requirements` map (`{option_name: nonneg amount}`, MERGE-not-replace) **on the SAME
  `authority://` object that already carries the additive `capacity` {value, unit, load}**. This is
  unit-coupled **by construction**: the authority holds both the capacity and the per-option
  requirements, so `AVAILABLE = recorded capacity VALUE − recorded load` derives in the SAME recorded
  unit. C2-safe (`capacity_requirements` has no temporal suffix). An org that records NO requirements
  keeps today's block byte-identical.
- **A per-option label from ONE recorded rule** (`_per_option_capacity_flags` helper, called only in
  the Q7/Q8 `capacity_constraint` block of `cockpit_s7l` when requirements are recorded): an option is
  `capacity_infeasible` iff its **RECORDED requirement > available**; otherwise `capacity_risk` as
  today (a consumer with no recorded requirement, or at/under available, when the org level is not
  headroom). The baseline (do-nothing/UNRESOLVED) is **NEVER flagged**; `reason`/`flag` still come from
  the frozen org-level `_capacity_reason` rule; the block is still a **LABEL** — no option removed, no
  re-rank, no §6 overrule — and, when requirements are recorded, it also surfaces the additive
  `per_option_requirements` map + `available_capacity` number on the block. Frozen functions
  (`rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`/`reconcile`/`run_scenario`/
  `_derive`/`_aggregate`/`_capacity_reason`) are untouched; no new noun; 49 `$defs`; SPEC v0.22.

Proof: `run_forecast_per_option_capacity_demo.py` (new, exit 0 = 88 PASS) reuses the five Sprint-28
byte-identical orgs (fc / vm / vmc-headroom / fl2 / deli) PLUS two NEW orgs that RECORD per-option
requirements:

| org | recorded capacity | per-option requirement | `options_flagged` |
|---|---|---|---|
| **`deli-infcap`** | **at-capacity** 500.0 res/day, load 1.3 → available **498.7** | heavy 3× 499.0; lighter 4× 50/100/200/200 | 3 **`capacity_infeasible`** + 4 `capacity_risk`; baseline absent |
| **`deli-deficit-inf`** | **deficit** lower-is-better latency, cap 30.0, load 0.9 → available **29.1** | heavy 3× 30.0; lighter 4× 10/15/20/20 | 3 **`capacity_infeasible`** + 4 `capacity_risk`; baseline absent |

On both, every `capacity_infeasible` label traces to a recorded requirement > available; every
`capacity_risk` to a requirement ≤ available (or a no-requirement consumer); the baseline (no recorded
requirement) is never flagged; `reason` is still at-capacity / deficit from the org-level rule and
AGREES with each org's Q9 `capacity_planning_attention` label BY CONSTRUCTION. The marker is STILL a
LABEL: for EVERY org (incl. the two infeasibility ones) `q7.options` (count + uris) +
`q7.machine_eligible_best` + `q8.recommendation`/`floor_gated` are EXACTLY equal to `cockpit_q7q8`, and
the Q8 recommendation stays `partial-settlement` even when a SPECIFIC option is infeasible. The five
reused orgs are byte-identical (Sprint-28 states preserved exactly; a no-requirements org carries NO
`per_option_requirements`/`available_capacity` key). Both new orgs' fixtures pass Sprint-0 C1–C5
(26 instances each, 49 `$defs`); full non-regression is green.

**Honest §16 verdict:** the marker now reaches `capacity_infeasible` for a SPECIFIC option from a
RECORDED per-option requirement + a recorded available number, while it is still a label — never a
removal, never a re-rank, never an overrule of the §6 human — and the Q8 recommendation provably stays
unchanged even when SOME option is infeasible. **Still not derivable (the honest frontier):** a
genuinely capacity-constrained **OPTIMIZATION** that RE-RANKS the recommendation for the machine stays
out of scope of the deterministic advisory stance (the marker never CHOOSES), and a per-option
requirement that is **NOT unit-coupled** to the capacity remains non-derivable (an org with no recorded
capacity value/load, or an option with no recorded requirement, carries no infeasibility label — the
engine never invents one). Additive; the ONLY engine file touched is `adjudication_engine.py`; SPEC
v0.22, 49 `$defs`, `ros/` untouched.

## 14. Update after Sprint 30 — the marker is a REASON, never a CHOICE: the RECOMMENDED option made `capacity_infeasible`, yet the Q8 recommendation provably stays unchanged

Sprint 29's own finding (`sprints/sprint-29/notes/findings.md`, "Open issues / next work") disclosed
the honest frontier the next sprint would face: **the marker still never CHOOSES a different option for
the machine — the §6 human always does.** In every Sprint-29 org the machine-eligible best
(`partial-settlement`) itself was `capacity_risk` (recorded requirement ≤ available), so the label-vs-
choice boundary had never been exercised at its sharpest — when the recorded per-option requirement
CLEARLY makes the option the machine WOULD recommend itself `capacity_infeasible`. **Sprint 30 closes
that boundary proof AS DATA, additively, with NO engine change** (Sprint 29's `_per_option_capacity_flags`
already labels ANY option — including the recommended one — `capacity_infeasible` when its recorded
requirement > available). The point is the story + the proof.

A REFACTOR-FREE, RECORDED-DATA-ONLY new org `deli-recommend-infcap` (`run_forecast_label_vs_choice_demo.py`,
new, exit 0 = ALL PASS) reuses the at-capacity record (cap 500.0 res/day, load 1.3 → available **498.7**)
but records a per-option requirement map in which the machine-eligible best / Q8 recommendation itself is
the infeasible one:

| `partial-settlement` (RECOMMENDED) | 499.0 (recorded) | > available 498.7 | **`capacity_infeasible`** |
| other 6 non-baseline options | 50/80/100/200/200/200 | ≤ available | `capacity_risk` |
| `unresolved` baseline | (no requirement recorded) | — | never flagged |

The Q7/Q8 `capacity_constraint` block labels `partial-settlement` `capacity_infeasible`, while the
cockpit **provably STILL recommends partial-settlement** — `q7.options` (count + uris) +
`machine_eligible_best` + `q8.recommendation` + `floor_gated` are EXACTLY equal to `cockpit_q7q8`, no
re-rank, no removal, no §6 overrule. The block's `note` names the UNCHANGED Q8 + the §6 human: the marker
LABELS "the recorded capacity says the recommended option can't run"; it does NOT pick a replacement.
`reason` stays `at-capacity` (== the org's Q9 `capacity_planning_attention` label BY CONSTRUCTION). This
is generic + additive — a recorded authority `capacity` + a recorded per-option `capacity_required`
descriptor + a recorded `metric://` series with point-`variance`/`band_variance`; no new noun, frozen
49 `$defs`, SPEC v0.22, `adjudication_engine.py` hash UNCHANGED (byte-identical — the seven Sprint-29
orgs still carry the exact §13 output, incl. a no-requirements org keeping today's block exactly).

**Honest §16 verdict:** the marker now reaches the RECORDED per-option limit at its sharpest — the
recommended option itself is `capacity_infeasible`, and the cockpit provably STILL recommends it (exactly
`cockpit_q7q8`); the marker is a REASON, never a CHOICE, and the §6 human always rules. **Still not
derivable (the honest frontier):** a capacity-constrained **OPTIMIZATION** that RE-RANKS the
recommendation for the machine stays out of scope of the deterministic advisory stance — choosing a
different option for the machine is a policy / user decision, not a label; and a per-option requirement
that is NOT unit-coupled to the recorded capacity / an option with no recorded requirement remains
non-derivable. No SPEC bump (v0.22). The optimization SEAM, if the prompt author ever wants it, is
spelled out in `sprints/sprint-30/notes/findings.md`: recorded per-option requirements already exist; a
deterministic next-best-non-infeasible rule by the frozen `rank` utility would be a deliberate
"re-rank for the machine" capability, explicitly out of the advisory stance unless requested.

## 15. Update after Sprint 31 — the WHOLE recorded-data decision surface is inventoried as reason-not-choice (positive consolidation, NO engine change)

Sprint 31 (`run_recorded_surface_demo.py`, new, exit 0 = ALL PASS) makes the label-vs-choice boundary the
ORGANIZING truth of a full inventory of the recorded-data decision surface. After six sprints (20-30) the
whole §7L surface is recorded-data + reason; Sprint 31 proves that in ONE comprehensive, auditable run.
**No engine change** — `adjudication_engine.py` hash `a60f8f7…` stays byte-identical (a new survey runner +
recorded data only, as Sprint 30). It drives 11 orgs (the eight Sprint-30 orgs byte-identical + INSPECT +
COVE + one no-data org, all new labels) and emits, per org, a `recorded_surface` dict:

- **present_recorded** = {metric_series, point_variance, band_variance, capacity,
  capacity_requirements, floor_gated, weights, reconcile_rule} (which RECORDED descriptors the org carries);
- **derived_reasons** = {Q3_forecast, Q6_projection, Q7Q8_capacity_constraint, Q9_capacity,
  Q8_do_nothing_impact} (the actual derived REASON each produced, or None);
- **derivable_universe** = the sorted set of every derived reason;
- **not_derivable** = the named optimization seam + any descriptor the org does NOT record.

It asserts, per org, that **every derived label traces to a recorded descriptor** (Q3/Q6/Q8-forecast →
metric_series; Q7Q8/Q9-capacity → capacity; no reason without its recorded source — the engine never
invents one, so the no-data org derives NOTHING), and the **reason-not-choice proof, totalled**: Q7
`options` + `machine_eligible_best` + Q8 `recommendation` + `floor_gated` EXACTLY equal `cockpit_q7q8`
for ALL 11 orgs. The tally prints ~"11/11 orgs the marker never re-ranks; INCLUDES the Sprint-30 org
`deli-recommend-infcap` where the RECOMMENDED option is `capacity_infeasible`" — the sharpest label-vs-
choice boundary, still a label, never a choice. New orgs `inspect-recorded` (QC on-time series,
at-capacity, per-option infeasible/risk), `cove-recorded` (lower-is-better answer-latency series,
deficit, per-option infeasible/risk), `inspect-nodata` (no recorded data — the derivable-vs-not control).

**§16 — is the whole recorded-data decision surface now recorded-data + reason?** Yes: the entire §7L
decision surface (Q3 forecast attention, Q6 projection + recorded band, Q7/Q8 capacity_constraint reason
+ per-option flags, Q9 capacity planning, Q8 do-nothing expected-impact) is provably recorded-data + a
REASON, and the Q8 recommendation provably stays the frozen `rank` output for every org (no recorded data
ever re-ranks). This is generic + additive: recorded `metric://` series + recorded point-`variance` + the
recorded `band_variance` source + a recorded authority `capacity` + a recorded per-option
`capacity_required` descriptor; no new noun, frozen 49 `$defs`, engine byte-identical (hash `a60f8f7…`).
**What is STILL not derivable:** the ONE remaining out-of-scope step — a capacity-constrained OPTIMIZATION
that RE-RANKS the Q8 recommendation for the machine (a deliberate "re-rank for the machine" POLICY / user
decision, NOT a label, deliberately NOT built; the seam is recorded per-option `capacity_requirements`
already present + a deterministic next-best-non-infeasible rule by the frozen `rank` utility — the only
missing piece; it CHANGES the Q8 recommendation). Plus a per-option requirement that is NOT unit-coupled
to the recorded capacity / an option with no recorded requirement remains non-derivable. No SPEC bump
(v0.22). New-org fixtures pass Sprint-0 C1-C5; the no-data org emits no fixtures (0 instances, correct).

## 16. Update after Sprint 32 — the capacity-constrained RE-RANK of the §7L Q8 recommendation for the machine (an EXPLICIT authorized POLICY step, distinct from the reason-not-choice advisory)

Sprint 32 (`capacity_rerank.py`, NEW module + `run_capacity_rerank_demo.py`, NEW runner, exit 0 = ALL PASS)
builds the ONE step Sprint 30/31 named and deliberately left out of scope — **because this prompt
explicitly asked for it**. The engine is UNTOUCHED (hash `a60f8f7…` byte-identical); the re-rank is a
NEW pure module that reuses the engine's public surface (the `capacity_constraint` block `cockpit_s7l`
renders from recorded data + the frozen `rank` utility). It computes, for an org whose machine-eligible
best is `capacity_infeasible` (from RECORDED per-option `capacity_requirements` > available =
recorded capacity.value − recorded load), the **highest-utility option that is neither floor-gated nor
`capacity_infeasible`** — a deterministic next-best-non-infeasible rule by the frozen `rank` utility.

Per re-ranked org it emits an additive **`capacity_rerank`** block: `prior_machine_best` (the unchanged
frozen `rank` output), `prior_best_capacity_flag`, `recorded_descriptors`, `available_capacity`,
`per_option_requirements`, `replacement`, `replacement_is_baseline`, `all_capacity_consuming_infeasible`,
`floor_respected`, `policy`, and an honest `why`. Deterministic; respects the §6 floor (a floor-gated
option is never auto-picked); never invents a requirement; falls back to the do-nothing/UNRESOLVED
baseline (and says so) when every capacity-consuming option is infeasible; reports the re-ranked
selection AS DATA without overwriting the engine's advisory Q8 recommendation.

PROVEN (forms the §16):
- RE-RANK fires on `deli-recommend-infcap` (partial-settlement → conditional-resolution),
  `inspect-recorded` (rework-partial-credit → conditional-accept-with-guarantee),
  `cove-recommend-infcap` (NEW — step-therapy-first → authorize-generic), and `deli-all-infeasible`
  (NEW — every capacity-consuming option infeasible → unresolved baseline, `replacement_is_baseline`
  True). For each, the re-ranked Q8 == the recomputed highest non-infeasible non-gated utility option
  by the frozen `rank`;
- UNCHANGED (best NOT infeasible → byte-identical to `cockpit_q7q8`): the nine other orgs including
  `cove-recorded` (best `step-therapy-first` = capacity_risk, runnable) and no-data `inspect-nodata`;
- the **advisory path NEVER re-ranks**: even where re-rank fires, the engine's Q8 recommendation still
  equals `cockpit_q7q8` — the Sprint-31 reason-not-choice inventory stands untouched;
- determinism (dict equality on re-run for all 13 orgs); the two NEW fixture dirs pass Sprint-0 C1-C5;
  full non-regression green; engine `a60f8f7…`, schema `7fc38c8c…`, 49 `$defs`, SPEC v0.22, no `://qk/`
  in the new fixtures; `ros/` + schema + sector `configs.py` untouched; no new noun.

**§16 verdict — is the ONE remaining frontier (a capacity-constrained, re-ranked Q8 recommendation under
recorded capacity) now derivable?** Yes, as an explicit authorized POLICY step distinct from the
deterministic advisory label-vs-choice boundary. The advisory path still labels and never re-ranks (the
Sprint-31 inventory provably stands); the re-rank computes a capacity-constrained replacement from
recorded data under POLICY, respects the §6 floor, and is deterministic + additive (new module, engine
byte-identical). **Still not derivable (honest residual):** a probabilistic/stochastic forecast (the
recorded band remains a spread, never a CI — nothing here invents a distribution); a per-option
requirement NOT unit-coupled to the recorded capacity value (no available figure → no infeasibility
label → nothing to re-rank); an option with no recorded requirement carries no infeasibility label (the
machine never invents one); and any choice the §6 human must make that recorded data cannot machine-decide
(the re-rank is POLICY-authorized, not a claim of objective best). No SPEC bump (v0.22).
## 17. Update after Sprint 33 — the now-TWO-path decision surface is consolidated as ONE coherent recorded-data framework (reason-not-choice ADVISORY + POLICY-authorized capacity-constrained RE-RANK), proven to compose without one silently shadowing the other

Sprints 31 (reason-not-choice inventory) and 32 (the capacity-constrained re-rank) left TWO deliberately
distinct decision PATHWAYS over the same recorded §7L data. Sprint 33 is a positive CONSOLIDATION: it makes
them one coherent framework and PROVES they never silently interfere. **No engine change** (`adjudication_engine.py`
sha256 `a60f8f7…` byte-identical) and **no `capacity_rerank.py` change** (sha256 `f7c6a185…` byte-identical) —
a new survey/audit runner + recorded data ONLY, the Sprint 31/32 proof shape. The runner (`run_two_path_demo.py`)
drives the SAME 13-org recorded set as Sprint 32 and emits, per org, a `two_path_surface` {advisory, rerank}
plus an EXHAUSTIVE-DISJOINT PATH class:

- **ADVISORY-no-capacity** (5 orgs: `deli`, `deli-forecast`, `deli-varmax`, `deli-flat2`, `inspect-nodata`) —
  no recorded authority `capacity` → nothing to constrain/re-rank; the advisory Q8 IS the (single) answer.
- **ADVISORY-best-runnable** (4: `cove-recorded`, `deli-infcap`, `deli-deficit-inf`, `deli-varmax-cap`) —
  capacity recorded, machine best NOT `capacity_infeasible` → the advisory stands, `needed=False`, and the
  replacement == advisory Q8 (they AGREE — one path, unchanged).
- **RE-RANK** (4: `deli-recommend-infcap`, `inspect-recorded`, `cove-recommend-infcap`, `deli-all-infeasible`) —
  best `capacity_infeasible` from recorded per-option `capacity_requirements` → by POLICY the machine picks
  the highest-utility option (frozen `rank`) that is neither floor-gated nor `capacity_infeasible`.

PROVEN (all exit 0 = ALL PASS, from the SAME recorded data):
- **composition / non-interference** — for every org the advisory Q8 recommendation STILL == `cockpit_q7q8`
  (the re-rank NEVER shadows it, 13/13); where `needed=True` the replacement is a DIFFERENT option from the
  advisory Q8 AND ≠ the machine_eligible_best (provably distinct paths); where `needed=False` the replacement
  == the advisory Q8 (they agree);
- **floor integrity** — no advisory or re-rank selection is ever a floor-gated option (asserted against the
  frozen `rank`), 13/13;
- **exhaustive-disjoint taxonomy** — every org is exactly one of the three classes; no org is two;
- **determinism vs history** — re-running gives an identical `two_path_surface`, AND the Sprint-31
  reason-not-choice tally (11/11 q7/q8 == `cockpit_q7q8`) + the Sprint-32 re-rank results (4 firings with a
  provably-different replacement, 9 unchanged) are BOTH reproduced from the same recorded data in this run —
  the consolidation is a VIEW over one dataset, not a rewrite.

**§17 verdict — are the two paths now a single coherent recorded-data decision framework?** Yes. The
reason-not-choice ADVISORY (Sprint 31, marker = a REASON never a CHOICE) and the POLICY-authorized
capacity-constrained RE-RANK (Sprint 32) compose without one silently overriding the other, table coordinated
over the same 13 orgs, exhaustive-disjoint classification, floor-respecting on both paths, both histories
reproduced from the same recorded data. **Still not derivable (the honest residual — unchanged by
consolidation):** a probabilistic/stochastic forecast (the recorded band is a spread, never a CI; nothing
invents a distribution); a per-option requirement NOT unit-coupled to the recorded capacity value (no
available figure → no infeasibility label → nothing to re-rank); an option with no recorded requirement
carries no infeasibility label (the machine never invents one); and any choice the §6 human must make that
recorded data cannot machine-decide (the re-rank is POLICY-authorized, not a claim of objective best). No
SPEC bump (v0.22); no new noun; frozen 49 `$defs`; `ros/` + schema + sector `configs.py` untouched.

## 18. CONSOLIDATION-AUDIT (Sprint 34): the two-path framework as ONE coherent recorded-data whole over the ENTIRE ORG CATALOG

Sprint 34 is a **pure, engine-free consolidation-audit**: it verifies the reference build stays green as one
whole and extends the Sprint-33 one-framework answer from the 13-org set to the **entire ORG CATALOG** — the
union of every org the `run_forecast_*`/`run_cockpit_*`/`run_adjudication_engine_demo`/`r32` CR demo runners
already construct (**22 orgs**, enumerated from those files, none invented). `adjudication_engine.py` (hash
`a60f8f7…`) AND `capacity_rerank.py` (hash `f7c6a185…`) stay **byte-identical**; no new capability, no new
noun, frozen 49 `$defs`, schema `34264934…`, SPEC v0.22.

The whole-catalog taxonomy is **12 ADVISORY-no-capacity / 6 ADVISORY-best-runnable / 4 RE-RANK = 22** (the
Sprint-33 13-org {5,4,4} is the strict subset; the 9 added are 7 no-capacity + 2 best-runnable `deli-atcap`/
`deli-deficit`, which record capacity but NO per-option requirements, so the machine best is `capacity_risk`,
never `capacity_infeasible`). The audit asserts advisory-never-shadowed (22/22 Q8 == `cockpit_q7q8`; re-rank
replacement provably distinct where it fires), exhaustive-disjoint classification, floor integrity (22/22),
determinism, and that the Sprint-31 tally (11/11) + Sprint-32 re-rank (4) + Sprint-33 taxonomy all reproduce
from the SAME recorded data. See the consolidated boundary cheat-sheet
`contested_reality/docs/DECISION-FRAMEWORK-BOUNDARY.md` and
`contested_reality/artifacts/adjudication/reports/two-path-catalog.md`.

**§18 verdict — does the two-path one-framework answer hold across the whole catalog?** Yes. The reason-not-
choice ADVISORY and the POLICY-authorized RE-RANK compose as ONE recorded-data framework over every org the
CR runners exercise — the deterministic advisory label-vs-choice boundary (a REASON, never a CHOICE) still
holds, `capacity_rerank.py` stays a pure untouched module, and the honest residual is unchanged
(probabilistic/stochastic forecast; a per-option requirement NOT unit-coupled to the recorded capacity / an
option with no recorded requirement — never invented; any §6-human choice recorded data cannot machine-
decide — the re-rank is POLICY-authorized, not objective best). No SPEC bump (v0.22).
