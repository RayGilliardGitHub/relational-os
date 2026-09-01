# SPRINT 28 — SUMMARY: the capacity marker is proven at its LIMIT (at-capacity / deficit)

## Goal
Close the honest frontier Sprint 27 disclosed (`sprints/sprint-27/notes/findings.md`, "Open issues /
next work"): the Sprint-27 Q7/Q8 `capacity_constraint` marker was proven end-to-end ONLY in its
**headroom** branch on a real org (`deli-varmax-cap` → `reason:"headroom", options_flagged:{}`); its
at-capacity / deficit branches existed in the shared `_capacity_reason` helper but were never
exercised on a real §7L Q1–Q10 cockpit. This sprint drives the non-headroom branches AS DATA on real,
recorded-data orgs and asserts the full block — reason + flag + `capacity_risk` labelling — while
PROVING the marker is a LABEL at its limit (Q7 options + machine-eligible-best + Q8 recommendation
EXACTLY equal to `cockpit_q7q8`, no §6 overrule, no re-rank, no option-removal).

**Additive — recorded data + a new runner ONLY, NO engine change.** The engine's `_capacity_reason`
(deficit > at-capacity when load>=1.0 > headroom) and the Q7/Q8 `capacity_constraint` block already
fully implement all three branches; Sprint-27 simply never drove the non-headroom orgs.

## The build: `run_forecast_horizon4_demo.py` (exit 0 = ALL PASS, 94 PASS lines)
Drives SEVEN fresh orgs (. python3, ~$0, deterministic):

| org | records | Q7/Q8 `capacity_constraint` |
|---|---|---|
| `deli-forecast` | series, no capacity / no band_variance | **absent** (byte-identical) |
| `deli-varmax` | series + band, no capacity | **absent** |
| `deli-varmax-cap` | series + band + capacity 500.0 (load 0.72) | reason **headroom**, flag False, `{}` (Sprint-27 default) |
| `deli-flat2` | series, no variance/band | **absent** (no-band control) |
| `deli` | no recorded series | **absent** (no-data org) |
| **`deli-atcap`** (NEW) | cap 500.0 res/day, **load 1.25**, band `{0.62,1.02}` | reason **at-capacity**, flag True |
| **`deli-deficit`** (NEW) | **lower-is-better** latency, band `{12.0,32.0}`, cap VALUE **30.0** | reason **deficit**, flag True |

### The two NEW non-headroom orgs — exact recorded numbers (reproducible)
- **`deli-atcap` (at-capacity)**: DELI relabeled; records the same whole-series band as `deli-varmax`
  (actuals 0.92/0.90/0.87/0.86, variances -0.18/-0.09/-0.06/-0.03, `band_variance:"all"` → sigma 0.18,
  horizon `{0.62, 1.02}`, higher-is-better); `record_capacity(value=500.0, unit="resolutions/day",
  load=1.25)`. `_capacity_reason`: horizon worst-side low 0.62 < capacity 500.0 (so **not** deficit),
  recorded load 1.25 >= 1.0 → **at-capacity**, flag True.
- **`deli-deficit` (deficit)**: DELI relabeled; records a **lower-is-better** latency series
  (Sprint-23 CO points: actuals 12/14/16/18, variances 2/4/6/8, `band_variance:"all"` → sigma 8,
  projections [20,22,24], horizon `{12.0, 32.0}`); `record_capacity(value=30.0, unit="resolutions/day",
  load=0.9)`. `_capacity_reason` (lower-is-better → worst-side = high): horizon high **32.0 >=
  capacity value 30.0** → **deficit**, flag True.

## What is proven (all real exit-0 output, 94 PASS)
- **(c) The non-headroom block is fully exercised.** On BOTH `deli-atcap` and `deli-deficit`, `q7`
  AND `q8` carry an identical `capacity_constraint` block: `reason` = at-capacity / deficit,
  `flag: True`, `options_flagged` marks EVERY capacity-consuming NON-baseline option `capacity_risk`
  (7 options for the deli set: accept-customer-refund, accept-company-full-payment,
  partial-settlement, conditional-resolution, request-more-evidence, escalate, external-adjudication)
  and NEVER the baseline `unresolved` (do-nothing consumes no capacity). The `reason` equals each
  org's Q9 `capacity_planning_attention` label **BY CONSTRUCTION** (shared `_capacity_reason`), flag
  True on both.
- **(d) The marker is a LABEL at its limit.** For EVERY org — including the at-capacity and deficit
  ones — `q7.options` (same count + uris), `q7.machine_eligible_best`, and `q8.recommendation` /
  `floor_gated` are EXACTLY equal to the frozen `cockpit_q7q8` line (no §6 overrule, no re-rank, no
  option-removal). The Q8 recommendation is `partial-settlement` / machine-eligible best
  `partial-settlement` on every org, even where the recorded data shows at-capacity or deficit.
- **(b) Byte-identity / Sprint-27 regression.** The five reused orgs are byte-identical (the headroom
  org still `reason:"headroom", options_flagged:{}`; the 4 no-capacity/no-band/no-data orgs carry NO
  `capacity_constraint` on q7 or q8 and no `capacity_planning_attention`; Q3 horizon-suffix `why` +
  Q9 `capacity_planning_attention` `{flag:False, "derived headroom"}` unchanged).
- **(e) Superset byte-identity + recorded-data provenance.** The capacity orgs' Q7/Q8 pre-existing
  keys (options/baseline/machine_eligible_best/recommendation/authority/floor_gated +
  do_nothing_expected_impact) are intact; every `capacity_constraint` value traces to a recorded
  field (authority.capacity {value,load}, closure.band_horizon, recorded threshold). No wall-clock, no
  invented number.
- **(f) Determinism.** Structured dict + rendered §7L line identical on re-run for all 7 orgs.
- **(g) Real output + conformance.** New runner ALL PASS; the two new orgs' fixtures pass Sprint-0
  C1–C5 (49 `$defs`). Full non-regression green (below).

## Verification (all exit 0, plain python3 + Sprint-0 venv for conformance)
- New runner: `python3 run_forecast_horizon4_demo.py` → **RESULT: ALL PASS**.
- Full non-regression: `run_forecast_horizon3_demo` + `run_forecast_horizon2_demo` +
  `run_forecast_horizon_demo` + `run_forecast_variance_all_demo` + `run_forecast_variance_demo` +
  `run_forecast_direction_demo` + `run_forecast_action_demo` + `run_forecast_capacity_demo` +
  `run_cockpit_s7l_demo` + `run_cockpit_q7q8_demo` + `run_adjudication_engine_demo` → all ALL PASS.
- Conformances (Sprint-0 venv): `conformance_adjudication.py` (16 labels) + `conformance_dispute` +
  `conformance_interest` + `conformance_lifecycle` + `conformance_tradeoff` → all ALL PASS;
  `instances/build_all.py` + `conformance_all.py` (12 sectors) → ALL SECTORS PASS; S5 reference
  `run_s5_demo.py` + `run_s5_conformance.py` → ALL PASS; agent `run_agent_demo.py` +
  `conformance_agent.py` → ALL PASS.
- Invariants: schema JSON hash `7fc38c8c0a6e5b76cd55393f2c732417675b224812970951778853a6677642c4`
  (`7fc38c8c…`) unchanged; **49 `$defs`**; SPEC v0.22; `ros/` + schema + sector `configs.py` untouched;
  NO engine change this sprint (source-controlled change is the new runner + docs only).

## Documents rolled forward
`docs/ENGINE-FORECAST-CAPACITY.md` §12 · `docs/ENGINE-S7L-COCKPIT.md` §10 · `instances/README.md`
Sprint-28 entry · `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after
Sprint 28".

## Honest §16 verdict
**The marker is now demonstrated across ALL THREE of its derived reasons (headroom / at-capacity /
deficit) on real orgs WHILE the Q8 recommendation provably stays unchanged even at at-capacity /
deficit.** `_capacity_reason` is a shared, recorded-data rule: the Q9 `capacity_planning_attention`
label and the Q7/Q8 `capacity_constraint` reason are the same value by construction; `options_flagged`
marks capacity-consuming non-baseline options `capacity_risk` (never `capacity_infeasible`, never the
baseline); the marker never re-ranks, never removes an option, never overrules the §6 human. **Still
not derivable:** a genuinely capacity-constrained OPTIMIZATION that re-ranks the recommendation for
the machine (out of scope of the deterministic advisory stance — the §6 human always rules; the marker
never CHOOSES), and `capacity_infeasible` (structurally unreachable until a RECORDED per-option
capacity requirement exists). No SPEC bump (v0.22), no new noun.