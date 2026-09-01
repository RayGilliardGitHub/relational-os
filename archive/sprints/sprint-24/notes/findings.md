# SPRINT 24 — NOTES / FINDINGS

## Assumptions that mattered
- **A recorded `band_variance` source parameter, not a computed aggregation.** The whole-series
  choices (`"all"` / `"minmax"`) both resolve to `max(|variance|)` over the recorded `points` — a pure
  function of recorded data. I deliberately did NOT implement `"minmax"` as `max(var) − min(var)`
  (a computed spread) because that would be an INVENTED number: the prompt's hard rule is *every
  possible sigma is a recorded point variance magnitude*. `max(|variance|)` is always a recorded point
  value. Honest and matches the byte-preserving constraint exactly.
- **Byte-identity via "emit `source` only when a whole-series choice is active".** The Sprint-23
  default orgs (`deli-forecast`, `deli-cost`) record no `band_variance` -> `band_source = None` ->
  the band dict has NO `source` key, no `band_variance` keys ride, no summary/why source phrase is
  added. This is what makes them byte-identical to Sprint 23 (verified against the Sprint-23 runner's
  constants). Only the whole-series org's band carries `source`, and only it carries `band_variance`.
- **`recorded_variance` still = the LAST point** (`forecast_metric.recorded_variance`). The whole-series
  sigma lives in `band["sigma"]` (and the `band_variance` source key), NOT in `recorded_variance`.
  This preserves Sprint-23 semantics for `recorded_variance`/`q6` (which render the last point to match
  `forecast_metric`) while the band prices the recorded whole-series worst-case. The runner asserts
  both facts (agreement with `forecast_metric` + whole-series max).
- **Band widening is the frontier.** `deli-varmax` proves the exact case Sprint 23 disclosed: last
  |variance| 0.03 SMALL, an EARLIER recorded |variance| 0.18 LARGER. The Sprint-23 last-point band would
  have been 0.77…0.83; Sprint 24's whole-series band is 0.62…0.98 (wider, priced from the recorded
  worst-case spread). This is the honest, data-only resolution of the collapsed-spread seam.
- **`band_variance` is the ONLY engine-file change for Sprint 24**, confined to `_forecast_closure`'s
  band block + its docstring. `render_cockpit_s7l` needed no change (its Q8 line reads `dn["band"]`
  generically and already renders the band). All frozen functions untouched.

## Verified (real tool output, all exit 0)
- Green baseline captured FIRST (Sprint-23 state, before any edit): all 5 forecast runners +
  `run_cockpit_s7l_demo` + 11 curated C-R demos + `conformance_adjudication` (16 labels) + 4 prior CR
  conformances + `build_all`/`conformance_all` + S5 reference + conformance + agent demo. Schema hash
  `7fc38c8c…`.
- After the additive change: new `run_forecast_variance_all_demo.py` -> **ALL PASS (56 assertions)**,
  and the Sprint-23/22/21/20 runners + everything in the baseline re-run -> ALL PASS.
- New org fixture `deli-varmax` passes the Sprint-0 C1–C5 conformance (26 instances, 49 `$defs`).
- Schema `relational-os.schema.json` hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` + sector
  instances untouched. `git status` confirms the only Sprint-24 source changes are
  `adjudication_engine.py` + new `run_forecast_variance_all_demo.py` (fixture churn = regenerated
  artifacts from running the runners).

## Pitfalls encountered
- **The patch tool's quote-handling can inject `\"` into a Markdown file** — writing an additive
  NOTES/README bullet with `"last"`/`"all"` literals produced literal backslash-quotes (`\"last\"`) in
  the output. Repaired by a follow-up patch with plain `"` (and `grep -c '\\"'` to confirm zero
  remaining). Rule of thumb for this repo: keep embedded straight-quote literals minimal in
  patch`new_string`, or re-patch the escapes out.
- **Pyright noise on `relabel_to`** — the recursive `_rw` JSON-rewrite helper (copied from the
  Sprint-22/23 runners) triggers a wall of `reportIndexIssue`/`reportArgumentType` type-checker errors
  on `c["label"] = ...` etc. These are FALSE POSITIVES (the identical pattern passes in every prior
  runner); `ast.parse` + runtime ALL PASS confirm correctness. Do not "fix" them.
- **The runner needs the ROS path added** exactly like its siblings (`ROS = INSTANCES.parents[0] /
  "sprints/sprint-5/artifacts"` in `sys.path`) or `from ros.substrate` fails — a common copy-paste
  miss when writing a new runner from the cartridge shape; the Sprint-23 runner has it, my first draft
  did not.
- **FLOAT-RENDERING in runner string assertions** — a whole-series sigma 0.18 renders "0.18", a
  sigma 8.0 renders "8.0" — the runner's summary-substring assertions must match the float rendering
  (they do; e.g. `recorded band 0.62…0.98 (± σ 0.18)` and `recorded band 16.0…32.0 (± σ 8.0)`).

## Open issues / next work (the honest frontier for Sprint 25)
- **The band is still around the SINGLE worst projected point**, priced at the do-nothing line; it does
  not aggregate a band across ALL projection periods or feed Q9 capacity. Sprint 23's finding stated
  this stays out of scope unless a later sprint makes it data-only + additive. A bounded Sprint 25
  slice could carry the recorded band onto Q9 capacity attention, or price a per-period worst-case
  across the horizon — still from recorded data only.
- **`"minmax"` is currently the same recorded value as `"all"`** (`max(|variance|)` over the points).
  If a future sprint wants `"minmax"` to mean a genuinely different recorded spread (e.g. the recorded
  min..max bandwidth across points used as its own magnitude), it must be defined as a recorded
  descriptor AND still resolve to a recorded point magnitude — otherwise it would invent a number and
  violate the honest stance. Kept identical here on purpose.
- **A recorded `band_variance` with NO per-point variances** falls back to the last point (the "last"
  default) — still a recorded value, but the whole-series choice is then a no-op. Correct fallback;
  could be surfaced more loudly (e.g. an additive note) in a future sprint if desirable.
- **The band remains a recorded spread, not a band over a stochastic forecast** — a stochastic/adaptive
  model stays explicitly out of scope of the deterministic ~$0 stance.

No normative gap surfaced -> SPEC stays v0.22.