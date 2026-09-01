# SPRINT 29 — SUMMARY: a RECORDED per-option capacity requirement lets the marker say `capacity_infeasible` for a SPECIFIC option

## Goal
Close the honest frontier Sprint 28 disclosed (`sprints/sprint-28/notes/findings.md`, "Open issues /
next work"): the Q7/Q8 `capacity_constraint` marker could label `capacity_risk`, but
`capacity_infeasible` was **STRUCTURALLY UNREACHABLE** because no PER-OPTION capacity requirement was
ever recorded — the engine compared the org-level recorded `load` / the horizon band's worst-side to
the recorded capacity VALUE, so it could flag a whole option set as risky but never say a SPECIFIC
option is infeasible under capacity, never price it per option. Sprint 29 makes the recorded capacity
PER-OPTION, additively, and proves a per-option `capacity_infeasible` / `capacity_risk` label from
RECORDED numbers only.

**Additive — the ONLY engine file touched is `adjudication_engine.py`.** Frozen functions
(`rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`/`reconcile`/`run_scenario`/`_derive`/
`_aggregate`/`_capacity_reason`/`SPEC_VOCAB`) untouched; no new noun; frozen 49 `$defs`; SPEC v0.22;
`ros/` + schema + sector `configs.py` untouched. A no-requirements org stays byte-identical.

## The build: `run_forecast_per_option_capacity_demo.py` (new, exit 0 = ALL PASS, 88 PASS lines)
Drives SEVEN fresh orgs — the five Sprint-28 orgs byte-identical PLUS two NEW orgs that RECORD
per-option requirements:

| org | records | Q7/Q8 `capacity_constraint` |
|---|---|---|
| `deli-forecast` / `deli-varmax` / `deli-flat2` / `deli` | (reused, no cap / no band / no-data) | **absent** (byte-identical) |
| `deli-varmax-cap` | (reused headroom cap 500, load 0.72) | reason **headroom**, flag False, `{}` — NO per-option key |
| **`deli-infcap`** (NEW) | **at-capacity** cap 500.0 res/day, load 1.3; records per-option `capacity_requirements` | reason **at-capacity**, flag True, `options_flagged` = 3 `capacity_infeasible` + 4 `capacity_risk`, baseline absent |
| **`deli-deficit-inf`** (NEW) | **deficit** lower-is-better latency cap 30.0, load 0.9; records per-option requirements | reason **deficit**, flag True, same per-option mix, baseline absent |

### The two NEW orgs — exact recorded numbers (reproducible), the per-option arithmetic
- **`deli-infcap`** (at-capacity): DELI relabeled; same whole-series band as `deli-varmax`
  (`band_variance:"all"`, sigma 0.18, horizon `{0.62,1.02}`, higher-is-better); `record_capacity(value=
  500.0, unit="resolutions/day", load=1.3)`; `record_capacity_requirements` = {accept-customer-refund:
  499.0, accept-company-full-payment:499.0, external-adjudication:499.0, partial-settlement:200.0,
  conditional-resolution:200.0, request-more-evidence:50.0, escalate:100.0}. **AVAILABLE = 500.0 − 1.3
  = 498.7** (recorded capacity VALUE − recorded load); the three 499.0 options > 498.7 →
  **`capacity_infeasible`**; the four ≤ 498.7 → `capacity_risk`. `_capacity_reason`: load 1.3 >= 1.0
  (and worst-side low 0.62 < 500.0 so NOT deficit) → **`at-capacity`**, flag True.
- **`deli-deficit-inf`** (deficit): DELI relabeled; lower-is-better latency series (Sprint-23 CO
  points: actuals 12/14/16/18, variances 2/4/6/8, `band_variance:"all"` → sigma 8, projections
  [20,22,24], horizon `{12.0,32.0}`); `record_capacity(value=30.0, unit="resolutions/day", load=0.9)`;
  `record_capacity_requirements` = {external-adjudication:30.0, accept-company-full-payment:30.0,
  accept-customer-refund:30.0, partial-settlement:20.0, conditional-resolution:20.0,
  request-more-evidence:10.0, escalate:15.0}. **AVAILABLE = 30.0 − 0.9 = 29.1**; the three 30.0 options
  > 29.1 → **`capacity_infeasible`**; the four ≤ 29.1 → `capacity_risk`. `_capacity_reason`
  (lower-is-better → worst-side high): horizon high **32.0 >= capacity value 30.0** → **`deficit`**,
  flag True.

The baseline (`unresolved` / do-nothing) RECORDS NO requirement and is NEVER flagged on either.

## What is proven (all real exit-0 output, 88 PASS)
- **(c) Per-option infeasibility derived from RECORDED numbers.** On BOTH new orgs, `q7` and `q8`
  carry an identical `capacity_constraint` block with `reason` at-capacity / deficit (org-level rule
  unchanged), `flag: True`, `options_flagged` DISTINGUISHES 3 `capacity_infeasible` from 4
  `capacity_risk`, the baseline never flagged, and the block surfaces the recorded
  `per_option_requirements` map + `available_capacity` (498.7 / 29.1). Every `capacity_infeasible`
  option's RECORDED requirement > available; every `capacity_risk` option's ≤ available — asserted
  arithmetically in the runner. The `reason` equals each org's Q9 `capacity_planning_attention` label
  BY CONSTRUCTION (shared `_capacity_reason`).
- **(d) The marker is STILL a LABEL.** For EVERY org — including the two where a SPECIFIC option is
  infeasible — `q7.options` (count 8 + uris), `q7.machine_eligible_best`, `q8.recommendation`, and
  `q8.floor_gated` are EXACTLY equal to `cockpit_q7q8`; the Q8 recommendation stays
  `partial-settlement` and machine-eligible best `partial-settlement` even when some option is
  `capacity_infeasible`. No §6 overrule, no re-rank, no option-removal.
- **(b) Byte-identity / Sprint-28 regression.** The five reused orgs carry the exact Sprint-28 output
  (the headroom org still `{reason:"headroom", flag:False, options_flagged:{}}` and NOW no
  `per_option_requirements`/`available_capacity` key; the 4 no-capacity/no-band/no-data orgs carry NO
  `capacity_constraint`; Q3 horizon-suffix + Q9 `capacity_planning_attention` unchanged).
- **(e) Superset byte-identity + recorded-data provenance.** A no-requirements org keeps today's block
  EXACTLY (strict superset); every `capacity_infeasible`/`capacity_risk` label traces to a recorded
  field (authority.capacity {value,load} + authority.capacity_requirements); `available_capacity` ==
  recorded capacity VALUE − recorded load.
- **(f) Determinism.** Structured dict + rendered §7L line identical on re-run for all 7 orgs.
- **(g) Real output + conformance.** New runner ALL PASS; both new orgs' fixtures pass Sprint-0 C1–C5
  (26 instances each, 49 `$defs`); full non-regression green.

## Verification (all exit 0, plain python3 + Sprint-0 venv for conformance)
- New runner: `python3 run_forecast_per_option_capacity_demo.py` → **RESULT: ALL PASS** (88 PASS).
- Full non-regression: `run_forecast_horizon4`/`horizon3`/`horizon2`/`horizon`/`variance_all`/
  `variance`/`direction`/`action`/`capacity`/`cockpit_s7l`/`cockpit_q7q8`/`adjudication_engine` demos →
  ALL PASS; conformances (Sprint-0 venv) `conformance_adjudication` (16 labels) + `conformance_dispute`
  + `conformance_interest` + `conformance_lifecycle` + `conformance_tradeoff` → ALL PASS;
  `instances/build_all.py` + `conformance_all.py` (12 sectors) → ALL SECTORS PASS; S5 reference
  `run_s5_demo.py` + `run_s5_conformance.py` → ALL PASS; agent `run_agent_demo.py` +
  `conformance_agent.py` → ALL PASS.
- Invariants: schema raw hash `7fc38c8c…` unchanged; **49 `$defs`**; SPEC v0.22; `ros/` + schema +
  sector `configs.py` untouched; the ONLY source change is `adjudication_engine.py` (additive:
  `record_capacity_requirements` recorder + `_per_option_capacity_flags` helper + the additive
  extension of the Q7/Q8 `capacity_constraint` block) + the new runner.

## Documents rolled forward
`docs/ENGINE-FORECAST-CAPACITY.md` §13 · `docs/ENGINE-S7L-COCKPIT.md` §11 · `instances/README.md`
Sprint-29 entry · `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after
Sprint 29" · `references/` updated via the relational-os skill note (below).

## Honest §16 verdict
**Sprint 28's frontier is closed: the marker now reaches `capacity_infeasible` for a SPECIFIC option
from a RECORDED per-option requirement + a recorded available number only.** The new REPLAYABLE
recorder `record_capacity_requirements` appends an additive `capacity_requirements` map on the SAME
`authority://` object as the recorded `capacity` — so `available = recorded capacity VALUE − recorded
load`, unit-coupled by construction — and the Q7/Q8 `capacity_constraint` block labels an option
`capacity_infeasible` iff its recorded requirement > available, else `capacity_risk`. Proven on real
orgs: `deli-infcap` (at-capacity; heavy 499.0 > 498.7) and `deli-deficit-inf` (deficit; heavy 30.0 >
29.1), each with some `capacity_risk`, baseline never flagged. **It is still a LABEL:** never a removal,
never a re-rank, never an overrule of the §6 human — the Q8 recommendation provably stays `partial-
settlement` even when SOME option is infeasible. Orgs that record NO per-option requirement keep the
Sprint-28 block byte-identical (strict superset). **Still not derivable (the honest frontier):** a
genuinely capacity-constrained OPTIMIZATION that RE-RANKS the recommendation for the machine stays out
of scope of the deterministic advisory stance (the marker never CHOOSES), and a per-option requirement
that is NOT unit-coupled to the capacity remains non-derivable (an org with no recorded capacity
value/load, or an option with no recorded requirement, carries no infeasibility label — the engine never
invents one). No SPEC bump (v0.22), no new noun.