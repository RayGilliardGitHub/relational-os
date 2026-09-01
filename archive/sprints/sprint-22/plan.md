# SPRINT 22 — plan

**Goal (bounded slice).** Make the forecast→attention crossing **direction** a recorded, additive
parameter, so the Sprint-21 closure — a recorded `metric://` series + `forecast_metric` projection —
flags **forecast-driven Q3 attention and prices the Q8 do-nothing expected-impact for BOTH directions**,
deterministically and data-only: (i) **higher-is-better** (rate/quality; the Sprint-21 default:
`min(projection) < threshold` is bad) and (ii) **lower-is-better** (cost/latency/defect/risk:
`max(projection) > threshold` is bad). The direction is recorded on the `metric://` object as an additive
`direction` field (`"higher-is-better"` is the DEFAULT, keeping Sprint-21 behavior byte-identical; an org
may record an explicit `"lower-is-better"`). No new noun, no schema/`$defs` edit, SPEC stays v0.22.

## Baseline (verified before any change — real output)
- `run_forecast_action_demo.py` → RESULT: ALL PASS, exit 0.
- 12 prior CR runners ALL PASS; `conformance_adjudication.py` (16 labels) + the 4 other C-R conformances ALL PASS.
- `instances/build_all.py` + `conformance_all.py` ALL PASS; S5 reference demo + conformance ALL PASS;
  agent demo + conformance ALL PASS.
- Schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22.

## The additive engine change (single file: `instances/contested_reality/adjudication_engine.py`)
Only `_forecast_closure` is extended (plus a render line if needed). Frozen functions untouched.
1. Read the recorded direction off the metric object:
   `direction = str(fap_metric.get("direction") or "higher-is-better").strip().lower()`.
2. Set `worst` per direction: higher-is-better → `min(proj)`; lower-is-better → `max(proj)`.
   `worst_period` = that period.
3. Crossing per direction: higher-is-better → `worst < thr`; lower-is-better → `worst > thr`.
4. `attention_item.why` worded per direction: higher → "projected to fall below {thr} ({src}) — worst
   {worst} at period {p}"; lower → "projected to rise above {thr} ({src}) — worst {worst} at period {p}".
5. Do-nothing `summary`/`gap` oriented per direction: higher → "below recorded {src} {thr} by {gap}"
   (gap = thr − worst); lower → "above recorded {src} {thr} by {gap}" (gap = worst − thr).
   On-target wording per direction ("stays at/above" vs "stays at/below").
6. Record `direction` on the returned closure dict, the `q8["forecast"]` block, and the
   `do_nothing` block (additive) so the runner can assert it.
The threshold resolution is UNCHANGED (`forecast_threshold` → metric `target` → last `actual`).
**Default `direction == "higher-is-better"` ⇒ byte-identical to Sprint 21** (same worst=min, same
crossing `<`, same wording).

## The runner (`run_forecast_direction_demo.py`, exit 0 = ALL PASS) — ≥4 orgs on fresh Substrates
- `deli-forecast` — higher-is-better deteriorating (Sprint-21 series [0.92,0.90,0.87,0.86]→[0.84,0.82,0.8],
  target 0.95). **Assert byte-identical to Sprint 21** (Q3 `[forecast]` + do-nothing on_target=False).
- `deli-forecast-flat` — higher-is-better on-target control ([0.96,0.97,0.96,0.96]→[0.96,0.96,0.96]).
  **Assert byte-identical to Sprint 21** (no forecast attention, do-nothing on_target=True).
- `deli-cost` — NEW lower-is-better: a recorded cost/latency series that RISES above a recorded ceiling.
  e.g. `metric://deli-cost/m-latency`, actuals 12/14/16/18 ms, ceiling/target 16,
  projection [20,22,24] → `max > ceiling` → forecast Q3 attention + do-nothing on_target=False,
  gap projected in the RISING orientation. Records explicit `direction="lower-is-better"`.
- `deli-cost-flat` — OPTIONAL second lower-is-better control whose projection stays BELOW the ceiling
  (e.g. actuals 8/9/8/8→flat 8, ceiling 10) → no forecast attention, do-nothing on_target=True.
  Mirrors the Sprint-21 flat control.
- `deli` — no-data org → unchanged fallback (no forecast/do-nothing fields).
Asserts: full §7L Q1–Q10 on each; higher-is-better byte-identical to Sprint 21; lower-is-better Q3
carries `[forecast]` + Q8/trade-off prices do-nothing in the RISING orientation (on_target=False);
flat controls add no forecast attention + price on_target=True; determinism on re-run; agreement of
Q3/Q8 projection+threshold with `forecast_metric`; no §6 overrule (Q8 recommendation ==
`cockpit_q7q8` for every org); no wall-clock. Emits fixtures + a report.

## Non-regression (after the change)
Re-run every baseline command from above (the full list in the PROMPT's Verification section) → ALL PASS.
84 `$defs`? NO — keep 49. Schema hash `7fc38c8c…` unchanged, SPEC v0.22, `ros/` untouched,
deli/cove fixtures unchanged up to the clock, the two Sprint-21 recorded orgs' Q3/Q8 byte-identical.

## Documentation (roll-forward)
- `contested_reality/docs/ENGINE-FORECAST-DIRECTION.md` (new) + additive Sprint-22 note in
  `docs/ENGINE-FORECAST-ACTION.md`.
- `instances/README.md` (Sprint-22 entry); `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`
  ("Update after Sprint 22"); `references/` if useful.
- `sprints/sprint-22/{summary.md,notes/findings.md}`; write the next prompt at `sprints/sprint-23/PROMPT.md`.
- Do NOT bump SPEC unless a genuine normative gap surfaces (log it then).