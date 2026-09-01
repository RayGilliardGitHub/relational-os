# SPRINT 10 — PROMPT  (Conflicting-Interest experiment: human-vs-human reality under shared constraints)

You are Hermes Agent in a **fresh session** with **NO memory** of prior conversation. Rely ONLY on the
files named here. Read before acting; do not guess or invent. **Every command you document MUST be run and
its real output captured** — never fabricate. This sprint builds the **next extension of the contested-reality
work**: the experiment the Sprint-9 review identified as the thing that decides whether the word *relational*
is earned — resolving a **conflicting interest** (two parties with legitimate interests that conflict under a
shared organizational constraint), as opposed to the disputed-*fact* case already demonstrated.

## Context — read first, in full
- Canonical spec (the contract): `/home/rlg/relational-os/SPEC.md` (v0.22)
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md`
- Work completed, in order, so you understand what exists and the design rules:
  - `/home/rlg/relational-os/sprints/sprint-9/summary.md` and `plan.md` (contested-reality disputed-fact
    experiment — READ FIRST for the pattern, invariants, and where it stops).
  - `/home/rlg/relational-os/sprints/sprint-9/notes/findings.md` (the pitfalls: Evidence `kind` enum,
    state transitions must MERGE not replace).
  - `/home/rlg/relational-os/instances/contested_reality/run_dispute_demo.py` and
    `/home/rlg/relational-os/instances/contested_reality/docs/CONTESTED-REALITY-EXPERIMENT.md` (the working
    experiment you extend).
  - `/home/rlg/relational-os/sprints/sprint-8/summary.md` (real-LLM recommendation containment; proves the
    advisory-`decision://` + §6-floor pattern).
  - The reviews that set the direction:
    `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` (Scenario B — the remote-work
    employee↔manager conflict — is your brief), and its "Update after Sprint 9" note.
- Project invariants & operational recipes: the `relational-os` skill (frozen ontology/URI cap; additive
  fields; single-threaded; plan-before-build; real output; ~$0 local; read the footguns: subpackage
  self-anchoring, schema required-field enforcement, merge-not-replace on state updates).

## What Sprint 10 IS and is NOT
- **IS:** a runnable experiment (built on the Sprint-9 contested-reality engine) that models **two parties
  with legitimate, conflicting interests under a shared organizational constraint** and demonstrates a
  defensible, evidence-backed resolution — **while preserving authority, uncertainty, disagreement,
  human judgment, and the right to leave something UNRESOLVED.** Use the review's remote-work Scenario B
  (employee wants remote work; manager needs on-site coverage to meet a 30-minute customer-response SLA;
  employee has unused leave; manager has staffing constraints; company policy permits remote work under
  conditions) as the concrete case. The system must go beyond the disputed-*fact* case (which Sprint 9
  solved) and represent an actual **conflict of interests**, an **appeal** path, and the trade-offs.
- **IS NOT:** a new service, new schema, new URI noun, or a re-implementation of S1–S5/BOL. **Do NOT change
  the frozen ontology or URI cap (§7J.11/§C16) or the 49-`$def` schema.** Interests/conflict/negotiation
  must be represented as **additive fields / additive objects** on existing primitives (a `case://`, the
  parties' `relationship://`, `decision://`, `expectation://`, `policy://`) — exactly like
  Exception/Priority/Recommendation/capacity and the Sprint-9 `epistemic_state`. If you believe a new noun
  (e.g. `interest://` or `negotiation://`) is genuinely warranted, make it an **explicit, additive,
  documented decision in `notes/findings.md`** — do NOT add it silently.

## The target (what "done" looks like)
Extend the contested-reality framework so it can represent and resolve a **conflicting interest**:
1. **Two parties' interests are modeled** (e.g. Employee: remote work / unused leave; Manager: on-site
   coverage to meet the SLA) — each an explicit object with stakes, not just a claim about a fact.
2. **The shared constraint is represented** (the 30-minute SLA, the staffing floor, the conditional
   remote-work policy) as binding context both parties are subject to.
3. **Conflict detection** deterministically flags the interest collision under the constraint (interests are
   mutually exclusive AND each is legitimate/within policy).
4. **The conflict is opened as a `case://`** (reuse the BOL case lifecycle) with the conflict recorded as an
   additive field; uncertainty is recorded, not hidden.
5. **A defensible resolution exists** that may be: side-with-employee / side-with-manager / a conditional
   middle option (e.g. remote-with-coverage-plan) / **UNRESOLVED** (insufficient admissible basis). The
   **inviolable UNRESOLVED rule from Sprint 9 must hold** — the system MUST be able to conclude that no
   resolution is justified.
6. **An appeal path is demonstrated**: after a determination, the losing-interest party can appeal; the appeal
   is recorded, and (if warranted) re-adjudicated by a higher authority or left pending. At minimum, the
   appeal is a first-class, signed, queryable step — not a silent redo.
7. **Every step is signed and on the ledger**; the adjudicator's determination carries the authority it
   requires (§7J.9); the whole run preserves the signed authority chain.

