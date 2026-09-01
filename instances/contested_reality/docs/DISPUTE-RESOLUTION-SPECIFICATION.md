# Contested Reality / Dispute Resolution — RelationalOS Specification

**Scope.** The completeness review's decisive test: *does RelationalOS understand disagreement?* This
specification answers it as **a working system, not an argument**. It consolidates the contested-
reality engine that Sprints 9–11 built piecemeal into one coherent, runnable new concept and applies
it to the four demanded scenarios. The executable proof (`run_full_dispute.py`) is part of the
deliverable — every claim below maps to real, exit-0 output.

**Design constraint honored throughout:** no redesign, no large new ontology, no collapse of distinct
concepts. The seven distinctions the review insists on — Event, Evidence, Claim, Inference,
Determination, Decision, Outcome — are all separately represented and maps to distinct `$defs` /
URI schemes: Event (`event://`), Evidence (`evidence://`), Claim (`claim://` + additive
`epistemic_status`), Inference (additive on claims), Determination (additive on the `dispute://` +
`decision://`), Decision (`decision://`), Outcome (`event://` + additive `resolution_outcome` /
verified). None are conflated. The frozen 49 `$defs` and URI cap are unchanged; SPEC stays v0.22.

---

## 1. Minimum Semantics: what represents what

| Requirement | Existing concept | How | New concept needed? |
|---|---|---|---|
| conflicting claims | `claim://` (§3.17) | `proposer`/`statement`; two parties → same-situation claims; kept separate | No |
| conflicting evidence | `evidence://` kind/source/`verity.confidence`, additive `reliability`/`supports` | multiple evidence refs on a claim; sources disagree → conflict detected additively | No |
| disputed obligations / expectations | `obligation://`, `expectation://` (native) | dispute `about` an obligation; condition→threshold expectation | No |
| conflicting interests | additive `interest` blocks (Sprint 10) | per-party stakes on the relationship/dispute | No (additive) |
| uncertainty | additive `epistemic_state` / `conflict.uncertainty` | not-CLEAR is representable; no forced CLEAR | No (additive) |
| unresolved situations | additive `determination=UNRESOLVED`, `epistemic_state=INSUFFICIENT_EVIDENCE` | a legal outcome; case stays OPEN | No (additive; enum frozen) |
| adjudication | additive on `dispute://` + `decision://` | authorized adjudicator decides among options | No (additive) |
| resolution | additive `resolution_type`/`resolution` | accept/partial/settle/conditional/etc | No (additive) |
| appeal | `right://` type=APPEAL + `decision://` | first-class Right; re-adjudicated by higher authority | No (exists) |
| settlement | additive `resolution_type=partial-settlement` | a negotiated/modified determination | No (additive) |
| determination | additive `determination` on `dispute://` + `decision://` | the human's operative call, distinguished from decision/outcome | No (additive) |

**Finding.** Every required semantic is either already a native `$def` or is an *additive
envelope field* on an existing object. No new ontology primitive is genuinely required. This matches
the project's standing rule: Exception/Priority/Recommendation/capacity were settled the same way.

## 2. Epistemic status
The ten statuses (observed/reported/claimed/inferred/disputed/supported/contradicted/verified/
unresolved/determined) are carried as an **additive `epistemic_status` field on the claiming object**
(`claim://`), not new claim types or evidence classifications. This is deliberate: whether a claim is
*determined* is a property of the organization's adjudication of it, not a property of the proposition
or of any single evidence item. `evidence://` keeps its own `verity.procedure/confidence` + additive
`reliability` (the evidence class, §3.17). The proof walks a claim from `claimed` → `disputed`
(contradictory evidence attaches) → either `supported`/`contradicted` under the determination or left
`unresolved` (`INSUFFICIENT_EVIDENCE`). A status is a *property*, not a new object.

