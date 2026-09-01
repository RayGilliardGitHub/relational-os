# SPRINT 21 — PROMPT (the honest frontier Sprints 13–20 disclosed: the Q6 forecast is computed but not CONNECTED to what the org does about it)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 13–20 built a configurable adjudication engine (`instances/contested_reality/
`adjudication_engine.py`): a config-authorable reconciliation RULE (registry → declarative `rule_spec`
DSL → cross-org `RULE_LIBRARY` → rule learning), a first-class §7L Q7/Q8 line (Sprint 18), the FULL
§7L Q1–Q10 morning cockpit rendered BY the engine, data-only (Sprint 19), and — Sprint 20 — **recorded-data
Q6 FORECAST and Q9 CAPACITY** (`forecast_metric` + `record_metric_series`/`record_capacity`: an org that
records a `metric://` realized-vs-expected series and a `capacity` field on its `authority://` gets a
deterministic Q6 projection and a Q9 capacity number AS DATA, with the honest no-data fallback unchanged).
**Sprint 20's own finding (see `sprints/sprint-20/notes/findings.md`, "Residual seams") discloses the next
honest frontier: the Q6 projection is COMPUTED and RENDERED but not CONNECTED to the org's decision
surface** — a projected deterioration ("if nothing changes") does not by itself change Q3 attention or the
Q8 expected-impact / trade-off "do-nothing" cost, even though §7K.1's Decision→Expected→Variance→WHY loop and
§7J.5 attention exist precisely to turn a measured/forecast gap into prioritized action. Sprint 21 closes a
bounded slice of that: make the RECORDED forecast DRIVE the attention + the expected-impact of the Q8
recommendation (via the trade-off's do-nothing baseline), all deterministically from the recorded-data
surfaces Sprint 20 built — same data-only discipline, no §6 overrule, no new noun.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7J.5 (attention), §7J.9
  (cockpit/authority), §7K.1 (Policy, Trade-off, Organizational Learning, Ownership, Forecast —
  Decision→Expected→Actual→Variance→WHY→change-future-policy), §7L (the ten morning questions with their
  evidence requirements), §7J.11 + §C16 (URI cap). The reference sector BI (`sprints/sprint-5/artifacts/
  reports/cockpit.md`) shows on-time projected + the §7K.1 forecast-to-action idiom (a forecast below target
  → an attention item → a re-balance #8 recommendation with an expected impact).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  best-effort ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — esp. `cockpit_s7l` (the `.q3`, `.q6`, `.q8`
    blocks), `forecast_metric`, `_recorded_metric_with_series`, `rank`/`machine_eligible_best`/
    `render_tradeoff`, and `cockpit_q7q8` (do NOT rewrite the frozen functions: `reconcile`,
    `run_scenario`, `_derive`, `SPEC_VOCAB`, `_aggregate`, `rank`, `machine_eligible_best`,
    `render_tradeoff`, `cockpit_q7q8`).
  - `run_forecast_capacity_demo.py` (Sprint 20 runner — how it RECORDS a metric series + capacity on a new
    org `deli-forecast`, and drives the no-data `deli` control), `adjudication_configs.py`
    (DELI/COVE/INSPECT + variants, `RULE_LIBRARY`), `reconcile_learning.py`.
  - `sprints/sprint-20/summary.md` + `notes/findings.md` (esp. the "Residual seams" paragraph) and
    `docs/ENGINE-FORECAST-CAPACITY.md` + the Sprint-20 appendix in `docs/ENGINE-S7L-COCKPIT.md`.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16); additive
  only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get one-arg,
  `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2 RFC3339
  temporal-suffix keys — never name an additive field ending in `at|time|deadline|expires|expiry|effective|
  due|since` — strict C5 tables, `eng.reconcile(sub, cfg)` ARG ORDER, the Sprint-0 venv
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance, runner
  CWD-sensitivity, the `[0]`-indexed `parents` for the Sprint-0 path, json round-trip converts `floor_gated`
  sets — restore them).

## What Sprint 21 IS and IS NOT
- **IS:** make the RECORDED Q6 forecast (Sprint 20's `forecast_metric` result) **drive the §7L Q3
  attention and the Q8 expected-impact / trade-off do-nothing cost**, deterministically and data-only: (i)
  when the recorded series is present and its **horizon projection crosses a recorded threshold** (e.g. the
  metric's own `target`, or an explicit `forecast_threshold` additive field, or the projected value falls
  below the last `actual`/`target`), `cockpit_s7l`'s Q3 `prioritized` gains a **forecast-driven attention
  item** (the projected-to-break metric, tagged `forecast`), so a "do nothing and it gets worse" signal is
  itself attention; and (ii) Q8's recommendation block + the trade-off's **do-nothing expected-impact**
  carry the projected cost (the deterministic projection), so "what should we do?" and its trade-off are
  grounded in the recorded forecast where it exists — with the honest no-data fallback unchanged (an org
  without a recorded series keeps today's Q3/Q8 exactly). Prove it with a runner that drives the Sprint-20
  `deli-forecast` org (recorded series THAT DETERIORATES: its trend crosses the 0.95 target) and a control
  org whose recorded series is FLAT/above-target (no forecast-driven attention, no projected-cost trade-off)
  plus a no-data org (Sprint-20 `deli`), and asserts the full §7L on each plus the projection→attention→
  expected-impact closure, determinism, agreement with the recorded series, and no §6 overrule.
- **IS NOT:** a new service, a new URI noun, a schema/`$defs` edit, a Trust change (S5), a change that lets
  the machine overrule the §6 human (a forecast-driven Q3 item is ATTENTION — Q8's recommendation stays the
  §6-floor-gated machine-eligible best and the determination stays the §6 human's `determination_policy`
  call; the forecast only prices the do-nothing baseline, never auto-picks an action), a re-implementation
  of `run_scenario`/`reconcile`/`cockpit_q7q8`, an adaptive/learned forecast model, or any wall-clock/
  best-guess. **The §L gate** ("#8 becomes authorized work") is NOT re-litigated — Sprint 19 met it; this
  hardens the forecast-to-action seam as data. No frontier spend.

## The target (what "done" looks like)
1. An additive, generic **forecast→attention→expected-impact closure** in the engine: `cockpit_s7l`'s `.q3`
   adds a forecast-driven attention item (tagged `forecast`) when the recorded series' horizon projection
   crosses a recorded threshold, and `.q8`/the trade-off carry the projected-cost of doing nothing, all
   deterministic from the recorded `metric://` series + `forecast_metric` (no wall-clock). No-data orgs keep
   today's Q3/Q8/trade-off exactly.
