# SPRINT 12 — PROMPT  (the consolidated contested-reality lifecycle: spec + executable proof)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** This sprint answers the completeness review's decisive question — **"Does RelationalOS
understand disagreement?"** — with a **runnable proof**, not another document: consolidate the
Sprints 9–11 disputed-reality pieces into ONE coherent lifecycle over real signed ledger events and
write the corresponding specification.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). Read §3.13 (`dispute://`), §3.17
  (Claim/Evidence), §7J.9, §7K.1 (trade-off, organizational learning), and the §6 human floor in full.
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md`.
- The engine you consolidate (read ALL of these first — they already implement the pieces):
  - `/home/rlg/relational-os/instances/contested_reality/` — `run_dispute_demo.py` (Sprint 9:
    contested fact, UNRESOLVED, Trust-safe), `run_interest_conflict_demo.py` (Sprint 10: conflict of
    interest, appeal, authority), `tradeoff_model.py` + `run_tradeoff_demo.py` (Sprint 11: the
    optimizer / business-model, §6 floor, contained AI), and their `conformance_*.py` gates + the
    `docs/` (`CONTESTED-REALITY-EXPERIMENT.md`, `CONFLICTING-INTEREST-EXPERIMENT.md`,
    `TRADE-OFF-IMPLEMENTATION.md`).
  - The Sprint-8 AI-containment pattern: `/home/rlg/relational-os/instances/agent_demo/`
    (`run_agent_demo.py`, `agent_adapter.py`, `prompts/`).
  - The acceptance brief: `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` +
    `/home/rlg/relational-os/instances/contested_reality/docs/DISPUTE-RESOLUTION-SPECIFICATION.md`
    (the 16-section spec your sprint reproduces/runs).
- Project invariants & operational recipes: the `relational-os` skill (frozen ontology/URI cap;
  additive fields; single-threaded; plan-before-build; real output; ~$0; footguns incl. `Graph.get`
  one-arg, `evidence` refs are ARRAYS, strict C5 state-machine tables, merge-not-replace,
  additive-key temporal-suffix trap, C2 RFC3339 recursion, sibling subpackage self-anchoring, two
  interpreters — plain `python3` for demos, Sprint-0 venv
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance).

## The target (what "done" looks like)
1. **One consolidated lifecycle proof** under `instances/contested_reality/` (e.g. `run_full_dispute.py`
   + `conformance_lifecycle.py`) walking a single dispute through the WHOLE chain over real signed,
   append-only ledger events: 
   A-claim+B-claim → Evidence (with provenance/reliability/timestamps) → Conflict detection →
   Uncertainty → Epistemic status → Interests → Obligations → Constraints → Available resolutions
   (incl. do-nothing + settlement) → Authorized adjudicator → Recommendation (machine trade-off AND/
   OR a contained real local model) → Human decision → Resolution → Outcome → Verification → Learning,
   **plus** the adversarial branches the review demands:
   - **UNRESOLVED** as a valid, Trust-safe outcome (no forced winner; case stays OPEN; propagates).
   - **appeal → REOPEN on new evidence → reassessment → NEW determination**, history preserved, the
     original determination/evidence NOT rewritten (append-only).
   - **error-vs-deception Trust**: an overturned *honest* claim does not depress scoped Trust;
     incorrect ≠ untrustworthy; Trust moves only via the deterministic formula over adequately-evidenced
     determinations; the AI never writes Trust.
2. **Keep every distinction** — Event / Evidence / Claim / Inference / Determination / Decision /
   Outcome separate (they map to distinct `$defs` and/or additive fields; never collapse them).
3. **The AI is contained** (§6 + Sprint-8): it may retrieve/summarize/identify/hypothesize/recommend,
   recorded as an effect-free `decision://`; it CANNOT determine disputed facts, grant authority,
   approve its own recommendation, execute an irreversible action, erase evidence, or convert
   uncertainty into certainty.
4. **Auditor-reconstructable ledger**: every event signed with actor/authority/causation/correlation/
   timestamp/state_update; an independent auditor can rebuild who said what, what evidence existed,
   what the system knew/didn't, what it recommended, who decided/authorized, what happened, whether
   verified, what was learned.
5. A **specification document** (`docs/DISPUTE-RESOLUTION-SPECIFICATION.md` if absent, else extend) with
   the 16 sections — incl. the §13 **sufficiency table** (existing concept → additional semantics →
   new concept needed?) and an **honest §16 final assessment** (A/B/C + the skeptical "is this a new
   category vs an integration of CRM/ERP/ITSM/workflow/BI/AI?" verdict). Do NOT claim A if it isn't.

## Mandatory rules
- **Write-first:** `sprints/sprint-12/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only** on every documented command; honest "stuck/failed" over fabrication.
- **Additive, #new-noun-unless-documented, keep 49 `$defs` + URI cap + SPEC v0.22.** Re-verify `ros/`,
  the schema, the reference build, and the 12+ sector instances untouched.
- **Single-threaded** per PROTOCOL (no subagents). **Budget ~$0** — local/deterministic; the local
  model is optional-and-contained.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST: `run_full_dispute.py` (this sprint, if it exists) → ALL PASS and its
  conformance → ALL PASS; Sprint-11 `run_tradeoff_demo.py` + `conformance_tradeoff.py`; Sprint-10
  demo + conformance; Sprint-9 demo + conformance.
- New assertions ALL PASS covering: contradictory claims preserved; contradictory evidence preserved;
  uncertainty modelled; epistemic status tracked; a determination reachable; UNRESOLVED a valid +
  Trust-safe outcome; the AI cannot set the determination or Trust (or bypass authority); a wrong
  determination reopens and reassesses without rewriting history; error-vs-deception Trust kept
  distinct; authority (§7J.9) + §6 floor preserved; the chain is reconstructable from the ledger.
- Non-regression: `instances/build_all.py` + `conformance_all.py`; `agent_demo/run_agent_demo.py`;
  S5 reference demo + conformance. All ALL PASS.

## Documentation (roll-forward)
- Add `docs/DISPUTE-RESOLUTION-SPECIFICATION.md` (16 sections + §13 table + §16 assessment) with real
  output embedded.
- Update `instances/README.md`; append an "Update after Sprint 12" note to
  `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-12/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize the lifecycle proof (what was built, where, verified build/
conformance commands with real results, the rendered lifecycle + the honest verdict on whether
RelationalOS "understands disagreement") and flag precisely what generalization is missing (the
adjudication semantics are per-scenario authored, not a configurable engine). Write the **next**
sprint's self-contained prompt at `sprints/sprint-13/PROMPT.md` (generalize the adjudication engine +
render the trade-off/lifecycle on the §7L cockpit Q7 + the Sprint-11 Decision-Learning/realized-cost
weights item). A fresh session depends on nothing else.