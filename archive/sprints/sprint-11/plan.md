# SPRINT 11 — Plan: the optimizer / business-model (Trade-off engine)

Closed by this sprint: the last honest gap named in STRESS-TEST-SCENARIOS.md Scenario B (#3,
the open "Update after Sprint 10" note) and in §7K.1 — **"what does *better* mean here?"** The
machine computes a defensible ranking of the adjudication options from the org's OWN recorded
constraints (SLA target, staffing floor, leave balance, policy satisfaction, costs, evidence
confidence), so the conflicting-interest determination is **informed** by a calculated trade-off
rather than authored from thin air. The determination stays human; the machine recommends; §6 floor
still binds on irreversible/unknown-cost. Additive only, no new noun, 49 `$defs` intact, SPEC v0.22.

## The design (KISS, deterministic, ~$0, pure local python)
A small **utility model** (`tradeoff_model.py`): for each option
{side-employee, side-manager, remote-with-coverage-plan, do-nothing/UNRESOLVED}, compute a
utility in [0,1] as a documented weighted sum of five factors — SLA compliance (customer binding,
heaviest), employee-interest satisfaction, manager/staffing satisfaction, accrued-leave
utilisation, and coordination cost — minus a §6 gate penalty when an option is irreversible or
unknown-cost. The weights ARE the business model ("what better means", §7K.1); the ranking is then
**computed** deterministically from the recorded constraint/interest data (on-site counts, floor,
leave balance, policy, cost flags). `do-nothing/UNRESOLVED` is always an explicit baseline in the
ranking. **§6 floor:** an option that is irreversible/unknown-cost is `floor_gated` — the machine
may not auto-select or execute it; it returns to the human.

`run_tradeoff_demo.py` builds a focused conflicting-interest scene (same numbers as Sprint 10:
12 leave days, 3 agents, floor 3, 30-min SLA), computes + renders the ranking, shows the human
adjudicator selecting WITH the ranking in view (determination matches top utility, or is an
explicit justifiable override), demonstrates the §6 floor on an irreversible/unknown-cost scenario
(→ UNRESOLVED, Trust untouched), and — optional — takes a real local model's **advisory** pick via
the Sprint-8 `agent_adapter` (recorded as an effect-free `decision://`; cannot set determination or
Trust; fallback-with-log, never fabricate). Emits fixtures under `artifacts/tradeoff/` and gates
them C1–C5 with `conformance_tradeoff.py`.

The trade-off object is emitted as an **additive field** on the `case://` matching the frozen
`Recommendation` `$def` shape (`by/for/options/includes_do_nothing/tradeoff/authority_required/
confidence/expected_impact/decision`). **No `recommendation://` scheme** (not in the frozen URI
catalog); no new noun.

## Sub-sprints (sequential, per PROTOCOL — single-threaded)
1. **Plan + baseline** — plan.md + work/1-plan.md; verify reference green (S5 demo, build_all,
   conformance_all, Sprint-9/10 demos + conformance).
2. **Build `tradeoff_model.py`** — pure deterministic utility engine + floor gating (+ unit
   self-check).
3. **Build `run_tradeoff_demo.py`** — scene, ranking, human selection, floor, optional model,
   fixture emit, assertions ALL PASS.
4. **Conformance** — `conformance_tradeoff.py` C1–C5 over the tradeoff fixtures.
5. **Non-regression + docs** — re-run all baselines; write docs/TRADE-OFF-IMPLEMENTATION.md,
   update instances/README.md, STRESS-TEST note; summary.md + notes/findings.md; Sprint-12 PROMPT.

## Definition of Done (real output, exit 0 everywhere)
- Sprint-10 `run_interest_conflict_demo.py` + `conformance_interest.py` green BEFORE building.
- `tradeoff_model.py` deterministic; ranking includes do-nothing/UNRESOLVED baseline.
- `run_tradeoff_demo.py` ALL PASS: determined option's utility computed+consistent; §6 floor
  triggers on irreversible/unknown-cost (model/rank suppresses, human decides); advisory model
  cannot set determination or Trust; authority/signature preserved.
- `conformance_tradeoff.py` ALL PASS (C1–C5, 49 `$defs`, URI cap intact, SPEC still v0.22).
- Non-regression: Sprint-9 + Sprint-10 demos + conformance; `build_all.py` + `conformance_all.py`;
  S5 reference demo. All ALL PASS.
- Honest note on whether the ranking is computed vs still human-authored.

## Exit criteria
`run_tradeoff_demo.py` exits 0 = ALL PASS; `conformance_tradeoff.py` exits 0 = ALL PASS; no
schema/spec/`ros/`/sector instance touched (re-verified untouched); docs + next PROMPT written.