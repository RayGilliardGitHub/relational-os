# CONFLICTING-INTEREST EXPERIMENT — the remote-work conflict under a shared constraint

**Sprint 10.** The *next* extension of the contested-reality work — the experiment the Sprint-9
review identified as the thing that decides whether the word *relational* is earned: resolving a
**conflicting interest** (two parties with legitimate interests that conflict under a shared
organizational constraint), as opposed to the disputed-*fact* case Sprint 9 already demonstrated.
Acceptance brief: `STRESS-TEST-SCENARIOS.md` **Scenario B**.

## The problem (from the review)

Scenario A (disputed *fact*) was addressed by Sprint 9. Scenario B — a *conflicting interest* —
was the remaining gap:

> Employee wants remote work. Manager wants on-site coverage. Customer contract requires response
> within 30 minutes. Employee has unused leave. Manager has staffing constraints. Company policy
> permits remote work under certain conditions.

The review's verdict on Scenario B was **WEAK / PARTIAL**: the system could *record* the decision
and its authority but could **not represent the organizational conflict itself** — interests,
negotiation, appeal, constraint trade-off. The nouns (interest, conflict, expectation, commitment,
authority, right) existed but had no runnable semantics.

## The change in one line

A **conflict of interests** is represented as *additive fields on existing primitives* — two
`interest` objects (one per party, with explicit stakes) on their `relationship://` objects, plus a
shared `constraint` object (the 30-minute SLA, a 3-agent staffing floor, and a **conditional**
remote-work `policy://`) binding both parties — and resolved through a lifecycle on the existing
`case://` primitive with a signed, first-class **appeal**. **No new noun, no schema edit, no
version bump (SPEC stays v0.22).**

## What was built (smallest runnable form)

`instances/contested_reality/run_interest_conflict_demo.py` + `conformance_interest.py`. It reuses
the Sprint-9 engine pattern (real substrate + S5, additive fields, signed ledger) and adds:

1. **Two interests with explicit stakes** (additive `interest` objects):
   - Employee (`relationship://ic/employment`): wants full remote + use 12 unused-leave days;
     legitimate, within-policy.
   - Manager (`relationship://ic/contract`): needs on-site coverage to meet the SLA; legitimate,
     within-policy.
2. **A shared constraint** (additive `constraint` object on the contract relationship) binding both:
   response target 30 min, coverage floor 3 agents, on-site count 3, conditional remote-work policy.
   The SLA is also a real `expectation://ic/sla` (§3.11) and the policy a real `policy://ic/remote`
   (§7K.1 Condition→Decision→Action).
3. **Deterministic conflict detection** under the constraint: if the employee goes **full remote**,
   one agent leaves the on-site count (3→2) which violates the 3-agent floor → the 30-min SLA cannot
   be guaranteed → the two interests are **mutually exclusive** though each is legitimate/within-policy.
4. **Case OPEN** (`case://ic/remote-conflict`) carrying an additive `conflict` object: both interests,
   the constraint, `detected:true`, `mutually_exclusive:true`, and a recorded `uncertainty` string
   (coverage on remote days unverified). Reuses the BOL `case://` lifecycle (status OPEN).
5. **A defensible determination** — the adjudicator (Manager, `authority://ic/adjudicate-remote`)
   decides among `{side-employee, side-manager, remote-with-coverage-plan, UNRESOLVED}`, choosing the
   **conditional middle option** (`remote-with-coverage-plan`): remote Mon/Wed/Fri + 2 leave days,
   on-site Tue/Thu keeps staffing at floor so the SLA holds. The option set keeps **UNRESOLVED**
   explicitly present (the inviolable review rule).
6. **The inviolable UNRESOLVED is reachable**: a second micro-case (`case://ic/remote-uncertain`)
   where coverage data on proposed remote days is **unverifiable / no independent source** → the
   adjudicator concludes **UNRESOLVED / INSUFFICIENT_EVIDENCE**, case left OPEN — a forced winner is
   never manufactured. Trust is untouched (same safety as Sprint 9).
7. **A first-class, signed appeal**: the losing-interest employee appeals via the native
   `right://ic/emp-appeal` (**type=APPEAL** — the schema already defines an APPEAL Right literal).
   The appeal is recorded as a signed `event://ic/appeal` + an additive `appeal` object
   (`appeals_for`, `appealing`, `ground`, `status=OPEN`, `authority`), then **re-adjudicated by a
   higher authority** (`person://ic/director`, `authority://ic/for-appeal`) → a new signed
   `decision://ic/appeal-decision` (ruling: modify — remote 4 days/wk + 3 leave days, on-site 1 day
   still meets the floor). Not a silent redo: it has its own authority, signature, and audit trail.
