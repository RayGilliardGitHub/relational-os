# SPRINT 30 — PLAN: the sharpest label-vs-choice boundary (a RECOMMENDED option made capacity_infeasible)

## Goal / what we are proving
Close the honest frontier Sprint 29 disclosed: the per-option `capacity_infeasible` marker can NAME a
single option from a recorded requirement, but it **never CHOOSES a different option for the machine** —
the §6 human always rules. Sprint 30 demonstrates the sharpest version of that boundary ON A REAL ORG:
the recorded per-option requirement makes the **frozen machine-eligible best / Q8 recommendation itself**
(`partial-settlement`) `capacity_infeasible`, yet the cockpit **STILL recommends partial-settlement**
(provably exactly `cockpit_q7q8`). The marker says "the recorded capacity says the recommended option
can't run" AS DATA; it does not pick a replacement. A capacity-constrained OPTIMIZATION that re-ranks
the recommendation is named honestly as out of scope (a policy/user decision, not a label).

Key finding driving the design: **NO engine change is required.** Sprint 29's `_per_option_capacity_flags`
already labels ANY option (including the recommended one) `capacity_infeasible` when its recorded
requirement > available. So Sprint 30 is pure recorded-data + a new runner + the boundary proof + docs.
`adjudication_engine.py` stays byte-identical (verified by the baseline capturing its hash).

## The new org: `deli-recommend-infcap`
DELI relabeled (same 8 options, weights, reconcile, floor gate) — `partial-settlement` is the
machine-eligible best / Q8 recommendation (utility 0.7275, non-gated, verified pre-plan).
RECORDS (reproducible, exactly):
- `record_metric_series` — the Sprint-29 `deli-infcap` whole-series band (VM points, `band_variance:"all"`,
  target 0.95, higher-is-better) -> horizon band {0.62, 1.02}.
- `record_capacity(value=500.0, unit="resolutions/day", load=1.3)`  -> at-capacity (load 1.3 >= 1.0).
- `record_capacity_requirements` = {accept-customer-refund:499.0, accept-company-full-payment:499.0,
  external-adjudication:499.0, partial-settlement:499.0, conditional-resolution:200.0,
  request-more-evidence:50.0, escalate:100.0}.
  AVAILABLE = 500.0 − 1.3 = **498.7**. The FOUR 499.0 options (INCLUDING `partial-settlement`, the
  recommendation) > 498.7 -> **`capacity_infeasible`**; the three ≤ 498.7 -> `capacity_risk`;
  baseline `unresolved` records NO requirement -> NEVER flagged. `_capacity_reason`: load 1.3 >= 1.0 and
  worst-side low 0.62 < 500.0 (not deficit) -> **`at-capacity`**, flag True.
- The 4 `capacity_infeasible` options are exactly those whose recorded requirement 499.0 > 498.7:
  `{partial-settlement, accept-customer-refund, accept-company-full-payment, external-adjudication}`.

## The proof (the marker is a REASON, never a CHOICE)
On `deli-recommend-infcap` assert:
1. `capacity_constraint.options_flagged["partial-settlement"] == "capacity_infeasible"` (the RECOMMENDED option).
2. `q7.options` (count 8 + uris) + `q7.machine_eligible_best == "partial-settlement"` + `q8.recommendation ==
   "partial-settlement"` + `q8.floor_gated` EXACTLY equal `cockpit_q7q8`. The Q8 recommendation is STILL
   partial-settlement even though options_flagged marks it `capacity_infeasible`.
3. The `capacity_constraint.note` names the UNCHANGED Q8 + the §6 human (marker labels "this recommended
   option cannot run"; it does NOT pick a replacement).
4. `reason == "at-capacity"` == Q9 `capacity_planning_attention` label BY CONSTRUCTION (shared `_capacity_reason`).
5. `44` (4 infeasible incl. recommended + 3 risk) partition `non_baseline`, baseline absent.

## Regression (Sprint 29 byte-identity)
Reuse `r29.build_orgs()`'s seven orgs and assert the reused orgs carry the EXACT Sprint-29 output:
- `deli-infcap` / `deli-deficit-inf` with the same `{reason, flag, options_flagged, per_option_requirements,
  available_capacity}` (byte-identical) — proves the new runner added the exact Sprint-29 blocks.
- `deli-varmax-cap` headroom `{reason:"headroom", flag:False, options_flagged:{}}`, NO per-option/available keys.
- the 4 no-capacity orgs (`deli-forecast`, `deli-varmax`, `deli-flat2`, `deli`): NO `capacity_constraint`.
- a no-requirements org keeps today's block exactly (strict superset — no new key leaks).
- Q3 horizon-suffix + Q9 `capacity_planning_attention` unchanged.

## Runner: `run_forecast_label_vs_choice_demo.py` (new, exit 0 = ALL PASS)
- Reuses `r29` build_orgs + its seven orgs + `_new_per_option_org` builders/constants, plus the new org.
- Asserts the per-org label-vs-choice block + full label-vs-choice proof above + byte-identity regression +
  determinism (dict + render) + recorded-data provenance.
- Emits fixtures for the new org + `artifacts/adjudication/reports/cockpit-label-vs-choice.md`.
- Imports: `run_forecast_per_option_capacity_demo as r29`, `run_forecast_horizon_demo as rfh`,
  `adjudication_configs as ac`, `adjudication_engine as eng`.

## Mandatory verification (all real exit 0)
- Green baseline FIRST (capture it): run, plain python3, all 13 CR demo runners from Sprint 29's list +
  the 5 CR conformances (Sprint-0 venv) + `build_all.py` + `conformance_all.py` + S5 reference
  demo/conformance + agent demo/conformance. Record schema raw sha256.
- New runner ALL PASS.
- Full non-regression re-run after (all of the above still green).
- Invariants: 49 `$defs`, URI cap, SPEC v0.22, `ros/` + schema + sector `configs.py` untouched, NO source
  change to `adjudication_engine.py` (additive recorded-data only).

## Docs to roll forward (additive)
`docs/ENGINE-FORECAST-CAPACITY.md` §14 · `docs/ENGINE-S7L-COCKPIT.md` §12 · `instances/README.md`
Sprint-30 entry · `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after
Sprint 30" note · the relational-os skill note (this story).

## §16 verdict (honest)
The marker now reaches the RECORDED per-option limit at its sharpest: the recommended option itself is
`capacity_infeasible`, and the cockpit provably STILL recommends it (exactly `cockpit_q7q8`) — the marker
is a REASON, never a CHOICE; the §6 human always rules. What is still NOT derivable: a capacity-constrained
OPTIMIZATION that RE-RANKS the recommendation for the machine stays out of scope of the deterministic
advisory stance (that is a policy/user decision, not a label); a per-option requirement NOT unit-coupled to
the recorded capacity / an option with no recorded requirement stays non-derivable. No SPEC bump (v0.22).

## Deliverables / checklist
[ ] plan.md (this file, done first)
[ ] work/1-green-baseline.md then capture green baseline
[ ] work/2-runner-plan.md before writing the runner
[ ] run_forecast_label_vs_choice_demo.py -> ALL PASS
[ ] full non-regression green
[ ] docs §14/§12 + README + STRESS-TEST
[ ] summary.md + notes/findings.md + sprints/sprint-31/PROMPT.md