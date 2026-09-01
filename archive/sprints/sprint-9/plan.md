# SPRINT 9 — PLAN — Contested-Reality / Dispute-Resolution experiment

**Driver:** ChatGPT's response to the Sprint-8 review. Headline finding: RelationalOS handles
`accountable execution` well but `contested human reality` poorly — it can record disagreement but
cannot reason about it. The recommended next step (renumbered #1): **build the smallest runnable
"Contested Reality / Dispute Resolution" experiment** using the existing customer-dispute scenario,
with one inviolable rule: **the system MUST be allowed to conclude UNRESOLVED when evidence does not
justify a determination.**

## Objective
Demonstrate that RelationalOS can take a messy, contested, multi-party situation and produce a
defensible, evidence-backed resolution — OR honestly leave it UNRESOLVED — while preserving the signed
authority chain. This tests whether the *relational* claim is real (the word in the name), not just
whether the execution chain works.

## Hard invariants (from the reviews + project)
- **No new noun.** The URI catalog already has `dispute://` (Appendix C; schema `$defs/Dispute`,
  §3.13). The frozen `status` enum is [OPEN, ADJUDICATED, RESOLVED]. The **UNRESOLVED / insufficient-
  evidence** epistemic state is an **additive envelope field** (`epistemic_state`, `resolution` string)
  on the existing dispute object — NOT a new state literal that would force a schema edit. Keep the 49
  `$defs` byte-identical. SPEC stays v0.22.
- **Additive only.** Ride existing primitives: `dispute://`, `claim://`, `evidence://`, `decision://`,
  `relationship://`. Zero changes to `ros/`, schema, reference build.
- **Fact / Claim / Determination separation** (the review's three-layer epistemology): an EVENT is a
  record; a CLAIM is someone's interpretation; a DETERMINATION is the organization's decision to treat
  X as operative. The experiment makes each a distinct, first-class object.
- **Single-threaded**, plan-before-build, real tool output only, no fabrication.

## Design
A self-contained `instances/contested_reality/` experiment using the substrate directly:
1. **Provision** actors (Customer, Supplier, Company/Manager) + the delivery relationship + authority
   (adjudicator = Manager, grant `adjudicate_dispute`).
2. **Facts (events)** — the recorded timeline (a committed delivery, a GPS timestamp, a contract deadline,
   a payment) as signed OUTCOME/EXCHANGE-ledger facts.
3. **Two conflicting claims** — Customer: "late / not delivered"; Supplier: "delivered on time." Each tied
   to its evidence:// with a degree under a procedure.
4. **Conflict detection** — claims are mutually exclusive *and* their evidence does not dominate → a
   `dispute://` is opened (OPEN).
5. **Disputed state + uncertainty** — record the evidence-confidence spread + epistemic_state=UNDETERMINED.
6. **Adjudication** — the authorized adjudicator (Manager) receives an AI-or-deterministic recommendation
   (option set: side-with-customer, side-with-supplier, seek-more-evidence, UNRESOLVED) + must decide.
7. **Resolution** — three legal outcomes: determination (a claim accepted → fact-plus-determination),
   remand (seek more evidence), or **UNRESOLVED** (insufficient evidence) — the inviolable case.
8. **Outcome / Trust / Learning** — only a *determination* with adequate evidence advances Trust via the
   S5 formula; an UNRESOLVED result is recorded as such and does NOT corrupt Trust (a key safety property).
9. **Assertions (real):** the UNRESOLVED path is reachable; the dispute lifecycle is legal; authoring the
   determination required the adjudicator's signature; an unresolved dispute does not update Trust.

Reuse `agent_adapter` where a real model recommendation is valuable (optional, $0, additive) — but the
determination itself is the human adjudicator's, not the model's.

## Verify (real output)
G1 `cd instances/contested_reality && python3 run_dispute_demo.py` → RESULT ALL PASS (both a resolved
   and an UNRESOLVED branch demonstrated)
G2 `<venv>/python conformance_dispute.py` → C1–C5 ALL PASS (fixtures valid; additive fields OK)
G3 non-regression: reference demo + conformance; sector build_all + conformance → ALL PASS
G4 `python3 build_all_disputes.py` → dispute engine runs across all 12 sector configs ALL PASS

## Definition of Done
- Dispute lifecycle OPEN→ADJUDICATED→(RESOLVED | UNRESOLVED) demonstrated, resolution + epistemic state
  recorded.
- THE inviolable rule holds: **UNRESOLVED is reachable and is not treated as a forced winner.**
- Trust update only on a determination with adequate evidence; an unresolved dispute leaves Trust untouched.
- Fact/Claim/Determination are distinct objects (record vs interpretation vs operative).
- G1–G4 all exit 0; docs + findings + summary written; SPEC stays v0.22.

## Exit criteria
As above, real output, no fabricated model text, honest failure logging.