8. **Authority preserved** (§7J.9): every determination carries the authority it requires AND the
   signer — `decision://ic/adjudication` via `authority://ic/adjudicate-remote` (by Manager),
   `decision://ic/appeal-decision` via `authority://ic/for-appeal` (by Director).

## What the run actually proved (REAL, all PASS)

```
=== CONFLICTING-INTEREST experiment (remote-work, Scenario B) ===

  [PASS] conflict detected: employee full-remote vs manager on-site coverage are mutually
         exclusive under the 30-min SLA + staffing floor  — on-site_if_full_remote=2 floor=3
         policy=permitted-conditional
  [PASS] case OPEN with the conflicting-interests + uncertainty recorded
  [PASS] determination is defensible AND includes the inviolable UNRESOLVED option
         — status=RESOLVED determination=remote-with-coverage-plan options=[...‘UNRESOLVED’]
  [PASS] appeal is a signed, queryable, first-class step (recorded additive field + native
         Right type=APPEAL)
  [PASS] appeal re-adjudicated by a HIGHER authority, signed, not a silent redo
         — appeal_outcome=modify adjudicated_by=person://ic/director
  [PASS] adjudicator's determination conserves the authority it requires (§7J.9)
  [PASS] INVIOLABLE: UNRESOLVED is reachable when the admissible basis is insufficient
         (no forced winner)  — determination=UNRESOLVED epistemic=INSUFFICIENT_EVIDENCE
  [PASS] UNRESOLVED outcome does NOT advance Trust (same safety as Sprint 9)

RESULT: ALL PASS     (exit 0)
```

## Verified commands (REAL output, all exit 0)

```
cd /home/rlg/relational-os/instances/contested_reality
python3 run_interest_conflict_demo.py            -> RESULT: ALL PASS   (8 assertions)
<venv>/python conformance_interest.py            -> INTEREST-CONFLICT CONFORMANCE: ALL PASS (C1-C5, 17 instances)

# non-regression (nothing frozen changed)
cd /home/rlg/relational-os/archive/sprints/sprint-5/artifacts
python3 run_s5_demo.py                           -> RESULT: ALL PASS
<venv>/python run_s5_conformance.py              -> RESULT: ALL PASS
cd /home/rlg/relational-os/instances
python3 build_all.py                             -> RESULT: ALL SECTORS PASS
<venv>/python conformance_all.py                 -> SECTOR CONFORMANCE: ALL SECTORS PASS
cd /home/rlg/relational-os/instances/contested_reality
python3 run_dispute_demo.py                      -> RESULT: ALL PASS   (Sprint 9 intact)
```

## Honest assessment — what this does and does not prove

**Demonstrated:**
- A genuine **conflict of interests** (not a disputed fact) is representable and runnable: two
  legitimate, mutually-exclusive interests under a shared SLA/staffing/policy constraint.
- The **shared constraint** is first-class context both parties are subject to (not a claim).
- **Deterministic conflict detection** under the constraint; the conflict is a queried, signed state.
- **Negotiation/trade-off** is expressible: the defensible determination is a **conditional middle**
  (`remote-with-coverage-plan`) that meets the employee's remote interest AND the manager's SLA.
- The **inviolable UNRESOLVED** rule holds for *interests* exactly as for *facts*: insufficient
  admissible basis → UNRESOLVED, case left OPEN, Trust untouched.
- **Appeal** is now a first-class, signed, queryable step re-adjudicated by a higher authority —
  not a silent redo — riding the schema's native `right://` type=APPEAL.
- **Authority preserved** through the whole chain, including the appeal.

**Honest limits (unchanged, explicit):**
- The adjudicator is a **human**; a local model could *recommend* but does not in this minimal form
  (same advisory-`decision://` + §6-floor pattern proven in Sprint 8 could extend it).
- **No optimizer/business-model** for "what does *better* mean" (§7K.1) — the conditional plan's
  defensibility is authored by the human adjudicator, not computed by the machine. This remains the
  genuine frontier (see `STRESS-TEST-SCENARIOS.md` §What remains).
- One conflict shape (remote-work) at reference scale, local, ~$0.

## Conclusion

The review asked whether RelationalOS can represent the *organizational conflict itself* — interests,
negotiation, appeal, constraint trade-off — under Scenario B. This experiment demonstrates the minimum
viable version: a conflicting interest is detected under a shared constraint, opened as a case with
recorded uncertainty, resolved (defensibly) OR left **UNRESOLVED**, and an appeal is a first-class
signed step re-adjudicated by a higher authority — all additive on existing primitives, all
schema-safe, SPEC staying v0.22. It earns the word *relational* for the conflicting-interest case as
far as a signed, evidence-traceable, authority-preserving ledger of human judgment can — the machine
still does not decide what "better" means, which is the honest next frontier.