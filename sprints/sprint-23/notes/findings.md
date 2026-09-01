# SPRINT 23 — NOTES / FINDINGS

## Assumptions that mattered
- **Band preserves byte-identity by construction.** The add flashes to keys ONLY when the last recorded
  point's `variance` is numeric — `rv = _num(fc["recorded_variance"])` is not None. A no-variance series
  (or no-data org) takes the exact Sprint-22 path: no `band`, no `recorded_variance`/`variance`, no
  `expected_last`, no summary phrase. Verified on `deli-flat2`: `set(dn.keys()) == {baseline, priced,
  on_target, summary, metric, direction}` and the summary byte-equal to the single-point template.
- **Superset byte-identity via prefix, not equality.** The old summary/`why` strings are the strict
  PREFIX of the new ones (the band phrase is appended). This is what lets the Sprint-21/20 runners pass
  untouched (they use `in`/containment checks) and makes the Sprint-22 assertion update minimal, not a
  re-write.
- **Only the LAST recorded point's variance is used** (`forecast_metric.recorded_variance` = the last
  point's `variance`, as a magnitude). This is the honest, bounded choice — it is recorded data, it
  matches what Q6 already renders, and it needs no aggregation choice. It also means a series that
  recorded different variances earlier is collapsed to the final spread (see Open issues).
- **Float rendering matters.** `str(CO_THR)` where `CO_THR=16.0` renders `"16.0"` (not `"16"`), so the
  band phrases and the runner assertions must match the float rendering; the runner's band dicts use the
  exact rounded floats computed from the recorded data.
- **The band is NOT a confidence interval.** It bounds the deterministic worst by the recorded spread.
  Framing this precisely in the docs (a recorded-data range, no probability claim) keeps the
  deterministic ~$0 stance honest.

## Verified (real tool output, all exit 0)
- Green baseline captured FIRST (Sprint-22 state, before any edit): all three forecast runners, the 12
  curated C-R demos, `conformance_adjudication` (16 labels), the 4 prior CR conformances,
  `build_all`/`conformance_all`, S5 reference + conformance, agent demo. Template hash `7fc38c8c…`.
- After the additive change: new `run_forecast_variance_demo.py` ALL PASS (27 assertions) + the full
  non-regression re-run of every runner/conformance above → ALL PASS. New org fixtures (`deli-flat2`,
  `deli-forecast`, `deli-cost`) pass the Sprint-0 C1–C5 conformance.
- Template `relational-os.schema.json` hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` + sector
  instances untouched. `git status` confirms the only source changes are `adjudication_engine.py`,
  `run_forecast_direction_demo.py` (additive-aware), new `run_forecast_variance_demo.py`, and the
  docs (fixture churn = regenerated artifacts from running the runners).

## Pitfalls encountered
- **The tool parser blocks chained/redirect+`$(...)` shell payloads** — run the runners as short single
  commands (`python3 <name>.py 2>&1 | tail -1`), not `>file; echo exit=$? $(grep ...)`.
- **Watch the escaping**: a patch that introduced `\"` into a `.py` file broke `ast.parse`; the
  patch tool's `new_string` must be written with plain `"` (verified via `ast.parse` after the repair).
  Repaired programmatically and re-`ast.parse`d.

## Open issues / next work (the honest frontier for Sprint 24)
- **The band uses only the LAST recorded variance.** A series whose `variance` changed across its
  recorded points (widening OR narrowing spread) is collapsed to the final `variance` in the band.
  Sprint 24's bounded slice could make the band's variance source a **recorded, additive parameter** —
  e.g. `band_variance` = the last point's variance (today's default, byte-identical) vs a recorded
  whole-series choice (largest recorded magnitude / min-max of the recorded variances) — still
  recorded-data only, no invented number, additive, with the last-point default keeping Sprint 23
  bytes identical. That would let an org whose measured spread WIDENED over time price a do-nothing
  band from the recorded worst-case spread, and one that CONVERGED tighten it — still honest: no
  probability, no model, only recorded points.
- **The band is around the single worst projected point**, priced at the do-nothing line; it does not
  aggregate a band across ALL projection periods or feed Q9 capacity. Out of scope unless a later
  sprint makes it data-only + additive.
- **A no-variance series cannot produce a band** (correct fallback) and a **stochastic/adaptive
  forecast** is still explicitly out of scope of the deterministic ~$0 stance.

No normative gap surfaced → SPEC stays v0.22.