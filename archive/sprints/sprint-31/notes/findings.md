# SPRINT 31 — NOTES / FINDINGS

## Assumptions that mattered
- **NO engine change.** Sprint 31 is a POSITIVE CONSOLIDATION, not a capability sprint: after six
  sprints (20-30) the whole §7L decision surface is recorded-data + reason, so the deliverable is a
  survey/boundary RUNNER that inventories it and proves reason-not-choice in one auditable run.
  `adjudication_engine.py` sha256 = `a60f8f7…` verified BEFORE and AFTER — identical. Pure recorded
  data + a new runner, exactly the Sprint-30 proof shape.
- **The reusable org set is the eight from Sprint 30** (`r30.build_orgs()`), and the sprint genuinely
  needs THREE new orgs to bound the surface: INSPECT (a different options/weights/rule org),
  COVE (a different business model + a lower-is-better latency series), and one no-data control org.
  All NEW labels (`inspect-recorded`, `cove-recorded`, `inspect-nodata`) so no existing fixture dir is
  overwritten. This gives the inventory breadth beyond DELI-relabels.
- **reason-to-descriptor trace map** is the inventory's target: Q3_forecast / Q6_projection /
  Q8_do_nothing_impact all trace to `metric_series`; Q7Q8_capacity_constraint / Q9_capacity trace to
  `capacity`. The no-data org (records no series and no capacity) must therefore derive NOTHING — the
  strongest "the engine never invents a reason" proof.
- **`floor_gated`/`weights`/`reconcile_rule` are config descriptors, present in EVERY org**, so the
  no-data org still shows them present — that is the correct semantics (they are authored config, not
  recorded data). The "nothing derivable" assertion had to check only the five RECORDED descriptors
  (metric_series/point_variance/band_variance/capacity/capacity_requirements), not the config fields.

## Verified (real tool output, all exit 0)
- **Green baseline captured FIRST** (Sprint-30 state): all 14 prior CR demo runners + all 5 CR
  conformances (Sprint-0 venv) + `build_all`/`conformance_all` (12 sectors) + S5 reference demo +
  conformance + agent demo + conformance → ALL PASS. Schema raw sha256 `7fc38c8c…`, 49 `$defs`,
  SPEC v0.22. Note: `conformance_all.py` + `run_s5_conformance.py` + all CR conformances REQUIRE the
  Sprint-0 venv (jsonschema) — `python3` gives `ModuleNotFoundError`; use the absolute venv path.
- **New runner** `run_recorded_surface_demo.py` → **RESULT: ALL PASS**. Key outputs:
  - All 11 orgs emit a `recorded_surface` ({present_recorded, derived_reasons, derivable_universe,
    not_derivable}).
  - **Every derived reason traces to a recorded descriptor** for every org (missing-trace=[] on all).
  - No-data org `inspect-nodata`: derived=[] and all five recorded descriptors False — NOTHING derivable.
  - Capacity-derived reasons present iff a capacity is recorded — True for all 11.
  - **Reason-not-choice tally: 11/11 orgs Q7/Q8 EXACTLY == `cockpit_q7q8`; INCLUDES the Sprint-30 org
    `deli-recommend-infcap` where the RECOMMENDED option is `capacity_infeasible`.**
  - Determinism (dict + render) on re-run for all 11.
- **New-org fixtures pass Sprint-0 C1-C5** (the no-data org correctly emits no fixtures — 0 instances,
  C3 skip — which is the honest empty surface). Full non-regression still green after the new runner.
- Engine hash `a60f8f7…` unchanged; schema `7fc38c8c…`; 49 `$defs`; SPEC v0.22; `ros/` + schema +
  sector `configs.py` untouched; none of the three new fixture dirs contains `://qk/`.

## Pitfalls encountered
- **The Sprint-0 conformance's FIXTURES override is label-driven, not global**: `conformance_adjudication.py`
  loops its OWN `labels` tuple, so monkeypatching `conformance.FIXTURES` in the runner's process doesn't
  reach the new orgs. Validate new orgs against the C1-C5 validator directly: set `conformance.FIXTURES`
  = the new fixture dir + call `conformance.Conformance().run()` (I did this via a small throwaway
  script). The `inspect-nodata` no-data org correctly yields 0 instances / no ledger — that is the
  honest empty surface, not a failure.
- **The `conformance` module lives at `sprints/sprint-0/artifacts/`, not the runner cwd** — a bare
  `import conformance` from the contested_reality dir fails; add `sprints/sprint-0/artifacts` to
  `sys.path` and use the Sprint-0 venv.
- **A module-vs-local naming `/ dict-vs-f-string` trap** in the new runner's final print (a `%`-format
  split across two adjacent strings) surfaced as a SyntaxError — switched to a clean f-string (the
  known Sprint-13 trailing-comma/dict lesson family). Also initial REQS values for `inspect-recorded`
  had 2 infeasible-only-by-assert (460/490 were NOT all > 498.7) — the run-time assert caught it and I
  set all three heavy options genuinely > available (500/499/510). Assertions exist to catch this.
- **No `{{` placeholder leak** — grep `{{` = 0 across all four doc files (re-read after paged patches;
  the S7L §13 append had a duplicated "the the" from a fuzzy patch — caught and fixed).
- **Pyright noise** on the runner (unresolved `ros.substrate`, optional-dict `not in`/`-` on None) is the
  known, expected artifact of the runtime `sys.path` injection + optional dict access — identical to
  every CR runner; not a defect.

## Open issues / next work (the honest frontier after Sprint 31)
- **The WHOLE recorded-data §7L decision surface is now positively inventoried as reason-not-choice** —
  every derived label (Q3 forecast attention, Q6 projection + band, Q7/Q8 capacity_constraint reason +
  per-option flags, Q9 capacity planning, Q8 do-nothing expected-impact) provably traces to a RECORDED
  descriptor, and the Q8 recommendation provably stays the frozen `rank` output for all 11 orgs (no
  recorded data ever re-ranks).
- **The ONE remaining out-of-scope step is a capability, not a consolidation:** a capacity-constrained
  OPTIMIZATION that RE-RANKS the Q8 recommendation for the machine — a "re-rank for the machine"
  POLICY / user decision, NOT a label, deliberately NOT built. The seam is fully spelled: recorded
  per-option `capacity_requirements` already exist; the ONLY missing piece is a deterministic
  next-best-non-infeasible rule by the frozen `rank` utility (pick the highest-utility option not
  labeled `capacity_infeasible`); it CHANGES the Q8 recommendation and does NOT fit a label. A future
  sprint build of that optimization is a deliberate capability change requiring the prompt author to
  explicitly ask for it.
- **Non-derivable residuals that remain honest:** a per-option requirement NOT unit-coupled to the
  recorded capacity (no capacity VALUE to subtract) / an option with no recorded requirement carries no
  infeasibility label — the engine never invents one. An org with no recorded series gets no Q6
  projection / no Q3 forecast / no Q8 do-nothing pricing. `band_variance:"minmax"` still equals `"all"`;
  the band remains a recorded spread, not a stochastic forecast.

No normative gap surfaced -> SPEC stays v0.22.