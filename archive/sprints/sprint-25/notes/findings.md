# SPRINT 25 — NOTES / FINDINGS

## Assumptions that mattered
- **Horizon-wide band is a per-period application of the SAME recorded sigma**, not an aggregation that
  produces a new number. Every `band_periods` bound = `projected ± sigma` (the recorded sigma is the
  same value that already prices the single-worst band), and `band_horizon` = `min(period lows)` /
  `max(period highs)`. So `band_horizon.high` is NOT sigma again — it is the farthest period low/high
  the series already projects. `sigma` is still exactly one recorded point |variance| magnitude.
- **The widening is data, not a model.** `deli-varmax`'s horizon-wide high (1.02) exceeds its
  single-worst band high (0.98) because period 1's projected value (0.84) + σ0.18 = 1.02 sits ABOVE
  the worst point's own +σ band (worst 0.8 + 0.18 = 0.98). This is a pure per-period application of
  the recorded sigma over recorded projections — an honest "the whole-horizon worst case is wider than
  the single-worst point's band", NOT a wider invented sigma and NOT a confidence interval.
- **The single-worst `band` field is left EXACTLY as Sprint 23/24.** `band_periods`/`band_horizon` are
  strictly ADDITIVE; the old `band = {worst, sigma, low, high, crosses}` (with `source` when a
  whole-series choice is active) is byte-identical. The do-nothing summary phrase is appended AFTER the
  Sprint-23/24 phrase, keeping the old string a strict prefix (Sprint-23's prefix-preservation rule).
- **Q9 capacity-attention is a flag/reason, never a capacity NUMBER.** `band_capacity_attention`
  derives from the horizon range + the recorded threshold; `why` can reference the RECORDED `capacity`
  (value/unit/load) but the engine never fabricates or mutates it. Verified by the `deli-varmax-cap`
  org whose `why` names 500.0 resolutions/day (load 0.72) while the capacity object stays intact.
- **No-band / no-data orgs carry none of the new keys** — `band_capacity_attention` is emitted only
  when a band exists AND the thorough threshold is numeric; the no-variance control and no-data org
  are byte-identical (verified by assertions on `deli-flat2` + `deli`).
- **One engine file, two additive blocks.** Only `adjudication_engine.py`'s `_forecast_closure` band
  block (band_periods/band_horizon + summary phrase + ride keys) and `cockpit_s7l`'s Q9 block
  (band_capacity_attention) were extended. All frozen functions untouched. `render_cockpit_s7l` needed
  no change (its Q8/Q9 lines are generic).

## Verified (real tool output, all exit 0)
- **Green baseline captured FIRST** (Sprint-24 state, before any edit): all 5 forecast runners +
  `run_cockpit_s7l_demo` + the 12 curated C-R demos + `conformance_adjudication` (16 labels) + the 4
  prior CR conformances + `build_all`/`conformance_all` + S5 reference + conformance + agent demo.
  Schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22.
- **After the additive change:** new `run_forecast_horizon_demo.py` -> **ALL PASS**, and every runner /
  conformance in the baseline re-run -> ALL PASS (all exit 0).
- **Superset byte-identity:** `deli-forecast`'s single-worst band == the Sprint-23 runner's `FC_BAND`
  exactly and the do-nothing summary keeps the Sprint-23/24 string as a strict prefix (verified
  against the Sprint-23 runner's constants via `run_forecast_horizon_demo.py`).
- **New org fixtures pass the Sprint-0 C1–C5 conformance** (26 instances, 49 `$defs`), driven directly
  for `deli-varmax-cap` and via `conformance_adjudication` for the others. Conformance returns `True`
  (not a string) — the runbook's note that `Conformance().run()` returns a bool (a previous sprint's
  assumption that the return is the "ALL PASS" string is inaccurate; the printed PASS lines are the
  real check).
- Schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` + schema + sector `configs.py` untouched.
  `git status` (source only) shows `adjudication_engine.py` + new `run_forecast_horizon_demo.py` + the
  docs; the rest is regenerated-artifact churn from running the runners.

## Pitfalls encountered
- **The patch tool can still inject `\"` into a `.py` string literal** — the runner's first draft had a
  literal `\"` inside a summary string that broke the byte-identity substring check; repaired with a
  plain `"` and re-`ast.parse`d (this echoes the Sprint-23/24 note).
- **Pyright noise on `relabel_to`'s recursive `_rw` JSON rewriter** (consistent with Sprint 23/24): the
  wall of `reportIndexIssue`/`reportArgumentType` errors on `c["label"] = ...` etc. are FALSE POSITIVES
  (the identical pattern passes in every prior runner); `ast.parse` + runtime ALL PASS confirm
  correctness. Do not "fix" them.
- **The C2 temporal-suffix probe:** the new additive keys `band_periods`, `band_horizon`,
  `band_capacity_attention`, and their fields (`low`/`high`/`crosses`/`flag`/`why`/`periods`) carry no
  `at|time|deadline|expires|expiry|effective|due|since` suffix, so C2 stays green (verified in the
  conformance runs).
- **`band_horizon` min/max are straightforward, but the runner must compute them from the SAME
  period list the closure uses** (not hand-authored floats) or an off-by-rounding mismatch appears.
  The runner recomputes `min(b["low"])`/`max(b["high"])` over the real `band_periods` and asserts
  equality — no drift.

## Open issues / next work (the honest frontier for Sprint 26)
- **`band_horizon` aggregates the min/max of per-period bands but the engine does not yet SURFACE it
  on the Q3 attention item** — Q6/Q8/do-nothing carry it, but the Q3 forecast-driven `why` still names
  the single worst point + single-worst band (Sprint-23/24 shape). A bounded Sprint 26 slice could add
  an additive Q3 `why` suffix naming the horizon-wide range (still data-only, strict-prefix).
- **`band_capacity_attention` is a FLAG; it does not yet drive any capacity-planning recommendation** —
  the org records a `capacity` and the flag reasons about the horizon band vs the threshold, but there
  is no capacity-deficit/RPO-style guidance. That stays out of scope unless a later sprint defines a
  recorded, additive capacity-planning rule (respecting the "never invent a capacity number" stance).
- **`"minmax"` remains the same recorded value as `"all"`** (`max(|variance|)` over the points) — an
  honest placeholder; if a future sprint wants it to mean a genuinely different recorded spread it must
  be defined as a recorded descriptor AND resolve to a recorded point magnitude (Sprint-24 finding
  stands).
- **The horizon-wide band is still a RECORDED spread, not a stochastic forecast** — a probabilistic /
  adaptive model stays explicitly out of scope of the deterministic ~$0 stance.

No normative gap surfaced -> SPEC stays v0.22.