## Grounding research to do first (real)
- Re-read `STRESS-TEST-SCENARIOS.md` Scenario B fully and treat it as the acceptance brief.
- Confirm what already exists: run `cd /home/rlg/relational-os/instances/contested_reality && python3 run_dispute_demo.py`
  and the conformance gate `…/sprints/sprint-0/artifacts/.venv/bin/python conformance_dispute.py` — both
  must be green before you start (that is your baseline).
- Confirm which primitives the schema already provides for interests/expectations/rights (read
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/schema/relational-os.schema.yaml` — note `Expectation`,
  `Right`, `Obligation`, `Commitment`, `Decision`, `Dispute`). Prefer riding these.

## Mandatory rules
- **Write-first:** `sprints/sprint-10/plan.md` FIRST, then a `<sprint>/work/` plan before drafting
  code/content (per PROTOCOL).
- **Real tool output only.** Run every command you document; embed real output. No fabricated prose,
  evidence, or results.
- **URI cap / frozen ontology / 49 `$defs` / SPEC v0.22:** no new scheme; no schema edit; interests/conflict/
  negotiation/appeal are additive. If a genuinely-warranted new noun exists, decide + document it in
  findings (never silently) — AND it must stay beyond the operating-noun cap or be justified additively.
- **Do NOT disturb the verified chain:** `ros/`, the schema, the reference build, and the 12+ sector
  instances stay as-is; re-verify them untouched.
- **Single-threaded** per PROTOCOL — no `delegate_task`/subagents; all work in ONE sequential process.
- **Budget:** ~$0; local, no frontier-API spend. A real local model (Ollama, e.g. `phi4-mini:3.8b-q8_0`) MAY
  be used as an optional adviser, but the **determination is a human adjudicator's**, not the model's.
- **Raymond:** clean English, `file://` absolute paths, honest "stuck/failed" over fabricated success, report
  status at each long step.

## Verification / Definition of Done (mandatory, real output, all exit 0)
- `cd /home/rlg/relational-os/sprints/sprint-10` — `plan.md` written FIRST; a `work/` plan too.
- The extension lives under `/home/rlg/relational-os/instances/contested_reality/` (extend `run_dispute_demo.py`
  or add `run_interest_conflict_demo.py` sharing its engine) — keep it reusable, self-contained, plain python3.
- New assertions ALL PASS demonstrating, on the remote-work brief:
  - two interests modeled with stakes + the shared SLA/staffing/policy constraint;
  - conflict flagged under the constraint;
  - case OPEN, uncertainty recorded;
  - a determination that is defensible AND includes the inviolable option **UNRESOLVED**;
  - an **appeal** step that is signed and queryable (not a silent redo);
  - the adjudicator's determination carries the authority it requires.
- `cd /home/rlg/relational-os/instances/contested_reality && python3 run_<new>.py` → `RESULT: ALL PASS`
- `…/venv/bin/python conformance_<new>.py` → C1–C5 `ALL PASS` (fork `conformance_dispute.py` to cover the new
  fixtures; the additive fields must not break C2/C4).
- Non-regression (prove you changed nothing frozen):
  - `cd /home/rlg/relational-os/sprints/sprint-5/artifacts && python3 run_s5_demo.py` → `RESULT: ALL PASS`
  - `…/venv/bin/python run_s5_conformance.py` → `RESULT: ALL PASS`
  - `cd /home/rlg/relational-os/instances && python3 build_all.py` → `RESULT: ALL SECTORS PASS`
  - `…/venv/bin/python conformance_all.py` → `SECTOR CONFORMANCE: ALL SECTORS PASS`
  - `cd /home/rlg/relational-os/instances/contested_reality && python3 run_dispute_demo.py` → still ALL PASS
    (Sprint-9 experiment intact).

## Documentation (roll-forward, non-negotiable)
- Update `/home/rlg/relational-os/instances/contested_reality/docs/CONTESTED-REALITY-EXPERIMENT.md` (or add a
  companion) so it now covers the conflicting-interest case + appeal, with real output embedded.
- Update `/home/rlg/relational-os/instances/README.md` (a short note on the interest-conflict extension) and
  the reviews' `STRESS-TEST-SCENARIOS.md` "Update after Sprint 9" note if it belongs there.
- `/home/rlg/relational-os/README.md` — keep the Documentation section pointing at the instances work.
- **Do NOT bump the spec version; keep v0.22.** Only a genuine normative change to `SPEC.md` would justify a
  minor bump (log it then).
- Write `sprints/sprint-10/summary.md` (what was built, verified commands/output, a rendered determination +
  appeal excerpt, design decisions incl. whether any new noun was added) and `sprints/sprint-10/notes/findings.md`
  (assumptions that broke, schema-enforcement surprises, decisions).

## Hand-off requirement
Your **final message** must summarize the conflicting-interest experiment (what was added, where it lives,
the verified build/conformance commands with real results, a rendered determination + appeal excerpt) and
point to `sprints/sprint-10/summary.md` and `/home/rlg/relational-os/instances/contested_reality/` (absolute
paths). Write the **next** sprint's self-contained prompt at `sprints/sprint-11/PROMPT.md` (a fresh session
depends on nothing else). This is a decision of whether the architecture earns the word *relational* for the
conflicting-interest case; if you conclude the architecture cannot yet represent it fully, say so plainly and
specify precisely what primitive/semantic is needed next — do not fake success.