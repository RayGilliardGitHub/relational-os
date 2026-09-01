# SPRINT 11 — PROMPT  (the optimizer/business-model gap: "what does 'better' mean?")

You are Hermes Agent in a **fresh session** with **NO memory** of prior conversation. Rely ONLY on the
files named here. Read before acting; do not guess or invent. **Every command you document MUST be run
and its real output captured** — never fabricate. This sprint closes the explicit honest gap that both
Sprint-9 and Sprint-10 left open and that `STRESS-TEST-SCENARIOS.md` names as architectural: the
**optimizer / business-model** that answers **"what does *better* mean here?"** — ranking the
adjudication options (side-employee / side-manager / remote-with-coverage-plan / do-nothing /
UNRESOLVED) from the organization's own constraints, evidence, and costs, so the human adjudicator's
choice (in the contested-reality and conflicting-interest experiments) can be **informed** by a computed
trade-off rather than authored from thin air. The determination stays the human's — the machine
*recommends* — contained by the §6 floor (Sprint-8 `agent_demo` pattern).

## Context — read first, in full
- Canonical spec (the contract): `/home/rlg/relational-os/SPEC.md` (v0.22)
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md`
- The experiments you extend (read FIRST for the pattern — this is an additive, engine-level extension):
  - `/home/rlg/relational-os/instances/contested_reality/run_dispute_demo.py` (Sprint 9: disputed fact,
    UNRESOLVED + Trust-safety) and `docs/CONTESTED-REALITY-EXPERIMENT.md`.
  - `/home/rlg/relational-os/instances/contested_reality/run_interest_conflict_demo.py` (Sprint 10:
    conflicting interest, shared constraint, appeal) and `docs/CONFLICTING-INTEREST-EXPERIMENT.md`.
  - `/home/rlg/relational-os/instances/contested_reality/conformance_dispute.py` and
    `conformance_interest.py` (the C1–C5 gates you fork).
  - `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` — the acceptance brief; Scenario B's
    gap #3 (resolve the SLA-vs-preference trade-off — no optimizer/business-model) is your target, and the
    Sprint-10 "remains" note names this exactly.
  - `/home/rlg/relational-os/instances/agent_demo/` (Sprint 8) — the proven pattern for a **real local
    model recommending via advisory `decision://`, contained by the §6 floor**, to reuse for the optional
    model-informed half.
- Project invariants & operational recipes: the `relational-os` skill (frozen ontology/URI cap; additive
  fields; single-threaded; plan-before-build; real output; ~$0 local; footguns incl. `Graph.get` one-arg,
  strict C5 state-machine tables, merge-not-replace, additive-key temporal-suffix trap, YAGNI on new nouns).

## What Sprint 11 IS and is NOT
- **IS:** a runnable, additive **trade-off / cost-benefit scoring engine** that, from a relationship's
  documented constraints (SLA target, staffing floor, leave balance, policy conditions, costs, evidence
  confidence), computes a **defensible ranking of the adjudication options** (`utility` per option +
  an explicit `do-nothing`/`UNRESOLVED` baseline), emits it as an advisory **`decision://`-adjacent
  artifact** (additive on existing primitives), and demonstrates the human adjudicator selecting an option
  WITH the computed trade-off in view (and, optionally, a real local model's recommendation also
  contained by the §6 floor). This makes the conflicting-interest/contested-reality determination
  **informed** by the org's own numbers.
- **IS NOT:** a new service, new schema, new URI noun, or a change to the frozen ontology (49 `$defs`,
  SPEC v0.22). No changing of how Trust updates (S5 stays deterministic). Nothing replaces the human
  adjudicator or bypasses the §6 floor.

