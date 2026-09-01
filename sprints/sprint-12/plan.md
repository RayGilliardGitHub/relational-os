# SPRINT 12 — Contested Reality / Dispute Resolution: consolidated lifecycle spec + executable proof

## Why this sprint
The completeness review demanded the one decisive test: **"Does RelationalOS understand
disagreement?"** — not another document, but a **small executable proof** of the full contested
lifecycle under one roof. Sprints 9 (contested fact, UNRESOLVED), 10 (conflicting interest, appeal)
and 11 (trade-off/optimizer, AI containment, §6 floor) built the pieces incrementally. Sprint 12
consolidates them into a **single coherent lifecycle** — the review's wheel:

```
A-claim + B-claim → Evidence → Conflict detection → Uncertainty → Interests →
Obligations → Constraints → Available resolutions → Authorized adjudicator →
Recommendation → Human decision → Resolution → Outcome → Verification → Learning
```

It closes the genuine gaps the pieces left open: a **timestamp evidence-conflict reconciliation**
(GPS / contract deadline / receipt / supplier records), a **first-class lifecycle state machine**
(OPEN→…→CLOSED + APPEALED/REOPENED/ESCALATED/UNRESOLVED/SETTLED), **appeal → reopen → reassessment
→ new determination** without rewriting the ledger, the **error-vs-deception Trust taxonomy**, and an
**independent-auditor-reconstructable event sequence**. Then it renders the honest verdict.

## Design
- **Executable proof:** `instances/contested_reality/run_full_dispute.py` — one financial/customer
  dispute ($18,000) with four conflicting timestamp evidence items. It runs the ENTIRE lifecycle as
  real signed ledger events: provision → claims → evidence → conflict detection → uncertainty →
  epistemic status → dispute OPEN → interests/obligations/constraints → options + trade-off (reuse
  `tradeoff_model`) → advisory (machine + optional real model, contained) → authorized human
  determination (or UNRESOLVED when evidence insufficient) → outcome → verification → learning →
  appeal → reopen on new evidence → reassessment → new determination. All additive on the frozen
  $defs (Claim/Evidence/Dispute/Decision/Trust); no new noun, 49 $defs, SPEC v0.22.
- **Specification:** `instances/contested_reality/docs/DISPUTE-RESOLUTION-SPECIFICATION.md` —
  the full 16-section answer, ending with the Section-13 **sufficiency table** and the Section-16
  **final assessment** (honest: A / B / C), plus the skeptical "is this a new category?" verdict.
- **Trust taxonomy:** error vs deception kept distinct — an honest-but-overturned claim does not
  equate to untrustworthiness; only adequately-evidenced determinations move Trust (S5 stays
  deterministic). A deliberate-misrepresentation path is modelled where the architecture permits it.
- **Ledger:** every step signed, append-only; an independent auditor can reconstruct who said what,
  what evidence existed, what the system knew/didn't, what it recommended, who decided/authorized,
  what happened, whether verified, what was learned.

## Sub-sprints (sequential, single-threaded)
1. Plan + baseline (reference + S9/10/11 all green).
2. Build `run_full_dispute.py` (the lifecycle proof).
3. Conformance gate (`conformance_lifecycle.py`) C1–C5.
4. Write `DISPUTE-RESOLUTION-SPECIFICATION.md` (16 sections + §13 table + §16 assessment).
5. Non-regression + README/STRESS-TEST update, summary, findings, next-sprint prompt.

## Definition of Done (real output, exit 0)
- Green baseline before/after (build_all, conformance_all, S5, S9/10/11 demos + conformance).
- `run_full_dispute.py` → ALL PASS: contradictory claims+evidence preserved; uncertainty modelled;
  determination reachable AND UNRESOLVED reachable; AI cannot determine or bypass authority; a later
  determination reopens and reassesses without rewriting history; Trust error-vs-deception handled;
  the full chain is reconstructable from the ledger; authority/signature preserved.
- `conformance_lifecycle.py` → ALL PASS (C1–C5, 49 $defs, URI cap intact, SPEC v0.22).
- Spec document written with sufficiency table + an honest final assessment (no forced "revolutionary").

## Exit criteria
`run_full_dispute.py` + `conformance_lifecycle.py` exit 0; no schema/spec/`ros/`/sector instance
touched (re-verified); spec + summary + findings + next PROMPT written.