## 3. Conflicting evidence → can we reach a determination?
The four timestamp items (GPS 16:12 / contract deadline 16:00 / customer receipt 16:15 / supplier
15:58) are each `evidence://` with provenance (source), reliability, and `captured_at`. They *both*
support and contradict: GPS + receipt say late; supplier log says on-time. The single-source S5
verifier therefore cannot reach CLEAR — that is **correct**; the system represents the contradiction
rather than forcing a winner. The proof then shows two legal paths:
- **Determination reached** when an *independent anchored* source (degree 0.97) resolves the
  ambiguity → authorized human adjudicator determines `conditional-resolution` (delivered within
  grace).
- **UNRESOLVED** when no decisive source exists → adjudicator records `UNRESOLVED` /
  `INSUFFICIENT_EVIDENCE`, the dispute stays OPEN, and this propagates: no determination → no refund
  → the customer may escalate or seek external adjudication. UNRESOLVED never advances Trust.

## 4. Human-vs-human conflict (remote work)
Expressly modeled in Sprint 10 (`run_interest_conflict_demo.py`, same numbers reused in Sprint 11).
Each actor's claim is an additive `interest`; the shared SLA + staffing + conditional-policy is an
additive `constraint`; obligations and manager authority are native. The proof answers all questions:
claims (both legitimate), evidence (leave balance, staffing counts, policy), conflicting interests,
obligations, constraints, authority (manager adjudicator / director appeal), options (incl.
do-nothing), recommendation (machine trade-off + advisory), what needs human judgment (the coverage
judgment; §6 floor on the unresolvable branch), disagreement (appeal), negotiated resolution
(conditional plan), and whether it can stay unresolved (yes — UNRESOLVED, Trust-safe).

## 5. Customer/business dispute ($18,000)
The consolidated proof runs this end-to-end: customer "charged for non-delivery" vs company
"delivered" vs supplier "shipped on time" → four conflicting evidence items + invoice → conflict +
uncertainty → interests/obligations/constraints → options incl. settlement → constrained trade-off →
contained AI advisory → authorized human determination → verified outcome → learning → appeal →
reopen on new evidence (clock mis-set) → reassessment by higher authority → **new** determination
(partial settlement), history preserved.

## 6. Adjudication model — Recommendation ≠ Determination ≠ Decision ≠ Authorization ≠ Execution
These five are kept distinct and never conflated:
- **Recommendation** = `decision://…agent-advisory` (machine trade-off *and/or* real model). It only
  informs; by construction it is not the determination.
- **Determination** = additive `determination` on `dispute://` — *who/what operative reality is*.
- **Decision** = the authorized human's `decision://` record (adjudicator, authority, alternatives,
  evidence, confidence, expected/actual outcome).
- **Authorization** = the `authority://` the decision conserves (§7J.9) — the proof asserts each
  decision carries the authority it requires.
- **Execution** = a separate `event://`; irreversible/unknown-cost actions are gated by the §6 human
  floor (Sprint 11): the machine never auto-executes a floor-gated option.

## 7. AI's role (the exact control boundary)
The real local model may retrieve evidence, summarize claims, identify contradictions/missing
evidence, hypothesize, list possible resolutions, estimate consequence, and recommend — surfaced as an
**effect-free `decision://`** (type DECISION, never an ACTION). It cannot determine disputed facts,
grant authority, approve its own recommendation, execute an irreversible action, erase contradictory
evidence, or convert uncertainty into certainty. The proof's assertions hold even when the model's
pick *disagrees* with the machine's: the determination stays the human's and no `trust://` object is
ever written by the advisory. This is the Sprint-8 `agent_demo` containment, re-asserted on a full
lifecycle.

## 8. Resolution types
The dispute carries an additive `available_resolutions` list that includes all review types:
accept-customer / accept-company / partial-settlement / conditional / request-more-evidence / defer /
escalate / unresolved / external-adjudication. Nothing anywhere assumes a winner — the utility space
and the UNRESOLVED branch both treat "no winner" as legitimate and Trust-safe.

## 9. Appeals and reopening
A determination later shown to be **wrong** is reopened, not rewritten: `decision://` #1 (manager,
conditional-resolution) is preserved verbatim while new evidence (`evidence://lf/clock-mis-set`,
"9-min fast", honest source error) drives REOPEN → REASSESSMENT → `decision://` #2 (director,
partial settlement). The immutable ledger retains the whole layering; an auditor sees the original
determination, the new evidence, and the supersession. Trust/claims/decisions are not destroyed —
the earlier determination's Trust effect is kept (and, because it was honest error, does not depress
scoped Trust — §10).