2. `render_cockpit_s7l` renders the new Q3 item + the projected-cost do-nothing on Q8/trade-off where present.
3. A runner (`run_forecast_action_demo.py`, exit 0 = ALL PASS) that drives ≥3 orgs: the Sprint-20
   `deli-forecast` (deteriorating recorded series → forecast-driven attention + projected do-nothing cost), a
   recorded-data control whose series does NOT cross the threshold (no forecast-driven attention, do-nothing
   cost still priced but labelled on-target), and a no-data org (Sprint-20 `deli`, unchanged fallback). Asserts:
   full §7L Q1–Q10 on each; the deteriorating org's Q3 carries the forecast item + Q8/trade-off prices do-nothing
   from the projection; the flat/above-target control does NOT add a forecast attention item; the no-data org is
   byte-identical to Sprint-20's Q3/Q8 (fallback); determinism on re-run; agreement between the projection used
   in Q3/Q8 and `forecast_metric` on the same org; and no §6 overrule (Q8 recommendation unchanged by the
   forecast; the forecast only prices attention + do-nothing cost). Emit fixtures + a report.
4. **Honest docs** (`docs/ENGINE-FORECAST-ACTION.md` + an additive note in `docs/ENGINE-FORECAST-CAPACITY.md`):
   the forecast→attention→expected-impact rule (which threshold triggers a forecast-driven attention item;
   how the do-nothing baseline is priced); the honest no-data fallback; and a **§16-style verdict: does the
   recorded-data forecast now close the loop from "what if we do nothing?" (Q6) to "what should we do?" (Q8)
   through prioritized attention (Q3), all AS DATA where the data exists — and what is still not derivable?**
5. **Real output:** new runner ALL PASS; full non-regression green; no new noun, 49 `$defs`, SPEC v0.22.

## Mandatory rules
- **Write-first:** `sprints/sprint-21/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is
  `instances/contested_reality/adjudication_engine.py` (extend `cockpit_s7l`'s `.q3`/`.q8` +
  `render_cockpit_s7l` — do NOT rewrite `reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/
  `rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`, frozen by Sprints 13–18). Keep 49 `$defs`
  + URI cap + SPEC v0.22. Re-verify `ros/`, the schema hash (`7fc38c8c…`), and the sector instances
  untouched. deli/cove byte-identical up to the clock.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-20 state): `run_forecast_capacity_demo.py` + the 6 curated runners +
  `run_cockpit_s7l_demo.py`, `conformance_adjudication.py` (16 labels), the 4 prior CR demos + conformances,
  `build_all.py` + `conformance_all.py`, S5 reference + conformance, `agent_demo` + conformance.
- New assertions ALL PASS (above). Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema clean.
- Every projection/expected-impact derived from recorded series values only (no wall-clock / no invented number).

## Documentation (roll-forward)
- Add `docs/ENGINE-FORECAST-ACTION.md`; append a Sprint-21 entry to `instances/README.md`; append an
  "Update after Sprint 21" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`; append
  an additive note to `docs/ENGINE-FORECAST-CAPACITY.md` (Q6's projection now drives Q3 attention + the Q8
  do-nothing expected-impact where the data exists); reference the new build in `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-21/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize what the forecast→attention→expected-impact closure reports per org (the
threshold rule that flags a forecast-driven Q3 attention item; how the do-nothing baseline is priced on Q8/the
trade-off; the honest no-data fallback; which of Q6→Q3→Q8 is now connected AS DATA), how it is generic +
additive (recorded `metric://` series + `forecast_metric`, no new noun, frozen 49 `$defs`), the ≥3-org proof
(deteriorating recorded series → forecast attention + projected do-nothing cost; on-target control → no
forecast attention; no-data org → unchanged fallback; all full §7L), the honest §16 verdict on whether the §7L
morning cockpit now closes the Q6-forecast → Q3-attention → Q8-recommendation loop as data where the data
exists, and the verified build + conformance commands. Write the **next** sprint's self-contained prompt at
`sprints/sprint-22/PROMPT.md`.