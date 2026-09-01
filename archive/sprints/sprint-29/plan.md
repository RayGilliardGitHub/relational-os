# SPRINT 29 — PLAN: recorded PER-OPTION capacity requirement -> per-option capacity_infeasible

## Goal
Close the honest frontier Sprint 28 disclosed (`sprints/sprint-28/notes/findings.md`, "Open issues /
next work"): today the Q7/Q8 `capacity_constraint` marker can label `capacity_risk` but
`capacity_infeasible` is STRUCTURALLY UNREACHABLE because no PER-OPTION capacity requirement is ever
recorded — the engine compares the org-level recorded `load` and the horizon band's worst-side to the
recorded capacity VALUE, so it can flag a whole option set as risky but can never say a SPECIFIC
option is infeasible under capacity, and never per-option. Sprint 29 makes the recorded capacity
PER-OPTION, additively, and proves a per-option `capacity_infeasible` / `capacity_risk` label from
RECORDED numbers only.

## What already exists (Sprint 28 state, verified by reading + green baseline)
- `adjudication_engine._capacity_reason(capacity_obj, band_horizon, direction)` -> (label, flag):
  deficit (priority, horizon worst-side >= capacity VALUE) > at-capacity (load >= 1.0) > headroom.
  Shared by Q9 `capacity_planning_attention` and the Q7/Q8 `capacity_constraint.reason` — agree by
  construction.
- `cockpit_s7l` Q7/Q8 `capacity_constraint` block (Sprint 27/28): emitted where a numeric `capacity`
  + band + numeric threshold are recorded; `options_flagged` marks every capacity-consuming
  NON-BASELINE option `capacity_risk` when reason != headroom, baseline never flagged, never a
  re-rank/removal/§6 overrule, `capacity_infeasible` never emitted.
- `record_capacity(sub, authority_uri, value, unit, load)` — REPLAYABLE recorder for the additive
  authority `capacity` field (MERGE-not-replace).
- Green baseline captured FIRST: all 12 CR demo runners + conformances + build_all + S5 + agent PASS;
  schema raw sha256 `7fc38c8c0a6e5b76cd55393f2c732417675b224812970951778853a6677642c4`, 49 `$defs`,
  SPEC v0.22.

## Design — one recorded descriptor + one per-option rule (additive, engine only)
1. **Recorded per-option capacity requirement.** A NEW REPLAYABLE recorder
   `record_capacity_requirements(sub, authority_uri, requirements: dict, signer)` appends an additive
   `capacity_requirements` map (`{option: required_amount}`) MERGE-not-replace onto the SAME
   `authority://` object that already carries `capacity`. C2-safe (`capacity_requirements` has no
   temporal suffix). It is unit-coupled BY CONSTRUCTION: the authority holds both the `capacity`
   {value, unit, load} and the per-option requirements, so `available = capacity.value − capacity.load`
   derives in the SAME recorded unit. Default orgs that record NO requirements keep today's block
   EXACTLY (strict superset). The engine NEVER invents a requirement — the label only exists for
   options the org RECORDED a requirement for.
2. **Per-option infeasibility via ONE recorded rule** (additive in `cockpit_s7l`'s Q7/Q8
   `capacity_constraint` block, behind the `_capacity_reason`-gated block). When the authority carries
   a non-empty recorded `capacity_requirements`:
   - AVAILABLE = recorded capacity VALUE − recorded `load` (both recorded, same unit);
   - an option is `capacity_infeasible` iff its RECORDED requirement > available;
   - otherwise `capacity_risk` as today (a consumer with no recorded requirement, or a requirement at
     or below available, when reason != headroom);
   - the baseline (do-nothing/UNRESOLVED) is NEVER flagged (consumes none);
   - the `reason` / `flag` STILL come from the frozen org-level `_capacity_reason` rule (the label is
     per-option, the reason is org-level — unchanged);
   - a NO-requirements org keeps today's block byte-for-byte.
   Implemented as a new pure helper `_per_option_capacity_flags(...)` (no change to any frozen
   function: `rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`/`reconcile`/
   `run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate` untouched). No new URI noun, 49 `$defs`,
   SPEC v0.22, `ros/` + schema + sector configs untouched.

## The new runner: `run_forecast_per_option_capacity_demo.py` (new, exit 0 = ALL PASS)
Reuses the Sprint-28 five byte-identical orgs (`deli-forecast`, `deli-varmax`, `deli-varmax-cap`,
`deli-flat2`, `deli`) via `r26.build_orgs()` PLUS two NEW orgs that RECORD per-option requirements:

| org | records | `capacity_constraint` |
|---|---|---|
| `deli-forecast` | series, no cap / band | (reused) absent — byte-identical |
| `deli-varmax` | band, no cap | absent |
| `deli-varmax-cap` | headroom cap 500, load 0.72 | reason `headroom`, `{}` |
| `deli-flat2` | series, no variance | absent |
| `deli` | no-data | absent |
| **`deli-infcap`** (NEW) | **at-capacity** cap 500.0 res/day, **load 1.3**, VM band; records per-option `capacity_requirements` (heavy 499.0 > available 498.7 → `capacity_infeasible`; lighter ≤ available → `capacity_risk`; baseline absent) | reason **at-capacity**, flag True, per-option mix |
| **`deli-deficit-inf`** (NEW) | **deficit** lower-is-better latency cap 30.0, load 0.9, horizon {12,32}; records per-option requirements (heavy 30.0 > available 29.1 → infeasible; lighter → risk) | reason **deficit**, flag True, per-option mix |

### Exact recorded numbers for the NEW orgs (reproducible)
- **`deli-infcap`**: DELI relabeled; same whole-series band as deli-varmax (VM_POINTS, band_variance
  "all", sigma 0.18, horizon {0.62,1.02}, higher-is-better); `record_capacity(value=500.0,
  unit="resolutions/day", load=1.3)`; `record_capacity_requirements`: `accept-customer-refund`=499.0,
  `accept-company-full-payment`=499.0, `external-adjudication`=499.0 (each > available 498.7 →
  `capacity_infeasible`), `partial-settlement`=200.0, `conditional-resolution`=200.0,
  `request-more-evidence`=50.0, `escalate`=100.0 (each ≤ available 498.7 → `capacity_risk`); baseline
  `unresolved` recorded with NO requirement → never flagged. `_capacity_reason`: load 1.3 >= 1.0 (and
  worst-side low 0.62 < 500.0 so not deficit) → **at-capacity**, flag True. available = 500.0 − 1.3 =
  498.7.
- **`deli-deficit-inf`**: DELI relabeled; lower-is-better latency series (Sprint-23 CO points, sigma
  8, horizon {12.0,32.0}); `record_capacity(value=30.0, unit="resolutions/day", load=0.9)`; per-option
  requirements: `external-adjudication`=30.0, `accept-company-full-payment`=30.0,
  `accept-customer-refund`=30.0 (each > available 29.1 → `capacity_infeasible`),
  `partial-settlement`=20.0, `conditional-resolution`=20.0, `request-more-evidence`=10.0,
  `escalate`=15.0 (≤ available 29.1 → `capacity_risk`); baseline absent. `_capacity_reason`: horizon
  worst-side high 32.0 >= capacity value 30.0 → **deficit**, flag True. available = 30.0 − 0.9 = 29.1.

## Assertions (per work/2-runner-plan, items a–g)
(a) full §7L Q1–Q10 + evidence on all 7; (b) Sprint-28 byte-identity on the 5 reused orgs (headroom
org still `{reason:"headroom", options_flagged:{}}`; 4 non-capacity orgs carry NO `capacity_constraint`;
Q3 suffix + Q9 `capacity_planning_attention` unchanged); (c) per-option infeasibility derived from
RECORDED numbers: on `deli-infcap`/`deli-deficit-inf` `options_flagged` distinguishes SOME
options `capacity_infeasible` from SOME `capacity_risk`, baseline absent, `reason` still
at-capacity/deficit (org-level rule) — every infeasible/risk label traces to a recorded requirement vs
available; (d) marker still a LABEL — for EVERY org q7.options (count+uris) + machine_eligible_best +
q8.recommendation + floor_gated EXACTLY equal to `cockpit_q7q8` (no §6 overrule / no re-rank / no
removal even when an option is infeasible); (e) superset byte-identity + recorded-data provenance;
(f) determinism (dict + render); (g) emit fixtures (incl. the 2 new orgs, C1–C5 validatable) + report
`cockpit-forecast-per-option-capacity.md`.

## Verification (all exit 0; plain python3, Sprint-0 venv for conformance)
- Green baseline FIRST (Sprint-28 state — already captured above, all green).
- New runner ALL PASS. Full non-regression: run_forecast_horizon4 + horizon3 + horizon2 + horizon +
  variance_all + variance + direction + action + capacity + cockpit_s7l + cockpit_q7q8 +
  adjudication_engine demos; conformances (16-label + dispute + interest + lifecycle + tradeoff,
  Sprint-0 venv); build_all + conformance_all (12 sectors); S5 reference + conformance; agent demo +
  conformance.
- Invariants: schema raw hash `7fc38c8c…` unchanged (49 `$defs`); SPEEC v0.22; `ros/` + schema +
  sector configs untouched; ONLY `adjudication_engine.py` modified (additive: recorder +
  `_per_option_capacity_flags` + one block extension).

## Documentation (roll-forward)
- `docs/ENGINE-FORECAST-CAPACITY.md` + a §13; `docs/ENGINE-S7L-COCKPIT.md` + §11; `instances/README.md`
  Sprint-29 entry; `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after
  Sprint 29"; `sprints/sprint-29/summary.md` + `notes/findings.md`; write `sprints/sprint-30/PROMPT.md`.
- Do NOT bump SPEC (v0.22) — a per-option recorded requirement is a capability/data addition only.

## Honest §16 verdict (target)
The marker now reaches `capacity_infeasible` for a SPECIFIC option from a RECORDED per-option
requirement (available = capacity VALUE − load, same unit), while it is still a label — never a
removal, never a re-rank, never overruling the §6 human — and the Q8 recommendation provably stays
unchanged even when SOME option is infeasible. STILL NOT DERIVABLE: a genuinely capacity-constrained
OPTIMIZATION that re-ranks the recommendation for the machine (out of scope of the deterministic
advisory stance), and a per-option requirement that is NOT unit-coupled to the capacity (e.g. no
recorded capacity value/load, or an option with no recorded requirement → no infeasibility label; the
engine never invents one).

## Protocol
Single-threaded, plan-before-build (work/<n>-plan.md), real tool output only (~$0, plain python3).
Additive only. Do NOT touch `ros/`, the schema, `adjudication_configs.py`, or any frozen engine
function.