# Sprint 10 — SUMMARY — Conflicting-Interest experiment (remote-work, Scenario B)

**What was built:** the *next* extension of the contested-reality engine — proving RelationalOS can
represent and resolve a genuine **conflict of interests** (not just a disputed *fact*, which Sprint 9
solved). Built on the Sprint-9 engine and the review's **Scenario B** (remote work): employee wants
full remote + use unused leave; manager needs on-site coverage to meet a 30-minute customer-response
SLA with a staffing floor; company policy permits remote under conditions. Two legitimate,
mutually-exclusive interests are detected under a shared constraint, opened as a case, resolved
defensibly OR honestly left **UNRESOLVED**, and appealed through a signed, higher-authority path.

## What was added (all ADDITIVE on existing primitives — no new noun, no schema edit)
- `instances/contested_reality/run_interest_conflict_demo.py` — the self-contained runner (8 assertions).
- `instances/contested_reality/conformance_interest.py` — C1–C5 gate over the new fixtures.
- Two `interest` objects (explicit stakes) on the parties' `relationship://` objects; a shared
  `constraint` object (30-min SLA + 3-agent staffing floor + conditional `policy://`) binding both.
- Deterministic **conflict detection** under the constraint; an OPEN `case://` with an additive
  `conflict` object + recorded `uncertainty`.
- A **defensible determination** = the conditional middle (`remote-with-coverage-plan`) — the option
  set keeps **UNRESOLVED** explicitly present, and the **inviolable rule holds** (a separate
  insufficient-data case concludes UNRESOLVED, Trust untouched).
- A **first-class, signed appeal** (native `right://` type=APPEAL) re-adjudicated by a higher
  authority (Director) — not a silent redo; the signed authority chain is preserved throughout (§7J.9).

## Verified commands — REAL output (all exit 0)
```
cd /home/rlg/relational-os/instances/contested_reality
python3 run_interest_conflict_demo.py            -> RESULT: ALL PASS   (8 assertions)
<venv>/python conformance_interest.py            -> INTEREST-CONFLICT CONFORMANCE: ALL PASS  (C1-C5, 17 instances)
# non-regression (nothing frozen changed)
cd /home/rlg/relational-os/sprints/sprint-5/artifacts
python3 run_s5_demo.py                           -> RESULT: ALL PASS
<venv>/python run_s5_conformance.py              -> RESULT: ALL PASS
cd /home/rlg/relational-os/instances
python3 build_all.py                             -> RESULT: ALL SECTORS PASS
<venv>/python conformance_all.py                 -> SECTOR CONFORMANCE: ALL SECTORS PASS
cd /home/rlg/relational-os/instances/contested_reality
python3 run_dispute_demo.py                      -> RESULT: ALL PASS   (Sprint 9 intact)
```

## Rendered determination + appeal excerpt (REAL)
```
[PASS] conflict detected: employee full-remote vs manager on-site coverage are mutually
       exclusive under the 30-min SLA + staffing floor  — on-site_if_full_remote=2 floor=3
[PASS] case OPEN with the conflicting-interests + uncertainty recorded
[PASS] determination is defensible AND includes the inviolable UNRESOLVED option
       — status=RESOLVED determination=remote-with-coverage-plan options=[... 'UNRESOLVED']
[PASS] appeal re-adjudicated by a HIGHER authority, signed, not a silent redo
       — appeal_outcome=modify adjudicated_by=person://ic/director
[PASS] INVIOLABLE: UNRESOLVED is reachable when the admissible basis is insufficient
       — determination=UNRESOLVED epistemic=INSUFFICIENT_EVIDENCE
RESULT: ALL PASS
```
- **Determination:** `remote-with-coverage-plan` (employee remote Mon/Wed/Fri + 2 leave days; on-site
  Tue/Thu keeps the 3-agent floor so the 30-min SLA holds). Signed by Manager `authority://ic/adjudicate-remote`.
- **Appeal:** employee appeals RULING via `right://ic/emp-appeal` (type=APPEAL) → Director re-adjudicates
  (`authority://ic/for-appeal`) → `decision://ic/appeal-decision`, outcome `modify` (remote 4 days/wk +
  3 leave days, on-site 1 day still meets floor). Signed, queryable, not a silent redo.

## Design decisions
- **No new noun** (`interest://` / `negotiation://`) — explicitly decided and documented in
  `notes/findings.md`. Interests, conflict, negotiation, and appeal are **additive fields** on existing
  primitives. The schema already provides the native `right://` **APPEAL** literal and `decision://`,
  so the appeal rides it natively. 49 `$defs` intact, SPEC stays **v0.22**.
- State transitions **MERGE** (spread the existing object first) — the Sprint-9 lesson; additive
  fields survive C4 round-trip.
- Additive field keys avoid the C2 temporal suffixes (`at|time|deadline|expires|expiry|effective|due|since`)
  — e.g. `response_target_minutes`, `coverage_floor_agents`, `unused_leave_days`.

## Honest boundaries
- The adjudicator is a **human**; the defensibility of the conditional plan is authored, not computed.
- The **optimizer / business-model** ("what does *better* mean", §7K.1) is still absent — that, plus an
  advisory real-local-model recommendation (contained by the §6 floor), is the honest next frontier.

## Key files
- `instances/contested_reality/run_interest_conflict_demo.py`, `conformance_interest.py`,
  `artifacts/interest/`.
- `instances/contested_reality/docs/CONFLICTING-INTEREST-EXPERIMENT.md` (new companion).
- `sprints/sprint-10/plan.md`, `work/1-plan.md`, `notes/findings.md`.

## Spec status
SPEC stays **v0.22**. Additive demonstration; no schema edit, no new noun, no version bump.