## The target (what "done" looks like)
1. **A small additive scoring model** (pure local python, ~$0) computing a utility for each option in the
   conflicting-interest case from explicit inputs: SLA response target (30 min) + coverage floor (3) +
   on-site count per arrangement, employee leave balance, an irreversible/unknown-cost flag (→ floor),
   policy satisfaction, and a cost term. It must handle at least {side-employee, side-manager,
   remote-with-coverage-plan, do-nothing/UNRESOLVED} and rank them deterministically.
2. **The trade-off is emitted additively** (e.g. a `tradeoff` object on the `case://` or as a documented
   `recommendation://`-adjacent artifact — reuse the schema's `Recommendation` `$def` `by/for/options/
   includes_do_nothing/tradeoff/confidence` if it fits; if you believe a genuinely new noun is warranted,
   decide + document in `notes/findings.md`, never silently).
3. **Demonstrate the human adjudicator selecting WITH the ranking in view**: the chosen determination
   matches the top utility (or is an explicit, justifiable override), and the §6 floor still binds when an
   option is irreversible/unknown-cost.
4. **Optional (additive, ~$0, local):** a real local model (Ollama, `phi4-mini:3.8b-q8_0`) issues an
   **advisory** recommendation on which option it'd take, bounded by capability/delegation, forced to the
   §6 floor, never able to set the determination or Trust (mirror `agent_demo`, strict single-line-JSON
   prompt, `max_tokens>=2048`, parse + fallback-with-log, never fabricate a model answer).
5. **Every step signed and on the ledger;** the human's determination keeps the authority it requires (§7J.9).

## Mandatory rules
- **Write-first:** `sprints/sprint-11/plan.md` FIRST, then `work/1-plan.md` BEFORE building.
- **Real tool output only** on every documented command.
- **Additive, #new-noun-unless-documented, keep 49 `$defs` + URI cap + SPEC v0.22.** Do NOT touch `ros/`,
  the schema, the reference build, or the 12+ sector instances (re-verify them untouched).
- **Single-threaded** per PROTOCOL — no subagents.
- **Budget ~$0** — local, deterministic; a local model is optional-and-contained.
- **Raymond:** clean English, absolute `file://` paths, honest "stuck/failed" over fabricated success,
  report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (before you build): Sprint-10 `run_interest_conflict_demo.py` →
  `RESULT: ALL PASS`, and its `conformance_interest.py` → `ALL PASS`.
- The trade-off engine lives under `/home/rlg/relational-os/instances/contested_reality/` (add e.g.
  `tradeoff_model.py` + `run_tradeoff_demo.py`, sharing the Sprint-10/9 engine where useful), written big
  enough to be useful, opaque and small enough to be KISS.
- New assertions ALL PASS demonstrating: ranking includes do-nothing/UNRESOLVED; the determined option's
  utility is computed and consistent; §6 floor triggers on irreversible/unknown-cost; the advisory model
  (if used) cannot set the determination or Trust; authority/signature preserved.
- Non-regression (real): Sprint-9 + Sprint-10 demos + conformance; `instances/build_all.py` +
  `conformance_all.py`; S5 reference demo + conformance. All ALL PASS.

## Documentation (roll-forward)
- Add a `docs/TRADE-OFF-IMPLEMENTATION.md` (or extend the contest docs) with real output embedded.
- Update `instances/README.md`, the reviews' `STRESS-TEST-SCENARIOS.md` "Update after Sprint 11" note.
- Do NOT bump SPEC (v0.22) unless the model surfaces a genuine normative gap (log it then).
- Write `sprints/sprint-11/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize the trade-off engine (what was added, where it lives, verified
build/conformance commands with real results, a rendered ranking + the chosen determination, and an
honest note on whether the optimization actually improved defensibility or is still human-authored). Write
the **next** sprint's self-contained prompt at `sprints/sprint-12/PROMPT.md` (a fresh session depends on
nothing else). If you conclude the trade-off cannot be meaningfully computed from recorded data (i.e. the
ranking is still hand-authored), say so plainly and specify precisely what data/primitive is missing —
do not fake success.