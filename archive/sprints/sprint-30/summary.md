# SPRINT 30 — SUMMARY: the label-vs-choice boundary at its sharpest — a RECORDED per-option requirement makes the RECOMMENDED option `capacity_infeasible`, yet the cockpit provably STILL recommends it

## Goal
Close the honest frontier Sprint 29 disclosed (`sprints/sprint-29/notes/findings.md`, "Open issues /
next work"): the per-option `capacity_infeasible` marker NAMES a specific option from a recorded
requirement, but **it still never CHOOSES a different option for the machine — the §6 human always
does.** In every Sprint-29 org the machine-eligible best (`partial-settlement`) was itself
`capacity_risk` (recorded requirement ≤ available), so the label-vs-choice boundary had never been
exercised at its sharpest — when the recorded capacity CLEARLY says the option the machine WOULD
recommend is itself `capacity_infeasible`. Sprint 30 drives THAT story on a real org and proves the
marker is a REASON, never a CHOICE: the Q8 recommendation provably stays unchanged even when it is
itself marked `capacity_infeasible`.

**Key finding: NO engine change is required.** Sprint 29's `_per_option_capacity_flags` already labels
ANY option (including the recommended one) `capacity_infeasible` when its recorded requirement >
available. Sprint 30 is pure recorded data + a new runner + the boundary proof + docs.
`adjudication_engine.py` is byte-identical (sha256 `a60f8f7…` confirmed before and after). No new noun;
frozen 49 `$defs`; SPEC v0.22; `ros/` + schema + sector `configs.py` untouched; ~$0.

## The build: `run_forecast_label_vs_choice_demo.py` (new, exit 0 = ALL PASS)
Drives EIGHT orgs — the seven Sprint-29 orgs byte-identical PLUS one NEW org that RECORDS a per-option
requirement making the RECOMMENDED option itself infeasible:

| org | records | Q7/Q8 `capacity_constraint` |
|---|---|---|
| `deli-forecast` / `deli-varmax` / `deli-flat2` / `deli` | (reused, no cap / no band / no-data) | **absent** (byte-identical) |
| `deli-varmax-cap` | (reused headroom cap 500, load 0.72) | reason **headroom**, flag False, `{}` — NO per-option key |
| `deli-infcap` / `deli-deficit-inf` | (reused, at-capacity / deficit with per-option reqs) | **byte-identical** to Sprint 29 |
| **`deli-recommend-infcap`** (NEW) | **at-capacity cap 500.0 res/day, load 1.3 → available 498.7**; records per-option requirements where the machine-eligible best / Q8 recommendation is the infeasible one | reason **at-capacity**, flag True, `options_flagged` = **`{partial-settlement: capacity_infeasible}`** (the RECOMMENDED) + 6 `capacity_risk`, baseline absent |

### The NEW org — exact recorded numbers (reproducible), the per-option arithmetic
- **`deli-recommend-infcap`**: DELI relabeled; the same whole-series band as `deli-varmax`/`deli-infcap`
  (`band_variance:"all"`, VM points, target 0.95, higher-is-better, horizon `{0.62,1.02}`);
  `record_capacity(value=500.0, unit="resolutions/day", load=1.3)`; `record_capacity_requirements` =
  {partial-settlement:499.0, conditional-resolution:200.0, accept-customer-refund:200.0,
  accept-company-full-payment:200.0, external-adjudication:100.0, request-more-evidence:50.0,
  escalate:80.0}. **AVAILABLE = 500.0 − 1.3 = 498.7**.
- **`partial-settlement` (the machine-eligible best, utility 0.7275, non-gated — the Q8 recommendation)
  RECORDS 499.0 > 498.7 → `capacity_infeasible` ON THE RECOMMENDED OPTION.** The other 6 non-baseline
  options ≤ 498.7 → `capacity_risk`; the `unresolved` baseline (no recorded requirement) → **never
  flagged**. `_capacity_reason`: load 1.3 >= 1.0 (and worst-side low 0.62 < 500.0 so NOT deficit) →
  **`at-capacity`**, flag True.

## What is proven (all real exit-0 output)
- **(a) The sharpest label-vs-choice boundary, on a real org.** `deli-recommend-infcap`'s Q7/Q8
  `capacity_constraint` (`reason` at-capacity, flag True, `available_capacity` 498.7, the recorded
  `per_option_requirements`) marks `partial-settlement` — the machine-eligible best / Q8
  recommendation — `capacity_infeasible`, with 6 `capacity_risk` and the baseline never flagged. The
  record clearly says the option the machine WOULD recommend cannot run under recorded capacity.
- **(b) The marker is a REASON, never a CHOICE.** On `deli-recommend-infcap`, `q8.recommendation` and
  `q7.machine_eligible_best` are STILL `partial-settlement`; `q7.options` (count 8 + uris) +
  `machine_eligible_best` + `q8.recommendation` + `floor_gated` EXACTLY equal `cockpit_q7q8` (no re-rank,
  no removal, no §6 overrule); the `capacity_constraint.note` names the UNCHANGED Q8 + the §6 human. The
  marker LABELS "the recorded capacity says the recommended option can't run"; it does NOT pick a
  replacement — the §6 human must.
- **(c) Byte-identity / Sprint-29 regression.** The seven reused orgs carry the EXACT Sprint-29 output
  (`deli-infcap`/`deli-deficit-inf` byte-identical with the same `{reason, flag, options_flagged,
  per_option_requirements, available_capacity}`; `deli-varmax-cap` `{reason:"headroom", flag:False,
  options_flagged:{}}` no per-option keys; the 4 no-capacity orgs carry NO `capacity_constraint`). A
  no-requirements org keeps today's block exactly (strict superset — no new key leaks).
- **(d) Recorded-data provenance.** Every label traces to a recorded field
  (authority.capacity {value,load} + authority.capacity_requirements); `available_capacity` == recorded
  capacity VALUE − recorded load == 498.7; the recommended option's infeasibility is 499.0 (recorded) >
  498.7.
- **(e) Determinism.** Structured dict + rendered §7L line identical on re-run for all 8 orgs.
- **(f) Real output + conformance.** New runner ALL PASS; the new org's fixtures pass Sprint-0 C1–C5
  (26 instances, 49 `$defs`); full non-regression green; `adjudication_engine.py` hash unchanged
  (`a60f8f7…`); schema hash `7fc38c8c…`, 49 `$defs`, SPEC v0.22, `ros/` + schema + sector configs
  untouched, no new noun.

## Verification (all exit 0, plain python3 + Sprint-0 venv for conformance)
- NEW runner: `python3 run_forecast_label_vs_choice_demo.py` → **RESULT: ALL PASS**.
- Full non-regression (captured twice — once as the Sprint-29 green baseline, once after the new runner):
  `run_forecast_per_option_capacity` (Sprint 29) + `horizon4`/`horizon3`/`horizon2`/`horizon`/
  `variance_all`/`variance`/`direction`/`action`/`capacity`/`cockpit_s7l`/`cockpit_q7q8`/
  `adjudication_engine` demos → ALL PASS; conformances (Sprint-0 venv) `conformance_adjudication` (16
  labels) + `dispute` + `interest` + `lifecycle` + `tradeoff` → ALL PASS; `build_all.py` +
  `conformance_all.py` (12 sectors) → ALL PASS; S5 reference `run_s5_demo.py` + `run_s5_conformance.py`
  → ALL PASS; agent `run_agent_demo.py` + `conformance_agent.py` → ALL PASS.
- Invariants: schema raw sha256 `7fc38c8c0a6e5b76cd55393f2c732417675b224812970951778853a6677642c4`
  unchanged; **49 `$defs`**; SPEC v0.22; `ros/` + schema + sector `configs.py` untouched; `adjudication_engine.py`
  byte-identical (hash `a60f8f7…`); no `://qk/` in the config-driven fixtures (only the legacy
  hand-written `instances/financial/` v1, which is not a `configs.py` entry).

## Documents rolled forward
`docs/ENGINE-FORECAST-CAPACITY.md` §14 · `docs/ENGINE-S7L-COCKPIT.md` §12 · `instances/README.md`
Sprint-30 entry · `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after
Sprint 30" · the `relational-os` skill note (below).

## Honest §16 verdict
**Sprint 29's frontier is closed at its sharpest: the marker now reaches a RECORDED per-option
requirement that makes the machine-eligible best / Q8 recommendation ITSELF (`partial-settlement`)
`capacity_infeasible` (recorded 499.0 > available 498.7), and the cockpit provably STILL recommends
`partial-settlement` — exactly `cockpit_q7q8`, no re-rank, no removal, no §6 overrule.** The marker is
a REASON, never a CHOICE: it says "the recorded capacity says the recommended option can't run," and the
§6 human (not the machine) must choose the replacement (or overrule). This is generic + additive — a
recorded `metric://` series + recorded point-`variance` + the recorded `band_variance` source + a
recorded authority `capacity` + a recorded per-option `capacity_required` descriptor; no new noun, frozen
49 `$defs`, and the engine is provably UNCHANGED (a new runner + recorded data only). **Still not
derivable (the honest frontier):** a capacity-constrained OPTIMIZATION that RE-RANKS the recommendation
for the machine stays out of scope of the deterministic advisory stance — choosing a different option for
the machine is a policy / user decision, NOT a label; and a per-option requirement that is NOT
unit-coupled to the recorded capacity / an option with no recorded requirement remains non-derivable (the
engine never invents one). That optimization seam is spelled out in the findings: recorded per-option
requirements already exist, so a deterministic next-best-non-infeasible rule by the frozen `rank` utility
would be the *only* missing piece — and it is deliberately out of scope unless the prompt author asks for
it. No SPEC bump (v0.22), no new noun.