## 10. Trust implications (error vs. deception)
RelationalOS does **not** equate "incorrect" with "untrustworthy." Trust moves only via the S5
deterministic formula over **adequately-evidenced determinations**. The proof demonstrates: the
customer's overturned (honest) claim does not depress their scoped Trust (the receipt was authentic;
the error was a mis-set anchor clock). A deliberately misrepresented claim would, *where* an
adequately-evidenced determination proved it false, feed the deterministic formula — never an author
writing a trust score, and never the AI. This keeps error (a reliability/signaling matter, additive
`reliability_note`) distinct from deception (a verified-determination trust matter).

## 11. Formal state machine
The dispute carries an additive `lifecycle_state` walking the exact review machine
(`OPEN → EVIDENCE_COLLECTION → CONTESTED → ADJUDICATION → RESOLUTION → ACCEPTED → EXECUTED →
VERIFIED → CLOSED`), plus the branches `ESCALATED` (an `available_resolutions` option), `UNRESOLVED`
(stays OPEN, Trust-safe), `APPEALED` and `REOPENED` (both exercised in the proof), and `SETTLED`
(the second determination is a partial settlement). A legal representative walk is emitted for
conformance C5. All are **additive fields on the dispute**, not new transition tables in the schema.

## 12. Ledger representation
Every step is a real signed, append-only event (`event://lf/…`) with `event_id/type/actor/authority/
causation/correlation/idempotency_key/timestamp/state_update/signature`. The proof's final check
reconstructs the full chain (provision → claims → evidence → open → advisory → adjudicate → verify →
appeal → reopen → reassess → unresolved) and asserts **11/11 steps** are recoverable from the ledger,
so an independent auditor can rebuild who said what, what evidence existed, what the system knew
(and did not), what it recommended, who decided, who authorized, what happened, whether the outcome
was verified, and what was learned.

## 13. Is the existing ontology sufficient?

| Requirement | Existing RelationalOS concept | Additional semantics required | New concept required? |
|---|---|---|---|
| Event | `event://` (signed, append-only) | — | No |
| Evidence + provenance + reliability | `evidence://` kind/source/verity | additive `reliability`, `supports` | No |
| Claim / proposer / statement | `claim://` | — | No |
| Epistemic status of a claim | — | additive `epistemic_status` on claim | No (additive field) |
| Conflict / uncertainty | — | additive `conflict` object + `epistemic_state` on dispute | No (additive field) |
| Dispute (parties/about/status) | `dispute://` (§3.13) | additive lifecycle/epistemic/determination | No (additive field) |
| Determination | — | additive on dispute + `decision://` | No (additive field) |
| Obligation / expectation | `obligation://`, `expectation://` | — | No |
| Interest / constraint | — | additive `interest`/`constraint` blocks (S9–11) | No (additive field) |
| Resolution types incl. settlement | — | additive `resolution_type`, `available_resolutions` | No (additive field) |
| Appeal | `right://` type=APPEAL | — | No |
| Reopen / supersede | — | additive `reopened`/`supersedes` on dispute/decision | No (additive field) |
| Trust (scoped, error vs deception) | `trust://` + S5 deterministic formula | — | No |
| AI recommendation (contained) | `decision://` (advisory) | `Recommendation` `$def` shape | No (`Recommendation` $def exists) |
| Trade-off / optimizer | — | additive `Recommendation`-shape `tradeoff` (Sprint 11) | No (additive field) |

**Verdict: the existing ontology is sufficient.** Everything the review demands is either a native
$def or an additive envelope field. The 49 `$defs` and URI cap are byte-identical across Sprints 9–12;
C1–C5 passes on every fixture generation including this one.

