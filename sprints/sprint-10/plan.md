# SPRINT 10 — PLAN — Conflicting-Interest experiment (human-vs-human, shared constraint)

**Driver:** the Sprint-9 review identified the *next* extension that decides whether the word
*relational* is earned: resolving a **conflicting interest** (two parties with legitimate interests
that conflict under a shared organizational constraint) — as opposed to the disputed-*fact* case
Sprint 9 already demonstrated. Acceptance brief: `STRESS-TEST-SCENARIOS.md` **Scenario B** (the
remote-work conflict).

## Objective
Extend the contested-reality engine (`instances/contested_reality/`) so it can represent and resolve
a **conflicting interest**: employee wants remote work; manager needs on-site coverage to meet a
30-minute customer-response SLA; employee has unused leave; manager has staffing constraints; company
policy permits remote work under conditions. Demonstrate detection of the interest collision, an OPEN
case, uncertainty, a **defensible determination** (incl. a conditional middle option), the **inviolable
UNRESOLVED** outcome, an **appeal** path, and the preserved signed authority chain.

## What Sprint 10 IS / IS NOT
- **IS:** a runnable, self-contained experiment on the Sprint-9 engine that models two parties'
  legitimate conflicting interests under a shared SLA/staffing/policy constraint, resolves them (or
  leaves UNRESOLVED), and demonstrates a signed appeal.
- **IS NOT:** a new service, new schema, new URI noun, or re-implementation of S1–S5/BOL. The frozen
  ontology and URI cap (49 `$defs`, SPEC v0.22) are untouched. Interests/conflict/negotiation/appeal
  are **additive fields** on existing primitives (`case://`, `relationship://`, `decision://`,
  `expectation://`, `policy://`, `right://`, `claim://`).

## Design (additive fields on existing primitives)
Model the remote-work conflict entirely additively. **No new noun.** If a genuinely-warranted new noun
is found, document it in `notes/findings.md` — do not silently add, and it must stay additive or beyond
the operating cap. We ride the existing `case://`, `relationship://` (employment + authority + contract),
`expectation://` (SLA), `policy://` (remote-work policy), `right://` (type APPEAL — the schema already has
an `APPEAL` Right literal, so appeal rides it natively), `claim://` (interests as claims), `decision://`
(adjudication), `authority://` (adjudicator). The conflict and each party's interest are additive
`conflict` / `interest` objects on the case + relationships.

Steps:
1. Provision actors (Employee, Manager, Customer, Company), relationships (employment w/ unused leave;
   contract w/ SLA; manager authority), rights (employee RIGHT APPEAL), adjudicator authority.
2. Policy: remote-work policy `policy://ic/remote` (condition → decision → action) + SLA expectation
   `expectation://ic/sla` (30-min) + staffing constraint (capacity floor).
3. Two interests modeled with explicit stakes:
   - Employee interest (remote work / use of unused leave) → additive `interest` on the employment
     relationship.
   - Manager interest (on-site coverage to meet SLA) → additive `interest` on the authority/contract rel.
4. Conflict detection: interests are mutually exclusive under the shared constraint AND each is
   legitimate/within-policy → flag the collision deterministically.
5. Open `case://ic/remote-conflict` (reuse BOL case lifecycle) with `conflict` additive field + recorded
   uncertainty.
6. Adjudication by the authorized human adjudicator among {side-employee, side-manager,
   remote-with-coverage-plan, UNRESOLVED}. Demonstrate a **defensible middle** (remote-with-coverage-plan)
   OR **UNRESOLVED** (inviolable) when the admissible basis is insufficient. Both outcomes exercised.
7. Appeal: the losing-interest party (employee) appeals via `right://…` type=APPEAL; the appeal is
   recorded as a signed, first-class, queryable step and re-adjudicated by a higher authority (or left
   pending). Not a silent redo.
8. Assertions: conflict flagged, case OPEN, determination defensible, UNRESOLVED reachable, appeal
   signed+queryable, authority chain preserved.

## Verify (real output, exit 0)
- G1 `cd instances/contested_reality && python3 run_interest_conflict_demo.py` → RESULT ALL PASS
- G2 `<venv>/python conformance_interest.py` → INTEREST-CONFLICT CONFORMANCE ALL PASS (C1–C5)
- G3 non-regression: reference demo+conformance, sector build_all+conformance, Sprint-9 dispute demo.
- G4 optional (if local model available, $0): a real-LLM advisory recommendation contained by §6 floor.

## Definition of Done
- Two interests modeled with stakes + the shared SLA/staffing/policy constraint binding both.
- Conflict flagged under the constraint; case OPEN; uncertainty recorded.
- A determination that is defensible AND includes the inviolable **UNRESOLVED** option (reachable).
- An **appeal** step that is signed and queryable (re-adjudicated by higher authority).
- Adjudicator's determination carries the authority it requires (§7J.9).
- G1–G3 all exit 0; docs, summary, findings written; SPEC stays v0.22.

## Sub-sprints
1. Context/baseline confirm (done in read phase). `work/1-plan.md`.
2. Build + run `run_interest_conflict_demo.py`.
3. Build + run `conformance_interest.py`.
4. Non-regression suite.
5. Docs + summary + findings + next PROMPT.

## Exit criteria
As above, real output only, honest failure logging, no fabricated prose/evidence.