## 14. Minimal prototype
`run_full_dispute.py` (this sprint) is the minimal executable proof. Tests demonstrating (all exit 0 =
ALL PASS): contradictory claims preserved; contradictory evidence preserved; `UNRESOLVED` a valid
outcome and Trust-safe; AI cannot bypass authority or set determine / Trust; original evidence and
the original determination cannot be rewritten (reopen is additive); a later determination reopens
and reassesses; the complete history remains auditable; authority/signature preserved. Non-regression:
Sprint-9/10/11 demos + conformance, `build_all.py` + `conformance_all.py`, S5 reference — all ALL PASS.

## 15. Do not hide failure — What works / What needs work / What is fundamentally unresolved
- **Works now (proven, exit 0):** multi-actor conflicting claims + evidence; conflict detection;
  uncertainty; epistemic status; interests/obligations/constraints; resolution options incl.
  do-nothing + settlement; a constrained trade-off; a contained real-AI advisory; authorized human
  determination; UNRESOLVED; verified outcome + learning; appeal → reopen → reassess without rewrite;
  error-vs-deception Trust; an auditor-reconstructable ledger; §6 floor + §7J.9 authority.
- **Requires new semantics (all additive, done here):** epistemic status, lifecycle state machine,
  evidence reliability/reconciliation-of-thumb, resolution-type names, reopen/supersede flags.
- **Requires new implementation (not yet built):** a general policy/Rules engine to *auto-generate*
  the resolution options and utility weights from a configurable business model (currently the weights
  and option set are authored per scenario, per §7K.1's acknowledgement that the optimizer needs to
  know what "better" means). A full auditor-facing query surface over the reconstructed chain.
- **FUNDAMENTALLY UNRESOLVED (architectural, not hidden):** the ontology represents and *contains*
  disagreement but **does not manufacture certainty**. When evidence genuinely cannot decide, the
  correct answer is UNRESOLVED and stays that way until a decisive admissible source or a human
  adjudicator (with authority) resolves it — the machine will never pretend. That is a boundary of the
  design, stated rather than papered over. Related: the weights/objective of the business model are a
  human organizational choice; the machine computes the ranking, not the value system.

## 16. Final Assessment — # Does RelationalOS Understand Disagreement?

**Assessment: B — Partially, but the partial is real and operationally meaningful.**

It is not **A (Yes)**: RelationalOS cannot *manufacture* a determination from insufficient evidence
(after ruling out `UNRESOLVED`), and its adjudication semantics are expressed as documented additive
fields over a generic envelope rather than a configurable dispute-DSL. It is not **C (No)** either: it
does **not** assume a single authoritative reality — contradictory claims and evidence are first-class
and preserved, UNRESOLVED is a lawful, Trust-safe outcome, the machine cannot force reality, and a
wrong determination can be reopened and reassessed without rewriting history.

The decisive, demonstrated strength is that RelationalOS treats disagreement as **state to be carried
and contained, never collapsed** — it holds "here are three versions of what happened, each with its
own evidence, and nobody agrees what should happen next" without flattening them, while keeping the
AI advisory, keeping the human as the only determiner, keeping an immutable auditor-reconstructable
ledger, and keeping *error distinct from deception* in Trust.

**On the larger question — does handling contested reality materially strengthen the claim that
RelationalOS is a new category, not an integration of CRM/ERP/ITSM/workflow/BI/AI? — be skeptical:**

Partially, but not yet categorically. The parts that *would* differentiate it are present and now
demonstrable: an ontology whose first-class unit is the *relationship and its disagreement* (not a
record or a ticket), truthful UNRESOLVED instead of forced resolution, and error-vs-deception Trust.
But the differentiating claim is only fully earned if two things follow, and they are **not yet
built**: (1) the adjudication semantics must become a *general, configurable* capability rather than a
per-scenario authored model (so any org's disputes run without re-coding the engine), and (2) the
whole loop must render onto the §7L cockpit so a Fed-org executive hands the "what are our options and
what should we do" question to it daily. Until those are real, the honest position is: **RelationalOS
currently demonstrates operational accountability under contested reality — a genuine and unusual
asset — but the "new category" claim rests on generalizing that ability, which is the next work, not
a finished fact.**

*(Evidence: all assertions above are real exit-0 output from `run_full_dispute.py` and
`conformance_lifecycle.py`, plus the standing Sprint-9/10/11 + reference + sector conformance suites.)*